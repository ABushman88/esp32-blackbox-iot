from django.urls import path
from .views import add_sensor_data

urlpatterns = [
    path('data/', add_sensor_data),
]