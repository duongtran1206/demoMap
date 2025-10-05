#!/usr/bin/env python
"""
Management script for Vercel deployment
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import execute_from_command_line

def create_superuser():
    """Create superuser if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'  # Change this in production
        )
        print("✓ Superuser created: admin/admin123")
    else:
        print("✓ Superuser already exists")

def migrate_database():
    """Run database migrations"""
    execute_from_command_line(['manage.py', 'migrate'])
    print("✓ Database migrations completed")

if __name__ == '__main__':
    print("Setting up Django for Vercel...")
    migrate_database()
    create_superuser()
    print("✓ Setup completed!")