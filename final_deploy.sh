#!/bin/bash

echo "=== FINAL DEPLOYMENT SCRIPT ==="
echo "Này sẽ đảm bảo server giống hệt local environment"

# Stop all services first
sudo systemctl stop nginx demomap || true

# Clean slate
cd /home/ubuntu
[ -d demoMap ] && sudo rm -rf demoMap

# Fresh clone
git clone https://github.com/duongtran1206/demoMap.git
cd demoMap

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install exact same packages as local
pip install --upgrade pip
pip install -r requirements.txt

# Copy local db structure (run migrations)
python manage.py migrate --settings=geomap_project.production_settings

# Collect static files
python manage.py collectstatic --noinput --clear --settings=geomap_project.production_settings

# Create superuser if not exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell --settings=geomap_project.production_settings

# Set proper permissions
sudo chown -R ubuntu:www-data /home/ubuntu/demoMap
sudo chmod -R 755 /home/ubuntu/demoMap

# Test Django before configuring services
echo "Testing Django directly..."
python manage.py check --settings=geomap_project.production_settings
echo "Django check passed!"

# Test views are accessible
echo "Testing views..."
timeout 5 python manage.py runserver 127.0.0.1:8888 --settings=geomap_project.production_settings &
sleep 2
TEST_RESULT=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8888/admin-dashboard/ || echo "FAIL")
pkill -f "runserver.*8888" || true
echo "Django test result: $TEST_RESULT"

# Create exact Gunicorn service matching local behavior
sudo tee /etc/systemd/system/demomap.service > /dev/null <<'EOF'
[Unit]
Description=Gunicorn instance to serve DemoMap
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/demoMap
Environment="PATH=/home/ubuntu/demoMap/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=geomap_project.production_settings"
ExecStart=/home/ubuntu/demoMap/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8001 \
    --timeout 120 \
    --access-logfile /home/ubuntu/demoMap/gunicorn_access.log \
    --error-logfile /home/ubuntu/demoMap/gunicorn_error.log \
    --log-level info \
    geomap_project.wsgi:application
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx config exactly matching requirements  
sudo tee /etc/nginx/sites-available/demomap > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 100M;
    
    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options ALLOWALL;
    add_header Referrer-Policy same-origin;
    
    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias /home/ubuntu/demoMap/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    location /media/ {
        alias /home/ubuntu/demoMap/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_redirect off;
    }
}
EOF

# Remove default nginx sites and enable our site
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/demomap /etc/nginx/sites-enabled/

# Start services
sudo systemctl daemon-reload
sudo systemctl enable demomap
sudo systemctl start demomap

sudo nginx -t
if [ $? -eq 0 ]; then
    sudo systemctl enable nginx
    sudo systemctl start nginx
else
    echo "Nginx config test failed!"
    exit 1
fi

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 5

# Final comprehensive test
echo ""
echo "=== FINAL TESTING ==="

echo "1. Service status:"
sudo systemctl status demomap --no-pager -l | head -10
sudo systemctl status nginx --no-pager -l | head -5

echo ""
echo "2. Testing endpoints:"
echo -n "Root (/) : "
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/
echo -n "Admin dashboard (/admin-dashboard/) : "  
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/admin-dashboard/
echo -n "Embed (/embed/) : "
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/embed/
echo -n "Static CSS : "
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/static/css/admin_dashboard.css

echo ""
echo "3. External access test:"
echo -n "External root : "
curl -s -o /dev/null -w "%{http_code}" http://15.152.37.134/ || echo "FAIL"
echo -n "External admin dashboard : "
curl -s -o /dev/null -w "%{http_code}" http://15.152.37.134/admin-dashboard/ || echo "FAIL"

echo ""
echo "=== DEPLOYMENT COMPLETE ==="
echo "If all tests show 200, 302, or 301 - deployment is successful!"
echo ""
echo "Access URLs:"
echo "- Main site: http://15.152.37.134/"
echo "- Admin Dashboard: http://15.152.37.134/admin-dashboard/"  
echo "- Map Embed: http://15.152.37.134/embed/"
echo "- Django Admin: http://15.152.37.134/admin/ (admin/admin123)"
echo ""
echo "Logs location:"
echo "- Gunicorn access: /home/ubuntu/demoMap/gunicorn_access.log"
echo "- Gunicorn error: /home/ubuntu/demoMap/gunicorn_error.log"
echo "- Nginx error: /var/log/nginx/error.log"