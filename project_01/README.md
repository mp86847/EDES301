# Trach-Hero: Emergency Training Game

## Project Description
This project is a "bop-it" style game with abstractions to trachoetomy care. Players attempt to resolve as many "deccanulation", "tube obstruction", and "emergency" scenarios in 30 seconds.

## Hardware Required
* **Controller:** PocketBeagle
* **Actuator:** Micro Servo 9g (Simulates patient movement)
* **Sensors:** * VL6180X Time-of-Flight Distance Sensor (Suction detection)
    * 3144 Hall Effect Sensor (Tube detection)
    * 2x Momentary Push Buttons (Inputs)
* **Outputs:**
    * HT16K33 7-Segment Display (Score/Status)
    * 2x Piezo Buzzers (Heartbeat & Alarm)
    * 5x LEDs (Status Indicators)

## Software Build Instructions
1.  **Configure Pins:**
    Ensure the `configure_pins.sh` script is executable:
    ```bash
    chmod +x configure_pins.sh
    ```

2.  **Install Libraries:**
    This project uses standard Linux I2C commands and Python libraries.
    ```bash
    sudo apt-get update
    sudo apt-get install python3-smbus i2c-tools
    ```

3.  **Directory Structure:**
    Ensure all component drivers are located in the `drivers/` subdirectory.

## Software Operation Instructions
1.  **Initialize the System:**
    Run the configuration script to set up GPIO, PWM, and I2C modes:
    ```bash
    sudo ./configure_pins.sh
    ```

2.  **Run the Game:**
    Start the main game loop using Python 3:
    ```bash
    sudo python3 game.py
    ```

3.  **Gameplay:**
    * The display will show "RDY". Press the **Start Button** to begin.
    * **Green LED:** Remove the magnet from the Hall sensor, then replace it.
    * **Yellow LED:** Hold your hand over the Distance Sensor for 1.5 seconds.
    * **White LED:** Press the EMS button.
    * Survive as long as possible!

## Hackster.io Project Page
For detailed build instructions, wiring diagrams, and a demo video, please visit the project page: https://www.hackster.io/mp86/trach-hero-a10c02

