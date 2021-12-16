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

    print("Factorial of", 3, "is", factorial(3))

    # Define Combination

    def combination(n, m):
        Choose = factorial(n)/(factorial(n-m)*factorial(m))
        return Choose

    print("Combination of", 7, "and", 3, "is", combination(7, 3))

    # if n % 2 == 0:
    #     print("Even")
    #     d = len(a)/2
    #     midar = a[d]
    #     print(midar)

    # if n % 2 == 1:
    #     print("Odd")
    #     d = len(a)
    #     midar = d/2
    #     print(midar)

    # END
    # print('END')
    # print(a)
    # print("Factorial of", n, "is", factorial(n))

# Driver Code
