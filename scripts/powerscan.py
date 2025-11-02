import argparse
import contextlib
import multiprocessing
import os
import re
import sys
import time
import getpass
import logging
from datetime import datetime
from netmiko import ConnectHandler
from netmiko import exceptions as netmiko_exceptions
import csv


# ---------------- Logger Setup ----------------
def create_console_logger(script_name, log_dir):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{script_name}.log")

    logger = logging.getLogger(script_name)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)
    logger.setLevel(logging.INFO)
    return logger


# ---------------- Global Vars ----------------
_script_name_ = os.path.basename(sys.argv[0])

# Base directories (use raw strings or os.path.join)
base_results_dir = r"D:\PythonScripts\results"
log_dir = os.path.join(base_results_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

logger = create_console_logger(_script_name_, log_dir)

cpu = multiprocessing.cpu_count() * 2

results_dir = os.path.join(
    base_results_dir,
    _script_name_,
    datetime.now().strftime("%Y%m%d_%H%M%S")
)
os.makedirs(results_dir, exist_ok=True)

csv_header = "timestamp,device,Details\n"
devices = ["192.168.91.116", "192.168.91.115"]  # Placeholder for device list


# ---------------- Main Audit Function ----------------
def cisco_8800_FAN_power_audit(device):
    """
    Connects to a Cisco 8800 device and audits FAN power status.
    Returns a list of tuples: (device_info, detail, status)
    """
    audit_results = []
    try:
        handler = ConnectHandler(
            device_type="cisco_ios",
            host=device,
            username="admin",
            password="Eveng138343",
            timeout=10
        )
        fan_output = handler.send_command("show environment power")

    except Exception as e:
        logger.error(f"Error connecting to {device}: {e}")
        return [(device, "connection_failed", "error")]

    try:
        pattern = r'\s*(0/FT\d+)\s+\S+\d+\d+\s+\d+\s+ON\b'

        if isinstance(fan_output, str):
            fan_output_lines = fan_output.splitlines()
            fan_details_from_device = re.findall(pattern, fan_output, re.MULTILINE)
            
            logger.info(f"Fan details from device {device}: {fan_details_from_device}")

            fan_expected_ports = ["0/FT0", "0/FT1", "0/FT2", "0/FT3"]

            missing_fans = set(fan_expected_ports) - set(fan_details_from_device)

            if missing_fans:
                for missing_fan in missing_fans:
                    logger.info(f"Missing fan at port {missing_fan} on device {device}")
                audit_results.append((device, list(missing_fans), "missing"))
            else:
                logger.info(f"All fans are present on device {device}")
                audit_results.append((device, "All fans present", "good"))
        
        handler.disconnect()

    except Exception as e:
        logger.error(f"Error parsing fan output for {device}: {e}")
        audit_results.append((device, "Error parsing fan output", "error"))
    
    return audit_results


# ==========================================================
# Function: parse_results
# ==========================================================
def parse_results(results):
    """
    Takes a list of tuples (device, detail, status) and saves them into CSV files.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    user = os.getenv("USERNAME", "network_audit")
    base_dir = r"D:\PythonScripts\results"

    results_dir = os.path.join(
        base_dir,
        _script_name_,
        datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    os.makedirs(results_dir, exist_ok=True)

    good, missing, failed = [], [], []

    for result in results:
        # result = (device_host, detail, status)
        if "error" in result:
            failed.append(result)
        elif result[2] == "missing":
            missing.append(result)
        elif result[2] == "good":
            good.append(result)
        else:
            failed.append(result)

    # Helper to write to CSV
    def write_csv(filename, data):
        filepath = os.path.join(results_dir, filename)
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "Device", "Detail", "Status"])
            for row in data:
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), *row])
        return filepath

    # Write each category
    files = {
        "good": write_csv("fan_audit_good.csv", good),
        "missing": write_csv("fan_audit_missing.csv", missing),
        "failed": write_csv("fan_audit_failed.csv", failed)
    }

    print("\n✅ Audit completed. Results saved in:")
    for status, path in files.items():
        print(f"  - {status.title()} results: {path}")

    return files


# ==========================================================
# Function: main
# ==========================================================
def main():
    start = datetime.now()
    logger.info(f"Starting Power Scan Audit on {len(devices)} devices at {start.strftime('%Y-%m-%d %H:%M:%S')}")

    # Run audits in parallel
    with contextlib.closing(multiprocessing.Pool(processes=cpu)) as pool:
        results = pool.map(cisco_8800_FAN_power_audit, devices)
    
    # Flatten list of lists
    results = [item for result in results for item in result]

    # Parse and save final results
    parse_results(results)
    end = datetime.now()

    logger.info(f"Completed Power Scan Audit in {str(end - start)}")
    logger.info(f"Power Scan Audit completed at {end.strftime('%Y-%m-%d %H:%M:%S')}")


# ==========================================================
# Entry Point
# ==========================================================
if __name__ == "__main__":
    main()
