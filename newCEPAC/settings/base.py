import os
from pathlib import Path

# BASE_DIR points to project root (one level above newCEPAC/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7)-+&q=xmn!)ibo$bfvqxu8t8221udkkb64g045ueygxd!qr)p"


# Default to False; overridden in dev
DEBUG = False

ALLOWED_HOSTS = ["cepac-eg.com,www.cepac-eg.com"]

# Application definition
INSTALLED_APPS = [
    # Django core
    
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your apps
    "accounts",
    "core",
    "main",
    "portfolio",
    "services.kmz_polygon_analysis",
    "services.kmz_to_excel",
    "services.kmz_to_shapefile",
    "services.shap_to_kmz",
    "services.pdf_to_word",
    "services.trip_length_distribution",
    "services.outlier",
    "services.trip_generation",
   
    

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'core.middleware.AccountAgeRestrictionMiddleware',

]

ROOT_URLCONF = "newCEPAC.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates", BASE_DIR / "main" / "templates"],
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

WSGI_APPLICATION = "newCEPAC.wsgi.application"

# Database placeholder (overridden in dev/prod)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "main" / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_FROM_EMAIL = "info@cepac-eg.com"

LOGIN_URL = 'accounts:login'             
LOGIN_REDIRECT_URL = "/" 
LOGOUT_REDIRECT_URL = 'accounts:login'  

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

