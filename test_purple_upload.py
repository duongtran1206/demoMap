#!/usr/bin/env python
import requests
import json

# Test với màu tím
test_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Test Purple Location"},
            "geometry": {
                "type": "Point", 
                "coordinates": [106.9, 10.7]
            }
        }
    ]
}

with open('test_purple.geojson', 'w') as f:
    json.dump(test_geojson, f)

print("Testing purple color upload...")

url = 'http://localhost:8000/api/geojson-files/'
data = {
    'name': 'Test Purple File',
    'description': 'File with purple color',
    'color': '#8B00FF'  # Màu tím
}

auth = ('admin', 'admin123')

with open('test_purple.geojson', 'rb') as f:
    files = {'file': f}
    try:
        response = requests.post(url, data=data, files=files, auth=auth)
        print(f"Upload response: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Purple file created: {result['name']} with color {result['color']}")
        else:
            print(f"✗ Upload failed: {response.text}")
    
    except Exception as e:
        print(f"✗ Error: {e}")

# Cleanup
import os
if os.path.exists('test_purple.geojson'):
    os.remove('test_purple.geojson')