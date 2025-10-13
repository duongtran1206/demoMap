#!/bin/bash

# Script to reset all configurations for Django GeoMap project on EC2
# Usage: ./reset_ec2.sh [domain]
# If domain is provided, it will configure SSL for that domain

DOMAIN=""
if [ $# -eq 1 ]; then
    DOMAIN=$1
    echo "Domain provided: $DOMAIN"
    echo "SSL will be configured for this domain after reset"
fi

echo "=== Resetting EC2 Configuration for Django GeoMap ==="

# Stop and disable services
echo "Stopping and disabling services..."
sudo systemctl stop demomap 2>/dev/null || true
sudo systemctl disable demomap 2>/dev/null || true
sudo systemctl stop nginx 2>/dev/null || true
sudo systemctl disable nginx 2>/dev/null || true

# Remove systemd service file
echo "Removing systemd service file..."
sudo rm -f /etc/systemd/system/demomap.service

# Remove nginx configuration
echo "Removing nginx configuration..."
sudo rm -f /etc/nginx/sites-available/demomap
sudo rm -f /etc/nginx/sites-enabled/demomap

# Remove SSL certificates (for HTTPS reset)
echo "Removing SSL certificates..."
if [ -n "$DOMAIN" ]; then
    sudo rm -rf /etc/letsencrypt/live/$DOMAIN 2>/dev/null || true
    sudo rm -rf /etc/letsencrypt/archive/$DOMAIN 2>/dev/null || true
    sudo rm -rf /etc/letsencrypt/renewal/$DOMAIN.conf 2>/dev/null || true
    echo "Removed SSL certificates for domain: $DOMAIN"
else
    # Remove any existing certificates
    sudo rm -rf /etc/letsencrypt/live/* 2>/dev/null || true
    sudo rm -rf /etc/letsencrypt/archive/* 2>/dev/null || true
    sudo rm -rf /etc/letsencrypt/renewal/*.conf 2>/dev/null || true
    echo "Removed all existing SSL certificates"
fi

# Remove self-signed certificates if they exist
sudo rm -f /etc/ssl/certs/selfsigned.crt 2>/dev/null || true
sudo rm -f /etc/ssl/private/selfsigned.key 2>/dev/null || true

# Remove project directory (optional - uncomment if needed)
# echo "Removing project directory..."
# sudo rm -rf /home/ubuntu/demoMap

# Clean up any existing virtual environment (optional)
# echo "Removing virtual environment..."
# sudo rm -rf /home/ubuntu/demoMap/venv

# Reset nginx to default
echo "Resetting nginx to default configuration..."
if [ -d "/etc/nginx/sites-available" ] && [ -d "/etc/nginx/sites-enabled" ]; then
    sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup 2>/dev/null || true
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/ 2>/dev/null || true
fi

# Reload systemd daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Clean up any running processes
echo "Cleaning up running processes..."
pkill -f gunicorn 2>/dev/null || true
pkill -f "manage.py runserver" 2>/dev/null || true

# Clean up log files
echo "Cleaning up log files..."
sudo rm -f /home/ubuntu/demoMap/django.log
sudo rm -f /var/log/nginx/demomap_error.log
sudo rm -f /var/log/nginx/demomap_access.log

# Reset permissions (will be set properly in deploy script)
echo "Resetting basic permissions..."
sudo chown -R ubuntu:ubuntu /home/ubuntu/demoMap/ 2>/dev/null || true

# Save domain configuration if provided
if [ -n "$DOMAIN" ]; then
    echo "Saving domain configuration..."
    echo "DOMAIN=$DOMAIN" > /home/ubuntu/demoMap/.domain_config
    echo "EMAIL=admin@$DOMAIN" >> /home/ubuntu/demoMap/.domain_config
    echo "Domain configuration saved to /home/ubuntu/demoMap/.domain_config"
fi

echo "=== Reset Complete ==="
if [ -n "$DOMAIN" ]; then
    echo "Domain configured: $DOMAIN"
    echo "SSL certificates will be obtained when you run: sudo ./start_service.sh"
    echo ""
    echo "To start the service with SSL:"
    echo "  sudo ./start_service.sh"
else
    echo "No domain specified. Will use IP address with self-signed SSL."
    echo "To configure domain SSL, run: sudo ./reset_ec2.sh yourdomain.com"
    echo ""
    echo "To start the service:"
    echo "  sudo ./start_service.sh"
fi