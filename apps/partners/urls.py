from django.urls import path

from apps.partners.views import partner_list

urlpatterns = [
    path("", partner_list, name="list"),
]
