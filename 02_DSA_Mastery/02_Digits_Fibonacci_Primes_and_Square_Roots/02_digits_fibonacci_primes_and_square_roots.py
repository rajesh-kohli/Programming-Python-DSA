###############################################################################
#             02 - Digits, Fibonacci, Primes, and Square Roots                #
###############################################################################

# =============================================================================
# SECTION 1: Digit Extraction
# =============================================================================

def reverse_integer(n: int) -> int:
    sign = -1 if n < 0 else 1
    n = abs(n)
    rev = 0
    
    while n > 0:
        digit = n % 10
        rev = rev * 10 + digit
        n = n // 10
        
    return rev * sign

def sum_of_digits(n: int) -> int:
    n = abs(n)
    total = 0
    while n > 0:
        total += n % 10
        n = n // 10
    return total


# =============================================================================
# SECTION 2: Fibonacci Sequence
# =============================================================================

# ----- Approach 1: Recursive (Naive) -----
def fibonacci_recursive(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
# Time: O(2^n), Space: O(n) for call stack

# ----- Approach 2: Iterative (Optimal) -----
def fibonacci_iterative(n: int) -> int:
    if n <= 1:
        return n
        
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
        
    return b
# Time: O(n), Space: O(1)


# =============================================================================
# SECTION 3: Prime Numbers
# =============================================================================

# ----- Approach 1: Naive -----
def is_prime_naive(n: int) -> bool:
    if n <= 1: return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
# Time: O(n)

# ----- Approach 2: Optimized -----
def is_prime_optimized(n: int) -> bool:
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    
    # Check up to sqrt(n)
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
        
    return True
# Time: O(sqrt(n))


# =============================================================================
# SECTION 4: Integer Square Root
# =============================================================================

# ----- Approach: Binary Search (Optimal) -----
def integer_square_root(x: int) -> int:
    if x < 2: return x
    
    lo, hi = 2, x // 2
    ans = 0
    
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        
        if sq == x:
            return mid
        elif sq < x:
            ans = mid  # Store potential floor value
            lo = mid + 1
        else:
            hi = mid - 1
            
    return ans
# Time: O(log x), Space: O(1)


# --- Practice Skeletons ---

def practice_is_palindrome_number(n: int) -> bool:
    """ Check if an integer reads the same forwards and backwards (e.g., 121 -> True) """
    pass

def practice_print_fibonacci_sequence(n: int):
    """ Print the first n Fibonacci numbers """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    print("--- Digits ---")
    print("Reverse 12345:", reverse_integer(12345))
    print("Sum of digits 987:", sum_of_digits(987))
    
    print("\n--- Fibonacci ---")
    print("Fibonacci(10):", fibonacci_iterative(10))
    
    print("\n--- Primes ---")
    print("Is 97 prime?", is_prime_optimized(97))
    print("Is 100 prime?", is_prime_optimized(100))
    
    print("\n--- Square Roots ---")
    print("Integer sqrt(64):", integer_square_root(64))
    print("Integer sqrt(10):", integer_square_root(10))
    
    print("\n--- Practice Skeletons ---")
    print("Is 121 palindrome?", practice_is_palindrome_number(121))
