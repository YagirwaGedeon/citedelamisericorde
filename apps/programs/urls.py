from django.urls import path

from apps.programs.views import program_detail, program_list

urlpatterns = [
    path("", program_list, name="list"),
    path("<slug:slug>/", program_detail, name="detail"),
]
