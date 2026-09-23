"""Routes principales du projet Cité de la Miséricorde."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.core.admin_site import admin_site
from apps.core.sitemaps import ArticleSitemap, CoreSitemap, PageSitemap, ProjectSitemap
from apps.core.views import home, offline_view, robots_txt, service_worker

sitemaps = {
    "core": CoreSitemap,
    "articles": ArticleSitemap,
    "projets": ProjectSitemap,
    "pages": PageSitemap,
}

urlpatterns = [
    path("", home, name="home"),
    # Espace admin principal (panel personnalisé)
    path("admin/", include(("apps.adminpanel.urls", "adminpanel"))),
    # Admin Django classique (accès secondaire)
    path("django-admin/", admin_site.urls),
    path("offline/", offline_view, name="offline"),
    path("sw.js", service_worker, name="service_worker"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots"),
    path("i18n/", include("django.conf.urls.i18n")),  # set_language (sélecteur de langue)
    # apps
    path("", include(("apps.pages.urls", "pages"))),
    path("actualites/", include(("apps.articles.urls", "articles"))),
    path("programmes/", include(("apps.programs.urls", "programs"))),
    path("projets/", include(("apps.projects.urls", "projects"))),
    path("dons/", include(("apps.donations.urls", "donations"))),
    path("payments/", include(("apps.payments.urls", "payments"))),
    path("galerie/", include(("apps.gallery.urls", "gallery"))),
    path("temoignages/", include(("apps.testimonials.urls", "testimonials"))),
    path("partenaires/", include(("apps.partners.urls", "partners"))),
    path("impact/", include(("apps.statistics.urls", "statistics"))),
    path("newsletter/", include(("apps.newsletter.urls", "newsletter"))),
    path("contact/", include(("apps.contact.urls", "contact"))),
    path("migration/", include(("apps.migration.urls", "migration"))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin_site.site_header = "Cité de la Miséricorde — Administration"
admin_site.site_title = "Cité de la Miséricorde"
admin_site.index_title = "Tableau de bord"
