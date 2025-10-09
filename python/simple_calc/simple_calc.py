#
# File: simple_calc.py
# Author: Meghan Paral
# License: 3-Clause BSD


import operator
import sys

# Dictionary of operators
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

def get_user_input():
    """Get input from the user.
    Returns tuple: (number, number, function) or
    (None, None, None) if the inputs are invalid
    """
    if sys.version_info[0] < 3:
        input_func = raw_input
    else:
        input_func = input

    try:
        in1 = input_func("Enter first number: ")
        op  = input_func("Enter function (valid values are +, -, *, /, >>, <<, %, **): ")
        in2 = input_func("Enter second number: ")

        func = operators.get(op)

        
        if op == ">>" or op == "<<":
            number1 = int(in1)
            number2 = int(in2)
        else:
            number1 = float(in1)
            number2 = float(in2)

    except:
        return (None, None, None)

    return (number1, number2, func)

if __name__ == "__main__":

    while True:
        (num1, num2, func) = get_user_input()

        if (num1 is None) or (num2 is None) or (func is None):
            print("Invalid input")
            break

        print(func(num1, num2))