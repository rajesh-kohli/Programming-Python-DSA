###############################################################################
#                    01 - Basics, Conditionals, and Loops                     #
###############################################################################

# =============================================================================
# SECTION 1: Basic Math & Variable Assignment
# =============================================================================

def math_basics():
    a, b = 10, 3   # Multiple assignment (packing) from L04/007

    print(f"Addition:           {a} + {b} = {a + b}")
    print(f"Subtraction:        {a} - {b} = {a - b}")
    print(f"Multiplication:     {a} * {b} = {a * b}")
    print(f"Float Division:     {a} / {b} = {a / b}")     # Always returns float: 3.333...
    print(f"Integer Division:   {a} // {b} = {a // b}")   # Floor/truncate: 3
    print(f"Modulo (Remainder): {a} % {b} = {a % b}")     # 1  (key for even/odd, digit extraction)
    print(f"Exponentiation:     {a} ** {b} = {a ** b}")   # 1000


# =============================================================================
# SECTION 2: Operator Precedence
# =============================================================================
# From L04/009arithmeticOpsPrecedence.py
# PEMDAS: Parentheses > Exponents > Multiply/Divide > Add/Subtract
# CRITICAL: ** is RIGHT-ASSOCIATIVE. 2**3**2 = 2**(3**2) = 2**9 = 512, NOT 64.

def operator_precedence_demo():
    print("--- Operator Precedence ---")
    print(3 + 5 * 4)       # 23  (* before +)
    print(9 - 8 / 2)       # 5.0 (/ before -, result is float)
    print((3 + 5) * 4)     # 32  (parens override)
    print((9 - 8) / 2)     # 0.5 (parens override)
    print(100 / 10 * 10)   # 100.0 (left-to-right, same precedence)
    print(5 - 2 + 3)       # 6 (left-to-right)
    print(2 ** 3 ** 2)     # 512 (RIGHT-associative: 2**(3**2) = 2**9, NOT (2**3)**2 = 64)


# =============================================================================
# SECTION 3: I/O and Type Casting
# =============================================================================
# From L04/004input.py, 005numericInput.py, 006numericInput2.py
#
# *** NOTE: These functions show the patterns. In a real script, replace
#     the hard-coded values with the actual input() calls shown in comments. ***

def io_type_casting_demo():
    """
    In actual use:
        x = input()                          # reads a raw string
        x = int(input())                     # reads a single integer
        x = float(input())                   # reads a single float
        x, y, z = map(int, input().split())  # reads "1 2 3" → three integers
    """
    # Simulation (no live input):
    raw = "42"
    x = int(raw)
    print(f"int('{raw}') → {x}, type: {type(x).__name__}")   # int

    raw_float = "3.14"
    y = float(raw_float)
    print(f"float('{raw_float}') → {y}, type: {type(y).__name__}")  # float

    # map(int, ...) is the competitive programming input pattern
    raw_line = "10 20 30"
    a, b, c = map(int, raw_line.split())
    print(f"map(int, '{raw_line}'.split()) → a={a}, b={b}, c={c}")


# =============================================================================
# SECTION 4: Variable Packing / Unpacking & Multiple Assignment
# =============================================================================
# From L04/007packingUnpacking.py

def packing_unpacking_demo():
    # Multiple assignment (packing)
    x, y = 5, 2
    print(f"x={x}, y={y}")

    # Pythonic swap — NO temp variable.
    # Python evaluates the RHS as a tuple (y, x) FIRST, then unpacks.
    x, y = y, x
    print(f"After swap: x={x}, y={y}")

    # Starred unpacking — capture the rest into a list
    first, *rest = [1, 2, 3, 4, 5]
    print(f"first={first}, rest={rest}")  # first=1, rest=[2, 3, 4, 5]


# =============================================================================
# SECTION 5: print() Formatting — sep= and end=
# =============================================================================
# From L04/001helloWorld.py

def print_formatting_demo():
    # sep= controls what's printed BETWEEN arguments (default: " ")
    # end= controls what's printed AT THE END (default: "\n")
    print("hello", 50, 2.71, True, 2 + 3, sep="*", end=".\n")  # hello*50*2.71*True*5.

    # Printing on one line using end=" "
    for i in range(5):
        print(i, end=" ")   # 0 1 2 3 4
    print()                 # bare print() just moves to the next line


# =============================================================================
# SECTION 6: Conditional Logic (if / elif / else)
# =============================================================================

def check_number_sign(n: int) -> str:
    """ Positive, Negative, or Zero. """
    if n > 0:
        return "Positive"
    elif n < 0:
        return "Negative"
    else:
        return "Zero"

def is_even(n: int) -> bool:
    """ O(1): Uses modulo to check for remainder. """
    return n % 2 == 0

def leap_year_check(year: int) -> bool:
    """
    A year is a leap year if:
      - Divisible by 4 AND NOT by 100
      - OR divisible by 400
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# ----- Problem: Largest of 3 Numbers -----
# From L04/016largestOf3Numbers.py and student notes §1.1
#
# Approach: Compare each number against the other two using 'and'.
# Edge Case: Ties (x == y > z) — the elif is NOT entered, so we fall to else.
# The robust fix is: return max(a, b, c)
#
# Time: O(1) — fixed number of comparisons
# Space: O(1)

def largest_of_three(a: int, b: int, c: int) -> int:
    # ----- Approach 1: Explicit conditionals (teaches the logic) -----
    if a > b and a > c:
        return a
    elif b > a and b > c:
        return b
    else:
        return c
    # WARNING: Fails on ties like (5, 5, 3) → returns 3 (wrong!)

def largest_of_three_robust(a: int, b: int, c: int) -> int:
    # ----- Approach 2: Robust (handles all ties) -----
    return max(a, b, c)

# ----- Problem: Grade Classifier -----
# From L04/015ifElseIfStatement.py
# Classic elif chain — order of conditions is critical (most specific first).

def grade_classifier(marks: int) -> str:
    if marks > 60:
        return "Grade A"
    elif marks > 50:
        return "Grade B"
    elif marks > 40:
        return "Grade C"
    else:
        return "Grade F"


# =============================================================================
# SECTION 7: Loops (while, for, break, continue, sentinel)
# =============================================================================

def while_loop_example(limit: int):
    """ Basic while loop counting from 0 to limit-1. """
    print("While Loop Counting:")
    i = 0
    while i < limit:
        print(i, end=" ")
        i += 1
    print()

def for_loop_range_examples():
    """ Demonstrates all range() variants. """
    print("range(5):", list(range(5)))           # [0, 1, 2, 3, 4]
    print("range(2, 6):", list(range(2, 6)))     # [2, 3, 4, 5]
    print("range(1, 10, 2):", list(range(1, 10, 2)))   # Odd numbers: [1, 3, 5, 7, 9]
    print("range(2, 11, 2):", list(range(2, 11, 2)))   # Even numbers: [2, 4, 6, 8, 10]
    print("range(5, 0, -1):", list(range(5, 0, -1)))   # Countdown: [5, 4, 3, 2, 1]
    print("range(n-1,-1,-1):", list(range(4, -1, -1))) # Reverse index 0..4: [4,3,2,1,0]

def break_and_continue_example():
    print("Break and Continue:")
    for i in range(1, 10):
        if i == 3:
            print("  Skipping 3 (continue)")
            continue    # Skip remaining body, jump to next iteration
        if i == 7:
            print("  Breaking at 7 (break)")
            break       # Exit the loop entirely
        print(f"  Processing {i}")

def for_else_loop(target: int):
    """
    The 'else' clause on a loop executes ONLY if the loop exits naturally
    (i.e., was never broken). This is the Pythonic search pattern.
    """
    print(f"Searching for {target} in [1..5]...")
    for i in range(1, 6):
        if i == target:
            print(f"  Found {target}! Breaking.")
            break
    else:
        # This block runs ONLY if 'break' was never hit
        print(f"  {target} not found. Loop finished naturally.")

# ----- Sentinel Loop: while True + break -----
# From L05/008breakStatement.py
# Use this pattern when the exit condition is INSIDE the loop body,
# or when you don't know how many iterations you need upfront.

def count_positives_sentinel(numbers: list) -> int:
    """
    Simulates: keep reading numbers until a negative is entered.
    Uses the 'while True + break' sentinel loop pattern.
    Time: O(n), Space: O(1)
    """
    cnt = 0
    idx = 0
    while True:
        num = numbers[idx]
        idx += 1
        if num < 0:
            break       # Sentinel: exit when we see the terminating value
        cnt += 1
    return cnt

# ----- Problem: Largest of N Numbers -----
# From L05/007largestOfNNumbers.py and student notes §3
# Pattern: Initialize max to -infinity so any real number will be larger.
# Time: O(n) — single pass, Space: O(1)

def largest_of_n(numbers: list) -> int:
    """
    Uses float('-inf') as the initial max — the correct, robust approach.
    Handles negative-only lists (e.g., [-5, -3, -1] → -1) which
    initializing with 0 would incorrectly handle.
    """
    max_so_far = float('-inf')
    for num in numbers:
        if num > max_so_far:
            max_so_far = num
    return max_so_far

# ----- Problem: Series Generation a + i*b -----
# From student notes §1.2
# Time: O(1) — always 3 iterations regardless of a or b

def print_series(a: int, b: int):
    """
    Prints: a+b, a+2b, a+3b
    Example: a=10, b=5 → 15 20 25
    """
    for i in range(1, 4):
        print(a + i * b, end=" ")
    print()


# =============================================================================
# SECTION 8: FizzBuzz — Naive to Correct Code Evolution
# =============================================================================

# ----- WHAT IS FIZZBUZZ? -----
# Print numbers 1 to n.
# If divisible by 3: print "Fizz"
# If divisible by 5: print "Buzz"
# If divisible by both 3 AND 5: print "FizzBuzz"
# Otherwise: print the number.

# ----- Approach 1: BUGGY (Wrong condition order) -----
# This is the classic mistake — the interviewer is watching for this.

def fizz_buzz_buggy(n: int):
    """
    BUG: The conditions for 3 and 5 are checked BEFORE checking for both.
    For i=15: 15%3==0 is True, so it prints "Fizz" and skips "FizzBuzz".
    "FizzBuzz" is NEVER printed.
    """
    for i in range(1, n + 1):
        if i % 3 == 0:
            print("Fizz", end=" ")      # 15 hits here → wrong!
        elif i % 5 == 0:
            print("Buzz", end=" ")
        else:
            print(i, end=" ")
    print()

# ----- Approach 2: CORRECT (Most specific condition first) -----
# Rule: Always check the MOST RESTRICTIVE / MOST SPECIFIC case first.
# "Divisible by both" is more specific than "divisible by just 3".

def fizz_buzz_correct(n: int):
    """
    Correct ordering: check the compound condition (% 15 OR and-ed) first.
    Time: O(n), Space: O(1)
    """
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:  # Most specific: both divisors
            print("FizzBuzz", end=" ")
        elif i % 3 == 0:
            print("Fizz", end=" ")
        elif i % 5 == 0:
            print("Buzz", end=" ")
        else:
            print(i, end=" ")
    print()

# ----- Approach 3: Pythonic (using string building) -----
# Eliminates the need for the compound condition check entirely.
# Preferred in production code.

def fizz_buzz_pythonic(n: int):
    """
    Build the output string by concatenation — avoids the ordering pitfall.
    Time: O(n), Space: O(1)
    """
    for i in range(1, n + 1):
        output = ""
        if i % 3 == 0:
            output += "Fizz"
        if i % 5 == 0:
            output += "Buzz"
        print(output if output else i, end=" ")
    print()


# =============================================================================
# SECTION 9: Sum Patterns
# =============================================================================

# ----- Sum of First N Natural Numbers (two approaches) -----
# From student notes §1.5

def sum_of_n_loop(n: int) -> int:
    """
    Brute Force: Accumulate with a loop.
    Time: O(n), Space: O(1)
    """
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

def sum_of_n_formula(n: int) -> int:
    """
    Optimal: Gauss's formula — n*(n+1)//2.
    Derived from pairing: (1+n) + (2+n-1) + ... = n/2 pairs each summing to n+1.
    Time: O(1), Space: O(1)
    """
    return n * (n + 1) // 2


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_fizz_buzz(n: int):
    """
    Print numbers 1 to n following FizzBuzz rules.
    Hint: What must you check FIRST to avoid the classic bug?
    """
    pass

def practice_sum_of_n(n: int) -> int:
    """
    Return the sum of all numbers from 1 to n.
    Bonus: Can you solve it in O(1) using the Gauss formula?
    """
    pass

def practice_largest_of_three(a: int, b: int, c: int) -> int:
    """
    Return the largest of three numbers.
    Edge case to handle: what if two are equal and both larger than the third?
    """
    pass

def practice_count_positives_sentinel(numbers: list) -> int:
    """
    Using a 'while True + break' sentinel loop, count how many numbers
    appear before the first negative number in the list.
    Example: [3, 5, 2, -1, 4] → 3 (stops at -1)
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("SECTION 1: Math Basics")
    print("=" * 60)
    math_basics()

    print("\n" + "=" * 60)
    print("SECTION 2: Operator Precedence")
    print("=" * 60)
    operator_precedence_demo()

    print("\n" + "=" * 60)
    print("SECTION 3: I/O and Type Casting (Simulated)")
    print("=" * 60)
    io_type_casting_demo()

    print("\n" + "=" * 60)
    print("SECTION 4: Packing / Unpacking")
    print("=" * 60)
    packing_unpacking_demo()

    print("\n" + "=" * 60)
    print("SECTION 5: print() Formatting")
    print("=" * 60)
    print_formatting_demo()

    print("\n" + "=" * 60)
    print("SECTION 6: Conditionals")
    print("=" * 60)
    print("Sign of -7:", check_number_sign(-7))
    print("Sign of 0:", check_number_sign(0))
    print("Is 10 even?", is_even(10))
    print("Is 2024 a leap year?", leap_year_check(2024))
    print("Largest of (3, 9, 6):", largest_of_three(3, 9, 6))
    print("Largest of (5, 5, 3):", largest_of_three(5, 5, 3), "← BUG: returns 3")
    print("Largest of (5, 5, 3) robust:", largest_of_three_robust(5, 5, 3), "← Correct")
    print("Grade for 55:", grade_classifier(55))
    print("Grade for 35:", grade_classifier(35))

    print("\n" + "=" * 60)
    print("SECTION 7: Loops")
    print("=" * 60)
    while_loop_example(5)
    for_loop_range_examples()
    break_and_continue_example()
    for_else_loop(3)
    for_else_loop(10)
    print("Sentinel: positives before -1 in [3,5,2,-1,4]:",
          count_positives_sentinel([3, 5, 2, -1, 4]))
    print("Largest of N [-5,-3,-1]:", largest_of_n([-5, -3, -1]))
    print("Largest of N [12,45,3,67,22]:", largest_of_n([12, 45, 3, 67, 22]))
    print("Series a=10 b=5:", end=" "); print_series(10, 5)

    print("\n" + "=" * 60)
    print("SECTION 8: FizzBuzz Evolution")
    print("=" * 60)
    print("Buggy (n=15):    ", end=""); fizz_buzz_buggy(15)
    print("Correct (n=15):  ", end=""); fizz_buzz_correct(15)
    print("Pythonic (n=15): ", end=""); fizz_buzz_pythonic(15)

    print("\n" + "=" * 60)
    print("SECTION 9: Sum Patterns")
    print("=" * 60)
    print("Sum 1..10 (loop):   ", sum_of_n_loop(10))
    print("Sum 1..10 (formula):", sum_of_n_formula(10))

    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS")
    print("=" * 60)
    practice_fizz_buzz(15)
    print("Practice sum of 5:", practice_sum_of_n(5))
    print("Practice largest_of_three(3,9,6):", practice_largest_of_three(3, 9, 6))
    print("Practice sentinel [3,5,-1]:", practice_count_positives_sentinel([3, 5, -1]))
