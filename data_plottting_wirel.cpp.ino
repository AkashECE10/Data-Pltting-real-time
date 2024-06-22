#include <M5StickCPlus2.h>
#include <WiFi.h>

const char *ssid = "M5StickCPlus2_AP";
const char *password = "12345678";
WiFiServer server(80);

void setup() {
    M5.begin();
    Serial.begin(115200);

    // Initialize IMU
    if (M5.Imu.init() != 0) {
        Serial.println("IMU initialization failed");
    } else {
        Serial.println("IMU Initialized");
    }

    // Initialize Wi-Fi in AP mode
    WiFi.softAP(ssid, password);
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);

    // Start the server
    server.begin();
}

void loop() {
    WiFiClient client = server.available();
    if (client) {
        Serial.println("New Client Connected.");

        while (client.connected()) {
            float ax, ay, az;
            float gx, gy, gz;
            float temperature = 0; // Variable to store temperature

            // Read acceleration data
            M5.Imu.getAccelData(&ax, &ay, &az);
            // Read gyroscope data
            M5.Imu.getGyroData(&gx, &gy, &gz);

            // Dummy temperature value
            temperature = 25.0;

            // Send data to client
            String data = String(ax) + "," + String(ay) + "," + String(az) + "," +
                          String(gx) + "," + String(gy) + "," + String(gz) + "\n";
            client.print(data);

            delay(500);
        }

        client.stop();
        Serial.println("Client Disconnected.");
    }
}
