"""Formulaires de dons."""

from django import forms

from apps.donations.models import BankTransferConfirmation, Donation
from apps.projects.models import Project

PRESET_AMOUNTS = [10, 20, 50, 100]


class BankTransferConfirmForm(forms.ModelForm):
    """Formulaire « J’ai effectué le virement » (preuve facultuelle)."""

    class Meta:
        model = BankTransferConfirmation
        fields = [
            "full_name",
            "email",
            "country",
            "amount",
            "currency",
            "transfer_date",
            "transaction_reference",
            "proof",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "input", "placeholder": "Votre nom complet", "autocomplete": "name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "input", "placeholder": "vous@exemple.org", "autocomplete": "email"}
            ),
            "country": forms.TextInput(
                attrs={"class": "input", "placeholder": "République Démocratique du Congo", "autocomplete": "country-name"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "input", "step": "0.01", "min": "0.01", "placeholder": "100.00"}
            ),
            "currency": forms.Select(attrs={"class": "input"}),
            "transfer_date": forms.DateInput(
                attrs={"type": "date", "class": "input"}
            ),
            "transaction_reference": forms.TextInput(
                attrs={"class": "input", "placeholder": "Ex. : TRX-98231 / Réf. bancaire"}
            ),
            "proof": forms.ClearableFileInput(
                attrs={
                    "class": "input",
                    "accept": ".pdf,.png,.jpg,.jpeg,.webp,image/*,application/pdf",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].required = name != "proof"
        self.fields["proof"].required = False
        self.fields["proof"].label = "Preuve de paiement (reçu, capture ou PDF — optionnel)"

    def clean_transaction_reference(self):
        ref = (self.cleaned_data.get("transaction_reference") or "").strip()
        if not ref:
            raise forms.ValidationError("Indiquez la référence de la transaction bancaire.")
        return ref[:120]

    def clean_full_name(self):
        name = (self.cleaned_data.get("full_name") or "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Indiquez votre nom complet.")
        return name

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("Une adresse e-mail est requise.")
        return email

    def clean_country(self):
        country = (self.cleaned_data.get("country") or "").strip()
        if not country:
            raise forms.ValidationError("Indiquez votre pays.")
        return country[:100]

    def clean_proof(self):
        proof = self.cleaned_data.get("proof")
        if proof and hasattr(proof, "size") and proof.size > 5 * 1024 * 1024:
            raise forms.ValidationError("La preuve ne doit pas dépasser 5 Mo.")
        return proof


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
