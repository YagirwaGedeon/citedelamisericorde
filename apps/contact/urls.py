from django.urls import path

from apps.contact.views import contact_create, contact_success

urlpatterns = [
    path("", contact_create, name="create"),
    path("merci/", contact_success, name="success"),
]
