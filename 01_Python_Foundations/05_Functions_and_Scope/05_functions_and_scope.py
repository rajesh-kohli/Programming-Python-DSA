# =============================================================================
# SECTION 1: Functions Basics & Return vs Print
# =============================================================================

def add_print(a, b):
    # This prints the result to the screen but returns None
    print(f"Inside add_print: {a + b}")

def add_return(a, b):
    # This returns the result to the caller
    return a + b

if __name__ == "__main__":
    print("--- Return vs Print ---")
    result_print = add_print(3, 4)
    print(f"Result from add_print: {result_print}")  # Output: None
    
    result_return = add_return(3, 4)
    print(f"Result from add_return: {result_return}")  # Output: 7

# =============================================================================
# SECTION 2: The Call Stack
# =============================================================================
# 
# CALL STACK TRACE:
# 1. Main calls func1(5, 6)
# 2. func1 starts executing.
# 3. func1 calls func2(3, 4). func2 pushes onto stack.
# 4. func2 computes 3*4=12, returns 12, pops off stack.
# 5. func1 discards the return value (it isn't assigned to anything!).
# 6. func1 calls fun3(). fun3 pushes onto stack.
# 7. fun3 returns 99, pops off stack.
# 8. func1 assigns 99 to x.
# 9. func1 finishes and returns None.

def func2(a, b):
    return a * b

def fun3():
    return 99

def func1(a, b):
    # The return value of func2 is discarded because we don't save it!
    func2(3, 4) 
    
    # The return value of fun3 is saved to x, but x is never used.
    x = fun3()
    
    print(f"func1 finished with inputs {a}, {b}")

    print("\n--- Call Stack Trace ---")
    func1(5, 6)


# =============================================================================
# SECTION 3: Scope and Global Variables
# =============================================================================

global_x = 10
global_y = 20

def local_scope_demo():
    # This creates a NEW local variable named global_x.
    # It does NOT modify the global one.
    global_x = 7
    print(f"Inside local_scope_demo, global_x is: {global_x}")

def global_scope_demo():
    # Use the global keyword to modify the outer variable.
    # BEST PRACTICE: Avoid this. Pass arguments and return values instead.
    global global_y
    global_y = 99
    print(f"Inside global_scope_demo, global_y modified to: {global_y}")

    print("\n--- Scope Demo ---")
    print(f"Before local demo, global_x: {global_x}")
    local_scope_demo()
    print(f"After local demo, global_x: {global_x} (Unchanged!)")
    
    print(f"Before global demo, global_y: {global_y}")
    global_scope_demo()
    print(f"After global demo, global_y: {global_y} (Changed!)")

    # LOOP VARIABLE SCOPE LEAK
    # In Python, loop variables leak into the enclosing scope!
    for i in range(3):
        pass
    print(f"\nLoop variable i leaked! Its value is: {i}") # Output: 2

# =============================================================================
# SECTION 4: Python Quirks (Precedence, Identity, Integer Division)
# =============================================================================

    print("\n--- Operator Precedence (Right-Associative **) ---")
    # 2**3**2 is evaluated as 2**(3**2) = 2**9 = 512
    # NOT (2**3)**2 = 8**2 = 64
    print(f"2**3**2 = {2**3**2}") 

    print("\n--- Integer Division (Floor Division) ---")
    # // rounds DOWN to the nearest whole number (towards negative infinity)
    print(f" 7 // 2 = {7 // 2}")    # Output: 3
    print(f"-7 // 2 = {-7 // 2}")   # Output: -4 (not -3!)

    print("\n--- List Identity: += vs = + ---")
    a = [1, 2, 3]
    id_before = id(a)
    
    # In-place addition (modifies original object)
    a += [4]
    print(f"a += [4]: {a}, ID matches before? {id(a) == id_before}") # True
    
    # Creates a NEW list object
    a = a + [5]
    print(f"a = a + [5]: {a}, ID matches before? {id(a) == id_before}") # False

# =============================================================================
# SECTION 5: Prime Checking (Algorithm Evolution)
# =============================================================================

    print("\n--- Prime Checking ---")
    n_prime = 29
    n_not = 27
    n_edge = 1
    
    # APPROACH 1: For-Else loop O(n)
    # The `else` block runs ONLY if the loop finishes without hitting `break`.
    def check_prime_for_else(n):
        if n <= 1:
            return False
        for i in range(2, n):
            if n % i == 0:
                return False
        return True

    print(f"Is {n_prime} prime? {check_prime_for_else(n_prime)}")
    
    # APPROACH 2 & 3: Optimized Function O(sqrt(n))
    # Why sqrt(n)? If a number n is not a prime, it can be factored into a * b.
    # If both a and b were greater than sqrt(n), a * b would be greater than n.
    # So, at least one factor must be <= sqrt(n).
    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
            
        i = 5
        # i * i <= n is the same as i <= sqrt(n) but without float math
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    print(f"Is {n_not} prime? {is_prime(n_not)}")
    
    # PRINT PRIMES IN RANGE
    print("\n--- Primes in Range ---")
    lower = 10
    upper = 50
    # *** BUG (Original): for i in range(lower, upper, upper+1) -> Step size was wrong!
    # *** FIX: range(lower, upper + 1)
    primes = []
    for num in range(lower, upper + 1):
        if is_prime(num):
            primes.append(num)
    print(f"Primes between {lower} and {upper}: {primes}")

# === PRACTICE ZONE ===
# Implement these from scratch:

def practice_is_prime(n):
    """Return True if n is prime, False otherwise. Use O(sqrt(n)) logic."""
    pass

def count_primes_in_range(start, end):
    """Return the count of prime numbers between start and end (inclusive)."""
    pass
