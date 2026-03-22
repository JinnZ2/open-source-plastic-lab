"""
Sensor Logger — Read and log Arduino sensor data over serial.

Connects to the master water treatment controller and logs turbidity,
pH, conductivity, temperature, and flow rate to CSV.

Usage:
    python -m models.measure.sensor_logger --port /dev/ttyUSB0
    python -m models.measure.sensor_logger --port COM3 --interval 5
"""

import argparse
import csv
import struct
import sys
import time
from datetime import datetime
from pathlib import Path

# WaterData struct layout (matches master_water_controller.ino)
# float turbidity, ph, conductivity, temperature, flowRate
# int treatmentStage
# float microplasticsRecovered, powerGenerated
WATER_DATA_FORMAT = "<fffffiff"
WATER_DATA_SIZE = struct.calcsize(WATER_DATA_FORMAT)
FIELD_NAMES = [
    "turbidity", "ph", "conductivity", "temperature",
    "flow_rate_mL_min", "treatment_stage",
    "microplastics_recovered_g", "power_generated_mWh",
]
STAGE_NAMES = {
    0: "Filling",
    1: "Electrocoagulation",
    2: "Settling",
    3: "Magnetic Separation",
    4: "Bio-electrochemical",
    5: "Advanced Oxidation",
    6: "Discharge",
}


def parse_water_data(raw_bytes):
    """Unpack raw I2C bytes into a dict matching the Arduino WaterData struct."""
    values = struct.unpack(WATER_DATA_FORMAT, raw_bytes)
    return dict(zip(FIELD_NAMES, values))


def log_to_csv(filepath, data_row):
    """Append a single data row to a CSV file, creating headers if needed."""
    file_exists = filepath.exists()
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp"] + FIELD_NAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_row)


def print_reading(data):
    """Pretty-print a single sensor reading to the console."""
    stage = STAGE_NAMES.get(data["treatment_stage"], "Unknown")
    print(
        f"  Turbidity: {data['turbidity']:.0f}"
        f"  | pH: {data['ph']:.2f}"
        f"  | Cond: {data['conductivity']:.0f}"
        f"  | Temp: {data['temperature']:.1f}C"
        f"  | Flow: {data['flow_rate_mL_min']:.1f} mL/min"
        f"  | Stage: {stage}"
    )


def run(port, baud=9600, interval=1, output_dir="logs"):
    """Main logging loop — reads serial and writes CSV."""
    try:
        import serial
    except ImportError:
        print("Install pyserial:  pip install pyserial")
        sys.exit(1)

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    log_file = output_path / f"sensor_log_{datetime.now():%Y%m%d_%H%M%S}.csv"

    print(f"Connecting to {port} at {baud} baud...")
    ser = serial.Serial(port, baud, timeout=2)
    print(f"Logging to {log_file}  (Ctrl+C to stop)\n")

    try:
        while True:
            raw = ser.read(WATER_DATA_SIZE)
            if len(raw) == WATER_DATA_SIZE:
                data = parse_water_data(raw)
                data["timestamp"] = datetime.now().isoformat()
                print_reading(data)
                log_to_csv(log_file, data)
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\nStopped. Log saved to {log_file}")
    finally:
        ser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Arduino water treatment sensors to CSV")
    parser.add_argument("--port", required=True, help="Serial port (e.g. /dev/ttyUSB0 or COM3)")
    parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")
    parser.add_argument("--interval", type=float, default=1, help="Seconds between reads (default: 1)")
    parser.add_argument("--output-dir", default="logs", help="Output directory for CSV files")
    args = parser.parse_args()
    run(args.port, args.baud, args.interval, args.output_dir)
