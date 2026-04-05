from rest_framework import serializers
from .models import SensorData, Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class SensorDataSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
    class Meta:
        model = SensorData
        fields = ['id', 'device', 'temperature', 'humidity', 'timestamp']
