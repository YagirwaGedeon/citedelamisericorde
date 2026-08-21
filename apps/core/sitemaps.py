"""Sitemaps (§27)."""

from django.contrib.sitemaps import Sitemap
from django.db.models import Q
from django.utils import timezone

from apps.articles.models import Article
from apps.pages.models import Page
from apps.projects.models import Project


class CoreSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            {"location": "/", "lastmod": timezone.now()},
            {"location": "/a-propos/", "lastmod": timezone.now()},
            {"location": "/notre-histoire/", "lastmod": timezone.now()},
            {"location": "/notre-mission/", "lastmod": timezone.now()},
            {"location": "/notre-vision/", "lastmod": timezone.now()},
            {"location": "/nos-valeurs/", "lastmod": timezone.now()},
            {"location": "/notre-equipe/", "lastmod": timezone.now()},
            {"location": "/programmes/", "lastmod": timezone.now()},
            {"location": "/projets/", "lastmod": timezone.now()},
            {"location": "/impact/", "lastmod": timezone.now()},
            {"location": "/actualites/", "lastmod": timezone.now()},
            {"location": "/galerie/", "lastmod": timezone.now()},
            {"location": "/partenaires/", "lastmod": timezone.now()},
            {"location": "/dons/faire-un-don/", "lastmod": timezone.now()},
            {"location": "/dons/reception-des-dons/", "lastmod": timezone.now()},
            {"location": "/contact/", "lastmod": timezone.now()},
        ]

    def location(self, item):
        return item["location"]

    def lastmod(self, item):
        return item["lastmod"]


class ArticleSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Article.objects.filter(
            Q(status="published") & Q(published_at__lte=timezone.now())
        )

    def location(self, obj):
        return f"/actualites/{obj.slug}/"

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return f"/projets/{obj.slug}/"

    def lastmod(self, obj):
        return obj.updated_at


class PageSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Page.objects.filter(status="published")

    def location(self, obj):
        return f"/page/{obj.slug}/"
