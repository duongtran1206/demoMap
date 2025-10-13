#!/usr/bin/env python
"""
Test script to verify JSON editor authentication
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_get_json_content():
    """Test GET request (should work without auth)"""
    try:
        # Assuming file_id 1 exists
        response = requests.get(f'{BASE_URL}/api/json-editor/111/')
        print(f'GET /api/json-editor/111/ - Status: {response.status_code}')
        if response.status_code == 200:
            print('✓ Public viewing works')
        else:
            print(f'✗ Public viewing failed: {response.text}')
    except Exception as e:
        print(f'✗ GET request failed: {e}')

def test_add_feature_unauthenticated():
    """Test POST request without auth (should fail)"""
    try:
        data = {
            "type": "Feature",
            "properties": {"name": "Test Point"},
            "geometry": {"type": "Point", "coordinates": [8.0, 50.0]}
        }
        response = requests.post(f'{BASE_URL}/api/json-editor/111/add/', json=data)
        print(f'POST /api/json-editor/111/add/ (unauthenticated) - Status: {response.status_code}')
        if response.status_code == 401 or response.status_code == 403:
            print('✓ Authentication required for editing (good)')
        else:
            print(f'✗ Authentication not enforced: {response.text}')
    except Exception as e:
        print(f'✗ POST request failed: {e}')

def test_delete_feature_unauthenticated():
    """Test DELETE request without auth (should fail)"""
    try:
        response = requests.delete(f'{BASE_URL}/api/json-editor/111/delete/0/')
        print(f'DELETE /api/json-editor/111/delete/0/ (unauthenticated) - Status: {response.status_code}')
        if response.status_code == 401 or response.status_code == 403:
            print('✓ Authentication required for editing (good)')
        else:
            print(f'✗ Authentication not enforced: {response.text}')
    except Exception as e:
        print(f'✗ DELETE request failed: {e}')

if __name__ == '__main__':
    print('Testing JSON Editor Authentication...')
    test_get_json_content()
    test_add_feature_unauthenticated()
    test_delete_feature_unauthenticated()
    print('Test completed.')