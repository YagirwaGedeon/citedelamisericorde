"""Tests de l'Étape 10 — paiements (flux sandbox, idempotence, webhooks).

Exécution : python manage.py test apps.payments apps.donations
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.donations.models import Donation, Donor
from apps.payments.models import PaymentProvider, PaymentTransaction, WebhookEvent
from apps.payments.services import get_provider, process_webhook, settle_transaction


def create_donation(status="PENDING"):
    donor = Donor.objects.create(email="test@example.org", name="Test Donateur")
    donation = Donation.objects.create(
        donor=donor,
        amount="25.00",
        currency="USD",
        frequency="once",
        status=status,
        idempotency_key=f"key-{Donation.objects.count() + 1}",
    )
    return donation


class SandboxFlowTest(TestCase):
    def setUp(self):
        PaymentProvider.objects.get_or_create(
            code="sandbox", defaults={"name": "Sandbox", "is_active": True}
        )

    def test_full_sandbox_flow(self):
        donation = create_donation()
        url = reverse("donations:pay", kwargs={"pk": donation.pk, "provider_code": "sandbox"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("donations:success", kwargs={"pk": donation.pk}))

        donation.refresh_from_db()
        self.assertEqual(donation.status, "SUCCEEDED")
        self.assertIsNotNone(donation.paid_at)
        self.assertTrue(donation.receipt_pdf.name.endswith(".pdf"))  # reçu généré

    def test_success_page_generates_receipt(self):
        donation = create_donation()
        provider = get_provider("sandbox")
        txn = PaymentTransaction.objects.create(
            donation=donation, provider=PaymentProvider.objects.get(code="sandbox"),
            amount=donation.amount, currency="USD", status="PROCESSING",
        )
        settle_transaction(txn, succeeded=True, event_type="sandbox.completed")
        donation.refresh_from_db()
        response = self.client.get(reverse("donations:success", kwargs={"pk": donation.pk}))
        self.assertEqual(response.status_code, 200)
        donation.refresh_from_db()
        self.assertTrue(donation.receipt_pdf)

    def test_double_settlement_is_idempotent(self):
        donation = create_donation()
        provider = PaymentProvider.objects.get(code="sandbox")
        txn = PaymentTransaction.objects.create(
            donation=donation, provider=provider,
            amount=donation.amount, currency="USD", status="PROCESSING",
        )
        self.assertTrue(settle_transaction(txn, True, "evt.1"))
        self.assertFalse(settle_transaction(txn, True, "evt.2"))
        self.assertFalse(settle_transaction(txn, False, "evt.3"))
        txn.refresh_from_db()
        donation.refresh_from_db()
        self.assertEqual(txn.status, "SUCCEEDED")
        self.assertEqual(donation.status, "SUCCEEDED")

    def test_webhook_without_signature_is_rejected(self):
        donation = create_donation()
        provider = PaymentProvider.objects.get(code="sandbox")
        PaymentTransaction.objects.create(
            donation=donation, provider=provider,
            amount=donation.amount, currency="USD", status="PROCESSING",
        )
        response = self.client.post(
            reverse("payments:webhook", kwargs={"provider_code": "sandbox"}),
            data='{"type": "payment.succeeded"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["ok"], False)
        event = WebhookEvent.objects.first()
        self.assertIsNotNone(event)
        self.assertFalse(event.signature_valid)
        self.assertFalse(event.is_processed)

    def test_unknown_provider_checkout(self):
        donation = create_donation()
        url = reverse("donations:pay", kwargs={"pk": donation.pk, "provider_code": "inconnu"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ProviderModelTest(TestCase):
    def test_inactive_provider_not_offered(self):
        PaymentProvider.objects.get_or_create(
            code="sandbox", defaults={"name": "Sandbox", "is_active": False}
        )
        donation = create_donation()
        response = self.client.get(reverse("donations:checkout", kwargs={"pk": donation.pk}))
        self.assertNotContains(response, "Sandbox")

    def test_checkout_redirects_when_donation_already_succeeded(self):
        PaymentProvider.objects.get_or_create(
            code="sandbox", defaults={"name": "Sandbox", "is_active": True}
        )
        donation = create_donation(status="SUCCEEDED")
        response = self.client.get(reverse("donations:checkout", kwargs={"pk": donation.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("donations:success", kwargs={"pk": donation.pk}))


class WebhookProcessTest(TestCase):
    def test_process_webhook_unknown_event_safe(self):
        result = process_webhook(_FakeRequest(b'{"type": "ping"}'), "stripe")
        self.assertEqual(result.ok, False)


class _FakeRequest:
    def __init__(self, body: bytes):
        self.body = body
        self.headers = {}
        self.META = {}
