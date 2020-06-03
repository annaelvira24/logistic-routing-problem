
from loadFiles import *
from mtsp import *

def askMethod():
    method = 0
    while(not(method == '1' or method == '2')):
        print("Which method do you prefer?")
        print("1. Original Branch and Bound")
        print("2. Optimized with MIP library")
        method = str(input())
        if(not(method == '1' or method == '2')):
            print("Please enter a valid number")

    return method

print("=========================LOGISTIC ROUTING SOLVER======================")
exit = False
while(not exit):
    print("Please choose the city")
    print("1. Oldenburg")
    print("2. San Francisco")
    print("Type 'EXIT' to quit the program")
    choice = str(input())

    if(choice == '1'):
        print("--------------WELCOME TO OLDENBURG!------------------")
        print()
        method = askMethod()
        mtsp(loadNodes('../map/OLNodes.txt'), loadEdges('../map/OLEdges.txt'), method)

    elif(choice == '2'):
        print("--------------WELCOME TO SAN FRANSISCO!------------------")
        print()
        method = askMethod()
        mtsp(loadNodes('../map/SFNodes.txt'), loadEdges('../map/SFEdges.txt'), method)
        
    elif(choice.upper() == "EXIT"):
        print("Good Bye")
        exit = True
    else:
        print("Please enter a valid number")
    
    print()



