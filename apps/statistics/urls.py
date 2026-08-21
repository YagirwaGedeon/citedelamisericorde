from django.urls import path

from apps.statistics.views import impact_list

urlpatterns = [
    path("", impact_list, name="list"),
]
