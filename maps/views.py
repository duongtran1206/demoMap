from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .models import GeoJSONFile, MapLayer, FeatureVisibility
from .serializers import GeoJSONFileSerializer, MapLayerSerializer
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User


class GeoJSONFileViewSet(viewsets.ModelViewSet):
    queryset = GeoJSONFile.objects.filter(is_active=True)
    serializer_class = GeoJSONFileSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        """Custom create method to handle file upload"""
        # Ensure is_active defaults to True if not provided
        data = request.data.copy()
        if 'is_active' not in data:
            data['is_active'] = True
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Create the instance
        instance = serializer.save()
        
        # Handle file upload if present
        if 'file' in request.FILES:
            instance.file = request.FILES['file']
            instance.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Custom update method to handle file upload"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Save the instance
        instance = serializer.save()
        
        # Handle file upload if present
        if 'file' in request.FILES:
            instance.file = request.FILES['file']
            instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class MapLayerViewSet(viewsets.ModelViewSet):
    queryset = MapLayer.objects.all()
    serializer_class = MapLayerSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def select_all(self, request):
        """Select all layers"""
        try:
            MapLayer.objects.all().update(is_visible=True)
            return Response({'message': 'Selected all layers', 'status': 'success'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @csrf_exempt
    @action(detail=False, methods=['post'])  
    def deselect_all(self, request):
        """Deselect all layers"""
        try:
            MapLayer.objects.all().update(is_visible=False)
            return Response({'message': 'Deselected all layers', 'status': 'success'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def update(self, request, *args, **kwargs):
        """Override update to handle PATCH requests"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @csrf_exempt
    @action(detail=True, methods=['post'])
    def toggle_feature(self, request, pk=None):
        """Toggle visibility of a specific feature"""
        try:
            layer = self.get_object()
            feature_index = request.data.get('feature_index')
            is_visible = request.data.get('is_visible', True)
            
            if feature_index is None:
                return Response({'error': 'feature_index is required'}, status=400)
            
            feature_visibility, created = FeatureVisibility.objects.get_or_create(
                map_layer=layer,
                feature_index=feature_index,
                defaults={'is_visible': is_visible}
            )
            
            if not created:
                feature_visibility.is_visible = is_visible
                feature_visibility.save()
            
            return Response({
                'message': f'Feature {feature_index} visibility updated',
                'is_visible': is_visible,
                'status': 'success'
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


def map_embed_view(request):
    """View for displaying embeddable map"""
    return render(request, 'maps/embed_new.html')


def map_data_api(request):
    """API returns map data for frontend - public access for embed"""
    try:
        layers = MapLayer.objects.filter(
            geojson_file__is_active=True
        ).select_related('geojson_file').prefetch_related('feature_visibilities')
        
        data = []
        for layer in layers:
            geojson_data = layer.geojson_file.geojson_data
            if geojson_data and 'features' in geojson_data:
                # Filter visible features
                visible_features = []
                feature_visibilities = {fv.feature_index: fv.is_visible for fv in layer.feature_visibilities.all()}
                
                for index, feature in enumerate(geojson_data['features']):
                    # Default visible if no specific visibility setting
                    is_visible = feature_visibilities.get(index, True)
                    if layer.is_visible and is_visible:
                        visible_features.append(feature)
                
                # Always include layer for layer control, but filter features for map display
                filtered_geojson = {
                    'type': 'FeatureCollection',
                    'features': visible_features
                }
                
                # Get feature details for layer control (all features, not just visible)
                features_detail = []
                for index, feature in enumerate(geojson_data['features']):
                    # Extract feature name and address
                    props = feature.get('properties', {})
                    name_fields = ['name', 'Name', 'NAME', 'ten', 'tên', 'title', 'Title']
                    address_fields = ['address', 'Address', 'ADDRESS', 'dia_chi', 'địa chỉ', 'location', 'Location']
                    
                    name = None
                    address = None
                    
                    for field in name_fields:
                        if props.get(field):
                            name = props[field]
                            break
                    
                    for field in address_fields:
                        if props.get(field):
                            raw_address = props[field]
                            # Handle address object vs string
                            if isinstance(raw_address, dict):
                                # If it's an object, format it properly
                                if raw_address.get('full_address'):
                                    address = raw_address['full_address']
                                else:
                                    # Build address from components
                                    parts = []
                                    if raw_address.get('street'):
                                        parts.append(raw_address['street'])
                                    if raw_address.get('postal_code') or raw_address.get('city'):
                                        city_part = []
                                        if raw_address.get('postal_code'):
                                            city_part.append(raw_address['postal_code'])
                                        if raw_address.get('city'):
                                            city_part.append(raw_address['city'])
                                        parts.append(' '.join(city_part))
                                    if raw_address.get('country'):
                                        parts.append(raw_address['country'])
                                    address = ', '.join(parts)
                            else:
                                # If it's a string, use it directly
                                address = str(raw_address)
                            break
                    
                    features_detail.append({
                        'index': index,
                        'name': name or f'Location #{index + 1}',
                        'address': address or '',
                        'is_visible': feature_visibilities.get(index, True)
                    })
                
                data.append({
                        'id': layer.id,
                        'name': layer.geojson_file.name,
                        'color': layer.geojson_file.color,
                        'is_visible': layer.is_visible,
                        'feature_count': layer.geojson_file.feature_count,
                        'features': features_detail,
                        'geojson': filtered_geojson
                    })
        
        # Get the most recent update time from GeoJSON files
        from django.db.models import Max
        last_updated = GeoJSONFile.objects.aggregate(
            last_updated=Max('updated_at')
        )['last_updated']
        
        return JsonResponse({
            'layers': data,
            'last_updated': last_updated.isoformat() if last_updated else None
        })
        
    except Exception as e:
        # Return empty data with error info for debugging
        import traceback
        return JsonResponse({
            'layers': [],
            'last_updated': None,
            'error': str(e),
            'debug_info': traceback.format_exc() if request.GET.get('debug') else None
        }, status=200)  # Use 200 instead of 500 to avoid breaking the frontend


def is_admin_user(user):
    """Check if user is admin"""
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required(login_url='/login/')
@user_passes_test(is_admin_user, login_url='/login/')
def admin_dashboard_view(request):
    """View để hiển thị admin dashboard - chỉ admin mới truy cập được"""
    return render(request, 'maps/dashboard.html')


@csrf_exempt
def select_all_layers_api(request):
    """API để chọn tất cả layers - chỉ admin"""
    # Check if user is authenticated and is admin
    if not request.user.is_authenticated or not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({
            'error': 'Authentication required - Admin access only', 
            'status': 'error'
        }, status=403)
        
    if request.method == 'POST':
        try:
            MapLayer.objects.all().update(is_visible=True)
            return JsonResponse({
                'message': 'Selected all layers', 
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e), 
                'status': 'error'
            }, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def deselect_all_layers_api(request):
    """API để bỏ chọn tất cả layers - chỉ admin"""
    # Check if user is authenticated and is admin
    if not request.user.is_authenticated or not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({
            'error': 'Authentication required - Admin access only', 
            'status': 'error'
        }, status=403)
        
    if request.method == 'POST':
        try:
            MapLayer.objects.all().update(is_visible=False)
            return JsonResponse({
                'message': 'Deselected all layers', 
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e), 
                'status': 'error'
            }, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def admin_login_view(request):
    """View cho admin login"""
    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and (user.is_superuser or user.is_staff):
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions. Admin access required.')
    
    return render(request, 'maps/login.html')


def admin_logout_view(request):
    """View cho admin logout"""
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('admin_login')


def init_db_api(request):
    """Initialize database for Vercel deployment"""
    try:
        # Run migrations
        from django.core.management import execute_from_command_line
        import sys
        
        # Save original argv
        original_argv = sys.argv
        
        try:
            # Run migrate command
            sys.argv = ['manage.py', 'migrate', '--run-syncdb']
            execute_from_command_line(sys.argv)
            
            # Create superuser if it doesn't exist
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                
            return JsonResponse({
                'status': 'success',
                'message': 'Database initialized successfully'
            })
            
        finally:
            # Restore original argv
            sys.argv = original_argv
            
    except Exception as e:
        import traceback
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }, status=500)
