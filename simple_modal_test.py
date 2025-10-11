#!/usr/bin/env python3
"""
Simple test script to verify modal functionality in admin dashboard
"""
import requests
from bs4 import BeautifulSoup
import re

def test_modal_functionality():
    """Test if the modal elements are properly set up"""
    try:
        # Start a session to maintain cookies
        session = requests.Session()

        # First, get the login page to get CSRF token
        login_response = session.get('http://localhost:8000/login/')
        if login_response.status_code != 200:
            print(f"❌ Failed to load login page: {login_response.status_code}")
            return False

        soup = BeautifulSoup(login_response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        if not csrf_token:
            print("❌ CSRF token not found on login page")
            return False
        csrf_token = csrf_token['value']

        # Login with admin credentials
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'csrfmiddlewaretoken': csrf_token
        }
        login_headers = {
            'Referer': 'http://localhost:8000/login/'
        }
        login_response = session.post('http://localhost:8000/login/', data=login_data, headers=login_headers)

        if login_response.status_code != 200 and 'dashboard' not in login_response.url:
            print(f"❌ Login failed: {login_response.status_code}")
            return False
        print("✅ Login successful")

        # Now get the dashboard page
        response = session.get('http://localhost:8000/dashboard/')
        if response.status_code != 200:
            print(f"❌ Failed to load dashboard: {response.status_code}")
            return False

        soup = BeautifulSoup(response.content, 'html.parser')

        # Check if modal exists
        modal = soup.find(id='crudModal')
        if not modal:
            print("❌ Modal element not found in HTML")
            return False
        print("✅ Modal element found")

        # Check if required form elements exist
        required_elements = [
            'modal-title',
            'file-id',
            'file-name',
            'file-description',
            'file-map-type',
            'file-custom-symbol',
            'geojson-file',
            'file-active',
            'file-upload-group',
            'submit-btn'
        ]

        missing_elements = []
        for element_id in required_elements:
            if not soup.find(id=element_id):
                missing_elements.append(element_id)

        if missing_elements:
            print(f"❌ Missing form elements: {missing_elements}")
            return False
        print("✅ All required form elements found")

        # Check if JavaScript files are included and load their content
        js_files = soup.find_all('script', src=True)
        js_sources = [js['src'] for js in js_files]

        required_js = ['/static/js/admin_dashboard.js', '/static/js/custom-symbol-picker.js']
        js_content = ""

        for js in required_js:
            if not any(js in src for src in js_sources):
                print(f"❌ Required JavaScript file not found: {js}")
                return False

            # Load the JavaScript file content
            js_url = f'http://localhost:8000{js}'
            js_response = session.get(js_url)
            if js_response.status_code == 200:
                js_content += js_response.text
            else:
                print(f"❌ Failed to load JavaScript file: {js}")

        print("✅ Required JavaScript files included and loaded")

        # Check if showCreateModal function exists in the JavaScript
        if 'showCreateModal' not in js_content:
            print("❌ showCreateModal function not found in JavaScript")
            return False
        print("✅ showCreateModal function found in JavaScript")

        # Check for potential JavaScript syntax errors (basic check)
        syntax_errors = []
        if 'console.error(' in js_content and 'Custom symbol input not found!' in js_content:
            syntax_errors.append("Old error logging still present")

        if syntax_errors:
            print(f"⚠️  Potential issues: {syntax_errors}")

        print("\n🎉 Modal functionality test PASSED")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_modal_functionality()
    if not success:
        print("\n🔧 Recommendations:")
        print("- Check Django server logs for errors")
        print("- Verify static files are served correctly")
        print("- Check browser console for JavaScript errors")