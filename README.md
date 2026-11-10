# ESP8266 Signal Lab

An ethical, passive WiFi monitoring and analysis project that brings together the learning and reconnaissance themes of **Nugget-Invader**, **esp8266_deauther**, **ESP8266-Wardriving**, and **HaxxDetector**—without carrying over features that disrupt networks or impersonate access points.

Use it only in a lab or location where you have permission to monitor. WiFi identifiers and GPS coordinates can be sensitive; keep captures local, minimize retention, and get consent before collecting location-linked data.

## What this project includes

- **Passive WiFi survey:** ESP8266 scans visible access points and records SSID, BSSID, RSSI, channel, and security mode.
- **Optional consent-based GPS logging:** reads NMEA from a GPS module and attaches the most recent valid fix to scan records.
- **Local CSV collection:** Python serial collector saves measurements on your computer.
- **Signal and change analysis:** Jupyter notebook visualizes signal levels and flags unusual scan-to-scan changes for human review.
- **Ethical detection workflow:** supports review of suspicious wireless conditions; scan disappearance is only an indicator, not proof of deauthentication or an attack.
- **ESP8266 Nugget learning context:** firmware is a simple serial-driven scanner suitable for compatible ESP8266 boards.

## What it deliberately excludes

This is a defensive, passive project. It does **not** transmit deauthentication/disassociation frames, jam, spoof access points, create deceptive networks, or automate attacks. It also does not claim that ordinary network scan results can identify deauthentication frames. Use purpose-built, authorized lab equipment and procedures if your assessment requires protocol-level validation.

## Repository layout

```text
.
├── docs/
│   ├── ETHICS.md
│   └── FEATURES.md
├── firmware/
│   ├── platformio.ini
│   └── src/main.cpp
├── notebooks/
│   ├── README.md
│   └── 01_scan_analysis.ipynb
├── scripts/collect_signal_data.py
├── requirements.txt
└── README.md
```

## Hardware

Required:
- ESP8266 board (NodeMCU / D1 mini class)
- USB cable

Optional GPS:
- NMEA-0183 GPS module
- Connect GPS TX to ESP8266 D6 (GPIO12), GPS ground to ESP8266 ground. GPS RX is not needed for receive-only logging.
- Ensure the module's logic level is safe for the ESP8266; its GPIOs are not 5 V tolerant.

The GPS receiver is read on a software serial input so USB serial remains available for logs. Configure pins in `firmware/src/main.cpp` if your board wiring differs. GPS geotagging is disabled when there is no valid fix.

## Build and run

### Firmware

Install PlatformIO, then:

```bash
cd firmware
pio run
pio run --target upload
pio device monitor --baud 115200
```

The monitor prints `SCAN` records in a pipe-delimited key/value format. Scanning is passive and periodically reports results. It does not intentionally connect to discovered networks.

### Collect serial data

Install Python dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

Find your serial port, then run:

```bash
python scripts/collect_signal_data.py --port /dev/ttyUSB0 --output data/scan.csv
```

On Windows, use a port such as `COM3`. Stop collection with `Ctrl+C`. The collector adds a local collection timestamp; GPS columns are populated only when the firmware reports a valid fix.

### Analyze

Launch Jupyter from the repository root:

```bash
jupyter lab
```

Open `notebooks/01_scan_analysis.ipynb` and set the input path to your capture. The notebook summarizes channels and signal strengths and highlights notable changes across scans. Treat every flagged pattern as a lead to investigate, not an attack attribution.

## Data format

The collected CSV has columns:

`timestamp,elapsed_ms,ssid,bssid,rssi_dbm,channel,security,latitude,longitude,altitude_m`

Keep captures out of version control. The supplied `.gitignore` excludes local data exports.

## Responsible use

- Obtain explicit permission before scanning or collecting data in any location.
- Do not use the project to interfere with other people's connectivity.
- Avoid publishing SSIDs, BSSIDs, or precise coordinates; redact or aggregate before sharing.
- Follow applicable laws, organizational policies, and site rules.
- See [docs/ETHICS.md](docs/ETHICS.md) and [docs/FEATURES.md](docs/FEATURES.md).

## Credits and scope

This project is inspired by the themes and learning goals of the four repositories listed above. It is an independent, safety-focused starter implementation, not a wholesale copy or merge of their source code. Attribution and licensing must be reviewed before incorporating code from any upstream project.

## License

MIT; see [LICENSE](LICENSE).
