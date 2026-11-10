#!/usr/bin/env python3
"""Collect passive ESP8266 Signal Lab serial records into a local CSV file."""

import argparse
import csv
import datetime as dt
import re
import sys
import time
from pathlib import Path

import serial

FIELDS = [
    "timestamp", "elapsed_ms", "ssid", "bssid", "rssi_dbm", "channel",
    "security", "latitude", "longitude", "altitude_m",
]
RECORD_RE = re.compile(r'([A-Z_]+)=("(?:[^"]|"")*"|[^|]*)')


def parse_record(line):
    if not line.startswith("SCAN | "):
        return None
    values = {}
    for key, raw in RECORD_RE.findall(line):
        value = raw.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('""', '"')
        values[key] = value
    return {
        "timestamp": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "elapsed_ms": values.get("ELAPSED_MS", ""),
        "ssid": values.get("SSID", ""),
        "bssid": values.get("BSSID", ""),
        "rssi_dbm": values.get("RSSI_DBM", ""),
        "channel": values.get("CHANNEL", ""),
        "security": values.get("SECURITY", ""),
        "latitude": values.get("LATITUDE", ""),
        "longitude": values.get("LONGITUDE", ""),
        "altitude_m": values.get("ALTITUDE_M", ""),
    }


def collect(port, output_path, baud):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not output.exists() or output.stat().st_size == 0
    with serial.Serial(port, baudrate=baud, timeout=1) as device, output.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if needs_header:
            writer.writeheader()
        print(f"Collecting from {port} to {output}; press Ctrl+C to stop.")
        while True:
            line = device.readline().decode("utf-8", errors="replace").strip()
            row = parse_record(line)
            if row:
                writer.writerow(row)
                file.flush()
                print(f"{row['timestamp']} {row['bssid']} {row['rssi_dbm']} dBm")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, help="Serial port (for example COM3 or /dev/ttyUSB0)")
    parser.add_argument("--output", default="data/scan.csv", help="CSV output path")
    parser.add_argument("--baud", type=int, default=115200)
    args = parser.parse_args()
    try:
        collect(args.port, args.output, args.baud)
    except KeyboardInterrupt:
        print("\nStopped.")
    except serial.SerialException as exc:
        sys.exit(f"Serial error: {exc}")


if __name__ == "__main__":
    main()
