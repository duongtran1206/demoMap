#!/bin/bash

# Script to start Django GeoMap project as a service on EC2
# HTTP only - no SSL (for demo purposes)

echo "=== Starting Django GeoMap Service on EC2 (HTTP Only) ==="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo: sudo ./start_service.sh"
    exit 1
fi

# Set variables
PROJECT_DIR="/demoMap"
VENV_DIR="$PROJECT_DIR/venv"
USER="ubuntu"
GROUP="www-data"

# Check if we're in the project directory
if [ ! -f "$PROJECT_DIR/manage.py" ]; then
    echo "Error: Project not found at $PROJECT_DIR"
    echo "Please ensure the project is cloned/moved to /demoMap/"
    exit 1
fi

cd $PROJECT_DIR

# Get public IP address
echo "Getting public IP address..."
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "localhost")
echo "Public IP: $PUBLIC_IP"

# Update system packages
echo "Updating system packages..."
apt update

# Install required system packages
echo "Installing required system packages..."
apt install -y python3 python3-pip python3-venv nginx

# Create virtual environment if it doesn't exist
echo "Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    sudo -u $USER python3 -m venv $VENV_DIR
fi

# Check if virtual environment was created successfully
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "Error: Failed to create virtual environment. Installing python3-venv..."
    apt install -y python3-venv
    sudo -u $USER python3 -m venv $VENV_DIR
fi

# Activate virtual environment and install/update requirements
echo "Installing/updating Python packages..."
sudo -u $USER $VENV_DIR/bin/pip install --upgrade pip
sudo -u $USER $VENV_DIR/bin/pip install -r requirements.txt

# Run Django migrations
echo "Running Django migrations..."
sudo -u $USER $VENV_DIR/bin/python manage.py migrate

# Create superuser if not exists
echo "Creating superuser..."
sudo -u $USER $VENV_DIR/bin/python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
PYEOF

# Collect static files
echo "Collecting static files..."
sudo -u $USER $VENV_DIR/bin/python manage.py collectstatic --noinput

# Create systemd service file
echo "Creating systemd service..."
cat > /etc/systemd/system/demomap.service << EOF
[Unit]
Description=Django GeoMap Application
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
Environment="DJANGO_SETTINGS_MODULE=geomap_project.settings"
ExecStart=$VENV_DIR/bin/gunicorn --workers 3 --bind unix:$PROJECT_DIR/demomap.sock geomap_project.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration (HTTP only)
echo "Creating nginx configuration (HTTP only)..."
cat > /etc/nginx/sites-available/demomap << EOF
server {
    listen 80 default_server;
    server_name $PUBLIC_IP localhost _;

    client_max_body_size 100M;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

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
        proxy_pass http://unix:$PROJECT_DIR/demomap.sock;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
EOF

# Enable nginx site
echo "Enabling nginx site..."
ln -sf /etc/nginx/sites-available/demomap /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "Testing nginx configuration..."
nginx -t

if [ $? -ne 0 ]; then
    echo "Error: Nginx configuration test failed!"
    exit 1
fi

# Set proper permissions
echo "Setting permissions..."
chown -R $USER:$GROUP $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
chmod -R 755 $PROJECT_DIR/staticfiles/
chmod -R 755 $PROJECT_DIR/media/

# Allow nginx to access socket
usermod -a -G $GROUP $USER 2>/dev/null || true

# Reload systemd daemon
systemctl daemon-reload

# Stop any existing services
echo "Stopping existing services..."
systemctl stop demomap 2>/dev/null || true

# Start and enable services
echo "Starting services..."
systemctl start demomap
systemctl enable demomap
systemctl restart nginx
systemctl enable nginx

# Wait a moment for services to start
sleep 3

# Check service status
echo ""
echo "=== Service Status ==="
systemctl status demomap --no-pager -l | head -20
echo ""
systemctl status nginx --no-pager -l | head -15

# Test the application
echo ""
echo "=== Testing Application ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ Application is running successfully!"
else
    echo "✗ Application test returned HTTP code: $HTTP_CODE"
    echo "  Check logs: sudo journalctl -u demomap -n 50"
fi

echo ""
echo "=== Deployment Complete ==="
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Application URLs (HTTP only - for demo):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Access from browser:"
echo "   http://$PUBLIC_IP/"
echo "   http://$PUBLIC_IP/admin-dashboard/"
echo "   http://$PUBLIC_IP/embed/"
echo "   http://$PUBLIC_IP/embed_vn/"
echo "   http://$PUBLIC_IP/editlayer/"
echo "   http://$PUBLIC_IP/admin/"
echo ""
echo "👤 Admin credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📋 Useful commands:"
echo "   Check Django logs:  sudo journalctl -u demomap -f"
echo "   Check Nginx logs:   sudo tail -f /var/log/nginx/error.log"
echo "   Restart Django:     sudo systemctl restart demomap"
echo "   Restart Nginx:      sudo systemctl restart nginx"
echo "   Update code:        cd /demoMap && git pull && sudo ./start_service.sh"
echo ""
echo "⚠️  NOTE: This is HTTP only (no SSL) - suitable for demos"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"