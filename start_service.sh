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

# Load domain configuration if exists
if [ -f "$PROJECT_DIR/.domain_config" ]; then
    echo "Loading domain configuration from .domain_config..."
    source $PROJECT_DIR/.domain_config
    echo "Using domain: $DOMAIN"
    echo "Using email: $EMAIL"
else
    echo "No domain configuration found. Using IP address with self-signed SSL."
    # Try to get public IP
    DOMAIN=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "localhost")
    EMAIL="admin@localhost"
    echo "Using IP/domain: $DOMAIN"
fi

# Create virtual environment if it doesn't exist
echo "Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi

# Check if virtual environment was created successfully
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "Error: Failed to create virtual environment. Installing python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv
    python3 -m venv $VENV_DIR
fi

# Activate virtual environment and install/update requirements
echo "Installing/updating Python packages..."
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run Django migrations
echo "Running Django migrations..."
python3 manage.py migrate

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

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

# Check if nginx is installed
echo "Checking nginx installation..."
if ! command -v nginx &> /dev/null; then
    echo "Installing nginx..."
    sudo apt update
    sudo apt install -y nginx
fi

# Create nginx directories if they don't exist
echo "Creating nginx directories..."
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled
sudo tee /etc/nginx/sites-available/demomap > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    # SSL settings (will be updated by Certbot)
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

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

    location /admin-dashboard/ {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/demoMap/demomap.sock;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        client_max_body_size 100M;
    }

    location /embed/ {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/demoMap/demomap.sock;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        client_max_body_size 100M;
    }

    location /embed_vn/ {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/demoMap/demomap.sock;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        client_max_body_size 100M;
    }

    location /editlayer/ {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/demoMap/demomap.sock;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        client_max_body_size 100M;
    }

    # Return blank page for all other URLs
    location / {
        return 200 "<!DOCTYPE html><html><head><title></title></head><body></body></html>";
        add_header Content-Type text/html;
    }
}
EOF

# Enable nginx site
echo "Enabling nginx site..."
sudo ln -sf /etc/nginx/sites-available/demomap /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "Testing nginx configuration..."
sudo nginx -t

# Reload nginx
echo "Reloading nginx..."
sudo systemctl reload nginx

# Install Certbot and get SSL certificate (only for real domains, not IP addresses)
if [[ $DOMAIN =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || [[ $DOMAIN == "localhost" ]]; then
    echo "Using IP address/localhost. Generating self-signed SSL certificate..."
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/selfsigned.key -out /etc/ssl/certs/selfsigned.crt -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
    echo "Self-signed SSL certificate generated successfully!"
else
    echo "Using domain: $DOMAIN. Obtaining Let's Encrypt SSL certificate..."
    # Install Certbot and get SSL certificate
    echo "Installing Certbot..."
    sudo apt install snapd -y
    sudo snap install core; sudo snap refresh core
    sudo snap install --classic certbot
    sudo ln -s /snap/bin/certbot /usr/bin/certbot

    echo "Obtaining SSL certificate for $DOMAIN..."
    sudo certbot certonly --standalone -d $DOMAIN --email $EMAIL --agree-tos --non-interactive

    # Set up automatic certificate renewal
    echo "Setting up automatic certificate renewal..."
    sudo crontab -l | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet"; } | sudo crontab -

    echo "HTTPS setup completed successfully!"
fi

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
curl -k -s -o /dev/null -w "%{http_code}" https://$DOMAIN/ | grep -q "200" && echo "✓ Application is running successfully over HTTPS!" || echo "✗ Application test failed"

echo "=== Service Start Complete ==="
echo "Application should now be accessible at: https://$DOMAIN/"
echo "Admin dashboard: https://$DOMAIN/admin-dashboard/"
echo "Map embed: https://$DOMAIN/embed/"
echo "Vietnamese embed: https://$DOMAIN/embed_vn/"
echo "Layer editor: https://$DOMAIN/editlayer/"
echo "Django admin: https://$DOMAIN/admin/ (admin/admin123)"
echo ""

if [[ $DOMAIN =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || [[ $DOMAIN == "localhost" ]]; then
    echo "⚠️  NOTE: Using self-signed SSL certificate for IP address access"
    echo "   Browser will show security warning - this is normal for IP-based HTTPS"
    echo "   For production, configure domain SSL with: sudo ./reset_ec2.sh yourdomain.com"
    echo ""
    echo "SSL Certificate Information:"
    echo "  Certificate type: Self-signed"
    echo "  Certificate location: /etc/ssl/certs/selfsigned.crt"
    echo "  Private key location: /etc/ssl/private/selfsigned.key"
else
    echo "✅ NOTE: Using Let's Encrypt SSL certificate for domain access"
    echo "   Full HTTPS encryption with trusted certificate"
    echo ""
    echo "SSL Certificate Information:"
    echo "  Certificate location: /etc/letsencrypt/live/$DOMAIN/"
    echo "  Auto-renewal: Daily at 12:00 via cron"
    echo "  To manually renew: sudo certbot renew"
fi

echo ""
echo "To check logs:"
echo "  Django: sudo journalctl -u demomap -f"
echo "  Nginx: sudo tail -f /var/log/nginx/error.log"

echo ""
echo "To restart services:"
echo "  sudo systemctl restart demomap"
echo "  sudo systemctl restart nginx"