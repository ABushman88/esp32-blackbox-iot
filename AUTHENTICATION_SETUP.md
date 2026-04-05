# ESP32 Telemetry Platform - Authentication & Admin Dashboard Setup

## ✅ What Was Built

### 1. **User Authentication System**
- **Login Page** (`/auth/login/`): Secure login with username and password
- **Register Page** (`/auth/register/`): User registration with validation
- **Logout Functionality**: Secure session management
- **Password Validation**: Minimum 8 characters, strength validation
- **Email Verification**: Prevents duplicate emails

### 2. **Admin Dashboard** (`/auth/dashboard/`)
Comprehensive dashboard with:
- **Statistics Overview**
  - Total Devices count
  - Total Sensor Records
  - Active Users counter
- **Device Management**
  - View all registered devices
  - Add new devices
  - Edit device details
  - Delete devices
- **Sensor Data Monitoring**
  - Display recent 10 sensor readings
  - Temperature and humidity data
  - Device-sensor correlation
  - Timestamp tracking

### 3. **Device Management**
- **Add Device** (`/auth/device/add/`): Register new ESP32 devices
- **Edit Device** (`/auth/device/<id>/edit/`): Update device information
- **Delete Device** (`/auth/device/<id>/delete/`): Remove devices

### 4. **User Interface**
- **Responsive Design**: Mobile and desktop friendly
- **Modern Styling**: Gradient backgrounds, smooth animations
- **Interactive Elements**: Hover effects, form validation
- **Professional Layout**: Card-based design, clear navigation

---

## 📋 URL Routes

### Authentication Routes
| URL | Purpose |
|-----|---------|
| `/` | Redirects to login |
| `/auth/login/` | User login page |
| `/auth/register/` | User registration page |
| `/auth/logout/` | Logout and redirect to login |

### Dashboard Routes
| URL | Purpose |
|-----|---------|
| `/auth/dashboard/` | Main admin dashboard |
| `/auth/device/add/` | Add new device form |
| `/auth/device/<id>/edit/` | Edit device form |
| `/auth/device/<id>/delete/` | Delete device |

### API Routes (for ESP32)
| URL | Method | Purpose |
|-----|--------|---------|
| `/api/api/data/` | GET/POST | Sensor data endpoints |
| `/api/api/device-id/` | GET | Get device ID by name |

---

## 🚀 Quick Start

### 1. **Start the Development Server**
```bash
cd c:\Users\bush5\OneDrive\Desktop\esp32-blackbox-iot
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

### 2. **Create a New User**
1. Navigate to `http://127.0.0.1:8000/auth/register/`
2. Fill in the registration form
   - Username: Choose a unique username
   - Email: Enter a valid email
   - Password: Must be at least 8 characters
   - Confirm Password: Must match the password field
3. Click "Register"
4. You'll be redirected to login

### 3. **Login to Dashboard**
1. Go to `http://127.0.0.1:8000/auth/login/`
2. Enter your username and password
3. Click "Login"
4. You'll be taken to the admin dashboard

### 4. **Add a Device**
1. From the dashboard, click "+ Add New Device"
2. Fill in device details:
   - Device Name: e.g., "Temperature Sensor 1"
   - Device ID: Unique identifier, e.g., "ESP32-001"
   - Location: Optional location info
   - Created Date: Optional timestamp
3. Click "Add Device"

### 5. **Manage Devices**
- **View**: All devices listed in the dashboard
- **Edit**: Click "Edit" button to modify device details
- **Delete**: Click "Delete" button to remove a device

---

## 📁 Project Structure

```
esp32-blackbox-iot/
├── devices/
│   ├── templates/devices/
│   │   ├── base.html              # Base template with CSS
│   │   ├── login.html             # Login page
│   │   ├── register.html          # Registration page
│   │   ├── dashboard.html         # Admin dashboard
│   │   ├── add_device.html        # Add device form
│   │   └── edit_device.html       # Edit device form
│   ├── static/css/
│   │   └── style.css              # Complete styling
│   ├── views.py                   # All views (auth + dashboard)
│   ├── urls.py                    # URL routing
│   ├── models.py
│   ├── serializers.py
│   └── admin.py
├── backend/
│   ├── settings.py                # Updated with auth settings
│   ├── urls.py                    # Root URL config
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── db.sqlite3
└── README.md
```

---

## 🔐 Security Features

✅ **CSRF Protection**: All forms include CSRF tokens  
✅ **Password Hashing**: Passwords stored securely using Django's hash functions  
✅ **Session-based Auth**: Secure session management  
✅ **Login Required**: Dashboard and device management require authentication  
✅ **Validation**: Form validation on both client and server side  
✅ **Confirmation Dialogs**: Delete actions require confirmation  

---

## 📊 Database Models

### Device Model
```python
- name: CharField (Device name)
- device_id: CharField (Unique identifier)
- location: CharField (Optional location)
- created_at: CharField (Optional timestamp)
```

### SensorData Model
```python
- device: ForeignKey (Link to Device)
- temperature: FloatField
- humidity: FloatField
- timestamp: DateTimeField (Auto-set)
```

### User Model (Django built-in)
```python
- username: CharField (Unique)
- email: EmailField
- password: Hashed password
```

---

## 🔧 Customization

### Change Dashboard Title
Edit `dashboard.html`:
```html
<h2>ESP32 Telemetry Platform</h2>
```

### Adjust Color Scheme
Edit `style.css`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add More Stats Cards
Add new cards to `dashboard.html`:
```html
<div class="card">
    <h3>Custom Stat</h3>
    <div class="stat-value">{{ custom_value }}</div>
    <div class="stat-label">Label</div>
</div>
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 at `/` | Make sure the redirect is working. Check `backend/urls.py` |
| Login not working | Ensure user is created via registration page |
| Dashboard empty | Add devices and sensor data through the forms |
| Static files not loading | Run `python manage.py collectstatic --noinput` |
| Database errors | Run `python manage.py migrate` |

---

## 📱 API Integration with ESP32

The existing API endpoints remain available for your ESP32 device:

```c
// Example for ESP32:
// Get device ID
http://127.0.0.1:8000/api/api/device-id/?name=YourDeviceName

// Post sensor data
HTTP POST http://127.0.0.1:8000/api/api/data/
{
    "device": 1,
    "temperature": 25.5,
    "humidity": 60.2
}
```

---

## 🎯 Next Steps

1. ✅ User authentication system - DONE
2. ✅ Admin dashboard - DONE
3. ✅ Device management - DONE
4. 📊 Add graphs/charts for sensor data visualization
5. 📧 Add email notifications for alerts
6. 🔔 Real-time data updates (WebSockets)
7. 📱 Mobile app integration
8. 📈 Data export functionality (CSV/Excel)
9. 🌐 Deployment to production server

---

## 📞 Support

For issues or questions about the implementation, refer to:
- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- ESP32 Arduino Docs: https://docs.espressif.com/projects/arduino-esp32/

