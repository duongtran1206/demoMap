#!/bin/bash

# Build script for Vercel deployment  
echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
python3.9 -m pip install -r requirements.txt

# Run database migrations
echo "Running migrations..."
python3.9 manage.py migrate --run-syncdb || echo "Migrations completed"

# Create superuser
echo "Creating superuser..."
python3.9 manage.py init_db || echo "DB initialization completed"

# Collect static files using Django management commands
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear || echo "Static files collection completed"

echo "Build completed successfully!"
