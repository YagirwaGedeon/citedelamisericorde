"""Vues des articles : liste paginée + détail."""

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from apps.articles.models import Article, ArticleCategory


def article_list(request):
    """Liste des articles : pagination, catégories, recherche, temps de lecture."""
    articles = Article.objects.filter(
        Q(status="published") & Q(published_at__lte=timezone.now())
    ).select_related("author")

    category_slug = request.GET.get("categorie", "")
    category = None
    if category_slug:
        category = ArticleCategory.objects.filter(slug=category_slug).first()
        if category:
            articles = articles.filter(categories=category)

    query = request.GET.get("q", "").strip()
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(articles, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "articles/list.html",
        {
            "page_obj": page_obj,
            "articles": page_obj.object_list,
            "categories": ArticleCategory.objects.all(),
            "current_category": category,
            "query": query,
        },
    )


def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.select_related("author").prefetch_related("categories", "tags"),
        slug=slug,
        status="published",
    )
    Article.objects.filter(pk=article.pk).update(views=article.views + 1)
    related = Article.objects.filter(status="published").exclude(pk=article.pk)[:3]
    share_url = request.build_absolute_uri(f"/actualites/{article.slug}/")
    return render(
        request,
        "articles/detail.html",
        {
            "article": article,
            "related": related,
            "share_url": share_url,
            "share_title": article.title,
        },
    )
