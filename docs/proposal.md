## System Overview

The ESP32 acts as the core of the black box system, where multiple sensors (such as the DHT22) are connected to collect environmental data. This data is read and processed by the ESP32, then transmitted over WiFi to a Django-based backend server.
Django is responsible for handling user accounts, authentication, and database management. It stores the incoming sensor data and provides a web interface where users and administrators can view, manage, and interact with the data.
The overall data flow consists of sensors collecting data → ESP32 processing and sending the data → Django storing it in a database → users accessing the data through a web application.


