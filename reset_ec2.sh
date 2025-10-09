#!/bin/bash

# Script to reset all configurations for Django GeoMap project on EC2
# This will remove all existing configurations and prepare for fresh deployment

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

# Remove project directory (optional - uncomment if needed)
# echo "Removing project directory..."
# sudo rm -rf /home/ubuntu/demoMap

# Clean up any existing virtual environment (optional)
# echo "Removing virtual environment..."
# sudo rm -rf /home/ubuntu/demoMap/venv

# Reset nginx to default
echo "Resetting nginx to default configuration..."
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup 2>/dev/null || true
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

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

echo "=== Reset Complete ==="
echo "You can now run the deploy script: sudo ./deploy_ec2.sh"
echo "Or run the start service script: sudo ./start_service.sh"