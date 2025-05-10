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
