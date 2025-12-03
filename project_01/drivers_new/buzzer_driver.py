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

File: buzzer_driver.py
Author: Meghan Paral
Date:  12/02/2025
Description: A simple driver that controls a buzzer for audio feedback, enabling tones or alerts during gameplay events.
"""

import Adafruit_BBIO.PWM as PWM
import time

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        PWM.start(self.pin, 0, 2000, 0)

    def tone(self, frequency, duration=None):
        """
        Plays a tone at the specified frequency (Hz).
        If duration is provided, plays for that time and then stops.
        """
        PWM.set_frequency(self.pin, frequency)
        PWM.set_duty_cycle(self.pin, 50) # 50% Duty Cycle = Max Volume
        
        if duration:
            time.sleep(duration)
            self.off()

    def heartbeat(self):
        """Plays a 'lub-dub' heartbeat sound."""
        self.tone(1000, 0.1) # Lub
        time.sleep(0.1)
        self.tone(1000, 0.1) # Dub

    def alarm(self):
        """Plays a high-pitched alarm chirp."""
        self.tone(3000, 0.2)

    def off(self):
        """Silences the buzzer."""
        PWM.set_duty_cycle(self.pin, 0)

    def cleanup(self):
        """Stops PWM and cleans up."""
        PWM.stop(self.pin)
        PWM.cleanup()

# --- TEST CODE ---
if __name__ == "__main__":
    print("--- Testing Buzzers ---")
    print("Testing Heartbeat (P2_01)...")
    heartbeat = Buzzer("P2_1")
    
    for i in range(3):
        heartbeat.heartbeat()
        time.sleep(0.8)
    
    heartbeat.cleanup()
    print("Testing Alarm (P2_03)...")
    alarm = Buzzer("P2_3")
    
    for i in range(3):
        alarm.alarm()
        time.sleep(0.3)
        
    alarm.cleanup()
    print("Test Complete.")
