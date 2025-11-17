#!/bin/bash

# Script to reset all configurations for Django GeoMap project on EC2
# Usage: sudo ./reset_ec2.sh

echo "=== Resetting EC2 Configuration for Django GeoMap ==="

# Stop and disable services
echo "Stopping and disabling services..."
sudo systemctl stop demomap 2>/dev/null || true
sudo systemctl disable demomap 2>/dev/null || true
sudo systemctl stop nginx 2>/dev/null || true

# Remove systemd service file
echo "Removing systemd service file..."
sudo rm -f /etc/systemd/system/demomap.service

# Remove nginx configuration
echo "Removing nginx configuration..."
sudo rm -f /etc/nginx/sites-available/demomap
sudo rm -f /etc/nginx/sites-enabled/demomap

# Enable default nginx site
echo "Enabling default nginx site..."
sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default 2>/dev/null || true

# Reload systemd daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Clean up any running processes
echo "Cleaning up running processes..."
sudo pkill -f gunicorn 2>/dev/null || true
sudo pkill -f "manage.py runserver" 2>/dev/null || true

# Clean up log files
echo "Cleaning up log files..."
sudo rm -f /demoMap/django.log 2>/dev/null || true
sudo rm -f /var/log/nginx/demomap_error.log 2>/dev/null || true
sudo rm -f /var/log/nginx/demomap_access.log 2>/dev/null || true

# Clean up database and collected static files
echo "Cleaning up database and static files..."
sudo rm -f /demoMap/db.sqlite3 2>/dev/null || true
sudo rm -rf /demoMap/staticfiles/* 2>/dev/null || true

# Reset permissions (will be set properly in deploy script)
echo "Resetting basic permissions..."
sudo chown -R ubuntu:ubuntu /demoMap/ 2>/dev/null || true

# Restart nginx
echo "Restarting nginx..."
sudo systemctl restart nginx 2>/dev/null || true

echo "=== Reset Complete ==="
echo ""
echo "To deploy the application:"
echo "  cd /demoMap"
echo "  sudo ./start_service.sh"