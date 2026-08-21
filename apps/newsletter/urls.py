from django.urls import path

from apps.newsletter.views import confirm, subscribe, unsubscribe

urlpatterns = [
    path("inscription/", subscribe, name="subscribe"),
    path("confirmation/<str:token>/", confirm, name="confirm"),
    path("desinscription/<str:token>/", unsubscribe, name="unsubscribe"),
]
