#KRAKENSPLOIT
<div style="text-align: center;">
    <img src="https://github.com/10T4/krakensploit/blob/main/addons/krak%26logo.png" width="600" height="600">
</div>

---

## Introduction

KrakenSploit is a versatile tool designed to simplify and streamline penetration testing by combining several popular security tools into a single, user-friendly interface. Whether you're a professional pentester or a security enthusiast, this tool provides a comprehensive range of features to scan, discover, and exploit vulnerabilities in your networks and web applications.

---

## Key Features

- **Nmap Integration**: Full network scan to discover active hosts, open ports, running services and vulnerability.
- **Dirb Integration**: Web site analysis to discover hidden directories and files.
- **Other Tools**: Easy integration of other popular security tools.
- **Intuitive User Interface**: User-friendly and easy-to-use interface, ideal for beginners and experts alike.
- **CLI and GUI Modes**: Supports both Command Line Interface (CLI) and Graphical User Interface (GUI) modes.
---

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/10T4/krakensploit.git
```

2. Navigate to the project directory:

```bash
cd krakensploit
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Command Line Interface (CLI)

To run the tool in CLI mode:

```bash
python3 cli.py -h
```

### Graphical User Interface (GUI)

To run the tool in GUI mode:

```bash
sudo python3 gui.py
```

---

## Examples

### Example 1: Network Scan with Nmap

```bash
python3 cli.py nmap --ip_address="IP" scan_vuln
```

### Example 2: Network Scan on GUI


<img src="https://github.com/10T4/krakensploit/blob/main/addons/krakensploit.png">

