"""Vues de don : formulaire, choix de la passerelle et lancement du paiement (§18–19).

Étape 10 : le paiement est exécuté par les passerelles de ``apps.payments``.
Aucune donnée bancaire n'est collectée ou stockée ici (hormis confirmation de virement).
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from apps.donations.forms import BankTransferConfirmForm, DonationForm
from apps.donations.models import BankTransferConfirmation, Donation, Donor
from apps.payments.models import PaymentProvider, PaymentTransaction
from apps.payments.receipts import generate_receipt, send_thank_you_email
from apps.payments.services import PaymentServiceError, get_provider, settle_transaction
from apps.projects.models import Project

# Coordonnées bancaires internationales (affichées publiquement — pas de secret).
BANK_TRANSFER_DETAILS = {
    "beneficiary": "ORPHELINAT CJPD",
    "bank": "EQUITY BANK SA",
    "account_number": "00011-05040-02000422389-82",
    "currency": "USD",
    "swift_beneficiary": "BCDCCDKI",
    "swift_international": "CITIUS33",
}


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


# ---------------------------------------------------------------- Virement bancaire
def donation_bank_transfer(request, pk=None):
    """Coordonnées bancaires + formulaire de confirmation du virement."""
    donation = None
    if pk is not None:
        donation = get_object_or_404(Donation, pk=pk)

    bank = BANK_TRANSFER_DETAILS
    show_form = request.GET.get("confirmer") == "1" or request.method == "POST"
    confirmation_sent = False

    initial = {}
    if donation is not None:
        initial["amount"] = donation.amount
        initial["currency"] = donation.currency
        if donation.donor_id and donation.donor.email:
            initial["email"] = donation.donor.email
        if donation.donor_id and donation.donor.country:
            initial.setdefault("country", donation.donor.country)

    form = BankTransferConfirmForm(
        request.POST or None, request.FILES or None, initial=initial
    )

    if request.method == "POST" and form.is_valid():
        confirmation = form.save(commit=False)
        if donation is not None:
            confirmation.donation = donation
            if not confirmation.amount:
                confirmation.amount = donation.amount
            if not confirmation.currency:
                confirmation.currency = donation.currency
        confirmation.save()
        if donation is not None and donation.status == "PENDING":
            donation.status = "PROCESSING"
            donation.provider_reference = confirmation.transaction_reference
            donation.save(update_fields=["status", "provider_reference", "updated_at"])
        confirmation_sent = True
        show_form = False
        form = BankTransferConfirmForm()
        messages.success(
            request,
            "Votre confirmation a bien été reçue. L’équipe de l’ORPHELINAT CJPD "
            "la vérifiera dans les plus brefs délais.",
        )

    return render(
        request,
        "donations/bank_transfer.html",
        {
            "bank": bank,
            "donation": donation,
            "form": form,
            "show_form": show_form,
            "confirmation_sent": confirmation_sent,
            "page_title": "Virement bancaire",
        },
    )


def donation_bank_transfer_confirm(request, pk):
    """Raccourci : même page pré-associée au don."""
    return donation_bank_transfer(request, pk=pk)
