# ESP32 Integration Checklist & Verification Guide

## ✅ Pre-Setup Verification

Before you start, verify you have:

### Hardware
- [ ] ESP32 Development Board (ESP32 DevKit C recommended)
- [ ] DHT22 Temperature/Humidity Sensor
- [ ] USB Micro-B cable (for programming)
- [ ] 4.7kΩ Resistor (for pull-up)
- [ ] Jumper wires (minimum 4)
- [ ] Breadboard (optional but recommended)
- [ ] WiFi router with 2.4GHz band

### Software
- [ ] Arduino IDE (version 2.0+)
- [ ] ESP32 Board Package installed
- [ ] DHT Sensor Library installed
- [ ] Django server running (`python manage.py runserver`)
- [ ] Device added to Django dashboard

### Information Ready
- [ ] WiFi SSID (network name)
- [ ] WiFi password
- [ ] Server IP address (e.g., 192.168.1.100)
- [ ] Server port (usually 8000)
- [ ] Device name (must match Django exactly)
- [ ] Device ID (unique identifier)

---

## 🔌 Hardware Assembly Verification

### Step 1: DHT22 Pinout Identification
```
Front of DHT22 (flat side):

  ↓ This side is flat
┌──────────────────────┐
│  DHT22 Sensor        │
└──────────────────────┘
└─ ┴ ┴ ┴ ┴ ┴
│  │  │  │  │
1  2  3  4  (back pins)
```

### Step 2: Pin Identification
| Pin | Name | Connection |
|-----|------|-----------|
| 1 | VCC | 3.3V (Power) |
| 2 | DATA | GPIO 4 (with 4.7kΩ pull-up) |
| 3 | NC | Not Connected |
| 4 | GND | Ground |

### Step 3: Verify Connections
```
DHT22          4.7kΩ Resistor      ESP32
────────────────────────────────────────
Pin 1 (VCC) ─────────────────────→ 3V3 Pin
                                    ↑
Pin 2 (DATA) ───[Resistor]─────────┤ GPIO 4
                                    ↓
Pin 4 (GND) ─────────────────────→ GND Pin
```

- [ ] DHT22 Pin 1 connected to ESP32 3V3
- [ ] DHT22 Pin 2 connected to GPIO 4 (with resistor)
- [ ] 4.7kΩ resistor between 3V3 and GPIO 4
- [ ] DHT22 Pin 4 connected to ESP32 GND
- [ ] DHT22 Pin 3 left unconnected
- [ ] All connections secure (no loose wires)
- [ ] No shorts between pins

---

## 💻 Software Installation Verification

### Step 1: Arduino IDE Setup
```
✓ Arduino IDE 2.0+ installed from https://www.arduino.cc/

In Arduino IDE:
  File > Preferences > Additional Boards Manager URLs:
  https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

  Tools > Board > Boards Manager:
  Search: esp32
  Install: "esp32" by Espressif Systems

- [ ] Arduino IDE installed
- [ ] Additional Board URL added
- [ ] ESP32 Board Package installed
```

### Step 2: Library Installation
```
In Arduino IDE:
  Sketch > Include Library > Manage Libraries

  Search: DHT
  Install: "DHT sensor library" by Adafruit (usually highest version)
  
  Search: Adafruit Unified Sensor
  Install: "Adafruit Unified Sensor" by Adafruit

- [ ] DHT sensor library installed
- [ ] Adafruit Unified Sensor installed
```

### Step 3: Verify Installation
```
In Arduino IDE:
  Sketch > Include Library > Contributed Libraries

Should show:
  ✓ Adafruit Unified Sensor
  ✓ DHT sensor library

- [ ] Libraries appear in Contributed Libraries list
- [ ] No errors when opening example sketches
```

---

## ⚙️ Configuration Checklist

Before uploading, configure the sketch:

### WiFi Configuration
Edit these lines (around line 8-9):
```cpp
const char* WIFI_SSID = "YOUR_WIFI_SSID";         // ← CHANGE THIS
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"; // ← CHANGE THIS
```

**Example:**
```cpp
const char* WIFI_SSID = "MyHomeWiFi";
const char* WIFI_PASSWORD = "SecurePassword123";
```

- [ ] WIFI_SSID set to your network name
- [ ] WIFI_PASSWORD set to your network password
- [ ] Password is correct (case-sensitive)
- [ ] Network is 2.4GHz (not 5GHz)

### Server Configuration
Edit this line (around line 11):
```cpp
const char* SERVER_URL = "http://192.168.1.X:8000"; // ← CHANGE THIS
```

**Example:**
```cpp
const char* SERVER_URL = "http://192.168.1.100:8000";
```

**How to find your server IP:**
1. Run: `ipconfig` in Command Prompt
2. Look for "IPv4 Address" under your network adapter
3. Example: 192.168.1.100

**For testing (same machine):**
```cpp
const char* SERVER_URL = "http://127.0.0.1:8000";
```

- [ ] SERVER_URL set to correct IP/domain
- [ ] Port is 8000 (or correct port)
- [ ] Format includes http:// or https://
- [ ] No trailing slash

### Device Configuration
Edit these lines (around line 15-16):
```cpp
const char* DEVICE_NAME = "ESP32-Sensor-01";  // ← MUST MATCH DJANGO
const char* DEVICE_ID = "ESP32-001";
```

**Important:** Device name MUST match exactly what you added in Django!

**Example:**
```cpp
const char* DEVICE_NAME = "Temperature-Sensor-Living-Room";  // Match this exactly
const char* DEVICE_ID = "ESP32-LR-01";
```

- [ ] DEVICE_NAME is unique and descriptive
- [ ] DEVICE_NAME matches Django device exactly (case-sensitive)
- [ ] DEVICE_ID is unique across all ESP32s
- [ ] Both are memorable/documented

### Sensor Configuration
Verify these lines (around line 19-21):
```cpp
#define DHTPIN 4        // GPIO pin 4
#define DHTTYPE DHT22   // DHT22 sensor
```

- [ ] DHTPIN is 4 (unless you connected to different GPIO)
- [ ] DHTTYPE is DHT22 (not DHT11)

---

## 🖥️ Arduino IDE Settings

### Board Selection
```
Tools Menu Settings:
├── Board: ESP32 Dev Module
├── Port: COM3 (or your serial port)
├── CPU Frequency: 80 MHz
├── Flash Mode: DIO
├── Flash Size: 4MB
├── Flash Freq: 40MHz
├── Upload Speed: 921600
└── Partition Scheme: Default
```

**Setting these:**
1. **Tools → Board:** Select "ESP32 Dev Module"
2. **Tools → Port:** Select your COM port (look in Device Manager)
3. **Tools → CPU Frequency:** 80 MHz
4. **Tools → Flash Mode:** DIO
5. **Tools → Upload Speed:** 921600

- [ ] Board set to ESP32 Dev Module
- [ ] Port selected (not grayed out)
- [ ] CPU Frequency: 80 MHz
- [ ] Flash Mode: DIO
- [ ] Upload Speed: 921600

### Finding Your Serial Port
**Windows:**
1. Plug in ESP32 via USB
2. Open Device Manager (Ctrl+Shift+Esc → Device Manager)
3. Look under "Ports (COM & LPT)"
4. Find "USB-SERIAL CH340" or "Silicon Labs CP210x" or similar
5. Note the COM number (e.g., COM3)

**In Arduino IDE:**
- Tools → Port → Select your COMx port

---

## 📤 Upload Procedure

### Pre-Upload Checklist
```
✓ WiFi configured correctly
✓ Server URL correct and Django running
✓ Device added to Django dashboard
✓ Device name matches exactly (case-sensitive)
✓ DHT22 connected to GPIO 4
✓ Pull-up resistor installed
✓ All connections secure
✓ ESP32 connected via USB
✓ COM port selected in Arduino IDE
✓ Board is "ESP32 Dev Module"
✓ Sketch opens without errors
```

### Upload Steps
1. **Verify Sketch**
   - Click the ✓ (Verify) button in Arduino IDE
   - Wait for "Sketch uses X bytes of program storage space"
   - No errors should appear

2. **Select Port**
   - Tools → Port → COM# (your port)

3. **Upload Sketch**
   - Click the → (Upload) button
   - Wait for "Connecting..."
   - You may see dots "....." during upload
   - Wait for "Hard resetting via RTS pin..."
   - Then "Upload Complete" message

4. **Open Serial Monitor**
   - Tools → Serial Monitor
   - Set baud to 115200 (bottom right)
   - Press ESP32 Reset button if needed
   - Should see startup messages

---

## 📊 Serial Monitor Verification

### Expected Output (Success)
```
========================================
ESP32 DHT22 Telemetry System
========================================

Initializing DHT22 sensor...
Starting WiFi connection...
SSID: MyHomeWiFi
.................
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

### Verification Checklist
- [ ] Startup messages appear within 2 seconds of upload
- [ ] No garbage characters (if you see garbage, baud rate is wrong)
- [ ] DHT22 sensor initializes successfully
- [ ] WiFi connects successfully
- [ ] IP address is assigned
- [ ] Signal strength is -90 or better (closer to 0 is better)
- [ ] Sensor readings show reasonable values
- [ ] Device ID is retrieved (1, 2, 3, etc.)
- [ ] Data sends successfully
- [ ] No error messages

### Serial Monitor Baud Rate
**⚠️ IMPORTANT:** Baud rate must be **115200**
```
Bottom right of Serial Monitor:
┌───────────┐
│▼ 115200 ◄─┘ (must be this)
└───────────┘
```

If you see garbage:
1. Check baud rate is 115200
2. Press ESP32 Reset button
3. Or close/reopen Serial Monitor

---

## 🌐 Django Dashboard Verification

### Add Device
1. Go to `http://192.168.1.100:8000/auth/dashboard/`
2. Login with your credentials
3. Click **"+ Add New Device"**
4. Fill in exactly:
   - **Device Name:** `ESP32-Sensor-01` (must match sketch)
   - **Device ID:** `ESP32-001`
   - **Location:** "Den" (optional)
5. Click **"Add Device"**

- [ ] Device appears in dashboard device list
- [ ] Device name matches sketch exactly
- [ ] Device ID is unique

### Verify Data Reception
1. Looking at dashboard, scroll to **"Recent Sensor Data"** section
2. New data should appear:
   - Device column shows device name
   - Temperature column shows a number (°C)
   - Humidity column shows a number (%)
   - Timestamp shows when data was received

- [ ] Sensor data table is not empty
- [ ] Temperature values look reasonable (15-35°C is normal room temp)
- [ ] Humidity values are 0-100%
- [ ] Timestamps are recent (within last minute)
- [ ] Data updates every 30 seconds

---

## 🚨 Troubleshooting Decision Tree

### Issue: Nothing appears in Serial Monitor
```
↓ Device plugged in via USB?
├─ NO  → Plug in USB cable
└─ YES → Continue

↓ Serial Monitor baud rate is 115200?
├─ NO  → Change to 115200, press Reset button
└─ YES → Continue

↓ Press ESP32 Reset button
↓ Messages now appear?
├─ NO  → Try different USB cable
├─ NO  → Try different USB port
└─ YES → Continue
```

### Issue: Garbage characters in Serial Monitor
```
↓ Baud rate is 115200?
├─ NO  → Change to 115200
└─ YES → Try different baud rate (230400)

↓ Try different USB cable (bad cable causes this)

↓ Reinstall COM drivers?
├─ Search for "CH340 driver" or "CP2102 driver"
└─ Install appropriate driver for your chip
```

### Issue: WiFi not connecting
```
Serial shows:
"✗ Failed to connect to WiFi
Please check SSID and password"

↓ Is SSID correct? (Check in code)
├─ NO  → Update WIFI_SSID
└─ YES → Continue

↓ Is password correct? (Check in code)
├─ NO  → Update WIFI_PASSWORD
└─ YES → Continue

↓ Is network 2.4GHz? (Not 5GHz)
├─ NO  → Connect to 2.4GHz band
└─ YES → Continue

↓ Move ESP32 closer to router
↓ Restart router
↓ Try again
```

### Issue: Device ID not found
```
Serial shows:
"✗ Error getting device ID. HTTP Response Code: 404
Device not found on server!"

↓ Is Django running?
├─ NO  → Run: python manage.py runserver
└─ YES → Continue

↓ Did you add the device to dashboard?
├─ NO  → Add device in Django admin
└─ YES → Continue

↓ Does device name match exactly?
├─ NO  → Update DEVICE_NAME in sketch
└─ YES → Continue

↓ Did you reload the dashboard after adding device?
├─ NO  → Refresh the page (F5)
└─ YES → Re-upload sketch to ESP32
```

### Issue: HTTP errors when sending data
```
Serial shows:
"Sending data to: http://192.168.1.100:8000/api/api/data/
✗ Error sending data. HTTP Response Code: 400"

↓ Is server URL correct?
├─ NO  → Update SERVER_URL
└─ YES → Continue

↓ Is Django running?
├─ NO  → Run: python manage.py runserver
└─ YES → Continue

↓ Can you reach server from computer?
├─ NO  → Check firewall, network settings
└─ YES → Check Django logs for errors
```

---

## ✅ Final Integration Test

### Complete Test Sequence
1. **Firmware Updated**
   - [ ] Sketch uploaded to ESP32
   - [ ] Serial Monitor shows startup messages

2. **WiFi Connected**
   - [ ] Serial shows "✓ WiFi Connected!"
   - [ ] IP address assigned
   - [ ] Signal strength shown

3. **Device Registered**
   - [ ] Device appears in Django dashboard
   - [ ] Device name matches exactly
   - [ ] Serial shows device ID retrieved

4. **Data Flowing**
   - [ ] Serial shows "✓ Data sent successfully!"
   - [ ] New entries in Recent Sensor Data table
   - [ ] Data updates every 30 seconds
   - [ ] No errors in Django logs

5. **Data Accuracy**
   - [ ] Temperature readings reasonable for room
   - [ ] Humidity readings between 0-100%
   - [ ] Multiple readings over time (verify consistency)
   - [ ] Timing intervals correct

---

## 📋 Quick Reference Card

Print this for your bench:

```
╔════════════════════════════════════════════════════════════╗
║     ESP32 DHT22 TELEMETRY SYSTEM - QUICK REFERENCE        ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║ SERIAL MONITOR:  115200 baud                             ║
║                                                            ║
║ ARDUINO IDE SETTINGS:                                    ║
║   Board: ESP32 Dev Module                               ║
║   Port: COM3 (your port)                                ║
║   CPU Freq: 80 MHz                                      ║
║   Flash Mode: DIO                                       ║
║   Upload Speed: 921600                                  ║
║                                                            ║
║ WIRING:                                                   ║
║   DHT22 Pin 1 (VCC) → ESP32 3V3                         ║
║   DHT22 Pin 2 (DATA) → GPIO 4 (with 4.7kΩ resistor)   ║
║   DHT22 Pin 4 (GND) → ESP32 GND                         ║
║   DHT22 Pin 3 (NC) → Not Connected                      ║
║                                                            ║
║ CRITICAL SETTINGS IN CODE:                              ║
║   WIFI_SSID = "Your WiFi"                              ║
║   WIFI_PASSWORD = "Your Password"                        ║
║   SERVER_URL = "http://192.168.1.100:8000"            ║
║   DEVICE_NAME = "ESP32-Sensor-01"                      ║
║   DHTPIN = 4                                            ║
║                                                            ║
║ DJANGO DASHBOARD:                                       ║
║   Add device with exact name: "ESP32-Sensor-01"        ║
║   Check "Recent Sensor Data" section                    ║
║                                                            ║
║ SUCCESS INDICATORS:                                      ║
║   ✓ Serial Monitor: "✓ WiFi Connected!"              ║
║   ✓ Serial Monitor: "✓ Device ID retrieved: 1"        ║
║   ✓ Serial Monitor: "✓ Data sent successfully!"        ║
║   ✓ Dashboard: New data in Recent Sensor Data          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## 📞 Support Contacts

If you encounter issues:

1. **Check Documentation:**
   - ESP32_SETUP_GUIDE.md (detailed setup)
   - ESP32_QUICK_REFERENCE.md (GPIO pins, troubleshooting)
   - ESP32_CODE_SUMMARY.md (code explanation)

2. **Check Serial Monitor Output:**
   - Most errors are clearly described in Serial Monitor output
   - Baud rate must be 115200

3. **Common Issues:**
   - No output: Different USB cable or port
   - Garbage text: Wrong baud rate
   - Can't connect to WiFi: Wrong SSID/password
   - 404 error: Device not added to dashboard or wrong name

4. **Resources:**
   - Arduino IDE Docs: arduino.cc
   - ESP32 Official: espressif.com
   - Django Docs: djangoproject.com

