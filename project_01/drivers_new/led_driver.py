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

File: led_driver.py
Author: Meghan Paral
Date:  12/02/2025
Description: A GPIO-based driver that controls LEDs
"""

import Adafruit_BBIO.GPIO as GPIO
import time

class LED:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.off() # Default to off

    def on(self):
        """Turns the LED on."""
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        """Turns the LED off."""
        GPIO.output(self.pin, GPIO.LOW)

    def toggle(self):
        """Switches the LED state."""
        if GPIO.input(self.pin):
            self.off()
        else:
            self.on()

    def blink(self, duration=1, rate=0.2):
        """Blinks the LED for 'duration' seconds at 'rate'."""
        end_time = time.time() + duration
        while time.time() < end_time:
            self.on()
            time.sleep(rate)
            self.off()
            time.sleep(rate)

# --- TEST CODE ---
if __name__ == "__main__":
    # Test with Green LED Pin (P2_18)
    green = LED("P2_18")
    print("Testing Green LED...")
    green.on()
    time.sleep(1)
    green.off()
    time.sleep(1)
    print("Blinking...")
    green.blink(3)
    print("Done.")
