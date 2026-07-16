###############################################################################
#               06 - Advanced Functions and Scope                             #
###############################################################################
#
# SOURCE: Coding_Python/1. Python - Intro/06_functions_advanced.py (979 lines)
#         LPLV26MAY/L08 - Functions (001-011)
#
# COMPLEXITY OVERVIEW:
#   Function call overhead : O(1)  — stack frame allocation
#   *args collection       : O(k)  — k extra positional args
#   **kwargs collection    : O(k)  — k extra keyword args
#   map / filter           : O(n)  — single pass, lazy iterator
#   reduce                 : O(n)  — single left-fold pass
#   sorted(key=fn)         : O(n log n) — Timsort, fn called O(n) times
#   Matrix multiplication  : O(p * q * c), O(n³) for square matrices

from functools import reduce
from typing import List, Optional


# =============================================================================
# SECTION 1: Why Functions Exist — DRY and Modularity
# =============================================================================
#
# A function is a reusable block of code that performs a specific task.
#
# WHY functions matter:
#   1. Modularity   — break big problems into small, manageable pieces
#   2. Reusability  — write once, call many times
#   3. Readability  — meaningful names make code self-documenting
#   4. Testability  — test each function independently
#   5. DRY          — Don't Repeat Yourself — one place to change

def why_functions_demo():
    """Contrast code with and without functions."""
    print("=" * 60)
    print("SECTION 1: Why Functions Exist")
    print("=" * 60)

    # WITHOUT functions — DRY violation
    print("\n  Without function (DRY violation — edit 3 places if greeting changes):")
    print("    Hello, Alice! Welcome aboard.")
    print("    Hello, Bob! Welcome aboard.")
    print("    Hello, Charlie! Welcome aboard.")

    # WITH a function — single source of truth
    def greet(name: str) -> None:
        print(f"    Hello, {name}! Welcome aboard.")

    print("\n  With function (single source of truth):")
    greet("Alice")
    greet("Bob")
    greet("Charlie")
    print("  Change the greeting once inside greet() and ALL calls update.")


# =============================================================================
# SECTION 2: Parameters vs Arguments — The Critical Distinction
# =============================================================================
#
# PARAMETER = the variable name in the function DEFINITION (placeholder)
# ARGUMENT  = the actual value you PASS when calling the function
#
# Memory walkthrough for multiply(4, 7):
#   1. Python evaluates a=4, b=7
#   2. Creates a NEW local stack frame:  x=4, y=7  (parameters bound to args)
#   3. Computes x * y = 28
#   4. Returns 28 → calling frame receives it → local frame is DESTROYED

def multiply(x, y):            # x, y are PARAMETERS (formal parameters)
    return x * y

def params_vs_args_demo():
    print("\n" + "=" * 60)
    print("SECTION 2: Parameters vs Arguments")
    print("=" * 60)

    a, b = 4, 7                # a, b are just variables holding values
    result = multiply(a, b)    # a, b are ARGUMENTS (actual parameters)
    print(f"\n  multiply(4, 7) = {result}")
    print("  x, y are parameters (placeholders in the def).")
    print("  4, 7 (the values of a, b) are arguments (values passed in).")


# =============================================================================
# SECTION 3: return vs print — The Most Common Beginner Confusion
# =============================================================================
#
# print()  → displays to the screen only. The value is NOT usable by the caller.
#             The function implicitly returns None.
# return   → sends the value BACK to the caller. Nothing appears on screen.
#             The caller can store it, compute with it, pass it further.
#
# Rule: in production and interviews, functions should RETURN values.
# Use print() only for debugging or display-only output.

def add_print(a, b):
    print(f"    {a} + {b} = {a + b}")  # side effect only, returns None

def add_return(a, b):
    return a + b                         # silent, value is usable

# Multiple return values — Python packs them into a tuple automatically
def min_max(numbers: List[int]):
    """Return both the minimum and maximum of a list."""
    return min(numbers), max(numbers)    # Python packs as a tuple

# Guard clauses — handle edge cases first via early return
def is_prime(n: int) -> bool:
    """Check if n is prime. Time: O(sqrt(n)) Space: O(1)"""
    if n < 2:                    # guard clause — reject trivially non-prime
        return False
    i = 2
    while i * i <= n:            # only need to check up to sqrt(n)
        if n % i == 0:
            return False         # early return — found a factor, not prime
        i += 1
    return True                  # survived all checks → prime

def return_vs_print_demo():
    print("\n" + "=" * 60)
    print("SECTION 3: return vs print")
    print("=" * 60)

    print("\n  add_print(7, 8):")
    r1 = add_print(7, 8)         # prints 15 on screen
    print(f"  r1 = {r1}   ← None! Can't compute with it.")

    r2 = add_return(7, 8)        # silent, result stored
    print(f"\n  r2 = add_return(7, 8) = {r2}   ← usable!")
    print(f"  r2 * 2 = {r2 * 2}   ← you can compute with returned values")

    # Multiple return values
    lo, hi = min_max([3, 1, 4, 1, 5, 9])
    print(f"\n  min_max([3,1,4,1,5,9]) → min={lo}, max={hi}  (tuple unpacking)")

    # Guard clauses / early return
    print(f"\n  is_prime(7)  = {is_prime(7)}")
    print(f"  is_prime(10) = {is_prime(10)}")
    print(f"  is_prime(1)  = {is_prime(1)}   ← guard clause catches n<2")
    print(f"  is_prime(0)  = {is_prime(0)}   ← guard clause catches n<2")


# =============================================================================
# SECTION 4: Positional vs Keyword vs Default Arguments
# =============================================================================
#
# POSITIONAL: assigned by ORDER. First arg → first param, second → second, etc.
# KEYWORD:    assigned by NAME. Order doesn't matter. Explicit and self-documenting.
# DEFAULT:    parameter has a pre-assigned value. Caller may omit it.
#
# RULES:
#   1. Positional arguments must come BEFORE keyword arguments in a call.
#   2. Parameters WITH defaults must come AFTER those WITHOUT in a definition.
#
# Common interview question: "what happens if you put keyword before positional?"
#   → SyntaxError: positional argument follows keyword argument

def describe_pet(animal: str, name: str, age: int) -> None:
    """Print a description of a pet."""
    print(f"    {name} is a {age}-year-old {animal}.")

def power(base: int, exponent: int = 2) -> int:
    """Raise base to exponent. Defaults to squaring."""
    return base ** exponent

def create_profile(name: str, age: int = 0, city: str = "Unknown") -> dict:
    return {"name": name, "age": age, "city": city}

def positional_keyword_demo():
    print("\n" + "=" * 60)
    print("SECTION 4: Positional / Keyword / Default Arguments")
    print("=" * 60)

    print("\n  Positional (ORDER matters):")
    describe_pet("dog", "Buddy", 5)       # animal="dog", name="Buddy", age=5

    print("\n  Keyword (ORDER doesn't matter — very readable for many params):")
    describe_pet(age=3, name="Whiskers", animal="cat")

    print("\n  Mixed (positional BEFORE keyword):")
    describe_pet("parrot", name="Polly", age=2)  # "parrot" fills animal positionally

    print("\n  Default argument (exponent defaults to 2):")
    print(f"    power(5)    = {power(5)}")    # 5² = 25
    print(f"    power(5, 3) = {power(5, 3)}") # 5³ = 125

    print("\n  Multiple defaults:")
    print(f"    {create_profile('Alice')}")
    print(f"    {create_profile('Bob', 25)}")
    print(f"    {create_profile('Charlie', 30, 'Mumbai')}")


# =============================================================================
# SECTION 5: The Mutable Default Argument Trap 🪤
# =============================================================================
#
# DEFAULT VALUES ARE EVALUATED ONCE AT FUNCTION DEFINITION TIME.
# NOT each time the function is called.
#
# For MUTABLE defaults (list, dict, set), the SAME object is reused on every
# call that doesn't supply its own value. It keeps accumulating state.
#
# WHY this happens:
#   Python stores default values on the function object itself:
#     append_BAD.__defaults__ == ([],)     ← that ONE list lives here forever
#   Every call without an explicit lst argument reaches into this object.
#
# THE FIX: use None as an immutable sentinel. None is safe — it's immutable.
#   Create a fresh mutable inside the function body if None is received.
#
# APPLIES TO: list [], dict {}, set set()
# SAFE defaults: int, str, float, bool, tuple, None — all immutable

def append_to_list_BAD(item, lst=[]):
    """
    BAD: The default list [] is created ONCE and shared across ALL calls
    that don't supply lst. Items accumulate across calls!
    """
    lst.append(item)
    return lst

def append_to_list_GOOD(item, lst=None):
    """
    GOOD: None is immutable — safe as sentinel.
    A fresh list is created inside the body for each call that needs one.
    """
    if lst is None:               # sentinel check
        lst = []                  # brand-new list for THIS call
    lst.append(item)
    return lst

def mutable_default_demo():
    print("\n" + "=" * 60)
    print("SECTION 5: Mutable Default Argument Trap")
    print("=" * 60)

    print("\n  ❌ BAD version (lst=[]) — accumulates across calls:")
    print(f"    Call 1: {append_to_list_BAD(1)}")   # [1]
    print(f"    Call 2: {append_to_list_BAD(2)}")   # [1, 2]  ← where did 1 come from?!
    print(f"    Call 3: {append_to_list_BAD(3)}")   # [1, 2, 3] ← the list persists!
    print(f"    append_BAD.__defaults__ = {append_to_list_BAD.__defaults__}")

    # Reset state for clarity — normally you can't easily undo this
    print("\n  ✅ GOOD version (lst=None) — each call gets a fresh list:")
    print(f"    Call 1: {append_to_list_GOOD(1)}")  # [1]
    print(f"    Call 2: {append_to_list_GOOD(2)}")  # [2]  ← independent!
    print(f"    Call 3: {append_to_list_GOOD(3)}")  # [3]  ← independent!

    print("\n  Rule: NEVER use [], {}, or set() as default argument values.")
    print("  Safe sentinel: None. Dict check: `if d is None: d = {}`")


# =============================================================================
# SECTION 6: *args and **kwargs — Packing and Unpacking
# =============================================================================
#
# MENTAL MODEL — *args and **kwargs are COLLECTING BUCKETS:
#
#   call: total(1, 2, 3)
#                ↓  ↓  ↓
#   *args → (1, 2, 3)             ← a TUPLE (ordered, immutable, positional)
#
#   call: info(name="Alice", age=25)
#                 ↓              ↓
#   **kwargs → {"name": "Alice", "age": 25}  ← a DICT (key=value pairs)
#
# The * and ** symbols here mean COLLECT (packing direction).
# In a function CALL they mean SPREAD (unpacking direction) — opposite operation.
#
# ORDER RULE:  regular params → *args → keyword-only → **kwargs
#
# Time: O(k) for collecting k extra arguments | Space: O(k)

def total(*args) -> int:
    """
    Sum any number of positional arguments.
    *args packs all extra positional args into a TUPLE.
    """
    print(f"    args = {args}, type = {type(args).__name__}")
    return sum(args)

def print_info(**kwargs) -> None:
    """
    Print arbitrary keyword arguments.
    **kwargs packs all extra keyword args into a DICT.
    """
    print(f"    kwargs = {kwargs}, type = {type(kwargs).__name__}")
    for key, value in kwargs.items():
        print(f"      {key} = {value}")

def flexible(required, *args, **kwargs):
    """
    Combine regular param, *args, and **kwargs.
    Order: required (normal) → *args → **kwargs
    """
    print(f"    required = {required!r}")
    print(f"    args     = {args}")
    print(f"    kwargs   = {kwargs}")

def add_three(a, b, c):
    return a + b + c

def log_message(level: str, *messages, **metadata):
    """Practical logger: level + arbitrary messages + optional metadata."""
    combined = " | ".join(str(m) for m in messages)
    meta_str = ", ".join(f"{k}={v}" for k, v in metadata.items())
    line = f"[{level.upper()}] {combined}"
    if meta_str:
        line += f"  ({meta_str})"
    print(f"    {line}")

def args_kwargs_demo():
    print("\n" + "=" * 60)
    print("SECTION 6: *args and **kwargs")
    print("=" * 60)

    print("\n  *args (positional bucket → TUPLE):")
    print(f"    total(1,2,3) = {total(1, 2, 3)}")
    print(f"    total(10,20) = {total(10, 20)}")
    print(f"    total()      = {total()}")

    print("\n  **kwargs (keyword bucket → DICT):")
    print_info(name="Alice", age=25, city="Delhi")

    print("\n  Combined: required + *args + **kwargs:")
    flexible("hello", 1, 2, 3, debug=True, verbose=False)

    # --- UNPACKING: spreading list/dict INTO a function call ---
    # * and ** here mean SPREAD (opposite of collecting)
    print("\n  Unpacking: * spreads list, ** spreads dict:")
    numbers = [10, 20, 30]
    print(f"    add_three(*{numbers}) = {add_three(*numbers)}")   # same as add_three(10,20,30)

    config = {"a": 100, "b": 200, "c": 300}
    print(f"    add_three(**{config}) = {add_three(**config)}")   # same as add_three(a=100,...)

    print("\n  Practical logger (level + *messages + **metadata):")
    log_message("info", "Server started", port=8080)
    log_message("error", "Connection failed", "Retrying...", attempt=3, timeout=30)


# =============================================================================
# SECTION 7: Variable Scope — The LEGB Rule
# =============================================================================
#
# When Python encounters a name, it searches in exactly this order:
#
#   L — Local:     inside the current function
#   E — Enclosing: inside any outer/parent function (for nested functions)
#   G — Global:    at the module / file level
#   B — Built-in:  Python's built-in names (print, len, range, sum, ...)
#
# If the name is not found in any of these four layers → NameError.
# Searches outward. NEVER inward (inner scope is invisible to outer scope).
#
# KEY RULES:
#   - To READ  a global inside a function: just use its name (LEGB resolves it)
#   - To MODIFY a global inside a function: must declare `global x` first
#   - To MODIFY an enclosing variable in a nested function: `nonlocal x`
#   - Without the declaration, Python creates a NEW local — a common bug!

global_counter = 0   # G — Global scope

a_global = 3         # G — visible to all functions below

def legb_demo():
    """Demonstrate all four LEGB layers with a concrete call-stack comment."""
    print("\n" + "=" * 60)
    print("SECTION 7: LEGB Scope Rule")
    print("=" * 60)

    # --- Local: lives only inside this function ---
    secret = 42                          # L — local to legb_demo
    print(f"\n  Local variable: secret = {secret}")
    # print(secret) from outside legb_demo → NameError

    # --- Global read (no keyword needed) ---
    def read_global():
        return global_counter            # LEGB: not Local → not Enclosing → Global ✓
    print(f"  Read global (no keyword): global_counter = {read_global()}")

    # --- Global modify (must declare global) ---
    def modify_global():
        global global_counter            # tells Python: use the module-level name
        global_counter += 1
        return global_counter
    print(f"  Modify global (+1): {modify_global()}")
    print(f"  global_counter is now: {global_counter}")

    # --- Full LEGB: outer/inner nesting ---
    def outer():
        b_enclosing = 4                  # E — Enclosing scope (visible to inner)

        def inner():
            c_local = 5                  # L — Local scope
            # Resolution:
            #   c_local     → L (found immediately)
            #   b_enclosing → E (found in outer's frame)
            #   a_global    → G (found at module level)
            #   print       → B (found in built-ins)
            result = a_global * b_enclosing * c_local
            print(f"    inner(): {a_global} * {b_enclosing} * {c_local} = {result}")
            return result

        return inner()

    print(f"\n  Full LEGB demo (3 * 4 * 5):")
    print(f"  outer() = {outer()}")

    # --- Call stack diagram (conceptual) ---
    # ┌────────────────────────────┐
    # │ outer()                    │
    # │   b_enclosing = 4          │
    # │   ┌──────────────────────┐ │
    # │   │ inner()              │ │
    # │   │   c_local = 5        │ │
    # │   │   looks up:          │ │
    # │   │     c_local → L ✓    │ │
    # │   │     b_enclosing → E ✓│ │
    # │   │     a_global → G ✓   │ │
    # │   └──────────────────────┘ │ ← inner() returns, its frame destroyed
    # └────────────────────────────┘ ← outer() returns, its frame destroyed

    # --- nonlocal: modify enclosing scope ---
    def counter_factory():
        """Returns a closure that counts each call via nonlocal."""
        count = 0                        # E — Enclosing
        def increment():
            nonlocal count               # tells Python: use count from outer frame
            count += 1
            return count
        return increment

    my_counter = counter_factory()
    print(f"\n  nonlocal counter:")
    print(f"    Call 1: {my_counter()}")   # 1
    print(f"    Call 2: {my_counter()}")   # 2
    print(f"    Call 3: {my_counter()}")   # 3
    print("  Each call updates 'count' in the enclosing frame, not a new local.")

    # --- Mutation vs Reassignment across function boundaries ---
    # Integers are immutable — reassignment inside a function creates a NEW local.
    # The caller's variable is UNCHANGED.
    def try_increment(x: int) -> None:
        x = x + 1                        # new local 'x', shadows the parameter
        print(f"    Inside try_increment, x = {x}")

    val = 10
    print(f"\n  Mutation vs Reassignment:")
    print(f"    Before: val = {val}")
    try_increment(val)
    print(f"    After:  val = {val}   ← unchanged! (int is immutable)")

    # Correct pattern: RETURN the new value, reassign at the call site
    def increment(x: int) -> int:
        return x + 1

    val = increment(val)
    print(f"    After increment + reassign: val = {val}  ← correct!")


# =============================================================================
# SECTION 8: Type Hints / Annotations
# =============================================================================
#
# Type hints tell readers and IDEs what types a function expects and returns.
# Syntax: def func(param: type) -> return_type:
#
# CRITICAL: type hints do NOT enforce types at runtime!
# They are documentation, not walls. A wrong type will crash at the first
# operation that fails, NOT at the function definition or call.
#
# Common annotations:
#   int, str, float, bool                — basic types
#   List[int], list[int]                 — list of ints
#   Dict[str, int], dict[str, int]       — dict with str keys, int values
#   Optional[int]  or  int | None        — could be int or None
#   Tuple[int, str]                      — tuple with specific types
#   Callable[[int], bool]                — a function: int → bool

def divide(a: float, b: float) -> float:
    """Divide a by b. Guard against division by zero."""
    if b == 0:
        return float('inf')          # guard clause
    return a / b

def find_index(lst: List[int], target: int) -> Optional[int]:
    """Return index of target in lst, or None if not found."""
    for i, val in enumerate(lst):
        if val == target:
            return i
    return None

def type_hints_demo():
    print("\n" + "=" * 60)
    print("SECTION 8: Type Hints")
    print("=" * 60)
    print(f"\n  divide(10, 3) = {divide(10, 3):.4f}")
    print(f"  divide(10, 0) = {divide(10, 0)}  ← guard returns inf")
    print(f"  find_index([10,20,30], 20) = {find_index([10, 20, 30], 20)}")
    print(f"  find_index([10,20,30], 99) = {find_index([10, 20, 30], 99)}")
    print("\n  Type hints are DOCUMENTATION, not enforcement.")
    print("  Violating them causes a runtime crash at the bad operation, not at definition.")


# =============================================================================
# SECTION 9: Lambda Functions
# =============================================================================
#
# A lambda is an anonymous (unnamed), one-EXPRESSION function.
# It automatically returns the result of the expression.
# Syntax: lambda parameters: expression
#
# LAMBDA vs DEF — same machine, different packaging:
#
#   def square(x):          square = lambda x: x ** 2
#       return x ** 2
#
#   Both create a callable: square(5) → 25
#   def  : named, multi-statement, docstring, reusable → prefer for complex logic
#   lambda: anonymous, single expression → ideal as inline key/predicate
#
# WHEN TO USE LAMBDA:
#   - Inside map(), filter(), sorted(), reduce() as a short one-off function
#   - The logic fits in one expression
#   - You won't need to call it by name elsewhere
#
# WHEN TO USE DEF:
#   - You need to reuse it (give it a name)
#   - It needs a docstring
#   - It has multiple statements / conditions

def lambda_demo():
    print("\n" + "=" * 60)
    print("SECTION 9: Lambda Functions")
    print("=" * 60)

    square = lambda x: x ** 2
    add = lambda a, b: a + b
    print(f"\n  square = lambda x: x**2")
    print(f"  square(5) = {square(5)}")
    print(f"  add(3, 7) = {add(3, 7)}")

    # Lambda as inline key for sorted — the canonical use
    words = ["banana", "apple", "cherry", "date"]
    by_len = sorted(words, key=lambda w: len(w))
    by_len_alpha = sorted(words, key=lambda w: (len(w), w))  # two-key sort

    print(f"\n  sorted by length:                 {by_len}")
    print(f"  sorted by (length, alphabetical): {by_len_alpha}")

    students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
    by_grade = sorted(students, key=lambda s: s[1], reverse=True)
    print(f"  sorted students by grade (desc):  {by_grade}")


# =============================================================================
# SECTION 10: Higher-Order Functions — map, filter, reduce, sorted
# =============================================================================
#
# A HIGHER-ORDER FUNCTION either:
#   (a) takes another function as an argument, OR
#   (b) returns a function as its result (closure)
#
# THE FOUR YOU MUST KNOW:
#
#   map(fn, iterable)   → apply fn to every element    → returns lazy iterator
#   filter(fn, iterable)→ keep where fn returns True   → returns lazy iterator
#   reduce(fn, iterable)→ accumulate left-to-right     → returns single value
#   sorted(it, key=fn)  → sort by fn's return value   → returns new list
#
# All four take O(n) calls to fn.
# map and filter return iterators (lazy) — wrap in list() to materialise.
# reduce requires `from functools import reduce`.

def higher_order_demo():
    print("\n" + "=" * 60)
    print("SECTION 10: Higher-Order Functions")
    print("=" * 60)

    # --- map: apply fn to every element ---
    # Time: O(n) | Space: O(1) for the iterator, O(n) when materialised
    temps_c = [0, 20, 37, 100]
    temps_f = list(map(lambda c: c * 9/5 + 32, temps_c))
    print(f"\n  map (Celsius → Fahrenheit):")
    print(f"    Celsius:    {temps_c}")
    print(f"    Fahrenheit: {temps_f}")

    nums = [1, 2, 3, 4, 5]
    squared = list(map(lambda x: x ** 2, nums))
    print(f"  map (square each): {nums} → {squared}")

    # --- filter: keep elements where fn returns True ---
    # Time: O(n) | Space: O(1) lazy, O(k) materialised (k = number that pass)
    ages = [12, 18, 25, 15, 30, 8, 21]
    adults = list(filter(lambda age: age >= 18, ages))
    print(f"\n  filter (adults ≥ 18):")
    print(f"    All ages:  {ages}")
    print(f"    Adults:    {adults}")

    evens = list(filter(lambda x: x % 2 == 0, nums))
    print(f"  filter (evens): {nums} → {evens}")

    # --- reduce: accumulate to a single value (left fold) ---
    # Time: O(n) | Space: O(1)
    # Step-by-step for product of [1,2,3,4,5]:
    #   acc=1,  x=2  → 1*2  = 2
    #   acc=2,  x=3  → 2*3  = 6
    #   acc=6,  x=4  → 6*4  = 24
    #   acc=24, x=5  → 24*5 = 120
    product = reduce(lambda acc, x: acc * x, nums)
    print(f"\n  reduce (product of {nums}):")
    print(f"    [1*2→2, 2*3→6, 6*4→24, 24*5→120]")
    print(f"    Result = {product}")

    total_chars = reduce(lambda acc, w: acc + len(w), ["hello", "world", "!"], 0)
    print(f"  reduce (total chars in ['hello','world','!']) = {total_chars}")

    # --- sorted with key= and complex keys ---
    # Time: O(n log n) | The key function is called O(n) times
    data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35}]
    by_age = sorted(data, key=lambda p: p["age"])
    print(f"\n  sorted(people, key=age): {[d['name'] for d in by_age]}")

    # Tiered sort: primary = length, secondary = alphabetical
    words = ["banana", "apple", "pear", "kiwi", "grape"]
    by_len_alpha = sorted(words, key=lambda w: (len(w), w))
    print(f"  sorted(words, key=(len,alpha)): {by_len_alpha}")


# =============================================================================
# SECTION 11: Closures — Functions with a "Backpack"
# =============================================================================
#
# A CLOSURE is an inner function that remembers variables from its enclosing
# scope even AFTER the outer function has returned and its frame is gone.
#
# HOW: Python detects that 'factor' is needed by multiplier, so instead of
# destroying it when make_multiplier returns, it stores 'factor' inside the
# returned function object itself — like tucking it into a "backpack".
#
# Each call to make_multiplier creates a NEW closure with its OWN backpack.
# double and triple are independent — they don't share state.
#
# WHY CLOSURES MATTER:
#   - Factory pattern: make_multiplier, make_adder, make_validator
#   - Stateful callbacks without class overhead
#   - DFS counters: use nonlocal to update a captured variable

def make_multiplier(factor: int):
    """
    Returns a function that multiplies its input by 'factor'.
    'factor' is captured in the closure's __closure__ cell.
    """
    def multiplier(x):
        return x * factor           # factor comes from ENCLOSING scope (LEGB: E)
    return multiplier               # return the FUNCTION OBJECT (not calling it!)

def apply_twice(func, value):
    """Higher-order: apply a function to its own output. func(func(value))."""
    return func(func(value))

def pipeline(data, *functions):
    """Pass data through a series of functions in sequence."""
    result = data
    for func in functions:
        result = func(result)
    return result

def closures_demo():
    print("\n" + "=" * 60)
    print("SECTION 11: Closures")
    print("=" * 60)

    double = make_multiplier(2)    # double's backpack: {factor: 2}
    triple = make_multiplier(3)    # triple's backpack: {factor: 3}

    print(f"\n  double = make_multiplier(2)  →  double's backpack: factor=2")
    print(f"  triple = make_multiplier(3)  →  triple's backpack: factor=3")
    print(f"  double(5) = {double(5)}   ← opens its own backpack")
    print(f"  triple(5) = {triple(5)}   ← opens its own independent backpack")

    # apply_twice: HOF that calls a function twice
    print(f"\n  apply_twice(square, 3):")
    print(f"    Step 1: 3²  = 9")
    print(f"    Step 2: 9²  = 81")
    print(f"    Result: {apply_twice(lambda x: x**2, 3)}")

    # Pipeline: compose functions left-to-right
    raw = "  Hello, World!  "
    cleaned = pipeline(raw, str.strip, str.lower, lambda s: s.replace("!", ""))
    print(f"\n  Pipeline (strip → lower → remove !):")
    print(f"    Input:  '{raw}'")
    print(f"    Output: '{cleaned}'")


# =============================================================================
# SECTION 12: Matrix Multiplication from Scratch
# =============================================================================
#
# A matrix is a list of rows: mat[i][j] = element at row i, column j.
#
# DIMENSION RULE:
#   mat1: (p × q)  @  mat2: (q × c)   ← INNER dimensions MUST match (both q)
#          ┗━━━━━━━┛
#        must be equal
#   result: (p × c)   ← OUTER dimensions become the result shape
#
# FORMULA for each result cell:
#   result[i][j] = dot product of row i of mat1 with column j of mat2
#                = Σ (k = 0..q-1)  mat1[i][k] * mat2[k][j]
#
# MANUAL VERIFICATION for result[0][0]:
#   row 0 of mat1 = [1, 2, 3], col 0 of mat2 = [7, 9, 11]
#   1*7 + 2*9 + 3*11 = 7 + 18 + 33 = 58
#
# TIME COMPLEXITY:  O(p * q * c) — three nested loops.
#                   For square n×n matrices: O(n³).
# SPACE COMPLEXITY: O(p * c) — the result matrix.
#
# NOTE: In production, NEVER write this by hand.
#   Use NumPy: np.array(m1) @ np.array(m2)  — C-implemented, 100×+ faster.
#   Implement from scratch in interviews to show nested-loop mastery.

def mat_multiply(mat1: List[List[int]], mat2: List[List[int]]) -> List[List[int]]:
    """
    Multiply two matrices. Returns the result matrix or raises ValueError.
    mat1: p × q   mat2: q × c   →   result: p × c

    Time: O(p * q * c) | Space: O(p * c)
    """
    p  = len(mat1)       # rows of mat1
    q1 = len(mat1[0])    # cols of mat1 (= inner dimension)
    q2 = len(mat2)       # rows of mat2 (must equal q1)
    c  = len(mat2[0])    # cols of mat2

    if q1 != q2:
        raise ValueError(f"Dimension mismatch: mat1 cols={q1} ≠ mat2 rows={q2}")

    # Initialize result matrix with 0s using a nested comprehension.
    # CRITICAL: [[0] * c] * p creates p REFERENCES to the same row!
    # [[0 for _ in range(c)] for _ in range(p)] creates p INDEPENDENT rows.
    result = [[0 for _ in range(c)] for _ in range(p)]

    for i in range(p):               # rows of mat1  (= rows of result)
        for j in range(c):           # cols of mat2  (= cols of result)
            for k in range(q1):      # shared/inner dimension
                result[i][j] += mat1[i][k] * mat2[k][j]   # dot product accumulation

    return result

def matrix_demo():
    print("\n" + "=" * 60)
    print("SECTION 12: Matrix Multiplication")
    print("=" * 60)

    mat1 = [[1, 2, 3],
            [4, 5, 6]]           # 2×3
    mat2 = [[7,  8],
            [9,  10],
            [11, 12]]            # 3×2  ← q (inner dim) matches: 3==3 ✓

    print(f"\n  mat1 (2×3): {mat1}")
    print(f"  mat2 (3×2): {mat2}")

    result = mat_multiply(mat1, mat2)
    print(f"  result (2×2): {result}")
    print(f"  Verification: result[0][0] = 1*7+2*9+3*11 = {1*7+2*9+3*11} ✓")
    print(f"  Verification: result[1][1] = 4*8+5*10+6*12 = {4*8+5*10+6*12} ✓")

    # Mismatched dimensions
    print(f"\n  Mismatched shapes (2×2) @ (1×3):")
    try:
        mat_multiply([[1,2],[3,4]], [[1,2,3]])
    except ValueError as e:
        print(f"    ValueError: {e}")

    print(f"\n  Complexity: O(p*q*c). For square n×n matrices → O(n³).")
    print(f"  Space: O(p*c) for the result matrix.")


# =============================================================================
# SECTION 13: Functions vs Methods + dir() Introspection
# =============================================================================

def introspection_demo():
    print("\n" + "=" * 60)
    print("SECTION 13: Functions vs Methods + dir()")
    print("=" * 60)

    # Function: standalone, not tied to any object
    def is_even(n): return n % 2 == 0

    # Method: called ON an object, implicitly receives the object as self
    nums = [1, 2, 3]
    nums.append(4)

    print(f"\n  is_even(4) [function]: {is_even(4)}")
    print(f"  nums after .append(4) [method]: {nums}")

    # dir() — discover what's available on any object
    list_methods = [m for m in dir([]) if not m.startswith('__')]
    print(f"\n  Public list methods (dir([])): {list_methods}")
    print(f"  Pro tip: when you forget a method name → dir(obj) is your friend.")


# =============================================================================
# SECTION 14: Practice Exercises (from source §12)
# =============================================================================

# --- Exercise 1: First M Primes ---
# Uses is_prime() from Section 3 (O(sqrt(p)) per check).
# Time: O(m * sqrt(p_m)) where p_m is the m-th prime  | Space: O(1)

def first_m_primes(m: int) -> List[int]:
    """Return a list of the first m prime numbers."""
    primes = []
    num = 2
    while len(primes) < m:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes


# --- Exercise 2: Fibonacci as a List ---
# Time: O(n) — single pass  | Space: O(n) — storing the list

def fibonacci(n: int) -> List[int]:
    """Return the first n Fibonacci numbers as a list."""
    if n <= 0: return []          # guard clause
    if n == 1: return [0]         # guard clause
    fibs = [0, 1]
    for _ in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])   # each = sum of previous two
    return fibs


# --- Exercise 3: Word Frequency Counter ---
# Time: O(n) where n = words  | Space: O(k) where k = unique words

def word_frequency(text: str) -> dict:
    """Count occurrences of each word (case-insensitive)."""
    freq: dict = {}
    for word in text.lower().split():
        freq[word] = freq.get(word, 0) + 1   # .get() returns 0 if missing
    return freq


# --- Exercise 4: Flexible Statistics Calculator (*args) ---
# Time: O(n log n) — dominated by sort for median  | Space: O(n)

def stats(*args: float) -> dict:
    """Calculate basic statistics for any number of values passed as *args."""
    if not args:
        return {"error": "No values provided"}
    n = len(args)
    total = sum(args)
    sorted_args = sorted(args)
    median = (
        sorted_args[n // 2]                                        # odd count
        if n % 2 == 1
        else (sorted_args[n // 2 - 1] + sorted_args[n // 2]) / 2  # even count
    )
    return {
        "count": n,
        "sum":   total,
        "mean":  round(total / n, 2),
        "min":   min(args),
        "max":   max(args),
        "median": median,
    }


# --- Exercise 5: Discount Pipeline (higher-order functions) ---
# Time: O(n * d) where n = items, d = discount functions  | Space: O(n)

def apply_discounts(prices: List[float], *discount_fns) -> List[float]:
    """Apply a chain of discount functions to each price in sequence."""
    result = list(prices)                        # copy — don't mutate input
    for discount in discount_fns:
        result = [discount(p) for p in result]   # apply each discount to all prices
    return [round(p, 2) for p in result]

def exercises_demo():
    print("\n" + "=" * 60)
    print("SECTION 14: Practice Exercises")
    print("=" * 60)

    print(f"\n  Ex 1 — First 10 primes: {first_m_primes(10)}")

    print(f"\n  Ex 2 — First 10 Fibonacci: {fibonacci(10)}")
    # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    sample = "the cat sat on the mat the cat"
    print(f"\n  Ex 3 — Word frequency of '{sample}':")
    print(f"    {word_frequency(sample)}")

    print(f"\n  Ex 4 — stats(10, 20, 30, 40, 50):")
    for k, v in stats(10, 20, 30, 40, 50).items():
        print(f"    {k}: {v}")

    ten_pct_off = lambda p: p * 0.90
    flat_five   = lambda p: max(0, p - 5)
    prices = [100.0, 50.0, 25.0, 10.0]
    final = apply_discounts(prices, ten_pct_off, flat_five)
    print(f"\n  Ex 5 — Discount pipeline (10% off, then $5 off):")
    print(f"    Original: {prices}")
    print(f"    Final:    {final}")
    # 100→90→85, 50→45→40, 25→22.5→17.5, 10→9→4


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_filter_evens(nums: List[int]) -> List[int]:
    """
    Use filter() and a lambda to return only even numbers.
    Hint: list(filter(lambda x: x % 2 == 0, nums))
    """
    pass

def practice_nested_counter():
    """
    Create an outer function initialising total_sum = 0.
    Create an inner function add(n) using nonlocal to add n to total_sum.
    Call add(5) and add(10), then return total_sum.
    """
    pass

def practice_make_adder(n: int):
    """
    Return a closure that adds n to its argument.
    double = make_adder(10) → double(5) should return 15.
    Hint: return a def/lambda that uses 'n' from enclosing scope.
    """
    pass

def practice_safe_append(item, lst=None) -> List:
    """
    Append item to lst and return lst.
    If lst is None, create a fresh list each time.
    The mutable default trap version (lst=[]) must NOT be used.
    """
    pass

def practice_mat_multiply(mat1: List[List[int]], mat2: List[List[int]]) -> List[List[int]]:
    """
    Multiply two matrices using the triple-nested loop algorithm.
    Raise ValueError if inner dimensions don't match.
    Time: O(p * q * c) | Space: O(p * c)
    """
    pass

def practice_stats_pipeline(*nums: float) -> dict:
    """
    Using *args, compute and return a dict with:
    {'count': n, 'sum': s, 'mean': m, 'min': lo, 'max': hi}
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    why_functions_demo()
    params_vs_args_demo()
    return_vs_print_demo()
    positional_keyword_demo()
    mutable_default_demo()
    args_kwargs_demo()
    legb_demo()
    type_hints_demo()
    lambda_demo()
    higher_order_demo()
    closures_demo()
    matrix_demo()
    introspection_demo()
    exercises_demo()

    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS")
    print("=" * 60)
    print("filter_evens([1..6]):", practice_filter_evens([1, 2, 3, 4, 5, 6]))
    print("nested_counter():", practice_nested_counter())
    adder = practice_make_adder(10)
    print("make_adder(10)(5):", adder(5) if adder else None)
    print("safe_append(1):", practice_safe_append(1))
    print("safe_append(2):", practice_safe_append(2))
    m1 = [[1,2],[3,4]]
    m2 = [[5,6],[7,8]]
    print("mat_multiply([[1,2],[3,4]], [[5,6],[7,8]]):", practice_mat_multiply(m1, m2))
    print("stats_pipeline(10,20,30):", practice_stats_pipeline(10, 20, 30))
    print("=" * 60)
    print("Fill in the skeletons above and re-run to verify.")
