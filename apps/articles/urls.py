from django.urls import path

from apps.articles.views import article_detail, article_list

urlpatterns = [
    path("", article_list, name="list"),
    path("<slug:slug>/", article_detail, name="detail"),
]
