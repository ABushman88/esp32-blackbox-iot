# ESP32 Quick Reference & Configuration

## 🔌 GPIO Pin Reference for ESP32

```
ESP32 DEVKIT C PINOUT

                          ┌─────────────────────────────────┐
                          │         ESP32 DevKit C          │
                          │                                 │
          ┌───────────────┤                                 ├───────────────┐
          │               │                                 │               │
    GND ◄─┤ GND           │                                 │ VIN ►──────────┤ USB
    3V3 ◄─┤ 3.3V          │                                 │ GND           │
    34 ◄─┤ D34           │                                 │ D23           ├─► GPIO 23
    35 ◄─┤ D35           │                                 │ D22           ├─► GPIO 22
    32 ◄─┤ D32           │                                 │ TX0(1)        │
    33 ◄─┤ D33           │                                 │ RX0(3)        │
    25 ◄─┤ D25           │                                 │ D21           ├─► GPIO 21
    26 ◄─┤ D26           │                                 │ D20           │
    27 ◄─┤ D27           │                                 │ GND           │
    14 ◄─┤ D14           │                                 │ D19           ├─► GPIO 19
    12 ◄─┤ D12           │                                 │ D18           ├─► GPIO 18
    13 ◄─┤ D13       ┌───┤ USB UART                       ├─ D17          │
    GND ◄─┤ GND      │   │                                 │ D16           │
    GND ◄─┤ GND      │   │ For Programming                 │ GND           │
    VIN ◄─┤ VIN      │   │ TX/RX Pins (Auto-Reset)        │ D4 ◄──────── GPIO 4 (DHT22 DATA)
    5V  ◄─┤ 5V       └───┤                                 │ D0            │
    EN  ◄─┤ EN            │                                 │ D2            │
          │               │                                 │ D15           │
          └───────────────┤                                 ├───────────────┘
                          └─────────────────────────────────┘

GPIO 4 = DHT22 Data Pin (Recommended)
GPIO 5 = Alternative for DHT22 Data Pin
GPIO 2 = Built-in LED (useful for debugging)
```

---

## 🛠️ Configuration Cheat Sheet

### WiFi Setup
```cpp
// Change these three lines:
const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* SERVER_URL = "http://192.168.1.100:8000";
```

### Device Setup
```cpp
// Change these two lines to match your Django device:
const char* DEVICE_NAME = "ESP32-Sensor-01";    // Must match dashboard name exactly
const char* DEVICE_ID = "ESP32-001";            // Unique ID
```

### Sensor Pin Setup
```cpp
#define DHTPIN 4        // GPIO pin connected to DHT22 DATA pin
#define DHTTYPE DHT22   // Sensor type (DHT11 or DHT22)
```

### Timing Setup
```cpp
const unsigned long SENSOR_READ_INTERVAL = 10000;   // 10 seconds (10000 ms)
const unsigned long SEND_DATA_INTERVAL = 30000;     // 30 seconds (30000 ms)
const unsigned long WIFI_RETRY_INTERVAL = 5000;     // 5 seconds (5000 ms)
```

---

## 🔧 Arduino IDE Setup One-Liner

1. **Board Manager URL:**
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```

2. **Board:** ESP32 Dev Module
3. **Port:** COM3 (or your serial port)
4. **Baud Rate:** 115200
5. **Flash Mode:** DIO
6. **CPU Frequency:** 80 MHz

---

## 📦 Required Libraries (Install via Arduino IDE)

| Library | Author | Status |
|---------|--------|--------|
| DHT sensor library | Adafruit | Required |
| Adafruit Unified Sensor | Adafruit | Required (Dependency) |
| WiFi | Built-in | Built-in |
| HTTPClient | Built-in | Built-in |

**Install:** Sketch → Include Library → Manage Libraries → Search and Install

---

## 🎯 Step-by-Step Connection Guide

### DHT22 to ESP32 Wiring

```
DHT22 Sensor Front View:
┌────────────────┐
│ ┌──────────────┐│
│ │    DHT22     ││
│ └──────────────┘│
├──┬──┬──┬──┬──┬──┤
1  2  3  4
│  │  │  │
│  │  │  └─────────────────→ GND → ESP32 GND Pin
│  │  │
│  │  └─ NC (Not Connected)
│  │
│  └─ DATA (Signal) → [4.7kΩ Resistor] → ESP32 GPIO 4
│                                          └─ Pull-up to 3.3V
│
└─ VCC (Power) ──────────────→ ESP32 3.3V Pin
```

**Pull-up Resistor Connection:**
```
ESP32 3.3V ──[4.7kΩ]──┬──→ ESP32 GPIO 4 (DHT22 DATA)
                       │
                 DHT22 Pin 2
```

---

## 📋 Board Setup Guide

### In Arduino IDE:

**Tools Menu:**
```
Tool             Setting
──────────────────────────────────────
Board            ESP32 Dev Module
Port             COM3 (or your port)
CPU Frequency    80 MHz
Flash Mode       DIO
Flash Size       4MB
Flash Freq       40MHz
Upload Speed     921600
Partition Scheme Default
Core Debug       None
PSRAM            Disabled
```

---

## ✅ Pre-Upload Checklist

```
□ WiFi SSID entered correctly
□ WiFi Password entered correctly
□ Server URL correct (e.g., http://192.168.1.100:8000)
□ Device Name matches Django dashboard name
□ Device ID is unique
□ GPIO pin is 4 (or correct for your setup)
□ DHT22 is DHT22 (not DHT11)
□ Sensor connected to GPIO 4
□ 4.7kΩ pull-up resistor installed
□ ESP32 connected via USB
□ Serial port selected correctly
□ Baud rate set to 115200
□ Sketch verified without errors
```

---

## 🟢 Success Indicators

### Serial Monitor Should Show:
```
========================================
ESP32 DHT22 Telemetry System
========================================

Initializing DHT22 sensor...
Starting WiFi connection...
SSID: YOUR_SSID
.................
✓ WiFi Connected!
IP Address: 192.168.X.X
Signal Strength (RSSI): -XX dBm

Reading DHT22 sensor...
✓ Sensor Data Read: | Temp: 23.45°C | Humidity: 55.32%

Getting device ID from server: http://192.168.1.100:8000/api/api/device-id/?name=ESP32-Sensor-01
Response: {"id": 1}
✓ Device ID retrieved: 1

Sending data to: http://192.168.1.100:8000/api/api/data/
Payload: {"device": 1, "temperature": 23.45, "humidity": 55.32}
✓ Data sent successfully! Response: {"message": "Data saved successfully"}
```

### Dashboard Should Show:
- Device appears in "Devices" table
- Sensor data appears in "Recent Sensor Data" section
- New data every 30 seconds

---

## 🚨 Common Error Messages & Fixes

### Error 1: "Error reading from DHT22 sensor!"
```
Causes:
  - Wrong GPIO pin
  - Loose DHT22 connection
  - Missing pull-up resistor
  - Faulty sensor

Fix:
  1. Check wiring with multimeter
  2. Try GPIO 5 instead of GPIO 4
  3. Verify pull-up resistor 4.7kΩ
  4. Replace sensor if needed
```

### Error 2: "Device not found on server!"
```
Causes:
  - Device name doesn't match
  - Device not added to dashboard
  - Typo in device name

Fix:
  1. Go to Django dashboard
  2. Add device with exact name
  3. Verify case-sensitive match
```

### Error 3: "WiFi not connected"
```
Causes:
  - Wrong SSID or password
  - WiFi out of range
  - 5GHz network (ESP32 needs 2.4GHz)
  - WiFi disabled

Fix:
  1. Verify SSID and password
  2. Move ESP32 closer to router
  3. Use 2.4GHz WiFi band
  4. Restart router
```

### Error 4: "HTTP Response Code: 404"
```
Causes:
  - Server URL wrong
  - Server not running
  - Port not accessible
  - Device still not added

Fix:
  1. Check server URL format
  2. Start Django: python manage.py runserver
  3. Check firewall port 8000
  4. Add device to database
```

---

## 🔄 Timing Intervals Explained

```
Time   Event
═══════════════════════════════════════════════════════════
0s     +-- WiFi Check
       +-- Device connects to WiFi
       +-- Start loop
       
10s    +-- Read DHT22 sensor
       +-- Store data in memory
       +-- Print to Serial Monitor
       
20s    +-- DHT22 read again (10s interval)
       
30s    +-- Get Device ID from server
       +-- Send stored sensor data to server
       +-- Receive confirmation
       +-- Print success message
       
40s    +-- DHT22 read
       
50s    +-- DHT22 read
       
60s    +-- Get Device ID (if needed)
       +-- Send next batch of sensor data
       
... pattern repeats
```

**Recommended Settings:**
- **Development/Testing:** SENSOR_READ=5s, SEND_DATA=15s
- **Production:** SENSOR_READ=30s, SEND_DATA=60s
- **Low Power:** SENSOR_READ=60s, SEND_DATA=300s (5 min)

---

## 📝 Serial Monitor Baud Rates

| Baud Rate | Result |
|-----------|--------|
| 9600 | Garbage characters |
| 115200 | ✅ **Correct** |
| 230400 | Possible garbage |

**Always use 115200 for this sketch**

---

## 🌐 Server URL Examples

| Network | URL | Notes |
|---------|-----|-------|
| Local Network | `http://192.168.1.100:8000` | Replace IP with your server |
| Different Subnet | `http://192.168.100.50:8000` | Must be same network or port-forwarded |
| Cloud Server | `http://myserver.example.com:8000` | Public domain |
| Testing | `http://127.0.0.1:8000` | Only works if on same machine |

---

## 💾 Backup Configuration

Save your working configuration:

```cpp
// YOUR WORKING CONFIG - SAVE THIS
const char* WIFI_SSID = "MyHomeWiFi";
const char* WIFI_PASSWORD = "MyPassword123";
const char* SERVER_URL = "http://192.168.1.100:8000";
const char* DEVICE_NAME = "ESP32-Sensor-01";
const char* DEVICE_ID = "ESP32-001";
#define DHTPIN 4
```

---

## 🔌 Alternative GPIO Pins

If GPIO 4 is needed for something else:

| Pin | Voltage | Notes |
|-----|---------|-------|
| GPIO 4 | 3.3V | ✅ Recommended for DHT22 |
| GPIO 5 | 3.3V | ✅ Good alternative |
| GPIO 12 | 3.3V | ✅ Also works |
| GPIO 13 | 3.3V | ✅ Also works |
| GPIO 14 | 3.3V | ✅ Also works |
| GPIO 2 | 3.3V | Debug LED alternative |
| GPIO 15 | 3.3V | Also works |

**Pins to AVOID:**
- GPIO 0, 1, 3 (UART, programming)
- GPIO 6-11 (Flash memory)
- Analog-only pins (ADC pins)

---

## 📞 Debugging Tips

1. **Always open Serial Monitor at 115200 baud**
2. **Check Serial Monitor immediately after upload**
3. **Press ESP32 Reset button if no output**
4. **Keep outdoor antenna on chip if you have one**
5. **Use good quality USB cable** (cheap ones cause issues)
6. **Keep WiFi password less than 32 characters**
7. **Device name is case-sensitive**
8. **Check server is actually running before testing**

