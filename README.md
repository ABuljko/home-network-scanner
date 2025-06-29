# Home Network Scanner

A Python tool to scan your local network for connected devices, log results, and optionally send email alerts when new devices are detected.

## Features

- Scans a specified network range for active devices using their IP and MAC addresses.
- Logs scan results in both JSON and CSV formats in the `logs/` directory.
- Detects new devices compared to previous scans.
- Optional email notifications for new device detection.

## Requirements

- Python 3.7+
- [nmap](https://nmap.org/) installed on your system
- Python packages: `python-nmap`, `colorama`

Install dependencies with:

```sh
pip install python-nmap colorama
```

## Usage

1. **Configure**  
   Edit [`config.json`](config.json) to set your network range and email settings.

2. **Run the scanner**  
   ```sh
   python scanner.py
   ```

3. **View logs**  
   Results are saved in the `logs/` folder as both `.json` and `.csv` files.

## Email Alerts

To enable email alerts, set `"email_alerts": true` in [`config.json`](config.json) and provide valid SMTP/email credentials.

## Files

- [`scanner.py`](scanner.py): Main script to scan the network and detect new devices.
- [`utils.py`](utils.py): Utility functions for logging, saving results, and sending emails.
- [`config.json`](config.json): Configuration file for network range and email settings.
- `logs/`: Directory where scan results are stored.

## Example Output

```
🔍 Scanning network...
📦 Total devices found: 5
✅ No new devices detected.
📁 Results saved: logs/20240610_153000.json, logs/20240610_153000.csv
```

## License

MIT