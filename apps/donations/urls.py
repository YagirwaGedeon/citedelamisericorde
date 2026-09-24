from django.urls import path

app_name = "donations"

from apps.donations.views import (
    donation_bank_transfer,
    donation_bank_transfer_confirm,
    donation_cancelled,
    donation_checkout,
    donation_create,
    donation_pay,
    donation_reception,
    donation_success,
)

urlpatterns = [
    path("faire-un-don/", donation_create, name="create"),
    path("reception-des-dons/", donation_reception, name="reception"),
    path("virement-bancaire/", donation_bank_transfer, name="bank_transfer"),
    path("virement-bancaire/<int:pk>/", donation_bank_transfer_confirm, name="bank_transfer_donation"),
    path("checkout/<int:pk>/", donation_checkout, name="checkout"),
    path("payer/<int:pk>/<str:provider_code>/", donation_pay, name="pay"),
    path("succes/<int:pk>/", donation_success, name="success"),
    path("annulation/<int:pk>/", donation_cancelled, name="cancelled"),
]
