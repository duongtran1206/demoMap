# Django GeoMap Project# OpenStreetMap GeoJSON Viewer



Một dự án Django chuyên nghiệp để quản lý và hiển thị bản đồ với dữ liệu GeoJSON. Bản đồ có thể nhúng vào các trang web khác với đầy đủ tính năng layer control.Một web application đơn giản để hiển thị nhiều file GeoJSON trên bản đồ OpenStreetMap với layer control.



## 🚀 Tính năng chính## Tính năng



- **Admin Dashboard chuyên nghiệp**: Quản lý upload/delete GeoJSON files- ✅ Hiển thị bản đồ OpenStreetMap với Leaflet

- **Bản đồ nhúng được**: Có thể embed vào trang web khác- ✅ Import nhiều file GeoJSON (.geojson, .json)

- **Layer Control tùy chỉnh**: Nằm bên phải bản đồ với các chức năng:- ✅ Layer control bên phải để bật/tắt từng layer

  - Select All / Deselect All- ✅ Hiển thị tên và địa chỉ trong popup

  - Hiển thị tên layer và số điểm- ✅ Đếm số điểm trong mỗi layer

  - Checkbox để bật/tắt từng layer- ✅ Hỗ trợ drag & drop file

  - Màu sắc tùy chỉnh cho từng layer- ✅ Có thể nhúng vào trang web khác

- **API RESTful**: Hỗ trợ tích hợp với các hệ thống khác- ✅ Multiple base maps (OpenStreetMap, Satellite, CartoDB)

- **Responsive Design**: Tương thích mọi thiết bị- ✅ Màu sắc ngẫu nhiên cho mỗi layer

- ✅ Tooltip hiển thị tên khi hover

## 🛠️ Công nghệ sử dụng

## Cách sử dụng

- **Backend**: Django 5.2.7, Django REST Framework

- **Frontend**: HTML5, CSS3, JavaScript ES6+1. Mở file `index.html` trong trình duyệt

- **Maps**: Leaflet.js, OpenStreetMap2. Click "📁 Thêm GeoJSON" để chọn file, hoặc kéo thả file vào bản đồ

- **Database**: SQLite (có thể thay đổi)3. Các layer sẽ xuất hiện trong layer control bên phải

- **File Upload**: Django FileField với validation4. Click vào các điểm để xem thông tin chi tiết

5. Sử dụng layer control để bật/tắt hiển thị từng layer

## 📋 Cài đặt và chạy

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

## 🎨 Giao diện

- **Professional Design**: Sử dụng Material Design principles
- **Custom Layer Control**: Giao diện đẹp, trực quan
- **Responsive**: Tương thích mobile và desktop
- **Dark/Light Theme**: Có thể tùy chỉnh theme

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