"""Routes de l'espace /admin/."""

from django.urls import path

from apps.adminpanel import views

app_name = "adminpanel"

urlpatterns = [
    path("", views.dashboard, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("analytics/", views.analytics_view, name="analytics"),

    path("home/", views.home_list, name="home_list"),
    path("home/create/", views.home_create, name="home_create"),
    path("home/<int:pk>/edit/", views.home_edit, name="home_edit"),
    path("home/<int:pk>/delete/", views.home_delete, name="home_delete"),

    path("projects/", views.projects_list, name="projects_list"),
    path("projects/create/", views.project_create, name="project_create"),
    path("projects/<int:pk>/edit/", views.project_edit, name="project_edit"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),

    path("news/", views.news_list, name="news_list"),
    path("news/create/", views.news_create, name="news_create"),
    path("news/<int:pk>/edit/", views.news_edit, name="news_edit"),
    path("news/<int:pk>/delete/", views.news_delete, name="news_delete"),

    path("media/", views.media_list, name="media_list"),
    path("media/upload/", views.media_upload, name="media_upload"),
    path("media/<int:pk>/delete/", views.media_delete, name="media_delete"),
    path("media/<int:pk>/file/", views.media_file, name="media_file"),

    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings_view, name="settings"),
    path("api/media-options/", views.api_media_options, name="api_media_options"),
]
