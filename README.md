# GPS LCD
This repository contains the code for interfacing a Raspberry Pi Model 3B (running Buster) with a 16x2 Character I2C LCD Display and a NEO 6M GPS Module.

## Materials
- 16x2 LCD Screen with I2C Converter: https://www.amazon.com/SunFounder-Serial-Module-Display-Arduino/dp/B019K5X53O
- NEO 6M GPS Module: https://www.amazon.com/gp/product/B01H5FNA4K/
- Raspberry Pi 3B: https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
- Jumper Cables: https://www.amazon.com/gp/product/B07GD2BWPY/
- MicroSD Card: https://www.amazon.com/SanDisk%C2%AE-microSDHCTM-8GB-Memory-Card/dp/B0012Y2LLE/
- USB to MicroUSB Cable: https://www.amazon.com/AmazonBasics-Male-Micro-Cable-Black/dp/B0711PVX6Z/

## References
The code and wiring diagrams contained in this repository is adapted from the following places:

**LCD Screen Driver and I2C Library:**
https://github.com/the-raspberry-pi-guy/lcd

**GPS Code**
https://github.com/amichael1227/gps_test/blob/rosBranch/gps_comm/scripts/gps_talker.py

**GPS Wiring & GPS Code**
https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/

## Wiring
For this section, please refer to the Raspberry Pi GPIO pinout diagram that is available in the Raspberry Pi Documentation found at https://www.raspberrypi.org/documentation/usage/gpio/.

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

### The Short Way
<ol>
<li>Make a <em>git</em> directory, and clone this repository into it.</li>
<ol>
<li><code>mkdir ~/git</code></li>
<li><code>cd ~/git</code>
<li><code>git clone https://github.com/amichael1227/gps-lcd.git</code></li> 
</ol>
</ol>

### The Long Way
<ol>
<li>Make sure the Pi is up to date.</li>
<ol>
<li><code>sudo apt-get update</code></li>
<li><code>sudo apt-get upgrade</code></li>
</ol>

<li>Edit the <em>/boot/config.txt</em> file to enable UART, the Serial Interface, and disable Bluetooth (thus making the GPIO pins the primary UART)</li>
<ol>
<li><code>sudo nano /boot/config.txt</code></li>
<li>Add the following segements as seperate lines at the bottom:</li>
	<code>dtparam=spi=on</code>
	<code>dtoverlay=pi3-disable-bt</code>
	<code>core_freq=250</code>
	<code>enable_uart=1</code>
	<code>force_turbo=1</code>
	<code>dtparam=i2c_arm=1</code>
<li>Save and exit by pressing <code>ctrl+x</code>, type <code>y</code>, and then press <code>enter</code>.</li>
</ol>

<li>Reboot the Pi</li>
<ol>
<li><code>sudo reboot</code></li>
</ol>

<li>Make a copy of the <em>/boot/cmdline.txt</em> file before it gets edited.</li>
<ol>
<li><code>sudo cp /boot/cmdline.txt /boot/cmdline_backup.txt</code></li>
</ol>

<li>Edit the <em>/boot/cmdline.txt</em> file.</li>
<ol>
<li>Open the file with <code>sudo nano /boot/cmdline.txt</code>.</li>
<li>Either delete or comment out the current contents, and then replace it with the text below</li>
<code>dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles</code>
<li>Save and exit by pressing <code>ctrl+x</code>, type <code>y</code>, and then press <code>enter</code>.</li>
</ol>

<li>Reboot the Pi.</li>
<ol>
<li><code>sudo reboot</code></li>
</ol>
<li>Run the <code>ls -l /dev</code> command. There will be two possible outputs, covered below. The photos used were taken from the <a href="https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/">Sparklers the Makers GitHub Blog</a>.</li>
<ol>
<p align="center">
  <img src="https://github.com/amichael1227/gps-lcd/blob/master/documentation-photos/I2C-Possible-Output-1.gif">
</p>
<li>If you get an output similar to the photo above, run the following two commands: <code>sudo systemctl stop serial-getty@ttyAMA0.service</code> <code>sudo systemctl disable serial-getty@ttyAMA0.service</code></li>
<p align="center">
  <img src="https://github.com/amichael1227/gps-lcd/blob/master/documentation-photos/I2C-Possible-Output-2.gif">
</p>
<li>If you get an output similar to the photo above, run the following two commands: <code>sudo systemctl stop serial-getty@ttyS0.service</code> <code>sudo systemctl disable serial-getty@ttyS0.service</code> </li>
</ol>
<li>Let's install the library we need to run the GPS program.</li>
<ol>
<li><code>sudo pip3 install pynmea2</code></li>
</ol>
<li>Make a <em>git</em> directory, and clone this repository into it.</li>
<ol>
<li><code>mkdir ~/git</code></li>
<li><code>cd ~/git</code>
<li><code>git clone https://github.com/amichael1227/gps-lcd.git</code></li> 
</ol>
<li>Move the LCD Display drivers into the Python folders.</li>
<ol>
<li><code>cd ~/</code></li>
<li><code>sudo cp ~/git/gps-lcd/lib-and-driver/* /usr/lib/python3.7</code></li>
</ol>
</ol>

## Run the Program
Now lets run the program to make sure it works!
1. `cd ~/git/gps-lcd/`
2. `sudo python3 gps_lcd.py`

Huzzah! You should get outputs like the ones below:

<p align="center">
  <img src="https://github.com/amichael1227/gps-lcd/blob/master/documentation-photos/Code-Output.gif">
</p>

<p align="center">
  <img src="https://github.com/amichael1227/gps-lcd/blob/master/documentation-photos/LCD-Output.gif">
</p>

## Coming Soon to a GitHub Near you
This respository will eventually have code to save the Latitude, Longitude, and a Timestamp to a .csv file and then map it using the folium library. The plan is to have all of this happening continously, so the .csv file and the .html file that folium spits out with a map will be constantly overwritten, which slows down the Python script. This does have a benefit though as it can reduce the excessive amount of datapoints that are generated (for example, without any kind of slow down, this setup will output 2345 datapoints for a 35 minute drive, or about 67 a minute, which for my purposes is excessive. That being said, ***it is all currently a very large work in progress***, but will be updated in the near future.
