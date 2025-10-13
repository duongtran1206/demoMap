# Django GeoMap Project# Django GeoMap Project



Một dự án Django chuyên nghiệp để quản lý và hiển thị bản đồ với dữ liệu GeoJSON. Bản đồ có thể nhúng vào các trang web khác với đầy đủ tính năng layer control.Một dự án Django chuyên nghiệp để quản lý và hiển thị bản đồ với dữ liệu GeoJSON. Bản đồ có thể nhúng vào các trang web khác với đầy đủ tính năng layer control.



## 🚀 Tính năng chính## 🚀 Tính năng chính



- **Admin Dashboard chuyên nghiệp**: Quản lý upload/delete GeoJSON files- **Admin Dashboard chuyên nghiệp**: Quản lý upload/delete GeoJSON files

- **Bản đồ nhúng được**: Có thể embed vào trang web khác- **Bản đồ nhúng được**: Có thể embed vào trang web khác

- **Layer Control tùy chỉnh**: Nằm bên phải bản đồ với các chức năng:- **Layer Control tùy chỉnh**: Nằm bên phải bản đồ với các chức năng:

  - Select All / Deselect All  - Select All / Deselect All

  - Hiển thị tên layer và số điểm  - Hiển thị tên layer và số điểm

  - Checkbox để bật/tắt từng layer  - Checkbox để bật/tắt từng layer

  - Màu sắc tùy chỉnh cho từng layer  - Màu sắc tùy chỉnh cho từng layer

- **API RESTful**: Hỗ trợ tích hợp với các hệ thống khác- **API RESTful**: Hỗ trợ tích hợp với các hệ thống khác

- **Responsive Design**: Tương thích mọi thiết bị- **Responsive Design**: Tương thích mọi thiết bị

- **5 Điểm trụ sở cố định**: Hiển thị với animation đẹp mắt- **5 Điểm trụ sở cố định**: Hiển thị với animation đẹp mắt



## 🛠️ Công nghệ sử dụng## 🛠️ Công nghệ sử dụng



- **Backend**: Django 5.2.7, Django REST Framework- **Backend**: Django 5.2.7, Django REST Framework

- **Frontend**: HTML5, CSS3, JavaScript ES6+- **Frontend**: HTML5, CSS3, JavaScript ES6+

- **Maps**: Leaflet.js, OpenStreetMap- **Maps**: Leaflet.js, OpenStreetMap

- **Database**: SQLite (có thể thay đổi)- **Database**: SQLite (có thể thay đổi)

- **File Upload**: Django FileField với validation- **File Upload**: Django FileField với validation



## 📋 Cài đặt và chạy## 📋 Cài đặt và chạy



### 1. Cài đặt dependencies### 1. Cài đặt dependencies



```bash```bash

pip install -r requirements.txtpip install -r requirements.txt

``````



### 2. Chạy migrations### 2. Chạy migrations



```bash```bash

python manage.py migratepython manage.py migrate

``````



### 3. Tạo superuser (tùy chọn)### 3. Tạo superuser (tùy chọn)



```bash```bash

python manage.py createsuperuserpython manage.py createsuperuser

``````



### 4. Chạy server development### 4. Chạy server development



```bash```bash

python manage.py runserverpython manage.py runserver

``````



### 5. Truy cập ứng dụng### 5. Truy cập ứng dụng



- **Admin Dashboard**: http://localhost:8000/admin/- **Admin Dashboard**: http://localhost:8000/admin/

  - Username: `admin`  - Username: `admin`

  - Password: `admin123`  - Password: `admin123`

- **Bản đồ nhúng**: http://localhost:8000/embed/- **Bản đồ nhúng**: http://localhost:8000/embed/

- **API**: http://localhost:8000/api/- **API**: http://localhost:8000/api/



## 🚀 Triển khai trên EC2## 🚀 Triển khai trên EC2



### Reset EC2 Configuration### Reset EC2 Configuration



Script `reset_ec2.sh` sẽ reset toàn bộ cấu hình EC2 về trạng thái ban đầu:Script `reset_ec2.sh` sẽ reset toàn bộ cấu hình EC2 về trạng thái ban đầu:



```bash```bash

# Đảm bảo script có quyền execute# Đảm bảo script có quyền execute

chmod +x reset_ec2.shchmod +x reset_ec2.sh



# Chạy script với quyền sudo# Chạy script với quyền sudo

sudo ./reset_ec2.shsudo ./reset_ec2.sh

``````



**Chức năng của reset_ec2.sh:****Chức năng của reset_ec2.sh:**

- Dừng và vô hiệu hóa services (demomap, nginx)- Dừng và vô hiệu hóa services (demomap, nginx)

- Xóa systemd service file- Xóa systemd service file

- Xóa nginx configuration- Xóa nginx configuration

- Clean up log files- Clean up log files

- Reset permissions- Reset permissions

- Reload systemd daemon- Reload systemd daemon



### Khởi động Service### Khởi động Service



Script `start_service.sh` sẽ khởi động lại toàn bộ service từ đầu:Script `start_service.sh` sẽ khởi động lại toàn bộ service từ đầu:



```bash```bash

# Đảm bảo script có quyền execute# Đảm bảo script có quyền execute

chmod +x start_service.shchmod +x start_service.sh



# Chạy script với quyền sudo# Chạy script với quyền sudo

sudo ./start_service.shsudo ./start_service.sh

``````



**Chức năng của start_service.sh:****Chức năng của start_service.sh:**

- Tạo/cập nhật Python virtual environment- Tạo/cập nhật Python virtual environment

- Cài đặt requirements từ `requirements.txt`- Cài đặt requirements từ `requirements.txt`

- Chạy Django migrations- Chạy Django migrations

- Collect static files- Collect static files

- Tạo systemd service cho Django- Tạo systemd service cho Django

- Cấu hình nginx- Cấu hình nginx

- Khởi động services- Khởi động services

- Test application- Test application



### Kiểm tra trạng thái services### Kiểm tra trạng thái services



```bash```bash

# Kiểm tra Django service# Kiểm tra Django service

sudo systemctl status demomapsudo systemctl status demomap



# Kiểm tra nginx# Kiểm tra nginx

sudo systemctl status nginxsudo systemctl status nginx



# Xem logs Django# Xem logs Django

sudo journalctl -u demomap -fsudo journalctl -u demomap -f



# Xem logs nginx# Xem logs nginx

sudo tail -f /var/log/nginx/error.logsudo tail -f /var/log/nginx/error.log

``````



### Khởi động lại services### Khởi động lại services



```bash```bash

# Restart Django# Restart Django

sudo systemctl restart demomapsudo systemctl restart demomap



# Restart nginx# Restart nginx

sudo systemctl restart nginxsudo systemctl restart nginx

``````



## 🎯 Cách sử dụng## 🎯 Cách sử dụng



### 1. Upload GeoJSON files### 1. Upload GeoJSON files



1. Truy cập admin dashboard: `/admin/`1. Truy cập admin dashboard: `/admin/`

2. Vào **Maps** > **GeoJSON Files**2. Vào **Maps** > **GeoJSON Files**

3. Click **Add GeoJSON File**3. Click **Add GeoJSON File**

4. Điền thông tin và upload file4. Điền thông tin và upload file

5. Chọn màu sắc và kích hoạt5. Chọn màu sắc và kích hoạt



### 2. Quản lý layers### 2. Quản lý layers



1. Trong admin, vào **Maps** > **Map Layers**1. Trong admin, vào **Maps** > **Map Layers**

2. Cài đặt visibility và order cho từng layer2. Cài đặt visibility và order cho từng layer



### 3. Nhúng bản đồ vào trang web khác### 3. Nhúng bản đồ vào trang web khác



```html```html

<iframe<iframe

    src="http://your-domain.com/embed/"    src="http://your-domain.com/embed/"

    width="100%"    width="100%"

    height="600px"    height="600px"

    frameborder="0"    frameborder="0"

    style="border: none;">    style="border: none;">

</iframe></iframe>

``````



## 📁 Cấu trúc dự án## 📁 Cấu trúc dự án



``````

geomap_project/geomap_project/

├── geomap_project/          # Django project settings├── geomap_project/          # Django project settings

├── maps/                    # Main app├── maps/                    # Main app

│   ├── models.py           # GeoJSONFile, MapLayer models│   ├── models.py           # GeoJSONFile, MapLayer models

│   ├── admin.py            # Admin interface customization│   ├── admin.py            # Admin interface customization

│   ├── views.py            # API views và embed view│   ├── views.py            # API views và embed view

│   ├── serializers.py      # DRF serializers│   ├── serializers.py      # DRF serializers

│   ├── urls.py             # URL routing│   ├── urls.py             # URL routing

│   └── templates/maps/│   └── templates/maps/

│       └── embed_new.html  # Embeddable map template│       └── embed_new.html  # Embeddable map template

├── static/                  # Static files├── static/                  # Static files

├── media/                   # Uploaded files├── media/                   # Uploaded files

├── manage.py               # Django management script├── manage.py               # Django management script

├── reset_ec2.sh            # EC2 reset script├── reset_ec2.sh            # EC2 reset script

├── start_service.sh        # Service start script├── start_service.sh        # Service start script

└── requirements.txt        # Python dependencies└── requirements.txt        # Python dependencies

``````



## 🔧 API Endpoints## 🔧 API Endpoints



- `GET /api/map-data/` - Lấy dữ liệu tất cả layers- `GET /api/map-data/` - Lấy dữ liệu tất cả layers

- `GET /api/geojson-files/` - Danh sách GeoJSON files- `GET /api/geojson-files/` - Danh sách GeoJSON files

- `GET /api/map-layers/` - Danh sách map layers- `GET /api/map-layers/` - Danh sách map layers

- `POST /api/map-layers/select_all/` - Chọn tất cả layers- `POST /api/map-layers/select_all/` - Chọn tất cả layers

- `POST /api/map-layers/deselect_all/` - Bỏ chọn tất cả layers- `POST /api/map-layers/deselect_all/` - Bỏ chọn tất cả layers

- `PATCH /api/map-layers/{id}/` - Cập nhật layer visibility- `PATCH /api/map-layers/{id}/` - Cập nhật layer visibility



## ⚙️ Tùy chỉnh## ⚙️ Tùy chỉnh



### Thay đổi base map### Thay đổi base map



Chỉnh sửa trong `embed_new.html`:Chỉnh sửa trong `embed_new.html`:

```javascript```javascript

const osmLayer = L.tileLayer('URL_CỦA_BẠN', {const osmLayer = L.tileLayer('URL_CỦA_BẠN', {

    attribution: 'Attribution của bạn'    attribution: 'Attribution của bạn'

});});

``````



### Thêm validation cho GeoJSON### Thêm validation cho GeoJSON



Chỉnh sửa trong `models.py`:Chỉnh sửa trong `models.py`:

```python```python

def clean(self):def clean(self):

    # Thêm validation logic    # Thêm validation logic

    pass    pass

``````



### Tùy chỉnh giao diện admin### Tùy chỉnh giao diện admin



Chỉnh sửa trong `admin.py`:Chỉnh sửa trong `admin.py`:

```python```python

class GeoJSONFileAdmin(admin.ModelAdmin):class GeoJSONFileAdmin(admin.ModelAdmin):

    # Thêm các tùy chỉnh    # Thêm các tùy chỉnh

    pass    pass

``````



## 🎨 Giao diện## 🎨 Giao diện



- **Professional Design**: Sử dụng Material Design principles- **Professional Design**: Sử dụng Material Design principles

- **Custom Layer Control**: Giao diện đẹp, trực quan- **Custom Layer Control**: Giao diện đẹp, trực quan

- **Responsive**: Tương thích mobile và desktop- **Responsive**: Tương thích mobile và desktop

- **5 Headquarters Markers**: Animation pulse và glow effects- **5 Headquarters Markers**: Animation pulse và glow effects



## 🔒 Bảo mật## 🔒 Bảo mật



- CORS được cấu hình cho embedding- CORS được cấu hình cho embedding

- File upload validation- File upload validation

- Admin authentication required- Admin authentication required

- CSRF protection enabled- CSRF protection enabled



## 📝 Ghi chú## 📝 Ghi chú



- Hỗ trợ file GeoJSON với định dạng chuẩn- Hỗ trợ file GeoJSON với định dạng chuẩn

- Tự động nhận diện fields: name, address- Tự động nhận diện fields: name, address

- Hiển thị popup với thông tin chi tiết- Hiển thị popup với thông tin chi tiết

- Tooltip khi hover- Tooltip khi hover

- Zoom tự động đến vùng dữ liệu- Zoom tự động đến vùng dữ liệu

- 5 điểm trụ sở cố định không thể xóa được- 5 điểm trụ sở cố định không thể xóa được

## Nhúng vào trang web khác

### 1. Khởi chạy server development:

```bashĐể nhúng vào trang web khác, sử dụng iframe:

python manage.py runserver

``````html

<iframe src="path/to/index.html" width="100%" height="600px" frameborder="0"></iframe>

### 2. Truy cập các URL:```

- **Admin Dashboard**: http://localhost:8000/admin/

  - Username: `admin`## Cấu trúc file GeoJSON

  - Password: `admin123`

- **Bản đồ nhúng**: http://localhost:8000/embed/Ứng dụng tự động nhận diện các trường sau:

- **API**: http://localhost:8000/api/- **Tên**: name, Name, NAME, ten, tên, title, Title

- **Địa chỉ**: address, Address, ADDRESS, dia_chi, địa chỉ, location, Location

## 📁 Cấu trúc dự án

Ví dụ GeoJSON:

``````json

geomap_project/{

├── geomap_project/          # Django project settings  "type": "FeatureCollection",

├── maps/                    # Main app  "features": [

│   ├── models.py           # GeoJSONFile, MapLayer models    {

│   ├── admin.py            # Admin interface customization      "type": "Feature",

│   ├── views.py            # API views và embed view      "geometry": {

│   ├── serializers.py      # DRF serializers        "type": "Point",

│   ├── urls.py             # URL routing        "coordinates": [105.8542, 21.0285]

│   └── templates/maps/           },

│       └── embed.html      # Embeddable map template      "properties": {

├── static/                  # Static files        "name": "Hồ Gươm",

├── media/                   # Uploaded files        "address": "Quận Hoàn Kiếm, Hà Nội",

└── manage.py               # Django management script        "type": "Hồ"

```      }

    }

## 🎯 Cách sử dụng  ]

}

### 1. Upload GeoJSON files:```

1. Truy cập admin dashboard: `/admin/`

2. Vào **Maps** > **GeoJSON Files**## Công nghệ sử dụng

3. Click **Add GeoJSON File**

4. Điền thông tin và upload file- HTML5

5. Chọn màu sắc và kích hoạt- CSS3

- JavaScript (ES6+)

### 2. Quản lý layers:- Leaflet.js 1.9.4

1. Trong admin, vào **Maps** > **Map Layers**- OpenStreetMap tiles

2. Cài đặt visibility và order cho từng layer

## Trình duyệt hỗ trợ

### 3. Nhúng bản đồ vào trang web khác:

```html- Chrome/Chromium

<iframe - Firefox

    src="http://localhost:8000/embed/" - Safari

    width="100%" - Edge

    height="600px" - Và các trình duyệt hiện đại khác hỗ trợ ES6+
    frameborder="0"
    style="border: none;">
</iframe>
```

## 🔧 API Endpoints

- `GET /api/map-data/` - Lấy dữ liệu tất cả layers
- `GET /api/geojson-files/` - Danh sách GeoJSON files
- `GET /api/map-layers/` - Danh sách map layers
- `POST /api/map-layers/select_all/` - Chọn tất cả layers
- `POST /api/map-layers/deselect_all/` - Bỏ chọn tất cả layers
- `PATCH /api/map-layers/{id}/` - Cập nhật layer visibility

## ⚙️ Tùy chỉnh

### Thay đổi base map:
Chỉnh sửa trong `embed.html`:
```javascript
const osmLayer = L.tileLayer('URL_CỦA_BẠN', {
    attribution: 'Attribution của bạn'
});
```

### Thêm validation cho GeoJSON:
Chỉnh sửa trong `models.py`:
```python
def clean(self):
    # Thêm validation logic
    pass
```

### Tùy chỉnh giao diện admin:
Chỉnh sửa trong `admin.py`:
```python
class GeoJSONFileAdmin(admin.ModelAdmin):
    # Thêm các tùy chỉnh
    pass
```

- **5 Headquarters Markers**: Animation pulse và glow effects

## 🔒 Bảo mật

- CORS được cấu hình cho embedding
- File upload validation
- Admin authentication required
- CSRF protection enabled

## 📝 Ghi chú

- Hỗ trợ file GeoJSON với định dạng chuẩn
- Tự động nhận diện fields: name, address
- Hiển thị popup với thông tin chi tiết
- Tooltip khi hover
- Zoom tự động đến vùng dữ liệu
- 5 điểm trụ sở cố định không thể xóa được