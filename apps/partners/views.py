"""Vues partenaires."""

from django.shortcuts import render

from apps.partners.models import Partner


def partner_list(request):
    partners = Partner.objects.filter(is_published=True)
    return render(request, "partners/list.html", {"partners": partners})
