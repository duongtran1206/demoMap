#!/usr/bin/env python
import requests
import json

response = requests.get('http://127.0.0.1:8000/api/geojson-files/')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = json.loads(response.text)
    print(f'Files found: {len(data)}')
    for f in data[:3]:
        print(f'ID: {f["id"]}, Name: {f["name"]}, Type: {f["map_type"]}')
else:
    print(f'Error: {response.text}')