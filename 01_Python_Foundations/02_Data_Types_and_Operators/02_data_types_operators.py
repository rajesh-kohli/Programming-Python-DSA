# =============================================================================
# SECTION 1: Python Operators
# =============================================================================

if __name__ == "__main__":
    print("--- Arithmetic Operators ---")
    a = 10
    b = 3
    print(f"{a} + {b} = {a + b}")    # Addition
    print(f"{a} - {b} = {a - b}")    # Subtraction
    print(f"{a} * {b} = {a * b}")    # Multiplication
    print(f"{a} / {b} = {a / b}")    # Float Division (always returns float)
    print(f"{a} // {b} = {a // b}")  # Floor Division (rounds down)
    print(f"{a} % {b} = {a % b}")    # Modulus (remainder)
    print(f"{a} ** {b} = {a ** b}")  # Exponentiation

    print("\n--- Compound Assignment ---")
    c = 5
    c += 2  # Equivalent to c = c + 2
    print(f"c += 2 -> {c}")
    c *= 3
    print(f"c *= 3 -> {c}")

    print("\n--- Membership Operators ---")
    my_list = [1, 2, 3, 4, 5]
    my_set = {1, 2, 3, 4, 5}
    # TIME COMPLEXITY: list `in` is O(n), set `in` is O(1)
    print(f"3 in my_list: {3 in my_list}")
    print(f"6 not in my_set: {6 not in my_set}")

    print("\n--- Identity Operators (is vs ==) ---")
    # == compares values, `is` compares memory addresses
    list1 = [1, 2, 3]
    list2 = [1, 2, 3]
    print(f"list1 == list2: {list1 == list2}")  # True
    print(f"list1 is list2: {list1 is list2}")  # False, different objects in memory

    x = 100
    y = 100
    print(f"100 is 100: {x is y}") # True, due to integer caching (-5 to 256)

# =============================================================================
# SECTION 2: Data Types
# =============================================================================

    print("\n--- Data Types ---")
    print(f"Integer: {type(10)}")
    print(f"Float: {type(10.5)}")
    print(f"Complex: {type(3 + 4j)}") # Note the 'j' instead of 'i'
    print(f"String: {type('hello')}")
    print(f"Boolean: {type(True)}")

    print("\n--- Collections ---")
    # LIST: Mutable, Ordered
    my_list = [10, 20, 30]
    my_list[0] = 99
    print(f"List after mutation: {my_list}")
    print(f"List slicing: {my_list[1:]}")
    print(f"List concatenation: {my_list + [40, 50]}")

    # TUPLE: Immutable, Ordered
    my_tuple = (10, 20, 30)
    # my_tuple[0] = 99  # TypeError: 'tuple' object does not support item assignment
    print(f"Tuple: {my_tuple}")

    # SET: Mutable, Unordered, Unique elements
    my_set = {1, 2, 3, 3, 2, 1}
    print(f"Set (duplicates removed): {my_set}")

    # DICTIONARY: Mutable, Key-Value pairs
    my_dict = {"name": "Alice", "age": 25}
    print(f"Dict: {my_dict}")

    # THE '{}' GOTCHA:
    empty_thing = {}
    print(f"Empty {{}} is a: {type(empty_thing)}") # dict, NOT set!
    empty_set = set()
    print(f"Empty set() is a: {type(empty_set)}")

    # *** BUG FIX DEMO ***
    # BUG: print(dict_1 = {"a": 1}) # SyntaxError: invalid syntax (keyword argument)
    # FIX:
    dict_1 = {"a": 1}
    print(f"dict_1 = {dict_1}")


# =============================================================================
# SECTION 3: DSA Problems
# =============================================================================

    print("\n--- Simple and Compound Interest ---")
    P = 1000
    R = 5
    T = 3
    
    # Simple Interest: SI = (P * R * T) / 100
    si = (P * R * T) / 100
    print(f"Simple Interest for P={P}, R={R}, T={T} is: {si}")
    
    # Compound Interest: CI = P * (1 + R/100)^T - P
    ci = P * (1 + R/100)**T - P
    print(f"Compound Interest for P={P}, R={R}, T={T} is: {ci:.2f}")

    print("\n--- Largest of N numbers ---")
    numbers = [45, 12, 89, 33, 7]
    
    # APPROACH 1: Naive Scan
    # TIME COMPLEXITY: O(n)
    # SPACE COMPLEXITY: O(1)
    largest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = num
    print(f"Largest (Naive Scan): {largest}")

    # APPROACH 2: Built-in max()
    # TIME COMPLEXITY: O(n)
    # SPACE COMPLEXITY: O(1)
    largest_max = max(numbers)
    print(f"Largest (Built-in max): {largest_max}")

# === PRACTICE ZONE ===
# Implement these from scratch:

def calculate_si(p, r, t):
    """Return Simple Interest"""
    pass

def calculate_ci(p, r, t):
    """Return Compound Interest"""
    pass

def find_largest(arr):
    """Return largest element in array without using max()"""
    pass
