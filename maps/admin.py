from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from .models import GeoJSONFile, MapLayer, CustomSymbol
import json
import io


def convert_custom_json_to_geojson(custom_data):
    """Convert custom JSON format to GeoJSON FeatureCollection"""
    if 'locations' not in custom_data:
        return custom_data  # Already GeoJSON
    
    features = []
    for location in custom_data['locations']:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [location['longitude'], location['latitude']]
            },
            "properties": {
                "name": location['name'],
                "display_name": location.get('display_name', location['name'])
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


@admin.register(GeoJSONFile)
class GeoJSONFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'map_type', 'feature_count_display', 'color_display', 'symbol_display', 'is_active', 'created_at']
    list_filter = ['is_active', 'map_type', 'custom_symbol', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['feature_count_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'description', 'file', 'map_type')
        }),
        ('Cài đặt hiển thị', {
            'fields': ('color', 'custom_symbol', 'is_active')
        }),
        ('Thông tin bổ sung', {
            'fields': ('feature_count_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save_model to handle custom JSON conversion"""
        if obj.file and not change:  # Only on creation
            try:
                # Read and parse the uploaded file
                file_content = obj.file.read().decode('utf-8')
                custom_data = json.loads(file_content)
                geojson_data = convert_custom_json_to_geojson(custom_data)
                
                # Create a new file-like object with GeoJSON content
                geojson_content = json.dumps(geojson_data, ensure_ascii=False, indent=2)
                geojson_file = io.BytesIO(geojson_content.encode('utf-8'))
                geojson_file.name = obj.file.name  # Keep original filename
                
                obj.file = geojson_file
            except json.JSONDecodeError:
                # If not valid JSON, save as is (assuming it's already GeoJSON)
                pass
        
        super().save_model(request, obj, form, change)
    
    def feature_count_display(self, obj):
        count = obj.feature_count
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{} điểm</span>', count)
        return format_html('<span style="color: red;">0 điểm</span>')
    feature_count_display.short_description = 'Số lượng điểm'
    
    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000; display: inline-block;"></div>',
            obj.color
        )
    color_display.short_description = 'Màu sắc'

    def symbol_display(self, obj):
        if obj.custom_symbol and obj.custom_symbol.image:
            return format_html('<img src="{}" style="max-width: 30px; max-height: 30px; border-radius: 3px;" title="{}" />', 
                             obj.custom_symbol.image.url, obj.custom_symbol.name)
        elif obj.symbol:
            return format_html('<span style="font-size: 16px;">📍</span> <small>({})</small>', obj.symbol)
        return "No symbol"
    symbol_display.short_description = "Symbol"


@admin.register(MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ['geojson_file', 'is_visible', 'order']
    list_filter = ['is_visible']
    list_editable = ['is_visible', 'order']
    ordering = ['order']

@admin.register(CustomSymbol)
class CustomSymbolAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'image_preview', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'category']
    list_editable = ['is_active']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'image', 'category')
        }),
        ('Cài đặt', {
            'fields': ('is_active',)
        }),
        ('Thông tin bổ sung', {
            'fields': ('image_preview', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px; border-radius: 5px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"
