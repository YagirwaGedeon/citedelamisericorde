"""Newsletter : inscription, confirmation, désinscription (§33)."""

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from apps.newsletter.models import Subscriber


def subscribe(request):
    """Inscription depuis le formulaire (POST). Envoie un email de confirmation."""
    email = request.POST.get("email", "").strip().lower()
    if not email:
        return redirect("home")
    subscriber, created = Subscriber.objects.get_or_create(email=email)
    if not subscriber.is_active or not subscriber.is_confirmed:
        subscriber.is_active = True
        subscriber.is_confirmed = False
        subscriber.save()
    # Email de confirmation (console en dev)
    confirm_url = request.build_absolute_uri(
        reverse("newsletter:confirm", kwargs={"token": subscriber.token})
    )
    send_mail(
        "Confirmez votre inscription à la newsletter",
        f"Bonjour,\n\nConfirmez votre inscription en cliquant sur ce lien :\n{confirm_url}\n\nMerci,\nCité de la Miséricorde",
        None,
        [subscriber.email],
        fail_silently=True,
    )
    return render(request, "newsletter/subscribed.html", {"email": email})


def confirm(request, token):
    subscriber = get_object_or_404(Subscriber, token=token)
    subscriber.is_confirmed = True
    subscriber.is_active = True
    subscriber.confirmed_at = timezone.now()
    subscriber.save()
    return render(request, "newsletter/confirmed.html", {"email": subscriber.email})


def unsubscribe(request, token):
    subscriber = get_object_or_404(Subscriber, token=token)
    subscriber.is_active = False
    subscriber.unsubscribed_at = timezone.now()
    subscriber.save()
    return render(request, "newsletter/unsubscribed.html", {"email": subscriber.email})
