from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100, unique=True, null=True)
    created_at = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return self.name

class SensorData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - {self.timestamp}"

