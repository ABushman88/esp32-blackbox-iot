from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard and Device Management URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('device/add/', views.add_device, name='add_device'),
    path('device/<int:device_id>/edit/', views.edit_device, name='edit_device'),
    path('device/<int:device_id>/delete/', views.delete_device, name='delete_device'),
    
    # API URLs (for ESP32)
    path('api/data/', views.add_sensor_data, name='add_sensor_data'),
    path('api/device-id/', views.get_device_id, name='get_device_id'),
]