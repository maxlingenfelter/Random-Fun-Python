import random
rolls = int(input("How many dice would you like to roll?"))

while rolls > 0:
    posiblle_results = [1, 2, 3, 4, 5, 6]
    result = random.choice(posiblle_results)
    #print("Result of dice rolling is : " + str(result))
    rolls = rolls-1
    print("Result > " + str(result))
