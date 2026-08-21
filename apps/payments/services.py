"""Étape 10 — Passerelles de paiement (Stripe, PayPal, Mobile Money, Sandbox).

Interface commune ``PaymentProviderInterface`` :
    - ``start_checkout(donation, txn)`` → CheckoutResult (URL de redirection)
    - ``verify_webhook(request)`` → WebhookResult (signature vérifiée)
    - ``handle_return(request)`` → confirmation côté fournisseur (retour navigateur)

Garanties exigées par le cahier des charges (§18–19) :
    - aucune donnée bancaire stockée ;
    - vérification systématique des signatures de webhooks ;
    - idempotence et anti-double-paiement (``settle_transaction``) ;
    - clés secrètes uniquement via l'environnement, jamais journalisées.

``SandboxProvider`` : simulateur de paiement pour le développement
(aucun réseau), utilisé quand aucune passerelle n'est configurée.
"""

import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass, field
from decimal import Decimal

from django.conf import settings
from django.db import transaction as db_transaction
from django.utils import timezone

from apps.payments.models import PaymentTransaction, WebhookEvent

try:  # SDK optionnel : utilisé uniquement par StripeProvider
    import stripe as _stripe
except ImportError:  # pragma: no cover
    _stripe = None


class PaymentServiceError(RuntimeError):
    """Erreur de création ou de traitement d'un paiement."""


@dataclass
class CheckoutResult:
    redirect_url: str
    provider_reference: str = ""


@dataclass
class WebhookResult:
    ok: bool
    event_type: str = ""
    provider_reference: str = ""
    succeeded: bool = False
    error: str = ""


def settle_transaction(txn: PaymentTransaction, succeeded: bool, event_type: str = "", error: str = "") -> bool:
    """Applique l'issue d'un paiement à la transaction et au don.

    Idempotent : un événement déjà traité (SUCCEEDED / REFUNDED) est ignoré —
    garantie anti-double-paiement (§19). Retourne True si un changement a eu lieu.
    """
    if txn.status in ("SUCCEEDED", "REFUNDED"):
        return False
    donation = txn.donation
    with db_transaction.atomic():
        if succeeded:
            txn.status = "SUCCEEDED"
            txn.succeeded_at = timezone.now()
            if donation.status != "SUCCEEDED":
                donation.status = "SUCCEEDED"
                donation.paid_at = timezone.now()
                donation.provider_reference = txn.provider_transaction_id
                donation.provider = txn.provider
                donation.save(update_fields=["status", "paid_at", "provider_reference", "provider", "updated_at"])
        else:
            txn.status = "FAILED"
            txn.error_message = error or event_type
            if donation.status == "PENDING" or donation.status == "PROCESSING":
                donation.status = "FAILED"
                donation.save(update_fields=["status", "updated_at"])
        txn.save(update_fields=["status", "succeeded_at", "error_message", "updated_at"])
    return True


class BaseProvider:
    """Interface commune des passerelles."""

    code = ""
    label = ""

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def is_configured(self) -> bool:
        """La passerelle peut-elle être utilisée (clés présentes) ?"""
        return False

    def start_checkout(self, donation, txn: PaymentTransaction) -> CheckoutResult:
        raise NotImplementedError

    def verify_webhook(self, request) -> WebhookResult:
        raise NotImplementedError

    def handle_return(self, request) -> WebhookResult:
        """Confirmation au retour du navigateur (capture PayPal, vérification Flutterwave…)."""
        raise NotImplementedError


def _post_json(url: str, payload: dict, headers: dict | None = None, timeout: int = 30) -> dict:
    """POST JSON via urllib ; retourne la réponse JSON."""
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Cite-de-la-Misericorde/1.0",
            **(headers or {}),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise PaymentServiceError(f"API {exc.code} : {detail}") from exc
    except urllib.error.URLError as exc:
        raise PaymentServiceError(f"Réseau : {exc.reason}") from exc


def _get_json(url: str, headers: dict | None = None, timeout: int = 30) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "Cite-de-la-Misericorde/1.0", **(headers or {})})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise PaymentServiceError(f"API {exc.code} : {detail}") from exc
    except urllib.error.URLError as exc:
        raise PaymentServiceError(f"Réseau : {exc.reason}") from exc


class StripeProvider(BaseProvider):
    """Stripe Checkout (international)."""

    code = "stripe"
    label = "Stripe"

    def is_configured(self) -> bool:
        return bool(self.config.get("secret_key")) and _stripe is not None

    def start_checkout(self, donation, txn: PaymentTransaction) -> CheckoutResult:
        if _stripe is None:  # pragma: no cover
            raise PaymentServiceError("SDK Stripe non installé")
        _stripe.api_key = self.config["secret_key"]
        amount_cents = int((donation.amount * 100).to_integral_value())
        line_items = [
            {
                "quantity": 1,
                "price_data": {
                    "currency": donation.currency.lower(),
                    "unit_amount": amount_cents,
                    "product_data": {"name": f"Don — {donation.reference} — Cité de la Miséricorde"},
                },
            }
        ]
        session_kwargs = dict(
            mode="payment",
            line_items=line_items,
            success_url=self.config.get("success_url", "").format(pk=donation.pk),
            cancel_url=self.config.get("cancel_url", "").format(pk=donation.pk),
            client_reference_id=str(donation.pk),
            metadata={
                "donation_reference": donation.reference,
                "transaction_id": str(txn.pk),
            },
        )
        session = _stripe.checkout.Session.create(**session_kwargs)
        return CheckoutResult(redirect_url=session.url, provider_reference=session.id)

    def verify_webhook(self, request) -> WebhookResult:
        secret = self.config.get("webhook_secret", "")
        signature = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        if not secret or not signature:
            return WebhookResult(ok=False, error="Signature Stripe manquante")
        try:
            event = _stripe.Webhook.construct_event(request.body, signature, secret)
        except Exception as exc:
            return WebhookResult(ok=False, error=f"Signature invalide : {exc}")
        obj = event.get("data", {}).get("object", {})
        reference = obj.get("id", "")
        succeeded = event.get("type") in ("checkout.session.completed", "payment_intent.succeeded")
        return WebhookResult(
            ok=True,
            event_type=event.get("type", ""),
            provider_reference=reference,
            succeeded=succeeded,
        )


class PayPalProvider(BaseProvider):
    """PayPal REST (Orders v2) — appels directs via urllib, pas de SDK."""

    code = "paypal"
    label = "PayPal"
    BASE = "https://api-m.sandbox.paypal.com" if settings.DEBUG or not settings.ALLOWED_HOSTS else "https://api-m.paypal.com"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        if config and config.get("mode") == "live":
            self.BASE = "https://api-m.paypal.com"

    def is_configured(self) -> bool:
        return bool(self.config.get("client_id") and self.config.get("client_secret"))

    def _token(self) -> str:
        import base64

        credentials = f"{self.config['client_id']}:{self.config['client_secret']}"
        request = urllib.request.Request(
            f"{self.BASE}/v1/oauth2/token",
            data=b"grant_type=client_credentials",
            headers={
                "Authorization": f"Basic {base64.b64encode(credentials.encode()).decode()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise PaymentServiceError(f"PayPal token : HTTP {exc.code}") from exc
        return data["access_token"]

    def start_checkout(self, donation, txn: PaymentTransaction) -> CheckoutResult:
        token = self._token()
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": f"{txn.pk}",
                    "description": f"Don {donation.reference} — Cité de la Miséricorde",
                    "amount": {
                        "currency_code": donation.currency,
                        "value": f"{donation.amount:.2f}",
                    },
                }
            ],
            "application_context": {
                "brand_name": "Cité de la Miséricorde",
                "return_url": self.config.get("return_url", "").format(pk=donation.pk, code=self.code),
                "cancel_url": self.config.get("cancel_url", "").format(pk=donation.pk),
            },
        }
        data = _post_json(
            f"{self.BASE}/v2/checkout/orders", payload, {"Authorization": f"Bearer {token}"}
        )
        approve_url = next(
            (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"), ""
        )
        if not approve_url:
            raise PaymentServiceError("PayPal : lien d'approbation absent")
        return CheckoutResult(redirect_url=approve_url, provider_reference=data.get("id", ""))

    def _capture(self, order_id: str) -> dict:
        token = self._token()
        return _post_json(
            f"{self.BASE}/v2/checkout/orders/{order_id}/capture", {}, {"Authorization": f"Bearer {token}"}
        )

    def handle_return(self, request) -> WebhookResult:
        order_id = request.GET.get("token", "")
        if not order_id:
            return WebhookResult(ok=False, error="Token PayPal absent")
        try:
            data = self._capture(order_id)
        except PaymentServiceError as exc:
            return WebhookResult(ok=False, error=str(exc))
        status = (data.get("status") or "").upper()
        if status in ("COMPLETED", "APPROVED"):
            return WebhookResult(
                ok=True,
                event_type="PAYMENT.CAPTURE.COMPLETED",
                provider_reference=order_id,
                succeeded=True,
            )
        return WebhookResult(ok=False, event_type=status, provider_reference=order_id, error=f"PayPal : {status}")

    def verify_webhook(self, request) -> WebhookResult:
        headers = request.headers
        if request.headers.get("Content-Type", "").startswith("application/json"):
            body = request.body
        else:
            body = urllib.parse.parse_qs(request.body.decode("utf-8", errors="replace"))
            body = json.dumps(body).encode("utf-8")
        verification = _post_json(
            f"{self.BASE}/v1/notifications/verify-webhook-signature",
            {
                "auth_algo": headers.get("Paypal-Auth-Algo", ""),
                "cert_url": headers.get("Paypal-Cert-Url", ""),
                "transmission_id": headers.get("Paypal-Transmission-Id", ""),
                "transmission_sig": headers.get("Paypal-Transmission-Sig", ""),
                "transmission_time": headers.get("Paypal-Transmission-Time", ""),
                "webhook_id": self.config.get("webhook_id", ""),
                "webhook_event": json.loads(body.decode("utf-8")),
            },
            timeout=30,
        )
        if verification.get("verification_status") != "SUCCESS":
            return WebhookResult(ok=False, error="Signature PayPal invalide")
        event = json.loads(body.decode("utf-8"))
        order_id = (event.get("resource", {}).get("supplementary_data", {}).get("related_ids", {}).get("order_id", ""))
        return WebhookResult(
            ok=True,
            event_type=event.get("event_type", ""),
            provider_reference=order_id or "",
            succeeded=event.get("event_type") in ("PAYMENT.CAPTURE.COMPLETED", "CHECKOUT.ORDER.APPROVED"),
        )


class MobileMoneyProvider(BaseProvider):
    """Mobile Money RDC via Flutterwave (Airtel / M-Pesa / Orange Money)."""

    code = "mobile_money"
    label = "Mobile Money (Flutterwave)"
    BASE = "https://api.flutterwave.com/v3"

    def is_configured(self) -> bool:
        return bool(self.config.get("flutterwave_secret_key"))

    def start_checkout(self, donation, txn: PaymentTransaction) -> CheckoutResult:
        tx_ref = f"CMD-{txn.pk}-{uuid.uuid4().hex[:10]}"
        payload = {
            "tx_ref": tx_ref,
            "amount": f"{donation.amount:.2f}",
            "currency": donation.currency,
            "redirect_url": self.config.get("return_url", "").format(pk=donation.pk, code=self.code),
            "customer": {
                "email": donation.donor.email or "don@citedelamisericorde.org",
                "name": donation.donor.name or "Donateur anonyme",
            },
            "customizations": {
                "title": f"Don {donation.reference}",
                "description": f"CITE DE LA MISERICORDE — {donation.reference}",
            },
        }
        data = _post_json(
            f"{self.BASE}/payments",
            payload,
            {"Authorization": f"Bearer {self.config['flutterwave_secret_key']}"},
        )
        if not data.get("status") == "success":
            raise PaymentServiceError(f"Flutterwave : {data.get('message', 'échec')}")
        link = (data.get("data") or {}).get("link", "")
        if not link:
            raise PaymentServiceError("Flutterwave : lien de paiement absent")
        return CheckoutResult(redirect_url=link, provider_reference=(data.get("data") or {}).get("id", ""))

    def handle_return(self, request) -> WebhookResult:
        tx_ref = request.GET.get("tx_ref", "")
        if not tx_ref:
            return WebhookResult(ok=False, error="tx_ref absent")
        try:
            data = _get_json(
                f"{self.BASE}/transactions/{urllib.parse.quote(tx_ref)}/verify",
                {"Authorization": f"Bearer {self.config['flutterwave_secret_key']}"},
            )
        except PaymentServiceError as exc:
            return WebhookResult(ok=False, error=str(exc))
        status = (data.get("data") or {}).get("status", "").lower()
        return WebhookResult(
            ok=True,
            event_type=f"charge.{status}",
            provider_reference=tx_ref,
            succeeded=status == "successful",
        )

    def verify_webhook(self, request) -> WebhookResult:
        secret = self.config.get("webhook_secret", "")
        expected = hashlib.sha256(f"{secret}{request.body.decode('utf-8', errors='replace')}".encode()).hexdigest()
        if not secret or request.headers.get("Verif-Hash", "") != expected:
            return WebhookResult(ok=False, error="Signature Flutterwave invalide")
        event = json.loads(request.body.decode("utf-8"))
        data = event.get("data", {})
        return WebhookResult(
            ok=True,
            event_type=event.get("event", {}).get("type", ""),
            provider_reference=data.get("tx_ref", ""),
            succeeded=event.get("event", {}).get("type") == "charge.completed"
            and (data.get("status") or "").lower() == "successful",
        )


class SandboxProvider(BaseProvider):
    """Simulateur de paiement (développement) : succès immédiat, sans réseau."""

    code = "sandbox"
    label = "Mode démo (sans paiement réel)"

    def is_configured(self) -> bool:
        return True

    def start_checkout(self, donation, txn: PaymentTransaction) -> CheckoutResult:
        reference = f"sandbox-{uuid.uuid4().hex}"
        txn.provider_transaction_id = reference
        txn.status = "PROCESSING"
        txn.save(update_fields=["provider_transaction_id", "status", "updated_at"])
        settle_transaction(txn, succeeded=True, event_type="sandbox.completed")
        return CheckoutResult(
            redirect_url=self.config.get("success_url", "").format(pk=donation.pk),
            provider_reference=reference,
        )

    def verify_webhook(self, request) -> WebhookResult:
        return WebhookResult(ok=False, error="Sandbox : pas de webhook")


def get_provider(code: str) -> BaseProvider:
    """Fabrique la passerelle correspondant au code ; Sandbox en repli (DEBUG)."""
    config = dict(getattr(settings, "PAYMENT_PROVIDERS", {}).get(code, {}))
    config.setdefault("success_url", settings.PAYMENT_SUCCESS_URL or "/dons/succes/{pk}/")
    config.setdefault("cancel_url", settings.PAYMENT_CANCEL_URL or "/dons/annulation/{pk}/")
    config.setdefault("return_url", settings.PAYMENT_RETURN_URL or "/payments/retour/{code}/")
    if code == "stripe":
        return StripeProvider(config)
    if code == "paypal":
        return PayPalProvider(config)
    if code == "mobile_money":
        return MobileMoneyProvider(config)
    if code == "sandbox":
        return SandboxProvider(config)
    raise PaymentServiceError(f"Passerelle inconnue : {code}")


def process_webhook(request, provider_code: str) -> WebhookResult:
    """Vérifie la signature, journalise l'événement puis règle la transaction.

    L'événement est toujours tracé dans WebhookEvent (vérif. d'audit, §19),
    même en cas de signature invalide.
    """
    provider = get_provider(provider_code)
    raw_payload = request.body.decode("utf-8", errors="replace")[:20000]
    result = provider.verify_webhook(request)
    try:
        parsed = json.loads(raw_payload) if raw_payload else {}
    except json.JSONDecodeError:
        parsed = {}

    event_type = result.event_type or parsed.get("type") or parsed.get("event_type") or "unknown"
    reference = result.provider_reference or parsed.get("id") or parsed.get("tx_ref") or ""
    from apps.payments.models import PaymentProvider

    provider_model, _ = PaymentProvider.objects.get_or_create(
        code=provider_code,
        defaults={"name": provider.label or provider_code, "is_active": False},
    )
    event = WebhookEvent(
        provider=provider_model,
        event_id=f"{provider_code}-{reference or uuid.uuid4().hex}",
        event_type=event_type,
        payload=parsed,
        signature_valid=result.ok,
        is_processed=result.ok,
        error_message=result.error if not result.ok else "",
    )
    if result.ok:
        txn = _find_transaction(provider_code, reference)
        if txn:
            settle_transaction(txn, result.succeeded, event_type=event_type, error=result.error)
        else:
            event.is_processed = False
            event.error_message = "Transaction introuvable"
    event.save()
    return result


def _find_transaction(provider_code: str, reference: str) -> PaymentTransaction | None:
    if not reference:
        return None
    if provider_code == "mobile_money":
        txn = PaymentTransaction.objects.filter(pk=reference.split("-")[1]).first() if reference.startswith("CMD-") else None
        return txn
    return PaymentTransaction.objects.filter(provider_transaction_id=reference).first()
