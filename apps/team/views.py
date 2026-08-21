"""Vue publique de la page Équipe (contenu issu du document officiel de l'organisation)."""

from django.shortcuts import render

from apps.team.models import TeamMember

TEAM_INTRO = (
    "La Cité de la Miséricorde s'appuie sur une équipe technique et dirigeante "
    "composée de professionnels engagés dans les domaines du développement, de l'action "
    "humanitaire, de la santé communautaire, de l'économie rurale, du suivi-évaluation, "
    "de la finance et de la logistique."
)


def team_view(request):
    members = TeamMember.objects.filter(is_published=True)
    return render(request, "team/list.html", {"members": members, "intro": TEAM_INTRO})