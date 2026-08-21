"""Formulaire de contact (§32) avec champ honeypot anti-spam."""

from django import forms

from apps.contact.models import ContactMessage


class ContactForm(forms.ModelForm):
    """Formulaire public. Le champ `website` est un honeypot (jamais rempli par un humain)."""

    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "off", "tabindex": "-1", "style": "display:none"}),
        label="",
    )

    g_recaptcha_response = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"id": "g-recaptcha-response"}),
        label="",
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-lg border px-4 py-2"}),
            "email": forms.EmailInput(attrs={"class": "w-full rounded-lg border px-4 py-2"}),
            "phone": forms.TextInput(attrs={"class": "w-full rounded-lg border px-4 py-2"}),
            "subject": forms.Select(attrs={"class": "w-full rounded-lg border px-4 py-2"}),
            "message": forms.Textarea(attrs={"class": "w-full rounded-lg border px-4 py-2", "rows": 6}),
        }

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website:
            raise forms.ValidationError("Formulaire non valide.")
        return website
