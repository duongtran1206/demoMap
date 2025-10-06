#!/bin/bash
# Debug script for Django static files

echo "=== Django Static Files Debug ==="
echo "Current directory: $(pwd)"
echo "Python path: $(which python)"

# Check if venv is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment: $VIRTUAL_ENV"
else
    echo "WARNING: No virtual environment detected"
fi

echo ""
echo "=== Django Settings Check ==="
python manage.py check --settings=geomap_project.production_settings

echo ""
echo "=== Static Files Debug ==="
echo "STATIC_URL: $(python manage.py shell --settings=geomap_project.production_settings -c "from django.conf import settings; print(settings.STATIC_URL)")"
echo "STATIC_ROOT: $(python manage.py shell --settings=geomap_project.production_settings -c "from django.conf import settings; print(settings.STATIC_ROOT)")"

echo ""
echo "=== Directory Structure ==="
echo "Static source directory:"
ls -la static/ 2>/dev/null || echo "No static/ directory found"

echo ""
echo "Static files collected directory:"
ls -la staticfiles/ 2>/dev/null || echo "No staticfiles/ directory found"

echo ""
echo "=== Collect Static Files ==="
python manage.py collectstatic --noinput --settings=geomap_project.production_settings

echo ""
echo "=== Check Collected Files ==="
ls -la staticfiles/ 2>/dev/null || echo "No staticfiles/ directory found"
ls -la staticfiles/css/ 2>/dev/null || echo "No CSS files found"
ls -la staticfiles/js/ 2>/dev/null || echo "No JS files found"

echo ""
echo "=== Test Django Admin Dashboard ==="
echo "Testing admin dashboard URL..."
python manage.py shell --settings=geomap_project.production_settings -c "
from django.test import Client
from django.contrib.auth.models import User

# Create test user if doesn't exist
user, created = User.objects.get_or_create(username='admin')
if created:
    user.set_password('admin123')
    user.is_staff = True
    user.is_superuser = True
    user.save()

client = Client()
response = client.get('/admin-dashboard/')
print(f'Dashboard response status: {response.status_code}')

if response.status_code == 302:
    print(f'Redirect to: {response.url}')
"

echo ""
echo "=== Debug Complete ==="