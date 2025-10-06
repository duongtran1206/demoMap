#!/bin/bash

# Quick update script for EC2
echo "Updating Django GeoMap on EC2..."

cd /home/ubuntu/demoMap

# Remove staticfiles to avoid merge conflicts
sudo rm -rf staticfiles/

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Run migrations if needed
python manage.py migrate --settings=geomap_project.production_settings

# Collect static files
python manage.py collectstatic --noinput --settings=geomap_project.production_settings

# Set proper permissions
sudo chown -R ubuntu:www-data /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/staticfiles/

# Restart services
sudo systemctl restart demomap
sudo systemctl restart nginx

echo "Update completed!"
echo "Check status: sudo systemctl status demomap"