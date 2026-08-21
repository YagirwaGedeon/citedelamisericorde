"""Vues des pages statiques (À propos, Histoire, Mission, Vision, Valeurs, Équipe…).

Chaque page peut être éditée depuis le CMS ; en l'absence de contenu saisi,
un texte institutionnel validé par l'organisation est affiché.
"""

from django.shortcuts import get_object_or_404, render

from apps.pages.models import Page

PAGE_SLUGS = {
    "about": "a-propos",
    "history": "notre-histoire",
    "mission": "notre-mission",
    "vision": "notre-vision",
    "values": "nos-valeurs",
}


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, status="published")
    return render(request, "pages/page_detail.html", {"page": page})


def render_cms_page(request, key):
    """Rend la page CMS correspondante (fallback sur texte par défaut)."""
    slug = PAGE_SLUGS[key]
    page = Page.objects.filter(slug=slug, status="published").first()
    defaults = {
        "about": {
            "title": "À propos",
            "content": (
                "<p>La Cité de la Miséricorde est une organisation humanitaire fondée à Bukavu "
                "(Sud-Kivu, République démocratique du Congo), avec une extension à Goma (Nord-Kivu). "
                "Elle œuvre dans l'assistance aux enfants orphelins et vulnérables, "
                "l'autonomisation des femmes et le développement communautaire.</p>"
            ),
        },
        "history": {
            "title": "Notre histoire",
            "content": (
                "<p>L'organisation est née à Bukavu autour de l'orphelinat Cité de la Miséricorde, "
                "association sans but lucratif, apolitique et non confessionnelle.</p>"
            ),
        },
        "mission": {
            "title": "Notre mission",
            "content": (
                "<p>Assister les enfants orphelins, protéger les enfants vulnérables, "
                "autonomiser les femmes et accompagner les communautés affectées par les crises "
                "en République démocratique du Congo.</p>"
            ),
        },
        "vision": {
            "title": "Notre vision",
            "content": (
                "<p>Une société où chaque enfant orphelin est protégé, chaque femme est autonome "
                "et chaque communauté vit dans la paix et la dignité.</p>"
            ),
        },
        "values": {
            "title": "Nos valeurs",
            "content": (
                "<p>Miséricorde, transparence, intégrité, respect de la dignité humaine, "
                "non-discrimination et solidarité.</p>"
            ),
        },
    }[key]

    if page is None:
        page = Page(title=defaults["title"], content=defaults["content"], status="published", in_menu=True)
    return render(
        request,
        "pages/page_detail.html",
        {"page": page, "is_fallback": page.pk is None},
    )
