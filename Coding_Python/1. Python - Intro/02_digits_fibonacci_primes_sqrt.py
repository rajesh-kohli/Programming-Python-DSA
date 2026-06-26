###############################################################################
#          Lecture 5 - Loops: Digits, Fibonacci, Primes & Square Root         #
###############################################################################


# =============================================================================
# SECTION 1: Sum of Digits of a Number
# =============================================================================

"""
sum of digits of a number
"""

# ----- Core Idea -----
# To extract digits from a number, we use two operations repeatedly:
#   num % 10   --> gives the LAST digit   (e.g., 1234 % 10 = 4)
#   num // 10  --> removes the LAST digit  (e.g., 1234 // 10 = 123)
#
# ----- Walkthrough -----
# num = 1234, sum = 0
#
# Iteration 1: digit = 1234 % 10 = 4,  sum = 0 + 4 = 4,   num = 1234 // 10 = 123
# Iteration 2: digit = 123 % 10 = 3,   sum = 4 + 3 = 7,   num = 123 // 10 = 12
# Iteration 3: digit = 12 % 10 = 2,    sum = 7 + 2 = 9,   num = 12 // 10 = 1
# Iteration 4: digit = 1 % 10 = 1,     sum = 9 + 1 = 10,  num = 1 // 10 = 0
# num == 0, loop ends. Answer: 10

# Time:  O(d) where d = number of digits in num. Since d = floor(log10(n)) + 1, this is O(log n)
# Space: O(1) — just two variables (sum, digit)
# All three methods below have the same complexity.

# ----- Method 1: Using modulo and integer division -----

num = int(input("Enter a number: "))
sum = 0
while num != 0:
    digit = num % 10    # extract last digit
    sum += digit         # add it to running total
    num //= 10           # chop off last digit
print("Sum of digits:", sum)

# ----- Method 2: Treat the number as a string and iterate over characters -----

# OR
num = input("Enter a number: ")  ## keep it string to iterate over it
sum = 0
for digit in num:               # each 'digit' is a character like '1', '2', etc.
    sum += int(digit)            # convert the digit to int before adding it to sum
print("Sum of digits:", sum)

# ----- Method 3: Using map() for a one-liner -----

# OR using map
num = input("Enter a number: ")
total = sum(map(int, num))  # map(int, num) will convert each character in the string num to an integer, and then sum() will add them up.
print("Sum of digits:", total)

# NOTE: Methods 1 & 2 use 'sum' as a variable name, which shadows Python's
# built-in sum() function. If you run all three methods in sequence, Method 3
# would fail because 'sum' is no longer the built-in function. Use 'total'
# as the variable name (like Method 3 does) to avoid this issue.


# =============================================================================
# SECTION 2: Reverse a Number
# =============================================================================

"""
Reverse a number

eg. 123 -> 321
3*10
3*10 + 2 = 32
32*10
32*10 + 1 = 321
"""

# ----- Core Idea -----
# Build the reversed number digit by digit:
#   1. Extract the last digit of num      (num % 10)
#   2. Append it to rev by:               rev = rev * 10 + digit
#      - rev * 10 shifts existing digits left (makes room)
#      - + digit places the new digit at the ones place
#   3. Remove last digit from num          (num // 10)
#
# ----- Walkthrough -----
# num = 123, rev = 0
#
# Iteration 1: digit = 123 % 10 = 3,  rev = 0*10 + 3 = 3,     num = 12
# Iteration 2: digit = 12 % 10 = 2,   rev = 3*10 + 2 = 32,    num = 1
# Iteration 3: digit = 1 % 10 = 1,    rev = 32*10 + 1 = 321,  num = 0
# Answer: 321

# Time:  O(d) where d = number of digits = O(log n)
# Space: O(1) — just rev and digit variables

# ----- Method 1: Mathematical approach -----

num = int(input("Enter a number: "))
rev = 0
while num != 0:
    digit = num % 10            # extract last digit
    rev = rev * 10 + digit      # build reversed number
    num //= 10                  # remove last digit
print("Reversed number:", rev)

# Time:  O(d) — string slicing creates a new string by visiting each character
# Space: O(d) — the reversed string is a new object of same length

# ----- Method 2: String slicing -----

# OR - read a string and then reverse it using slicing
num = input("Enter a number: ")
rev = num[::-1]  # slicing to reverse the string # also can use reversed() function and join() to reverse the string
# strings are immutable in python, so we cannot change the original string, but we can create a new string that is the reverse of the original string.
# num and rev don't have the same string object in memory, they are different objects. num is the original string, and rev is the new string that is the reverse of num.
print("Reversed number:", rev)  # remember that rev is a string here, if you want it as an integer, you can convert it using int(rev)

# ----- Method 3: Inline reverse without creating new variable -----

# if you don't want to create a new object rev, and just copy num and print the reverse of num, you can do it like this:
num = input("Enter a number: ")
print("Reversed number:", num[::-1])  # slicing to reverse the string

# ----- How does [::-1] work? -----
# Syntax: string[start:stop:step]
# When step = -1, it traverses the string BACKWARDS
# Omitting start and stop means "from end to beginning"
# "hello"[::-1] --> "olleh"


# =============================================================================
# SECTION 3: Fibonacci Series
# =============================================================================

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

# ----- The Fibonacci Sequence -----
#
# Index:  0   1   2   3   4   5   6   7    8    9    10
# Value:  0   1   1   2   3   5   8   13   21   34   55
#
# Each number = sum of the two before it
# fib(n) = fib(n-1) + fib(n-2)
#
# ----- Core Idea (Iterative) -----
# Keep TWO variables (a, b) representing consecutive Fibonacci numbers.
# In each step, compute the next one and shift the window forward:
#
#   Before:  a = fib(k),   b = fib(k+1)
#   Compute: c = a + b     (this is fib(k+2))
#   Shift:   a = b,  b = c
#   After:   a = fib(k+1), b = fib(k+2)
#
# ----- Walkthrough for n=6 -----
#
# Start: a=0, b=1
# i=2: c = 0+1 = 1,  a=1, b=1     (fib(2) = 1)
# i=3: c = 1+1 = 2,  a=1, b=2     (fib(3) = 2)
# i=4: c = 1+2 = 3,  a=2, b=3     (fib(4) = 3)
# i=5: c = 2+3 = 5,  a=3, b=5     (fib(5) = 5)
# i=6: c = 3+5 = 8,  a=5, b=8     (fib(6) = 8)
# Answer: c = 8

# ----- Method 1: Explicit with base case check -----

n = int(input("Enter a number: "))
if n == 0 or n == 1:
    print(n)
else:
    a, b = 0, 1
    for i in range(2, n + 1):      # run (n-1) times
        c = a + b                   # next Fibonacci number
        a = b                       # shift window
        b = c
    print(c)

# ----- Method 2: Pythonic with tuple unpacking (most elegant) -----

# OR
n = int(input("Enter a number: "))
a, b = 0, 1
for i in range(n):
    a, b = b, a + b    # simultaneous assignment: a becomes old b, b becomes old a + old b
print(a)  # a will be the nth Fibonacci number after the loop ends

# How does `a, b = b, a + b` work?
# Python evaluates the RIGHT side first (using old values), then assigns.
# It's equivalent to: temp = a + b,  a = b,  b = temp
# This avoids needing a third variable 'c'.
#
# Trace for n=6:
#   Start:  a=0, b=1
#   i=0:    a=1, b=0+1=1     (a is now fib(1))
#   i=1:    a=1, b=1+1=2     (a is now fib(2))
#   i=2:    a=2, b=1+2=3     (a is now fib(3))
#   i=3:    a=3, b=2+3=5     (a is now fib(4))
#   i=4:    a=5, b=3+5=8     (a is now fib(5))
#   i=5:    a=8, b=5+8=13    (a is now fib(6))
#   print(a) = 8  ✓

# ----- Method 3: While loop version -----

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
    print(c)  # c will be the nth Fibonacci number after the loop ends

# Time complexity: O(n) - because the loop runs exactly n times
# Space complexity: O(1) - we are using constant space, only a few variables to keep track of the previous two Fibonacci numbers


# =============================================================================
# SECTION 4: Largest of N Numbers
# =============================================================================

"""
Largest of N numbers
We can assign a variable msf (max so far) = -infinity , we can use math module in python to assign infinity to a variable. import math
We can assign negative infinity in two ways: - math.inf or float('-inf')
Then we can use a loop to iterate over the numbers, and if the current number is greater than msf, we can update msf to the current number.
"""

# ----- Core Idea -----
# Start with the smallest possible value (negative infinity).
# Compare every number against it - if bigger, update.
# At the end, you have the largest.
#
# ----- Why -infinity and not 0? -----
# If all numbers are negative (e.g., [-5, -3, -1]), starting with 0 would
# give the wrong answer (0 > all of them). Starting with -infinity ensures
# ANY number will be larger.
#
# ----- Walkthrough -----
# nums = [3, 7, 2, 9, 1], msf = -inf
#
# num=3: 3 > -inf? YES  --> msf = 3
# num=7: 7 > 3?    YES  --> msf = 7
# num=2: 2 > 7?    NO   --> msf = 7
# num=9: 9 > 7?    YES  --> msf = 9
# num=1: 1 > 9?    NO   --> msf = 9
# Answer: 9

# Time:  O(n) — single pass through n numbers
# Space: O(n) for Method 1 & 2 (storing nums as a list), O(1) for Method 3 (reads one at a time)

# ----- Method 1: Using if comparison -----

import math
nums = list(map(int, input("Enter numbers separated by space: ").split()))
msf = float("-inf")  # msf is the maximum so far, and we are using float to represent infinity
for num in nums:
    if num > msf:
        msf = num
print("Largest number:", msf)

# ----- Method 2: Using built-in max() -----

# OR
import math
nums = list(map(int, input("Enter numbers separated by space: ").split()))
msf = float("-inf")
for num in nums:
    msf = max(msf, num)     # max() returns the larger of the two arguments
print("Largest number:", msf)


# ----- Infinity in Python: Different Ways -----

"""
-2^31 (Int Min) to 2^31-1 (Int Max) are the range of integers in python
-2^63 (Long Min) to 2^63-1 (Long Max) are the range of long in python aka LLong-Min and LLong-Max
We can use Int min/max or Long min/max when we need to find integers or longs in a range, and the problem statement specifically asks for integers and longs, and not floats.
In python, we can use sys module to get the maximum integer and the minimum integer in the range.
sys.maxsize is the maximum long in the range, and sys.maxint is the maximum integer in the range
So we can use sys.maxsize and sys.maxint to find the largest number in the range
if the range is empty, it will return positive infinity
To get negative infinity, we can use -sys.maxsize -1 (calculates as -(2^63-1) - 1 = -2^63)
-2^31 to 2^31-1 are the range of int in python
-2^63 to 2^63-1 are the range of long in python aka LLong-Min and LLong-Max
We can use Int min/max or Long min/max when we need to find integers or longs in a range, and the problem statement sepcifically asks for integers and longs, and not floats.
Use the sys module when you need integers - otherwise use -math.inf and math.inf or float('-inf') and float('inf')
"""

# ----- Quick Reference for Infinity -----
#
# | What you need         | How to write it            |
# |-----------------------|----------------------------|
# | + infinity (float)    | float('inf') or math.inf   |
# | - infinity (float)    | float('-inf') or -math.inf |
# | Max integer (sys)     | sys.maxsize  (2^63 - 1)    |
# | Min integer (sys)     | -sys.maxsize - 1  (-2^63)  |
#
# Use float('inf') / float('-inf') for general comparisons.
# Use sys.maxsize when the problem specifically asks for integer bounds.

# ----- Method 3: Reading numbers one at a time -----

n = int(input())  ## let's say n = 5 meaning we will get 5 integer values from the user
max_so_far = float("-inf")
for _ in range(n):
    num = int(input())  # Here we get 5 integer values from the user
    if num > max_so_far:
        max_so_far = num
    #max_so_far = max(max_so_far, num)
print(max_so_far)


# =============================================================================
# SECTION 5: Controlling Loops - break, continue, pass
# =============================================================================

"""_Controlling Loops in Python_
    - Break statement: used to prematurely exit a loop
    - Continue statement: used to skip the rest of the current iteration and move to the next iteration
    - Pass statement: used to do nothing in a loop
"""

# ----- break -----
# Immediately EXIT the loop. Code after the loop continues.
#
# ----- Analogy -----
# break    = "I'm done, leave the room"
# continue = "Skip this one, move to the next"
# pass     = "Do nothing" (placeholder for empty blocks)

# ----- Example: Count numbers until negative is entered -----
# Time:  O(k) where k = number of inputs before the sentinel value
# Space: O(1)

cnt = 0
while True:                            # infinite loop
    num = int(input("Enter a number: "))
    if num < 0:
        break                           # exit loop when negative number entered
    cnt += 1
print("Total number of numbers entered:", cnt)

# OR
cnt = 0
while True:
    num = int(input("Enter a number: "))
    if num == 0:
        break                           # exit loop when 0 is entered
    cnt += 1
print("Total number of numbers entered:", cnt)

## When you encounter a break statement, the loop is immediately terminated, and the program continues with the next statement after the loop.
# You only break out of the innermost loop you're in.


# =============================================================================
# SECTION 6: Check if a Number is a Fibonacci Number
# =============================================================================

"""
Check Fibonacci Number
Output should be True or False
Start generating the Fibonacci sequence until the nth Fibonacci number is greater than the number you entered.
As long as the Fibonacci number is less than the number you entered, keep generating the Fibonacci sequence.
And if the Fibonacci number is greater than the number you entered, stop generating the Fibonacci sequence.
"""

# ----- Core Idea -----
# Generate Fibonacci numbers one by one.
# If we hit the target exactly --> True (it IS a Fibonacci number)
# If we overshoot (Fibonacci > target) --> False (we passed it, so it's not one)
#
# ----- Walkthrough: Is 8 a Fibonacci number? -----
# Sequence: 0, 1, 1, 2, 3, 5, 8 --> YES, we hit 8 exactly!
#
# a=0, b=1
# c = 0+1 = 1  --> 1 < 8, keep going.   a=1, b=1
# c = 1+1 = 2  --> 2 < 8, keep going.   a=1, b=2
# c = 1+2 = 3  --> 3 < 8, keep going.   a=2, b=3
# c = 2+3 = 5  --> 5 < 8, keep going.   a=3, b=5
# c = 3+5 = 8  --> 8 == 8, print True, break!
#
# ----- Walkthrough: Is 6 a Fibonacci number? -----
# Sequence: 0, 1, 1, 2, 3, 5, 8 --> jumped from 5 to 8, skipped 6. NO!
#
# a=0, b=1
# c=1 < 6, c=2 < 6, c=3 < 6, c=5 < 6, c=8 > 6 --> print False, break!

# Time:  O(n) — generates Fibonacci numbers up to n; the k-th Fibonacci number
#         grows exponentially, so we reach n in about O(log_phi(n)) ≈ O(log n) steps.
#         But thinking simply: at most proportional to n steps.
# Space: O(1) — only 3 variables (a, b, c)

n = int(input("Enter a number: "))
if n == 0 or n == 1:
    print(True)             # 0 and 1 are both Fibonacci numbers
else:
    a = 0  # 0th Fibonacci number
    b = 1  # 1st Fibonacci number
    while True:
        c = a + b
        if c == n:
            print(True)
            break
        elif c > n:
            print(False)
            break
        else:
            a = b
            b = c


# =============================================================================
# SECTION 7: Check Prime Number
# =============================================================================

"""
Check Prime Number
"""

# ----- What is a Prime Number? -----
# A number greater than 1 that has NO divisors other than 1 and itself.
# Examples: 2, 3, 5, 7, 11, 13, 17, 19, 23, ...
# Non-primes (composite): 4=2x2, 6=2x3, 9=3x3, 10=2x5, ...
#
# ----- Why check only up to sqrt(n)? -----
# If n has a divisor d, then n/d is also a divisor.
# One of d or n/d must be <= sqrt(n).
# So if no divisor is found up to sqrt(n), there won't be one above it either.
#
# Example: n = 36
#   Divisor pairs: (1,36), (2,18), (3,12), (4,9), (6,6)
#   sqrt(36) = 6. Every pair has at least one number <= 6.
#   So checking 2 to 6 is enough!
#
# ----- Walkthrough: Is 13 prime? -----
# sqrt(13) ≈ 3.6, so check divisors 2 and 3 only.
# 13 % 2 = 1 (not divisible)
# 13 % 3 = 1 (not divisible)
# i=4, 4 > 3.6, loop ends --> prime!
#
# ----- Walkthrough: Is 12 prime? -----
# sqrt(12) ≈ 3.46
# 12 % 2 = 0 (divisible!) --> not prime, break immediately.

# Time:  O(sqrt(n)) — checks divisors from 2 to sqrt(n)
# Space: O(1) — just loop variable and flag
# All methods below have the same complexity.

# ----- Method 1: while-else (Python-specific feature) -----

n = int(input())
i = 2
while i <= (n ** 0.5):
    if n % i == 0:
        print("not prime")
        break
    i += 1
else:
    print("prime")

"""
While can have an else clause which is executed when the loop is finished normally
In case you break, then else clause is not executed
This is helpful from the above example - to avoid printing both "not prime" and "prime" in case of composite numbers,
we can use else clause to only print "not prime" in case of composite numbers and "prime" in case of prime numbers
Eg. if the number is 13 - the while condition is False, so the else clause is executed
if the number is 10 - the while loop break statement is executed, so the else clause is not executed
and you come out of the loop after printing "not prime" and the else clause is not executed
"""

# ----- How while-else works -----
#
#  while condition:     <-- if this becomes False naturally...
#      body             <-- ...and no 'break' was hit...
#  else:
#      this runs        <-- ...then else block executes!
#
#  If 'break' is hit --> else does NOT run.
#  Think of it as: "else = the loop completed without interruption"

# ----- Method 2: Using a flag variable -----

# OR (instead of else clause)

# we can use boolean variable as flag to keep track of whether the number is prime or not
n = int(input())
i = 2
flag = True  # assume the number is prime
while i <= (n ** 0.5):
    if n % i == 0:
        print("not prime")
        flag = False
        break
    i += 1
if flag:
    print("prime")

# ----- Method 3: Check loop variable after loop -----

# OR if I don't want to use flag or else clause - another approach is:

n = int(input())
i = 2
while i <= (n ** 0.5):
    if n % i == 0:
        print("not prime")
        break
    i += 1
if i > (n ** 0.5):     # if i went past sqrt(n), no divisor was found
    print("prime")


# ----- IMPORTANT: Avoiding Floating Point Issues -----

"""
In DSA, it's always preferable to avoid using floating point numbers. That is one issue with the above 3 approaches for prime number checking as we are calculating square root of a number.
As the universe of these floating point numbers is infinite, and it's not possible to represent all of them in a finite amount of space.
The memory space of a computer is finite, and it's not possible to represent all of the floating point numbers in a finite amount of space.
So, we can use integers to represent floating point numbers, and we can use the sys module to get the maximum integer and the minimum integer in the range.
What would happen if we try to fit all of the floating point numbers in a finite amount of space?
Maybe the floating point numbers that are close to each other will be stored in the same memory location. They will get the same binary
In discrete mathematics, there is a principle called Pigeonhole Principle, which states that if you have more than n items, then at least one of the items must be in more than one of the n boxes.
This principle is used in computer science to solve the problem of storing all of the floating point numbers in a finite amount of space.
We have this infinite universe of floating point numbers, and we want to map them to a finite set of binary representations.
So when we work with floating point numbers, we encounter "Precision Loss" and "Rounding Error" problems.
Precision loss is when we lose precision when we convert a floating point number to a binary representation.
Rounding error is when we round a floating point number to a binary representation, and the binary representation is not exactly the same as the original floating point number.
Eg. If we try to save 3.0 in memory, it's very likely that the binary representation of 3.0 will be different from the original floating point number.
If we try to save 3.141592653589793 in memory, it's very likely that the binary representation of 3.141592653589793 will be different from the original floating point number.
This is the reason we never compare floating point numbers for equality using == or !=
Eg. if I try to compare 3.0 with 3.0, it's likely one 3.0 is stored in binary form as 3.0000000001 and the other 3.0 is stored as 2.999999999, and they will never be equal.
"""

# ----- Summary of Floating Point Issues -----
#
# Problem:   Infinite real numbers, finite memory --> some numbers share the same
#            binary representation (Pigeonhole Principle)
# Result:    Precision loss and rounding errors
# Rule:      NEVER compare floats with == or !=
#            Instead of:  if x == 3.0        (DANGEROUS)
#            Use:         if abs(x - 3.0) < 0.0001   (SAFE)
#
# ----- The Fix for Prime Checking -----
# Instead of:  i <= n ** 0.5     (uses float square root)
# Use:         i * i <= n        (pure integer arithmetic, no precision issues!)

"""
So in the above prime number example, instead of using i<=(n**0.5), we can do i*i<=n

"""

# ----- Preferred versions using i*i <= n (integer-only) -----

# Method 1: while-else
n = int(input())
i = 2
while i * i <= n:
    if n % i == 0:
        print("not prime")
        break
    i += 1
else:
    print("prime")

# Method 2: flag variable
# we can use boolean variable as flag to keep track of whether the number is prime or not
n = int(input())
i = 2
flag = True  # assume the number is prime
while i * i <= n:
    if n % i == 0:
        print("not prime")
        flag = False
        break
    i += 1
if flag:
    print("prime")

# Method 3: check loop variable
# OR if I don't want to use flag or else clause - another approach is:

n = int(input())
i = 2
while i * i <= n:
    if n % i == 0:
        print("not prime")
        break
    i += 1
if i * i > n:
    print("prime")


# =============================================================================
# SECTION 8: continue Statement
# =============================================================================

""" Continue statement
Continue statement is used to skip the rest of the current iteration and move to the next iteration
It's similar to break statement, but it's not immediately terminated, and the program continues with the next iteration of the loop.
"""

# ----- How continue works -----
#
#   for i in range(10):
#       if i == 5:
#           continue        <-- skip everything below, jump to next iteration
#       print(i)            <-- this line is SKIPPED when i == 5
#
# Output: 0 1 2 3 4 6 7 8 9   (no 5!)

for i in range(10):
    if i == 5:
        continue  ## will print all numbers except for 5
    print(i)

"""
    IMPORTANT: If you are using continue in a while loop, make sure the update (i+=1)
    doesn't get skipped, else you will be stuck in an infinite loop
    This problem doesn't happen in a for loop, because for loop does everything on its own
    like initializing the loop variable, checking the condition, and updating the loop variable.
    See example below:

    i = 0
    while i < 10:
        if i == 5:
            continue
        print(i)
        i += 1 ## Here the i will now stay stuck at 5, because the update (i+=1) is skipped
"""

# ----- Why this infinite loop happens -----
#
#   i = 0
#   while i < 10:
#       if i == 5:
#           continue    <-- jumps back to "while i < 10"
#       print(i)        <-- SKIPPED
#       i += 1          <-- ALSO SKIPPED! i stays 5 forever!
#
# Fix: put i += 1 BEFORE the continue check:
#
#   i = 0
#   while i < 10:
#       i += 1          <-- always runs
#       if i == 5:
#           continue    <-- skips print, but i already incremented
#       print(i)

# ----- break vs continue vs pass -----
#
#   break:    EXIT the entire loop immediately
#   continue: SKIP the rest of THIS iteration, go to the next one
#   pass:     Do NOTHING (used as a placeholder when syntax requires a body)
#
# Example of pass:
#   for i in range(10):
#       pass    # TODO: implement later (empty loop body needs something)


# =============================================================================
# SECTION 9: Square Root of a Number (without built-in functions)
# =============================================================================

"""
Find SQUARE ROOT of a number
NOTE: Do this question without using the math module or any builtin functions or operators
eg. N = 64 Output: 8 #perfect square
N = 30 Output: 5.47

This below strategy would work for perfect squares:
Square root of any number is always going to be non-negative i.e >= 0
And the square of the square root of a number is always going to be <= the original number
So now, starting from zero, I will search for the largest number where the above condition is satisfied.
i.e keep going until i*i <= n
Once i*i > n, I will stop searching and return i-1

"""

# Time:  O(sqrt(n)) for integer part — we count from 0 to sqrt(n)
# Space: O(1)

# ----- Part 1: Perfect Squares -----
#
# Strategy: start from 0, keep incrementing by 1.
#           stop when ans*ans > n, then the answer is ans-1.
#
# ----- Walkthrough: sqrt(64) -----
# ans=0: 0*0=0 <= 64 ✓, ans=1: 1 <= 64 ✓, ans=2: 4 <= 64 ✓, ...
# ans=8: 64 <= 64 ✓, ans=9: 81 > 64 ✗ --> stop!
# Answer: 9 - 1 = 8 ✓
#
# ----- Walkthrough: sqrt(30) -----
# ans=5: 25 <= 30 ✓, ans=6: 36 > 30 ✗ --> stop!
# Answer: 6 - 1 = 5  (integer part only)

n = int(input("Enter a number: "))
ans = 0

while ans * ans <= n:
    ans += 1
print(ans - 1)


# ----- Part 2: Non-Perfect Squares (decimal precision) -----
#
# For n=30, we got 5 above. But the real answer is ~5.477.
# To get decimal places, after finding the integer part,
# repeat the same process with smaller increments:
#   +0.1 to find the tenths place
#   +0.01 to find the hundredths place
#   +0.001 to find the thousandths place, etc.
#
# ----- Walkthrough: sqrt(30) to 2 decimal places -----
#
# Step 1 (integer part, increment by 1):
#   ans=0,1,2,3,4,5 --> 5*5=25 <= 30 ✓
#   ans=6 --> 36 > 30 ✗ --> ans = 6-1 = 5
#
# Step 2 (tenths place, increment by 0.1):
#   ans=5.0, 5.1, 5.2, 5.3, 5.4 --> 5.4*5.4=29.16 <= 30 ✓
#   ans=5.5 --> 30.25 > 30 ✗ --> ans = 5.5-0.1 = 5.4
#
# Step 3 (hundredths place, increment by 0.01):
#   ans=5.40, 5.41, 5.42, ..., 5.47 --> 5.47*5.47=29.9209 <= 30 ✓
#   ans=5.48 --> 30.0304 > 30 ✗ --> ans = 5.48-0.01 = 5.47
#
# Answer: 5.47

## Now for non-perfect squares: instead of adding/subtracting 1, we add/subtract 0.1 or 0.01 or 0.001 etc. depending on how many decimal places we want to round to.

n = int(input("Enter a number: "))
ans = 0

while ans * ans <= n:
    ans += 1

ans = ans - 1               # integer part found

while ans * ans <= n:
    ans += 0.1

ans = ans - 0.1             # tenths place found

while ans * ans <= n:
    ans += 0.01
ans = ans - 0.01            # hundredths place found


while ans * ans <= n:
    ans += 0.001
ans = ans - 0.001           # thousandths place found


# ----- Part 3: Generalized to any number of decimal places -----

"""
Now let's generalize this to any number of decimal places.
We can see depending on the number of decimal places, p, we want in the output, we run the same while loop that many times.

"""

# ----- First attempt (has a quirk) -----
# Note: when i=0, 0.1**0 = 1, which redoes the integer search unnecessarily.
# It works but wastes one iteration. The version below it is cleaner.

n = int(input("Enter a number: "))
p = int(input("Enter the number of decimal places: "))
ans = 0

while ans * ans <= n:
    ans = ans + 1

ans = ans - 1

for i in range(p):
    while ans * ans <= n:
        ans += 0.1 ** i     # i=0: adds 1 (redundant), i=1: adds 0.1, i=2: adds 0.01
    ans = ans - 0.1 ** i

print(ans)

# ----- Cleaner version using inc_fac -----
# Uses a separate variable for the increment factor, starts at 0.1 (not 1).

### More general way of doing it

n = int(input("Enter a number: "))
p = int(input("Enter the number of decimal places: "))
ans = 0

while ans * ans <= n:
    ans = ans + 1

ans = ans - 1
inc_fac = 0.1               # start at 0.1, not 1

for _ in range(p):
    while ans * ans <= n:
        ans = ans + inc_fac
    ans = ans - inc_fac
    inc_fac = inc_fac / 10   # 0.1 --> 0.01 --> 0.001 --> ...

print(round(ans, p))  # rounding to p decimal places

# another way to do round is using the f string - .4f means round to 4 decimal places

print(f"{ans:.4f}")

# ----- Time Complexity -----
# Integer part: O(sqrt(n)) iterations
# Each decimal place: up to 10 iterations (0.1, 0.2, ..., 0.9 at most)
# Total for p decimal places: O(sqrt(n) + 10*p)
# This is a LINEAR search approach. Binary search can do this in O(log n) - covered later!
