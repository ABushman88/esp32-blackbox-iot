## Data Model Design

### Device
The Device Model represents the physical ESP32 unit used for data collection.

- name: A user-defined name for the device (e.g., "Blackbox #1)
- device_id: A unique identifier for each ESP32 device
- owner: The user who owns and manages the device

### SensorReading
The Sensorreading model represents individual data points colected from sensors connected to a device.

- device: The device that generated the reading (foreign key relationship)
- sensor_type: The type of sensor data (e.g., temperature, humidity)
- value: The recorded sensor value
- timestamp: The date and time when the reading was captured
