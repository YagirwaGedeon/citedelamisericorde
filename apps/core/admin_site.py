"""Site d'administration personnalisé avec dashboard de statistiques (§21).

Indicateurs : visiteurs aujourd'hui, dons aujourd'hui, dons ce mois,
total des dons, donateurs, projets actifs, articles publiés, messages reçus,
plus l'évolution mensuelle des dons (graphique barres).
"""

from datetime import date, timedelta

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.db.models import Count, Sum
from django.urls import path, reverse_lazy
from django.utils import timezone

from apps.articles.models import Article
from apps.contact.models import ContactMessage
from apps.donations.models import Donation, Donor
from apps.projects.models import Project
from apps.analytics.models import PageView


class MisericordeAdminSite(admin.AdminSite):
    site_header = "Cité de la Miséricorde — Administration"
    site_title = "Cité de la Miséricorde"
    index_title = "Tableau de bord"
    enable_nav_sidebar = False

    def register(self, model_or_iterable, admin_class=None, **options):
        if admin_class is None:

            def _decorator(cls):
                super(MisericordeAdminSite, self).register(
                    model_or_iterable, admin_class=cls, **options
                )
                return cls

            return _decorator
        super().register(model_or_iterable, admin_class=admin_class, **options)
        return model_or_iterable

    def get_urls(self):
        urls = super().get_urls()
        catch_all = None
        for i, url in enumerate(urls):
            route = getattr(getattr(url, "pattern", None), "_regex", "")
            if getattr(url, "name", None) == "catch_all" or route == "(?P<url>.*)$":
                catch_all = urls.pop(i)
                break
        password_urls = [
            path(
                "password_reset/",
                auth_views.PasswordResetView.as_view(
                    template_name="registration/password_reset_form.html",
                    email_template_name="registration/password_reset_email.html",
                    subject_template_name="registration/password_reset_subject.txt",
                    success_url=reverse_lazy("admin:password_reset_done"),
                ),
                name="password_reset",
            ),
            path(
                "password_reset/done/",
                auth_views.PasswordResetDoneView.as_view(
                    template_name="registration/password_reset_done.html"
                ),
                name="password_reset_done",
            ),
            path(
                "reset/<uidb64>/<token>/",
                auth_views.PasswordResetConfirmView.as_view(
                    template_name="registration/password_reset_confirm.html",
                    success_url=reverse_lazy("admin:password_reset_complete"),
                ),
                name="password_reset_confirm",
            ),
            path(
                "reset/done/",
                auth_views.PasswordResetCompleteView.as_view(
                    template_name="registration/password_reset_complete.html"
                ),
                name="password_reset_complete",
            ),
        ]
        urls.extend(password_urls)
        if catch_all:
            urls.append(catch_all)
        return urls

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.dashboard_data())
        return super().index(request, extra_context=extra_context)

    @staticmethod
    def dashboard_data() -> dict:
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        month_start = today_start.replace(day=1)

        total_donations = (
            Donation.objects.filter(status="SUCCEEDED")
            .aggregate(total=Sum("amount"))["total"]
            or 0
        )

        # Évolution mensuelle des dons sur 6 mois (graphique)
        months = []
        values = []
        for i in range(5, -1, -1):
            first = (today_start - timedelta(days=30 * i)).replace(day=1)
            last = (first + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            total = (
                Donation.objects.filter(status="SUCCEEDED", paid_at__gte=first, paid_at__lte=last)
                .aggregate(t=Sum("amount"))["t"]
                or 0
            )
            months.append(first.strftime("%b %y"))
            values.append(float(total))

        # Répartition par passerelle (graphique horizontal)
        succeeded = Donation.objects.filter(status="SUCCEEDED").select_related("provider")
        provider_totals = {}
        for donation in succeeded:
            name = donation.provider.name if donation.provider else "—"
            entry = provider_totals.setdefault(name, {"count": 0, "total": 0.0})
            entry["count"] += 1
            entry["total"] += float(donation.amount or 0)
        provider_breakdown = [
            {"label": name, "count": data["count"], "total": data["total"]}
            for name, data in sorted(provider_totals.items(), key=lambda item: -item[1]["total"])
        ]

        # Répartition par région (pays des donateurs)
        region_totals = {}
        for donation in succeeded:
            country = (donation.donor.country or "—") if donation.donor else "—"
            entry = region_totals.setdefault(country, {"count": 0, "total": 0.0})
            entry["count"] += 1
            entry["total"] += float(donation.amount or 0)
        region_breakdown = [
            {"label": country, "count": data["count"], "total": data["total"]}
            for country, data in sorted(region_totals.items(), key=lambda item: -item[1]["total"])
        ]

        # Activité récente (10 derniers éléments de chaque type)
        def _recent_donations():
            rows = []
            for d in (
                Donation.objects.filter(status="SUCCEEDED")
                .select_related("donor", "project")
                .order_by("-paid_at")[:6]
            ):
                rows.append(
                    {
                        "reference": d.reference,
                        "amount": d.amount,
                        "currency": d.currency,
                        "donor": (d.donor.name or d.donor.email or "Anonyme") if d.donor else "Anonyme",
                        "paid_at": d.paid_at,
                    }
                )
            return rows

        def _recent_messages():
            rows = []
            for m in ContactMessage.objects.order_by("-created_at")[:6]:
                rows.append({"name": m.name, "email": m.email, "subject": m.subject, "created_at": m.created_at, "is_read": m.is_read})
            return rows

        def _recent_articles():
            rows = []
            for a in Article.objects.order_by("-published_at")[:6]:
                rows.append({"title": a.title, "published_at": a.published_at, "status": a.status, "slug": a.slug})
            return rows

        return {
            "dashboard": {
                "visitors_today": PageView.objects.filter(created_at__gte=today_start, is_bot=False).count(),
                "donations_today": Donation.objects.filter(created_at__gte=today_start).count(),
                "donations_month": Donation.objects.filter(created_at__gte=month_start).count(),
                "total_donations": float(total_donations),
                "donors_count": Donor.objects.count(),
                "active_projects": Project.objects.count(),
                "published_articles": Article.objects.filter(status="published").count(),
                "unread_messages": ContactMessage.objects.filter(is_read=False, is_spam=False).count(),
                "chart_months": months,
                "chart_values": values,
                "max_chart_value": max(values) if values else 1,
                "chart": list(zip(months, values)),
                "provider_breakdown": provider_breakdown,
                "region_breakdown": region_breakdown,
                "max_provider_count": max((b["count"] for b in provider_breakdown), default=1),
                "max_region_count": max((b["count"] for b in region_breakdown), default=1),
                "recent_donations": _recent_donations(),
                "recent_messages": _recent_messages(),
                "recent_articles": _recent_articles(),
            },
            "dashboard_kpis": [
                {"label": "Visiteurs aujourd'hui", "value": PageView.objects.filter(created_at__gte=today_start, is_bot=False).count()},
                {"label": "Dons aujourd'hui", "value": Donation.objects.filter(created_at__gte=today_start).count()},
                {"label": "Dons ce mois", "value": Donation.objects.filter(created_at__gte=month_start).count()},
                {"label": "Total des dons (USD)", "value": f"{float(total_donations):,.2f}".replace(",", " ").replace(".", ",")},
                {"label": "Donateurs", "value": Donor.objects.count()},
                {"label": "Projets", "value": Project.objects.count()},
                {"label": "Articles publiés", "value": Article.objects.filter(status="published").count()},
                {"label": "Messages non lus", "value": ContactMessage.objects.filter(is_read=False, is_spam=False).count()},
            ],
        }


admin_site = MisericordeAdminSite(name="admin")
