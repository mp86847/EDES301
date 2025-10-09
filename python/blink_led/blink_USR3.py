#
# File: blink_USR3.py
# Author: Meghan Paral
# License: 3-Clause BSD
#
# Description:
# This script blinks the USR3 LED on the PocketBeagle at 5 Hz.
# [cite: 1007, 1008]
#

import Adafruit_BBIO.GPIO as GPIO
import time

# Define the LED and frequency
USR3_LED = "USR3"
FREQ_HZ  = 5.0
DELAY_S  = 1.0 / (2 * FREQ_HZ) # Delay for on and off states (0.1s)

GPIO.setup(USR3_LED, GPIO.OUT)

print("Blinking USR3 LED at 5 Hz. Press Ctrl+C to stop.")

try:
    while True:
        # Turn LED on
        GPIO.output(USR3_LED, GPIO.HIGH)
        time.sleep(DELAY_S)

        # Turn LED off
        GPIO.output(USR3_LED, GPIO.LOW)
        time.sleep(DELAY_S)

except KeyboardInterrupt:
    print("\nCleaning up and exiting.")
    GPIO.cleanup()