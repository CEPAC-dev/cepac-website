import os
from django.core.asgi import get_asgi_application

# Allow switching via DJANGO_SETTINGS_MODULE env var; default to dev
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newCEPAC.settings.dev")

application = get_asgi_application()
