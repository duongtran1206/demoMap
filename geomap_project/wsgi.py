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
from django.contrib.staticfiles.handlers import StaticFilesHandler

# Add the project directory to the Python path
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')

# Initialize Django
application = get_wsgi_application()

# For Vercel, handle static files
if os.environ.get('VERCEL'):
    application = StaticFilesHandler(application)

# Vercel serverless function handler
app = application
