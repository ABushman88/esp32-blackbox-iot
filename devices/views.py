from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData
from .serializers import SensorDataSerializer

@api_view(['GET', 'POST'])
def add_sensor_data(request):
    if request.method == 'GET':
        data = SensorData.objects.all()
        serializer = SensorDataSerializer(data, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data saved successfully"})
        return Response(serializer.errors)
