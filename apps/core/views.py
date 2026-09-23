"""Vues du socle : accueil, page hors-ligne PWA, robots.txt."""

import re
from pathlib import Path

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from apps.adminpanel.models import HomePost
from apps.articles.models import Article
from apps.pages.models import Page
from apps.partners.models import Partner
from apps.programs.models import Program
from apps.projects.models import Project
from apps.statistics.models import Statistic
from apps.testimonials.models import Testimonial


def _founder_section():
    """Extrait le « Mot du fondateur » depuis la page histoire (contenu importé)."""
    page = Page.objects.filter(slug="notre-histoire", status="published").first()
    if page is None:
        return None
    text = re.sub(r"<[^>]+>", " ", page.content or "")
    text = re.sub(r"\s+", " ", text).strip()
    image_srcs = re.findall(r'src="([^"]+)"', page.content or "")
    return {
        "page": page,
        "excerpt": text[:350] + ("…" if len(text) > 350 else ""),
        "image": image_srcs[0] if image_srcs else "",
    }


def home(request):
    """Page d'accueil (§12–16)."""
    try:
        home_posts = list(
            HomePost.objects.filter(
                status="published", published_at__lte=timezone.now()
            ).select_related("image")[:6]
        )
    except Exception:
        # Table absente (migration non encore appliquée) : ne jamais casser l'accueil.
        home_posts = []
    context = {
        "programs": Program.objects.filter(is_active=True)[:4],
        "featured_projects": Project.objects.select_related("status").filter(is_featured=True)[:3],
        "latest_articles": Article.objects.filter(
            Q(status="published") & Q(published_at__lte=timezone.now())
        )[:3],
        "impact_statistics": Statistic.objects.filter(is_published=True)[:4],
        "testimonials": Testimonial.objects.filter(is_published=True, publication_authorized=True)[:3],
        "partners": Partner.objects.filter(is_published=True)[:6],
        "founder": _founder_section(),
        "home_posts": home_posts,
    }
    return render(request, "core/home.html", context)


def offline_view(request):
    """Page hors-ligne affichée par le service worker (§25)."""
    return render(request, "core/offline.html", status=200)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /django-admin/",
        "Allow: /",
        "",
        "Sitemap: {scheme}://{host}/sitemap.xml".format(
            scheme=request.scheme, host=request.get_host()
        ),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def service_worker(request):
    """Sert le service worker à la racine pour couvrir tout le site (§25 PWA)."""
    path = Path(settings.BASE_DIR) / "static" / "service-worker.js"
    return HttpResponse(path.read_bytes(), content_type="application/javascript")
