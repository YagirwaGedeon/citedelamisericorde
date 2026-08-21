"""Vues des programmes (domaines d'intervention)."""

from django.shortcuts import get_object_or_404, render

from apps.programs.models import Program


def program_list(request):
    programs = Program.objects.filter(is_active=True)
    return render(request, "programs/list.html", {"programs": programs})


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug, is_active=True)
    projects = program.projects.all()
    return render(
        request,
        "programs/detail.html",
        {"program": program, "projects": projects},
    )
