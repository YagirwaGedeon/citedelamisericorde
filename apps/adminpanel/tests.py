"""Tests de l'espace admin (7 points de vérification)."""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.adminpanel.models import HomePost
from apps.articles.models import Article
from apps.projects.models import Project

User = get_user_model()


@override_settings(ALLOWED_HOSTS=["*", "testserver", "localhost", "127.0.0.1"])
class AdminPanelTests(TestCase):
    """Valide connexion, routes protégées, CRUD et absence de secrets frontend."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="Manasse Kamole",
            password="Manasse2026",
            email="manasse@test.local",
            is_staff=True,
            is_superuser=True,
            role="superadmin",
        )

    def test_login_page_ok(self):
        r = self.client.get("/admin/login/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "csrfmiddlewaretoken")

    def test_protected_routes_redirect_anonymous(self):
        for path in (
            "/admin/",
            "/admin/dashboard/",
            "/admin/home/",
            "/admin/projects/",
            "/admin/news/",
            "/admin/media/",
            "/admin/profile/",
            "/admin/settings/",
            "/admin/analytics/",
            "/admin/bank_transfers/",
            "/admin/messages/",
            "/admin/messages/1/",
        ):
            r = self.client.get(path)
            self.assertEqual(r.status_code, 302, path)
            self.assertIn("/admin/login/", r["Location"], path)

    def test_wrong_password_rejected(self):
        r = self.client.post(
            "/admin/login/",
            {"username": "Manasse Kamole", "password": "wrong-password"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.wsgi_request.user.is_authenticated)

    def test_good_login_and_dashboard(self):
        ok = self.client.login(username="Manasse Kamole", password="Manasse2026")
        self.assertTrue(ok)
        r = self.client.get("/admin/dashboard/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Tableau de bord")

    def test_dashboard_quick_actions_and_advanced_panel(self):
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get("/admin/dashboard/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Nouvelle actualité")
        self.assertContains(r, "Nouveau projet")
        self.assertContains(r, "Publication accueil")
        self.assertContains(r, "Importer un média")
        self.assertContains(r, "Options avancées")
        self.assertContains(r, "Quitter l’option avancée")
        self.assertContains(r, 'id="advanced-panel"')
        self.assertContains(r, "btn-advanced-close")
        # Lien de sortie depuis l’admin Django avancée
        r = self.client.get("/django-admin/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Quitter l’option avancée")

    def test_analytics_page_and_sidebar(self):
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get("/admin/analytics/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Analytics")
        self.assertContains(r, "Articles les plus lus")
        self.assertContains(r, "Pays des visiteurs")
        self.assertContains(r, "Tendance des visites")
        self.assertContains(r, "chart-visits")
        self.assertContains(r, "chart-articles")
        self.assertContains(r, "chart-countries")
        self.assertContains(r, "chart.js")
        self.assertContains(r, 'class="nav-item is-active"')
        r = self.client.get("/admin/dashboard/")
        self.assertContains(r, "Analytics")

    def test_responsive_sidebar_controls(self):
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get("/admin/dashboard/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'id="admin-sidebar"')
        self.assertContains(r, 'id="sidebar-open"')
        self.assertContains(r, 'id="sidebar-close"')
        self.assertContains(r, 'id="sidebar-collapse"')
        self.assertContains(r, 'id="sidebar-expand"')
        self.assertContains(r, 'id="sidebar-toggle-desktop"')
        self.assertContains(r, "admin-sidebar is-open")
        self.assertContains(r, "sidebar-collapsed")
        # Contrôles sur les autres pages admin aussi
        for path in ("/admin/home/", "/admin/projects/", "/admin/news/", "/admin/media/"):
            r = self.client.get(path)
            self.assertContains(r, 'id="admin-sidebar"', html=False, count=None)

    def test_password_is_hashed_not_plaintext(self):
        user = User.objects.get(username="Manasse Kamole")
        self.assertNotIn("Manasse2026", user.password)
        self.assertTrue(user.check_password("Manasse2026"))

    def test_home_post_crud(self):
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.post(
            "/admin/home/create/",
            {
                "title": "Publication de test",
                "excerpt": "Extrait",
                "content": "<p>Contenu</p>",
                "image": "",
                "button_text": "Lire",
                "button_url": "/",
                "status": "published",
                "published_at": "2026-09-23T12:00",
                "order": "0",
            },
        )
        self.assertEqual(r.status_code, 302)
        post = HomePost.objects.get(title="Publication de test")
        self.assertEqual(post.status, "published")

        r = self.client.post(
            f"/admin/home/{post.pk}/edit/",
            {
                "title": "Publication modifiée",
                "excerpt": "",
                "content": "<p>OK</p>",
                "image": "",
                "button_text": "",
                "button_url": "",
                "status": "draft",
                "published_at": "2026-09-23T12:00",
                "order": "1",
            },
        )
        self.assertEqual(r.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.title, "Publication modifiée")
        self.assertEqual(post.status, "draft")

        r = self.client.post(f"/admin/home/{post.pk}/delete/")
        self.assertEqual(r.status_code, 302)
        self.assertFalse(HomePost.objects.filter(pk=post.pk).exists())

    def test_project_and_news_crud(self):
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.post(
            "/admin/projects/create/",
            {
                "title": "Projet de test",
                "program": "",
                "status": "",
                "location": "Bukavu",
                "context": "",
                "problem": "",
                "objectives": "",
                "beneficiaries": "",
                "activities": "",
                "results": "",
                "progress_percent": "10",
                "start_date": "",
                "end_date": "",
                "budget": "",
                "currency": "USD",
                "cover_image": "",
                "seo_description": "",
            },
        )
        self.assertEqual(r.status_code, 302)
        project = Project.objects.get(title="Projet de test")

        r = self.client.post(
            "/admin/news/create/",
            {
                "title": "Actu de test",
                "excerpt": "Extrait",
                "content": "<p>Corps</p>",
                "cover_image": "",
                "categories": [],
                "status": "published",
                "published_at": "2026-09-23T12:00",
            },
        )
        self.assertEqual(r.status_code, 302)
        article = Article.objects.get(title="Actu de test")

        r = self.client.post(f"/admin/projects/{project.pk}/delete/")
        self.assertEqual(r.status_code, 302)
        r = self.client.post(f"/admin/news/{article.pk}/delete/")
        self.assertEqual(r.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())
        self.assertFalse(Article.objects.filter(pk=article.pk).exists())

    def test_public_home_shows_published_home_posts(self):
        HomePost.objects.create(
            title="Pub accueil",
            content="Visible publiquement",
            status="published",
            order=0,
        )
        HomePost.objects.create(
            title="Brouillon caché",
            content="Ne doit pas apparaître",
            status="draft",
            order=1,
        )
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Pub accueil")
        self.assertNotContains(r, "Brouillon caché")

    def test_no_secret_in_frontend(self):
        r = self.client.get("/admin/login/")
        body = r.content.decode()
        self.assertNotIn("Manasse2026", body)
        self.assertNotIn("DJANGO_SECRET_KEY", body)
        r = self.client.get("/")
        body = r.content.decode()
        self.assertNotIn("Manasse2026", body)

    def test_profile_and_settings_pages(self):
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        self.assertEqual(self.client.get("/admin/profile/").status_code, 200)
        self.assertEqual(self.client.get("/admin/settings/").status_code, 200)
        self.assertEqual(self.client.get("/admin/media/").status_code, 200)
        self.assertEqual(self.client.get("/admin/projects/").status_code, 200)
        self.assertEqual(self.client.get("/admin/news/").status_code, 200)
        self.assertEqual(self.client.get("/admin/home/").status_code, 200)

    def test_urls_resolved(self):
        self.assertEqual(reverse("adminpanel:login"), "/admin/login/")
        self.assertEqual(reverse("adminpanel:dashboard"), "/admin/dashboard/")
        self.assertEqual(reverse("adminpanel:home_list"), "/admin/home/")
        self.assertEqual(reverse("adminpanel:projects_list"), "/admin/projects/")
        self.assertEqual(reverse("adminpanel:news_list"), "/admin/news/")
        self.assertEqual(reverse("adminpanel:media_list"), "/admin/media/")
        self.assertEqual(reverse("adminpanel:profile"), "/admin/profile/")
        self.assertEqual(reverse("adminpanel:settings"), "/admin/settings/")
        self.assertEqual(reverse("adminpanel:bank_transfers_list"), "/admin/bank_transfers/")

    def test_bank_transfers_list_and_sidebar(self):
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get("/admin/bank_transfers/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Virements bancaires")
        self.assertContains(r, "En attente")
        self.assertContains(r, "Vérifié")
        self.assertContains(r, 'class="nav-item is-active"')
        r = self.client.get("/admin/dashboard/")
        self.assertContains(r, "Virements")

    def test_bank_transfer_status_change(self):
        from decimal import Decimal

        from apps.donations.models import BankTransferConfirmation, Donation, Donor

        donor = Donor.objects.create(email="d@example.org", name="Donateur")
        donation = Donation.objects.create(
            donor=donor, amount=Decimal("50.00"), currency="USD", status="PROCESSING",
            idempotency_key="bt-test-1",
        )
        item = BankTransferConfirmation.objects.create(
            donation=donation,
            full_name="Donateur Test",
            email="d@example.org",
            country="France",
            amount=Decimal("50.00"),
            currency="USD",
            transfer_date="2026-09-20",
            transaction_reference="TRX-001",
            status="pending",
        )
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.post(
            f"/admin/bank_transfers/{item.pk}/status/",
            {"status": "verified", "admin_note": "Reçu confirmé"},
        )
        self.assertEqual(r.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.status, "verified")
        self.assertIsNotNone(item.reviewed_at)
        self.assertEqual(item.admin_note, "Reçu confirmé")
        donation.refresh_from_db()
        self.assertEqual(donation.status, "SUCCEEDED")

        r = self.client.post(
            f"/admin/bank_transfers/{item.pk}/status/",
            {"status": "invalid", "admin_note": ""},
        )
        self.assertEqual(r.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.status, "verified")

    def test_bank_transfer_proof_requires_staff(self):
        from django.core.files.base import ContentFile

        from apps.donations.models import BankTransferConfirmation

        item = BankTransferConfirmation.objects.create(
            full_name="Preuve",
            email="p@example.org",
            country="Canada",
            amount=10,
            currency="USD",
            transfer_date="2026-09-21",
            transaction_reference="TRX-P",
            status="pending",
        )
        item.proof.save("recu.pdf", ContentFile(b"%PDF-1.4 test"), save=True)

        # Anonyme → redirection login
        r = self.client.get(f"/admin/bank_transfers/{item.pk}/proof/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/admin/login/", r["Location"])

        # Staff → téléchargement
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get(f"/admin/bank_transfers/{item.pk}/proof/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("attachment", r.get("Content-Disposition", ""))

    def _make_message(self, **overrides):
        from apps.contact.models import ContactMessage

        data = {
            "name": "Visiteur Test",
            "email": "visiteur@example.org",
            "subject": "general",
            "message": "Bonjour, j'aimerais des informations sur vos projets.",
        }
        data.update(overrides)
        return ContactMessage.objects.create(**data)

    def test_messages_list_and_sidebar_badge(self):
        msg = self._make_message()
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get("/admin/messages/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Messages de contact")
        self.assertContains(r, "Visiteur Test")
        self.assertContains(r, "Non lus : 1")
        self.assertContains(r, 'class="nav-item is-active"')
        # Badge sidebar sur le dashboard
        r = self.client.get("/admin/dashboard/")
        self.assertContains(r, "Messages")
        # KPI cliquable vers la liste filtrée
        self.assertContains(r, "/admin/messages/?status=unread")

    def test_message_detail_marks_read_and_badge_decrements(self):
        msg = self._make_message()
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        # Avant lecture : badge = 1
        r = self.client.get("/admin/dashboard/")
        self.assertContains(r, "1 non lu")
        # Ouverture du détail → marqué lu automatiquement
        r = self.client.get(f"/admin/messages/{msg.pk}/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Visiteur Test")
        self.assertContains(r, "aimerais des informations")
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)
        self.assertIsNotNone(msg.read_at)
        # Après lecture : plus de badge non lu
        r = self.client.get("/admin/dashboard/")
        self.assertNotContains(r, "1 non lu")

    def test_message_toggle_read(self):
        msg = self._make_message()
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.post(f"/admin/messages/{msg.pk}/toggle-read/")
        self.assertEqual(r.status_code, 302)
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)
        r = self.client.post(f"/admin/messages/{msg.pk}/toggle-read/")
        self.assertEqual(r.status_code, 302)
        msg.refresh_from_db()
        self.assertFalse(msg.is_read)
        self.assertIsNone(msg.read_at)

    def test_messages_list_filters(self):
        self._make_message()
        self._make_message(name="Lu Exemple", email="lu@example.org", is_read=True)
        self._make_message(name="Spam Exemple", email="spam@example.org", is_spam=True)
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get("/admin/messages/?status=unread")
        self.assertContains(r, "Visiteur Test")
        self.assertNotContains(r, "Lu Exemple")
        r = self.client.get("/admin/messages/?status=spam")
        self.assertContains(r, "Spam Exemple")
        r = self.client.get("/admin/messages/?status=read")
        self.assertContains(r, "Lu Exemple")

    def test_dashboard_messages_items_are_links(self):
        msg = self._make_message()
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get("/admin/dashboard/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, f'/admin/messages/{msg.pk}/')

    def test_django_admin_badge_on_all_pages(self):
        from apps.contact.models import ContactMessage

        ContactMessage.objects.create(
            name="Badge Test", email="badge@example.org",
            subject="donation", message="Message badge.",
        )
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        for path in ("/django-admin/", "/django-admin/contact/contactmessage/"):
            r = self.client.get(path)
            self.assertEqual(r.status_code, 200, path)
            self.assertContains(r, "adm-notif-dot", msg_prefix=path)
            self.assertContains(r, "is_read__exact=0", msg_prefix=path)
