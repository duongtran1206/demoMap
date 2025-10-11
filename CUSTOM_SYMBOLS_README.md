# Custom Symbol System for GeoMap

Hệ thống biểu tượng tùy chỉnh cho phép bạn upload ảnh của riêng mình để sử dụng làm marker trên bản đồ thay vì emoji mặc định.

## Tính năng

- ✅ Upload ảnh tùy chỉnh làm symbol cho map markers
- ✅ Quản lý danh sách symbols trong admin
- ✅ Hiển thị symbols đẹp và chuẩn trên bản đồ
- ✅ Tương thích ngược với emoji symbols cũ
- ✅ Responsive design cho mobile

## Cách sử dụng

### 1. Upload Custom Symbols

1. Truy cập Django Admin: `/admin/`
2. Vào phần "Maps" > "Custom symbols"
3. Click "Add Custom Symbol"
4. Upload ảnh và đặt tên
5. Chọn category (tùy chọn)

### 2. Sử dụng trong GeoJSON Files

1. Trong admin dashboard, khi tạo/sửa GeoJSON file
2. Trong phần "Map Symbol", click vào dropdown
3. Chọn từ danh sách custom symbols đã upload
4. Upload file GeoJSON như bình thường

### 3. Hiển thị trên bản đồ

- Symbols sẽ tự động hiển thị trên `/embed/` và `/embed_vn/`
- Kích thước tối ưu: 24x24px đến 64x64px
- Tự động resize và căn giữa

## Định dạng ảnh được hỗ trợ

- **Format**: PNG, JPG, JPEG, GIF
- **Kích thước khuyến nghị**: 32x32px đến 64x64px
- **Background**: Transparent hoặc solid color
- **Aspect ratio**: Vuông (1:1) cho kết quả tốt nhất

## API Endpoints

### Lấy danh sách symbols
```
GET /api/custom-symbols/
```

Response:
```json
{
  "status": "success",
  "symbols": [
    {
      "id": 1,
      "name": "HWK Schraube",
      "image_url": "/media/symbols/hwk_schraube.png",
      "category": "Hardware",
      "is_active": true
    }
  ]
}
```

## Cấu trúc Database

### CustomSymbol Model
- `name`: Tên symbol
- `image`: File ảnh (upload to `media/symbols/`)
- `category`: Phân loại (tùy chọn)
- `is_active`: Trạng thái active
- `created_at/updated_at`: Timestamp

### GeoJSONFile Model (cập nhật)
- Thêm field `custom_symbol`: ForeignKey đến CustomSymbol
- Giữ lại `symbol` field cũ để tương thích ngược

## Rendering Logic

1. **Ưu tiên Custom Symbol**: Nếu `custom_symbol` có giá trị → sử dụng ảnh
2. **Fallback to Emoji**: Nếu không có custom symbol → dùng emoji từ `OSM_SYMBOLS`
3. **Marker Styling**: Tự động resize, thêm border và shadow

## Files đã tạo/cập nhật

### Models
- `maps/models.py`: Thêm `CustomSymbol` model

### Admin
- `maps/admin.py`: Admin interface cho CustomSymbol

### API
- `maps/views.py`: API endpoint `/api/custom-symbols/`
- `maps/serializers.py`: Serializer cho CustomSymbol
- `maps/urls.py`: URL routing

### Frontend
- `static/js/custom-symbol-picker.js`: Component picker
- `static/css/custom-symbol-picker.css`: Styling
- `maps/templates/maps/dashboard.html`: Tích hợp picker
- `maps/templates/maps/embed_new.html`: Render markers

### Database
- Migration `0006_customsymbol_alter_geojsonfile_symbol_and_more.py`

## Troubleshooting

### Symbol không hiển thị
- Kiểm tra symbol có `is_active = True`
- Kiểm tra file ảnh tồn tại trong `media/symbols/`
- Check browser console cho lỗi 404

### Upload lỗi
- Kiểm tra quyền write trong thư mục `media/`
- Đảm bảo format ảnh được hỗ trợ
- Kích thước file không quá lớn

### Performance
- Resize ảnh về 64x64px trước khi upload
- Sử dụng format PNG cho transparent background
- Compress ảnh để giảm size

## Mở rộng

### Thêm categories mới
```python
# Trong admin hoặc code
symbol.category = "New Category"
symbol.save()
```

### Custom marker sizes
```javascript
// Trong embed template
iconSize: [32, 32], // Thay đổi kích thước
iconAnchor: [16, 16], // Cập nhật anchor
```

### Batch upload
Có thể thêm tính năng upload nhiều symbols cùng lúc trong admin.