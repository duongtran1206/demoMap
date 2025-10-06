#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

from maps.models import GeoJSONFile

def check_files():
    print("=== CHECK FILE PATHS ===")
    
    files = GeoJSONFile.objects.all()
    for f in files:
        print(f"\nFile: {f.name} (ID: {f.id})")
        print(f"  File field: {f.file}")
        if f.file:
            print(f"  File path: {f.file.path}")
            print(f"  File exists: {os.path.exists(f.file.path) if f.file.path else 'No path'}")
            if f.file.path and os.path.exists(f.file.path):
                print(f"  File size: {os.path.getsize(f.file.path)} bytes")
                try:
                    with open(f.file.path, 'r') as file:
                        content = file.read()
                        print(f"  Content length: {len(content)}")
                        print(f"  First 100 chars: {content[:100]}")
                except Exception as e:
                    print(f"  Error reading file: {e}")
        else:
            print("  No file attached!")

if __name__ == '__main__':
    check_files()