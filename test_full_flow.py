#!/usr/bin/env python
import requests
import json

# Test data
test_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "API Test Location"},
            "geometry": {
                "type": "Point", 
                "coordinates": [106.7, 10.8]
            }
        }
    ]
}

# Create a temporary file
with open('api_test.geojson', 'w') as f:
    json.dump(test_geojson, f)

print("Testing file upload via API...")

# Test the upload
url = 'http://localhost:8000/api/geojson-files/'
data = {
    'name': 'API Test File',
    'description': 'File uploaded via API test',
    'color': '#00FF00'
}

# Use basic auth for admin user
auth = ('admin', 'admin123')  # Adjust credentials as needed

with open('api_test.geojson', 'rb') as f:
    files = {'file': f}
    try:
        response = requests.post(url, data=data, files=files, auth=auth)
        print(f"Upload response: {response.status_code}")
        print(f"Upload response body: {response.text}")
        
        if response.status_code == 201:
            print("✓ Upload successful!")
            
            # Test the map-data API
            map_data_response = requests.get('http://localhost:8000/api/map-data/')
            print(f"\nMap data API response: {map_data_response.status_code}")
            
            if map_data_response.status_code == 200:
                data = map_data_response.json()
                print(f"✓ Map data API working - {len(data['layers'])} layers returned")
                
                # Look for our uploaded file
                for layer in data['layers']:
                    if 'API Test File' in layer['name']:
                        print(f"✓ Found uploaded file: {layer['name']}")
                        print(f"  Features: {len(layer['geojson']['features'])}")
                        break
                else:
                    print("✗ Uploaded file not found in API response")
            else:
                print(f"✗ Map data API error: {map_data_response.text}")
        else:
            print("✗ Upload failed!")
    
    except requests.exceptions.ConnectionError:
        print("✗ Connection error - is the Django server running on localhost:8000?")
    except Exception as e:
        print(f"✗ Error: {e}")

# Cleanup
import os
if os.path.exists('api_test.geojson'):
    os.remove('api_test.geojson')