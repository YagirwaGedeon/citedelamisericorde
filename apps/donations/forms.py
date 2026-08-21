"""Formulaires de dons."""

from django import forms

from apps.donations.models import Donation
from apps.projects.models import Project

PRESET_AMOUNTS = [10, 20, 50, 100]


class DonationForm(forms.Form):
    amount = forms.DecimalField(
        label="Montant",
        min_value=1,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "1"}),
    )
    currency = forms.ChoiceField(
        label="Devise", choices=[("USD", "USD ($)"), ("EUR", "EUR (€)"), ("CDF", "CDF (FC)")], initial="USD"
    )
    frequency = forms.ChoiceField(
        label="Fréquence",
        choices=[("once", "Don unique"), ("monthly", "Don mensuel")],
        initial="once",
    )
    project = forms.ModelChoiceField(
        label="Projet (optionnel)", queryset=Project.objects.filter(needs_donation=True), required=False
    )
    name = forms.CharField(label="Nom complet", max_length=200, required=False)
    email = forms.EmailField(label="Email", required=False)
    phone = forms.CharField(label="Téléphone", max_length=50, required=False)
    country = forms.CharField(label="Pays", max_length=100, required=False)
    is_anonymous = forms.BooleanField(label="Don anonyme", required=False)
    message = forms.CharField(label="Message (optionnel)", widget=forms.Textarea, required=False)
    amount_preset = forms.ChoiceField(
        label="Montant prédéfini",
        choices=[(str(a), f"${a}") for a in PRESET_AMOUNTS] + [("custom", "Autre montant")],
        required=False,
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("is_anonymous") and not cleaned.get("email") and not cleaned.get("name"):
            # Un don anonyme peut rester sans identité ; le reçu reste émis avec la référence.
            pass
        elif not cleaned.get("email"):
            self.add_error("email", "Veuillez fournir une adresse email pour recevoir votre reçu.")
        return cleaned
