#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

from maps.models import GeoJSONFile, MapLayer
from maps.views import map_data_api
from django.test import RequestFactory
import json

print("=== Testing map_data_api function ===")

# Create a request
request = RequestFactory().get('/api/map-data/')

# Call the API function
response = map_data_api(request)

# Parse the JSON response
data = json.loads(response.content.decode('utf-8'))

print(f"API Response Status: {response.status_code}")
print(f"API Response Content Type: {response.get('Content-Type')}")

print(f"\nLayers count: {len(data.get('layers', []))}")
print(f"Last updated: {data.get('last_updated')}")

if data['layers']:
    print("\nLayers in API response:")
    for layer in data['layers']:
        print(f"  - ID: {layer.get('id')}")
        print(f"    Name: {layer.get('name')}")
        print(f"    Color: {layer.get('color')}")
        print(f"    Visible: {layer.get('is_visible')}")
        print(f"    Feature count: {layer.get('feature_count')}")
        print(f"    GeoJSON features: {len(layer.get('geojson', {}).get('features', []))}")
        print()
else:
    print("No layers in API response!")
    
    # Debug: check database directly
    print("\n=== Database Debug ===")
    print(f"Total GeoJSONFiles: {GeoJSONFile.objects.count()}")
    print(f"Active GeoJSONFiles: {GeoJSONFile.objects.filter(is_active=True).count()}")
    print(f"Total MapLayers: {MapLayer.objects.count()}")
    
    # List all files
    for geojson_file in GeoJSONFile.objects.filter(is_active=True):
        print(f"\nGeoJSON File ID={geojson_file.id}:")
        print(f"  Name: {geojson_file.name}")
        print(f"  File: {geojson_file.file.name if geojson_file.file else 'No file'}")
        print(f"  Is Active: {geojson_file.is_active}")
        print(f"  Has GeoJSON data: {geojson_file.geojson_data is not None}")
        
        # Check associated MapLayers
        layers = MapLayer.objects.filter(geojson_file=geojson_file)
        print(f"  Associated MapLayers: {layers.count()}")
        for layer in layers:
            print(f"    Layer ID={layer.id}, Visible={layer.is_visible}")