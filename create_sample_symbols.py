#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

from maps.models import CustomSymbol

def create_sample_symbols():
    """Create sample custom symbols for testing"""

    # Create some sample custom symbols
    symbols_data = [
        {'name': 'HWK Schraube', 'category': 'Hardware'},
        {'name': 'OIP Image', 'category': 'General'},
        {'name': 'Location Pin', 'category': 'Navigation'},
        {'name': 'Store Icon', 'category': 'Business'},
        {'name': 'Restaurant Marker', 'category': 'Food'},
        {'name': 'Hospital Icon', 'category': 'Healthcare'},
    ]

    for symbol_data in symbols_data:
        symbol, created = CustomSymbol.objects.get_or_create(
            name=symbol_data['name'],
            defaults={
                'category': symbol_data['category'],
                'is_active': True
            }
        )
        if created:
            print(f'Created symbol: {symbol.name}')
        else:
            print(f'Symbol already exists: {symbol.name}')

    print(f'Total symbols: {CustomSymbol.objects.count()}')

if __name__ == '__main__':
    create_sample_symbols()