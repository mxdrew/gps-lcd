#!/usr/bin/env python3
# Imports all the libraries we use for the GPS
import serial
import pynmea2

# Imports the driver/library for the LCD Screen
import lcddriver
import time

# Imports the things we need to log the Latitude and Longitude
import csv
import datetime

# Load the driver and set it to "display"
display = lcddriver.lcd()
display.lcd_clear()

# Initialize the serial object for the GPS Module
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=5.0) #initialize serial object


# Display this to delay sensor reading until the Pi fully boots
# and for fix to theoretically be acquired.
# Was getting an error when running this script at boot
# without this section.
display.lcd_display_string("  Booting up!", 1)
display.lcd_display_string("       3", 2)
time.sleep(1)
display.lcd_display_string("       2", 2)
time.sleep(1)
display.lcd_display_string("       1",2)
time.sleep(1)
display.lcd_display_string("  Now Logging",1)
display.lcd_display_string("  Lat & Long",2)
time.sleep(2)
display.lcd_clear()


# Create the CSV file we will be using to log to.
# Please note that this will be added every time
# that the program is run, so keep that in mind.
csvfile = "raw_gps_data.csv"
with open(csvfile, "a") as fp:
    wr = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wr.writerow(["Latitude", "Longitude", "Timestamp"])


# Try loop that allows for a graceful exit if needed
try:
    while True:
        try:
            # Gets the data from the sensor and writes it in a
            # format that the rest of the code can read.
            encoded_line = ser.readline() #read nmea sentence
            line = encoded_line.decode('utf-8')
            msg = pynmea2.parse(line)
           # print(repr(msg)) # Uncomment this line to debug, prints out full message

            if line.find('GGA') > 0: # Search for the specific GPS message we want

                # Gets the timestamp of when the fix is acquired and
                # prints out Latitude, Longitude, and stamp when a fix is acquired
                timestamp = "  {}".format(datetime.datetime.now()) # The spaces help make Excel not do math when this is opened, plus make the teminal prinouts look nice
                print("-----------------------------")
                print(" Fix Acquired:")
                print("  Lat:",round(msg.latitude,6), msg.lat_dir)
                print("  Long:",abs(round(msg.longitude,6)), msg.lon_dir)
                print(timestamp)

                # Code for printing out on the LCD
                lat_str = "  {} {}".format(round(msg.latitude,6),msg.lat_dir) # Sets Latitude variable to print
                lon_str = "  {} {}".format(abs(round(msg.longitude,6)),msg.lon_dir) # Sets Longitude vaiable to print
                display.lcd_display_string(lat_str, 1) # Prints out the Latitude on row 1
                display.lcd_display_string(lon_str, 2) # Prints out the Latitude on row 2

                # Logs the data to a csv file
                with open(csvfile, "a") as fp:
                    wr = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    wr.writerow([msg.latitude, msg.longitude, timestamp])
                time.sleep(5) # Time the program loops again, in seconds
                display.lcd_clear() # Clears the screen to prevent getting "NN", "WW", "SS", or "EE" after the Lat and Long

        # If there is a device error, inform user, wait two seconds to see
        # if it will correct itself, and then continue
        except serial.SerialException as e:
            print('Device error: {}'.format(e))
            display.lcd_display_string("Device error",1)
            display.lcd_display_string("Please hold",2)
            time.sleep(2)
            display.lcd_clear()
            continue

        # If there is a parsing error, inform user, wait two seconds to see
        # if it will correct itself, and then continue
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            display.lcd_display_string("Parse error",1)
            display.lcd_display_string("Please hold",2)
            time.sleep(2)
            display.lcd_clear()
            continue


# Graceful exit
except (KeyboardInterrupt, SystemExit):
    display.lcd_clear()
    print("\nExiting.")


