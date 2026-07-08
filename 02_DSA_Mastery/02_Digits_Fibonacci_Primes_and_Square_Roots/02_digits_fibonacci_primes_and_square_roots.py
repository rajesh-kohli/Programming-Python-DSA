###############################################################################
#         02 - Digits, Fibonacci, Primes, and Square Roots                    #
###############################################################################

# =============================================================================
# SECTION 1: Sum of Digits — Three Approaches
# =============================================================================
#
# Core idea: to extract digits from an integer, use two operations in a loop:
#   n % 10   → last digit   (e.g. 1234 % 10 = 4)
#   n // 10  → remove last  (e.g. 1234 // 10 = 123)
#
# Time:  O(log n) — a number with d digits loops d times; d = ⌊log₁₀(n)⌋ + 1
# Space: O(1) for approaches 1 & 2; O(log n) for approach 3 (creates string)
#
# ⚠️  GOTCHA: Never name a variable `sum` — it shadows Python's built-in sum().
#     If you do `sum = 0` then later call `sum(map(...))` → TypeError!
#     Use `total` or `digit_sum` instead.

# ----- Approach 1: Mathematical (% 10 / // 10) — works on integers -----
def sum_of_digits_math(n: int) -> int:
    n = abs(n)          # handle negatives
    total = 0
    while n != 0:
        digit = n % 10  # extract last digit
        total += digit  # accumulate
        n //= 10        # chop off last digit
    return total

# Time: O(log n), Space: O(1)

# ----- Approach 2: String Iteration — treat each character as a digit -----
def sum_of_digits_string(n: int) -> int:
    total = 0
    for ch in str(abs(n)):   # each ch is '0'..'9'
        total += int(ch)
    return total

# Time: O(log n), Space: O(log n) — the string is O(d) where d = # digits

# ----- Approach 3: One-Liner using map() -----
def sum_of_digits_oneliner(n: int) -> int:
    return sum(map(int, str(abs(n))))  # map(int, ...) converts each char to int

# Time: O(log n), Space: O(log n)


# =============================================================================
# SECTION 2: Reverse a Number — Two Approaches
# =============================================================================
#
# ----- Core idea (mathematical) -----
# Build the reversed number digit by digit:
#   1. digit = n % 10          → extract last digit
#   2. rev = rev * 10 + digit  → shift left and place digit
#   3. n //= 10                → remove last digit
#
# Walkthrough for n = 123, rev = 0:
#   Iter 1: digit=3, rev = 0*10+3 = 3,   n = 12
#   Iter 2: digit=2, rev = 3*10+2 = 32,  n = 1
#   Iter 3: digit=1, rev = 32*10+1 = 321, n = 0
#   Answer: 321

# ----- Approach 1: Mathematical (integer arithmetic) -----
def reverse_integer_math(n: int) -> int:
    sign = -1 if n < 0 else 1
    n = abs(n)
    rev = 0
    while n != 0:
        digit = n % 10
        rev = rev * 10 + digit
        n //= 10
    return rev * sign

# Time: O(log n), Space: O(1) — no extra data structures

# ----- Approach 2: String Slicing ([::-1]) -----
def reverse_integer_string(n: int) -> int:
    sign = -1 if n < 0 else 1
    # str(abs(n))[::-1] traverses the string backwards
    # step=-1 means: start from end, stop at beginning
    return sign * int(str(abs(n))[::-1])

# Time: O(log n), Space: O(log n) — creates a new reversed string object


# =============================================================================
# SECTION 3: Fibonacci Sequence — Three Implementations
# =============================================================================
#
# Sequence:  0  1  1  2  3  5  8  13  21  34  55 ...
# Index:     0  1  2  3  4  5  6   7   8   9  10
#
# F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)
#
# Chain-of-boxes:
#   [0] + [1] = [1] + [2] = [3] + [5] = [8] ...
#   Each new number is the sum of the two immediately before it.

# ----- Approach 1: Recursive (Naive) — NEVER use in interviews -----
def fibonacci_recursive(n: int) -> int:
    """
    Computes fib(n) by branching into two recursive calls.
    The call tree has exponential width — fib(5) calls fib(4)+fib(3),
    which call fib(3)+fib(2) and fib(2)+fib(1), recomputing the same
    values over and over.
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# Time: O(2^n) — exponential (recomputes the same sub-problems)
# Space: O(n) — maximum call stack depth

# ----- Approach 2: Iterative with explicit c variable (Clearest) -----
def fibonacci_iterative_explicit(n: int) -> int:
    """
    Uses variables a (fib(k)) and b (fib(k+1)) and slides the window forward.
    Computes next = a + b, then shifts: a = b, b = next.

    Walkthrough for n = 6:
      Start: a=0, b=1
      i=2: c=0+1=1,  a=1, b=1   (fib(2))
      i=3: c=1+1=2,  a=1, b=2   (fib(3))
      i=4: c=1+2=3,  a=2, b=3   (fib(4))
      i=5: c=2+3=5,  a=3, b=5   (fib(5))
      i=6: c=3+5=8,  a=5, b=8   (fib(6))
      Answer: c = 8
    """
    if n == 0 or n == 1:
        return n
    a, b = 0, 1
    for i in range(2, n + 1):   # runs n-1 times
        c = a + b
        a = b
        b = c
    return c

# Time: O(n), Space: O(1)

# ----- Approach 3: Iterative with Tuple Swap (Most Pythonic) -----
def fibonacci_iterative_pythonic(n: int) -> int:
    """
    Uses simultaneous tuple assignment: a, b = b, a + b
    Python evaluates the entire RHS using OLD values before assigning.
    This eliminates the need for a temporary variable c.

    Trace for n = 6 (starts at fib(0), loop runs n times):
      a=0, b=1
      i=0: a=1, b=0+1=1    → a is fib(1)
      i=1: a=1, b=1+1=2    → a is fib(2)
      i=2: a=2, b=1+2=3    → a is fib(3)
      i=3: a=3, b=2+3=5    → a is fib(4)
      i=4: a=5, b=3+5=8    → a is fib(5)
      i=5: a=8, b=5+8=13   → a is fib(6)
      return a = 8 ✓
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Time: O(n), Space: O(1)

# ----- Approach 4: While-loop version (from LPLV26MAY) -----
def fibonacci_while_loop(n: int) -> int:
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    i = 1
    while i <= n - 1:   # runs n-1 times
        c = a + b
        a = b
        b = c
        i += 1
    return c

# Time: O(n), Space: O(1)


# =============================================================================
# SECTION 4: Check if a Number IS a Fibonacci Number
# =============================================================================
#
# Strategy: generate Fibonacci numbers one by one.
#   - If we hit the target exactly → True
#   - If we overshoot (generated > target) → False (it's between two Fibs)
#
# Uses the 'while True + break' sentinel pattern since we don't know
# how many iterations until we hit or pass the target.
#
# Walkthrough: Is 8 a Fibonacci number?
#   Sequence: 0, 1, 1, 2, 3, 5, 8 → hit 8 exactly → True
#
# Walkthrough: Is 6 a Fibonacci number?
#   Sequence: 0, 1, 1, 2, 3, 5, 8 → jumped from 5 to 8, skipped 6 → False
#
# Time:  O(log n) — Fibonacci numbers grow as ~φ^k (φ ≈ 1.618), so we reach n
#         in about log_φ(n) steps. Often stated as O(log n).
# Space: O(1) — only 3 variables

def is_fibonacci_number(n: int) -> bool:
    if n == 0 or n == 1:
        return True         # 0 and 1 are both Fibonacci numbers
    a, b = 0, 1
    while True:
        c = a + b
        if c == n:
            return True     # Hit the target exactly
        elif c > n:
            return False    # Overshot — n is NOT in the sequence
        else:
            a = b           # Slide window forward
            b = c


# =============================================================================
# SECTION 5: Prime Numbers — Three Levels of Optimization
# =============================================================================
#
# A prime is a number > 1 with no divisors other than 1 and itself.
# Primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, ...
# NOT prime: 0, 1, 4, 6, 8, 9, 10, 12, ...
#
# WHY CHECK ONLY UP TO √n?
# If n = a × b, one of a or b must be ≤ √n.
# Factor pairs of 36 (√36 = 6):
#   (1,36) (2,18) (3,12) (4,9) (6,6)
#   Every pair has at least one factor ≤ 6.
#   So checking 2 to 6 is sufficient — past 6 we'd only re-find the same pairs.
#
# ⚠️  FLOATING POINT WARNING: Prefer `i * i <= n` over `i <= n ** 0.5`
#     `n ** 0.5` computes a float which suffers from precision loss
#     (the Pigeonhole Principle: infinite reals, finite binary memory).
#     `i * i <= n` is pure integer arithmetic — always exact, no rounding.

# ----- Level 1: Naive — O(n) -----
# Check every number from 2 to n-1. Simple but too slow for large n.
def is_prime_naive(n: int) -> bool:
    if n <= 1: return False
    for i in range(2, n):       # checks 2, 3, 4, ..., n-1
        if n % i == 0:
            return False
    return True

# Time: O(n), Space: O(1)

# ----- Level 2: Optimized — O(√n) using while-else -----
# Only check up to √n. Use Python's while-else for clean structure.
# 'else' on a while/for loop runs ONLY if the loop exits naturally (no break).
def is_prime_while_else(n: int) -> bool:
    if n <= 1: return False
    if n == 2: return True      # 2 is prime (only even prime)
    i = 2
    while i * i <= n:           # ← use i*i not i <= n**0.5 (avoids float)
        if n % i == 0:
            return False        # found a divisor → not prime
        i += 1
    return True                 # no divisor found → prime

# Time: O(√n), Space: O(1)

# ----- Level 2b: Optimized — O(√n) using flag variable -----
# Same algorithm, using an explicit flag. This style ports to Java/C++ directly.
def is_prime_flag(n: int) -> bool:
    if n <= 1: return False
    if n == 2: return True
    i = 2
    is_prime = True             # assume prime until proven otherwise
    while i * i <= n:
        if n % i == 0:
            is_prime = False
            break               # no need to keep checking
        i += 1
    return is_prime

# Time: O(√n), Space: O(1)

# ----- Level 2c: Optimized — O(√n) using check-variable-after-loop -----
# After the loop, if i * i > n, the loop completed without finding a divisor.
def is_prime_check_var(n: int) -> bool:
    if n <= 1: return False
    if n == 2: return True
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return i * i > n            # True only if loop ran fully without breaking

# Time: O(√n), Space: O(1)

# ----- Level 3: 6k±1 Trick — O(√n / 3) -----
# All primes > 3 are of the form 6k ± 1.
# (Because all integers 6k, 6k+2, 6k+3, 6k+4 are divisible by 2 or 3.)
# We can skip multiples of 2 and 3 entirely, checking only 5, 7, 11, 13, 17, 19 ...
def is_prime_optimized_6k(n: int) -> bool:
    if n <= 1: return False
    if n <= 3: return True          # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0: return False  # eliminates all even and 3-mult
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:  # checks i and i+2 (6k-1 and 6k+1)
            return False
        i += 6                      # jump to next 6k group
    return True

# Time: O(√n / 3) — checks ~1/3 of numbers, Space: O(1)

# ----- Comparison Table -----
# | Level | Range Checked    | Time       | Notes                                |
# |-------|------------------|------------|--------------------------------------|
# | 1     | 2 to n-1         | O(n)       | Naive brute force                    |
# | 2     | 2 to √n          | O(√n)      | Standard interview answer            |
# | 3     | 5,7,11,13...     | O(√n / 3)  | 6k±1 trick; skips 2 and 3 multiples |


# =============================================================================
# SECTION 6: Square Root — Three Levels of Precision
# =============================================================================
#
# Find √n WITHOUT using math.sqrt() or n ** 0.5.

# ----- Level 1: Integer Square Root — Linear Scan, O(√n) -----
# Count up from 0 until ans*ans > n, then step back by 1.
#
# Walkthrough for n = 64:
#   ans=8: 64 <= 64 ✓,  ans=9: 81 > 64 ✗  → answer = 9-1 = 8
#
# Walkthrough for n = 30:
#   ans=5: 25 <= 30 ✓,  ans=6: 36 > 30 ✗  → answer = 6-1 = 5

def integer_sqrt_linear(n: int) -> int:
    if n < 0: return -1     # undefined for negative
    ans = 0
    while ans * ans <= n:
        ans += 1
    return ans - 1          # step back one (we overshot by 1)

# Time: O(√n), Space: O(1)

# ----- Level 2: Decimal Precision — Iterative Refinement -----
# After finding integer part, refine with decreasing increments:
#   +0.1 for tenths, +0.01 for hundredths, +0.001 for thousandths
#
# Walkthrough for n=30, p=2 (2 decimal places):
#   Integer part:   ans=5 (5*5=25<=30, 6*6=36>30)
#   Tenths:         ans=5.4 (5.5*5.5=30.25>30)
#   Hundredths:     ans=5.47 (5.48*5.48=30.03>30)
#   Answer: 5.47

def sqrt_decimal_precision(n: int, p: int) -> float:
    """
    Returns √n rounded to p decimal places using iterative refinement.
    """
    ans = 0
    while ans * ans <= n:       # Step 1: find integer part
        ans += 1
    ans -= 1                    # step back (we went one too far)

    inc_fac = 0.1               # start at 0.1 for tenths place
    for _ in range(p):          # one pass per decimal place
        while ans * ans <= n:
            ans += inc_fac
        ans -= inc_fac          # step back (overshot this decimal place)
        inc_fac /= 10           # 0.1 → 0.01 → 0.001 → ...

    return round(ans, p)

# Time: O(√n + 10*p) — integer part is O(√n), each decimal place ≤ 10 iters
# Space: O(1)

# ----- Level 3: Binary Search — O(log n) -----
# Since f(x) = x² is monotonically increasing, we can binary search [0, n//2].
# At each step, compare mid² to n and halve the search space.
#
# This is the OPTIMAL approach and what you'd use in a real interview.
#
# Walkthrough for n = 30:
#   lo=0, hi=15
#   mid=7: 49 > 30  → hi=6
#   mid=3: 9  < 30  → lo=4, ans=3
#   mid=5: 25 < 30  → lo=6, ans=5
#   mid=6: 36 > 30  → hi=5
#   lo > hi, stop. Return ans = 5 ✓

def integer_sqrt_binary_search(x: int) -> int:
    if x < 0: return -1
    if x < 2: return x          # sqrt(0)=0, sqrt(1)=1

    lo, hi = 2, x // 2         # answer must be in [2, x//2] for x >= 4
    ans = 1

    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid

        if sq == x:
            return mid          # perfect square
        elif sq < x:
            ans = mid           # best floor answer so far
            lo = mid + 1        # try larger
        else:
            hi = mid - 1        # try smaller

    return ans

# Time: O(log n) — halving the search space each iteration, Space: O(1)

# ----- Comparison Table -----
# | Level | Approach           | Time       | Returns              |
# |-------|--------------------|------------|----------------------|
# | 1     | Linear scan        | O(√n)      | Integer floor        |
# | 2     | Iterative refine   | O(√n+10p)  | Float to p decimals  |
# | 3     | Binary search      | O(log n)   | Integer floor        |


# =============================================================================
# SECTION 7: Largest of N Numbers (float('-inf') pattern)
# =============================================================================
#
# Key insight: initialize max to -infinity so ANY real number will be larger.
# Starting with 0 fails when all inputs are negative (e.g., [-5, -3, -1]).
#
# Infinity options in Python:
#   float('inf')  / float('-inf')  — for float comparisons (most common)
#   math.inf      / -math.inf      — equivalent
#   sys.maxsize   / -sys.maxsize-1 — use only when problem specifies integer bounds

def largest_of_n(numbers: list) -> float:
    """
    Single-pass O(n) maximum finder using -infinity initialization.
    Correctly handles all-negative lists.
    """
    max_so_far = float('-inf')
    for num in numbers:
        if num > max_so_far:
            max_so_far = num
    return max_so_far

# Time: O(n), Space: O(1)


# =============================================================================
# SECTION 8: continue — The While-Loop Infinite Loop Trap
# =============================================================================
#
# `continue` in a for loop is safe — the loop variable increments automatically.
# `continue` in a while loop is DANGEROUS if the update (i += 1) is AFTER continue.
#
# DANGEROUS (infinite loop):
#   i = 0
#   while i < 10:
#       if i == 5:
#           continue      ← jumps back to "while i < 10"
#       print(i)
#       i += 1            ← NEVER REACHED when i == 5
#
# FIX: place the update BEFORE the continue (or use a for loop):
#   i = 0
#   while i < 10:
#       i += 1            ← always runs first
#       if i == 5:
#           continue
#       print(i)

def demonstrate_continue():
    print("for-loop continue (safe):")
    for i in range(8):
        if i == 5:
            continue    # loop variable auto-increments — no infinite loop risk
        print(i, end=" ")
    print()


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_sum_of_digits(n: int) -> int:
    """
    Return the sum of digits of n using the % 10 / // 10 math loop.
    Do NOT convert to string.
    Example: 1234 → 10
    """
    pass

def practice_reverse_integer(n: int) -> int:
    """
    Reverse the digits of n using the math approach (rev = rev*10 + digit).
    Handle negatives: -123 → -321
    Example: 12345 → 54321
    """
    pass

def practice_is_palindrome_number(n: int) -> bool:
    """
    A number is a palindrome if it reads the same forwards and backwards.
    Approach: reverse n mathematically and compare to original.
    Edge case: negative numbers are NEVER palindromes.
    Example: 121 → True, -121 → False, 10 → False
    """
    pass

def practice_fibonacci_nth(n: int) -> int:
    """
    Return the nth Fibonacci number iteratively in O(n) time, O(1) space.
    Use the tuple-swap approach: a, b = b, a + b
    Example: n=10 → 55
    """
    pass

def practice_is_fibonacci(n: int) -> bool:
    """
    Return True if n is a Fibonacci number, False otherwise.
    Use the while True + break sentinel pattern.
    Example: 8 → True, 6 → False
    """
    pass

def practice_is_prime(n: int) -> bool:
    """
    Return True if n is prime. Use the O(√n) approach with `i * i <= n`.
    Remember edge cases: n <= 1 is never prime. n == 2 is prime.
    """
    pass

def practice_integer_sqrt(x: int) -> int:
    """
    Return the integer (floor) square root of x WITHOUT using math.sqrt or x**0.5.
    Use binary search for O(log n) performance.
    Example: 64 → 8, 10 → 3
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    SEP = "=" * 60

    print(SEP)
    print("SECTION 1: Sum of Digits")
    print(SEP)
    print("sum_of_digits_math(1234):     ", sum_of_digits_math(1234))
    print("sum_of_digits_string(1234):   ", sum_of_digits_string(1234))
    print("sum_of_digits_oneliner(1234): ", sum_of_digits_oneliner(1234))
    print("sum_of_digits_math(-987):     ", sum_of_digits_math(-987))  # handles negatives

    print(f"\n{SEP}")
    print("SECTION 2: Reverse Integer")
    print(SEP)
    print("reverse_integer_math(12345):   ", reverse_integer_math(12345))
    print("reverse_integer_string(12345): ", reverse_integer_string(12345))
    print("reverse_integer_math(-123):    ", reverse_integer_math(-123))

    print(f"\n{SEP}")
    print("SECTION 3: Fibonacci")
    print(SEP)
    print("fibonacci_recursive(10):        ", fibonacci_recursive(10))
    print("fibonacci_iterative_explicit(10):", fibonacci_iterative_explicit(10))
    print("fibonacci_iterative_pythonic(10):", fibonacci_iterative_pythonic(10))
    print("fibonacci_while_loop(10):       ", fibonacci_while_loop(10))
    # Verify all four agree
    assert all(f(10) == 55 for f in [
        fibonacci_recursive,
        fibonacci_iterative_explicit,
        fibonacci_iterative_pythonic,
        fibonacci_while_loop
    ]), "Fibonacci implementations disagree!"
    print("✓ All 4 implementations agree: fib(10) = 55")

    print(f"\n{SEP}")
    print("SECTION 4: Is Fibonacci Number?")
    print(SEP)
    print("is_fibonacci(0):  ", is_fibonacci_number(0))   # True
    print("is_fibonacci(1):  ", is_fibonacci_number(1))   # True
    print("is_fibonacci(8):  ", is_fibonacci_number(8))   # True
    print("is_fibonacci(6):  ", is_fibonacci_number(6))   # False
    print("is_fibonacci(13): ", is_fibonacci_number(13))  # True
    print("is_fibonacci(14): ", is_fibonacci_number(14))  # False

    print(f"\n{SEP}")
    print("SECTION 5: Prime Numbers")
    print(SEP)
    tests = [0, 1, 2, 3, 4, 97, 100]
    for t in tests:
        naive = is_prime_naive(t)
        opt   = is_prime_while_else(t)
        adv   = is_prime_optimized_6k(t)
        match = "✓" if naive == opt == adv else "✗ MISMATCH"
        print(f"  n={t:3d}: naive={naive}, while-else={opt}, 6k±1={adv}  {match}")

    print(f"\n{SEP}")
    print("SECTION 6: Square Root")
    print(SEP)
    for x in [0, 1, 4, 10, 30, 64, 100]:
        lin = integer_sqrt_linear(x)
        bs  = integer_sqrt_binary_search(x)
        match = "✓" if lin == bs else "✗ MISMATCH"
        print(f"  sqrt({x:3d}): linear={lin}, binary_search={bs}  {match}")
    print("sqrt_decimal_precision(30, 2):", sqrt_decimal_precision(30, 2))
    print("sqrt_decimal_precision(2,  4):", sqrt_decimal_precision(2, 4))

    print(f"\n{SEP}")
    print("SECTION 7: Largest of N")
    print(SEP)
    print("largest_of_n([3,7,2,9,1]):    ", largest_of_n([3, 7, 2, 9, 1]))
    print("largest_of_n([-5,-3,-1]):     ", largest_of_n([-5, -3, -1]))   # correctly returns -1

    print(f"\n{SEP}")
    print("SECTION 8: continue demo")
    print(SEP)
    demonstrate_continue()

    print(f"\n{SEP}")
    print("PRACTICE SKELETONS")
    print(SEP)
    print("sum_of_digits(1234):     ", practice_sum_of_digits(1234))
    print("reverse_integer(12345):  ", practice_reverse_integer(12345))
    print("is_palindrome(121):      ", practice_is_palindrome_number(121))
    print("fibonacci_nth(10):       ", practice_fibonacci_nth(10))
    print("is_fibonacci(8):         ", practice_is_fibonacci(8))
    print("is_prime(97):            ", practice_is_prime(97))
    print("integer_sqrt(64):        ", practice_integer_sqrt(64))
