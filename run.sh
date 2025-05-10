#!/usr/bin/env bash

python3 -m venv env
source "$(dirname "$0")/env/bin/activate"
pip install -r requirements.txt
# -e: stop if any commands fail
# -u: stop if a variable wasn't set
# -o pipefail: if a part of the pipeline fails, the whole pipeline fails
set -euo pipefail

# Build Docker image
docker build -t ardupilot-sim .

# Stop and remove any existing container
# docker rm -f ardupilot-sim-instance 2>/dev/null || true

# Run the container
docker run -d --name ardupilot-sim-instance -p 5760:5760 ardupilot-sim

echo "Waiting for simulator to start..."
sleep 10  # wait for MAVLink connection to be ready

# Pass any args (like "get SYSID_THISMAV" or "set ARMING_CHECK 0") to the Python CLI
python3 mavctl.py 
# "$@"

# Optional: stop and clean up container after use
# docker stop ardupilot-sim-instance
# docker rm ardupilot-sim-instance
