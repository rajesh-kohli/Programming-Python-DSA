# =============================================================================
# SECTION 1: Bitwise Operators
# =============================================================================

if __name__ == "__main__":
    print("--- Basic Bitwise Operators ---")
    # Using 5 (0101) and 3 (0011)
    a = 5
    b = 3
    print(f"{a} & {b}  = {a & b}")   # AND: 0001 (1)
    print(f"{a} | {b}  = {a | b}")   # OR:  0111 (7)
    print(f"{a} ^ {b}  = {a ^ b}")   # XOR: 0110 (6)
    print(f"~{a}     = {~a}")        # NOT: -(5+1) = -6
    print(f"{a} << 1 = {a << 1}")    # Left Shift: 5 * 2^1 = 10 (1010)
    print(f"{a} >> 1 = {a >> 1}")    # Right Shift: 5 / 2^1 = 2 (0010)

    print("\n--- Compound Expressions ---")
    x = 6
    # Trace: x=6
    # expr1: ~x -> -7
    expr1 = ~x
    print(f"~x (x=6) -> {expr1}")

    # Trace: x=6 (0110), 3 (0011). x^3 -> 0101 (5).
    expr2 = x ^ 3
    print(f"x ^ 3 (x=6) -> {expr2}")

    # Trace: x=6 (0110). x>>1 -> 3 (0011). 3 | 2 (0010) -> 3 (0011).
    expr3 = (x >> 1) | 2
    print(f"(x >> 1) | 2 (x=6) -> {expr3}")

    print("\n--- Even/Odd Check using Bitwise AND ---")
    # n & 1 is 1 if n is odd, 0 if n is even. This is faster than n % 2 == 0.
    number = 7
    
    # Version 1: Double IF
    if (number & 1) == 0:
        print(f"{number} is Even (Double-if)")
    if (number & 1) == 1:
        print(f"{number} is Odd (Double-if)")
        
    # Version 2: IF-ELSE (Better)
    if (number & 1) == 0:
        print(f"{number} is Even (If-Else)")
    else:
        print(f"{number} is Odd (If-Else)")

    print("\n--- XOR Swap Trick ---")
    a = 5
    b = 6
    print(f"Before swap: a={a}, b={b}")
    a = a ^ b
    b = a ^ b
    a = a ^ b
    print(f"After swap:  a={a}, b={b}")

# =============================================================================
# SECTION 2: Conditionals & Math Problems
# =============================================================================

    print("\n--- Point and Circle Problem ---")
    # A circle is centered at (0,0) with given radius. Is a point (x,y) inside, outside, or on it?
    radius = 5
    x_cor = 3
    y_cor = 4
    
    # Distance squared from origin = x^2 + y^2
    distance_sq = x_cor**2 + y_cor**2
    radius_sq = radius**2
    
    if distance_sq < radius_sq:
        print("Point is INSIDE the circle")
    elif distance_sq == radius_sq:
        print("Point is ON the circle")
    else:
        print("Point is OUTSIDE the circle")


# =============================================================================
# SECTION 3: DSA Problems (Unique Number)
# =============================================================================
    print("\n--- Unique Number Problem ---")
    # Given an array where every element appears twice except one, find it.
    arr = [2, 3, 5, 4, 5, 3, 4]
    
    # APPROACH 1: Brute Force O(n^2)
    # TIME COMPLEXITY: O(n^2)
    # SPACE COMPLEXITY: O(1)
    unique_bf = None
    for num1 in arr:
        count = 0
        for num2 in arr:
            if num1 == num2:
                count += 1
        if count == 1:
            unique_bf = num1
            break
    print(f"Unique Number (Brute Force): {unique_bf}")
    
    # APPROACH 2: Hash Map / Dictionary O(n) space
    # TIME COMPLEXITY: O(n)
    # SPACE COMPLEXITY: O(n)
    counts = {}
    for num in arr:
        counts[num] = counts.get(num, 0) + 1
    
    unique_hash = None
    for num, count in counts.items():
        if count == 1:
            unique_hash = num
            break
    print(f"Unique Number (Hash Map): {unique_hash}")
    
    # APPROACH 3: Optimal using XOR O(1) space
    # TIME COMPLEXITY: O(n)
    # SPACE COMPLEXITY: O(1)
    # Intuition: x ^ x = 0. All duplicate pairs cancel out to 0. 0 ^ unique = unique.
    unique_xor = 0
    for num in arr:
        unique_xor ^= num
    print(f"Unique Number (Optimal XOR): {unique_xor}")


# === PRACTICE ZONE ===
# Implement these from scratch:

def is_even_bitwise(n):
    """Return True if even, False if odd using bitwise &"""
    pass

def find_unique_number(arr):
    """Return the unique number using XOR"""
    pass

def swap_numbers(a, b):
    """Return (b, a) using XOR trick"""
    pass
