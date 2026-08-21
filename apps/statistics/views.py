"""Vues impact (indicateurs + témoignages)."""

from django.shortcuts import render

from apps.statistics.models import Statistic
from apps.testimonials.models import Testimonial


def impact_list(request):
    statistics = Statistic.objects.filter(is_published=True)
    testimonials = Testimonial.objects.filter(is_published=True, publication_authorized=True)
    return render(
        request,
        "statistics/list.html",
        {"statistics": statistics, "testimonials": testimonials},
    )
