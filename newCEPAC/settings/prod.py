from .base import *
import os

DEBUG = True

# Example: parse allowed hosts from env
ALLOWED_HOSTS = ['cepac-eg.com', 'www.cepac-eg.com']


# Secure headers (if behind proxy)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "1") == "1"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Example PostgreSQL configuration via DATABASE_URL
# Requires psycopg2-binary and dj-database-url if you want to parse automatically.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Override secret key in production
SECRET_KEY = "django-insecure-7)-+&q=xmn!)ibo$bfvqxu8t8221udkkb64g045ueygxd!qr)p"
