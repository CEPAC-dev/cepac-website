from .base import *

DEBUG = True

# In dev allow all hosts (you can restrict if needed)
ALLOWED_HOSTS = []


# Use SQLite (already set in base), but you can customize here.

# Email backend for development (console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Optional: Django debug toolbar if installed
INSTALLED_APPS += [
    # "debug_toolbar",  # uncomment if you install it
]

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",  # if using
] + MIDDLEWARE  # prepend

# Internal IPs for debug toolbar
INTERNAL_IPS = []
