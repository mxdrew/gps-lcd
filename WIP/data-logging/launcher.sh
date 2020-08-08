#!/bin/sh
# launcher.sh

sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service


cd /
cd /home/pi/gps_lcd_program/
sudo python3 gps_lcd_startup.py
cd /
