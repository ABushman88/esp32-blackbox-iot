from rest_framework import serializers
from .models import Device, SensorData

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'Device'
        fields = '__all__'

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'Device'
        fields = '__all__'
