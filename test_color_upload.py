#!/usr/bin/env python
import requests
import json

# Test tạo GeoJSON với màu tùy chỉnh
test_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Test Blue Location"},
            "geometry": {
                "type": "Point", 
                "coordinates": [106.8, 10.9]
            }
        }
    ]
}

# Tạo file tạm
with open('test_blue.geojson', 'w') as f:
    json.dump(test_geojson, f)

print("Testing color upload...")

# Test upload với màu xanh dương
url = 'http://localhost:8000/api/geojson-files/'
data = {
    'name': 'Test Blue File',
    'description': 'File with blue color',
    'color': '#0066FF'  # Màu xanh dương
}

auth = ('admin', 'admin123')

with open('test_blue.geojson', 'rb') as f:
    files = {'file': f}
    try:
        response = requests.post(url, data=data, files=files, auth=auth)
        print(f"Upload response: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✓ File created successfully!")
            print(f"  ID: {result['id']}")
            print(f"  Name: {result['name']}")
            print(f"  Color: {result['color']}")
            
            # Test API để xem màu có được trả về đúng không
            map_response = requests.get('http://localhost:8000/api/map-data/')
            if map_response.status_code == 200:
                map_data = map_response.json()
                for layer in map_data['layers']:
                    if layer['name'] == 'Test Blue File':
                        print(f"✓ Layer color in API: {layer['color']}")
                        break
        else:
            print(f"✗ Upload failed: {response.text}")
    
    except Exception as e:
        print(f"✗ Error: {e}")

# Cleanup
import os
if os.path.exists('test_blue.geojson'):
    os.remove('test_blue.geojson')