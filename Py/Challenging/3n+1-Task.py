# Creation Date:  04/13/2022
# Run: python 3n+1-Task.py
# Description: This program is written for the AP Computer Science Principles Performance Task.
# The Collatz Conjecture is a formula that states if the number is even divide it by 2. If it's odd, multiply it by 3 and add 1.
# The porgram will evaluate the stopping time (the number of steps required for the new calculated number to be less than the original) 
# and highest number of a given range of values based on user input. The input requested by the user is the range of values the program
# will evaluate starting from 1 and going to the number the user has provided.
# At the end of the program a table will displayed that contains the orginal number, highest number, stopping time and total stopping time 
# of each evalutated number.


# Install these packages:
# pip install tabulate
# pip install matplotlib
# pip install numpy

# Add all needed imports
from matplotlib.pyplot import plot, draw, show
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import random

# DEFINING THE FUNCTIONS
def rannum(): 
    return random.randint(0, 255) # Generate a random number between 0 and 255

def ranhex(): 
    nums=(rannum(), rannum(), rannum()) # Make a pair of three random numbers
    hex =  '#%02X%02X%02X' % nums # Convert the numbers to hexadecimal
    return hex

def even(x):  # Define the actions if the value is even
    x = x/2  # Divide the number by 2
    array.append(x)  # Add the new number to the array
    return x  # Return the new number

def odd(x):  # Define the actions if the value is odd
    x = (x*3)+1  # Multiply the number by 3 and add 1
    array.append(x)  # Add new number to the array
    return x  # Return the new number

def findStopTime(array): # Finds the stopping time of the array
    global stoppingtime # Define the global variable for stoppingtime
    stoppingtime = 0 # Define the global variable as 0 to start, this is needed because otherwise the value will be "None" if no stoppingtime is found
    for num in array: #For each number in the array from first to last
        if num < array[0]: # If the number is less than the first number in the array
            if stoppingtime == 0: # If the current stopping time is 0
                stoppingtime = array.index(num) # Defines stopping time as the postion of the first number lower than the orginal number in the array.

def evenOdd(number): # The funtion the is used to determine if the number is even or odd and them trigger the corrispoinding function.
    if number % 2 == 0:
        even(number) # See above description
    else:
        odd(number)  # See above description
        
# END OF DEFINING THE FUNCTIONS


run = 1  # Creates a variable that can be used to make an infinite loop.
while run == 1:  # This is the loop that keeps the program running.
    datas = []     # Creates an empty list that will later be used to store data thats printed as a table at the end of the program.

    inputnum = int(input("Please enter a starting number: ")) # The starting number also wraped in a paramater to make it only work if the input is an integer.

    if not inputnum > 1:  # Make sure the number is greater than 1.
        # If the user does not enter a number greater than 1, the program will return this message.
        print("Please enter a number greater than 1 for the program to run.")
    
    for i in range(1, inputnum+1): # For each number in the range of 1 to the number the user has provided.
        
        n = i # Define the variable n as the current number in the loop.
        
        array = [] # Creates an empty array that will be used to store the numbers that are tested.
        
        array.append(n) # Pushes the starting number into the array.
        
        ornum = n # Define the original number inputted by the user, this is referenced at the end when logging the output and is not changed during the program.
        
        highnum = n # Define the highest number as the inputted number, this is later changed if a higher number is found throughout the program.
                
        output = 1 # Define the variable that will be used to determine if the program should output the results.

        count = 0  # global variable

        while n > 1:  # Does not run the formula if the defined number is less than 2.
            evenOdd(n) # See above description
            n = array[-1] # Defines the new variable n as the last number in the array.

        findStopTime(array) # See above description
        highnum = max(array) # Finds the highest number in the array.
        data = [[ornum, highnum,  stoppingtime, len(array)-1]] # Creates a list that will be used to store the data that will be printed as a table at the end of the program.
        # Plotting Graph
        x = np.arange(0, len(array)) # Defines the x axis of the graph as steps taken during the program.
        y = np.array(array) # Defines the y axis of the graph as the numbers that are tested.
        plt.title("Collatz Conjecture For Number " + str(ornum)) # Title of the graph.
        plt.xlabel("Steps") # Label of the x axis.
        plt.ylabel("Numbers") # Label of the y axis.
        plt.plot(x, y, ranhex()) # Plots the graph.
        plt.draw() # Draws the graph.
        datas.append(data[0]) # Adds the table data to the existing array that will be printed at the end.
        print (array) # Prints the array of numbers that were tested. (This can be commented out to increase calculation speed its simpliy so the user can see the numbers being tested) 

    print('') # Create padding
    print('') # Create padding
    print(tabulate(datas, headers=["Orginal Number", "Highest Number", "stopping Time", "Total stopping Time"])) # Prints the table of all data for orginal number, highest number, stopping time and total stopping time
    print('')# Create padding
    print('')# Create padding
    plt.show() # Displays the interactive grapgh to the user 
