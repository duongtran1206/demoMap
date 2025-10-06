#!/bin/bash

echo "=== DJANGO DEBUG SCRIPT ==="

cd /home/ubuntu/demoMap
source venv/bin/activate

echo "1. Checking Django settings..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.production_settings')
import django
django.setup()
from django.conf import settings
print('DEBUG:', settings.DEBUG)
print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)
print('ROOT_URLCONF:', settings.ROOT_URLCONF)
"

echo ""
echo "2. Testing Django management commands..."
python manage.py check --settings=geomap_project.production_settings

echo ""
echo "3. Listing URL patterns..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.production_settings')
import django
django.setup()
from django.urls import get_resolver
resolver = get_resolver()
for pattern in resolver.url_patterns:
    print(f'Pattern: {pattern.pattern}')
"

echo ""
echo "4. Testing direct views..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.production_settings')
import django
django.setup()
try:
    from maps.views import welcome_view, admin_dashboard_view, map_embed_view
    print('Views imported successfully')
except Exception as e:
    print(f'View import error: {e}')
"

echo ""
echo "5. Testing Gunicorn locally..."
timeout 3 gunicorn --bind 127.0.0.1:8002 --env DJANGO_SETTINGS_MODULE=geomap_project.production_settings geomap_project.wsgi:application &
sleep 2
curl -I http://127.0.0.1:8002/ 2>/dev/null | head -1 || echo "Gunicorn test failed"
curl -I http://127.0.0.1:8002/admin-dashboard/ 2>/dev/null | head -1 || echo "Admin dashboard test failed"
pkill -f "gunicorn.*8002" || true

echo ""
echo "6. Checking current service status..."
sudo systemctl status demomap --no-pager -l | head -20

echo ""
echo "7. Recent Gunicorn logs..."
sudo journalctl -u demomap -n 10 --no-pager

echo ""
echo "=== DEBUG COMPLETE ==="