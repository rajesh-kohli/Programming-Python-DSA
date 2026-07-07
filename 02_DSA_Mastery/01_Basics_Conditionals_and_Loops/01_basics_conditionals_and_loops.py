###############################################################################
#                    01 - Basics, Conditionals, and Loops                     #
###############################################################################

# =============================================================================
# SECTION 1: Basic Math & Variable Assignment
# =============================================================================

def math_basics():
    a = 10
    b = 3
    
    print(f"Addition: {a} + {b} = {a + b}")
    print(f"Subtraction: {a} - {b} = {a - b}")
    print(f"Multiplication: {a} * {b} = {a * b}")
    
    # Division Types
    print(f"Float Division: {a} / {b} = {a / b}")    # Output: 3.333...
    print(f"Integer/Floor Division: {a} // {b} = {a // b}") # Output: 3
    print(f"Modulo (Remainder): {a} % {b} = {a % b}")   # Output: 1
    
    # Exponentiation
    print(f"Exponentiation: {a} ** {b} = {a ** b}") # Output: 1000

# =============================================================================
# SECTION 2: Conditional Logic (if/elif/else)
# =============================================================================

def check_number_sign(n: int) -> str:
    if n > 0:
        return "Positive"
    elif n < 0:
        return "Negative"
    else:
        return "Zero"

def is_even(n: int) -> bool:
    # Uses modulo to check for remainder
    return n % 2 == 0

def leap_year_check(year: int) -> bool:
    # A year is a leap year if divisible by 4.
    # EXCEPT if it's divisible by 100, then it's NOT a leap year.
    # UNLESS it's also divisible by 400.
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

# =============================================================================
# SECTION 3: Loops (while, for, break, continue)
# =============================================================================

def while_loop_example(limit: int):
    print("While Loop Counting:")
    i = 0
    while i < limit:
        print(i, end=" ")
        i += 1
    print()

def for_loop_range_examples():
    # range(stop) -> 0 to stop-1
    print("range(5):", list(range(5)))
    
    # range(start, stop) -> start to stop-1
    print("range(2, 6):", list(range(2, 6)))
    
    # range(start, stop, step)
    print("range(1, 10, 2):", list(range(1, 10, 2)))
    
    # Reverse iteration
    print("range(5, 0, -1):", list(range(5, 0, -1)))

def break_and_continue_example():
    print("Break and Continue Example:")
    for i in range(1, 10):
        if i == 3:
            print("Skipping 3 (continue)")
            continue # Skips the rest of this iteration
        if i == 7:
            print("Breaking at 7 (break)")
            break # Exits the loop entirely
        print(f"Processing {i}")

def for_else_loop(target: int):
    # 'else' executes only if the loop does NOT hit a 'break'
    print(f"Searching for {target}...")
    for i in range(1, 6):
        if i == target:
            print("Found target! Breaking.")
            break
    else:
        print("Target not found. Loop finished naturally.")

# --- Practice Skeletons ---

def practice_fizz_buzz(n: int):
    """
    Print numbers 1 to n.
    If multiple of 3, print "Fizz".
    If multiple of 5, print "Buzz".
    If multiple of both, print "FizzBuzz".
    Otherwise, print the number.
    """
    pass

def practice_sum_of_n(n: int) -> int:
    """ Return the sum of all numbers from 1 to n using a loop. """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    print("--- Math Basics ---")
    math_basics()
    
    print("\n--- Conditionals ---")
    print("Is 10 even?", is_even(10))
    print("Is 2024 a leap year?", leap_year_check(2024))
    
    print("\n--- Loops ---")
    while_loop_example(5)
    for_loop_range_examples()
    break_and_continue_example()
    
    for_else_loop(3)
    for_else_loop(10)
    
    print("\n--- Practice Skeletons ---")
    practice_fizz_buzz(15)
    print("Sum of 5:", practice_sum_of_n(5))
