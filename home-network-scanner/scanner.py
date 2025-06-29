import json
from colorama import Fore
import nmap
from datetime import datetime
from utils import (
    colored, ensure_logs_folder, load_previous_devices,
    save_results, send_email
)

# Load config
with open("config.json") as f:
    config = json.load(f)

nm = nmap.PortScanner()

def scan_network():
    print(colored("🔍 Scanning network...", Fore.YELLOW))
    result = nm.scan(hosts=config["network_range"], arguments='-sn')
    devices = []
    now = datetime.now().isoformat()
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            devices.append({
                'ip': nm[host]['addresses'].get('ipv4', ''),
                'mac': nm[host]['addresses'].get('mac', ''),
                'time': now
            })
    return devices

def detect_new_devices(current, previous):
    prev_set = {(d['ip'], d['mac']) for d in previous}
    return [d for d in current if (d['ip'], d['mac']) not in prev_set]

if __name__ == "__main__":
    ensure_logs_folder()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    current_devices = scan_network()
    print(colored(f"📦 Total devices found: {len(current_devices)}", Fore.GREEN))

    previous_devices = load_previous_devices()
    new_devices = detect_new_devices(current_devices, previous_devices)

    if new_devices:
        print(colored(f"🆕 New device(s) detected:", Fore.RED))
        for d in new_devices:
            print(colored(f" - {d['ip']} ({d['mac']})", Fore.RED))

        if config.get("email_alerts"):
            lines = [f"{d['ip']} ({d['mac']})" for d in new_devices]
            send_email("⚠️ New Devices Detected on Your Network", "\n".join(lines), config)
    else:
        print(colored("✅ No new devices detected.", Fore.GREEN))

    save_results(current_devices, base_name=timestamp)
