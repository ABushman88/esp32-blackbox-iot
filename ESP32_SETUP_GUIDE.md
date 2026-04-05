# ESP32 DHT22 Telemetry Setup Guide

## 📋 Overview
This guide provides step-by-step instructions to configure your ESP32 with a DHT22 temperature/humidity sensor and connect it to the Django backend.

---

## 🔧 Hardware Requirements

- **ESP32 Development Board** (e.g., ESP32 DevKit C)
- **DHT22 Sensor** (Temperature & Humidity)
- **USB Cable** (Micro-USB for programming)
- **Jumper Wires**
- **4.7kΩ Resistor** (Pull-up resistor for DHT22)
- **Breadboard** (optional, for easy connections)
- WiFi access point

---

## 🔌 Hardware Connections

### DHT22 Pinout
```
DHT22 Sensor
┌─────────────┐
│ 1 | 2 | 3 | 4│
└─────────────┘
 │   │   │   │
 ↓   ↓   ↓   ↓
VCC DATA NC GND
```

### Connection to ESP32
| DHT22 Pin | ESP32 Pin | Notes |
|-----------|-----------|-------|
| VCC (Pin 1) | 3V3 (3.3V) | Power supply |
| DATA (Pin 2) | GPIO 4 | Sensor data line |
| NC (Pin 3) | — | Not Connected |
| GND (Pin 4) | GND | Ground |

### Wiring Diagram
```
DHT22 Sensor
    │
    ├─ VCC ────────→ ESP32 3V3 (3.3V)
    │
    ├─ DATA ──[4.7kΩ]──→ ESP32 GPIO 4 (with pull-up to 3V3)
    │
    └─ GND ────────→ ESP32 GND
```

**Important:** Use a pull-up resistor (4.7kΩ) between DATA and VCC for proper communication.

---

## 💻 Software Setup

### 1. Install Arduino IDE
- Download from: https://www.arduino.cc/en/software
- Install for your operating system

### 2. Add ESP32 Board Support

1. Open **Arduino IDE**
2. Go to **File → Preferences**
3. Find **Additional boards manager URLs**
4. Add this URL:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
5. Click **OK**
6. Go to **Tools → Board → Boards Manager**
7. Search for "esp32"
8. Install **"esp32"** by Espressif Systems
9. Wait for installation to complete

### 3. Install DHT22 Library

1. Go to **Sketch → Include Library → Manage Libraries**
2. Search for "DHT"
3. Install **"DHT sensor library"** by Adafruit
4. Also install **"Adafruit Unified Sensor"** dependency
5. Click **Install**

---

## ⚙️ Configure the Sketch

### Step 1: Configure WiFi Settings
Open `esp32_telemetry_dht22.ino` and modify these lines:

```cpp
const char* WIFI_SSID = "YOUR_WIFI_SSID";           // Replace with your WiFi name
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";   // Replace with your WiFi password
```

**Example:**
```cpp
const char* WIFI_SSID = "MyHomeWiFi";
const char* WIFI_PASSWORD = "MyWiFiPassword123";
```

### Step 2: Configure Server Address
Find this line and replace with your server IP or domain:

```cpp
const char* SERVER_URL = "http://192.168.1.X:8000";  // Change this
```

**Example:**
```cpp
const char* SERVER_URL = "http://192.168.1.100:8000";  // For local network
// OR
const char* SERVER_URL = "http://myserver.com:8000";   // For external server
```

### Step 3: Configure Device Information
Customize these settings for your device:

```cpp
const char* DEVICE_NAME = "ESP32-Sensor-01";        // Device name (must match dashboard)
const char* DEVICE_ID = "ESP32-001";                // Unique device ID

#define DHTPIN 4                                    // GPIO pin for DHT22 (change if needed)
```

### Step 4: Configure Timing (Optional)
Adjust sensor reading and data sending intervals:

```cpp
const unsigned long SENSOR_READ_INTERVAL = 10000;   // Read every 10 seconds
const unsigned long SEND_DATA_INTERVAL = 30000;     // Send every 30 seconds
```

---

## 🚀 Upload to ESP32

### 1. Connect ESP32 to Computer
- Use USB cable to connect ESP32 to your computer
- You should see a new COM port appear

### 2. Select Board and Port
1. **Tools → Board → esp32 → ESP32 Dev Module**
2. **Tools → Port → COM#** (select the port your ESP32 is on)

### 3. Verify and Upload
1. Click the **Verify** button (✓) to check for errors
2. If no errors, click the **Upload** button (→) to upload to ESP32
3. Wait for "Connecting..." message
4. Upload should complete with "Leaving... Hard resetting via RTS pin..."

### 4. Monitor Serial Output
1. Go to **Tools → Serial Monitor**
2. Set baud rate to **115200**
3. You should see:
   ```
   ========================================
   ESP32 DHT22 Telemetry System
   ========================================
   
   Initializing DHT22 sensor...
   Starting WiFi connection...
   SSID: MyHomeWiFi
   ```

---

## 📱 Dashboard Registration

Before the ESP32 can send data, you must add the device in the Django admin dashboard:

### 1. Open Dashboard
- Go to `http://<your-server-ip>:8000/auth/dashboard/`
- Login with your credentials

### 2. Add Device
1. Click **"+ Add New Device"** button
2. Fill in exactly as configured in the sketch:
   - **Device Name:** `ESP32-Sensor-01` (must match `DEVICE_NAME`)
   - **Device ID:** `ESP32-001` (matches `DEVICE_ID`)
   - **Location:** e.g., "Living Room" (optional)
   - **Created Date:** (optional)
3. Click **"Add Device"** button

**Important:** The device name must match exactly what's in the sketch!

---

## 📊 Monitoring Data

### Serial Monitor Output
When everything is configured correctly, you'll see in the Serial Monitor:

```
========================================
ESP32 DHT22 Telemetry System
========================================

Initializing DHT22 sensor...
✓ WiFi Connected!
IP Address: 192.168.1.50
Signal Strength (RSSI): -65 dBm

Reading DHT22 sensor...
✓ Sensor Data Read: | Temp: 23.45°C | Humidity: 55.32%

Getting device ID from server: http://192.168.1.100:8000/api/api/device-id/?name=ESP32-Sensor-01
Response: {"id": 1}
✓ Device ID retrieved: 1

Sending data to: http://192.168.1.100:8000/api/api/data/
Payload: {"device": 1, "temperature": 23.45, "humidity": 55.32}
✓ Data sent successfully! Response: {"message": "Data saved successfully"}
```

### Django Dashboard
1. Go to your dashboard
2. Check the **"Recent Sensor Data"** section
3. You should see data being displayed with:
   - Device name
   - Temperature reading
   - Humidity percentage
   - Timestamp

---

## 🐛 Troubleshooting

### Issue: WiFi not connecting
**Serial Output:**
```
Starting WiFi connection...
SSID: MyHomeWiFi
..................
✗ Failed to connect to WiFi
Please check SSID and password
```

**Solutions:**
- Verify WiFi SSID and password are correct
- Check if ESP32 is in range of WiFi router
- Try restarting the ESP32 (press Reset button)
- Ensure WiFi network is 2.4GHz (ESP32 may not support 5GHz)

### Issue: DHT22 sensor not reading
**Serial Output:**
```
Reading DHT22 sensor...
✗ Error reading from DHT22 sensor!
  - Check if DHT22 is properly connected
  - Verify GPIO pin configuration
```

**Solutions:**
- Check all DHT22 wiring connections
- Verify 4.7kΩ pull-up resistor is connected
- Check if GPIO pin number matches in code
- Try different GPIO pin (e.g., GPIO 5) if available
- Replace DHT22 if sensor is faulty

### Issue: Device ID not found
**Serial Output:**
```
Getting device ID from server: http://192.168.1.100:8000/api/api/device-id/?name=ESP32-Sensor-01
✗ Error getting device ID. HTTP Response Code: 404
  Device not found on server!
  Please add the device through the admin dashboard first:
```

**Solutions:**
- Add the device in Django admin dashboard (see "Dashboard Registration" section)
- Verify device name matches exactly (case-sensitive)
- Check server URL/IP address is correct

### Issue: Data not sending to server
**Solutions:**
- Verify server is running: `python manage.py runserver`
- Check server URL is correct and accessible from ESP32
- Verify device was added in dashboard
- Check Django logs for errors
- Ensure firewall allows port 8000

### Issue: Serial Monitor shows garbage
**Solution:**
- Change baud rate to **115200** at the bottom of Serial Monitor

---

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      ESP32 Cycle                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Connect to WiFi                                        │
│     ↓                                                       │
│  2. Every 10 seconds:                                      │
│     ↓                                                       │
│     Read DHT22 sensor (temperature & humidity)             │
│     Store readings in memory                               │
│     ↓                                                       │
│  3. Every 30 seconds:                                      │
│     ↓                                                       │
│     Get device ID from server (if not cached)              │
│     ↓                                                       │
│     Send sensor data as JSON to /api/api/data/             │
│     ↓                                                       │
│     Server stores in database                              │
│     ↓                                                       │
│     Data appears in Django dashboard                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 API Endpoints Reference

### Get Device ID
```
GET /api/api/device-id/?name=ESP32-Sensor-01
Response: {"id": 1}
```

### Send Sensor Data
```
POST /api/api/data/
Content-Type: application/json

{
    "device": 1,
    "temperature": 23.45,
    "humidity": 55.32
}

Response: {"message": "Data saved successfully"}
```

---

## ✅ Checklist Before Testing

- [ ] DHT22 sensor connected to GPIO 4
- [ ] 4.7kΩ pull-up resistor installed
- [ ] WiFi SSID and password configured
- [ ] Server IP/domain configured in sketch
- [ ] Device name and ID configured
- [ ] Device added to Django dashboard
- [ ] Django server running (`python manage.py runserver`)
- [ ] ESP32 connected via USB and uploaded
- [ ] Serial Monitor opened at 115200 baud

---

## 🎯 Expected Results

After proper setup, you should see:
1. ✅ ESP32 connects to WiFi
2. ✅ DHT22 readings appear in Serial Monitor
3. ✅ Device ID retrieved from server
4. ✅ Data sent successfully every 30 seconds
5. ✅ Data visible in Django dashboard under "Recent Sensor Data"

---

## 📞 Support Resources

- **ESP32 Documentation:** https://docs.espressif.com/
- **Arduino Documentation:** https://www.arduino.cc/reference/
- **DHT Library:** https://github.com/adafruit/DHT-sensor-library
- **Django Documentation:** https://docs.djangoproject.com/

---

## 💡 Tips for Success

1. **Test WiFi connection first** before worrying about sensors
2. **Use Serial Monitor** to debug issues
3. **Start with small intervals** (10s/30s) for testing
4. **Verify device name matches** between sketch and dashboard
5. **Check IP address format** when accessing remote servers
6. **Keep sketch simple** - add features after basic functionality works

---

## 🔐 Security Considerations (Future)

- Use HTTPS instead of HTTP in production
- Add authentication tokens to API requests
- Implement rate limiting on device uploads
- Use environment variables for WiFi credentials
- Consider encrypted storage of server URLs

