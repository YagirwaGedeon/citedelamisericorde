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
