"""Vues de la galerie."""

from django.shortcuts import get_object_or_404, render

from apps.gallery.models import Gallery


def gallery_list(request):
    galleries = Gallery.objects.filter(is_published=True).prefetch_related("items__media")
    return render(request, "gallery/list.html", {"galleries": galleries})


def gallery_detail(request, slug):
    gallery = get_object_or_404(
        Gallery.objects.prefetch_related("items__media"), slug=slug, is_published=True
    )
    return render(request, "gallery/detail.html", {"gallery": gallery})
