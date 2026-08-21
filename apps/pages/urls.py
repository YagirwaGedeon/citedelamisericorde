from django.urls import path

app_name = "pages"

from apps.pages.views import page_detail, render_cms_page
from apps.team.views import team_view

urlpatterns = [
    path("a-propos/", render_cms_page, {"key": "about"}, name="about"),
    path("notre-histoire/", render_cms_page, {"key": "history"}, name="history"),
    path("notre-mission/", render_cms_page, {"key": "mission"}, name="mission"),
    path("notre-vision/", render_cms_page, {"key": "vision"}, name="vision"),
    path("nos-valeurs/", render_cms_page, {"key": "values"}, name="values"),
    path("notre-equipe/", team_view, name="team"),
    path("page/<slug:slug>/", page_detail, name="page_detail"),
]

