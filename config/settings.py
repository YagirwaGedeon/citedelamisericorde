"""
Django settings for Cité de la Miséricorde.
Projet: citedelamisericorde — config package.
Tous les secrets passent par les variables d'environnement (fichier .env à la racine).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "on")


def env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


# ---------------------------------------------------------------- sécurité
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-only-key-change-me")

DEBUG = env_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "*" if DEBUG else "")

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", False)
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS")
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD")
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE")
SESSION_COOKIE_HTTPONLY = True

# ---------------------------------------------------------------- applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
    "django_filters",
    "crispy_forms",
    "crispy_tailwind",
    # apps métier
    "apps.accounts",
    "apps.core",
    "apps.pages",
    "apps.articles",
    "apps.programs",
    "apps.projects",
    "apps.donations",
    "apps.payments",
    "apps.media",
    "apps.gallery",
    "apps.testimonials",
    "apps.partners",
    "apps.statistics",
    "apps.newsletter",
    "apps.contact",
    "apps.analytics",
    "apps.migration",
    "apps.team",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.RateLimitMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------------- base de données
_use_postgres = env_bool("DJANGO_USE_POSTGRES", False)
_db_engine = os.environ.get(
    "DJANGO_DB_ENGINE",
    "django.db.backends.postgresql" if _use_postgres else "django.db.backends.sqlite3",
)
_db_options = {"connect_timeout": 5} if "postgres" in _db_engine else {}
DATABASES = {
    "default": {
        "ENGINE": _db_engine,
        "NAME": os.environ.get(
            "DJANGO_DB_NAME",
            os.environ.get("POSTGRES_DB", "citedelamisericorde") if _use_postgres else str(BASE_DIR / "db.sqlite3"),
        ),
        "USER": os.environ.get("POSTGRES_USER", "cite"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": _db_options,
    }
}

# ---------------------------------------------------------------- auth & rôles
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# ---------------------------------------------------------------- i18n (FR / EN / Swahili)
LANGUAGES = [
    ("fr", "Français"),
    ("en", "English"),
    ("sw", "Kiswahili"),
]
LANGUAGE_CODE = os.environ.get("DJANGO_LANGUAGE_CODE", "fr")
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "Africa/Lubumbashi")
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------- fichiers statiques et médias
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------- email
EMAIL_BACKEND = os.environ.get("DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "Cité de la Miséricorde <no-reply@citedelamisericorde.org>")
CONTACT_TO_EMAIL = os.environ.get("CONTACT_TO_EMAIL", "contact@citedelamisericorde.org")

# ---------------------------------------------------------------- paiements
PAYMENT_PROVIDERS = {
    "stripe": {
        "secret_key": os.environ.get("STRIPE_SECRET_KEY", ""),
        "publishable_key": os.environ.get("STRIPE_PUBLISHABLE_KEY", ""),
        "webhook_secret": os.environ.get("STRIPE_WEBHOOK_SECRET", ""),
    },
    "paypal": {
        "client_id": os.environ.get("PAYPAL_CLIENT_ID", ""),
        "client_secret": os.environ.get("PAYPAL_CLIENT_SECRET", ""),
        "mode": os.environ.get("PAYPAL_MODE", "sandbox"),
        "webhook_id": os.environ.get("PAYPAL_WEBHOOK_ID", ""),
    },
    "mobile_money": {
        "flutterwave_public_key": os.environ.get("FLW_PUBLIC_KEY", ""),
        "flutterwave_secret_key": os.environ.get("FLW_SECRET_KEY", ""),
        "webhook_secret": os.environ.get("FLW_WEBHOOK_SECRET", ""),
    },
}
PAYMENT_WEBHOOK_URL = "/payments/webhook/"
PAYMENT_SUCCESS_URL = "/dons/succes/{pk}/"
PAYMENT_CANCEL_URL = "/dons/annulation/{pk}/"
PAYMENT_RETURN_URL = "/payments/retour/{code}/"

# ---------------------------------------------------------------- analytics
ANALYTICS_GOOGLE_GA4 = os.environ.get("ANALYTICS_GOOGLE_GA4", "")
ANALYTICS_SEARCH_CONSOLE = os.environ.get("ANALYTICS_SEARCH_CONSOLE", "")
ANALYTICS_MATOMO_URL = os.environ.get("ANALYTICS_MATOMO_URL", "")
ANALYTICS_MATOMO_SITE_ID = os.environ.get("ANALYTICS_MATOMO_SITE_ID", "")

# ---------------------------------------------------------------- WordPress (migration — jamais en clair dans Git)
WORDPRESS_API_BASE = os.environ.get("WORDPRESS_API_BASE", "https://public-api.wordpress.com/rest/v1.1/sites/citedelamisericorde.wordpress.com")
WORDPRESS_USERNAME = os.environ.get("WORDPRESS_USERNAME", "")
WORDPRESS_PASSWORD = os.environ.get("WORDPRESS_PASSWORD", "")
WORDPRESS_SITE = os.environ.get("WORDPRESS_SITE", "https://citedelamisericorde.wordpress.com")

# ---------------------------------------------------------------- PWA / SEO
PWA_MANIFEST_PATH = BASE_DIR / "static" / "manifest.json"
SITE_NAME = "Cité de la Miséricorde"
SITE_TAGLINE = "Heureux ceux qui procurent la paix"

# ---------------------------------------------------------------- sécurité Django (bruit minimal)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_NAME = "csrftoken"

# ---------------------------------------------------------------- reCAPTCHA v3 (formulaire de contact)
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "")
RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCHA_MIN_SCORE = float(os.environ.get("RECAPTCHA_MIN_SCORE", "0.5"))

# ---------------------------------------------------------------- rate limiting (apps.core.middleware)
RATE_LIMIT_MAX_REQUESTS = int(os.environ.get("RATE_LIMIT_MAX_REQUESTS", "120"))
RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("RATE_LIMIT_WINDOW_SECONDS", "60"))

# ---------------------------------------------------------------- Celery / Redis
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_ALWAYS_EAGER = env_bool("CELERY_TASK_ALWAYS_EAGER", DEBUG)

# ---------------------------------------------------------------- stockage médias
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "eu-west-3")

# ---------------------------------------------------------------- misc
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
