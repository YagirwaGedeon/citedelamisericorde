"""Étape 10 — Webhooks de paiement et retours fournisseur (§19).

Les webhooks sont exempts de CSRF (appelés par les serveurs des
passerelles) et vérifient systématiquement la signature avant tout
règlement de transaction.
"""

import json
import logging

from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.payments.models import PaymentTransaction
from apps.payments.receipts import generate_receipt, send_thank_you_email
from apps.payments.services import PaymentServiceError, get_provider, process_webhook, settle_transaction

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
@csrf_exempt
def webhook(request, provider_code: str):
    """Point d'entrée des événements des passerelles (signature obligatoire)."""
    if not request.body:
        return JsonResponse({"status": "ignored", "reason": "empty"}, status=200)
    try:
        result = process_webhook(request, provider_code)
    except PaymentServiceError as exc:
        logger.warning("Webhook %s rejeté : %s", provider_code, exc)
        return JsonResponse({"status": "rejected", "reason": str(exc)}, status=400)
    except Exception as exc:  # pragma: no cover — filet de sécurité
        logger.error("Webhook %s : erreur interne %s", provider_code, exc)
        return JsonResponse({"status": "error"}, status=500)
    return JsonResponse(
        {"status": "ok" if result.ok else "ignored", "event": result.event_type, "ok": result.ok},
        status=200,
    )


@require_http_methods(["GET"])
@csrf_exempt
def provider_return(request, provider_code: str):
    """Retour du donateur depuis la passerelle (capture PayPal, vérif. Flutterwave).

    En cas de succès : redirection vers la page de succès ; sinon annulation.
    """
    provider = get_provider(provider_code)
    try:
        result = provider.handle_return(request)
    except PaymentServiceError as exc:
        logger.warning("Retour %s : %s", provider_code, exc)
        result = None
    reference = provider_result_reference(request, provider_code)
    donation = None
    if reference:
        txn = _resolve_transaction(provider_code, reference)
        if txn:
            donation = txn.donation
            if result is not None and result.ok:
                settle_transaction(txn, result.succeeded, event_type=result.event_type, error=result.error)
            pk = donation.pk
        else:
            pk = request.GET.get("donation") or request.GET.get("client_reference_id") or 0
    else:
        pk = request.GET.get("donation") or request.GET.get("client_reference_id") or 0

    if pk:
        from apps.donations.models import Donation

        donation = Donation.objects.filter(pk=pk).first()
    if donation and donation.status == "SUCCEEDED":
        generate_receipt(donation)
        if not donation.receipt_sent_at:
            send_thank_you_email(donation)
        return redirect("donations:success", pk=donation.pk)
    return redirect("donations:cancelled", pk=pk or 0)


def provider_result_reference(request, provider_code: str) -> str:
    if provider_code == "paypal":
        return request.GET.get("token", "")
    if provider_code == "mobile_money":
        return request.GET.get("tx_ref", "")
    return ""


def _resolve_transaction(provider_code: str, reference: str) -> PaymentTransaction | None:
    if provider_code == "mobile_money":
        parts = reference.split("-")
        if len(parts) >= 2 and parts[0] == "CMD":
            return PaymentTransaction.objects.filter(pk=parts[1]).first()
        return None
    return PaymentTransaction.objects.filter(provider_transaction_id=reference).first()
