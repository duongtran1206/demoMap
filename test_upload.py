#!/usr/bin/env python
import requests
import json

def test_upload():
    # Login first
    session = requests.Session()
    
    # Get CSRF token from login page
    login_page = session.get('http://127.0.0.1:8000/login/')
    print(f"Login page status: {login_page.status_code}")
    
    # Login
    login_data = {
        'username': 'admin',
        'password': 'admin123',
        'csrfmiddlewaretoken': session.cookies.get('csrftoken', '')
    }
    
    login_response = session.post('http://127.0.0.1:8000/login/', data=login_data)
    print(f"Login response status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print("Login failed")
        return
    
    # Test upload
    files = {'file': open('test_custom_locations.json', 'rb')}
    data = {
        'name': 'Custom Locations Test',
        'description': 'Test upload via API with custom JSON format',
        'is_active': 'true'
    }
    
    headers = {
        'X-CSRFToken': session.cookies.get('csrftoken', '')
    }
    
    response = session.post('http://127.0.0.1:8000/api/geojson-files/', 
                           files=files, data=data, headers=headers)
    
    print(f"Upload response status: {response.status_code}")
    print(f"Response content: {response.text}")

if __name__ == '__main__':
    test_upload()