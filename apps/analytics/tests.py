"""Tests analytics : tracking middleware + page /admin/analytics/."""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.analytics.geo import country_from_accept_language
from apps.analytics.middleware import AnalyticsMiddleware, _is_bot
from apps.analytics.models import PageView
from apps.articles.models import Article
from apps.projects.models import Project

User = get_user_model()


class GeoTests(TestCase):
    def test_accept_language_region(self):
        self.assertEqual(country_from_accept_language("fr-CD,fr;q=0.9,en;q=0.8"), "RD Congo")
        self.assertEqual(country_from_accept_language("en-US,en;q=0.9"), "États-Unis")
        self.assertEqual(country_from_accept_language("fr-FR,fr;q=0.9"), "France")
        self.assertEqual(country_from_accept_language("sw-KE"), "Kenya")

    def test_accept_language_lang_only(self):
        self.assertEqual(country_from_accept_language("fr"), "France")
        self.assertEqual(country_from_accept_language("sw"), "Afrique de l’Est")
        self.assertEqual(country_from_accept_language(""), "")
        self.assertEqual(country_from_accept_language(None), "")

    def test_bot_detection(self):
        self.assertTrue(_is_bot("Mozilla/5.0 (compatible; Googlebot/2.1)"))
        self.assertTrue(_is_bot(""))
        self.assertFalse(_is_bot("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"))


@override_settings(ALLOWED_HOSTS=["*", "testserver", "localhost", "127.0.0.1"])
class TrackingMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client(
            HTTP_USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
            HTTP_ACCEPT_LANGUAGE="fr-CD,fr;q=0.9",
        )

    def test_public_page_creates_pageview_with_country(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(PageView.objects.filter(path="/").exists())
        pv = PageView.objects.filter(path="/").first()
        self.assertEqual(pv.country, "RD Congo")
        self.assertFalse(pv.is_bot)
        self.assertTrue(pv.visitor_key)

    def test_bot_not_tracked(self):
        c = Client(HTTP_USER_AGENT="Mozilla/5.0 (compatible; Googlebot/2.1 +http://www.google.com/bot.html)")
        c.get("/")
        self.assertEqual(PageView.objects.count(), 0)

    def test_admin_paths_not_tracked(self):
        self.client.get("/admin/login/")
        self.assertFalse(PageView.objects.filter(path__startswith="/admin/").exists())

    def test_staff_visits_not_tracked(self):
        User.objects.create_user(
            username="staffx", password="x", is_staff=True, role="admin",
        )
        self.client.login(username="staffx", password="x")
        self.client.get("/")
        # staff non tracké
        self.assertEqual(PageView.objects.filter(path="/").count(), 0)


@override_settings(ALLOWED_HOSTS=["*", "testserver", "localhost", "127.0.0.1"])
class AnalyticsAdminPageTests(TestCase):
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
        cls.article = Article.objects.create(
            title="Article test lu",
            content="<p>Contenu</p>",
            status="published",
            author=cls.admin,
            views=42,
        )
        cls.project = Project.objects.create(
            title="Projet test",
            views=17,
            publication_authorized=True,
        )
        now = timezone.now()
        for i, (path, country) in enumerate(
            [
                ("/actualites/article-test-lu/", "RD Congo"),
                ("/actualites/article-test-lu/", "France"),
                ("/projets/projet-test/", "RD Congo"),
                ("/", "Kenya"),
                ("/actualites/", "RD Congo"),
            ]
        ):
            PageView.objects.create(
                path=path,
                country=country,
                is_bot=False,
                visitor_key=f"vk{i}",
                created_at=now,
            )

    def test_analytics_requires_login(self):
        r = self.client.get("/admin/analytics/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/admin/login/", r["Location"])

    def test_analytics_page_ok_with_charts(self):
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get("/admin/analytics/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Analytics")
        self.assertContains(r, "Chart")
        self.assertContains(r, "Articles les plus lus")
        self.assertContains(r, "Pays des visiteurs")
        self.assertContains(r, "Article test lu")
        self.assertContains(r, "RD Congo")
        self.assertContains(r, 'id="chart-visits"')
        self.assertContains(r, 'id="chart-articles"')
        self.assertContains(r, 'id="chart-countries"')
        self.assertContains(r, 'id="chart-pages"')
        self.assertContains(r, 'class="nav-item is-active"')

    def test_sidebar_has_analytics_link(self):
        self.client.login(username="Manasse Kamole", password="Manasse2026")
        r = self.client.get("/admin/dashboard/")
        self.assertContains(r, "Analytics")

    def test_article_and_project_view_counters(self):
        self.client.get(f"/actualites/{self.article.slug}/")
        self.article.refresh_from_db()
        self.assertEqual(self.article.views, 43)

        self.client.get(f"/projets/{self.project.slug}/")
        self.project.refresh_from_db()
        self.assertEqual(self.project.views, 18)

    def test_url_resolves(self):
        self.assertEqual(reverse("adminpanel:analytics"), "/admin/analytics/")
