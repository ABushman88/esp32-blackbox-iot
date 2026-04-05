#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// ============================================================================
//                         CONFIGURATION SETTINGS
// ============================================================================

// WiFi Configuration
const char* WIFI_SSID = "YOUR_WIFI_SSID";           // Change this to your WiFi SSID
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";   // Change this to your WiFi password

// Server Configuration
const char* SERVER_URL = "http://192.168.1.128:8000"; // ← UPDATED WITH YOUR IP & PORT 8000
const char* API_DATA_ENDPOINT = "/api/api/data/";
const char* API_DEVICE_ENDPOINT = "/api/api/device-id/";

// Device Configuration
const char* DEVICE_NAME = "ESP32-Sensor-01";        // Give your device a unique name
const char* DEVICE_ID = "ESP32-001";                // Unique device ID

// DHT22 Sensor Configuration
#define DHTPIN 4                                    // GPIO pin connected to DHT22 data pin
#define DHTTYPE DHT22                               // DHT 22 (AM2302)
DHT dht(DHTPIN, DHTTYPE);

// Timing Configuration (in milliseconds)
const unsigned long SENSOR_READ_INTERVAL = 10000;   // Read sensor every 10 seconds
const unsigned long SEND_DATA_INTERVAL = 30000;     // Send data every 30 seconds
const unsigned long WIFI_RETRY_INTERVAL = 5000;     // Retry WiFi every 5 seconds

// ============================================================================
//                         GLOBAL VARIABLES
// ============================================================================

unsigned long lastSensorReadTime = 0;
unsigned long lastDataSendTime = 0;
unsigned long lastWiFiRetryTime = 0;

float temperatureData = 0.0;
float humidityData = 0.0;
int deviceID = -1;  // Will be obtained from server

// ============================================================================
//                         SETUP FUNCTION
// ============================================================================

void setup() {
  Serial.begin(115200);
  delay(2000); // Wait for Serial to initialize
  
  Serial.println("\n\n");
  Serial.println("========================================");
  Serial.println("ESP32 DHT22 Telemetry System");
  Serial.println("========================================\n");
  
  // Initialize DHT22 sensor
  Serial.println("Initializing DHT22 sensor...");
  dht.begin();
  delay(500);
  
  // Connect to WiFi
  connectToWiFi();
}

// ============================================================================
//                         MAIN LOOP
// ============================================================================

void loop() {
  // Check if WiFi is still connected
  if (WiFi.status() != WL_CONNECTED) {
    if (millis() - lastWiFiRetryTime >= WIFI_RETRY_INTERVAL) {
      Serial.println("\nWiFi disconnected! Attempting to reconnect...");
      connectToWiFi();
      lastWiFiRetryTime = millis();
    }
  } else {
    // Read sensor data at specified interval
    if (millis() - lastSensorReadTime >= SENSOR_READ_INTERVAL) {
      readSensorData();
      lastSensorReadTime = millis();
    }
    
    // Send data to server at specified interval
    if (millis() - lastDataSendTime >= SEND_DATA_INTERVAL) {
      if (deviceID == -1) {
        getDeviceID();  // Get device ID from server first
      }
      if (deviceID != -1) {
        sendSensorData();
      }
      lastDataSendTime = millis();
    }
  }
  
  delay(100);  // Small delay to prevent watchdog timeout
}

// ============================================================================
//                    WIFI CONNECTION FUNCTION
// ============================================================================

void connectToWiFi() {
  Serial.println("\nStarting WiFi connection...");
  Serial.print("SSID: ");
  Serial.println(WIFI_SSID);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    Serial.print("Signal Strength (RSSI): ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm\n");
  } else {
    Serial.println("\n✗ Failed to connect to WiFi");
    Serial.println("Please check SSID and password\n");
  }
}

// ============================================================================
//                    SENSOR DATA READING FUNCTION
// ============================================================================

void readSensorData() {
  Serial.println("Reading DHT22 sensor...");
  
  // Read humidity (%)
  float humidity = dht.readHumidity();
  
  // Read temperature (Celsius)
  float temperature = dht.readTemperature();
  
  // Check if readings are valid
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("✗ Error reading from DHT22 sensor!");
    Serial.println("  - Check if DHT22 is properly connected");
    Serial.println("  - Verify GPIO pin configuration");
    return;
  }
  
  // Store data for transmission
  temperatureData = temperature;
  humidityData = humidity;
  
  // Display readings
  Serial.print("✓ Sensor Data Read:");
  Serial.print(" | Temp: ");
  Serial.print(temperature);
  Serial.print("°C | Humidity: ");
  Serial.print(humidity);
  Serial.println("%");
}

// ============================================================================
//                    GET DEVICE ID FROM SERVER
// ============================================================================

void getDeviceID() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("✗ WiFi not connected, cannot get device ID");
    return;
  }
  
  HTTPClient http;
  
  // Build the request URL with device name parameter
  String url = String(SERVER_URL) + String(API_DEVICE_ENDPOINT) + "?name=" + String(DEVICE_NAME);
  
  Serial.print("Getting device ID from server: ");
  Serial.println(url);
  
  http.begin(url);
  int httpResponseCode = http.GET();
  
  if (httpResponseCode == 200) {
    String payload = http.getString();
    Serial.print("Response: ");
    Serial.println(payload);
    
    // Parse JSON response: {"id": 1}
    // For simplicity, we'll extract the id value
    if (payload.indexOf("\"id\"") != -1) {
      int idPos = payload.indexOf("\":") + 2;
      int endPos = payload.indexOf("}", idPos);
      String idStr = payload.substring(idPos, endPos);
      deviceID = idStr.toInt();
      Serial.print("✓ Device ID retrieved: ");
      Serial.println(deviceID);
    }
  } else {
    Serial.print("✗ Error getting device ID. HTTP Response Code: ");
    Serial.println(httpResponseCode);
    
    // If device doesn't exist, provide guidance
    if (httpResponseCode == 404) {
      Serial.println("  Device not found on server!");
      Serial.println("  Please add the device through the admin dashboard first:");
      Serial.print("  Device Name: ");
      Serial.println(DEVICE_NAME);
      Serial.print("  Device ID: ");
      Serial.println(DEVICE_ID);
    }
  }
  
  http.end();
}

// ============================================================================
//                    SEND SENSOR DATA TO SERVER
// ============================================================================

void sendSensorData() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("✗ WiFi not connected, cannot send data");
    return;
  }
  
  if (deviceID == -1) {
    Serial.println("✗ Device ID not obtained, cannot send data");
    return;
  }
  
  HTTPClient http;
  String url = String(SERVER_URL) + String(API_DATA_ENDPOINT);
  
  Serial.print("Sending data to: ");
  Serial.println(url);
  
  // Create JSON payload
  String jsonData = "{\"device\": " + String(deviceID) + 
                    ", \"temperature\": " + String(temperatureData, 2) + 
                    ", \"humidity\": " + String(humidityData, 2) + "}";
  
  Serial.print("Payload: ");
  Serial.println(jsonData);
  
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  int httpResponseCode = http.POST(jsonData);
  
  if (httpResponseCode == 200 || httpResponseCode == 201) {
    String response = http.getString();
    Serial.print("✓ Data sent successfully! Response: ");
    Serial.println(response);
  } else {
    Serial.print("✗ Error sending data. HTTP Response Code: ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    if (response.length() > 0) {
      Serial.print("  Error details: ");
      Serial.println(response);
    }
  }
  
  http.end();
}

// ============================================================================
//                    ERROR HANDLING & DIAGNOSTICS
// ============================================================================

void printWiFiDiagnostics() {
  Serial.println("\n=== WiFi Diagnostics ===");
  Serial.print("WiFi Status: ");
  switch(WiFi.status()) {
    case WL_NO_SSID_AVAIL: Serial.println("SSID not found"); break;
    case WL_CONNECT_FAILED: Serial.println("Connection failed"); break;
    case WL_DISCONNECTED: Serial.println("Disconnected"); break;
    case WL_CONNECTED: Serial.println("Connected"); break;
    default: Serial.println("Unknown");
  }
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Signal Strength: ");
  Serial.println(WiFi.RSSI());
  Serial.println("========================\n");
}

// ============================================================================
//                    DEBUG/LOGGING FUNCTIONS (Optional)
// ============================================================================

// Uncomment this function and call it in setup() for extended diagnostics
void printStartupInfo() {
  Serial.println("\n=== ESP32 System Information ===");
  Serial.print("Chip Model: ");
  Serial.println(ESP.getChipModel());
  Serial.print("Chip Revision: ");
  Serial.println(ESP.getChipRevision());
  Serial.print("Free Heap: ");
  Serial.println(ESP.getFreeHeap());
  Serial.print("Sketch Size: ");
  Serial.println(ESP.getSketchSize());
  Serial.println("================================\n");
}
