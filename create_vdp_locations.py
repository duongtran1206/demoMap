#!/usr/bin/env python
"""
Script to create VDP locations GeoJSON file
"""
import os
import sys
import django
from django.core.files import File

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

from maps.models import GeoJSONFile, CustomSymbol

def create_vdp_locations():
    """Create VDP locations GeoJSON file"""

    # Check if file exists
    geojson_path = 'vdp_locations.geojson'
    if not os.path.exists(geojson_path):
        print(f"❌ File {geojson_path} not found")
        return

    # Get Caritas symbol
    try:
        caritas_symbol = CustomSymbol.objects.get(name='Caritas')
        print(f"✅ Found symbol: {caritas_symbol.name} (ID: {caritas_symbol.id})")
    except CustomSymbol.DoesNotExist:
        print("❌ Caritas symbol not found")
        return

    # Create GeoJSON file record
    try:
        with open(geojson_path, 'rb') as f:
            # Create GeoJSONFile
            geojson_file = GeoJSONFile.objects.create(
                name='VDP Service Points',
                description='VDP Personal service locations in Vietnam',
                color='#007bff',  # Blue color
                custom_symbol=caritas_symbol,
                map_type='embed',
                is_active=True
            )

            # Save file
            geojson_file.file.save('vdp_locations.geojson', File(f))
            geojson_file.save()

            print(f"✅ Created GeoJSON file: {geojson_file.name}")
            print(f"   - ID: {geojson_file.id}")
            print(f"   - Features: {geojson_file.feature_count}")
            print(f"   - Symbol: {caritas_symbol.name}")
            print(f"   - Color: {geojson_file.color}")

    except Exception as e:
        print(f"❌ Error creating GeoJSON file: {e}")

if __name__ == '__main__':
    print("Creating VDP Locations...")
    create_vdp_locations()
    print("Done!")