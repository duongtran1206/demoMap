#!/bin/bash

# Script to test if Django GeoMap is working correctly after deployment

echo "=== Testing Django GeoMap Deployment ==="
echo ""

# Get public IP
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "localhost")

echo "Testing against: http://$PUBLIC_IP"
echo ""

# Test 1: Check if nginx is running
echo "Test 1: Nginx service..."
if systemctl is-active --quiet nginx; then
    echo "✓ Nginx is running"
else
    echo "✗ Nginx is NOT running"
fi

# Test 2: Check if demomap service is running
echo "Test 2: Django service..."
if systemctl is-active --quiet demomap; then
    echo "✓ Django service is running"
else
    echo "✗ Django service is NOT running"
fi

# Test 3: Check if gunicorn socket exists
echo "Test 3: Gunicorn socket..."
if [ -S "/home/ubuntu/demoMap/demomap.sock" ]; then
    echo "✓ Gunicorn socket exists"
else
    echo "✗ Gunicorn socket NOT found"
fi

# Test 4: Test HTTP response
echo "Test 4: HTTP response..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ HTTP response OK (200)"
else
    echo "✗ HTTP response: $HTTP_CODE"
fi

# Test 5: Test admin dashboard
echo "Test 5: Admin dashboard..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/admin-dashboard/)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
    echo "✓ Admin dashboard OK"
else
    echo "✗ Admin dashboard: $HTTP_CODE"
fi

# Test 6: Test embed page
echo "Test 6: Embed page..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/embed/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ Embed page OK"
else
    echo "✗ Embed page: $HTTP_CODE"
fi

# Test 7: Check static files
echo "Test 7: Static files..."
if [ -d "/home/ubuntu/demoMap/staticfiles" ] && [ "$(ls -A /home/ubuntu/demoMap/staticfiles)" ]; then
    echo "✓ Static files collected"
else
    echo "✗ Static files NOT found"
fi

# Test 8: Check database
echo "Test 8: Database..."
if [ -f "/home/ubuntu/demoMap/db.sqlite3" ]; then
    echo "✓ Database exists"
else
    echo "✗ Database NOT found"
fi

echo ""
echo "=== Test Complete ==="
echo ""
echo "Access URLs:"
echo "  http://$PUBLIC_IP/"
echo "  http://$PUBLIC_IP/admin-dashboard/"
echo "  http://$PUBLIC_IP/embed/"
echo ""
echo "Check logs if any test failed:"
echo "  sudo journalctl -u demomap -n 50"
echo "  sudo tail -f /var/log/nginx/error.log"
