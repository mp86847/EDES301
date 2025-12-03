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

File: servo_driver.py
Author: Meghan Paral
Date:  12/02/2025
Description: A PWM-based driver for SG90 servos that maps positions to duty cycles
"""

import Adafruit_BBIO.PWM as PWM

SG90_FREQ = 50      # 50Hz
SG90_POL = 0        # Rising Edge polarity
SG90_MIN_DUTY = 5   # 5% duty cycle (Fully clockwise/right)
SG90_MAX_DUTY = 10  # 10% duty cycle (Fully anti-clockwise/left)

class Servo():
    pin = None
    position = None

    def __init__(self, pin=None, default_position=0):
        """ Initialize variables and set up the Servo """
        if (pin == None):
            raise ValueError("Pin not provided for Servo()")
        else:
            self.pin = pin
            self.position = default_position
            self._setup(default_position)

    def _setup(self, default_position):
        """Setup the hardware components."""
        PWM.start(self.pin, self._duty_cycle_from_position(default_position),
                  SG90_FREQ, SG90_POL)

    def _duty_cycle_from_position(self, position):
        """ Compute the duty cycle from the position. """
        return ((SG90_MAX_DUTY - SG90_MIN_DUTY) * (position / 100)) + SG90_MIN_DUTY

    def get_position(self):
        """ Return the position of the servo """
        return self.position

    def turn(self, position):
        """
        Turn Servo to the desired position based on percentage of motion range
        0 = Fully clockwise (right)
        100 = Fully anti-clockwise (left)
        """
        self.position = position
        PWM.set_duty_cycle(self.pin, self._duty_cycle_from_position(position))

    def stop(self):
        """
        Stops the signal to the servo to prevent buzzing/heating.
        (Added for Game functionality)
        """
        PWM.set_duty_cycle(self.pin, 5)

    def cleanup(self):
        """Cleanup the hardware components."""
        PWM.stop(self.pin)

# ------------------------------------------------------------------------
# Test script
# ------------------------------------------------------------------------
if __name__ == '__main__':
    import time
    print("Servo Test")
    servo = Servo("P1_36")
    print("Use Ctrl-C to Exit")
    
    try:
        while(1):
            # Turn Servo anti-clockwise
            print("Turning to 0%")
            servo.turn(5)
            time.sleep(0.5)
            
            print("Turning to 100%")
            servo.turn(35)
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        pass
    
    servo.cleanup()
    print("Test Complete")