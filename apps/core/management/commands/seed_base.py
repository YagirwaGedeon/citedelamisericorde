"""Commande : python manage.py seed_base

Crée les données de base du site :
    - paramètres du site (SiteSettings)
    - les 4 programmes (§12)
    - les statuts de projets (En cours / Réalisé / Urgent / Planifié)
    - les pages CMS institutionnelles (à éditer ensuite dans l'admin)
    - les groupes de rôles (§22)
"""

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from apps.core.models import SiteSettings
from apps.pages.models import Page
from apps.programs.models import Program
from apps.projects.models import ProjectStatus


class Command(BaseCommand):
    help = "Crée les données de base (paramètres, programmes, statuts, pages, groupes)."

    def handle(self, *args, **options):
        # --- Paramètres du site ---
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            settings.organization_name = "Cité de la Miséricorde"
            settings.legal_name = "Cité de la Miséricorde"
            settings.tagline = "Heureux ceux qui procurent la paix"
            settings.email = "citedelamisericorde2024@gmail.com"
            settings.phone = "+243 970 884 579"
            settings.address_bukavu = "Bukavu, Commune d'Ibanda, Quartier Panzi, Sud-Kivu — RDC"
            settings.address_goma = "Goma, Nord-Kivu — RDC"
            settings.pwa_theme_color = "#0f766e"
            settings.donation_currency = "USD"
            settings.save()
            self.stdout.write("  + Paramètres du site créés")
        else:
            self.stdout.write("  = Paramètres du site déjà présents")

        # --- Programmes (§12) ---
        programs = [
            ("children", "Enfants vulnérables", "Assistance, protection et accompagnement des enfants orphelins et vulnérables."),
            ("women", "Autonomisation des femmes", "Formation, soutien socio-économique et autonomisation des femmes."),
            ("humanitarian", "Assistance humanitaire", "Réponse aux crises : nutrition, aide d'urgence, accompagnement des personnes affectées."),
            ("community", "Développement communautaire", "Développement communautaire, mobilisation des partenaires et de la société civile."),
        ]
        for domain, title, short in programs:
            obj, created = Program.objects.get_or_create(
                domain=domain, defaults={"title": title, "short_description": short, "is_active": True}
            )
            if created:
                self.stdout.write(f"  + Programme créé : {title}")

        # --- Statuts de projets ---
        statuses = [
            ("ongoing", "En cours", "#0d9488"),
            ("completed", "Réalisé", "#16a34a"),
            ("urgent", "Urgent", "#dc2626"),
            ("planned", "Planifié", "#f59e0b"),
        ]
        for code, name, color in statuses:
            obj, created = ProjectStatus.objects.get_or_create(
                code=code, defaults={"name": name, "color": color}
            )
            if created:
                self.stdout.write(f"  + Statut de projet créé : {name}")

        # --- Pages CMS ---
        pages = [
            ("a-propos", "À propos", "À propos de la Cité de la Miséricorde."),
            ("notre-histoire", "Notre histoire", "L'histoire de la Cité de la Miséricorde."),
            ("notre-mission", "Notre mission", "Notre mission humanitaire."),
            ("notre-vision", "Notre vision", "Notre vision pour les communautés."),
            ("nos-valeurs", "Nos valeurs", "Les valeurs qui guident notre action."),
            ("notre-equipe", "Notre équipe", "Les personnes engagées au service des bénéficiaires."),
        ]
        for slug, title, content in pages:
            obj, created = Page.objects.get_or_create(
                slug=slug,
                defaults={"title": title, "content": f"<p>{content}</p>", "status": "draft", "in_menu": True},
            )
            if created:
                self.stdout.write(f"  + Page CMS créée : {title} (brouillon)")

        # --- Groupes de rôles (§22) ---
        for group_name in [
            "Super Admin", "Administrateur", "Éditeur",
            "Gestionnaire de projets", "Gestionnaire financier", "Auteur",
        ]:
            Group.objects.get_or_create(name=group_name)

        # --- Passerelles de paiement (§18) ---
        from django.conf import settings

        from apps.payments.models import PaymentProvider

        providers = [
            ("stripe", "Stripe", False, 10,
             "Cartes bancaires internationales (USD, EUR)", "US,BE,FR,GB,KE,NG"),
            ("paypal", "PayPal", False, 20,
             "Compte PayPal (international)", "US,BE,FR,GB,KE,NG"),
            ("mobile_money", "Mobile Money (Flutterwave)", False, 30,
             "Airtel Money, M-Pesa, Orange Money (RDC)", "CD,KE,UG,TZ,RW"),
            ("sandbox", "Mode démo (sans paiement réel)", bool(settings.DEBUG), 99,
             "Simulation de paiement — développement uniquement", ""),
        ]
        for code, name, active, order, description, countries in providers:
            obj, created = PaymentProvider.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "is_active": active,
                    "display_order": order,
                    "description": description,
                    "supported_countries": countries,
                },
            )
            if created:
                self.stdout.write(f"  + Passerelle créée : {name} (active={active})")

        self.stdout.write(self.style.SUCCESS("Seed terminé."))