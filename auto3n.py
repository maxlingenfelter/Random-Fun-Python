import math
import time
run = 1
runnumn = 295147905179352825856


while run == 1:
    runnumn = runnumn + 1
    n = runnumn
    ornum = n
    highnum = n
    runtimes = 0

    while n != 1:

        if n > highnum:
            highnum = n

        if n % 2 == 0:
            print("Even")
            n = n/2
            print(n)
            runtimes = runtimes + 1
            if n == 1:
                break
            # input()

        if n % 2 == 1:
            print("Odd")
            n = (3 * n) + 1
            print(n)
            runtimes = runtimes + 1
            if n == 1:
                break
            # input()

    runtimes = runtimes + 1
    print('')
    print('')
    print('-------------------------------------------')
    print('Original Number > ' + str(ornum))
    print('Highest Number Reached > ' + str(highnum))
    print('Times Checked > ' + str(runtimes))
    print('-------------------------------------------')
    print('')
    print('')
    time.sleep(.45)


# print(runtimes)
