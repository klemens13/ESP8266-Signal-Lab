#!/usr/bin/env python3
"""Simple helper for collecting serial output from the ESP8266 scanner.

Usage:
    python3 scripts/collect_signal_data.py --port /dev/ttyUSB0 --output data/scan.csv
"""

import argparse
import csv
import serial
import time
from pathlib import Path


def parse_line(line: str):
    """Convert lines like:
    SSID=MyNetwork | RSSI=-62 dBm | CH=6 | BSSID=AA:BB:CC:DD:EE:FF | SEC=Encrypted
    into a dict for CSV output.
    """
    parts = {}
    for segment in line.split("|"):
        key_value = segment.strip().split("=", 1)
        if len(key_value) == 2:
            key, value = key_value
            parts[key.strip()] = value.strip()
    return parts


def collect(port: str, output_path: str, baud: int = 115200, timeout: float = 2.0):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with serial.Serial(port, baud, timeout=timeout) as ser:
        time.sleep(2)
        with output.open("w", newline="") as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=["SSID", "RSSI", "CH", "BSSID", "SEC"],
            )
            writer.writeheader()

            while True:
                line = ser.readline()
                if not line:
                    continue

                decoded = line.decode("utf-8", errors="ignore").strip()
                if not decoded or "Scanning nearby WiFi networks" in decoded:
                    continue
                if decoded.startswith("Found") or decoded.startswith("---"):
                    continue
                if "SSID=" not in decoded:
                    continue

                row = parse_line(decoded)
                if row:
                    writer.writerow(row)
                    print(decoded)


def main():
    parser = argparse.ArgumentParser(description="Collect serial WiFi scan data from ESP8266 Signal Lab.")
    parser.add_argument("--port", required=True, help="Serial port, e.g. /dev/ttyUSB0 or COM3")
    parser.add_argument("--output", default="data/scan.csv", help="Output CSV path")
    parser.add_argument("--baud", type=int, default=115200, help="Serial baud rate")
    args = parser.parse_args()

    try:
        collect(args.port, args.output, args.baud)
    except KeyboardInterrupt:
        print("\nCollection stopped by user.")
    except Exception as exc:
        raise SystemExit(f"Error: {exc}")


if __name__ == "__main__":
    main()
