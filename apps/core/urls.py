"""URLs du socle."""

from django.urls import path

from apps.core.views import robots_txt

urlpatterns = [
    path("robots.txt", robots_txt, name="robots"),
]
