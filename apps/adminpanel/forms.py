"""Formulaires de l'espace admin (validation serveur + nettoyage HTML)."""

import bleach
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.utils import timezone

from apps.adminpanel.models import HomePost
from apps.articles.models import Article, ArticleCategory
from apps.core.models import SiteSettings
from apps.media.models import MediaItem
from apps.projects.models import Project

ALLOWED_TAGS = [
    "p", "br", "strong", "b", "em", "i", "u", "s", "a", "ul", "ol", "li",
    "h2", "h3", "h4", "blockquote", "code", "pre", "img", "figure", "figcaption",
    "span", "div", "hr", "table", "thead", "tbody", "tr", "th", "td",
]
ALLOWED_ATTRIBUTES = {
    "*": ["class", "style"],
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title", "width", "height", "loading"],
}


def clean_rich_html(value: str) -> str:
    """Nettoie le HTML saisi (limite le XSS sans dépendre de |safe non contrôlé)."""
    if not value:
        return value
    cleaned = bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )
    return bleach.linkify(cleaned)


class AdminLoginForm(AuthenticationForm):
    """Formulaire de connexion du panel (messages d'erreur en français)."""

    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": (
            "Identifiants incorrects. Vérifiez votre identifiant et votre mot de passe."
        ),
        "inactive": "Ce compte est désactivé.",
    }

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not (user.is_staff or user.is_superuser or getattr(user, "role", "") in {
            "superadmin", "admin", "editor", "project_manager", "finance_manager"
        }):
            raise forms.ValidationError(
                "Ce compte n'a pas accès à l'espace administration.",
                code="no_staff_access",
            )


class HomePostForm(forms.ModelForm):
    content = forms.CharField(
        label="Contenu (texte)",
        widget=forms.Textarea(attrs={"rows": 6, "class": "input", "placeholder": "Texte de la publication…"}),
        required=False,
    )
    excerpt = forms.CharField(
        label="Extrait",
        required=False,
        max_length=400,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Courte description (optionnel)"}),
    )
    published_at = forms.DateTimeField(
        label="Date de publication",
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "input"}),
    )

    class Meta:
        model = HomePost
        fields = [
            "title", "excerpt", "content", "image", "button_text", "button_url",
            "status", "published_at", "order",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "Titre de la publication"}),
            "image": forms.Select(attrs={"class": "input"}),
            "button_text": forms.TextInput(attrs={"class": "input", "placeholder": "Ex. : En savoir plus"}),
            "button_url": forms.TextInput(attrs={"class": "input", "placeholder": "Ex. : /projets/"}),
            "status": forms.Select(attrs={"class": "input"}),
            "order": forms.NumberInput(attrs={"class": "input", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].queryset = MediaItem.objects.filter(kind="image").order_by("-created_at")
        self.fields["image"].required = False
        self.fields["image"].empty_label = "— Aucune image —"
        if self.instance and self.instance.pk and self.instance.published_at:
            self.initial["published_at"] = self.instance.published_at.strftime("%Y-%m-%dT%H:%M")

    def clean_content(self):
        return clean_rich_html(self.cleaned_data.get("content", ""))

    def clean_button_url(self):
        url = (self.cleaned_data.get("button_url") or "").strip()
        if url and not (url.startswith("/") or url.startswith("#") or url.startswith("http://") or url.startswith("https://")):
            raise forms.ValidationError("Lien invalide : commencez par / ou https://")
        return url

    def clean_published_at(self):
        value = self.cleaned_data.get("published_at")
        return value or timezone.now()


class ArticleForm(forms.ModelForm):
    content = forms.CharField(
        label="Contenu (HTML)",
        widget=forms.Textarea(attrs={"rows": 12, "class": "input"}),
        required=False,
    )
    excerpt = forms.CharField(
        label="Extrait",
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 3, "class": "input"}),
    )
    published_at = forms.DateTimeField(
        label="Date de publication",
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "input"}),
    )
    categories = forms.ModelMultipleChoiceField(
        label="Catégories",
        queryset=ArticleCategory.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Article
        fields = [
            "title", "excerpt", "content", "cover_image", "categories",
            "status", "published_at", "is_featured", "publication_authorized",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "Titre de l'actualité"}),
            "cover_image": forms.Select(attrs={"class": "input"}),
            "status": forms.Select(attrs={"class": "input"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-ink-300 text-brand-600 focus:ring-brand-500"}),
            "publication_authorized": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-ink-300 text-brand-600 focus:ring-brand-500"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cover_image"].queryset = MediaItem.objects.filter(kind="image").order_by("-created_at")
        self.fields["cover_image"].required = False
        self.fields["cover_image"].empty_label = "— Aucune image —"
        if self.instance and self.instance.pk and self.instance.published_at:
            self.initial["published_at"] = self.instance.published_at.strftime("%Y-%m-%dT%H:%M")

    def clean_content(self):
        return clean_rich_html(self.cleaned_data.get("content", ""))

    def clean_excerpt(self):
        return bleach.clean(self.cleaned_data.get("excerpt", "") or "", tags=[], strip=True)

    def clean_published_at(self):
        value = self.cleaned_data.get("published_at")
        return value or timezone.now()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title", "program", "status", "location", "context", "problem",
            "objectives", "beneficiaries", "activities", "results",
            "progress_percent", "start_date", "end_date", "budget", "currency",
            "cover_image", "is_featured", "publication_authorized", "needs_donation",
            "seo_description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "Titre du projet"}),
            "program": forms.Select(attrs={"class": "input"}),
            "status": forms.Select(attrs={"class": "input"}),
            "location": forms.TextInput(attrs={"class": "input", "placeholder": "Ex. : Bukavu, RDC"}),
            "context": forms.Textarea(attrs={"rows": 3, "class": "input"}),
            "problem": forms.Textarea(attrs={"rows": 3, "class": "input"}),
            "objectives": forms.Textarea(attrs={"rows": 3, "class": "input"}),
            "beneficiaries": forms.Textarea(attrs={"rows": 3, "class": "input"}),
            "activities": forms.Textarea(attrs={"rows": 3, "class": "input"}),
            "results": forms.Textarea(attrs={"rows": 3, "class": "input"}),
            "progress_percent": forms.NumberInput(attrs={"class": "input", "min": "0", "max": "100"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "input"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "input"}),
            "budget": forms.NumberInput(attrs={"class": "input", "step": "0.01", "min": "0"}),
            "currency": forms.TextInput(attrs={"class": "input", "maxlength": "3"}),
            "cover_image": forms.Select(attrs={"class": "input"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-ink-300 text-brand-600"}),
            "publication_authorized": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-ink-300 text-brand-600"}),
            "needs_donation": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-ink-300 text-brand-600"}),
            "seo_description": forms.TextInput(attrs={"class": "input", "maxlength": "300"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cover_image"].queryset = MediaItem.objects.filter(kind="image").order_by("-created_at")
        self.fields["cover_image"].required = False
        self.fields["cover_image"].empty_label = "— Aucune image —"
        self.fields["program"].required = False
        self.fields["status"].required = False
        self.fields["budget"].required = False

    def clean_progress_percent(self):
        value = self.cleaned_data.get("progress_percent") or 0
        if value > 100:
            raise forms.ValidationError("La progression ne peut dépasser 100 %.")
        return value


class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ["file", "title", "alt_text", "description", "kind", "category"]
        widgets = {
            "file": forms.ClearableFileInput(attrs={"class": "input", "accept": "image/*,.pdf,.doc,.docx"}),
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "Titre (optionnel)"}),
            "alt_text": forms.TextInput(attrs={"class": "input", "placeholder": "Description courte pour l'accessibilité"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "input"}),
            "kind": forms.Select(attrs={"class": "input"}),
            "category": forms.Select(attrs={"class": "input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = False
        self.fields["alt_text"].required = False
        self.fields["category"].required = False


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "phone", "bio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"class": "input"})
        self.fields["last_name"].widget.attrs.update({"class": "input"})
        self.fields["email"].widget.attrs.update({"class": "input", "type": "email"})
        self.fields["phone"].widget.attrs.update({"class": "input"})
        self.fields["bio"].widget.attrs.update({"class": "input", "rows": "4"})
        for name in ("first_name", "last_name", "email"):
            self.fields[name].required = name == "email"

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("L'email est obligatoire.")
        from django.contrib.auth import get_user_model

        User = get_user_model()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email


class AdminPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "input"})


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            "organization_name", "legal_name", "tagline", "email", "phone",
            "address_bukavu", "address_goma", "facebook", "instagram",
            "pinterest", "twitter", "youtube", "whatsapp", "map_embed_url",
            "donation_currency", "pwa_theme_color", "google_analytics_id",
            "matomo_url", "matomo_site_id", "recaptcha_site_key", "maintenance_mode",
        ]
        widgets = {name: forms.TextInput(attrs={"class": "input"}) for name in [
            "organization_name", "legal_name", "tagline", "email", "phone",
            "address_bukavu", "address_goma", "facebook", "instagram",
            "pinterest", "twitter", "youtube", "whatsapp", "map_embed_url",
            "donation_currency", "pwa_theme_color", "google_analytics_id",
            "matomo_url", "matomo_site_id", "recaptcha_site_key",
        ]}
        widgets["maintenance_mode"] = forms.CheckboxInput(
            attrs={"class": "h-4 w-4 rounded border-ink-300 text-brand-600"}
        )
