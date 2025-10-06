#!/bin/bash

# Fix git merge conflict with staticfiles
echo "Fixing git merge conflict..."

cd /home/ubuntu/demoMap

# Remove conflicting staticfiles
echo "Removing staticfiles directory..."
sudo rm -rf staticfiles/

# Reset git state
git reset --hard HEAD
git clean -fd

# Pull latest changes
echo "Pulling latest changes..."
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear --settings=geomap_project.production_settings

# Set proper permissions
echo "Setting permissions..."
sudo chown -R ubuntu:www-data /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/staticfiles/

# Restart services
echo "Restarting services..."
sudo systemctl restart demomap
sudo systemctl restart nginx

echo "Fix completed!"
echo "Check status: sudo systemctl status demomap nginx"