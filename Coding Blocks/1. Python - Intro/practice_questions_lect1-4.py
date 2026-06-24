"""
These are all the practice questions from the first 4 lectures 
(Flowcharts, Pseudocode, Intro/Syntax) of the DSA Coding Blocks.
"""

# Largest of three numbers
x,y,z = map(int, input("Enter three numbers: ").split())

if x > y and x > z:
    print(f"{x} is the largest")
elif y > x and y > z:
    print(f"{y} is the largest")
else:
    print(f"{z} is the largest")    
    

"""
Given two numbers say a and b, design an algorithm 
to print the following series [a+b, a+2*b, a+3*b]
"""
a, b = map(int, input("Enter two numbers: ").split())
for i in range(1, 4):
    print(a + i * b, end=" ")   # sep is between the printed values. end is after the entire printed line.

"""
Given a positive number n , design an algorithm to 
print the first n natural numbers
"""
num = int(input("Enter a number: "))
for i in range(1, num+1):
    print(i, end=" ")
    

"""
Print Even Numbers 
Given a positive number n , 
design an algorithm to print all the even numbers from 2 to n
"""
num = int(input("Enter a number: "))

for i in range(2, num+1, 2):
    print(i, end=" ")

"""
Sum of Natural Numbers 
Given a positive number n , 
design an algorithm to compute the sum of first n natural numbers
"""
num = int(input("Enter a number: "))
sum = 0
for i in range(1, num+1):
    sum += i
print(f"The sum of first {num} natural numbers is {sum}")

"""
Sum of Numbers 
Given a positive number n followed by n integer values
design an algorithm to find the sum of  n numbers
Example:
Input : n = 5 ; [ 10, 20, 30, 40, 50 ] 
Output : 150 
Explanation : 10+20+30+40+50 = 150
"""
num = int(input("Enter a number: "))
sum = 0
for i in range(num):
    sum += int(input("Enter a number: "))
print(f"The sum of the {num} numbers is {sum}")

"""
Prime Number Check
Given a positive number n,
design an algorithm to check if the number is prime
"""


num = int(input("Enter a number: "))

if num < 2:
    print("Not Prime")
else:
    is_prime = True
    for i in range(2, num):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print("Prime")
    else:
        print("Not Prime")

## Now do it with a while loop where you check for factors from
# 2 to sqrt(n) and break if you find one.

num = int(input("Enter a number: "))
if num < 2:
    print("Not Prime")
else:
    i = 2
    is_prime = True
    while i * i <= num: # or i <= int(num**0.5): or i <= math.sqrt(num)
        if num % i == 0:
            is_prime = False
            break
        i += 1
    if is_prime: 
        print("Prime")
    else:
        print("Not Prime")
    
### Now do it with a for loop where you check for factors from 2 to sqrt(n) and break if you find one.

num = int(input("Enter a number: "))
if num < 2:
    print("Not Prime")
else:
    is_prime = True
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            is_prime = False
            break 
    if is_prime: # this means that the loop completed without finding a factor, so the number is prime
        print("Prime")
    else:
        print("Not Prime")


"""
Largest of N numbers 
Given N integer values, design an algorithm to 
find the largest of the N numbers
"""

maxsofar = float('-inf') # or you can use max_so_far = None and then check if max_so_far is None before updating it
num = int(input("Enter a number: "))
for i in range(num):
    val = int(input("Enter a number: "))
    if val > maxsofar:
        maxsofar = val
print(f"The largest of the {num} numbers is {maxsofar}")
    
"""
Printing Stars
Given a positive number N,
design an algorithm to print N stars
Example Input : N = 3
  Output :
*  *  *
"""
num = int(input("Enter a number: "))
for i in range(num):
    print("*", end=" ") 


num = int(input("Enter a number: "))
for i in range(num):
    print("* " * num)  # prints a square of stars
    
for i in range(num):
    print("* " * (num - i))  # prints an inverted right-angled triangle of stars

for i in range(num):
    print("* " * (i + 1))  # prints a right-angled triangle of stars
    
for i in range(num):
    print(" " * (num - i - 1) + "*" * (i + 1))  # prints a right-angled triangle of stars aligned to the right

for i in range(num):
    print(" " * i + "*" * (num - i))  # prints an inverted right-angled triangle of stars aligned to the right

for i in range(num):
    print(" " * (num - i - 1) + "*" * (2 * i + 1))  # prints a pyramid of stars

for i in range(1, num+1):
    print(" " * (num-i) + "*" * (2 * i - 1))  # prints a pyramid of stars as well
    
for i in range(num):
    print(" " * i + "*" * (2 * (num - i) - 1))  # prints an inverted pyramid of stars
    
"""
Now do these stars patterns with multiple for loops, 
where you have one for loop for the spaces and one for loop for the stars.
"""
num = int(input("Enter a number: "))

# square of stars with multiple for loops

for i in range(num): ## no need for num + 1 here because we are not using the index for anything, just to repeat the loop num times
    for j in range(num):
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars


# right-angled triangle of stars with multiple for loops

for i in range(num):
    for j in range(i + 1): # here we are using index value to print the correct number of stars in each row
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars

for i in range(1, num+1):
    for j in range(1, i+1):
        print("*", end=" ")

#using while loop

i = 1
while i <= num:
    # for the ith row, print i stars
    j = 1
    while j <= i:
        print("*", end=" ") # by default print function goes to the next line after printing the value, so we use end=" " to print the stars without a new line
        j += 1
    print()
    i += 1

# inverted right-angled triangle of stars with multiple for loops

for i in range(num):
    for j in range(num - i): # here we are using index value to print the correct number of stars in each row
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars  


# right-angled triangle of stars aligned to the right with multiple for loops

for i in range(num):
    for j in range(num - i - 1): # print spaces
        print(" ", end=" ")
    for k in range(i + 1): # print stars
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars

# inverted right-angled triangle of stars aligned to the right with multiple for loops

for i in range(num):
    for j in range(i): # print spaces
        print(" ", end=" ")
    for k in range(num - i): # print stars
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars

# Pyramid of stars with multiple for loops

for i in range(1, num+1): 
    for j in range(num-i):
        print(" ", end=" ") # print spaces and end with a space or can also do print(" ", end="") for single space
    for k in range(2*i-1):
        print("*", end=" ") # print stars with spaces or can also do print("*", end="") and this won't have spaces between stars
    print() # this print() is to move to the next line after printing each row of stars

# inverted pyramid of stars with multiple for loops

for i in range(num):
    for j in range(i):
        print(" ", end=" ") # print spaces and end with a space or can also do print(" ", end="") for single space
    for k in range(2*(num - i) - 1):
        print("*", end=" ") # print stars with spaces or can also do print("*", end="") and this won't have spaces between stars
    print() # this print() is to move to the next line after printing each row of stars


##  "butterfly pattern (upper half)" — also called "mirror triangles" or "double right-angled triangle"
for i in range(1, num+1):
    for j in range(i):
        print("*", end=" ")
    for k in range(2*(num-i)):
        print(" ", end=" ")
    for l in range(i):
        print("*", end=" ")
    print() # this print() is to move to the next line after printing each row of       
    
# this is a more compact way to do the butterfly pattern (upper half)

for i in range(1, num+1):
    print("* " * i + "  " * (num - i) * 2 + "* " * i) 

# inverted butterfly pattern (lower half)   
for i in range(num):
    print("*" * (num - i) + " " * (2 * i) + "*" * (num - i))  # this is a more compact way 
    
# inverted butterfly pattern (lower half) with multiple for loops
for i in range(num):
    for j in range(num - i):
        print("*", end=" ")
    for k in range(2 * i):
        print(" ", end=" ")
    for l in range(num - i):
        print("*", end=" ")
    print() # this print() is to move to the next line after printing each row of stars
    
# inverted butterfly pattern (lower half) compact
for i in range(num):
    print("* " * (num - i) + "  " * i * 2 + "* " * (num - i)) ## notice the diff on line 263 and 277 - both do the same thing but this one makes it more visual with spaces
    

"""
print the below pattern
N = 5
1
0 1
1 0 1
0 1 0 1
1 0 1 0 1
""" 


