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

File: tof_driver.py
Author: Meghan Paral
Date:  12/02/2025
Description: A driver for the VL6180X time-of-flight sensor that measures distance in millimeters and detects nearby obstructions
"""

import time
import os
import vl6180x

class DistanceSensor:
    def __init__(self):
        """
        Initializes the VL6180X ToF sensor on I2C Bus 2.
        Uses local 'vl6180x.py' driver (No Adafruit libraries).
        """
        os.system("config-pin P1_26 i2c")
        os.system("config-pin P1_28 i2c")

        try:
            self.sensor = vl6180x.VL6180X(bus_id=2, address=0x29)
        except Exception as e:
            print(f"\n[ToF Error] {e}")
            print("Check: 1. 2.2k Pull-up resistors. 2. Wiring.")
            raise

    def get_distance(self):
        """Returns distance in millimeters."""
        return self.sensor.poll_range()

    def is_blocked(self, threshold_mm=40):
        """Returns True if object is closer than threshold."""
        return self.get_distance() < threshold_mm

# --- TEST CODE ---
if __name__ == "__main__":
    print("--- Testing VL6180X (Custom Driver) ---")
    
    try:
        tof = DistanceSensor()
        print("Sensor Initialized. Reading data...")
        
        while True:
            dist = tof.get_distance()
            status = "BLOCKED" if dist < 40 else "CLEAR"
            print(f"Dist: {dist} mm | Status: {status}")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nTest Stopped.")
    except Exception as e:
        print(f"\nCritical Error: {e}")
