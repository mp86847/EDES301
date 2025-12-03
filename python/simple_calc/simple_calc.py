# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Simple Calculator
--------------------------------------------------------------------------
License:   
Copyright 2025 - Meghan Paral

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Simple calculator that will 
  - Take in two numbers from the user
  - Take in an operator from the user
  - Perform the mathematical operation and provide the number to the user
  - Repeat

Operations:
  - "+" : addition
  - "-" : subtraction
  - "*" : multiplication
  - "/" : division
  - ">>": right shift
  - "<<": left shift
  - "%" : modulo
  - "**": exponentiation

Error conditions:
  - Invalid operator --> Program should exit
  - Invalid number   --> Program should exit

--------------------------------------------------------------------------
"""
import operator
import sys

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------
operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    ">>": operator.rshift,
    "<<": operator.lshift,
    "%": operator.mod,
    "**": operator.pow
}

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def get_user_input():
    """ Get input from the user.
        Returns tuple:  (number, number, function) or 
                        (None, None, None) if inputs invalid
    """
    # Use "try"/"except" statements to allow code to handle errors gracefully.      
    try:
        # Check Python version to use correct input function
        if sys.version_info[0] < 3:
            input_func = raw_input
        else:
            input_func = input
            
        in1 = input_func("Enter first number: ")
        op  = input_func("Enter function (valid values are +, -, *, /, >>, <<, %, **): ")
        in2 = input_func("Enter second number: ")

        func = operators.get(op)

        # Shift operators require integers
        if op == ">>" or op == "<<":
            number1 = int(in1)
            number2 = int(in2)
        else:
            number1 = float(in1)
            number2 = float(in2)
            
        return (number1, number2, func)

    except (ValueError, TypeError):
        return (None, None, None)
# End def

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
if __name__ == "__main__":
    while True:
        (num1, num2, func) = get_user_input()

        if (num1 is None) or (num2 is None) or (func is None):
            print("Invalid Input. Exiting.")
            break

        result = func(num1, num2)
        print(f"Result: {result}")