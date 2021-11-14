temp = int(input("Pick a tempature? >>>"))
fc = input("What unit are you starting with (F or C)>>>")
c = 0
f = 0

if fc == 'F':
    f = temp
    c = (f - 32) * 5/9
    print("Degrees Celsius")
    print(c)

if fc == 'C':
    c = temp
    f = (c * 9/5) + 32
    print("Degrees Fahrenheit")
    print(f)
