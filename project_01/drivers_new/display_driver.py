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

File: display_driver.py
Author: Meghan Paral
Date:  12/02/2025
Description: A driver for the HT16K33 LED display that shows numbers or short text and clears output for real-time game feedback.
"""

import ht16k33
import time
import os

class Display:
    def __init__(self):
        """
        Wrapper HT16K33 library
        """
        os.system("config-pin P1_26 i2c")
        os.system("config-pin P1_28 i2c")

        try:
            self.display = ht16k33.HT16K33(2, 0x70)
            self.display.setup(ht16k33.HT16K33_BLINK_OFF, ht16k33.HT16K33_BRIGHTNESS_HIGHEST)
            self.clear()
        except Exception as e:
            print(f"Error initializing display: {e}")

    def show_number(self, number):
        """Displays a number (0-9999)."""
        try:
            self.display.update(int(number))
        except ValueError:
            self.display.text("Err")

    def show_text(self, text):
        """Displays text (limited to 4 chars)."""
        self.display.text(str(text))

    def clear(self):
        """Turns off all LEDs."""
        self.display.blank()

    def colon(self, state):
        """Turns the colon on (True) or off (False)."""
        self.display.set_colon(state)

# --- TEST CODE ---
if __name__ == "__main__":
    print("--- Testing HT16K33 Display ---")
    try:
        disp = Display()
        
        print("Showing 1234...")
        disp.show_number(1234)
        time.sleep(1)
        
        print("Showing 'PLAY'...")
        disp.show_text("PLAY")
        time.sleep(1)
        
        print("Clearing (Should go dark)...")
        disp.clear()
        print("Test Complete.")

    except Exception as e:
        print(f"Test Failed: {e}")
