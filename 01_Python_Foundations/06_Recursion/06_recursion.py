# =============================================================================
# SECTION 1: Basic Recursion
# =============================================================================

def countdown(n):
    # Base Case
    if n <= 0:
        print("Liftoff!")
        return
    # Recursive Work
    print(n)
    # Leap of Faith (call with smaller input)
    countdown(n - 1)

def factorial(n):
    # TIME: O(n), SPACE: O(n) due to call stack
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def recursive_mul(a, b):
    # a * b is equivalent to adding a to itself b times
    if b == 0:
        return 0
    return a + recursive_mul(a, b - 1)

def sum_natural(n):
    # Sum of first N natural numbers. Note: n*(n+1)/2 is O(1).
    if n <= 0:
        return 0
    return n + sum_natural(n - 1)

# =============================================================================
# SECTION 2: Intermediate Recursion
# =============================================================================

def power_naive(a, n):
    # TIME: O(n), SPACE: O(n)
    if n == 0:
        return 1
    return a * power_naive(a, n - 1)

def power_fast(a, n):
    # FAST EXPONENTIATION
    # TIME: O(log n), SPACE: O(log n)
    if n == 0:
        return 1
    half_power = power_fast(a, n // 2)
    if n % 2 == 0:
        return half_power * half_power
    else:
        return a * half_power * half_power

def sum_digits(n):
    # n % 10 extracts last digit, n // 10 removes it
    if n == 0:
        return 0
    return (n % 10) + sum_digits(n // 10)

def reverse_string(s):
    # NOTE: Python string slicing s[1:] is O(n), making this entire function O(n^2).
    # Iterative s[::-1] is O(n) and preferred in Python.
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]

def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])

def count_char(s, char):
    if not s:
        return 0
    match = 1 if s[0] == char else 0
    return match + count_char(s[1:], char)

def print_both(n):
    # Demonstrates code executing before AND after the recursive call
    if n <= 0:
        return
    print(f"Pre-call: {n}")
    print_both(n - 1)
    print(f"Post-call: {n}")

# =============================================================================
# SECTION 3: Fibonacci & Complexity Evolution
# =============================================================================

def fib_naive(n):
    # APPROACH 1: Brute Force
    # TIME: O(2^n) - Exponential, terrible performance
    # SPACE: O(n) - Call stack depth is n
    if n == 0: return 0
    if n == 1: return 1
    return fib_naive(n - 1) + fib_naive(n - 2)

def fib_memo(n, memo=None):
    # APPROACH 2: Memoization (Top-Down Dynamic Programming)
    # TIME: O(n) - We only calculate each subproblem once
    # SPACE: O(n) - For the call stack and the memo dictionary
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n == 0: return 0
    if n == 1: return 1
    
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

def fib_iterative(n):
    # APPROACH 3: Iteration
    # TIME: O(n)
    # SPACE: O(1) - BEST APPROACH! No stack overflow risk.
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# =============================================================================
# SECTION 4: DSA Square Root
# =============================================================================

def sqrt_binary_search(n):
    # Find integer square root (floor) using binary search
    # TIME: O(log n), SPACE: O(1)
    if n == 0 or n == 1:
        return n
        
    left, right = 1, n
    ans = 0
    
    while left <= right:
        mid = (left + right) // 2
        if mid * mid == n:
            return mid
        elif mid * mid < n:
            left = mid + 1
            ans = mid  # store floor value
        else:
            right = mid - 1
    return ans

if __name__ == "__main__":
    print("--- Countdown ---")
    countdown(3)
    
    print(f"\nFactorial of 4: {factorial(4)}")
    print(f"Mul 6 * 4: {recursive_mul(6, 4)}")
    print(f"Sum natural 5: {sum_natural(5)}")
    
    print("\n--- Power Function ---")
    print(f"2^10 (naive): {power_naive(2, 10)}")
    print(f"2^10 (fast): {power_fast(2, 10)}")
    
    print("\n--- String/Digit Recursion ---")
    print(f"Sum digits 1234: {sum_digits(1234)}")
    print(f"Reverse 'hello': {reverse_string('hello')}")
    print(f"Is 'racecar' palindrome? {is_palindrome('racecar')}")
    print(f"Count 'l' in 'hello': {count_char('hello', 'l')}")
    
    print("\n--- Fibonacci Evolution ---")
    n_fib = 10
    print(f"Fib({n_fib}) Naive: {fib_naive(n_fib)}")
    print(f"Fib({n_fib}) Memo: {fib_memo(n_fib)}")
    print(f"Fib({n_fib}) Iter: {fib_iterative(n_fib)}")
    
    print("\n--- Square Root (Binary Search) ---")
    print(f"Sqrt(25): {sqrt_binary_search(25)}")
    print(f"Sqrt(24): {sqrt_binary_search(24)}")

# === PRACTICE ZONE ===
# Implement these from scratch:

def factorial_practice(n):
    """Return n!"""
    pass

def fib_practice(n):
    """Return nth Fibonacci number iteratively"""
    pass

def power_fast_practice(a, n):
    """Return a^n in O(log n) time"""
    pass

def is_palindrome_practice(s):
    """Return True if string s is a palindrome using recursion"""
    pass
