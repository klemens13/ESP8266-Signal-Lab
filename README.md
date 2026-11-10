# ESP8266 Signal Lab

ESP8266 Signal Lab is a learning-focused toolkit for authorized WiFi monitoring, consent-based wardriving, signal detection, and notebook-driven wireless analysis. It is designed for ethical security research, network visibility, and educational experimentation on networks you own or are explicitly authorized to assess.

## Mission

This project helps researchers and hobbyists:
- passively scan nearby WiFi networks
- capture signal and channel metadata
- detect suspicious or unusual wireless activity patterns
- export data for notebook-based visualization and analysis
- learn how WiFi telemetry can be monitored and interpreted responsibly

## Ethical use

This toolkit must be used only in environments where you have explicit authorization to scan, monitor, or test. Do not use it against private, public, or third-party networks without permission.

See `docs/ETHICS.md` for our usage policy and safety guidance.

## Features

- ESP8266-based WiFi scanning and telemetry collection
- Passive discovery of access points and nearby networks
- Signal strength, channel, and local environment sampling
- Export-ready scan data for CSV/JSON processing
- A simple analysis flow for Jupyter notebooks
- Ethical-first project structure for learning and research

## Repository layout

```text
ESP8266-Signal-Lab/
├── README.md
├── .gitignore
├── docs/
│   └── ETHICS.md
├── firmware/
│   ├── platformio.ini
│   └── src/
│       └── main.cpp
├── scripts/
│   └── collect_signal_data.py
├── notebooks/
│   └── README.md
└── LICENSE
```

## Quick start

### 1) Firmware

Install PlatformIO and build the firmware:

```bash
cd firmware
pio run
```

Upload to an ESP8266 board:

```bash
pio run --target upload
```

### 2) Run scanning

The firmware scans nearby WiFi networks and prints:
- SSID
- RSSI
- channel
- BSSID
- security mode

### 3) Export and analyze data

Use the helper script to collect serial output into a CSV or JSON file:

```bash
python3 scripts/collect_signal_data.py --port /dev/ttyUSB0 --output data/scan.csv
```

Then open the notebook templates in `notebooks/` for analysis and visualization.

## Example hardware

- ESP8266 NodeMCU or similar compatible board
- USB cable for programming
- Optional external power supply for portable field use

## Safety

- Never operate this project on unauthorized networks
- Use only on devices you own or clearly manage
- Obtain approval before testing in any environment
- Prefer passive monitoring over active disruption

## Project status

This repository is a starter project focused on responsible WiFi telemetry and analysis. It is intended as a research and learning toolkit rather than a general-purpose attack platform.

## License

This project is licensed under the MIT License.
