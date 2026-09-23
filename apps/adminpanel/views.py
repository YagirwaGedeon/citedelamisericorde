"""Vues de l'espace administration (/admin/*)."""

from hashlib import sha256

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from apps.adminpanel.decorators import staff_login_required
from apps.adminpanel.forms import (
    AdminPasswordChangeForm,
    AdminLoginForm,
    ArticleForm,
    HomePostForm,
    MediaUploadForm,
    ProfileForm,
    ProjectForm,
    SiteSettingsForm,
)
from apps.adminpanel.models import HomePost
from apps.analytics.models import PageView
from apps.articles.models import Article
from apps.contact.models import ContactMessage
from apps.core.models import SiteSettings
from apps.donations.models import Donation, Donor
from apps.media.models import MediaItem
from apps.projects.models import Project

User = get_user_model()

LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 15 * 60
LOGIN_FAIL_CACHE = "adminpanel:login_fail:"


def _client_ip(request) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _login_fail_key(ip: str) -> str:
    return f"{LOGIN_FAIL_CACHE}{ip}"


def _is_locked(ip: str) -> bool:
    return (cache.get(_login_fail_key(ip)) or 0) >= LOGIN_MAX_ATTEMPTS


def _register_fail(ip: str) -> int:
    key = _login_fail_key(ip)
    count = (cache.get(key) or 0) + 1
    cache.set(key, count, LOGIN_WINDOW_SECONDS)
    return count


def login_view(request):
    if request.user.is_authenticated:
        return redirect("adminpanel:dashboard")

    ip = _client_ip(request)
    locked = _is_locked(ip)
    form = AdminLoginForm(request, data=request.POST or None)

    if request.method == "POST" and not locked and form.is_valid():
        user = form.get_user()
        cache.delete(_login_fail_key(ip))
        auth_login(request, user)
        messages.success(request, f"Bienvenue, {user.get_full_name() or user.username} !")
        next_url = request.GET.get("next") or request.POST.get("next")
        if next_url and next_url.startswith("/") and not next_url.startswith("//"):
            return redirect(next_url)
        return redirect("adminpanel:dashboard")

    if request.method == "POST" and not locked:
        _register_fail(ip)
        remaining = LOGIN_MAX_ATTEMPTS - (cache.get(_login_fail_key(ip)) or 0)
        if remaining <= 0:
            messages.error(
                request,
                "Trop de tentatives échouées. Réessayez dans 15 minutes.",
            )
        else:
            messages.error(request, "Identifiants incorrects.")

    context = {
        "form": form,
        "locked": locked,
        "attempts_left": max(0, LOGIN_MAX_ATTEMPTS - (cache.get(_login_fail_key(ip)) or 0)),
    }
    return render(request, "adminpanel/login.html", context)


@require_POST
def logout_view(request):
    auth_logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect("adminpanel:login")


@staff_login_required
def dashboard(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = today_start.replace(day=1)

    total_donations = (
        Donation.objects.filter(status="SUCCEEDED").aggregate(total=Sum("amount"))["total"] or 0
    )
    kpis = [
        {"label": "Publications", "value": HomePost.objects.count(), "hint": "accueil"},
        {"label": "Projets", "value": Project.objects.count(), "hint": "au total"},
        {"label": "Actualités", "value": Article.objects.filter(status="published").count(), "hint": "publiées"},
        {"label": "Médias", "value": MediaItem.objects.count(), "hint": "fichiers"},
        {"label": "Messages non lus", "value": ContactMessage.objects.filter(is_read=False, is_spam=False).count(), "hint": "contact"},
        {"label": "Visiteurs aujourd'hui", "value": PageView.objects.filter(created_at__gte=today_start, is_bot=False).count(), "hint": "analytics"},
        {"label": "Dons réussis (USD)", "value": f"{float(total_donations):,.2f}".replace(",", " "), "hint": "cumul"},
        {"label": "Donateurs", "value": Donor.objects.count(), "hint": "en base"},
    ]
    context = {
        "page_title": "Tableau de bord",
        "kpis": kpis,
        "recent_home_posts": HomePost.objects.order_by("-updated_at")[:5],
        "recent_articles": Article.objects.order_by("-updated_at")[:5],
        "recent_projects": Project.objects.select_related("status").order_by("-updated_at")[:5],
        "recent_messages": ContactMessage.objects.filter(is_spam=False).order_by("-created_at")[:5],
        "donations_month": Donation.objects.filter(created_at__gte=month_start).count(),
        "active_section": "dashboard",
    }
    return render(request, "adminpanel/dashboard.html", context)


# ---------------------------------------------------------------- Accueil (publications)
@staff_login_required
def home_list(request):
    q = request.GET.get("q", "").strip()
    posts = HomePost.objects.select_related("image", "author")
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    page_obj = Paginator(posts, 20).get_page(request.GET.get("page"))
    return render(
        request,
        "adminpanel/home_list.html",
        {"page_obj": page_obj, "q": q, "page_title": "Publications d'accueil", "active_section": "home"},
    )


@staff_login_required
@require_http_methods(["GET", "POST"])
def home_create(request):
    if request.method == "POST":
        form = HomePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Publication créée.")
            return redirect("adminpanel:home_list")
    else:
        form = HomePostForm()
    return render(
        request,
        "adminpanel/home_form.html",
        {"form": form, "page_title": "Nouvelle publication", "active_section": "home"},
    )


@staff_login_required
@require_http_methods(["GET", "POST"])
def home_edit(request, pk):
    post = get_object_or_404(HomePost, pk=pk)
    if request.method == "POST":
        form = HomePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Publication mise à jour.")
            return redirect("adminpanel:home_list")
    else:
        form = HomePostForm(instance=post)
    return render(
        request,
        "adminpanel/home_form.html",
        {"form": form, "post": post, "page_title": "Modifier la publication", "active_section": "home"},
    )


@staff_login_required
@require_POST
def home_delete(request, pk):
    post = get_object_or_404(HomePost, pk=pk)
    post.delete()
    messages.success(request, "Publication supprimée.")
    return redirect("adminpanel:home_list")


# ---------------------------------------------------------------- Projets
@staff_login_required
def projects_list(request):
    q = request.GET.get("q", "").strip()
    projects = Project.objects.select_related("status", "program")
    if q:
        projects = projects.filter(Q(title__icontains=q) | Q(location__icontains=q))
    page_obj = Paginator(projects, 20).get_page(request.GET.get("page"))
    return render(
        request,
        "adminpanel/projects_list.html",
        {"page_obj": page_obj, "q": q, "page_title": "Projets", "active_section": "projects"},
    )


@staff_login_required
@require_http_methods(["GET", "POST"])
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet créé.")
            return redirect("adminpanel:projects_list")
    else:
        form = ProjectForm()
    return render(
        request,
        "adminpanel/project_form.html",
        {"form": form, "page_title": "Nouveau projet", "active_section": "projects"},
    )


@staff_login_required
@require_http_methods(["GET", "POST"])
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet mis à jour.")
            return redirect("adminpanel:projects_list")
    else:
        form = ProjectForm(instance=project)
    return render(
        request,
        "adminpanel/project_form.html",
        {"form": form, "project": project, "page_title": "Modifier le projet", "active_section": "projects"},
    )


@staff_login_required
@require_POST
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    messages.success(request, "Projet supprimé.")
    return redirect("adminpanel:projects_list")


# ---------------------------------------------------------------- Actualités
@staff_login_required
def news_list(request):
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    articles = Article.objects.select_related("author").prefetch_related("categories")
    if q:
        articles = articles.filter(Q(title__icontains=q) | Q(excerpt__icontains=q))
    if status in {"draft", "published", "archived"}:
        articles = articles.filter(status=status)
    page_obj = Paginator(articles, 20).get_page(request.GET.get("page"))
    return render(
        request,
        "adminpanel/news_list.html",
        {
            "page_obj": page_obj,
            "q": q,
            "status": status,
            "page_title": "Actualités",
            "active_section": "news",
        },
    )


@staff_login_required
@require_http_methods(["GET", "POST"])
def news_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            if not article.author_id:
                article.author = request.user
            article.save()
            form.save_m2m()
            messages.success(request, "Actualité créée.")
            return redirect("adminpanel:news_list")
    else:
        form = ArticleForm()
    return render(
        request,
        "adminpanel/news_form.html",
        {"form": form, "page_title": "Nouvelle actualité", "active_section": "news"},
    )


@staff_login_required
@require_http_methods(["GET", "POST"])
def news_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Actualité mise à jour.")
            return redirect("adminpanel:news_list")
    else:
        form = ArticleForm(instance=article)
    return render(
        request,
        "adminpanel/news_form.html",
        {"form": form, "article": article, "page_title": "Modifier l'actualité", "active_section": "news"},
    )


@staff_login_required
@require_POST
def news_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    messages.success(request, "Actualité supprimée.")
    return redirect("adminpanel:news_list")


# ---------------------------------------------------------------- Médiathèque
def _optimize_image(path) -> tuple[int | None, int | None]:
    """Compresse l'image (Pillow) et renvoie (largeur, hauteur)."""
    try:
        from PIL import Image, ImageOps
    except ImportError:
        return None, None
    try:
        with Image.open(path) as img:
            img = ImageOps.exif_transpose(img)
            width, height = img.size
            fmt = (img.format or "").upper()
            if fmt in {"JPEG", "JPG"}:
                img.save(path, format="JPEG", optimize=True, quality=85)
            elif fmt == "PNG":
                img.save(path, format="PNG", optimize=True)
            elif fmt == "WEBP":
                img.save(path, format="WEBP", quality=85, method=6)
            return width, height
    except Exception:
        return None, None


def _file_checksum(path) -> str:
    digest = sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


@staff_login_required
def media_list(request):
    q = request.GET.get("q", "").strip()
    kind = request.GET.get("kind", "").strip()
    items = MediaItem.objects.all()
    if q:
        items = items.filter(Q(title__icontains=q) | Q(alt_text__icontains=q) | Q(file__icontains=q))
    if kind in {"image", "document"}:
        items = items.filter(kind=kind)
    page_obj = Paginator(items, 24).get_page(request.GET.get("page"))
    upload_form = MediaUploadForm()
    return render(
        request,
        "adminpanel/media.html",
        {
            "page_obj": page_obj,
            "q": q,
            "kind": kind,
            "upload_form": upload_form,
            "page_title": "Médiathèque",
            "active_section": "media",
        },
    )


@staff_login_required
@require_POST
def media_upload(request):
    form = MediaUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "Import impossible : " + "; ".join(
            f"{k}: {', '.join(v)}" for k, v in form.errors.items()
        )[:400])
        return redirect("adminpanel:media_list")

    item = form.save(commit=False)
    if not item.title:
        item.title = getattr(item.file, "name", "").rsplit("/", 1)[-1]
    item.save()

    if item.kind == "image" and item.file and hasattr(item.file, "path"):
        try:
            width, height = _optimize_image(item.file.path)
            if width and height:
                item.width, item.height = width, height
            checksum = _file_checksum(item.file.path)
            if checksum != item.checksum:
                if MediaItem.objects.filter(checksum=checksum).exclude(pk=item.pk).exists():
                    checksum = item.checksum
                item.checksum = checksum
            item.save(update_fields=["width", "height", "checksum", "updated_at"])
        except Exception:
            pass

    messages.success(request, f"« {item.title} » importé et optimisé.")
    return redirect("adminpanel:media_list")


@staff_login_required
@require_POST
def media_delete(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)
    protected = False
    for rel in ("article_cover", "project_cover", "home_posts", "articles", "projects", "pages", "testimonial"):
        related = getattr(item, rel, None)
        if related is not None and hasattr(related, "exists") and related.exists():
            protected = True
            break
    if protected:
        messages.error(request, "Ce média est utilisé et ne peut pas être supprimé.")
        return redirect("adminpanel:media_list")
    item.delete()
    messages.success(request, "Média supprimé.")
    return redirect("adminpanel:media_list")


@staff_login_required
def media_file(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)
    if not item.file:
        raise Http404
    try:
        return FileResponse(item.file.open("rb"), as_attachment=False)
    except FileNotFoundError:
        raise Http404


# ---------------------------------------------------------------- Profil
@staff_login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        pwd_form = AdminPasswordChangeForm(user, request.POST, prefix="pwd")
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour.")
            if pwd_form.is_valid():
                pwd_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Mot de passe modifié.")
            return redirect("adminpanel:profile")
    else:
        form = ProfileForm(instance=user)
        pwd_form = AdminPasswordChangeForm(user, prefix="pwd")
    return render(
        request,
        "adminpanel/profile.html",
        {
            "form": form,
            "pwd_form": pwd_form,
            "page_title": "Mon profil",
            "active_section": "profile",
        },
    )


# ---------------------------------------------------------------- Paramètres du site
@staff_login_required
@require_http_methods(["GET", "POST"])
def settings_view(request):
    if not (request.user.is_superuser or getattr(request.user, "role", "") in {"superadmin", "admin"}):
        messages.error(request, "Accès réservé aux super administrateurs.")
        return redirect("adminpanel:dashboard")
    site = SiteSettings.get()
    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            messages.success(request, "Paramètres enregistrés.")
            return redirect("adminpanel:settings")
    else:
        form = SiteSettingsForm(instance=site)
    return render(
        request,
        "adminpanel/settings.html",
        {"form": form, "page_title": "Paramètres", "active_section": "settings"},
    )


@staff_login_required
def api_media_options(request):
    """JSON des images pour les sélecteurs (usage interne)."""
    items = MediaItem.objects.filter(kind="image").order_by("-created_at")[:200]
    return JsonResponse(
        {"results": [{"id": i.pk, "label": str(i)} for i in items]}
    )
