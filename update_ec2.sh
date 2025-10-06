#!/bin/bash

# Quick update script for EC2
echo "Updating Django GeoMap on EC2..."

cd /home/ubuntu/demoMap

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Run migrations if needed
python manage.py migrate --settings=geomap_project.production_settings

# Collect static files
python manage.py collectstatic --noinput --settings=geomap_project.production_settings

# Restart services
sudo systemctl restart demomap
sudo systemctl restart nginx

echo "Update completed!"
echo "Check status: sudo systemctl status demomap"