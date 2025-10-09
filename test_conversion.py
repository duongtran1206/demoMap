#!/usr/bin/env python
import json
import io

def convert_custom_json_to_geojson(custom_data):
    """Convert custom JSON format to GeoJSON FeatureCollection"""
    if 'locations' not in custom_data:
        return custom_data  # Already GeoJSON
    
    features = []
    for location in custom_data['locations']:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [location['longitude'], location['latitude']]
            },
            "properties": {
                "name": location['name'],
                "display_name": location.get('display_name', location['name'])
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

# Test the conversion
with open('test_custom_locations.json', 'r', encoding='utf-8') as f:
    custom_data = json.load(f)

geojson_data = convert_custom_json_to_geojson(custom_data)

print("Converted GeoJSON:")
print(json.dumps(geojson_data, indent=2, ensure_ascii=False))

# Save to file
with open('converted_test.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, indent=2, ensure_ascii=False)

print("Saved to converted_test.geojson")