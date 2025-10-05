from django.db import models
import json
import os


class GeoJSONFile(models.Model):
    """Model để lưu trữ thông tin GeoJSON files"""
    name = models.CharField(max_length=200, verbose_name="Tên layer")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    file = models.FileField(upload_to='geojson_files/', verbose_name="File GeoJSON")
    color = models.CharField(max_length=7, default="#FF0000", verbose_name="Màu sắc")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "GeoJSON File"
        verbose_name_plural = "GeoJSON Files"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def feature_count(self):
        """Đếm số feature trong GeoJSON file"""
        try:
            if self.file and os.path.exists(self.file.path):
                with open(self.file.path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'features' in data:
                        return len(data['features'])
            return 0
        except:
            return 0
    
    @property
    def geojson_data(self):
        """Trả về dữ liệu GeoJSON"""
        try:
            if self.file and os.path.exists(self.file.path):
                with open(self.file.path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except:
            return None


class MapLayer(models.Model):
    """Model để quản lý các layer trên bản đồ"""
    geojson_file = models.ForeignKey(GeoJSONFile, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True, verbose_name="Hiển thị")
    order = models.IntegerField(default=0, verbose_name="Thứ tự")
    
    class Meta:
        verbose_name = "Map Layer"
        verbose_name_plural = "Map Layers"
        ordering = ['order']
    
    def __str__(self):
        return f"Layer: {self.geojson_file.name}"


class FeatureVisibility(models.Model):
    """Model để quản lý hiển thị từng feature riêng biệt"""
    map_layer = models.ForeignKey(MapLayer, on_delete=models.CASCADE, related_name='feature_visibilities')
    feature_index = models.IntegerField(verbose_name="Chỉ số feature")
    feature_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tên feature")
    feature_address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ feature")
    is_visible = models.BooleanField(default=True, verbose_name="Hiển thị")
    
    class Meta:
        verbose_name = "Feature Visibility"
        verbose_name_plural = "Feature Visibilities"
        unique_together = ['map_layer', 'feature_index']
        ordering = ['feature_index']
    
    def __str__(self):
        return f"{self.feature_name or f'Feature #{self.feature_index}'} - {self.map_layer.geojson_file.name}"