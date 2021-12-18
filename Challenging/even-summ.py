import numpy as np
import statistics
import math
run = 1

while run == 1:
    i = int(input("Start Value? >>>"))
    k = int(input("Number Of Loops >>>"))
    out2 = 0

    for i in range(k):
        x = i
        out = 2 * x
        print(out)

        out2 = out2 + out
    print('Output =', out2)
