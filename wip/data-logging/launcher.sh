#!/bin/sh
# launcher.sh

sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service


cd /
cd /home/pi/git/gps-lcd/wip/data-logging
sudo python3 gps_logger.py
cd /
