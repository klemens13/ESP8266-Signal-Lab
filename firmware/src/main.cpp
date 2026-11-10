#include <ESP8266WiFi.h>

const int SCAN_INTERVAL_MS = 5000;

void printScanResult(int networkIndex) {
  Serial.printf("SSID=%s | RSSI=%d dBm | CH=%d | BSSID=%s | SEC=%s\n",
                WiFi.SSID(networkIndex).c_str(),
                WiFi.RSSI(networkIndex),
                WiFi.channel(networkIndex),
                WiFi.BSSIDstr(networkIndex).c_str(),
                WiFi.encryptionType(networkIndex) == ENC_TYPE_NONE ? "Open" : "Encrypted");
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.println("ESP8266 Signal Lab starting...");
  Serial.println("Scanning nearby WiFi networks...");
}

void loop() {
  int networkCount = WiFi.scanNetworks(false, true);

  if (networkCount == WIFI_SCAN_FAILED) {
    Serial.println("Scan failed");
  } else {
    Serial.printf("Found %d networks\n", networkCount);

    for (int i = 0; i < networkCount; i++) {
      printScanResult(i);
    }
  }

  WiFi.scanDelete();
  Serial.println("---");
  delay(SCAN_INTERVAL_MS);
}
