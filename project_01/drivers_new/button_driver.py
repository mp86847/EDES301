"""
--------------------------------------------------------------------------
Trach-Hero Game
--------------------------------------------------------------------------
License:   
Copyright 2025 - Meghan Paral

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

File: button_driver.py
Author: Meghan Paral
Date:  12/02/2025
Description: 
    A GPIO-based driver that detects button presses or Hall sensor activation, supporting press/release events with active-low logic

"""

import Adafruit_BBIO.GPIO as GPIO
import time

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def is_active(self):
        """
        Returns True if the button is pressed or Hall sensor detects a magnet.
        Active Low logic: 0 means active (grounded), 1 means inactive (pulled up to 3.3V).
        """
        return GPIO.input(self.pin) == 0

    def wait_for_press(self):
        """Blocks execution until the button is pressed (signal goes LOW)."""
        if self.is_active():
            return
        # Otherwise wait for the voltage to drop (Falling Edge)
        GPIO.wait_for_edge(self.pin, GPIO.FALLING)

    def wait_for_release(self):
        """Blocks execution until the button is released (signal goes HIGH)."""
        if not self.is_active():
            return
        GPIO.wait_for_edge(self.pin, GPIO.RISING)

# --- TEST CODE 
if __name__ == "__main__":
    test_pin = "P2_6"  #Hall Effect
    
    print(f"--- Testing Button on {test_pin} ---")
    button = Button(test_pin)

    if button.is_active():
        print("Button is currently HELD DOWN.")
    else:
        print("Button is OPEN (Not pressed).")

    print("Please PRESS the button now...")
    button.wait_for_press()
    print(">> Button PRESSED!")

    print("Now RELEASE the button...")
    button.wait_for_release()
    print(">> Button RELEASED!")
    print("Test Complete.")
