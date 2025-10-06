# Hướng dẫn Deploy Django GeoMap lên EC2

## Bước 1: SSH vào EC2
```bash
ssh -i ohio_ubuntu.pem ubuntu@15.152.37.134
```

## Bước 2: Clone project (nếu chưa có)
```bash
cd /home/ubuntu
git clone https://github.com/duongtran1206/demoMap.git
```

## Bước 3: Update code mới nhất
```bash
cd /home/ubuntu/demoMap
git pull origin main
```

## Bước 4: Chạy script deploy tự động
```bash
chmod +x deploy_ec2.sh
chmod +x update_ec2.sh
sudo ./deploy_ec2.sh
```

## Bước 5: Kiểm tra trạng thái
```bash
sudo systemctl status demomap
sudo systemctl status nginx
```

## Bước 6: Truy cập ứng dụng
- Trang chủ: http://15.152.37.134/
- Admin Dashboard: http://15.152.37.134/admin-dashboard/
- Map Embed: http://15.152.37.134/embed/
- Django Admin: http://15.152.37.134/admin/ (admin/admin123)

## Update code sau này
Khi có thay đổi mới, chỉ cần chạy:
```bash
cd /home/ubuntu/demoMap
sudo ./update_ec2.sh
```

## Troubleshooting

### Nếu gặp lỗi 403 Forbidden với static files:
```bash
cd /home/ubuntu/demoMap
chmod +x debug_ec2.sh
sudo ./debug_ec2.sh
```

### Kiểm tra logs chi tiết:
```bash
sudo journalctl -u demomap -f
sudo tail -f /var/log/nginx/error.log
sudo tail -f /home/ubuntu/demoMap/django.log
```

### Sửa permissions thủ công nếu cần:
```bash
sudo chown -R ubuntu:www-data /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/
sudo chmod -R 755 /home/ubuntu/demoMap/staticfiles/
```

## Restart services nếu cần
```bash
sudo systemctl restart demomap
sudo systemctl restart nginx
```