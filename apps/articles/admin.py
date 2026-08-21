"""Admin : articles."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.articles.models import Article, ArticleCategory, ArticleTag


@admin_site.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin_site.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin_site.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "author", "published_at", "is_featured", "views", "publication_authorized")
    list_filter = ("status", "is_featured", "publication_authorized", "categories")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories", "tags", "related_images")
    readonly_fields = ("views", "reading_time_minutes", "created_at", "updated_at")
    fieldsets = (
        ("Contenu", {"fields": ("title", "slug", "excerpt", "content", "cover_image", "related_images")}),
        ("Classification", {"fields": ("categories", "tags")}),
        ("Publication", {"fields": ("author", "status", "published_at", "is_featured", "allow_comments", "publication_authorized")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "canonical_url")}),
        ("Statistiques", {"fields": ("views", "reading_time_minutes")}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
