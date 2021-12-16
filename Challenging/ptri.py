import numpy as np
import statistics
import math


# def factorial(n):
#     # single line to find factorial
#     return 1 if (n == 1 or n == 0) else n * factorial(n - 1)


run = 1
while run == 1:
    n = int(input("Pick a line number? >>>"))
    max = n+1/2

    a = np.array([])

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
        return Choose

    # For example, to find the 4th number(3rd position in Python) on the 7th row we would say:
    print("Combination of row", n, "and position", 3, "is", combination(n, 3))

    length = len(a)

# Driver Code
