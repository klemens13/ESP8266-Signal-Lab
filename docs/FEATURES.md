# Feature scope and upstream mapping

ESP8266 Signal Lab brings together the broad ideas represented by the four source projects while maintaining a passive, privacy-conscious scope.

| Source project | Theme represented here | Scope / limitation |
| --- | --- | --- |
| Nugget-Invader | ESP8266-based WiFi learning and reconnaissance | Passive access-point scan only; no attack menu or packet transmission. |
| esp8266_deauther | ESP8266 wireless testing context | Active deauthentication, disruption, spoofing, and fake-network features are intentionally not included. |
| ESP8266-Wardriving | GPS-tagged scans and later data visualization | Optional GPS fix can be logged locally; only use with explicit permission and protect location data. |
| HaxxDetector | Awareness of deauthentication/disassociation events | This starter does not capture raw management frames. Scan anomalies may prompt investigation but cannot confirm a deauthentication event. |

## What the scan anomaly review can tell you

The notebook can flag an access point that disappears from consecutive scans or shows a substantial signal change. Such observations can result from movement, obstruction, channel changes, scan timing, power state, or radio conditions. They are **not proof** of an attack and must not be used to attribute intent.

For actual protocol-level incident response, use authorized monitoring equipment and validated methods in a controlled environment. This project remains a passive telemetry collector and does not transmit disruptive frames.
