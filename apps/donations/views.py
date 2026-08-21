"""Vues de don : formulaire, choix de la passerelle et lancement du paiement (§18–19).

Étape 10 : le paiement est exécuté par les passerelles de ``apps.payments``.
Aucune donnée bancaire n'est collectée ou stockée ici.
"""

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from apps.donations.forms import DonationForm
from apps.donations.models import Donation, Donor
from apps.payments.models import PaymentProvider, PaymentTransaction
from apps.payments.receipts import generate_receipt, send_thank_you_email
from apps.payments.services import PaymentServiceError, get_provider, settle_transaction
from apps.projects.models import Project


def donation_create(request):
    preset_amounts = [10, 20, 50, 100]
    active_providers = PaymentProvider.objects.filter(is_active=True).order_by("display_order")
    projects = Project.objects.filter(needs_donation=True)

    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            is_anonymous = data.get("is_anonymous", False)
            donor, _ = Donor.objects.get_or_create(
                email=data.get("email") or "",
                defaults={
                    "name": "" if is_anonymous else data.get("name", ""),
                    "phone": data.get("phone", ""),
                    "country": data.get("country", ""),
                    "is_anonymous": is_anonymous,
                },
            )
            donation = Donation.objects.create(
                donor=donor,
                project=data.get("project"),
                amount=data["amount"],
                currency=data.get("currency", "USD"),
                frequency=data.get("frequency", "once"),
                status="PENDING",
                is_anonymous=is_anonymous,
                donor_message=data.get("message", ""),
                idempotency_key=f"{request.session.session_key or 'anon'}-{timezone.now().timestamp()}",
            )
            return redirect(reverse("donations:checkout", kwargs={"pk": donation.pk}))
    else:
        form = DonationForm()

    return render(
        request,
        "donations/create.html",
        {
            "form": form,
            "preset_amounts": preset_amounts,
            "active_providers": active_providers,
            "projects": projects,
        },
    )


def donation_checkout(request, pk):
    """Écran de choix de la passerelle de paiement."""
    donation = get_object_or_404(Donation, pk=pk)
    if donation.status != "PENDING":
        if donation.status == "SUCCEEDED":
            return redirect("donations:success", pk=donation.pk)
        return redirect("donations:cancelled", pk=donation.pk)
    providers = PaymentProvider.objects.filter(is_active=True).order_by("display_order")
    return render(
        request,
        "donations/checkout.html",
        {"donation": donation, "providers": providers},
    )


def donation_pay(request, pk, provider_code):
    """Crée la transaction et redirige vers la passerelle (ou règle en sandbox)."""
    donation = get_object_or_404(Donation, pk=pk)
    if donation.status != "PENDING":
        return redirect("donations:checkout", pk=donation.pk)
    provider_model = get_object_or_404(PaymentProvider, code=provider_code, is_active=True)
    try:
        provider = get_provider(provider_code)
    except PaymentServiceError:
        return redirect("donations:checkout", pk=donation.pk)
    if not provider.is_configured() and provider_code != "sandbox":
        return redirect("donations:checkout", pk=donation.pk)

    txn = PaymentTransaction.objects.create(
        donation=donation,
        provider=provider_model,
        amount=donation.amount,
        currency=donation.currency,
        status="PENDING",
    )
    try:
        result = provider.start_checkout(donation, txn)
    except PaymentServiceError as exc:
        txn.status = "FAILED"
        txn.error_message = str(exc)
        txn.save(update_fields=["status", "error_message", "updated_at"])
        donation.status = "FAILED"
        donation.save(update_fields=["status", "updated_at"])
        return redirect("donations:cancelled", pk=donation.pk)

    # Le sandbox règle immédiatement la transaction (status SUCCEEDED) :
    # ne pas repasser en PROCESSING dans ce cas.
    if donation.status != "SUCCEEDED":
        txn.provider_transaction_id = result.provider_reference
        txn.status = "PROCESSING"
        txn.attempted_at = timezone.now()
        txn.save(update_fields=["provider_transaction_id", "status", "attempted_at", "updated_at"])
        donation.status = "PROCESSING"
        donation.provider = provider_model
        donation.save(update_fields=["status", "provider", "updated_at"])

    if result.redirect_url:
        return redirect(result.redirect_url)
    if donation.status == "SUCCEEDED":
        return redirect("donations:success", pk=donation.pk)
    return redirect("donations:cancelled", pk=donation.pk)


def donation_success(request, pk):
    """Page de confirmation après paiement réussi."""
    donation = get_object_or_404(Donation, pk=pk)
    if donation.status == "SUCCEEDED":
        generate_receipt(donation)
        if not donation.receipt_sent_at:
            send_thank_you_email(donation)
    return render(request, "donations/success.html", {"donation": donation})


def donation_reception(request):
    """Page « Système de réception des dons » : virements, transferts, mobile money, dons en nature, Canada."""
    return render(request, "donations/reception.html", {})


def donation_cancelled(request, pk):
    """Page d'annulation / échec de paiement."""
    donation = get_object_or_404(Donation, pk=pk)
    return render(request, "donations/cancelled.html", {"donation": donation})
