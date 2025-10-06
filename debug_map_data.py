#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

from maps.models import GeoJSONFile, MapLayer

def debug_map_data():
    print("=== DEBUG MAP DATA API ===")
    
    # Check GeoJSON Files
    files = GeoJSONFile.objects.all()
    print(f"\n1. GeoJSON Files ({files.count()}):")
    for f in files:
        print(f"   ID: {f.id}, Name: {f.name}")
        print(f"   Active: {f.is_active}")
        print(f"   Has geojson_data: {bool(f.geojson_data)}")
        if f.geojson_data:
            print(f"   Features count: {len(f.geojson_data.get('features', []))}")
        print()
    
    # Check MapLayers
    layers = MapLayer.objects.all()
    print(f"\n2. Map Layers ({layers.count()}):")
    for l in layers:
        print(f"   ID: {l.id}, File: {l.geojson_file.name}")
        print(f"   Visible: {l.is_visible}")
        print(f"   File Active: {l.geojson_file.is_active}")
        print()
    
    # Check the exact query used in map_data_api
    filtered_layers = MapLayer.objects.filter(
        geojson_file__is_active=True
    ).select_related('geojson_file').prefetch_related('feature_visibilities')
    
    print(f"\n3. Filtered Layers for API ({filtered_layers.count()}):")
    for layer in filtered_layers:
        print(f"   ID: {layer.id}, Name: {layer.geojson_file.name}")
        print(f"   File Active: {layer.geojson_file.is_active}")
        print(f"   Layer Visible: {layer.is_visible}")
        
        geojson_data = layer.geojson_file.geojson_data
        if geojson_data and 'features' in geojson_data:
            print(f"   Features in file: {len(geojson_data['features'])}")
            
            # Check feature visibilities
            feature_visibilities = {fv.feature_index: fv.is_visible for fv in layer.feature_visibilities.all()}
            print(f"   Feature visibilities: {feature_visibilities}")
            
            # Count visible features
            visible_count = 0
            for index, feature in enumerate(geojson_data['features']):
                is_visible = feature_visibilities.get(index, True)
                if layer.is_visible and is_visible:
                    visible_count += 1
            
            print(f"   Visible features: {visible_count}")
        else:
            print(f"   No geojson_data or no features")
        print()

if __name__ == '__main__':
    debug_map_data()