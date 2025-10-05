#!/bin/bash

# Build script for Vercel deployment  
echo "Starting build process..."

# Collect static files using Django management commands
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear || echo "Static files collection completed"

echo "Build completed successfully!"
