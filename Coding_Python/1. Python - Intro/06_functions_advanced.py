###############################################################################
#          Lecture 8: Functions — From Basics to Advanced Concepts             #
###############################################################################

"""
Comprehensive tutorial on Python functions covering:
  - Definition, calling, return values
  - Parameters vs arguments
  - Variable scope and the LEGB rule
  - Type hints / annotations
  - Positional, keyword, default, and optional arguments
  - *args and **kwargs (packing & unpacking)
  - Lambda functions
  - Higher-order functions (map, filter, reduce, sorted)
  - Practice exercises

Source reference: LPLV26MAY/L08 - Functions (001-011)

Run this file directly:  python 07_functions_advanced.py
All examples use print() so you can see the output immediately.
"""

from functools import reduce  # needed later in Section 11


# =============================================================================
# SECTION 1: What Are Functions and Why Use Them?
# =============================================================================

# A function is a reusable block of code that performs a specific task.
# Think of it like a recipe: you define the steps once, then "call" the
# recipe whenever you need it — no copy-pasting required.

# WHY functions matter:
# 1. Modularity   — break big problems into small, manageable pieces
# 2. Reusability  — write once, call many times
# 3. Readability  — meaningful names make code self-documenting
# 4. Testing      — test each function independently
# 5. DRY Principle (Don't Repeat Yourself)

# --- Without functions (violates DRY) ---
print("===== SECTION 1: Why Functions? =====")

# Imagine you need to greet three people:
print("Hello, Alice! Welcome aboard.")        # duplicated logic
print("Hello, Bob! Welcome aboard.")           # duplicated logic
print("Hello, Charlie! Welcome aboard.")       # duplicated logic

# If the greeting message changes, you must edit ALL three lines.
# With a function you edit ONE place:

def greet(name: str) -> None:
    """Greet a person by name."""
    print(f"Hello, {name}! Welcome aboard.")   # single source of truth

greet("Alice")                                 # call 1
greet("Bob")                                   # call 2
greet("Charlie")                               # call 3

# Now if the greeting changes, you only update the function body.


# =============================================================================
# SECTION 2: Function Definition and Calling
# =============================================================================

print("\n===== SECTION 2: Definition & Calling =====")

# Syntax:
#   def function_name(parameters):
#       """optional docstring"""
#       body
#       return value        # optional

# --- Function WITH a return value ---
def add(a, b):
    return a + b            # sends the result back to the caller

result = add(3, 5)          # 'result' now holds 8
print("add(3, 5) =", result)

# --- Function WITHOUT a return value ---
def say_hello():
    print("Hello from say_hello!")  # side effect only — no return

say_hello()                         # prints the message

# What does a function return when there's no explicit return?
x = say_hello()                     # calls the function, prints message
print("Return value:", x)           # None — Python returns None by default

# KEY INSIGHT:
# Every Python function returns something. If you omit 'return', or write
# 'return' with no value, the function returns None.


# =============================================================================
# SECTION 3: Parameters vs Arguments
# =============================================================================

print("\n===== SECTION 3: Parameters vs Arguments =====")

# Parameter = the variable name in the function DEFINITION (placeholder)
# Argument  = the actual value you PASS when calling the function

#            parameters (formal parameters)
#                 |   |
def multiply(x, y):        # x and y are PARAMETERS
    return x * y

a = 4                       # a and b are variables holding values
b = 7
print("multiply(4, 7) =", multiply(a, b))   # a, b are ARGUMENTS (actual parameters)
#                                    ^  ^
#                               arguments

# Memory walkthrough:
# 1. Python sees multiply(a, b) -> evaluates a=4, b=7
# 2. Creates local scope for multiply: x=4, y=7  (parameters bound to arguments)
# 3. Computes x * y = 28
# 4. Returns 28 -> caller receives it


# =============================================================================
# SECTION 4: Return Values
# =============================================================================

print("\n===== SECTION 4: Return Values =====")

# --- return vs print (COMMON BEGINNER CONFUSION) ---
# print() displays to the screen — the value is NOT usable later
# return sends the value back to the caller — the value IS usable

def add_print(a, b):
    print(a + b)            # shows 15 on screen, but returns None

def add_return(a, b):
    return a + b            # sends 15 back to caller, nothing on screen

r1 = add_print(7, 8)       # prints 15
r2 = add_return(7, 8)      # silent — result stored in r2

print("r1 (from print version):", r1)    # None — can't use it!
print("r2 (from return version):", r2)   # 15 — usable!
print("r2 doubled:", r2 * 2)             # 30 — you can compute with it

# --- Returning multiple values (as a tuple) ---
def min_max(numbers):
    """Return both the minimum and maximum of a list."""
    return min(numbers), max(numbers)   # Python packs these into a tuple

lo, hi = min_max([3, 1, 4, 1, 5, 9])   # tuple unpacking
print(f"min = {lo}, max = {hi}")        # min = 1, max = 9

# --- Early return for guard clauses ---
# Guard clauses handle edge cases first, keeping the main logic un-indented.

def is_prime(n: int) -> bool:
    """Check if n is prime.  Time: O(sqrt(n))  Space: O(1)"""
    if n < 2:                       # guard clause — reject trivially
        return False
    i = 2
    while i * i <= n:               # only check up to sqrt(n)
        if n % i == 0:
            return False            # early return — found a divisor
        i += 1
    return True                     # survived all checks -> prime

print("is_prime(7):", is_prime(7))      # True
print("is_prime(10):", is_prime(10))    # False
print("is_prime(1):", is_prime(1))      # False (guard clause catches it)


# =============================================================================
# SECTION 5: Variable Scope (Local vs Global) — IMPORTANT
# =============================================================================

print("\n===== SECTION 5: Variable Scope =====")

# --- Local variables: born inside a function, die when it returns ---

def demo_local():
    secret = 42                     # local to demo_local
    print("  Inside demo_local, secret =", secret)

demo_local()
# print(secret)  # <-- NameError! 'secret' does not exist out here

# --- Global variables: defined at module level, accessible everywhere ---

counter = 0                         # global variable

def read_global():
    print("  read_global sees counter =", counter)  # reading is fine

read_global()

# --- The 'global' keyword (use sparingly — it makes code harder to debug) ---

def increment_global():
    global counter                  # tells Python: use the module-level 'counter'
    counter += 1                    # modifies the global variable
    print("  Inside increment_global, counter =", counter)

increment_global()
print("After increment_global, counter =", counter)  # 1

# WHY AVOID 'global'?
# - Any function anywhere can change the variable -> hard to track bugs
# - Prefer passing values in and returning values out (pure functions)

# --- The LEGB Rule ---
# When Python encounters a variable name, it searches in this order:
#   L — Local:     inside the current function
#   E — Enclosing: inside any enclosing (outer) function (for nested functions)
#   G — Global:    at the module / file level
#   B — Built-in:  Python's built-in names (len, print, range, etc.)

a_global = 3                        # G — Global scope

def outer():
    b_enclosing = 4                 # E — Enclosing scope (for inner())

    def inner():
        c_local = 5                 # L — Local scope
        # Python resolves a_global via LEGB: not Local, not Enclosing -> Global
        result = a_global * b_enclosing * c_local
        print(f"  inner(): {a_global} * {b_enclosing} * {c_local} = {result}")
        return result

    return inner()

print("LEGB demo:", outer())        # 3 * 4 * 5 = 60

# --- Call stack visualization ---
# When you call outer():
#
# CALL STACK (grows downward)
# +--------------------------+
# | outer()                  |
# |   b_enclosing = 4        |
# |   +--------------------+ |
# |   | inner()            | |
# |   |   c_local = 5      | |
# |   |   looks up:        | |
# |   |     c_local -> L   | |
# |   |     b_enclosing->E | |
# |   |     a_global -> G  | |
# |   +--------------------+ |  <- inner() returns, its frame is destroyed
# +--------------------------+  <- outer() returns, its frame is destroyed

# --- Mutation vs Reassignment with function arguments ---

def try_increment(x: int) -> None:
    """Integers are immutable — reassignment creates a NEW local variable."""
    x = x + 1                       # x is now a NEW local int; original unchanged
    print(f"  Inside try_increment, x = {x}")

val = 10
print(f"Before try_increment, val = {val}")
try_increment(val)
print(f"After try_increment, val = {val}")   # still 10!

# To actually get the incremented value, RETURN it:
def increment(x: int) -> int:
    return x + 1

val = increment(val)                # reassign with the returned value
print(f"After increment + reassign, val = {val}")  # 11


# =============================================================================
# SECTION 6: Type Hints / Annotations
# =============================================================================

print("\n===== SECTION 6: Type Hints =====")

# Type hints tell readers (and IDEs) what types a function expects and returns.
# Syntax:  def func(param: type) -> return_type:

def divide(a: float, b: float) -> float:
    """Divide a by b. Returns a float."""
    if b == 0:
        return float('inf')         # guard clause for division by zero
    return a / b

print("divide(10, 3) =", divide(10, 3))      # 3.333...
print("divide(10, 0) =", divide(10, 0))      # inf

# Common type annotations:
#   int, str, float, bool                  — basic types
#   list[int]                              — list of integers
#   dict[str, int]                         — dict with str keys, int values
#   tuple[int, str]                        — tuple with specific element types
#   Optional[int]  (or int | None)         — could be int or None

from typing import Optional

def find_index(lst: list[int], target: int) -> Optional[int]:
    """Return index of target in lst, or None if not found."""
    for i, val in enumerate(lst):
        if val == target:
            return i                # found -> return index
    return None                     # not found

idx = find_index([10, 20, 30], 20)
print(f"find_index([10,20,30], 20) = {idx}")   # 1
idx = find_index([10, 20, 30], 99)
print(f"find_index([10,20,30], 99) = {idx}")   # None

# IMPORTANT: Type hints do NOT enforce types at runtime!
# This will run without error even though we "promised" floats:
print("divide('hello', 3) would crash at runtime, not at definition time")
# Python won't stop you from calling divide("hello", 3) — it only crashes
# when it tries to execute the division. Hints are DOCUMENTATION, not walls.


# =============================================================================
# SECTION 7: Positional vs Keyword Arguments
# =============================================================================

print("\n===== SECTION 7: Positional vs Keyword Arguments =====")

def describe_pet(animal: str, name: str, age: int) -> None:
    """Print a description of a pet."""
    print(f"  {name} is a {age}-year-old {animal}.")

# --- Positional arguments: ORDER MATTERS ---
describe_pet("dog", "Buddy", 5)     # animal="dog", name="Buddy", age=5

# --- Keyword arguments: use parameter names, ORDER DOESN'T MATTER ---
describe_pet(age=3, name="Whiskers", animal="cat")

# --- Mixing: positional MUST come before keyword ---
describe_pet("parrot", name="Polly", age=2)   # "parrot" is positional (1st param)

# This would FAIL:
# describe_pet(animal="dog", "Rex", 4)
#   SyntaxError: positional argument follows keyword argument


# =============================================================================
# SECTION 8: Default / Optional Arguments
# =============================================================================

print("\n===== SECTION 8: Default / Optional Arguments =====")

# You can give parameters default values. If the caller omits them,
# the defaults kick in.

def power(base: int, exponent: int = 2) -> int:
    """Raise base to exponent. Defaults to squaring."""
    return base ** exponent

print("power(5)    =", power(5))        # 5^2 = 25  (default exponent=2)
print("power(5, 3) =", power(5, 3))     # 5^3 = 125 (override exponent)

# Rule: parameters WITH defaults must come AFTER those WITHOUT.
# def bad(a=1, b):  <-- SyntaxError

def create_profile(name: str, age: int = 0, city: str = "Unknown") -> dict:
    return {"name": name, "age": age, "city": city}

print(create_profile("Alice"))                     # age=0, city="Unknown"
print(create_profile("Bob", 25))                   # city="Unknown"
print(create_profile("Charlie", 30, "Mumbai"))     # all provided

# --- GOTCHA: Mutable Default Arguments ---
# This is one of the MOST COMMON Python bugs!

def append_to_list_BAD(item, lst=[]):
    """BAD: The default list [] is created ONCE and shared across all calls!"""
    lst.append(item)
    return lst

# Watch what happens:
print("\nMutable default gotcha:")
print("Call 1:", append_to_list_BAD(1))   # [1]        — looks fine
print("Call 2:", append_to_list_BAD(2))   # [1, 2]     — WAIT, where did 1 come from?!
print("Call 3:", append_to_list_BAD(3))   # [1, 2, 3]  — the list PERSISTS between calls!

# WHY? Python evaluates default arguments ONCE at function definition time.
# The same list object is reused every time the function is called without lst.

# --- The Correct Way: use None as sentinel ---

def append_to_list_GOOD(item, lst=None):
    """GOOD: Create a fresh list each time if none is provided."""
    if lst is None:                 # sentinel check
        lst = []                    # brand new list for this call
    lst.append(item)
    return lst

print("\nFixed version:")
print("Call 1:", append_to_list_GOOD(1))   # [1]
print("Call 2:", append_to_list_GOOD(2))   # [2]   — independent!
print("Call 3:", append_to_list_GOOD(3))   # [3]   — independent!


# =============================================================================
# SECTION 9: Packing and Unpacking (*args, **kwargs)
# =============================================================================

print("\n===== SECTION 9: *args and **kwargs =====")

# --- *args: collect extra POSITIONAL arguments into a TUPLE ---

def total(*args) -> int:
    """Sum any number of positional arguments."""
    # args is a tuple: (1, 2, 3, ...)
    print(f"  args = {args}, type = {type(args).__name__}")
    return sum(args)

print("total(1, 2, 3):", total(1, 2, 3))          # 6
print("total(10, 20):", total(10, 20))             # 30
print("total():", total())                         # 0

# --- **kwargs: collect extra KEYWORD arguments into a DICT ---

def print_info(**kwargs) -> None:
    """Print arbitrary keyword arguments."""
    # kwargs is a dict: {"name": "Alice", "age": 25, ...}
    print(f"  kwargs = {kwargs}, type = {type(kwargs).__name__}")
    for key, value in kwargs.items():
        print(f"    {key} = {value}")

print("\nprint_info demo:")
print_info(name="Alice", age=25, city="Delhi")

# --- Combining regular params, *args, and **kwargs ---
# Order: regular params -> *args -> **kwargs

def flexible(required, *args, **kwargs):
    print(f"  required = {required}")
    print(f"  args     = {args}")
    print(f"  kwargs   = {kwargs}")

print("\nflexible demo:")
flexible("hello", 1, 2, 3, debug=True, verbose=False)
# required = "hello"
# args     = (1, 2, 3)
# kwargs   = {"debug": True, "verbose": False}

# --- Unpacking: passing a list/dict TO a function with * and ** ---

def add_three(a, b, c):
    return a + b + c

numbers = [10, 20, 30]
print(f"\nUnpacking list {numbers}:", add_three(*numbers))   # same as add_three(10, 20, 30)

config = {"a": 100, "b": 200, "c": 300}
print(f"Unpacking dict {config}:", add_three(**config))      # same as add_three(a=100, b=200, c=300)

# Practical example: building a flexible logger
def log_message(level: str, *messages, **metadata):
    """Log one or more messages with optional metadata."""
    combined = " | ".join(str(m) for m in messages)
    meta_str = ", ".join(f"{k}={v}" for k, v in metadata.items())
    print(f"  [{level.upper()}] {combined}" + (f"  ({meta_str})" if meta_str else ""))

print("\nLogger demo:")
log_message("info", "Server started", port=8080)
log_message("error", "Connection failed", "Retrying...", attempt=3, timeout=30)


# =============================================================================
# SECTION 10: Lambda Functions
# =============================================================================

print("\n===== SECTION 10: Lambda Functions =====")

# A lambda is an anonymous (unnamed) one-line function.
# Syntax:  lambda parameters: expression
# It automatically returns the result of the expression.

square = lambda x: x ** 2          # equivalent to def square(x): return x**2
print("square(5):", square(5))     # 25

add_lambda = lambda a, b: a + b
print("add_lambda(3, 7):", add_lambda(3, 7))  # 10

# --- Used with map() ---
# map(function, iterable) applies the function to each element

numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))  # square each number
print(f"map(square, {numbers}) = {squared}")     # [1, 4, 9, 16, 25]

# --- Used with filter() ---
# filter(function, iterable) keeps elements where function returns True

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"filter(even, {numbers}) = {evens}")      # [2, 4]

# --- Used with sorted() ---
# sorted(iterable, key=function) sorts by the key function's return value

words = ["banana", "apple", "cherry", "date"]
by_length = sorted(words, key=lambda w: len(w))
print(f"sorted by length: {by_length}")          # ['date', 'apple', 'banana', 'cherry']

students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
by_grade = sorted(students, key=lambda s: s[1], reverse=True)  # highest first
print(f"sorted by grade: {by_grade}")

# WHEN TO USE LAMBDA vs REGULAR FUNCTION:
# - Lambda: short, throwaway, used once (inside map/filter/sorted)
# - Regular function: reusable, multi-line, needs a docstring, complex logic
# Rule of thumb: if you need to name it or it's more than one expression,
# use a regular def.


# =============================================================================
# SECTION 11: Higher-Order Functions
# =============================================================================

print("\n===== SECTION 11: Higher-Order Functions =====")

# A higher-order function is a function that either:
#   (a) takes another function as an argument, OR
#   (b) returns a function as its result (or both)

# --- map(function, iterable) ---
# Applies function to every element, returns an iterator

temps_celsius = [0, 20, 37, 100]
temps_fahrenheit = list(map(lambda c: c * 9/5 + 32, temps_celsius))
print(f"Celsius {temps_celsius} -> Fahrenheit {temps_fahrenheit}")
# [32.0, 68.0, 98.6, 212.0]

# --- filter(function, iterable) ---
# Keeps only elements where function returns True

ages = [12, 18, 25, 15, 30, 8, 21]
adults = list(filter(lambda age: age >= 18, ages))
print(f"Adults from {ages}: {adults}")       # [18, 25, 30, 21]

# --- reduce(function, iterable) ---
# Accumulates a single result by applying function(accumulator, element)
# Must import from functools (done at top of file)

nums = [1, 2, 3, 4, 5]
product = reduce(lambda acc, x: acc * x, nums)
print(f"reduce(multiply, {nums}) = {product}")    # 1*2*3*4*5 = 120

# How reduce works step-by-step:
# Step 1: acc=1,  x=2  -> 1*2  = 2
# Step 2: acc=2,  x=3  -> 2*3  = 6
# Step 3: acc=6,  x=4  -> 6*4  = 24
# Step 4: acc=24, x=5  -> 24*5 = 120

# --- sorted() with key= ---
# key= tells sorted() HOW to compare elements

data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35}]
by_age = sorted(data, key=lambda person: person["age"])
print("Sorted by age:", [d["name"] for d in by_age])  # ['Bob', 'Alice', 'Charlie']

# --- Writing your own higher-order function ---

def apply_twice(func, value):
    """Apply a function twice: func(func(value))."""
    return func(func(value))

print("apply_twice(square, 3):", apply_twice(lambda x: x ** 2, 3))
# Step 1: (3)^2 = 9
# Step 2: (9)^2 = 81

def make_multiplier(factor: int):
    """Return a function that multiplies its input by 'factor'.
    This is a 'closure' — the returned function remembers 'factor'."""
    def multiplier(x):
        return x * factor           # 'factor' comes from the enclosing scope (LEGB: E)
    return multiplier               # return the function itself (not calling it!)

double = make_multiplier(2)         # double is now a function: x -> x*2
triple = make_multiplier(3)         # triple is now a function: x -> x*3

print("double(5):", double(5))      # 10
print("triple(5):", triple(5))      # 15

# --- Practical: composing functions for a data pipeline ---
def pipeline(data, *functions):
    """Pass data through a series of functions in order."""
    result = data
    for func in functions:
        result = func(result)
    return result

raw = "  Hello, World!  "
cleaned = pipeline(
    raw,
    str.strip,                      # remove whitespace
    str.lower,                      # lowercase
    lambda s: s.replace("!", ""),   # remove exclamation marks
)
print(f"pipeline('{raw}') -> '{cleaned}'")  # 'hello, world'


# =============================================================================
# Matrix Multiplication from Scratch
# =============================================================================

print("\n===== Matrix Multiplication from Scratch =====")

# ----- The Rule: when CAN two matrices be multiplied? -----
#
# A matrix is represented as a list of rows: mat[i][j] = element at row i, column j.
#   mat1 has dimensions (p x q1)  → p rows, q1 columns
#   mat2 has dimensions (q2 x c)  → q2 rows, c columns
#
# Multiplication mat1 @ mat2 is only possible if:
#       COLUMNS of mat1  ==  ROWS of mat2     (q1 == q2)
#
# The result mat3 has dimensions (p x c) — rows of mat1, columns of mat2.
#
# Visual:
#   mat1: (p x q1)  @  mat2: (q2 x c)   -- need q1 == q2
#              \_______/
#           "inner" dimensions must match
#   result: (p x c)        ← "outer" dimensions become the result shape
#
# ----- How each result cell is computed -----
#
# mat3[i][j] = (row i of mat1) DOT (column j of mat2)
#            = sum over k of  mat1[i][k] * mat2[k][j]
#
# Each cell is a SUM OF PRODUCTS across the shared dimension (q1 == q2).

def mat_multp(mat1: list[list[int]], mat2: list[list[int]]):
    """Multiply two matrices: mat1 (p x q1) and mat2 (q2 x c) -> result (p x c)."""
    p = len(mat1)        # rows of mat1
    q1 = len(mat1[0])    # columns of mat1

    q2 = len(mat2)        # rows of mat2
    cols_mat2 = len(mat2[0])  # columns of mat2 -> becomes columns of the result

    if q1 != q2:
        print("Dimension Mismatch, Matrix Multiplication not possible")
        return "Error"

    print("Matrix Multiplication possible")
    # Initialize the result matrix mat3 with zeros — same trick as list
    # initialization covered in 07_lists_tuples_slicing.py: nested
    # comprehension creates p independent rows (not p references to one row).
    mat3 = [[0 for _ in range(cols_mat2)] for _ in range(p)]

    # Triple nested loop — the classic O(n^3) matrix multiplication
    for i in range(p):              # iterate over rows of mat1 (= rows of result)
        for j in range(cols_mat2):  # iterate over columns of mat2 (= cols of result)
            for k in range(q1):     # iterate over the shared/common dimension
                mat3[i][j] += mat1[i][k] * mat2[k][j]   # accumulate the dot product

    return mat3

# ----- Demonstration -----
mat1 = [[1, 2, 3],
        [4, 5, 6]]            # 2x3 matrix
mat2 = [[7, 8],
        [9, 10],
        [11, 12]]             # 3x2 matrix — rows (3) match mat1's columns (3) ✓

print(f"mat1 (2x3): {mat1}")
print(f"mat2 (3x2): {mat2}")

result = mat_multp(mat1, mat2)
print(f"Result (2x2): {result}")
# Result: [[58, 64], [139, 154]]

# ----- Manual verification of result[0][0] -----
# row 0 of mat1: [1, 2, 3]      column 0 of mat2: [7, 9, 11]
# dot product = 1*7 + 2*9 + 3*11 = 7 + 18 + 33 = 58  ✓ matches mat3[0][0]

# ----- Mismatched dimensions example -----
mat_bad = [[1, 2], [3, 4]]     # 2x2
mat_other = [[1, 2, 3]]        # 1x3 — columns of mat_bad (2) != rows of mat_other (1)
print(f"\nTrying incompatible shapes (2x2) @ (1x3):")
print(mat_multp(mat_bad, mat_other))   # prints the mismatch message, returns "Error"

# ----- Complexity Analysis -----
# Time:  O(p * q1 * cols_mat2) — three nested loops.
#        For SQUARE matrices (n x n), this is O(n^3) — the classic complexity
#        of naive matrix multiplication. (Strassen's algorithm improves this
#        to ~O(n^2.807) but is rarely used outside specialized numerical libraries.)
# Space: O(p * cols_mat2) — the result matrix mat3.
#
# ----- In production, never write this by hand -----
# Use NumPy instead — it's implemented in C and uses highly optimized
# linear algebra libraries (BLAS/LAPACK), often 100x+ faster:
#   import numpy as np
#   result = np.array(mat1) @ np.array(mat2)     # or np.matmul(mat1, mat2)
# Writing it from scratch (like above) is purely for understanding the
# algorithm — exactly the kind of thing interviewers ask you to implement
# to test your grasp of nested loops and complexity analysis.


# =============================================================================
# SECTION 11.5: Functions vs Methods, and Introspection with dir()
# =============================================================================

print("\n===== SECTION 11.5: Functions vs Methods, Introspection =====")

# ----- Function vs Method: what's the actual difference? -----
#
# A FUNCTION is a piece of code called by name. You pass it data (parameters)
# and it can optionally return data.
#     len([1, 2, 3])      ← len is a function, the list is its argument
#
# A METHOD is a piece of code called via a name ATTACHED to an object.
# It behaves like a function with two key differences:
#   1. It is IMPLICITLY passed the object it was called on (that's 'self')
#   2. It can operate on data CONTAINED WITHIN that object/class
#     [1, 2, 3].append(4)  ← append is a method, implicitly operates on the list

def is_even(n):           # FUNCTION — standalone, not tied to any object
    return n % 2 == 0

nums = [1, 2, 3]
nums.append(4)             # METHOD — called ON nums, implicitly modifies nums
print(f"is_even(4) [function call]: {is_even(4)}")
print(f"nums after .append(4) [method call]: {nums}")

# ----- dir() — discover what's available on any object -----
#
# dir(obj) returns a list of every attribute and method name an object has.
# This is one of the most useful tools for EXPLORING Python interactively —
# when you forget a method name, dir() jogs your memory.

list_attributes = dir([])    # dir() on an empty list — shows what ALL lists support
# Most names starting with __ are "dunder" (double underscore) internal methods.
# Filter them out to see just the PUBLIC, commonly-used methods:
list_methods = [item for item in list_attributes if not item.startswith('__')]
print(f"\nPublic list methods: {list_methods}")
# ['append', 'clear', 'copy', 'count', 'extend', 'index', 'insert',
#  'pop', 'remove', 'reverse', 'sort']

# Try this with other types too: dir(""), dir({}), dir(5) — same pattern,
# instantly shows you every method that type supports.

# ----- The builtins module — every function available without import -----
#
# All the functions you've been using without `import` (print, len, range,
# sum, max, sorted, etc.) actually live in a module called 'builtins' that
# Python auto-imports into every script.

import builtins

all_builtins = dir(builtins)
# Built-in FUNCTIONS start with a lowercase letter.
# Built-in EXCEPTIONS (ValueError, TypeError, etc.) start with uppercase —
# exclude those to see just the functions:
builtin_functions = [item for item in all_builtins if item[0].islower() and not item.startswith('__')]
print(f"\nSample built-in functions: {builtin_functions[:15]} ...")
# ['abs', 'all', 'any', 'bin', 'bool', 'callable', 'chr', 'dict',
#  'dir', 'divmod', 'enumerate', 'filter', 'float', 'format', 'frozenset', ...]

# ----- The keyword module — Python's reserved words -----
#
# Keywords are words you CANNOT use as variable names (if, for, class, etc.)
# because Python's grammar reserves them for special syntax.

import keyword

print(f"\nStandard keywords: {keyword.kwlist}")
# ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
#  'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
#  'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
#  'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
#  'while', 'with', 'yield']

# Soft keywords (Python 3.9+) — special meaning ONLY in specific contexts,
# can still be used as variable names elsewhere (unlike hard keywords above).
print(f"Soft keywords: {keyword.softkwlist}")
# ['_', 'case', 'match', 'type']
#   e.g. 'match' and 'case' are only special inside a match statement;
#   you can still write `match = 5` as a normal variable assignment.

print(f"Is 'class' a keyword? {keyword.iskeyword('class')}")   # True
print(f"Is 'data' a keyword?  {keyword.iskeyword('data')}")    # False

# ----- Why this matters for interviews -----
# Being able to say "I wasn't sure of the exact method name, so I checked
# dir(my_object)" shows you know how to be self-sufficient in unfamiliar
# codebases — a skill interviewers value as much as memorized syntax.


# =============================================================================
# SECTION 12: Practice Exercises
# =============================================================================

print("\n===== SECTION 12: Practice Exercises =====")

# -----------------------------------------------------------------------------
# Exercise 1: Print First M Primes
# -----------------------------------------------------------------------------
# Given a number m, print the first m prime numbers.
# Uses the is_prime() function defined in Section 4.
# Time: O(m * sqrt(p)) where p is the m-th prime
# Space: O(1) — just a counter and a loop variable

def print_first_m_primes(m: int) -> None:
    """Print the first m prime numbers."""
    num = 2                         # start checking from 2
    count = 0                       # how many primes found so far
    while count < m:
        if is_prime(num):
            print(f"  Prime #{count+1}: {num}")
            count += 1
        num += 1

print("Exercise 1: First 5 primes")
print_first_m_primes(5)


# -----------------------------------------------------------------------------
# Exercise 2: Fibonacci with Return
# -----------------------------------------------------------------------------
# Return the first n Fibonacci numbers as a list.
# Time: O(n)   Space: O(n) — storing the list

def fibonacci(n: int) -> list[int]:
    """Return a list of the first n Fibonacci numbers."""
    if n <= 0:
        return []                   # guard clause
    if n == 1:
        return [0]                  # guard clause
    fibs = [0, 1]                   # seed values
    for _ in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])  # each new number = sum of previous two
    return fibs

print("\nExercise 2: First 10 Fibonacci numbers")
print(" ", fibonacci(10))
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# -----------------------------------------------------------------------------
# Exercise 3: Word Frequency Counter using **kwargs-style dict
# -----------------------------------------------------------------------------
# Given a string, return a dict mapping each word to its frequency.
# Time: O(n) where n = number of words   Space: O(k) where k = unique words

def word_frequency(text: str) -> dict[str, int]:
    """Count occurrences of each word in text (case-insensitive)."""
    freq: dict[str, int] = {}
    for word in text.lower().split():
        freq[word] = freq.get(word, 0) + 1   # .get() returns 0 if key missing
    return freq

print("\nExercise 3: Word frequency")
sample = "the cat sat on the mat the cat"
print(f"  Input: '{sample}'")
print(f"  Frequency: {word_frequency(sample)}")
# {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}


# -----------------------------------------------------------------------------
# Exercise 4: Flexible Statistics Calculator (*args)
# -----------------------------------------------------------------------------
# Accept any number of numerical arguments, return a dict with stats.
# Time: O(n)  Space: O(1) extra (besides the return dict)

def stats(*args: float) -> dict[str, float]:
    """Calculate basic statistics for any number of values."""
    if not args:
        return {"error": "No values provided"}
    n = len(args)
    total = sum(args)
    mean = total / n
    sorted_args = sorted(args)
    # Median: middle value (or average of two middle values)
    if n % 2 == 1:
        median = sorted_args[n // 2]
    else:
        median = (sorted_args[n // 2 - 1] + sorted_args[n // 2]) / 2
    return {
        "count": n,
        "sum": total,
        "mean": round(mean, 2),
        "min": min(args),
        "max": max(args),
        "median": median,
    }

print("\nExercise 4: Statistics calculator")
result = stats(10, 20, 30, 40, 50)
for key, val in result.items():
    print(f"  {key}: {val}")


# -----------------------------------------------------------------------------
# Exercise 5: Apply Discount Pipeline (higher-order functions)
# -----------------------------------------------------------------------------
# Given a list of prices and a series of discount functions,
# apply each discount in order and return final prices.
# Time: O(n * d) where n = items, d = number of discounts
# Space: O(n) for the result list

def apply_discounts(prices: list[float], *discount_fns) -> list[float]:
    """Apply a chain of discount functions to each price."""
    result = list(prices)                       # copy original list
    for discount in discount_fns:               # iterate over each discount function
        result = [discount(p) for p in result]  # apply to every price
    return [round(p, 2) for p in result]        # round for clean output

# Define some discount functions
ten_percent_off = lambda price: price * 0.90       # 10% off
flat_five_off   = lambda price: max(0, price - 5)  # subtract 5, floor at 0
half_off        = lambda price: price * 0.50       # 50% off

print("\nExercise 5: Discount pipeline")
original_prices = [100.0, 50.0, 25.0, 10.0]
final = apply_discounts(original_prices, ten_percent_off, flat_five_off)
print(f"  Original: {original_prices}")
print(f"  After 10% off then $5 off: {final}")
# 100 -> 90 -> 85, 50 -> 45 -> 40, 25 -> 22.5 -> 17.5, 10 -> 9 -> 4


# =============================================================================
# END OF TUTORIAL
# =============================================================================

print("\n" + "=" * 60)
print("Tutorial complete! Key takeaways:")
print("  1. Functions = reusable, testable blocks of code")
print("  2. return != print — return gives data back to the caller")
print("  3. Scope matters — understand LEGB to avoid bugs")
print("  4. Type hints document intent (but don't enforce at runtime)")
print("  5. *args and **kwargs make functions flexible")
print("  6. Lambdas are great for short throwaway functions")
print("  7. Higher-order functions unlock powerful data transformations")
print("  8. NEVER use mutable default arguments (use None instead)")
print("=" * 60)
