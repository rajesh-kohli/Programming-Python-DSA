## Problem Solving:
#Task: Repetitive problem statement
## Two ways to solve it:
# 1. Iterative Approach 2. Recursive Approach
### Task:
# 5 houses and 5 gifts - Santa has to give one gift to each house
# Approach 1: Santa takes the gift and delivers it to each house individually one by one (Repeat 5 times) 
#       --> Conventional --> Iterative --> performed with Loops
# Approach 2: Old Santa hires a manager who then hires 5 different people to deliver at each house
##  Here think of Manager as a function, and we then call the function 5 times with different paramenters
### This is called Recursive approach - where we are calling the same function itself again and again

## Iterative approach: Loop
#### Initialization, Condition, Updation
## Two kinds of loops in Python: For and While

## Initialization --> from where we need to start
## Condition --> upto where we need to go
## Updation  --> no of steps we need to take

# While loop:
# Syntax: 
#     Initialization
#     while condition:
#         stmnts
#         updation

# Example
print("Example 1")
#initialization
i = 1
#condition
while i <= 10:
    print(i)
    #updation
    i+=1

#Example
print("Example 2")
# i = 10
# while i<=10:
#     print(i)
#     i-=1

#Example    
print("Example 3")
i = 1
while i<=10:
    if i%2 == 0:
        print(i)
    else:
        print(i+1)
    i+=1

#Example
print("Example 4")
i = 1
while i<=10:
    if i%3 != 0:
        print(i<<2)
    else:
        print(i>>2)
    i+=2

#Example
print("Example 5")
i = 1
while i<= 15:
    if i%2==0:
        print(i+1<<2)
    else:
        print(3*i<<2)
    i+=3

#Example
print("Example 6")
i=1
while i<=15:
    if i%3==0:
        if i>3:
            print(i*2>>2)
    else:
        print(i*2<<1)
    i+=2

#4,12,20
#Example
print("Example 7")
i = 1
j=1
while i<=10:
    while j<=5:
        print(i+j)
        j+=1
    i+=1

#Example
print("Example 8")
i = 1
j = 1
while i<=20:
    while j<=10:
        if (i+j)%2==0:
            print((i+j)>>2)
        else:
            print((i+j)<<2)
        j+=1
    i+=2

#Example
print("Example 9")
i = 1

while i<=20:
    while j<=10:
        j = 1
        if (i+j)%2==0:
            print((i+j)>>2)
        else:
            print((i+j)<<2)
        j+=1
    i+=2
    print(i)