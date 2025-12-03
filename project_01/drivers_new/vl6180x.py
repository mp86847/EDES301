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

File: vl6180x.py
Author: Meghan Paral
Date:  12/02/2025
Description: A low-level driver for the VL6180X time-of-flight sensor that communicates over I²C
"""

import time
import smbus
import os

REG_IDENTIFICATION_MODEL_ID    = 0x000
REG_SYSTEM_FRESH_OUT_OF_RESET  = 0x016
REG_SYSRANGE_START             = 0x018
REG_SYSALS_START               = 0x038
REG_RESULT_RANGE_STATUS        = 0x04d
REG_RESULT_INTERRUPT_STATUS_GPIO = 0x04f
REG_RESULT_RANGE_VAL           = 0x062
REG_SYSTEM_INTERRUPT_CLEAR     = 0x015

class VL6180X:
    def __init__(self, bus_id=2, address=0x29):
        self.address = address
        self.bus = smbus.SMBus(bus_id)
        
        try:
            model_id = self.read_reg(REG_IDENTIFICATION_MODEL_ID)
            if model_id != 0xB4:
                print(f"Warning: Strange Model ID: {hex(model_id)}")
        except Exception as e:
            print(f"Error connecting to VL6180X: {e}")
            raise

        if self.read_reg(REG_SYSTEM_FRESH_OUT_OF_RESET) == 1:
            self.load_settings()
            self.write_reg(REG_SYSTEM_FRESH_OUT_OF_RESET, 0x00)

    def write_reg(self, reg, value):
        """Writes an 8-bit value to a 16-bit register."""
        reg_high = (reg >> 8) & 0xFF
        reg_low  = reg & 0xFF
        self.bus.write_i2c_block_data(self.address, reg_high, [reg_low, value])

    def read_reg(self, reg):
        """Reads an 8-bit value from a 16-bit register."""
        reg_high = (reg >> 8) & 0xFF
        reg_low  = reg & 0xFF
        self.bus.write_i2c_block_data(self.address, reg_high, [reg_low])
        
        return self.bus.read_byte(self.address)

    def poll_range(self):
        """Performs a single-shot range measurement."""
        self.write_reg(REG_SYSRANGE_START, 0x01)
        
        for _ in range(100):
            status = self.read_reg(REG_RESULT_INTERRUPT_STATUS_GPIO)
            if (status & 0x04):
                break
            time.sleep(0.001)
        
        range_mm = self.read_reg(REG_RESULT_RANGE_VAL)
        
        self.write_reg(REG_SYSTEM_INTERRUPT_CLEAR, 0x07)
        
        return range_mm

    def load_settings(self):
        """Loads mandatory tuning settings from datasheet."""
        self.write_reg(0x0207, 0x01)
        self.write_reg(0x0208, 0x01)
        self.write_reg(0x0096, 0x00)
        self.write_reg(0x0097, 0xfd)
        self.write_reg(0x00e3, 0x00)
        self.write_reg(0x00e4, 0x04)
        self.write_reg(0x00e5, 0x02)
        self.write_reg(0x00e6, 0x01)
        self.write_reg(0x00e7, 0x03)
        self.write_reg(0x00f5, 0x02)
        self.write_reg(0x00d9, 0x05)
        self.write_reg(0x00db, 0xce)
        self.write_reg(0x00dc, 0x03)
        self.write_reg(0x00dd, 0xf8)
        self.write_reg(0x009f, 0x00)
        self.write_reg(0x00a3, 0x3c)
        self.write_reg(0x00b7, 0x00)
        self.write_reg(0x00bb, 0x3c)
        self.write_reg(0x00b2, 0x09)
        self.write_reg(0x00ca, 0x09)
        self.write_reg(0x0198, 0x01)
        self.write_reg(0x01b0, 0x17)
        self.write_reg(0x01ad, 0x00)
        self.write_reg(0x00ff, 0x05)
        self.write_reg(0x0100, 0x05)
        self.write_reg(0x0199, 0x05)
        self.write_reg(0x01a6, 0x1b)
        self.write_reg(0x01ac, 0x3e)
        self.write_reg(0x01a7, 0x1f)
        self.write_reg(0x0030, 0x00)
