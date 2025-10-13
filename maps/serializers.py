from rest_framework import serializers
from .models import GeoJSONFile, MapLayer, FeatureVisibility, CustomSymbol


class CustomSymbolSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomSymbol
        fields = ['id', 'name', 'image_url', 'category', 'is_active']


class GeoJSONFileSerializer(serializers.ModelSerializer):
    feature_count = serializers.ReadOnlyField()
    geojson_data = serializers.ReadOnlyField()
    custom_symbol = serializers.PrimaryKeyRelatedField(
        queryset=CustomSymbol.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = GeoJSONFile
        fields = ['id', 'name', 'description', 'file', 'color', 'symbol', 'custom_symbol', 'is_active', 
                 'map_type', 'feature_count', 'geojson_data', 'created_at']
        extra_kwargs = {
            'file': {'required': False}
        }


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


class JSONEditorSerializer(serializers.Serializer):
    """Serializer for JSON editor operations"""
    features = serializers.ListField()  # To validate features array