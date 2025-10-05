"""
WSGI config for geomap_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "geomap_project"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')

application = get_wsgi_application()

# Vercel serverless function handler
app = application
