import os
import json
import csv
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from colorama import Fore, Style

def colored(msg, color=Fore.GREEN):
    return f"{color}{msg}{Style.RESET_ALL}"

def ensure_logs_folder():
    os.makedirs("logs", exist_ok=True)

def save_results(devices, base_name):
    json_path = os.path.join("logs", f"{base_name}.json")
    csv_path = os.path.join("logs", f"{base_name}.csv")
    with open(json_path, "w") as f:
        json.dump(devices, f, indent=2)
    save_csv(devices, csv_path)
    print(colored(f"📁 Results saved: {json_path}, {csv_path}", Fore.CYAN))

def save_csv(devices, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["ip", "mac", "time"])
        writer.writeheader()
        writer.writerows(devices)

def load_previous_devices():
    try:
        files = sorted(os.listdir("logs"), reverse=True)
        for f in files:
            if f.endswith(".json"):
                with open(os.path.join("logs", f), "r") as file:
                    return json.load(file)
    except Exception as e:
        print(colored(f"[!] Error loading previous devices: {e}", Fore.RED))
    return []

def send_email(subject, body, config):
    try:
        settings = config["email_settings"]
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = settings["sender"]
        msg["To"] = settings["receiver"]

        with smtplib.SMTP(settings["smtp_server"], settings["smtp_port"]) as server:
            server.starttls()
            server.login(settings["sender"], settings["password"])
            server.send_message(msg)
        print(colored("📧 Email notification sent.", Fore.MAGENTA))
    except Exception as e:
        print(colored(f"[!] Failed to send email: {e}", Fore.RED))
