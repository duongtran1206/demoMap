from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'geojson-files', views.GeoJSONFileViewSet)
router.register(r'map-layers', views.MapLayerViewSet)

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.admin_logout_view, name='admin_logout'),
    path('api/', include(router.urls)),
    path('embed/', views.map_embed_view, name='map_embed'),
    path('embed_vn/', views.map_embed_vn_view, name='map_embed_vn'),
    path('symbol-demo/', views.symbol_demo_view, name='symbol_demo'),
    path('api/custom-symbols/', csrf_exempt(views.custom_symbols_api), name='custom_symbols_api'),
    path('api/upload-symbol/', csrf_exempt(views.upload_symbol_api), name='upload_symbol_api'),
    path('api/delete-symbol/<int:symbol_id>/', csrf_exempt(views.delete_symbol_api), name='delete_symbol_api'),
    path('api/map-data/', csrf_exempt(views.map_data_api), name='map_data_api'),
    path('api/map-data/<str:map_type>/', csrf_exempt(views.map_data_api), name='map_data_api_typed'),
    path('api/select-all-layers/', views.select_all_layers_api, name='select_all_layers'),
    path('api/deselect-all-layers/', views.deselect_all_layers_api, name='deselect_all_layers'),
    path('api/init-db/', csrf_exempt(views.init_db_api), name='init_db'),
    path('api/health/', views.health_check, name='health_check'),
    path('dashboard/', views.admin_dashboard_view, name='dashboard'),
    path('editlayer/', views.editlayer, name='editlayer'),
]

# JSON Editor URLs
from .views import get_json_content, add_json_feature, delete_json_feature, download_json_file

urlpatterns += [
    path('api/json-editor/<int:file_id>/', get_json_content, name='get_json_content'),
    path('api/json-editor/<int:file_id>/add/', add_json_feature, name='add_json_feature'),
    path('api/json-editor/<int:file_id>/delete/<int:feature_index>/', delete_json_feature, name='delete_json_feature'),
    path('api/json-editor/<int:file_id>/download/', download_json_file, name='download_json_file'),
]