"""
WSGI config for intrip_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from decouple import config
from django.core.wsgi import get_wsgi_application

ENV = config("ENV", "dev")

if ENV == "dev":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intrip_backend.settings.development')

elif ENV == "prod":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intrip_backend.settings.production')

application = get_wsgi_application()
