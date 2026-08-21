"""Étape 10 — Reçus de don : génération PDF (reportlab) et email de remerciement.

Le reçu est émis **après** confirmation du paiement (settle_transaction).
Aucune donnée bancaire n'y figure : référence, montant, devise, date, donateur.
"""

import io
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.utils import timezone

from apps.core.models import SiteSettings


def _site_settings() -> SiteSettings:
    return SiteSettings.objects.first()


def build_receipt_pdf(donation) -> bytes:
    """Génère le PDF du reçu de don (référence CMD-DON-AAAA-NNNNNN)."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    settings_obj = _site_settings() or SiteSettings()
    org = settings_obj.organization_name or "Cité de la Miséricorde"
    legal = settings_obj.legal_name or ""
    amount = Decimal(str(donation.amount))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm, leftMargin=20 * mm, rightMargin=20 * mm
    )
    title_style = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, leading=20, spaceAfter=4)
    sub_style = ParagraphStyle("sub", fontName="Helvetica", fontSize=10, leading=13, textColor=colors.grey)
    normal = ParagraphStyle("normal", fontName="Helvetica", fontSize=10.5, leading=14)

    rows = [
        [Paragraph("REÇU DE DON", title_style)],
        [Paragraph(f"{org}{' — ' + legal if legal else ''}", sub_style)],
        [Spacer(1, 6 * mm)],
        [Table(
            [
                ["Référence du reçu", donation.reference or "—"],
                ["Date", timezone.localtime(donation.paid_at or donation.created_at).strftime("%d/%m/%Y %H:%M")],
                ["Montant", f"{amount:,.2f}".replace(",", " ") + f" {donation.currency}"],
                ["Fréquence", "Don unique" if donation.frequency == "once" else "Don mensuel"],
                ["Projet", str(donation.project) if donation.project else "Sans affectation"],
                ["Donateur", donation.donor.name or "Don anonyme"],
            ],
            colWidths=[50 * mm, 110 * mm],
        )],
        [Spacer(1, 6 * mm)],
        [Paragraph(
            "Merci pour votre générosité. Ce don contribue à l'assistance des enfants orphelins, "
            "à l'autonomisation des femmes et au développement communautaire en RDC.",
            normal,
        )],
        [Spacer(1, 10 * mm)],
        [Paragraph(f"Émis le {datetime.now():%d/%m/%Y} par {org}", sub_style)],
    ]
    flowables = [item for group in rows for item in group]
    doc.build(flowables)
    return buffer.getvalue()


def generate_receipt(donation) -> bool:
    """Crée le PDF du reçu et l'attache au don. Retourne True si généré."""
    if donation.receipt_pdf:
        return False
    try:
        pdf = build_receipt_pdf(donation)
    except Exception:
        return False
    filename = f"recu-{donation.reference or donation.pk}.pdf"
    donation.receipt_pdf.save(filename, ContentFile(pdf), save=True)
    return True


def send_thank_you_email(donation) -> bool:
    """Envoie l'email de remerciement avec le reçu en pièce jointe."""
    if not donation.donor.email:
        return False
    if not donation.receipt_pdf:
        generate_receipt(donation)
    settings_obj = _site_settings() or SiteSettings()
    org = settings_obj.organization_name or "Cité de la Miséricorde"
    subject = f"Merci pour votre don — {donation.reference}"
    message = (
        f"Bonjour {donation.donor.name or 'cher donateur'},\n\n"
        f"Nous vous remercions chaleureusement pour votre don de "
        f"{donation.amount:,.2f} {donation.currency} ({donation.reference}) "
        f"au profit de {org}.\n\n"
        "Votre soutien aide directement les enfants orphelins, les femmes et les "
        "communautés que nous accompagnons en République démocratique du Congo.\n\n"
        "Votre reçu fiscal (reçu de don) est joint à cet email.\n\n"
        "Avec gratitude,\n"
        f"L'équipe de {org}"
    )
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[donation.donor.email],
    )
    if donation.receipt_pdf:
        email.attach(
            f"recu-{donation.reference or donation.pk}.pdf",
            donation.receipt_pdf.read(),
            "application/pdf",
        )
    email.send(fail_silently=True)
    donation.receipt_sent_at = timezone.now()
    donation.save(update_fields=["receipt_sent_at", "updated_at"])
    return True
