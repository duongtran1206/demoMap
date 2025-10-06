from django.db import models
import json
import os


class GeoJSONFile(models.Model):
    """Model for storing GeoJSON files information"""
    name = models.CharField(max_length=200, verbose_name="Layer Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    file = models.FileField(upload_to='geojson_files/', verbose_name="GeoJSON File")
    color = models.CharField(max_length=7, default="#007cff", verbose_name="Display Color")
    symbol = models.CharField(max_length=50, default="marker", verbose_name="Map Symbol")
    is_active = models.BooleanField(default=True, verbose_name="Active")
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
        """Count number of features in GeoJSON file"""
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
        """Return GeoJSON data"""
        try:
            if self.file and os.path.exists(self.file.path):
                with open(self.file.path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except:
            return None


class MapLayer(models.Model):
    """Model for managing map layers"""
    geojson_file = models.ForeignKey(GeoJSONFile, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True, verbose_name="Visible")
    order = models.IntegerField(default=0, verbose_name="Order")
    
    class Meta:
        verbose_name = "Map Layer"
        verbose_name_plural = "Map Layers"
        ordering = ['order']
    
    def __str__(self):
        return f"Layer: {self.geojson_file.name}"


class FeatureVisibility(models.Model):
    """Model for managing individual feature visibility"""
    map_layer = models.ForeignKey(MapLayer, on_delete=models.CASCADE, related_name='feature_visibilities')
    feature_index = models.IntegerField(verbose_name="Feature Index")
    feature_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Feature Name")
    feature_address = models.TextField(blank=True, null=True, verbose_name="Feature Address")
    is_visible = models.BooleanField(default=True, verbose_name="Visible")
    
    class Meta:
        verbose_name = "Feature Visibility"
        verbose_name_plural = "Feature Visibilities"
        unique_together = ['map_layer', 'feature_index']
        ordering = ['feature_index']
    
    def __str__(self):
        return f"{self.feature_name or f'Feature #{self.feature_index}'} - {self.map_layer.geojson_file.name}"


# Signals for automatically creating MapLayer when GeoJSONFile is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=GeoJSONFile)
def create_map_layer(sender, instance, created, **kwargs):
    """Automatically create MapLayer when new GeoJSONFile is created"""
    if created:
        MapLayer.objects.create(
            geojson_file=instance,
            is_visible=True,
            order=0
        )
