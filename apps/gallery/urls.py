from django.urls import path

from apps.gallery.views import gallery_detail, gallery_list

urlpatterns = [
    path("", gallery_list, name="list"),
    path("<slug:slug>/", gallery_detail, name="detail"),
]
