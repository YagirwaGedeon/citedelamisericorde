from django.urls import path

from apps.payments.views import provider_return, webhook

app_name = "payments"

urlpatterns = [
    path("webhook/<str:provider_code>/", webhook, name="webhook"),
    path("retour/<str:provider_code>/", provider_return, name="return"),
]
