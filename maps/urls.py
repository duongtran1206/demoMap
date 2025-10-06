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
    path('symbol-demo/', views.symbol_demo_view, name='symbol_demo'),
    path('api/map-data/', csrf_exempt(views.map_data_api), name='map_data_api'),
    path('api/select-all-layers/', views.select_all_layers_api, name='select_all_layers'),
    path('api/deselect-all-layers/', views.deselect_all_layers_api, name='deselect_all_layers'),
    path('api/init-db/', csrf_exempt(views.init_db_api), name='init_db'),
    path('api/health/', views.health_check, name='health_check'),
    path('dashboard/', views.admin_dashboard_view, name='dashboard'),
]