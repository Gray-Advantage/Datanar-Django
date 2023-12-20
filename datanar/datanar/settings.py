from pathlib import Path

from decouple import config, strtobool
from django.conf import settings
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "DJANGO_SECRET_KEY",
    default="this_is_test_key_-_some_very_dummy_secret_key",
    cast=str,
)
DEBUG = bool(strtobool(config("DJANGO_DEBUG", "False")))

ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS",
    default="*",
    cast=lambda line: line.split(","),
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_user_agents",
    "rest_framework",
    "api.apps.ApiConfig",
    "core.apps.CoreConfig",
    "qr_codes.apps.QrCodesConfig",
    "homepage.apps.HomepageConfig",
    "users.apps.UsersConfig",
    "redirects.apps.RedirectsConfig",
    "statistic.apps.StatisticConfig",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

if settings.DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]


ROOT_URLCONF = "datanar.urls"

TEMPLATES_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            TEMPLATES_DIR,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "datanar.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


AUTH_USER_MODEL = "users.User"

DEFAULT_USER_IS_ACTIVE = bool(
    strtobool(config("DEFAULT_USER_IS_ACTIVE", "False")),
)

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_REQUIRED = True
if DEFAULT_USER_IS_ACTIVE:
    ACCOUNT_EMAIL_VERIFICATION = "none"
else:
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "<[DATANAR]> "
SITE_ID = 1

EMAIL_HOST = config("DJANGO_MAIL_HOST", default="smtp.mail.ru")
EMAIL_PORT = config("DJANGO_MAIL_PORT", default=2525, cast=int)
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = config("DJANGO_MAIL_USER", default="webmaster@localhost")
EMAIL_HOST_USER = config("DJANGO_MAIL_USER", default="webmaster@localhost")
EMAIL_HOST_PASSWORD = config(
    "DJANGO_MAIL_PASSWORD",
    default="this_very_secret_password_for_smtp_mail",
)

LANGUAGE_CODE = "ru-ru"

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = (BASE_DIR / "locale/",)

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev/",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

GEOIP_PATH = "geo_ip"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
