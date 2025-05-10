# 🛩️ ArduPilot CLI Controller

This project is a command-line interface (CLI) tool built in Python to interact with a containerized [ArduPilot](https://ardupilot.org/) drone simulator via the [MAVLink](https://mavlink.io/en/) protocol using [`pymavlink`](https://github.com/ArduPilot/pymavlink).

It allows users to read and modify live parameters from the drone simulator in real-time — a powerful tool for customizing and validating autonomous drone behavior.

---

## 🚀 Features

- 🐳 Dockerized ArduPilot SITL (Software In The Loop) environment  
- 🔌 MAVLink communication via `pymavlink`  
- 🛠️ CLI interface to:
  - Read parameter values (`get <PARAM>`)
  - Modify parameter values (`set <PARAM> <VALUE>`)
- 🔁 Smart runtime logic:
  - Automatically builds and runs Docker container if needed
  - Skips re-building if already available
- 🧪 Fully self-contained and testable via `run.sh`

---

## 🧰 Prerequisites

- Docker  
- Python 3.8+  
- Linux/macOS shell (or WSL on Windows)

---

## 🧱 Setup

```bash
# Create and activate a virtual environment
python3 -m venv env
source env/bin/activate

# Install required Python packages
pip install -r requirements.txt
```

## ▶️ Usage

Run the controller interactively:

```bash
./run.sh
```

Then enter commands:

```text
get SYSID_THISMAV
set ARMING_CHECK 0
exit
```

Or run one-off commands:

```bash
./run.sh get SYSID_THISMAV
./run.sh set ARMING_CHECK 0
```

## 📂 Project Structure

```
.
├── Dockerfile           # ArduPilot SITL simulator setup
├── mavctl.py            # Python CLI tool
├── run.sh               # Launcher script
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## 📌 Example Parameters

* `SYSID_THISMAV`: System ID of the drone
* `ARMING_CHECK`: Enable/disable pre-arm safety checks
* `FS_THR_ENABLE`: Throttle failsafe mode

Full parameter list: https://ardupilot.org/copter/docs/parameters.html

## 🧠 Design Decisions

* **Separation of Concerns**: The simulator runs in a Docker container; the CLI runs on the host.
* **Error Handling**: Graceful failure messages and parameter validation.
* **Extendability**: Easily extendable to support more MAVLink operations.
