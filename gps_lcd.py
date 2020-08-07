#!/usr/bin/env python3
# Imports all the libraries we use for the GPS
import serial
import pynmea2

# Imports the driver/library for the LCD Screen
import lcddriver
import time

# Load the driver and set it to "display"
display = lcddriver.lcd()

# Initialize the serial object for the GPS Module
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=5.0) #initialize serial object


# Try loop that allows for a graceful exit if needed
try:
    while True:
        try:
            # Gets the data from the sensor and writes it in a
            # format that the rest of the code can read.
            encoded_line = ser.readline() #read nmea sentence
            line = encoded_line.decode('utf-8')
            msg = pynmea2.parse(line)
            #print(repr(msg)) # Uncomment this line to debug, prints out full message

            if line.find('GGA') > 0: # Search for the specific GPS message we want
                # Prints out Latitude and Longitude when a fix is acquired
                print("-------------------")
                print("Fix Acquired") 
                print(msg.latitude, msg.lat_dir)
                print(abs(msg.longitude), msg.lon_dir)

                # Code for printing out on the LCD
                lat_str = "  {} {}".format(round(msg.latitude,6),msg.lat_dir) # Sets Latitude variable to print
                lon_str = "  {} {}".format(abs(round(msg.longitude,6)),msg.lon_dir) # Sets Longitude vaiable to print
                display.lcd_display_string(lat_str, 1) # Prints out the Latitude on row 1
                display.lcd_display_string(lon_str, 2) # Prints out the Latitude on row 2
                time.sleep(5) # Time the program loops again, in seconds

        except serial.SerialException as e:
            print('Device error: {}'.format(e)) 
            display.lcd_clear()
            continue
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            display.lcd_clear()
            continue


# Graceful exit
except (KeyboardInterrupt, SystemExit):
    display.lcd_clear()
    print("\nExiting.")

