# =============================================================================
# MIXED PRACTICE PROBLEMS
# =============================================================================
# This file covers a variety of topics: function tracing, global variables,
# operator precedence, prime number checking, loop scope, and while-else.
# These are the kinds of questions that appear in interviews and exams.


# =============================================================================
# SECTION 1: Function Tracing (Call Stack Practice)
# =============================================================================
# Trace through these functions step by step to predict the output.
# This is a critical skill -- interviewers often ask you to trace code
# on paper without running it.

def fun1(a, b):
    fun2(5, 6)           # Calls fun2, return value (9) is DISCARDED
    x = fun3()           # Calls fun3, x = 5
    return a + b * b     # 6 + 7*7 = 6 + 49 = 55
                         # Note: multiplication has higher precedence than addition

def fun2(p, q):
    return p + q - 2     # 5 + 6 - 2 = 9

def fun3():
    return 5

print(fun1(6, 7))
# Output: 55
#
# Call Stack Trace:
# 1. main calls fun1(6, 7)
# 2. fun1 calls fun2(5, 6) --> fun2 returns 9, but fun1 ignores it
# 3. fun1 calls fun3()     --> fun3 returns 5, stored in x (but x is unused)
# 4. fun1 computes 6 + 7*7 = 6 + 49 = 55 and returns it
# 5. print(55) displays "55"


# =============================================================================
# SECTION 2: Global Variables and the `global` Keyword
# =============================================================================
# In Python, variables inside a function are LOCAL by default.
# To modify a variable from the OUTER (global) scope, you need the
# `global` keyword.
#
# Without `global`: the function creates a NEW local variable with the
# same name, leaving the global one unchanged.
# With `global`: the function modifies the actual global variable.

x = 5

def g():
    global x    # This tells Python: "I want to modify the GLOBAL x"
    x = 7       # Now this changes the global x, not a local one

g()
print(x)
# Output: 7
#
# Without the `global` keyword, this would print 5, because x=7 inside
# g() would create a LOCAL x, leaving the global x=5 untouched.
#
# BEST PRACTICE: Avoid using `global` in real code. Instead, pass values
# as arguments and return results. Global state makes code harder to
# debug and test.


# =============================================================================
# SECTION 3: Operator Precedence
# =============================================================================
# Python follows standard mathematical precedence (PEMDAS/BODMAS):
#   ** (exponentiation) > unary +/- > * / // % > + - > >> << > comparisons > not > and > or
#
# KEY RULE: ** (exponentiation) is RIGHT-ASSOCIATIVE
#   2**3**2 is evaluated as 2**(3**2) = 2**9 = 512
#   NOT as (2**3)**2 = 8**2 = 64
#   Right-associative means: evaluate from RIGHT to LEFT

x = 2 ** 3
print(f"2 ** 3 = {x}")
# Output: 2 ** 3 = 8

a = 2 ** 3 ** 2       # Right-associative: 2 ** (3**2) = 2 ** 9 = 512
b = 2 * 2 * 2 * 2 * 2 * 2    # 2^6 = 64
c = 8 * 8 * 8         # 512
print(f"2**3**2 = {a}")   # 512
print(f"2^6 = {b}")        # 64
print(f"8^3 = {c}")        # 512
# Note: a == c == 512, but b == 64
# This confirms 2**3**2 = 2**9 = 512, not (2**3)**2 = 64


# =============================================================================
# SECTION 4: List Identity and the += Operator
# =============================================================================
# In Python, every object has an ID (memory address).
# For LISTS, += modifies the list IN-PLACE (same object, same ID).
# For LISTS, + creates a NEW list (different object, different ID).
#
# This is because lists are MUTABLE (can be changed in place).
# For immutable types like int/str/tuple, += always creates a new object.

a = [1, 2, 3, 4]
print("Original ID:", id(a))
a += [3, 4, 5]             # In-place! Same list, same ID
print("Result list:", a)
print("After += ID:", id(a))
# The IDs are the SAME because += on a list calls __iadd__ (in-place add)
# which extends the existing list rather than creating a new one.
#
# Compare with:
#   a = a + [3, 4, 5]      # This creates a NEW list and reassigns a
#   # The ID would CHANGE because a now points to a different object.


# =============================================================================
# SECTION 5: Integer Division
# =============================================================================
# // is integer division (floor division) -- it rounds DOWN to the nearest
# whole number (toward negative infinity).

a = 10 // 3
print(f"10 // 3 = {a}")
# Output: 10 // 3 = 3
#
# More examples:
#   7 // 2 = 3      (not 3.5)
#   -7 // 2 = -4    (rounds DOWN, not toward zero!)
#   7 // -2 = -4    (same: rounds DOWN)


# =============================================================================
# SECTION 6: Prime Number Checking
# =============================================================================
# A prime number is a number greater than 1 that has no divisors other
# than 1 and itself.
# Examples: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, ...
# Non-primes: 0, 1, 4 (2x2), 6 (2x3), 8 (2x4), 9 (3x3), ...

# ---- Approach 1: For loop with for-else ----
# Python's for-else: the `else` block runs ONLY if the loop completed
# WITHOUT hitting a `break`. This is perfect for prime checking!
#
# Time Complexity: O(n) -- checks every number from 2 to n-1
# Space Complexity: O(1)

n = 27
is_prime = True
if n < 2:
    print("Number is not Prime")

for i in range(2, n):
    if n % i == 0:
        is_prime = False
        print(f"Number {n} is not Prime")
        break
else:
    # This else belongs to the FOR loop, not the IF!
    # It runs only if the loop finished without break
    print(f"{n} is Prime")

# Output: Number 27 is not Prime (because 27 % 3 == 0)


# ---- Approach 2: While loop with sqrt optimization ----
# KEY OPTIMIZATION: You only need to check divisors up to sqrt(n).
# Why? If n = a * b and a <= b, then a <= sqrt(n).
# So if no divisor is found up to sqrt(n), n must be prime.
#
# Time Complexity: O(sqrt(n)) -- MUCH faster than O(n)!
#   For n = 1,000,000: O(n) checks 999,998 numbers
#                       O(sqrt(n)) checks only ~1,000 numbers
# Space Complexity: O(1)

import math

n = int(input("\nPrime check (while loop) - Enter a number: "))
i = 2
if n < 2:
    print(f"Number {n} is not Prime")
else:
    while i <= math.sqrt(n):   # Only check up to sqrt(n)
        if n % i == 0:
            print(f"{n} is not Prime")
            break
        i = i + 1
    else:
        # while-else: runs only if the loop finished without break
        print(f"{n} is Prime")


# ---- Approach 3: Function-based prime check ----
# Wrapping the logic in a function makes it reusable.
#
# Time Complexity: O(n) -- checks range(2, number)
# Space Complexity: O(1)
#
# NOTE: This checks range(2, number) which is O(n). To optimize to
# O(sqrt(n)), change the range to range(2, int(math.sqrt(number)) + 1).
# The +1 is needed because range() is exclusive on the upper end.

number = int(input("Function prime check - Enter a number: "))

def check_prime(number):
    """Check if a number is prime. Returns 'Prime' or 'Not Prime'."""
    if number < 2:
        return "Not Prime"
    for i in range(2, number):   # O(n) -- could be optimized to O(sqrt(n))
        if number % i == 0:
            return "Not Prime"
    else:
        return "Prime"

print(f"{number} is {check_prime(number)}")

# Optimized version (for reference):
# def check_prime_fast(number):
#     if number < 2:
#         return "Not Prime"
#     if number == 2:
#         return "Prime"
#     if number % 2 == 0:
#         return "Not Prime"
#     for i in range(3, int(math.sqrt(number)) + 1, 2):  # Only odd divisors
#         if number % i == 0:
#             return "Not Prime"
#     return "Prime"
#
# This is O(sqrt(n)/2) = O(sqrt(n)), and skips even numbers for extra speed.


# =============================================================================
# SECTION 7: Print All Primes in a Range
# =============================================================================
# Given a lower and upper limit, print all prime numbers in that range.
#
# BUG FIX: The original code had:
#   for i in range(lower_limit, upper_limit, upper_limit+1):
#   if
# This was incomplete and had a wrong step value. The step should be 1
# (check every number), not upper_limit+1 (which would skip almost everything).
#
# Time Complexity: O((upper - lower) * sqrt(n)) if using optimized check
#                  O((upper - lower) * n) with the basic check_prime
# Space Complexity: O(1)

lower_limit = int(input("\nPrimes in range - Enter lower limit: "))
upper_limit = int(input("Primes in range - Enter upper limit: "))

print(f"\nPrime numbers between {lower_limit} and {upper_limit}:")
for i in range(lower_limit, upper_limit + 1):   # +1 to include upper_limit
    if check_prime(i) == "Prime":
        print(i, end=" ")
print()  # Newline after the list

# Example: lower=10, upper=30
# Output: 11 13 17 19 23 29


# =============================================================================
# SECTION 8: Loop Variable Scope
# =============================================================================
# In Python, loop variables are NOT confined to the loop body.
# After a for loop ends, the loop variable retains its LAST value.
# This is different from languages like Java/C++ where loop variables
# are scoped to the loop.

i = 5                  # i starts as 5
for i in range(3):     # i takes values 0, 1, 2
    print(i)
print(f"After loop: i = {i}")
# Output:
# 0
# 1
# 2
# After loop: i = 2    (NOT 5! The for loop overwrote i)
#
# This is a common source of bugs! If you use `i` as a loop variable,
# it will overwrite any existing variable named `i` in the same scope.


# =============================================================================
# SECTION 9: while-else and the `pass` Statement
# =============================================================================
# while-else: The `else` block after a while loop runs ONLY if the loop
# ended normally (condition became False), NOT if it was exited via `break`.
#
# pass: A placeholder that does absolutely nothing. Used when Python
# requires a statement syntactically but you don't want to do anything.
# Common uses: empty function bodies, empty if/else branches, TODO placeholders.

i = 1
while i < 5:
    print(i)
    i += 1
    if i == 3:
        pass       # Does nothing! Loop continues normally.
                   # If this were `break`, the else block would NOT run.
else:
    print("While loop else block")

# Output:
# 1
# 2
# 3
# 4
# While loop else block
#
# Walkthrough:
# i=1: print 1, i becomes 2. i==3? No, pass skipped.
# i=2: print 2, i becomes 3. i==3? Yes, but pass does nothing.
# i=3: print 3, i becomes 4. i==3? No, pass skipped.
# i=4: print 4, i becomes 5. i==3? No, pass skipped.
# i=5: while condition (5 < 5) is False, loop ends NORMALLY.
# Since no `break` was hit, the else block runs.
#
# Compare: If `pass` were `break` when i==3:
#   Output would be: 1, 2
#   The else block would NOT run because loop was broken.


# =============================================================================
# SECTION 10: Key Takeaways
# =============================================================================
# 1. Function tracing: Follow the call stack step by step. Watch for
#    discarded return values and unused variables.
#
# 2. `global` keyword: Needed to modify a global variable inside a function.
#    Avoid in real code -- pass arguments and return results instead.
#
# 3. Operator precedence: ** is right-associative (2**3**2 = 512, not 64).
#    Bitwise operators have LOWER precedence than arithmetic.
#
# 4. List += is in-place (same ID), but list + creates a new list.
#
# 5. Prime checking:
#    - Basic: O(n), check all numbers from 2 to n-1
#    - Optimized: O(sqrt(n)), check only up to sqrt(n)
#    - Further: skip even numbers after checking 2
#
# 6. for-else / while-else: the else runs only if no `break` occurred.
#
# 7. Loop variables in Python leak into the enclosing scope -- be careful!
#
# 8. `pass` is a no-op placeholder -- it does absolutely nothing.
