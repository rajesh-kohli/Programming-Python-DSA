###############################################################################
#     Lectures 1-4: Flowcharts, Pseudocode, Intro/Syntax & Star Patterns     #
###############################################################################

"""
These are all the practice questions from the first 4 lectures
(Flowcharts, Pseudocode, Intro/Syntax) of the DSA Coding Blocks.
"""

# =============================================================================
# SECTION 1: Basic Problems (Conditionals & Loops)
# =============================================================================


# -----------------------------------------------------------------------------
# 1.1 Largest of Three Numbers
# -----------------------------------------------------------------------------

# ----- Approach -----
# Compare each number against the other two using 'and'.
# If x > y AND x > z, then x is the largest. Same logic for y and z.

# Time: O(1)  — fixed number of comparisons (at most 2)
# Space: O(1) — only 3 variables

# Largest of three numbers
x, y, z = map(int, input("Enter three numbers: ").split())

if x > y and x > z:
    print(f"{x} is the largest")
elif y > x and y > z:
    print(f"{y} is the largest")
else:
    print(f"{z} is the largest")

# NOTE: This doesn't handle ties (e.g., x == y > z). For a robust version:
# print(f"{max(x, y, z)} is the largest")


# -----------------------------------------------------------------------------
# 1.2 Print a Series: a+b, a+2b, a+3b
# -----------------------------------------------------------------------------

"""
Given two numbers say a and b, design an algorithm
to print the following series [a+b, a+2*b, a+3*b]
"""

# ----- Approach -----
# The pattern is: a + i*b, where i goes from 1 to 3.
#
# Example: a=10, b=5
#   i=1: 10 + 1*5 = 15
#   i=2: 10 + 2*5 = 20
#   i=3: 10 + 3*5 = 25
# Output: 15 20 25

# Time: O(1)  — always exactly 3 iterations (fixed, not dependent on input size)
# Space: O(1)

a, b = map(int, input("Enter two numbers: ").split())
for i in range(1, 4):
    print(a + i * b, end=" ")  # sep is between the printed values. end is after the entire printed line.


# -----------------------------------------------------------------------------
# 1.3 First N Natural Numbers
# -----------------------------------------------------------------------------

"""
Given a positive number n , design an algorithm to
print the first n natural numbers
"""

# ----- range(1, num+1) -----
# range(1, num+1) generates: 1, 2, 3, ..., num
# Remember: range(start, stop) goes up to stop-1, so we use num+1 to include num.

# Time: O(n)  — loop runs n times
# Space: O(1) — only the loop variable i

num = int(input("Enter a number: "))
for i in range(1, num + 1):
    print(i, end=" ")


# -----------------------------------------------------------------------------
# 1.4 Print Even Numbers from 2 to N
# -----------------------------------------------------------------------------

"""
Print Even Numbers
Given a positive number n ,
design an algorithm to print all the even numbers from 2 to n
"""

# ----- range(start, stop, step) -----
# The third argument is the STEP size.
# range(2, num+1, 2) generates: 2, 4, 6, 8, ..., up to num
# This skips odd numbers entirely — more efficient than checking if i % 2 == 0.

# Time: O(n)  — loop runs n/2 times, which is still O(n)
# Space: O(1)

num = int(input("Enter a number: "))

for i in range(2, num + 1, 2):
    print(i, end=" ")


# -----------------------------------------------------------------------------
# 1.5 Sum of First N Natural Numbers
# -----------------------------------------------------------------------------

"""
Sum of Natural Numbers
Given a positive number n ,
design an algorithm to compute the sum of first n natural numbers
"""

# ----- Approach -----
# Use an accumulator variable (sum) that starts at 0.
# Add each number 1, 2, 3, ..., n to it.
#
# Alternative: Use the formula  n * (n + 1) / 2  for O(1) time.
#   Example: n=5 --> 5 * 6 / 2 = 15 = 1+2+3+4+5 ✓

# Time: O(n)  — loop runs n times  (O(1) if using the formula)
# Space: O(1) — just one accumulator variable

num = int(input("Enter a number: "))
sum = 0
for i in range(1, num + 1):
    sum += i
print(f"The sum of first {num} natural numbers is {sum}")


# -----------------------------------------------------------------------------
# 1.6 Sum of N Given Numbers
# -----------------------------------------------------------------------------

"""
Sum of Numbers
Given a positive number n followed by n integer values
design an algorithm to find the sum of  n numbers
Example:
Input : n = 5 ; [ 10, 20, 30, 40, 50 ]
Output : 150
Explanation : 10+20+30+40+50 = 150
"""

# Time: O(n)  — reads and adds n numbers
# Space: O(1) — just one accumulator

num = int(input("Enter a number: "))
sum = 0
for i in range(num):
    sum += int(input("Enter a number: "))
print(f"The sum of the {num} numbers is {sum}")


# =============================================================================
# SECTION 2: Prime Number Check (3 Approaches)
# =============================================================================

"""
Prime Number Check
Given a positive number n,
design an algorithm to check if the number is prime
"""

# ----- What is a Prime Number? -----
# A number > 1 that is divisible ONLY by 1 and itself.
# Primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, ...
# Not prime: 0, 1, 4, 6, 8, 9, 10, 12, ...
#
# ----- Why check up to sqrt(n)? -----
# If n = a * b, then one of a or b must be <= sqrt(n).
# So if no factor is found up to sqrt(n), n is prime.
# This reduces time from O(n) to O(sqrt(n)).

# ----- Method 1: For loop, check all numbers from 2 to n-1 (Brute Force) -----
# Time: O(n)

num = int(input("Enter a number: "))

if num < 2:
    print("Not Prime")
else:
    is_prime = True
    for i in range(2, num):         # check every number from 2 to n-1
        if num % i == 0:
            is_prime = False
            break                    # no need to check further
    if is_prime:
        print("Prime")
    else:
        print("Not Prime")


# ----- Method 2: While loop, check from 2 to sqrt(n) (Optimized) -----
# Time: O(sqrt(n))

## Now do it with a while loop where you check for factors from
# 2 to sqrt(n) and break if you find one.

num = int(input("Enter a number: "))
if num < 2:
    print("Not Prime")
else:
    i = 2
    is_prime = True
    while i * i <= num:  # or i <= int(num**0.5): or i <= math.sqrt(num)
        if num % i == 0:
            is_prime = False
            break
        i += 1
    if is_prime:
        print("Prime")
    else:
        print("Not Prime")


# ----- Method 3: For loop with sqrt(n) range (Optimized + Clean) -----
# Time: O(sqrt(n))

### Now do it with a for loop where you check for factors from 2 to sqrt(n) and break if you find one.

num = int(input("Enter a number: "))
if num < 2:
    print("Not Prime")
else:
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):    # +1 because range excludes the end
        if num % i == 0:
            is_prime = False
            break
    if is_prime:  # this means that the loop completed without finding a factor, so the number is prime
        print("Prime")
    else:
        print("Not Prime")

# ----- Comparison -----
# | Method | Range checked   | Time       | Notes                        |
# |--------|-----------------|------------|------------------------------|
# | 1      | 2 to n-1        | O(n)       | Simple but slow for large n  |
# | 2      | 2 to sqrt(n)    | O(sqrt(n)) | Uses i*i <= n (integer-only) |
# | 3      | 2 to sqrt(n)    | O(sqrt(n)) | Uses range() (cleaner)       |


# =============================================================================
# SECTION 3: Largest of N Numbers
# =============================================================================

"""
Largest of N numbers
Given N integer values, design an algorithm to
find the largest of the N numbers
"""

# ----- Core Idea -----
# Start with -infinity so ANY number will be larger.
# Compare each input against max_so_far, update if bigger.
#
# ----- Walkthrough -----
# Input: 5 numbers --> 12, 45, 3, 67, 22
# msf = -inf
# 12 > -inf? YES --> msf = 12
# 45 > 12?   YES --> msf = 45
# 3 > 45?    NO
# 67 > 45?   YES --> msf = 67
# 22 > 67?   NO
# Answer: 67

# Time: O(n)  — single pass through all n numbers
# Space: O(1) — only one variable (maxsofar) regardless of input size

maxsofar = float('-inf')  # or you can use max_so_far = None and then check if max_so_far is None before updating it
num = int(input("Enter a number: "))
for i in range(num):
    val = int(input("Enter a number: "))
    if val > maxsofar:
        maxsofar = val
print(f"The largest of the {num} numbers is {maxsofar}")


# =============================================================================
# SECTION 4: Star Patterns — One-Liner Versions
# =============================================================================

"""
Printing Stars
Given a positive number N,
design an algorithm to print N stars
Example Input : N = 3
  Output :
*  *  *
"""

# ----- Complexity for ALL Star Patterns -----
# Time: O(n^2) — outer loop runs n times, inner work per row is up to n
#   Total characters printed ≈ 1 + 2 + 3 + ... + n = n*(n+1)/2 = O(n^2)
#   (Same for pyramids and butterflies — the total work is always O(n^2))
# Space: O(1) — no arrays, just loop variables
#   (One-liners using "* " * n create a temporary string of length O(n),
#    but this is transient and not stored)

# These use Python's string multiplication trick:
#   "* " * 3  -->  "* * * "
#   " " * 4   -->  "    "
# This lets us write patterns as one-liners.

num = int(input("Enter a number: "))

# ----- 4.1: Row of Stars -----
# Output (num=5): * * * * *

for i in range(num):
    print("*", end=" ")

# ----- 4.2: Square of Stars -----
# Output (num=4):
# * * * *
# * * * *
# * * * *
# * * * *

num = int(input("Enter a number: "))
for i in range(num):
    print("* " * num)  # prints a square of stars

# ----- 4.3: Inverted Right-Angled Triangle -----
# Output (num=5):
# * * * * *
# * * * *
# * * *
# * *
# *
#
# Row i (0-indexed): prints (num - i) stars

for i in range(num):
    print("* " * (num - i))  # prints an inverted right-angled triangle of stars

# ----- 4.4: Right-Angled Triangle -----
# Output (num=5):
# *
# * *
# * * *
# * * * *
# * * * * *
#
# Row i (0-indexed): prints (i + 1) stars

for i in range(num):
    print("* " * (i + 1))  # prints a right-angled triangle of stars

# ----- 4.5: Right-Aligned Right-Angled Triangle -----
# Output (num=5):
#         *
#       * *
#     * * *
#   * * * *
# * * * * *
#
# Row i: (num-i-1) spaces + (i+1) stars

for i in range(num):
    print(" " * (num - i - 1) + "*" * (i + 1))  # prints a right-angled triangle of stars aligned to the right

# ----- Same pattern with multiple inner loops -----
# (Helpful to understand when you can't use string multiplication)

n = 5
for i in range(1, n + 1):
    for j in range(n - i):         # print spaces
        print(" ", end=" ")
    for k in range(i):             # print stars
        print("*", end=" ")
    print()

# ----- 4.6: Right-Aligned Inverted Triangle -----
# Output (num=5):
# * * * * *
#   * * * *
#     * * *
#       * *
#         *
#
# Row i: i spaces + (num-i) stars

for i in range(num):
    print(" " * i + "*" * (num - i))  # prints an inverted right-angled triangle of stars aligned to the right

# ----- 4.7: Pyramid -----
# Output (num=5):
#         *
#       * * *
#     * * * * *
#   * * * * * * *
# * * * * * * * * *
#
# Row i (0-indexed): (num-i-1) spaces + (2*i+1) stars
# Row i (1-indexed): (num-i) spaces + (2*i-1) stars

for i in range(num):
    print(" " * (num - i - 1) + "*" * (2 * i + 1))  # prints a pyramid of stars

for i in range(1, num + 1):
    print(" " * (num - i) + "*" * (2 * i - 1))  # prints a pyramid of stars as well

# Both versions produce the same output — just different indexing (0-based vs 1-based).

# ----- 4.8: Inverted Pyramid -----
# Output (num=5):
# * * * * * * * * *
#   * * * * * * *
#     * * * * *
#       * * *
#         *
#
# Row i: i spaces + (2*(num-i)-1) stars

for i in range(num):
    print(" " * i + "*" * (2 * (num - i) - 1))  # prints an inverted pyramid of stars


# =============================================================================
# SECTION 5: Star Patterns — Multiple For Loops (Nested Loops)
# =============================================================================

"""
Now do these stars patterns with multiple for loops,
where you have one for loop for the spaces and one for loop for the stars.
"""

# These use nested loops instead of string multiplication.
# This is important to understand because:
#   1. Not all languages have string multiplication
#   2. When printing NUMBERS (not just stars), you can't use string multiplication
#   3. This teaches you how to think about nested loop structure

# ----- Understanding the Structure -----
# Every pattern row has the same structure:
#   [ spaces ][ stars ]
# So each row needs TWO inner loops:
#   Loop 1: prints the correct number of spaces
#   Loop 2: prints the correct number of stars

num = int(input("Enter a number: "))

# ----- 5.1: Square of Stars -----
# Output (num=4):
# * * * *
# * * * *
# * * * *
# * * * *
#
# Each row: 0 spaces + num stars

# square of stars with multiple for loops

for i in range(num):  ## no need for num + 1 here because we are not using the index for anything, just to repeat the loop num times
    for j in range(num):
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars


# ----- 5.2: Right-Angled Triangle -----
# Output (num=5):
# *
# * *
# * * *
# * * * *
# * * * * *
#
# Row i (0-indexed): 0 spaces + (i+1) stars
# Row i (1-indexed): 0 spaces + i stars

# right-angled triangle of stars with multiple for loops

for i in range(num):
    for j in range(i + 1):  # here we are using index value to print the correct number of stars in each row
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars

# Same thing with 1-based indexing:
for i in range(1, num + 1):
    for j in range(1, i + 1):
        print("*", end=" ")

# ----- Same pattern using while loop -----
# This shows how for and while loops map to each other:
#   for i in range(1, num+1):  ==  i=1; while i<=num: ... i+=1

#using while loop

i = 1
while i <= num:
    # for the ith row, print i stars
    j = 1
    while j <= i:
        print("*", end=" ")  # by default print function goes to the next line after printing the value, so we use end=" " to print the stars without a new line
        j += 1
    print()
    i += 1

# ----- 5.3: Inverted Right-Angled Triangle -----
# Output (num=5):
# * * * * *
# * * * *
# * * *
# * *
# *
#
# Row i (0-indexed): 0 spaces + (num-i) stars

# inverted right-angled triangle of stars with multiple for loops

for i in range(num):
    for j in range(num - i):  # here we are using index value to print the correct number of stars in each row
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars


# ----- 5.4: Right-Aligned Right-Angled Triangle -----
# Output (num=5):
#         *
#       * *
#     * * *
#   * * * *
# * * * * *
#
# Row i: (num-i-1) spaces + (i+1) stars
#
# ----- How to figure out the formula -----
# Row 0: 4 spaces + 1 star   --> spaces = num-1-0 = 4,  stars = 0+1 = 1
# Row 1: 3 spaces + 2 stars  --> spaces = num-1-1 = 3,  stars = 1+1 = 2
# Row 2: 2 spaces + 3 stars  --> spaces = num-1-2 = 2,  stars = 2+1 = 3
# Row 3: 1 space  + 4 stars  --> spaces = num-1-3 = 1,  stars = 3+1 = 4
# Row 4: 0 spaces + 5 stars  --> spaces = num-1-4 = 0,  stars = 4+1 = 5
# Pattern: spaces = (num - i - 1), stars = (i + 1)

# right-angled triangle of stars aligned to the right with multiple for loops

for i in range(num):
    for j in range(num - i - 1):  # print spaces
        print(" ", end=" ")
    for k in range(i + 1):  # print stars
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars

# ----- 5.5: Right-Aligned Inverted Triangle -----
# Output (num=5):
# * * * * *
#   * * * *
#     * * *
#       * *
#         *
#
# Row i: i spaces + (num-i) stars

# inverted right-angled triangle of stars aligned to the right with multiple for loops

for i in range(num):
    for j in range(i):  # print spaces
        print(" ", end=" ")
    for k in range(num - i):  # print stars
        print("*", end=" ")
    print()  # move to the next line after printing each row of stars

# ----- 5.6: Pyramid -----
# Output (num=5):
#         *
#       * * *
#     * * * * *
#   * * * * * * *
# * * * * * * * * *
#
# Row i (1-indexed): (num-i) spaces + (2*i-1) stars
#
# ----- Deriving the star count formula -----
# Row 1: 1 star    = 2*1-1
# Row 2: 3 stars   = 2*2-1
# Row 3: 5 stars   = 2*3-1
# Row 4: 7 stars   = 2*4-1
# Row 5: 9 stars   = 2*5-1
# Stars are always ODD numbers: 1, 3, 5, 7, 9 --> formula: (2*i - 1)

# Pyramid of stars with multiple for loops

for i in range(1, num + 1):
    for j in range(num - i):
        print(" ", end=" ")  # print spaces and end with a space or can also do print(" ", end="") for single space
    for k in range(2 * i - 1):
        print("*", end=" ")  # print stars with spaces or can also do print("*", end="") and this won't have spaces between stars
    print()  # this print() is to move to the next line after printing each row of stars

# ----- 5.7: Inverted Pyramid -----
# Output (num=5):
# * * * * * * * * *
#   * * * * * * *
#     * * * * *
#       * * *
#         *
#
# Row i (0-indexed): i spaces + (2*(num-i)-1) stars

# inverted pyramid of stars with multiple for loops

for i in range(num):
    for j in range(i):
        print(" ", end=" ")  # print spaces and end with a space or can also do print(" ", end="") for single space
    for k in range(2 * (num - i) - 1):
        print("*", end=" ")  # print stars with spaces or can also do print("*", end="") and this won't have spaces between stars
    print()  # this print() is to move to the next line after printing each row of stars


# =============================================================================
# SECTION 6: Butterfly Pattern
# =============================================================================

# ----- 6.1: Butterfly Upper Half -----
# Output (num=5):
# *                 *
# * *             * *
# * * *         * * *
# * * * *     * * * *
# * * * * * * * * * *
#
# Each row has THREE parts:
#   1. LEFT stars:   i stars
#   2. MIDDLE spaces: 2*(num-i) spaces
#   3. RIGHT stars:  i stars
#
# ----- Deriving the space count -----
# Row 1: 1 star + 8 spaces + 1 star  --> spaces = 2*(5-1) = 8
# Row 2: 2 stars + 6 spaces + 2 stars --> spaces = 2*(5-2) = 6
# Row 5: 5 stars + 0 spaces + 5 stars --> spaces = 2*(5-5) = 0

##  "butterfly pattern (upper half)" — also called "mirror triangles" or "double right-angled triangle"
for i in range(1, num + 1):
    for j in range(i):                 # LEFT stars
        print("*", end=" ")
    for k in range(2 * (num - i)):     # MIDDLE spaces
        print(" ", end=" ")
    for l in range(i):                 # RIGHT stars
        print("*", end=" ")
    print()  # this print() is to move to the next line after printing each row

# this is a more compact way to do the butterfly pattern (upper half)
num = 5

for i in range(1, num + 1):
    print("* " * i + "  " * (num - i) * 2 + "* " * i)

# ----- 6.2: Butterfly Lower Half (Inverted) -----
# Output (num=5):
# * * * * * * * * * *
# * * * *     * * * *
# * * *         * * *
# * *             * *
# *                 *
#
# Same idea, reversed: stars decrease, spaces increase.
# Row i (0-indexed): (num-i) stars + 2*i spaces + (num-i) stars

# inverted butterfly pattern (lower half)
for i in range(num):
    print("*" * (num - i) + " " * (2 * i) + "*" * (num - i))  # this is a more compact way

# inverted butterfly pattern (lower half) with multiple for loops
for i in range(num):
    for j in range(num - i):           # LEFT stars
        print("*", end=" ")
    for k in range(2 * i):             # MIDDLE spaces
        print(" ", end=" ")
    for l in range(num - i):           # RIGHT stars
        print("*", end=" ")
    print()  # this print() is to move to the next line after printing each row of stars

# inverted butterfly pattern (lower half) compact
for i in range(num):
    print("* " * (num - i) + "  " * i * 2 + "* " * (num - i))  ## notice the diff on line 263 and 277 - both do the same thing but this one makes it more visual with spaces


# =============================================================================
# SECTION 7: Binary Triangle Pattern (0s and 1s)
# =============================================================================

"""
print the below pattern
N = 5
1
0 1
1 0 1
0 1 0 1
1 0 1 0 1
"""

# This pattern is covered in detail in 03_pattern_printing.py (Pattern 3: Binary Triangle).
# Key ideas:
#   - Odd rows start with 1, even rows start with 0
#   - Values alternate using: num = 1 - num


# =============================================================================
# Quick Reference: Star Pattern Formulas (for num = N)
# =============================================================================

# | Pattern                    | Spaces per row  | Stars per row  |
# |----------------------------|-----------------|----------------|
# | Square                     | 0               | N              |
# | Right-angled triangle      | 0               | i + 1          |
# | Inverted triangle          | 0               | N - i          |
# | Right-aligned triangle     | N - i - 1       | i + 1          |
# | Right-aligned inv triangle | i               | N - i          |
# | Pyramid                    | N - i           | 2*i - 1        |
# | Inverted pyramid           | i               | 2*(N-i) - 1    |
# | Butterfly (upper)          | see above       | i + gap + i    |
# | Butterfly (lower)          | see above       | (N-i)+gap+(N-i)|
#
# (i is 0-indexed unless noted; pyramid uses 1-indexed for cleaner formula)
#
# ----- The Universal Approach -----
# 1. Draw the expected output on paper
# 2. Number the rows (0 or 1 indexed)
# 3. Count spaces and stars for each row
# 4. Find the formula relating row number (i) to those counts
# 5. Write the outer loop (rows), then inner loops (spaces, then stars)


# =============================================================================
# How to Think About Time & Space Complexity
# =============================================================================

# ----- What is Time Complexity? -----
# It measures how the number of operations GROWS as input size (n) increases.
# We use Big-O notation to express the WORST case growth rate.
#
# ----- Common Complexities (from fastest to slowest) -----
#
# | Big-O        | Name           | Example                        | n=1000      |
# |--------------|----------------|--------------------------------|-------------|
# | O(1)         | Constant       | Array lookup, math formula     | 1 op        |
# | O(log n)     | Logarithmic    | Binary search                  | ~10 ops     |
# | O(n)         | Linear         | Single loop, linear search     | 1,000 ops   |
# | O(n log n)   | Linearithmic   | Merge sort, Python's sort()    | ~10,000 ops |
# | O(n^2)       | Quadratic      | Nested loops, bubble sort      | 1,000,000   |
# | O(n^3)       | Cubic          | Triple nested loops            | 10^9 ops    |
# | O(2^n)       | Exponential    | All subsets, brute-force       | 10^301 ops  |
#
# ----- What is Space Complexity? -----
# It measures how much EXTRA memory the algorithm uses (beyond the input).
#   O(1): only a fixed number of variables (most problems in this file)
#   O(n): creating a list/array of size n
#
# ----- Quick Rules for Counting -----
# 1. Single loop over n elements            --> O(n)
# 2. Nested loop (loop inside a loop)       --> O(n^2)
# 3. Loop that halves the search space      --> O(log n)
# 4. Constants and lower-order terms drop   --> O(3n + 5) = O(n)
# 5. Consecutive (non-nested) loops ADD     --> O(n) + O(n) = O(n)
# 6. Nested loops MULTIPLY                  --> O(n) * O(n) = O(n^2)
#
# ----- How to Analyze Your Code -----
# Ask: "If I double the input size, how much longer does it take?"
#   O(1):     same time
#   O(log n): barely longer
#   O(n):     2x longer
#   O(n^2):   4x longer
#   O(n^3):   8x longer
