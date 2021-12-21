import numpy as np
import statistics
import math

run = 1

while run == 1:
    print('1. Basic')
    print('2. Even')
    print('3. Odd')

    type = int(input("Type Of Summ? >>>"))

    if type == 1:
        i = int(input("Start Value? >>>"))
        k = int(input("Number Of Loops >>>"))
        out2 = 0

        for i in range(i, k+1):
            x = i
            out = x
            print(out)

            out2 = out2 + out
        print('Output =', out2)

    if type == 2:
        i = int(input("Start Value? >>>"))
        k = int(input("Number Of Loops >>>"))
        out2 = 0

        for i in range(k):
            x = i
            out = 2 * x
            print(out)

            out2 = out2 + out
        print(' ')
        print('Output =', out2)
        print(' ')

    if type == 3:
        i = int(input("Start Value? >>>"))
        k = int(input("Number Of Loops >>>"))
        out2 = 0

        for i in range(k):
            x = i
            out = (2 * x) + 1
            print(out)

            out2 = out2 + out
        print(' ')
        print('Output =', out2)
        print(' ')
