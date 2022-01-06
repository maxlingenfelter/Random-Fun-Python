import numpy as np
import statistics
import math


# def factorial(n):
#     # single line to find factorial
#     return 1 if (n == 1 or n == 0) else n * factorial(n - 1)


run = 1
while run == 1:
    n = int(input("Pick a line number? >>>"))

    # Define factorial

    def factorial(a):
        Prod = 1
        for j in range(1, a+1):
            Prod = j*Prod
        return Prod

    # print("Factorial of", 7, "is", factorial(7)) = 720

    # Define Combination

    def combination(n, m):
        Choose = factorial(n)/(factorial(n-m)*factorial(m))
        # "m" is the postion in the array, "n" is the row number that you wish to get the values of.
        return Choose

    # For example, to find the 4th number(3rd position in Python) on the 7th row we would say:
    # print("Combination of row", 7, "and position", 3, "is", combination(7, 3))

    ar = []

    length = len(ar)

    len2 = n+1
    for c in range(len2):
        ar.append(1)
    # Add blank values to the array as placeholders

    # print(ar)

    for c in range(n+1):
        ar[c] = combination(n, c)
    # For each value in the array combign it with the row  number and use the factorial funtion.

    print('')
    print('')
    print('-------------------------------------------')
    print('The values of row ', n, ' are bellow.')
    print(ar)
    print('Thank you for using my script. -Max')
    print('Credit To Chandra Hull For The Help!')
    print('-------------------------------------------')
    print('')
    print('')

    # Driver Code
