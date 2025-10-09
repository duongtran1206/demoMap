#!/bin/bash

# Script to start Django GeoMap project as a service on EC2
# This creates systemd service and nginx configuration for persistent running

echo "=== Starting Django GeoMap Service on EC2 ==="

# Check if we're in the project directory
if [ ! -f "manage.py" ]; then
    echo "Error: Not in Django project directory. Please run from /home/ubuntu/demoMap/"
    exit 1
fi

# Set variables
PROJECT_DIR="/home/ubuntu/demoMap"
VENV_DIR="$PROJECT_DIR/venv"
USER="ubuntu"
GROUP="www-data"

# Create virtual environment if it doesn't exist
echo "Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi

# Activate virtual environment and install/update requirements
echo "Installing/updating Python packages..."
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create systemd service file
echo "Creating systemd service..."
sudo tee /etc/systemd/system/demomap.service > /dev/null <<EOF
[Unit]
Description=Django GeoMap Application
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
Environment="DJANGO_SETTINGS_MODULE=geomap_project.settings"
ExecStart=$VENV_DIR/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/demoMap/demomap.sock geomap_project.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration
echo "Creating nginx configuration..."
sudo tee /etc/nginx/sites-available/demomap > /dev/null <<EOF
server {
    listen 80;
    server_name 15.152.37.134;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/demoMap/demomap.sock;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;

        # Handle large file uploads
        client_max_body_size 100M;
    }
}
EOF

# Enable nginx site
echo "Enabling nginx site..."
sudo ln -sf /etc/nginx/sites-available/demomap /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Set proper permissions
echo "Setting permissions..."
sudo chown -R $USER:$GROUP $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR/staticfiles/
sudo chmod -R 755 $PROJECT_DIR/media/

# Allow nginx to access socket
sudo usermod -a -G $GROUP $USER 2>/dev/null || true

# Start and enable services
echo "Starting services..."
sudo systemctl daemon-reload
sudo systemctl start demomap
sudo systemctl enable demomap
sudo systemctl restart nginx

# Check service status
echo "Checking service status..."
sudo systemctl status demomap --no-pager -l
sudo systemctl status nginx --no-pager -l

# Test the application
echo "Testing application..."
sleep 3
curl -s -o /dev/null -w "%{http_code}" http://localhost/ | grep -q "200" && echo "✓ Application is running successfully!" || echo "✗ Application test failed"

echo "=== Service Start Complete ==="
echo "Application should now be accessible at: http://15.152.37.134/"
echo "Admin dashboard: http://15.152.37.134/admin-dashboard/"
echo "Map embed: http://15.152.37.134/embed/"
echo "Django admin: http://15.152.37.134/admin/ (admin/admin123)"

echo ""
echo "To check logs:"
echo "  Django: sudo journalctl -u demomap -f"
echo "  Nginx: sudo tail -f /var/log/nginx/error.log"

echo ""
echo "To restart services:"
echo "  sudo systemctl restart demomap"
echo "  sudo systemctl restart nginx"