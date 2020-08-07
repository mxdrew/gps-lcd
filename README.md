
# GPS LCD
This repository contains the code for interfacing a Raspberry Pi Model 3B (running Buster) with a 16x2 Character I2C LCD Display and a NEO 6M GPS Module.

## Materials
16x2 LCD Screen with I2C Converter: https://www.amazon.com/SunFounder-Serial-Module-Display-Arduino/dp/B019K5X53O
NEO 6M GPS Module: https://www.amazon.com/gp/product/B01H5FNA4K/
Raspberry Pi 3B: https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
Jumper Cables: https://www.amazon.com/gp/product/B07GD2BWPY/
MicroSD Card: https://www.amazon.com/SanDisk%C2%AE-microSDHCTM-8GB-Memory-Card/dp/B0012Y2LLE/
USB to MicroUSB Cable: https://www.amazon.com/AmazonBasics-Male-Micro-Cable-Black/dp/B0711PVX6Z/

## References
The code and wiring diagrams contained in this repository is adapted from the following places:

**LCD screen driver and I2C library:**
https://github.com/the-raspberry-pi-guy/lcd

**GPS Code**
https://github.com/amichael1227/gps_test/blob/rosBranch/gps_comm/scripts/gps_talker.py

**GPS Wiring & GPS Code**
https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/

## Wiring
**NEO 6M**
| NEO 6M Pin | Raspberry Pi Pin |
|:----------:|:----------------:|
|     VCC    |        5V        |
|     GND    |        GND       |
|     TX     |   RX (GPIO 15)   |

**16x2 I2C LCD**
| LCD Screen Pin | Raspberry Pi Pin |
|:--------------:|:----------------:|
|       VCC      |        5V        |
|       GND      |        GND       |
|       SDA      |   SDA (GPIO 2)   |
|       SCL      |   SCL (GPIO 3)   |

*Note*: There is an option to backlight the screen, to do so, connect the 5V pin of the Pi to the pin directly across from the GND pin for the I2C plugin. Please see the photo below for reference.

<p align="center">
  <img src="https://github.com/amichael1227/gps-lcd/blob/master/documentation-photos/I2C-LCD-Backlight-Wiring.gif">
</p>

## Software Setup
Follow the steps below to set up the Raspberry Pi for this project. Commands you need to perform and code you need to enter are written `like this`.

1. Make sure the Pi is up to date.
  a. `sudo apt-get update`
  b. `sudo apt-get upgrade`
  
2. Edit the */boot/config.txt* file to enable UART, the Serial Interface, and disable Bluetooth (thus making the GPIO pins the primary UART)
  a. `sudo nano /boot/config.txt`
  b. Add the following lines at the bottom:
  `dtparam=spi=on`
  `dtoverlay=pi3-disable-bt`
  `core_freq=250`
  `enable_uart=1`
  `force_turbo=1`
  `dtparam=i2c_arm=1`
  c. Save and exit by pressing `ctrl+x`, type `y`, and then press `enter`.
3. Make a copy of the */boot/cmdline.txt* file before it gets edited.
  a. `sudo cp /boot/cmdline.txt /boot/cmdline_backup.txt`
4. Edit the */boot/cmdline.txt* file.
  a. Open the file with `sudo nano /boot/cmdline.txt`. 
  b. Either delete or comment out the current contents, and then replace it with the text in step 4.c.
  c. `dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles`
  d. Save and exit by pressing `ctrl+x`, type `y`, and then press `enter`.
5. Reboot the Pi.
  a. `sudo reboot`
6. Run the `ls -l /dev` command. There will be two possible outputs, covered below. The photos used were taken from the [Sparklers the Makers GitHub Blog](https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/).
![Output 1](https://github.com/amichael1227/gps-lcd/blob/master/documentation-photos/I2C-Possible-Output-1.gif)
	a. If you get an output similar to the photo below, run the following two commands: `sudo systemctl stop serial-getty@ttyAMA0.service` `sudo systemctl disable serial-getty@ttyAMA0.service`  
  
	![Output 2](https://github.com/amichael1227/gps-lcd/blob/master/documentation-photos/I2C-Possible-Output-2.gif)
	b. If you get an output similar to the photo below, run the following two commands: `sudo systemctl stop serial-getty@ttyS0.service` `sudo systemctl disable serial-getty@ttyS0.service` 


8. Let's install the libraries and drivers that we need.
  a. `sudo pip3 install pynmea2`
  b. Make a *git* folder to clone this repository to by entering `mkdir ~/git`
  c. Clone this repository: `git clone https://github.com/amichael1227/gps-lcd.git`
9. Move the LCD Display drivers into the Python folders.
  a. `cd ~/`
  b. `sudo cp ~/git/gps-lcd/lib-and-driver/* /usr/lib/python3.7`
  
## Run the Program
Now lets run the program to make sure it works!
1. `cd ~/git/gps-lcd/`
2. `sudo python3 gps_lcd.py'

Huzzah! You should get outputs like the ones below:

<p align="center">
  <img src="https://github.com/amichael1227/gps-lcd/blob/master/documentation-photos/Code-Output.gif">
</p>

<p align="center">
  <img src="https://github.com/amichael1227/gps-lcd/blob/master/documentation-photos/LCD-Output.gif">
</p>
