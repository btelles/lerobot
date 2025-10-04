#!/usr/bin/env bash

. .venv/bin/activate

sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyACM1

python -m lerobot.teleoperate \
    --robot.type=koch_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=white \
    --teleop.type=koch_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=red \
    --display_data=true
    #--robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 1920, height: 1080, fps: 30}}" \