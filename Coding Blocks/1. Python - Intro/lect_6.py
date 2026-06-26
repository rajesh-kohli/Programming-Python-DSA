"""
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5

Same pattern as right angle triangle of stars, meaning the loop condition will stay the same
Except what we are going to print
"""
num = int(input("Enter a number:"))

for i in range(1, num+1):
    for j in range(1,i+1):
        print(j,end = " ")
    print()
print()

## While loop
i = 1
while i<=num:
    j = 1
    while j <= i:
        print(j, end = " ")
        j = j + 1
    i = i + 1
    print()
print()

## in the above approach, we are also using the same loop variable j to print as well
## Another strategy is to have a separate variable for printing and 
# use i & j only for iterating and controling the loop
# This approach would be useful in the future patterns

## While loop with a separate variable to print

num = int(input("Enter a number:"))
i = 1
# for the ith row, print i numbers starting from 1 in the increasing order
while i<=num:
    # for the ith row, print i numbers starting from 1 in the increasing order
    j = 1
    n = 1
    while j <= i:
        print(n, end = " ")
        j = j + 1
        n = n + 1
    i = i + 1
    print()
print()

"""
Output:
        1 
        1 2 
        1 2 3 
        1 2 3 4 
        1 2 3 4 5 
"""

# Pattern

"""
1
2 3
4 5 6
7 8 9 10

## Here we can clearly see the pattern for this question also matches with the previous question
and the right angled triangle of stars
# that means the loop condition is going to be the same, except what we are going to print
"""

n = 5
i = 1
num = 1 #we just moved this number outside, because we only want it to initialize once, not reset every time and this ensures the updates from the previous rows carry forward to the next row       
while i <= n:
    j = 1
    while j <= i:
        print(num, end = " ")
        j = j + 1
        num = num + 1
    i = i + 1
    print()
print()

"""
1 
2 3 
4 5 6 
7 8 9 10 
11 12 13 14 15 
"""

"""
Pattern
1
0 1
1 0 1
0 1 0 1
1 0 1 0 1

Same, the pattern is the same as previous questions, only the values we print are different
# Here we notice, when it's an even row, it starts with 0 and odd rows begin with 1 - we can use index starting with 1 for that
# And here the numbers are only 1's and 0's - need to keep flipping between 1 and 0 in row
# we can flip numbers either using num = ! num OR num = 1 - num (will be used frequently)
If else is another way but not used as often:
if num == 0:
    num = 1
else:
    num = 0

Mostly use num = 1 - num for swapping numbers
"""
n = int(input())

i = 1

while i <= n:
    # if i % 2 == 0:
    #     num = 0
    # else:
    #     num = 1
    num = 0 if i % 2 == 0 else 1
    j = 1
    while j <= i:
        print(num, end = " ")
        num = 1 - num
        j = j + 1
    i = i + 1
    print()
    
"""
Output:

1 
0 1 
1 0 1 
0 1 0 1 
1 0 1 0 1 
"""
"""
Pattern:
        1 
      2 3 
    3 4 5 
  4 5 6 7 
5 6 7 8 9 

Everything is straight forward here, except one thing to note in particular:
Everytime you're at the ith row, you need to start printing the numbers starting with i in increasing order

"""
  
n = int(input())

for i in range(1, n + 1):
    # for the ith row print n-i space
    for _ in range(n - i):
        print(" ", end=" ")

    # followed by i nos. starting with i in inc. order
    num = i
    for _ in range(i):
        print(num, end=" ")
        num = num + 1

    print()
    
"""

        1
      2 3 2
    3 4 5 4 3
  4 5 6 7 6 5 4
5 6 7 8 9 8 7 6 5


"""

num = int(input("Enter a number: "))
n = 0

for i in range(1, num+1):
    for j in range(num-i):
        print(" ", end = " ")
    for k in range(i):
        n = n + 1
        print(n, end = " ")
    for l in range(i-1):
        n = n - 1
        print(n, end = " ")
    print()
print()

"""
Output:
        1 
      2 3 2 
    3 4 5 4 3 
  4 5 6 7 6 5 4 
5 6 7 8 9 8 7 6 5 
"""


num = int(input("Enter any postive odd number:"))

for i in range(1,num+1):
    if i <= (num//2):
        print("* " * i, end = " ")
    else:
        print("* " * (num - i + 1, end = " "))
    print()
print()
    

