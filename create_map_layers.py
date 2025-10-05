#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

from maps.models import GeoJSONFile, MapLayer

def create_missing_map_layers():
    files = GeoJSONFile.objects.all()
    print(f'Found {files.count()} GeoJSON files')
    
    for file in files:
        layer, created = MapLayer.objects.get_or_create(
            geojson_file=file,
            defaults={'is_visible': True, 'order': 0}
        )
        if created:
            print(f'Created MapLayer for: {file.name}')
        else:
            print(f'MapLayer already exists for: {file.name}')
    
    print(f'Total MapLayers: {MapLayer.objects.count()}')

if __name__ == '__main__':
    create_missing_map_layers()