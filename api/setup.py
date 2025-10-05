"""
Vercel handler for Django management commands
"""
import os
import django
from django.core.management import execute_from_command_line
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

def handler(event, context):
    """
    Handler for Vercel serverless functions
    """
    # Collect static files on deployment
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    except:
        pass
    
    # Create superuser if needed
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    except:
        pass
    
    return {"statusCode": 200, "body": "Setup completed"}