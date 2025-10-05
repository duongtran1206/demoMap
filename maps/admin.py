from django.contrib import admin
from django.utils.html import format_html
from .models import GeoJSONFile, MapLayer


@admin.register(GeoJSONFile)
class GeoJSONFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'feature_count_display', 'color_display', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['feature_count_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'description', 'file')
        }),
        ('Cài đặt hiển thị', {
            'fields': ('color', 'is_active')
        }),
        ('Thông tin bổ sung', {
            'fields': ('feature_count_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
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


@admin.register(MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ['geojson_file', 'is_visible', 'order']
    list_filter = ['is_visible']
    list_editable = ['is_visible', 'order']
    ordering = ['order']
