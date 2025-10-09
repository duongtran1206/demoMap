from rest_framework import serializers
from .models import GeoJSONFile, MapLayer, FeatureVisibility


class GeoJSONFileSerializer(serializers.ModelSerializer):
    feature_count = serializers.ReadOnlyField()
    geojson_data = serializers.ReadOnlyField()
    
    class Meta:
        model = GeoJSONFile
        fields = ['id', 'name', 'description', 'file', 'color', 'symbol', 'is_active', 
                 'feature_count', 'geojson_data', 'created_at']


class FeatureVisibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureVisibility
        fields = ['id', 'feature_index', 'feature_name', 'feature_address', 'is_visible']


class MapLayerSerializer(serializers.ModelSerializer):
    geojson_file = GeoJSONFileSerializer(read_only=True)
    feature_visibilities = FeatureVisibilitySerializer(many=True, read_only=True)
    
    class Meta:
        model = MapLayer
        fields = ['id', 'geojson_file', 'is_visible', 'order', 'feature_visibilities']