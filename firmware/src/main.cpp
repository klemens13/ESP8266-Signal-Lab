#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>

// Optional receive-only NMEA input: GPS TX -> D6/GPIO12, shared GND.
// Move these pins if your board uses them for other hardware.
static const uint8_t GPS_RX_PIN = D6;
static const uint8_t GPS_TX_PIN = D5;  // Unused by a receive-only GPS module.
static const uint32_t GPS_BAUD = 9600;
static const uint32_t SCAN_INTERVAL_MS = 10000;

SoftwareSerial gpsSerial(GPS_RX_PIN, GPS_TX_PIN);
TinyGPSPlus gps;
uint32_t lastScanMs = 0;

String csvEscape(const String &value) {
  String escaped = "\"";
  for (size_t i = 0; i < value.length(); ++i) {
    if (value[i] == '\"') escaped += '\"';
    escaped += value[i];
  }
  escaped += '\"';
  return escaped;
}

String securityName(uint8_t encryption) {
  switch (encryption) {
    case ENC_TYPE_NONE: return "open";
    case ENC_TYPE_WEP: return "wep";
    case ENC_TYPE_TKIP: return "wpa_tkip";
    case ENC_TYPE_CCMP: return "wpa_ccmp";
    case ENC_TYPE_AUTO: return "auto";
    default: return "unknown";
  }
}

void readGps() {
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }
}

void printRecord(int index) {
  const String ssid = WiFi.SSID(index);
  const String bssid = WiFi.BSSIDstr(index);
  Serial.print("SCAN | ELAPSED_MS=");
  Serial.print(millis());
  Serial.print(" | SSID=");
  Serial.print(csvEscape(ssid));
  Serial.print(" | BSSID=");
  Serial.print(bssid);
  Serial.print(" | RSSI_DBM=");
  Serial.print(WiFi.RSSI(index));
  Serial.print(" | CHANNEL=");
  Serial.print(WiFi.channel(index));
  Serial.print(" | SECURITY=");
  Serial.print(securityName(WiFi.encryptionType(index)));
  Serial.print(" | LATITUDE=");
  if (gps.location.isValid() && gps.location.age() < 10000) Serial.print(gps.location.lat(), 6);
  Serial.print(" | LONGITUDE=");
  if (gps.location.isValid() && gps.location.age() < 10000) Serial.print(gps.location.lng(), 6);
  Serial.print(" | ALTITUDE_M=");
  if (gps.altitude.isValid() && gps.altitude.age() < 10000) Serial.print(gps.altitude.meters(), 1);
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(GPS_BAUD);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  Serial.println("ESP8266 Signal Lab: passive scan mode");
  Serial.println("No attack or access-point impersonation features are enabled.");
}

void loop() {
  readGps();
  const uint32_t now = millis();
  if (now - lastScanMs < SCAN_INTERVAL_MS) return;
  lastScanMs = now;

  const int count = WiFi.scanNetworks(false, true);
  readGps();
  if (count == WIFI_SCAN_FAILED) {
    Serial.println("STATUS | RESULT=scan_failed");
  } else {
    Serial.printf("STATUS | RESULT=scan_complete | COUNT=%d\n", count);
    for (int i = 0; i < count; ++i) {
      printRecord(i);
      readGps();
    }
  }
  WiFi.scanDelete();
}
