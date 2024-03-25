#!/usr/bin/env bash
set -e
source "/home/pi/birthday-poc/.venv/bin/activate"

cd "/home/pi/birthday-poc"

echo "Run..."
python3 /home/pi/birthday-poc/birthday.py >> /home/pi/birthday-poc/log.log 2>&1 

deactivate
