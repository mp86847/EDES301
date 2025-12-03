"""
--------------------------------------------------------------------------
Button Driver
--------------------------------------------------------------------------
License:   
Copyright 2021-2025 - Meghan Paral

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

Button Driver

  This driver can support buttons that have either a pull up resistor between the
button and the processor pin (i.e. the input is "High" / "1" when the button is
not pressed) and will be connected to ground when the button is pressed (i.e. 
the input is "Low" / "0" when the button is pressed), or a pull down resistor 
between the button and the processor pin (i.e. the input is "Low" / "0" when the 
button is not pressed) and will be connected to power when the button is pressed
(i.e. the input is "High" / "1" when the button is pressed).

  To select the pull up configuration, press_low=True.  To select the pull down
configuration, press_low=False.

"""
import time
import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
HIGH = GPIO.HIGH
LOW  = GPIO.LOW

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------
# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class Button():
    """ Button Class """
    pin                           = None
    unpressed_value               = None
    pressed_value                 = None
    sleep_time                    = None
    press_duration                = None
    pressed_callback              = None
    pressed_callback_value        = None
    unpressed_callback            = None
    unpressed_callback_value      = None
    on_press_callback             = None
    on_press_callback_value       = None
    on_release_callback           = None
    on_release_callback_value     = None
    
    def __init__(self, pin=None, press_low=True, sleep_time=0.1):
        if (pin == None):
            raise ValueError("Pin not provided for Button()")
        else:
            self.pin = pin
        
        if press_low:
            self.unpressed_value = HIGH
            self.pressed_value   = LOW
        else:
            self.unpressed_value = LOW
            self.pressed_value   = HIGH
        
        self.sleep_time      = sleep_time
        self.press_duration  = 0.0        
        self._setup()
    
    def _setup(self):
        """ Setup the hardware components. """
        # HW#4 TODO: (one line of code)
        GPIO.setup(self.pin, GPIO.IN)

    def is_pressed(self):
        """ Is the Button pressed? """
        # HW#4 TODO: (one line of code)
        return GPIO.input(self.pin) == self.pressed_value

    def wait_for_press(self):
        """ Wait for the button to be pressed. """
        button_press_time = None
        
        # Wait for button press
        # HW#4 TODO: (one line of code)
        while(GPIO.input(self.pin) == self.unpressed_value):
            if self.unpressed_callback is not None:
                self.unpressed_callback_value = self.unpressed_callback()
            time.sleep(self.sleep_time)
            
        button_press_time = time.time()
        
        if self.on_press_callback is not None:
            self.on_press_callback_value = self.on_press_callback()
        
        # Wait for button release
        # HW#4 TODO: (one line of code)
        while(GPIO.input(self.pin) == self.pressed_value):
            if self.pressed_callback is not None:
                self.pressed_callback_value = self.pressed_callback()
            time.sleep(self.sleep_time)
        
        self.press_duration = time.time() - button_press_time

        if self.on_release_callback is not None:
            self.on_release_callback_value = self.on_release_callback()        
        
    def get_last_press_duration(self):
        return self.press_duration
    
    def cleanup(self):
        pass
    
    # Callback Functions
    def set_pressed_callback(self, function):
        self.pressed_callback = function
    
    def get_pressed_callback_value(self):
        return self.pressed_callback_value
    
    def set_unpressed_callback(self, function):
        self.unpressed_callback = function
    
    def get_unpressed_callback_value(self):
        return self.unpressed_callback_value
    
    def set_on_press_callback(self, function):
        self.on_press_callback = function
    
    def get_on_press_callback_value(self):
        return self.on_press_callback_value
    
    def set_on_release_callback(self, function):
        self.on_release_callback = function
    
    def get_on_release_callback_value(self):
        return self.on_release_callback_value
# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
if __name__ == '__main__':
    print("Button Test")
    
    # In the assignment, the button is connected to P2_02 (GPIO 59)
    button = Button("P2_02")
    
    print("Waiting for button press ...")
    button.wait_for_press()
    print(f"    Button was pressed for {button.get_last_press_duration():.2f} seconds.")

    print("\nTest Complete")