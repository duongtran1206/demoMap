# Hướng dẫn Deploy Django GeoMap lên AWS Ubuntu EC2

## Yêu cầu
- AWS Ubuntu EC2 instance (Ubuntu 20.04 hoặc 22.04)
- SSH key để kết nối
- Quyền sudo trên server

## Bước 1: SSH vào EC2
```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

## Bước 2: Clone/Move project vào /home/ubuntu/demoMap
```bash
# Clone từ git trực tiếp vào /home/ubuntu/demoMap
sudo git clone https://github.com/duongtran1206/demoMap.git /home/ubuntu/demoMap

# Hoặc nếu đã clone vào /demoMap, di chuyển sang /home/ubuntu/demoMap
sudo mv /demoMap /home/ubuntu/demoMap

# Set quyền cho user ubuntu
sudo chown -R ubuntu:ubuntu /home/ubuntu/demoMap
```

## Bước 3: Deploy lần đầu

### 3.1. Vào thư mục project
```bash
cd /home/ubuntu/demoMap
```

### 3.2. Set quyền execute cho script
```bash
chmod +x reset_ec2.sh
chmod +x start_service.sh
```

### 3.3. Chạy deploy
```bash
sudo ./start_service.sh
```

Script sẽ tự động:
- Cài đặt Python, Nginx và các dependencies
- Tạo virtual environment
- Chạy migrations
- Tạo superuser (admin/admin123)
- Collect static files
- Cấu hình systemd service
- Cấu hình nginx (HTTP only)
- Khởi động services

## Bước 4: Truy cập ứng dụng

Sau khi deploy xong, truy cập các URL:
- Trang chủ: `http://YOUR_EC2_IP/`
- Admin Dashboard: `http://YOUR_EC2_IP/admin-dashboard/`
- Map Embed: `http://YOUR_EC2_IP/embed/`
- Map Embed VN: `http://YOUR_EC2_IP/embed_vn/`
- Edit Layer: `http://YOUR_EC2_IP/editlayer/`
- Django Admin: `http://YOUR_EC2_IP/admin/` (admin/admin123)

## Update code sau này

Khi có thay đổi mới:

```bash
cd /home/ubuntu/demoMap
git pull origin main
sudo ./start_service.sh
```

## Reset và deploy lại từ đầu

Nếu muốn reset toàn bộ và deploy lại:

```bash
cd /home/ubuntu/demoMap
sudo ./reset_ec2.sh
sudo ./start_service.sh
```

## Troubleshooting

### Kiểm tra trạng thái services
```bash
sudo systemctl status demomap
sudo systemctl status nginx
```

### Xem logs
```bash
# Django logs
sudo journalctl -u demomap -f

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### Restart services
```bash
sudo systemctl restart demomap
sudo systemctl restart nginx
```

### Kiểm tra nginx configuration
```bash
sudo nginx -t
```

### Nếu gặp lỗi permission
```bash
sudo chown -R ubuntu:www-data /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/staticfiles/
sudo chmod -R 755 /home/ubuntu/demoMap/media/
```

### Nếu port 80 bị chiếm dụng
```bash
# Kiểm tra port 80
sudo netstat -tlnp | grep :80

# Hoặc
sudo lsof -i :80

# Dừng process đang dùng port 80
sudo kill -9 PID
```

## Lưu ý quan trọng

1. **HTTP Only**: Deploy này chỉ dùng HTTP (không SSL) - phù hợp cho demo
2. **Project Path**: Project phải ở `/home/ubuntu/demoMap`
3. **Security Group**: Đảm bảo Security Group của EC2 cho phép:
   - Inbound port 22 (SSH)
   - Inbound port 80 (HTTP)
4. **Admin Credentials**: Username `admin`, Password `admin123`
5. **Database**: SQLite (db.sqlite3) - phù hợp cho demo, production nên dùng PostgreSQL

## Cấu trúc thư mục

```
/home/ubuntu/demoMap/                    # Project root
├── manage.py
├── requirements.txt
├── reset_ec2.sh            # Script reset
├── start_service.sh        # Script deploy
├── db.sqlite3              # Database
├── venv/                   # Virtual environment
├── staticfiles/            # Static files collected
├── media/                  # Media files
├── geomap_project/         # Django project
└── maps/                   # Django app
```

## Các lệnh hữu ích

```bash
# Xem tất cả services đang chạy
sudo systemctl list-units --type=service --state=running

# Xem thông tin chi tiết service
sudo systemctl show demomap

# Test nginx config
sudo nginx -t

# Reload nginx (không restart)
sudo systemctl reload nginx

# Xem processes của gunicorn
ps aux | grep gunicorn

# Kill tất cả gunicorn processes
sudo pkill -f gunicorn
```