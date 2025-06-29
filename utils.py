import smtplib
import csv
import os
from email.mime.text import MIMEText

def send_email(subject, body, config):
    settings = config["email_settings"]
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings["sender"]
    msg["To"] = settings["receiver"]

    with smtplib.SMTP(settings["smtp_server"], settings["smtp_port"]) as server:
        server.starttls()
        server.login(settings["sender"], settings["password"])
        server.send_message(msg)

def save_csv(devices, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["ip", "mac", "time"])
        writer.writeheader()
        for device in devices:
            writer.writerow(device)

def load_previous_devices():
    try:
        files = sorted(os.listdir("logs"), reverse=True)
        for f in files:
            if f.endswith(".json"):
                with open(os.path.join("logs", f), "r") as file:
                    import json
                    return json.load(file)
    except:
        pass
    return []
