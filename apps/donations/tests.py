"""Tests du module de virement bancaire."""

from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.donations.models import BankTransferConfirmation, Donation, Donor


@override_settings(ALLOWED_HOSTS=["*", "testserver", "localhost", "127.0.0.1"])
class BankTransferPageTests(TestCase):
    def _payload(self, **overrides):
        data = {
            "full_name": "Marie Dubois",
            "email": "marie@example.org",
            "country": "France",
            "amount": "150.00",
            "currency": "USD",
            "transfer_date": "2026-09-22",
            "transaction_reference": "TRX-98231",
        }
        data.update(overrides)
        return data

    def test_bank_page_shows_coordinates(self):
        r = self.client.get(reverse("donations:bank_transfer"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "ORPHELINAT CJPD")
        self.assertContains(r, "EQUITY BANK SA")
        self.assertContains(r, "00011-05040-02000422389-82")
        self.assertContains(r, "BCDCCDKI")
        self.assertContains(r, "CITIUS33")
        self.assertContains(r, "J’ai effectué le virement")
        self.assertContains(r, "data-copy")

    def test_confirmation_submission_without_donation(self):
        r = self.client.post(reverse("donations:bank_transfer"), self._payload())
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Confirmation bien reçue")
        self.assertContains(r, "ORPHELINAT CJPD")
        self.assertEqual(BankTransferConfirmation.objects.count(), 1)
        item = BankTransferConfirmation.objects.get()
        self.assertEqual(item.status, "pending")
        self.assertEqual(item.transaction_reference, "TRX-98231")

    def test_confirmation_with_proof_and_donation(self):
        donor = Donor.objects.create(email="linked@example.org", name="Lié")
        donation = Donation.objects.create(
            donor=donor,
            amount=Decimal("150.00"),
            currency="USD",
            status="PENDING",
            idempotency_key="bank-link-1",
        )
        proof = SimpleUploadedFile("recu.pdf", b"%PDF-1.4 fake", content_type="application/pdf")
        payload = self._payload(proof=proof)
        r = self.client.post(
            reverse("donations:bank_transfer_donation", args=[donation.pk]), payload
        )
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Confirmation bien reçue")
        item = BankTransferConfirmation.objects.get()
        self.assertEqual(item.donation_id, donation.pk)
        self.assertTrue(item.proof.name)
        # Preuve hors MEDIA_ROOT (stockage privé)
        self.assertNotIn("media/", item.proof.name)
        donation.refresh_from_db()
        self.assertEqual(donation.status, "PROCESSING")
        self.assertEqual(donation.provider_reference, "TRX-98231")

    def test_invalid_form_redisplays_errors(self):
        r = self.client.post(reverse("donations:bank_transfer"), {"email": "bad"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "field-error")
        self.assertEqual(BankTransferConfirmation.objects.count(), 0)

    def test_form_shown_with_confirmer_query(self):
        r = self.client.get(reverse("donations:bank_transfer") + "?confirmer=1")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'id="bank-confirm-form"')
        self.assertContains(r, "transaction_reference")

    def test_checkout_offers_bank_option(self):
        donor = Donor.objects.create(email="c@example.org", name="C")
        donation = Donation.objects.create(
            donor=donor, amount=Decimal("20.00"), currency="USD",
            status="PENDING", idempotency_key="bank-checkout-1",
        )
        r = self.client.get(reverse("donations:checkout", args=[donation.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Virement bancaire")
        self.assertContains(r, reverse("donations:bank_transfer_donation", args=[donation.pk]))

    def test_create_page_offers_bank_link(self):
        r = self.client.get(reverse("donations:create"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, reverse("donations:bank_transfer"))

    def test_reception_page_links_bank_details(self):
        r = self.client.get(reverse("donations:reception"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, reverse("donations:bank_transfer"))
        self.assertContains(r, "Voir les coordonnées bancaires")
