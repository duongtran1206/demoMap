# Quick Start Guide - Deploy trên AWS Ubuntu

## Chuẩn bị
1. EC2 Ubuntu instance (20.04 hoặc 22.04)
2. Clone code vào `/home/ubuntu/demoMap`

```bash
sudo git clone https://github.com/duongtran1206/demoMap.git /home/ubuntu/demoMap
sudo chown -R ubuntu:ubuntu /home/ubuntu/demoMap
```

## Deploy

```bash
cd /home/ubuntu/demoMap
chmod +x reset_ec2.sh start_service.sh
sudo ./start_service.sh
```

## Truy cập

- URL: `http://YOUR_EC2_IP/`
- Admin: `http://YOUR_EC2_IP/admin/` (admin/admin123)
- Dashboard: `http://YOUR_EC2_IP/admin-dashboard/`

## Reset và deploy lại

```bash
cd /home/ubuntu/demoMap
sudo ./reset_ec2.sh
sudo ./start_service.sh
```

## Xem logs

```bash
sudo journalctl -u demomap -f
```

Xem chi tiết: [DEPLOY_EC2.md](DEPLOY_EC2.md)
