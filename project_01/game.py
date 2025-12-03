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

File: game.py
Author: Meghan Paral
Date:  12/02/2025
Description: Main game loop for Trach-Hero Game
"""

import time
import random
import sys
import os

# --- PATH SETUP ---
# Add the 'drivers' folder to the system path so we can import our files
sys.path.append('drivers_new')

# --- IMPORT DRIVERS ---
from led_driver import LED
from button_driver import Button
from servo_driver import Servo
from buzzer_driver import Buzzer
from tof_driver import DistanceSensor
from display_driver import Display

# --- GAME CONFIGURATION ---
GAME_DURATION = 30        # Total game time in seconds
BASE_TIMEOUT = 10.0       # Starting time limit for scenarios (Easier)
MIN_TIMEOUT = 2.0         # Minimum time limit (fastest speed)
TOF_THRESHOLD = 39        # Distance in mm for "suction" detection

class TrachGame:
    def __init__(self):
        print("Initializing Hardware...")
        
        # --- OUTPUTS ---
        # LEDs (Active High) - Pins must NOT have leading zeros for Python library
        self.led_red  = LED("P2_18")
        self.led_yellow = LED("P2_20")
        self.led_green  = LED("P2_22")
        self.led_white    = LED("P2_24")
        self.led_blue   = LED("P2_28")
        
        # Servo (Professor's Driver uses 0-100% logic)
        # Start at 0% (Fully Clockwise / Closed)
        self.servo = Servo("P1_36", default_position=0)
        # Stop signal immediately to prevent buzzing
        self.servo.stop() 
        
        # Buzzers (PWM)
        self.buzzer_hb = Buzzer("P2_1")
        self.buzzer_alarm = Buzzer("P2_3")
        
        # Display (I2C)
        self.display = Display()
        
        # --- INPUTS ---
        # Buttons (Active Low)
        self.btn_start = Button("P2_2")
        self.btn_ems   = Button("P2_4")
        self.sensor_hall = Button("P2_6") # Hall acts like a button
        
        # Time-of-Flight Sensor (I2C)
        try:
            self.sensor_tof = DistanceSensor()
        except Exception as e:
            print(f"Warning: ToF Sensor init failed: {e}")
            self.sensor_tof = None # Graceful fallback if sensor fails

        self.score = 0
        self.current_timeout = BASE_TIMEOUT

    def setup_game(self):
        """Resets hardware to 'Ready' state."""
        self.all_leds_off()
        
        # Move Servo to Calm Position (10%)
        self.servo.turn(10)
        time.sleep(0.3)
        self.servo.stop() # Stop buzzing
        
        self.buzzer_hb.off()
        self.buzzer_alarm.off()
        self.display.clear()
        self.display.show_text("RDY")

    def all_leds_off(self):
        self.led_green.off()
        self.led_yellow.off()
        self.led_white.off()
        self.led_red.off()
        self.led_blue.off()

    def play_sound_success(self):
        """Happy Chime"""
        self.buzzer_alarm.tone(1500, 0.1)
        self.buzzer_alarm.tone(2000, 0.2)

    def play_sound_fail(self):
        """Sad Womp Womp"""
        self.buzzer_alarm.tone(400, 0.3)
        self.buzzer_alarm.tone(300, 0.5)

    def twitch_patient(self):
        """Simulates patient struggling using Servo."""
        # Move to random position between 20% and 60%
        target = random.randint(20, 60)
        self.servo.turn(target)
        time.sleep(0.15)
        self.servo.turn(10) # Return to rest
        time.sleep(0.15)
        self.servo.stop() # Stop buzzing

    # ---------------------------------------------------------
    # SCENARIO A: Accidental Decannulation
    # ---------------------------------------------------------
    def scenario_decannulation(self):
        """Task: Remove tube (Hall HIGH) -> Insert tube (Hall LOW)."""
        print("[A] Decannulation! (Green LED)")
        self.led_green.on()
        
        start_time = time.time()
        tube_removed = False
        
        # Step 1: Detect Removal (Magnet moves AWAY)
        # Hall Sensor is Active Low (0 = Magnet Present).
        # We wait for it to go HIGH (1 = Magnet Gone).
        while (time.time() - start_time) < self.current_timeout:
            if not self.sensor_hall.is_active(): # is_active is False when magnet gone
                tube_removed = True
                print("  -> Trach OUT! Quick, re-insert!")
                break
            time.sleep(0.05)
            
        if not tube_removed:
            return False # Failed step 1

        # Step 2: Detect Insertion (Magnet comes BACK)
        while (time.time() - start_time) < self.current_timeout:
            if self.sensor_hall.is_active(): # is_active is True when magnet present
                self.led_green.off()
                print("  -> Trach IN! Safe.")
                return True
            time.sleep(0.05)
            
        self.led_green.off()
        return False

    # ---------------------------------------------------------
    # SCENARIO B: Tube Obstruction
    # ---------------------------------------------------------
    def scenario_obstruction(self):
        """Task: Suction (ToF < 40mm) for 1.5 seconds."""
        print("[B] Obstruction! Suction! (Yellow LED)")
        self.led_yellow.on()
        
        if self.sensor_tof is None:
            return True # Auto-win if sensor broken

        start_time = time.time()
        suction_start_time = 0
        is_suctioning = False
        
        while (time.time() - start_time) < self.current_timeout:
            # Check distance
            blocked = self.sensor_tof.is_blocked(TOF_THRESHOLD)

            if blocked and not is_suctioning:
                # Started suctioning
                is_suctioning = True
                suction_start_time = time.time()
                print("  -> Suctioning Started...")
            
            elif blocked and is_suctioning:
                # Currently suctioning, check duration
                duration = time.time() - suction_start_time
                # Print progress every 0.5 seconds roughly
                if int(duration * 10) % 5 == 0: 
                    print(f"  -> Suctioning... {duration:.1f}s")

                if duration > 1.5:
                    self.led_yellow.off()
                    print("  -> Airway Cleared!")
                    return True
            
            elif not blocked and is_suctioning:
                # Pulled out too early, reset timer
                is_suctioning = False
                print("  -> Suction interrupted! Try again.")
            
            time.sleep(0.05)

        self.led_yellow.off()
        return False

    # ---------------------------------------------------------
    # SCENARIO C: Call EMS
    # ---------------------------------------------------------
    def scenario_ems(self):
        """Task: Press EMS Button."""
        print("[C] Call EMS! (White LED)")
        self.led_white.on()
        
        start_time = time.time()
        while (time.time() - start_time) < self.current_timeout:
            if self.btn_ems.is_active():
                self.led_white.off()
                print("  -> EMS Called!")
                return True
            time.sleep(0.05)
            
        self.led_white.off()
        return False

    # ---------------------------------------------------------
    # MAIN GAME LOOP
    # ---------------------------------------------------------
    def play_game(self):
        print("--- GAME START ---")
        self.score = 0
        self.current_timeout = BASE_TIMEOUT
        self.display.show_number(self.score)
        
        game_start = time.time()
        last_heartbeat = 0
        heartbeat_interval = 1.0
        
        # Initial Agitation
        self.servo.turn(30)
        time.sleep(0.5)
        self.servo.stop()

        while (time.time() - game_start) < GAME_DURATION:
            
            # --- 1. Anxiety Engine (Heartbeat) ---
            if (time.time() - last_heartbeat) > heartbeat_interval:
                self.buzzer_hb.heartbeat()
                last_heartbeat = time.time()
                # Speed up heartbeat as time runs out
                elapsed = time.time() - game_start
                heartbeat_interval = max(0.4, 1.0 - (elapsed / GAME_DURATION))

            # --- 2. Random Twitch ---
            if random.random() < 0.15: # 15% chance per loop
                self.twitch_patient()

            # --- 3. Run Random Scenario ---
            scenario = random.choice(['A', 'B', 'C'])
            success = False

            if scenario == 'A':
                success = self.scenario_decannulation()
            elif scenario == 'B':
                success = self.scenario_obstruction()
            elif scenario == 'C':
                success = self.scenario_ems()
            
            # --- 4. Handle Result ---
            if success:
                print(">> PASSED!")
                self.play_sound_success()
                self.score += 1
                self.display.show_number(self.score)
                # Increase difficulty (faster timeout)
                self.current_timeout = max(MIN_TIMEOUT, self.current_timeout - 0.5)
            else:
                print(">> FAILED! GAME OVER.")
                self.play_sound_fail()
                self.led_blue.on() # Cyanosis
                # Patient Coughs (Servo twitch)
                self.servo.turn(50)
                time.sleep(0.2)
                self.servo.turn(20)
                time.sleep(0.2)
                self.servo.stop()
                
                time.sleep(2) # Pause on failure
                return # End game

            time.sleep(0.5) # Breath between scenarios

        # --- Game Win (Time Expired) ---
        print("TIME UP! YOU SURVIVED.")
        self.display.show_text("DONE")
        
        # Score Celebration
        for _ in range(3):
            self.display.clear()
            time.sleep(0.3)
            self.display.show_number(self.score)
            time.sleep(0.3)

    def main_loop(self):
        try:
            self.setup_game()
            print("System Ready. Press START Button (P2_2).")
            
            while True:
                if self.btn_start.is_active():
                    self.play_game()
                    self.setup_game() # Reset for next round
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.all_leds_off()
            self.display.clear()
            # Only cleanup at the VERY end
            self.servo.cleanup()
            self.buzzer_hb.cleanup()
            self.buzzer_alarm.cleanup()

if __name__ == "__main__":
    # Run configuration script first to be safe
    os.system("./configure_pins.sh")
    
    game = TrachGame()
    game.main_loop()