#!/bin/bash

# EC2 Deployment Script for Django GeoMap Project
echo "Starting Django GeoMap deployment on EC2..."

# Update system
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git

# Navigate to project directory
cd /home/ubuntu/demoMap

# Pull latest changes
git pull origin main

# Create/activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install django==5.2.7
pip install djangorestframework
pip install django-cors-headers
pip install whitenoise
pip install gunicorn

# Run migrations
python manage.py migrate --settings=geomap_project.production_settings

# Create superuser if not exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell --settings=geomap_project.production_settings

# Collect static files
python manage.py collectstatic --noinput --clear --settings=geomap_project.production_settings

# Create gunicorn service file
sudo tee /etc/systemd/system/demomap.service > /dev/null <<EOF
[Unit]
Description=Gunicorn instance to serve DemoMap
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/demoMap
Environment="PATH=/home/ubuntu/demoMap/venv/bin"
ExecStart=/home/ubuntu/demoMap/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/demoMap/demomap.sock geomap_project.wsgi:application --env DJANGO_SETTINGS_MODULE=geomap_project.production_settings
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Set proper permissions for static files
sudo chown -R ubuntu:www-data /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/staticfiles/

# Create nginx configuration
sudo tee /etc/nginx/sites-available/demomap > /dev/null <<EOF
server {
    listen 80;
    server_name 15.152.37.134;
    client_max_body_size 100M;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /staticfiles/ {
        alias /home/ubuntu/demoMap/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        add_header Access-Control-Allow-Origin "*";
    }

    location /static/ {
        alias /home/ubuntu/demoMap/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        add_header Access-Control-Allow-Origin "*";
    }

    location /media/ {
        alias /home/ubuntu/demoMap/media/;
        add_header Access-Control-Allow-Origin "*";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/demoMap/demomap.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        add_header Cross-Origin-Opener-Policy "same-origin-allow-popups";
        add_header Cross-Origin-Embedder-Policy "require-corp";
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/demomap /etc/nginx/sites-enabled
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Start and enable services
sudo systemctl daemon-reload
sudo systemctl start demomap
sudo systemctl enable demomap
sudo systemctl restart nginx
sudo systemctl enable nginx

# Check service status
echo "Checking service status..."
sudo systemctl status demomap --no-pager
sudo systemctl status nginx --no-pager

echo "Deployment completed!"
echo "Access your application at: http://15.152.37.134"
echo "Admin dashboard: http://15.152.37.134/admin-dashboard/"
echo "Map embed: http://15.152.37.134/embed/"