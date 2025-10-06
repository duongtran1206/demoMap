#!/usr/bin/env python
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

from maps.models import GeoJSONFile, MapLayer
from django.core.files.uploadedfile import SimpleUploadedFile

# Test GeoJSON content
test_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Test Point"},
            "geometry": {
                "type": "Point",
                "coordinates": [105.123, 21.456]
            }
        }
    ]
}

print("Creating test GeoJSON file...")

# Create a mock uploaded file
json_content = json.dumps(test_geojson)
uploaded_file = SimpleUploadedFile(
    "test_point.geojson",
    json_content.encode('utf-8'),
    content_type="application/json"
)

# Create GeoJSONFile instance
geojson_file = GeoJSONFile.objects.create(
    name="Test Point File",
    description="Test file created via script",
    file=uploaded_file
)

print(f"Created GeoJSONFile: ID={geojson_file.id}, Name={geojson_file.name}")
print(f"File path: {geojson_file.file.path if geojson_file.file else 'None'}")

# Check if MapLayer was created
map_layers = MapLayer.objects.filter(geojson_file=geojson_file)
print(f"Associated MapLayers: {map_layers.count()}")

for layer in map_layers:
    print(f"  Layer ID={layer.id}, GeoJSON Name={layer.geojson_file.name}, Visible={layer.is_visible}")

# Test geojson_data property
print(f"GeoJSON data available: {geojson_file.geojson_data is not None}")
if geojson_file.geojson_data:
    print(f"GeoJSON data keys: {list(geojson_file.geojson_data.keys())}")
    print(f"Features count: {len(geojson_file.geojson_data.get('features', []))}")
else:
    print("GeoJSON data is None!")
    print(f"File exists: {geojson_file.file.name if geojson_file.file else 'No file'}")

# Test the API endpoint data
from maps.views import MapDataViewSet
from django.test import RequestFactory
from django.contrib.auth.models import User

request = RequestFactory().get('/api/map-data/')
viewset = MapDataViewSet()
viewset.request = request

try:
    data = viewset.get_map_data(request)
    print(f"\nAPI Response layers count: {len(data.data.get('layers', []))}")
    if data.data['layers']:
        print("Layers in API response:")
        for layer in data.data['layers']:
            print(f"  - ID: {layer.get('id')}, Name: {layer.get('name')}, Visible: {layer.get('is_visible')}")
    else:
        print("No layers in API response")
except Exception as e:
    print(f"API test error: {e}")