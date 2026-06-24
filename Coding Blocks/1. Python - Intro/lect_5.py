
"""
sum of digits of a number
"""

num = int(input("Enter a number: "))
sum = 0
while num != 0:
    digit = num % 10
    sum += digit
    num //= 10
print("Sum of digits:", sum)

# OR
num = input("Enter a number: ") ## keep it string to iterate over it
sum = 0
for digit in num:
    sum += int(digit) # convert the digit to int before adding it to sum
print("Sum of digits:", sum)

# OR using map
num = input("Enter a number: ")
sum = sum(map(int, num)) # map(int, num) will convert each character in the string num to an integer, and then sum() will add them up.
print("Sum of digits:", sum)

"""
Reverse a number

eg. 123 -> 321
3*10
3*10 + 2 = 32
32*10
32*10 + 1 = 321
"""
num = int(input("Enter a number: "))
rev = 0
while num != 0:
    digit = num % 10
    rev = rev * 10 + digit
    num //= 10
print("Reversed number:", rev)


# OR - read a string and then reverse it using slicing
num = input("Enter a number: ")
rev = num[::-1] # slicing to reverse the string # also can use reversed() function and join() to reverse the string
# strings are immutable in python, so we cannot change the original string, but we can create a new string that is the reverse of the original string.
# num and rev don't have the same string object in memory, they are different objects. num is the original string, and rev is the new string that is the reverse of num.
print("Reversed number:", rev) # remember that rev is a string here, if you want it as an integer, you can convert it using int(rev)

# if you don't want to create a new object rev, and just copy num and print the reverse of num, you can do it like this:
num = input("Enter a number: ")
print("Reversed number:", num[::-1]) # slicing to reverse the string   

"""
Fibonacci series - Given a non-negative integer n, find the nth Fibonacci number. The Fibonacci numbers are the numbers in the following integer sequence.
0, 1, 1, 2, 3, 5, 8
The sequence starts with 0 and 1, and each subsequent number is the sum of the previous two numbers. 
That is, fib(0) = 0, fib(1) = 1, and fib(n) = fib(n - 1) + fib(n - 2
for n > 1.
This is an important problem in coding interviews, and is a good example of dynamic programming and also used in algorithm design, recursion.
So has a lot of applications in real life, like in nature, computer science, and mathematics.

Logic:
if n == 0, we know it's 0
if n == 1, we know it's 1
so for 0 and 1, we can return the value directly.
For n > 1, we can use a loop to calculate the Fibonacci number iteratively.
2nd fibonacci number is 1, 3rd is 2, 4th is 3, 5th is 5, 6th is 8, and so on.
we can use two variables a & b to keep track of the previous two Fibonacci numbers, and update them in each iteration of the loop.
The loop needs to run n-1 times, because we already know the first two Fibonacci numbers.

"""
n = int(input("Enter a number: "))
if n == 0 or n == 1:
    print(n)
else:
    a, b = 0, 1
    for i in range(2, n + 1):
        c = a + b
        a = b
        b = c
    print(b)
    
# OR
n = int(input("Enter a number: "))
a, b = 0, 1
for i in range(n):
    a, b = b, a + b
print(a) # a will be the nth Fibonacci number after the loop ends

# OR
n = int(input("Enter a number: "))
if n == 0:
    print(0)
elif n == 1:
    print(1)
else:
    a = 0
    b = 1
    i = 1
    while i <= n - 1:
        c = a + b
        a = b
        b = c
        i += 1
    print(c) # c will be the nth Fibonacci number after the loop ends

# Time complexity: O(n) - because the loop runs exactly n times
# Space complexity: O(1) - we are using constant space, only a few variables to keep track of the previous two Fibonacci numbers

"""
Largest of N numbers - 
"""
num = 

