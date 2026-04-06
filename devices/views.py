from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Device, SensorData
from .serializers import SensorDataSerializer
from django.views.decorators.csrf import csrf_exempt

# ============================================================================
#                          HOMEPAGE VIEW
# ============================================================================

def homepage(request):
    """Display homepage - landing page for unauthenticated users, dashboard redirect for authenticated"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {
        'total_devices': Device.objects.count(),
        'total_sensor_readings': SensorData.objects.count(),
    }
    
    return render(request, 'devices/homepage.html', context)


# ============================================================================
#                          AUTHENTICATION VIEWS
# ============================================================================

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'devices/login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if not username or not email or not password1 or not password2:
            messages.error(request, 'All fields are required.')
            return render(request, 'devices/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'devices/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'devices/register.html')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'devices/register.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'devices/register.html')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'devices/register.html')
    
    return render(request, 'devices/register.html')


@login_required(login_url='login')
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# ============================================================================
#                          DASHBOARD VIEWS
# ============================================================================

@login_required(login_url='login')
def dashboard(request):
    """Admin dashboard with statistics and data overview"""
    devices = Device.objects.all()
    sensor_data = SensorData.objects.all().order_by('-timestamp')[:10]
    
    context = {
        'devices': devices,
        'sensor_data': sensor_data,
        'total_devices': devices.count(),
        'total_sensor_data': SensorData.objects.count(),
        'total_users': User.objects.count(),
    }
    
    return render(request, 'devices/dashboard.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def add_device(request):
    """Add a new device"""
    if request.method == 'POST':
        name = request.POST.get('name')
        device_id = request.POST.get('device_id')
        location = request.POST.get('location')
        created_at = request.POST.get('created_at')
        
        if not name or not device_id:
            messages.error(request, 'Device name and ID are required.')
            return redirect('add_device')
        
        if Device.objects.filter(device_id=device_id).exists():
            messages.error(request, 'Device with this ID already exists.')
            return redirect('add_device')
        
        try:
            Device.objects.create(
                name=name,
                device_id=device_id,
                location=location,
                created_at=created_at
            )
            messages.success(request, f'Device "{name}" added successfully!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Error adding device: {str(e)}')
            return redirect('add_device')
    
    return render(request, 'devices/add_device.html')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def edit_device(request, device_id):
    """Edit an existing device"""
    device = get_object_or_404(Device, id=device_id)
    
    if request.method == 'POST':
        device.name = request.POST.get('name', device.name)
        device.location = request.POST.get('location', device.location)
        device.created_at = request.POST.get('created_at', device.created_at)
        
        try:
            device.save()
            messages.success(request, f'Device "{device.name}" updated successfully!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Error updating device: {str(e)}')
    
    context = {'device': device}
    return render(request, 'devices/edit_device.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def device_detail(request, device_id):
    """Display device details with sensor data chart"""
    device = get_object_or_404(Device, id=device_id)
    
    # Get sensor data for this device, sorted by timestamp
    sensor_data = SensorData.objects.filter(device=device).order_by('timestamp')
    
    # Prepare data for chart
    timestamps = [data.timestamp.strftime('%Y-%m-%d %H:%M:%S') for data in sensor_data]
    temperatures = [data.temperature for data in sensor_data]
    humidities = [data.humidity for data in sensor_data]
    
    # Calculate statistics
    if sensor_data.exists():
        avg_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        avg_humidity = sum(humidities) / len(humidities)
        max_humidity = max(humidities)
        min_humidity = min(humidities)
    else:
        avg_temp = max_temp = min_temp = 0
        avg_humidity = max_humidity = min_humidity = 0
    
    context = {
        'device': device,
        'sensor_data': sensor_data,
        'timestamps': timestamps,
        'temperatures': temperatures,
        'humidities': humidities,
        'total_readings': sensor_data.count(),
        'avg_temp': round(avg_temp, 2),
        'max_temp': max_temp,
        'min_temp': min_temp,
        'avg_humidity': round(avg_humidity, 2),
        'max_humidity': max_humidity,
        'min_humidity': min_humidity,
    }
    
    return render(request, 'devices/device_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_device(request, device_id):
    """Delete a device"""
    device = get_object_or_404(Device, id=device_id)
    device_name = device.name
    
    try:
        device.delete()
        messages.success(request, f'Device "{device_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting device: {str(e)}')
    
    return redirect('dashboard')


# ============================================================================
#                          API VIEWS (for ESP32)
# ============================================================================

@csrf_exempt
@api_view(['GET'])
def get_device_id(request):
    name = request.GET.get('name')
    try:
        device = Device.objects.get(name=name)
        return Response({"id": device.id})
    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=404)
    
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
