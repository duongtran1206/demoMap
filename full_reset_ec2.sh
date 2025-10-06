#!/bin/bash

echo "=== RESET HOÀN TOÀN EC2 DEPLOYMENT ==="

# 1. Stop và remove tất cả services
echo "1. Stopping services..."
sudo systemctl stop nginx || true
sudo systemctl stop demomap || true
sudo systemctl disable demomap || true

# 2. Remove systemd service files
echo "2. Removing systemd services..."
sudo rm -f /etc/systemd/system/demomap.service
sudo systemctl daemon-reload

# 3. Reset Nginx về mặc định hoàn toàn
echo "3. Resetting Nginx to default..."
sudo systemctl stop nginx
sudo apt remove --purge nginx nginx-common nginx-core -y
sudo apt autoremove -y
sudo rm -rf /etc/nginx
sudo rm -rf /var/log/nginx
sudo rm -rf /var/cache/nginx

# Reinstall Nginx clean
sudo apt update
sudo apt install nginx -y

# 4. Backup và xóa project cũ
echo "4. Removing old project..."
cd /home/ubuntu
[ -d demoMap ] && sudo rm -rf "demoMap.backup.$(date +%s)" && sudo mv demoMap "demoMap.backup.$(date +%s)"
[ -d venv ] && sudo rm -rf venv

# 5. Clone fresh code
echo "5. Cloning fresh code..."
git clone https://github.com/duongtran1206/demoMap.git
cd demoMap

# 6. Install Python deps
echo "6. Installing Python environment..."
sudo apt install -y python3-venv python3-pip python3-dev
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 7. Django setup
echo "7. Setting up Django..."
python manage.py migrate --settings=geomap_project.production_settings
python manage.py collectstatic --noinput --clear --settings=geomap_project.production_settings

# Create superuser (admin/admin123)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell --settings=geomap_project.production_settings

# 8. Set permissions
echo "8. Setting file permissions..."
sudo chown -R ubuntu:www-data /home/ubuntu/demoMap
sudo chmod -R 755 /home/ubuntu/demoMap
sudo find /home/ubuntu/demoMap/staticfiles -type f -exec chmod 644 {} \;

# 9. Create simple Nginx config
echo "9. Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/demomap > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 100M;
    
    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias /home/ubuntu/demoMap/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/ubuntu/demoMap/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

# Enable site
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/demomap /etc/nginx/sites-enabled/

# 10. Create Gunicorn service 
echo "10. Creating Gunicorn service..."
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
ExecStart=/home/ubuntu/demoMap/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8001 --timeout 120 geomap_project.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 11. Start services
echo "11. Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable demomap
sudo systemctl start demomap

sudo nginx -t
sudo systemctl enable nginx
sudo systemctl start nginx

# 12. Test
echo "12. Testing deployment..."
sleep 3

echo "Service status:"
sudo systemctl status demomap --no-pager -l
sudo systemctl status nginx --no-pager -l

echo ""
echo "Testing endpoints:"
curl -I http://127.0.0.1/ 2>/dev/null | head -1
curl -I http://127.0.0.1/admin-dashboard/ 2>/dev/null | head -1  
curl -I http://127.0.0.1/static/css/admin_dashboard.css 2>/dev/null | head -1

echo ""
echo "=== DEPLOYMENT HOÀN THÀNH ==="
echo "Truy cập: http://15.152.37.134/"
echo "Admin Dashboard: http://15.152.37.134/admin-dashboard/"
echo "Django Admin: http://15.152.37.134/admin/ (admin/admin123)"