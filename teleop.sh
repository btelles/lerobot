#!/usr/bin/env bash

. .venv/bin/activate

sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyACM1

python3 teleop.py