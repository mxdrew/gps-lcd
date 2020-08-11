# Tells you what's happening
echo "Now setting up your Pi!"

# Updates Raspbian!
sudo apt-get update && sudo apt-get -y upgrade

# Navigates to home directory
cd /

# Navigates to boot directory
cd /boot/

# Makes a backups folder in the boot directory
sudo mkdir backups

# Makes a backup copy of the files
sudo cp /boot/config.txt /boot/backups/config.txt
sudo cp /boot/cmdline.txt /boot/backups/cmdline.txt

# Replaces the original copy of the files with ours
sudo cp -f /home/pi/git/gps-lcd/important_files/config.txt /boot/
sudo cp -f /home/pi/git/gps-lcd/important_files/cmdline.txt /boot/

# Navigates to home directory
cd /

# Comment the lines below out if pynmea2 doesn't work
#sudo apt-get remove -y python2.7
#sudo apt-get -y autoremove

# Installs the things we need
sudo pip3 install pynmea2 folium
sudo apt-get install -y python3-pandas

# Moves the drivers and library for the I2C Display
sudo cp /home/pi/git/gps-lcd/important_files/lib-and-driver/* /usr/lib/python3.7

# Tells you when it is all over
echo "Your Pi is now set up!"
