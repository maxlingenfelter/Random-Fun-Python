# Lol no imports

while True:
    print('1. Basic')
    print('2. Even')
    print('3. Odd')

    inp = input("Type Of Summ/Exit? >>> ");
    if(inp.lower() == "exit"):
        break

    i = int(input("Start Value? >>> "))
    k = int(input("Number Of Loops >>> "))
    type = int(inp)
    out2 = 0

    match type:
        case 1:
            for i in range(i, k+1):
                x = i
                out = x
                print(out) # These repeated statements could be cut down too but I'm too lazy
                out2 = out2 + out
        case 2:
            for i in range(k):
                x = i
                out = 2 * x
                print(out)
                out2 = out2 + out
        case 3:
            for i in range(k):
                x = i
                out = (2 * x) + 1
                print(out)
                out2 = out2 + out
    
    print(' ')
    print('Output =', out2)
    print(' ')
