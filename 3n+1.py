import math
n = int(input("Pick a number? >>>"))
runtimes = 0


while n != 1:
    if n % 2 == 0:
        print("Even")
        n = n/2
        print(n)
        if n == 1:
            break
        runtimes = runtimes + 1
        # input()

    if n % 2 == 1:
        print("Odd")
        n = (3 * n) + 1
        print(n)
        if n == 1:
            break
        runtimes = runtimes + 1
        # input()

print('Times Checked.')
print(runtimes)
# print(runtimes)
