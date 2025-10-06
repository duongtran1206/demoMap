#!/bin/bash

# Debug script for EC2 deployment issues
echo "=== Debugging EC2 Deployment ==="

echo "1. Check project directory permissions:"
ls -la /home/ubuntu/demoMap/
echo ""

echo "2. Check staticfiles directory:"
ls -la /home/ubuntu/demoMap/staticfiles/
echo ""

echo "3. Check specific static files:"
ls -la /home/ubuntu/demoMap/staticfiles/css/admin_dashboard.css
ls -la /home/ubuntu/demoMap/staticfiles/js/admin_dashboard.js
echo ""

echo "4. Test nginx configuration:"
sudo nginx -t
echo ""

echo "5. Check nginx error log:"
sudo tail -10 /var/log/nginx/error.log
echo ""

echo "6. Check gunicorn service status:"
sudo systemctl status demomap --no-pager
echo ""

echo "7. Check gunicorn logs:"
sudo journalctl -u demomap --no-pager -n 10
echo ""

echo "8. Test static file access directly:"
curl -I http://15.152.37.134/static/css/admin_dashboard.css
echo ""

echo "9. Check Django settings in production:"
cd /home/ubuntu/demoMap
source venv/bin/activate
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.production_settings')
import django
django.setup()
from django.conf import settings
print('STATIC_URL:', settings.STATIC_URL)
print('STATIC_ROOT:', settings.STATIC_ROOT)
print('STATICFILES_DIRS:', settings.STATICFILES_DIRS)
print('DEBUG:', settings.DEBUG)
print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)
"
echo ""

echo "=== Fix permissions and restart ==="
sudo chown -R ubuntu:www-data /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/staticfiles/
sudo systemctl restart demomap
sudo systemctl restart nginx

echo "Debug completed!"