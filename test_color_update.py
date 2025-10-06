#!/usr/bin/env python
import requests

# Test cập nhật màu cho file existing
print("Testing color update...")

# Lấy danh sách files
url = 'http://localhost:8000/api/geojson-files/'
auth = ('admin', 'admin123')

try:
    # Get existing files
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        files = response.json()
        
        if files:
            # Lấy file đầu tiên để test update
            file_to_update = files[0]
            print(f"Updating file: {file_to_update['name']}")
            print(f"Current color: {file_to_update.get('color', 'No color')}")
            
            # Update với màu mới
            update_data = {
                'color': '#00FF80'  # Màu xanh lá
            }
            
            update_url = f"{url}{file_to_update['id']}/"
            update_response = requests.patch(update_url, json=update_data, auth=auth)
            
            print(f"Update response: {update_response.status_code}")
            
            if update_response.status_code == 200:
                updated_file = update_response.json()
                print(f"✓ Color updated to: {updated_file['color']}")
                
                # Verify in map-data API
                map_response = requests.get('http://localhost:8000/api/map-data/')
                if map_response.status_code == 200:
                    map_data = map_response.json()
                    for layer in map_data['layers']:
                        if layer['id'] == file_to_update['id']:
                            print(f"✓ Map API shows color: {layer['color']}")
                            break
            else:
                print(f"✗ Update failed: {update_response.text}")
        else:
            print("No files found to update")
    else:
        print(f"✗ Failed to get files: {response.text}")

except Exception as e:
    print(f"✗ Error: {e}")