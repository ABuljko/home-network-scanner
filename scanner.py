import nmap
import json
import os
from datetime import datetime
from utils import send_email, save_csv, load_previous_devices

with open("config.json") as f:
    config = json.load(f)

nm = nmap.PortScanner()

def scan_network():
    print("[*] Scanning network...")
    result = nm.scan(hosts=config["network_range"], arguments='-sn')
    devices = []
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            devices.append({
                'ip': nm[host]['addresses'].get('ipv4', ''),
                'mac': nm[host]['addresses'].get('mac', ''),
                'time': datetime.now().isoformat()
            })
    return devices

def compare_devices(current, previous):
    previous_macs = {d['mac'] for d in previous}
    return [d for d in current if d['mac'] not in previous_macs]

def save_results(devices):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    json_path = os.path.join("logs", f"{timestamp}.json")
    csv_path = os.path.join("logs", f"{timestamp}.csv")
    with open(json_path, "w") as f:
        json.dump(devices, f, indent=2)
    save_csv(devices, csv_path)

if __name__ == "__main__":
    devices = scan_network()
    print(f"[+] Found {len(devices)} devices.")
    previous_devices = load_previous_devices()
    new_devices = compare_devices(devices, previous_devices)

    if new_devices:
        print(f"[!] {len(new_devices)} new device(s) detected:")
        for d in new_devices:
            print(f" - {d['ip']} ({d['mac']})")
        if config.get("email_alerts"):
            body = "\n".join([f"{d['ip']} ({d['mac']})" for d in new_devices])
            send_email("New Devices Detected", body, config)
    else:
        print("[✓] No new devices.")

    save_results(devices)
