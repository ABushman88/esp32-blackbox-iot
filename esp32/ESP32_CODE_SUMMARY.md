# ESP32 Code Summary & API Integration

## 📄 Code Overview

The ESP32 sketch (`esp32_telemetry_dht22.ino`) implements a complete IoT telemetry system that:

1. **Connects to WiFi** - Handles connection and reconnection
2. **Reads DHT22 Sensor** - Gets temperature and humidity data
3. **Communicates with Django Backend** - Sends data via HTTP REST API
4. **Manages Device Registration** - Registers with the server
5. **Sends Data Periodically** - Configurable intervals for readings and uploads

---

## 🔄 Program Flow

```
START
  │
  ├─→ Initialize Serial (debugging)
  │
  ├─→ Initialize DHT22 Sensor
  │
  ├─→ Connect to WiFi
  │     (Loop until connected)
  │
  └─→ MAIN LOOP (infinite)
       │
       ├─→ Check WiFi Connection
       │     (Reconnect if needed)
       │
       ├─→ Every 10 seconds:
       │     └─→ Read DHT22 sensor
       │          └─→ Get Temperature & Humidity
       │          └─→ Store in global variables
       │
       ├─→ Every 30 seconds:
       │     ├─→ If Device ID not known:
       │     │     └─→ GET /api/api/device-id/?name=ESP32-Sensor-01
       │     │          └─→ Parse device ID from response
       │     │
       │     └─→ If Device ID known:
       │           └─→ POST /api/api/data/
       │                └─→ Send: {"device": id, "temperature": XX, "humidity": YY}
       │                └─→ Receive confirmation
       │
       └─→ Loop continues...
```

---

## 📡 HTTP API Calls

### 1. Get Device ID

**Purpose:** Register device and get its ID from the server

**Request:**
```http
GET /api/api/device-id/?name=ESP32-Sensor-01 HTTP/1.1
Host: 192.168.1.100:8000
Connection: close
```

**Response (Success - 200):**
```json
{"id": 1}
```

**Response (Not Found - 404):**
```json
{"error": "Device not found"}
```

**When Called:**
- On first boot (if device_id == -1)
- Every 30 seconds if device_id is still unknown
- Never if device_id is successfully obtained

**Code Location:**
```cpp
void getDeviceID() {
    // Lines 140-170
}
```

---

### 2. Send Sensor Data

**Purpose:** Upload temperature and humidity readings to database

**Request:**
```http
POST /api/api/data/ HTTP/1.1
Host: 192.168.1.100:8000
Content-Type: application/json
Content-Length: 58
Connection: close

{"device": 1, "temperature": 23.45, "humidity": 55.32}
```

**Response (Success - 200/201):**
```json
{"message": "Data saved successfully"}
```

**Response (Error - 400/500):**
```json
{"error": "Invalid data"}
```

**When Called:**
- Every 30 seconds (if WiFi is connected and Device ID is known)
- Sends last read temperature & humidity values

**Code Location:**
```cpp
void sendSensorData() {
    // Lines 180-220
}
```

---

## 🔧 Main Functions

### `setup()`
- **Location:** Lines 58-72
- **Called:** Once at startup
- **Does:**
  1. Initialize Serial debugging
  2. Initialize DHT22 sensor
  3. Connect to WiFi
  4. Print startup messages

### `loop()`
- **Location:** Lines 76-97
- **Called:** Continuously (thousands of times per second)
- **Does:**
  1. Check WiFi connection status
  2. Trigger sensor reads every 10 seconds
  3. Trigger data sends every 30 seconds
  4. Small delay to prevent watchdog timeout

### `connectToWiFi()`
- **Location:** Lines 103-125
- **Does:**
  1. Start WiFi connection
  2. Loop until connected (max 20 attempts)
  3. Print IP address and signal strength
  4. Handle connection failures

### `readSensorData()`
- **Location:** Lines 131-163
- **Does:**
  1. Read humidity from DHT22
  2. Read temperature from DHT22
  3. Validate readings (check for NaN errors)
  4. Store values globally
  5. Print results to Serial Monitor

### `getDeviceID()`
- **Location:** Lines 169-208
- **Does:**
  1. Check WiFi connection
  2. Build API URL with device name
  3. Make HTTP GET request
  4. Parse JSON response
  5. Store device ID globally

### `sendSensorData()`
- **Location:** Lines 214-253
- **Does:**
  1. Check WiFi connection
  2. Check device ID is available
  3. Build JSON payload
  4. Make HTTP POST request
  5. Handle success/error responses

---

## 🌐 Networking

### WiFi Connection
```cpp
WiFi.begin(WIFI_SSID, WIFI_PASSWORD);  // Start connection
WiFi.status() == WL_CONNECTED           // Check if connected
WiFi.localIP()                          // Get assigned IP
WiFi.RSSI()                             // Get signal strength
```

### HTTP Requests
```cpp
HTTPClient http;
http.begin(url);                        // Start request
http.addHeader("Content-Type", "application/json");
int code = http.GET();                  // HTTP GET
int code = http.POST(jsonData);         // HTTP POST
String response = http.getString();     // Get response body
http.end();                             // Close connection
```

---

## 📊 Sensor Data

### DHT22 Readings
```cpp
DHT dht(DHTPIN, DHTTYPE);               // Initialize on GPIO 4
float humidity = dht.readHumidity();    // 0-100%
float temperature = dht.readTemperature();  // In Celsius
```

### Data Stored
```cpp
float temperatureData;  // Current temperature reading
float humidityData;     // Current humidity reading
int deviceID;           // Device ID from server (-1 if not obtained)
```

---

## ⏱️ Timing

### Key Intervals
```cpp
SENSOR_READ_INTERVAL = 10000 ms   (10 seconds)
SEND_DATA_INTERVAL = 30000 ms     (30 seconds)
WIFI_RETRY_INTERVAL = 5000 ms     (5 seconds)

lastSensorReadTime       // Tracks last sensor read
lastDataSendTime         // Tracks last data send
lastWiFiRetryTime        // Tracks last WiFi retry
```

### Timing Logic
```cpp
if (millis() - lastSensorReadTime >= SENSOR_READ_INTERVAL) {
    readSensorData();
    lastSensorReadTime = millis();  // Reset timer
}
```

---

## 🔌 GPIO Configuration

```cpp
#define DHTPIN 4          // GPIO 4 for DHT22 data pin
#define DHTTYPE DHT22     // Sensor type specification

// ESP32 Pin Configuration:
// GPIO 4  = DHT22 DATA (with 4.7kΩ pull-up)
// GND     = DHT22 GND
// 3.3V    = DHT22 VCC
```

---

## 📝 Configuration Variables

Located at top of file (lines 6-29):

| Variable | Type | Purpose | Example |
|----------|------|---------|---------|
| WIFI_SSID | const char* | WiFi network name | "MyWiFi" |
| WIFI_PASSWORD | const char* | WiFi password | "Password123" |
| SERVER_URL | const char* | Django server address | "http://192.168.1.100:8000" |
| API_DATA_ENDPOINT | const char* | Sensor data endpoint | "/api/api/data/" |
| API_DEVICE_ENDPOINT | const char* | Device ID endpoint | "/api/api/device-id/" |
| DEVICE_NAME | const char* | Device name for registration | "ESP32-Sensor-01" |
| DEVICE_ID | const char* | Unique device identifier | "ESP32-001" |
| DHTPIN | define | GPIO pin number | 4 |
| DHTTYPE | define | Sensor model | DHT22 |

---

## 🐛 Error Handling

### WiFi Errors
```cpp
WiFi.status() != WL_CONNECTED  // Not connected
// Handled by: connectToWiFi() and main loop retry logic
```

### Sensor Errors
```cpp
isnan(humidity) || isnan(temperature)  // Invalid reading
// Handled by: readSensorData() validation
```

### HTTP Errors
```cpp
httpResponseCode != 200        // Request failed
// Handled by: Response code checking and error messages
httpResponseCode == 404        // Device not found
// Handled by: Specific error message and guidance
```

---

## 📤 Example HTTP Transactions

### Successful Device ID Retrieval
```
→ GET /api/api/device-id/?name=ESP32-Sensor-01
← HTTP/1.1 200 OK
← {"id": 1}

Next step: Use id=1 for data uploads
```

### Successful Data Upload
```
→ POST /api/api/data/
→ Content-Type: application/json
→ {"device": 1, "temperature": 23.45, "humidity": 55.32}
← HTTP/1.1 200 OK
← {"message": "Data saved successfully"}

Result: Data stored in database, visible on dashboard
```

### Device Not Found Error
```
→ GET /api/api/device-id/?name=ESP32-Sensor-01
← HTTP/1.1 404 Not Found
← {"error": "Device not found"}

Next step: Add device to Django dashboard with matching name
```

---

## 🔐 Data Security

Current Implementation:
- ✅ HTTP POST requests (can be upgraded to HTTPS)
- ✅ JSON payload format
- ❌ No authentication tokens
- ❌ No encryption
- ❌ No rate limiting on client side

**Recommendations for Production:**
1. Use HTTPS instead of HTTP
2. Add API authentication tokens
3. Implement device-level security keys
4. Add data validation on backend
5. Implement rate limiting

---

## 📊 Serial Monitor Output Examples

### Startup Output
```
========================================
ESP32 DHT22 Telemetry System
========================================

Initializing DHT22 sensor...
Starting WiFi connection...
SSID: MyWiFi
.................
✓ WiFi Connected!
IP Address: 192.168.1.50
Signal Strength (RSSI): -65 dBm
```

### Normal Operation (Repeating)
```
Reading DHT22 sensor...
✓ Sensor Data Read: | Temp: 23.45°C | Humidity: 55.32%

Getting device ID from server: http://192.168.1.100:8000/api/api/device-id/?name=ESP32-Sensor-01
Response: {"id": 1}
✓ Device ID retrieved: 1

Sending data to: http://192.168.1.100:8000/api/api/data/
Payload: {"device": 1, "temperature": 23.45, "humidity": 55.32}
✓ Data sent successfully! Response: {"message": "Data saved successfully"}
```

### Error Output
```
✗ Error reading from DHT22 sensor!
  - Check if DHT22 is properly connected
  - Verify GPIO pin configuration
```

---

## 🔄 Data Cycle Visualization

```
Time    Sensor Read    Device ID Check    Data Send    Serial Output
────────────────────────────────────────────────────────────────────
0s                                                      WiFi connected
10s     ✓ Read 23.4°C
20s     ✓ Read 23.4°C
30s     ✓ Read 23.4°C   ✓ Get ID (id=1)    ✓ Send      ✓ Success
40s     ✓ Read 23.5°C
50s     ✓ Read 23.4°C
60s     ✓ Read 23.3°C             (cached)  ✓ Send      ✓ Success
70s     ✓ Read 23.4°C
80s     ✓ Read 23.5°C
90s     ✓ Read 23.4°C             (cached)  ✓ Send      ✓ Success
```

---

## 🎯 Next Steps for Enhancement

1. **Authentication:** Add API token or key
2. **HTTPS:** Upgrade from HTTP to HTTPS
3. **OTA Updates:** Add over-the-air firmware updates
4. **Local Storage:** Cache data if network fails
5. **Advanced Sensors:** Add pressure, light, etc.
6. **Power Management:** Deep sleep for battery operation
7. **Web Dashboard:** Real-time data visualization
8. **Mobile App:** Send notifications to smartphone

---

## 📞 Integration Checklist

- [ ] Arduino IDE installed with ESP32 support
- [ ] DHT library installed
- [ ] Sketch downloaded from `esp32_telemetry_dht22.ino`
- [ ] WiFi SSID/Password configured
- [ ] Server URL configured
- [ ] Device Name matches Django database
- [ ] DHT22 physically connected to GPIO 4
- [ ] 4.7kΩ pull-up resistor installed
- [ ] Sketch uploaded to ESP32
- [ ] Serial Monitor shows WiFi connection
- [ ] Device added to Django dashboard
- [ ] Serial Monitor shows successful data sends
- [ ] Dashboard shows new sensor data entries

