# Creation Date:  04/13/2022
# Run: python 3n+1-Task.py
# Description: This program is written for the AP Computer Science Principles Performance Task.
# Its purpose is to find how many loops of the 3n+1 (Collatz conjecture) formula it takes to reach 1.
# If you do not know what the Collatz Conjecture is, it's a formula that says if the number is even
# divide it by 2. If it's odd, multiply it by 3 and add 1.  You repeat this process until you reach one.
# My program automates this process and tells you how many times it looped through the even or odd
# formulas and what the highest number it reached.

# Add all needed imports
import math
import re
import time

run = 1
while run == 1:

    n = int(input("Pick a number? >>>"))

    ornum = n

    if not n > 1:  # Make sure the number is greater than 1.
        # If the user does not enter a number greater than 1, the program will return this message.
        print("Please enter a number greater than 1 for the program to run.")

    def DecimalToBinary(num):
        return "{0:b}".format(int(num))

    binum = DecimalToBinary(n)

    print('')
    print('')
    print('-------------------------------------------')
    # Prints the original number inputted by the user.
    print('Decimal Number > ' + str(ornum))
    print('Binary Number > ' + str(binum))

    # Prints the highest number reached during the loops.
    print('-------------------------------------------')
    print('')
    print('')
