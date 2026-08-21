"""Vue du formulaire de contact."""

from django.conf import settings
from django.contrib import messages as django_messages
from django.shortcuts import redirect, render

from apps.contact.forms import ContactForm
from apps.contact.security import verify_recaptcha


def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        token = request.POST.get("g_recaptcha_response", "")
        if form.is_valid() and verify_recaptcha(token, request.META.get("REMOTE_ADDR")):
            message = form.save(commit=False)
            message.ip_address = request.META.get("REMOTE_ADDR")
            message.user_agent = request.META.get("HTTP_USER_AGENT", "")[:300]
            message.save()
            django_messages.success(request, "Merci ! Votre message a bien été envoyé.")
            return redirect("contact:success")
    else:
        form = ContactForm()
    return render(
        request,
        "contact/create.html",
        {"form": form, "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY},
    )


def contact_success(request):
    return render(request, "contact/success.html")
