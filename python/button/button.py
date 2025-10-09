#
# File: button.py
# Author: Meghan Paral
#
# License: 3-Clause BSD
# Description: A class to manage and detect button presses on a GPIO pin.
#              The driver code waits for a button press on P2_02 and prints a message.
#
#

import Adafruit_BBIO.GPIO as GPIO
import time

class Button():
    """A class to represent a button connected to a GPIO pin."""
    def __init__(self, pin):
        """Initializes the button on a given pin."""
        self.pin = pin
        self._setup()

    def _setup(self):
        """Setup the button."""
        GPIO.setup(self.pin, GPIO.IN)

    def is_pressed(self):
        """Returns True if the button is pressed."""
        if GPIO.input(self.pin) == 0:
            return True
        else:
            return False

    def wait_for_press(self):
        """Waits for the button to be pressed."""
        GPIO.wait_for_edge(self.pin, GPIO.FALLING)

#
# Main function (Driver)
#
if __name__ == "__main__":
    
    BUTTON_PIN = "P2_02"
    button = Button(BUTTON_PIN)

    print(f"Waiting for button press on {BUTTON_PIN}... Press Ctrl+C to exit.")

    try:
        while True:
            button.wait_for_press()
            print("Button Pressed!")
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nCleaning up and exiting.")
        GPIO.cleanup()