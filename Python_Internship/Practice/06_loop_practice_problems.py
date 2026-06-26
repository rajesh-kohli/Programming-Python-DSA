# =============================================================================
# LOOP PRACTICE PROBLEMS (While Loops)
# =============================================================================
# These are classic beginner practice problems solved using while loops.
# Each problem builds on fundamental concepts: counters, accumulators,
# digit extraction, and nested loops for patterns.
#
# Key pattern in most problems:
#   1. Initialize a counter/accumulator
#   2. Loop while a condition holds
#   3. Update the counter/accumulator inside the loop
#   4. Print the result after the loop ends


# =============================================================================
# PROBLEM 1: Sum of All Even Numbers from 1 to N
# =============================================================================
# Given a number n, find the sum of all even numbers from 1 to n.
#
# Example: n = 10 --> 2 + 4 + 6 + 8 + 10 = 30
# Example: n = 7  --> 2 + 4 + 6 = 12
#
# Approach: Loop from 1 to n, check if each number is even (i%2 == 0),
# and add it to a running sum.
#
# Time Complexity: O(n) -- we check every number from 1 to n
# Space Complexity: O(1) -- only a few variables
#
# Note: There's a math formula for this: n/2 * (n/2 + 1), which is O(1),
# but the loop approach is better for learning.
#
# WARNING: We use 'sum' as a variable name here for simplicity, but in real
# code avoid shadowing Python's built-in sum() function. Use 'total' instead.

n = int(input("Problem 1 - Enter the number: "))
i = 1
sum = 0
while i <= n:
    if i % 2 == 0:
        sum = sum + i
    i += 1
print(f"Sum of even numbers from 1 to {n}: {sum}")

# Walkthrough for n = 10:
# i=1: odd, skip     | sum=0
# i=2: even, add 2   | sum=2
# i=3: odd, skip     | sum=2
# i=4: even, add 4   | sum=6
# i=5: odd, skip     | sum=6
# i=6: even, add 6   | sum=12
# i=7: odd, skip     | sum=12
# i=8: even, add 8   | sum=20
# i=9: odd, skip     | sum=20
# i=10: even, add 10 | sum=30
# Output: 30


# =============================================================================
# PROBLEM 2: Sum of Difference of Even and Odd Numbers from 1 to N
# =============================================================================
# Given n, compute: (sum of even numbers) - (sum of odd numbers), then
# take the absolute value.
#
# Example: n = 5
#   Even: 2 + 4 = 6
#   Odd:  1 + 3 + 5 = 9
#   Difference: |6 - 9| = 3
#
# Approach: Use a single accumulator -- add even numbers, subtract odd numbers.
# Then take abs() at the end.
#
# Time Complexity: O(n)
# Space Complexity: O(1)

n = int(input("Problem 2 - Enter the number: "))
i = 1
sum = 0
while i <= n:
    if i % 2 == 0:
        sum = sum + i
    else:
        sum = sum - i
    i += 1
print(f"Absolute difference of even and odd sums from 1 to {n}: {abs(sum)}")

# Walkthrough for n = 5:
# i=1: odd,  sum = 0 - 1 = -1
# i=2: even, sum = -1 + 2 = 1
# i=3: odd,  sum = 1 - 3 = -2
# i=4: even, sum = -2 + 4 = 2
# i=5: odd,  sum = 2 - 5 = -3
# abs(-3) = 3
# Output: 3


# =============================================================================
# PROBLEM 3: Sum of Digits of a Number
# =============================================================================
# Given a number, find the sum of its digits.
# Example: 123 --> 1 + 2 + 3 = 6
# Example: 9045 --> 9 + 0 + 4 + 5 = 18
#
# Approach 1 (Mathematical -- extracting digits using modulo and division):
#   - n % 10 gives the last digit (remainder when dividing by 10)
#   - n // 10 removes the last digit (integer division by 10)
#   - Repeat until n becomes 0
#
# This is a fundamental technique -- digit extraction comes up in many problems!
#
# Time Complexity: O(d) where d = number of digits = O(log10(n))
# Space Complexity: O(1)

n = int(input("Problem 3a - Enter the number: "))
original_n = n  # Save for display since we modify n
sum = 0
while n > 0:
    rem = n % 10       # Extract the last digit
    sum = sum + rem    # Add it to sum
    n = n // 10        # Remove the last digit
print(f"Sum of digits of {original_n}: {sum}")

# Walkthrough for n = 123:
# n=123: rem = 123%10 = 3, sum = 0+3 = 3, n = 123//10 = 12
# n=12:  rem = 12%10 = 2,  sum = 3+2 = 5, n = 12//10 = 1
# n=1:   rem = 1%10 = 1,   sum = 5+1 = 6, n = 1//10 = 0
# n=0: loop ends
# Output: 6


# ---- Approach 2 (String conversion): ----
# Convert the number to a string, iterate through each character,
# convert back to int, and add.
# This is simpler to read but slightly less efficient (creates a string).
#
# Time Complexity: O(d) where d = number of digits
# Space Complexity: O(d) -- the string stores all digits

n = int(input("Problem 3b - Enter the number: "))
n_str = str(n)
sum = 0
i = 0
while i < len(n_str):
    sum = sum + int(n_str[i])
    i += 1
print(f"Sum of digits (string method): {sum}")

# Note: A more Pythonic way would be:
#   sum(int(ch) for ch in str(n))
# But we use while loops here for practice.


# =============================================================================
# PROBLEM 4: Sum of Even Digits of a Number
# =============================================================================
# Given a number, find the sum of only its even digits.
# Example: 123 --> only 2 is even --> sum = 2
# Example: 2468 --> 2 + 4 + 6 + 8 = 20
# Example: 13579 --> no even digits --> sum = 0
#
# Approach: Same digit extraction as Problem 3, but add only if the digit
# is even (rem % 2 == 0). Note: 0 is considered even.
#
# Time Complexity: O(d) where d = number of digits
# Space Complexity: O(1)

n = int(input("Problem 4 - Enter the number: "))
original_n = n
sum_even = 0
while n > 0:
    rem = n % 10
    if rem % 2 == 0:   # Check if the digit itself is even
        sum_even += rem
    n = n // 10
print(f"Sum of even digits of {original_n}: {sum_even}")

# Walkthrough for n = 123:
# n=123: rem=3, 3%2!=0 (odd), skip   | sum_even=0, n=12
# n=12:  rem=2, 2%2==0 (even), add 2 | sum_even=2, n=1
# n=1:   rem=1, 1%2!=0 (odd), skip   | sum_even=2, n=0
# Output: 2


# =============================================================================
# PROBLEM 5: Factorial of a Number
# =============================================================================
# Factorial of n (written n!) = 1 * 2 * 3 * ... * n
# Example: 5! = 1 * 2 * 3 * 4 * 5 = 120
# Special case: 0! = 1 (by definition)
#
# Approach: Start with factorial = 1, multiply by each number from 1 to n.
# We use 1 as the starting value because 1 is the identity for multiplication
# (just like 0 is the identity for addition).
#
# Time Complexity: O(n)
# Space Complexity: O(1)
# Note: Factorials grow extremely fast! 20! = 2,432,902,008,176,640,000
# Python handles big integers natively, so no overflow, but it gets slow
# for very large n.

n = int(input("Problem 5 - Enter the number: "))
factorial = 1
i = 1
while i <= n:
    factorial = factorial * i
    i += 1
print(f"{n}! = {factorial}")

# Walkthrough for n = 5:
# i=1: factorial = 1 * 1 = 1
# i=2: factorial = 1 * 2 = 2
# i=3: factorial = 2 * 3 = 6
# i=4: factorial = 6 * 4 = 24
# i=5: factorial = 24 * 5 = 120
# Output: 120


# =============================================================================
# PROBLEM 6: Pyramid of Stars
# =============================================================================
# Print a pyramid pattern of stars with n rows.
#
# How it works:
#   For each row i (1 to n):
#     1. Print (n-i) spaces      -- to push the stars to the right
#     2. Print (2*i - 1) stars   -- odd number of stars per row (1, 3, 5, ...)
#     3. Print (n-i) spaces      -- trailing spaces (optional, for symmetry)
#     4. Move to next line
#
# Expected Output for n = 5:
#         *
#       * * *
#     * * * * *
#   * * * * * * *
# * * * * * * * * *
#
# (Each star is followed by a space, each leading space is two characters wide)
#
# Time Complexity: O(n^2) -- for each of n rows, we print up to ~2n characters
# Space Complexity: O(1)

print("\nPyramid of Stars")
n = int(input("Enter the value of n: "))
i = 1
while i <= n:
    # Print leading spaces (n-i spaces to center the stars)
    j = 1
    while j <= n - i:
        print(" ", end=" ")
        j = j + 1

    # Print stars (2*i - 1 stars in row i)
    k = 1
    while k <= 2 * i - 1:
        print("*", end=" ")
        k = k + 1

    # Print trailing spaces (for symmetry -- optional)
    l = 1
    while l <= n - i:
        print(" ", end=" ")
        l = l + 1

    i = i + 1
    print()  # Move to the next line after each row

# Walkthrough for n = 3:
# Row 1 (i=1): 2 spaces + 1 star  + 2 spaces  -->  "    *    "
# Row 2 (i=2): 1 space  + 3 stars + 1 space   -->  "  * * *  "
# Row 3 (i=3): 0 spaces + 5 stars + 0 spaces  -->  "* * * * *"
#
# Pattern insight:
#   Row i has (2*i - 1) stars: 1, 3, 5, 7, ...  (always odd!)
#   Row i has (n-i) leading spaces to center the pyramid
