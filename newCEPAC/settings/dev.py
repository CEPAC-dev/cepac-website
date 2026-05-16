from .base import *

DEBUG = True

# In dev allow all hosts (you can restrict if needed)
ALLOWED_HOSTS = []


# Use SQLite (already set in base), but you can customize here.

# Email backend for development using SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.hostinger.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "info@cepac-eg.com"
EMAIL_HOST_PASSWORD = "Info.cepac.com2026#"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = "info@cepac-eg.com"
SERVER_EMAIL = "info@cepac-eg.com"

# Optional: Django debug toolbar if installed
INSTALLED_APPS += [
    # "debug_toolbar",  # uncomment if you install it
]

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",  # if using
] + MIDDLEWARE  # prepend

# Internal IPs for debug toolbar
INTERNAL_IPS = []
