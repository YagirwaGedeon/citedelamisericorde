from django.urls import path

from apps.projects.views import project_detail, project_list

urlpatterns = [
    path("", project_list, name="list"),
    path("<slug:slug>/", project_detail, name="detail"),
]
