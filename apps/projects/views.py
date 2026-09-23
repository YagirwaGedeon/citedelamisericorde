"""Vues des projets (liste filtrable + fiche détaillée)."""

from django.shortcuts import get_object_or_404, render

from apps.projects.models import Project, ProjectStatus


def project_list(request):
    """Liste des projets avec filtre par statut (En cours / Réalisés / Urgent)."""
    statuses = ProjectStatus.objects.all()
    current_status = None
    status_filter = request.GET.get("statut", "")

    projects = Project.objects.select_related("status", "program").all()
    if status_filter:
        current_status = statuses.filter(code=status_filter).first()
        projects = projects.filter(status=current_status)

    return render(
        request,
        "projects/list.html",
        {
            "projects": projects,
            "statuses": statuses,
            "current_status": current_status,
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related("status", "program").prefetch_related("gallery"),
        slug=slug,
    )
    from django.db.models import F

    Project.objects.filter(pk=project.pk).update(views=F("views") + 1)
    project.refresh_from_db(fields=["views"])
    related = Project.objects.exclude(pk=project.pk)[:3]
    return render(
        request,
        "projects/detail.html",
        {"project": project, "related": related},
    )
