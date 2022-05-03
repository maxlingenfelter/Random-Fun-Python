import numpy as np
import statistics
import math

run = 1
while run == 1:
    n = int(input("Pick a line number? >>>"))

    # Define factorial

    def factorial(a):
        Prod = 1
        for j in range(1, a+1):
            Prod = j*Prod
        return Prod


    # Define Combination
    def combination(n, m):
        Choose = factorial(n)/(factorial(n-m)*factorial(m))
        print("Choose = "+str(factorial(n))+"/"+str((factorial(n-m)*factorial(m))))
        return Choose

    # For example, to find the 4th number(3rd position in Python) on the 7th row we would say:
    # print("Combination of row", 7, "and position", 3, "is", combination(7, 3))

    array = []

    length = len(array)

    len2 = n+1
    for c in range(len2):
        array.append(1)
    # Add blank values to the arrayray as placeholders

    # print(array)

    for c in range(n+1):
        array[c] = combination(n, c)
    # For each value in the arrayray combign it with the row  number and use the factorial funtion.

    print('')
    print('')
    print('-------------------------------------------')
    print('The values of row ', n, ' arraye bellow.')
    print(array)
    print('-------------------------------------------')
    print('')
    print('')

    # Driver Code
