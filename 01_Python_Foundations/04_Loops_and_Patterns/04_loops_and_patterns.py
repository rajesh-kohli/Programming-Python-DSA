# =============================================================================
# MODULE 04 — LOOPS AND PATTERNS
# File   : 04_loops_and_patterns.py
# Topics : while loops · for loops · loop control · patterns · DSA problems
# Author : Python + DSA Learning Repository
# =============================================================================
# HARDCODED TEST VALUES (no input() calls anywhere in this file)
#   n            = 10  (general loop count)
#   n_pyramid    = 5   (for pyramid / pattern problems)
#   number_digit = 123 (digit-sum / even-digit tests)
#   number_palin = 121 (palindrome check)
#   prime_test1  = 7   (prime — IS prime)
#   prime_test2  = 27  (prime — NOT prime)
#   lower_limit  = 10  upper_limit = 30 (prime range)
# =============================================================================

import math


# =============================================================================
# SECTION 1: THE LOOP ANALOGY — WHY LOOPS EXIST
# =============================================================================
# Think of Santa delivering gifts:
#
#   ITERATIVE (loop):               RECURSIVE (function calling itself):
#   Santa keeps a list.             Santa delegates sub-routes to Elves.
#   He ticks each house until done. Each Elf handles one sub-route.
#   One agent, repeated action.     Many agents, nested structure.
#
# Loops are the "one agent, repeated action" approach.
#
# EVERY loop has THREE mandatory components:
#
#   ┌─────────────────┬────────────────────────────────────────────────────┐
#   │  Component      │  Purpose                                           │
#   ├─────────────────┼────────────────────────────────────────────────────┤
#   │  INIT           │  Set starting state (e.g. i = 1)                  │
#   │  CONDITION      │  Guard — keep going while True                     │
#   │  UPDATE         │  Advance state (e.g. i += 1) — prevents infinity  │
#   └─────────────────┴────────────────────────────────────────────────────┘
#
# Missing UPDATE → INFINITE LOOP.
# Missing INIT   → NameError or stale value.
# Missing CONDITION guard → IndexError / wrong results.
# =============================================================================


# =============================================================================
# SECTION 2: WHILE LOOPS
# =============================================================================
#
# WHILE LOOP FLOW DIAGRAM:
#
#   ┌──────────────────────────────────────────┐
#   │  INIT  →  [CONDITION?]  →  NO  → EXIT   │
#   │                ↓ YES                     │
#   │           [LOOP BODY]                    │
#   │                ↓                         │
#   │            [UPDATE]  ───────→  [CONDITION?]│
#   └──────────────────────────────────────────┘
#
# Syntax:
#   i = 0          # INIT
#   while i < n:   # CONDITION
#       ...        # BODY
#       i += 1     # UPDATE

print("\n" + "="*65)
print("  SECTION 2 — WHILE LOOPS")
print("="*65)

# ------------------------------------------------------------------
# EXAMPLE 2-1: Print 1 to 10   | TIME: O(n) | SPACE: O(1)
# ------------------------------------------------------------------
# Trace table (n=10):
#   i  | Condition (i<=10) | Action       | i after update
#   1  |       True        | print 1      |   2
#   2  |       True        | print 2      |   3
#   ...
#   10 |       True        | print 10     |  11
#   11 |       False       | EXIT LOOP    |  --
# ------------------------------------------------------------------
print("\n--- Example 2-1: Print 1 to 10 ---")
i = 1                          # INIT
while i <= 10:                 # CONDITION
    print(i, end=" ")          # Expected Output: 1 2 3 4 5 6 7 8 9 10
    i += 1                     # UPDATE
print()

# TIME COMPLEXITY: O(n)   — loop body runs n times
# SPACE COMPLEXITY: O(1)  — only one variable i

# ------------------------------------------------------------------
# EXAMPLE 2-2: INFINITE LOOP DEMONSTRATION (commented — safe to read)
# ------------------------------------------------------------------
# The code below is intentionally commented out.
# If you run it, the program will NEVER terminate.
#
# BAD CODE (DO NOT UNCOMMENT):
#   i = 1
#   while i <= 10:
#       print(i)
#       # i += 1  ← UPDATE IS MISSING
#                   i stays 1 forever → infinite loop
#
# Python has no built-in infinite-loop protection.
# Always verify: does your loop variable change every iteration?

print("\n--- Example 2-2: Infinite Loop Danger (explained, not run) ---")
print("An infinite loop occurs when UPDATE is missing.")  # Output: reminder msg

# ------------------------------------------------------------------
# EXAMPLE 2-3: Conditional printing — even→print i, odd→print i+1
# ------------------------------------------------------------------
# Pattern: if i is even print i; if i is odd print i+1
# For n=10: 1→2, 2→2, 3→4, 4→4, 5→6, 6→6, 7→8, 8→8, 9→10, 10→10
# ------------------------------------------------------------------
print("\n--- Example 2-3: Even→i, Odd→i+1 ---")
i = 1
while i <= 10:
    if i % 2 == 0:
        print(f"i={i}: even → print {i}")     # Output: i=2: even → print 2
    else:
        print(f"i={i}: odd  → print {i+1}")   # Output: i=1: odd  → print 2
    i += 1

# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# EXAMPLE 2-4: Bitwise operators inside loop   i << 2, i >> 2
# ------------------------------------------------------------------
# i << 2  = i * 4  (left shift: multiply by 2^2)
# i >> 2  = i // 4 (right shift: integer divide by 2^2)
# mod 3 check: print only when i is divisible by 3
# ------------------------------------------------------------------
print("\n--- Example 2-4: Bitwise shifts + mod 3 check ---")
i = 1
while i <= 12:
    left  = i << 2       # i * 4
    right = i >> 2       # i // 4
    if i % 3 == 0:
        print(f"i={i:2d} | i<<2={left:3d} | i>>2={right} | (divisible by 3)")  # Output annotations
    else:
        print(f"i={i:2d} | i<<2={left:3d} | i>>2={right}")
    i += 1
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# EXAMPLE 2-5: Operator Precedence WARNING — i+1<<2 is i+(1<<2)
# ------------------------------------------------------------------
# ⚠️  OPERATOR PRECEDENCE TRAP:
#     i + 1 << 2   is evaluated as   i + (1 << 2)   = i + 4
#     NOT as   (i + 1) << 2
#
# << has LOWER precedence than +, so + binds first.
# This is a VERY common bug. Always use explicit parentheses!
# ------------------------------------------------------------------
print("\n--- Example 2-5: Precedence Warning  i+1<<2 vs (i+1)<<2 ---")
i = 3
result_wrong  = i + 1 << 2   # parsed as i + (1<<2) = 3 + 4 = 7
result_right  = (i + 1) << 2  # parsed as (3+1)<<2 = 4*4 = 16
print(f"i=3: i+1<<2 (wrong intent) = {result_wrong}")   # Output: 7
print(f"i=3: (i+1)<<2 (correct)   = {result_right}")    # Output: 16

i = 1
while i <= 5:
    step3_shift = i + 3           # simulated step-3 loop
    bitwise_val = step3_shift << 2
    print(f"  i={i} | i+3={step3_shift} | (i+3)<<2={bitwise_val}")
    i += 3
# TIME COMPLEXITY: O(n/step) = O(n)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# EXAMPLE 2-6: Nested conditions with bitwise
# ------------------------------------------------------------------
print("\n--- Example 2-6: Nested conditions with bitwise ---")
i = 1
while i <= 16:
    msb = i >> 3          # top bits (i // 8)
    lsb = i & 0b0111      # bottom 3 bits (i % 8)
    if msb > 0 and lsb % 2 == 0:
        print(f"  i={i:2d} (0b{i:04b}) | msb={msb} | lsb={lsb} ← msb>0 & lsb even")  # Output annotated
    i += 1
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# EXAMPLES 2-7/8/9: CRITICAL NESTED WHILE LOOP BUG
# ------------------------------------------------------------------
#
# BUG: j initialized OUTSIDE the outer while loop.
#      After the first inner loop finishes, j == n.
#      On every subsequent outer iteration, j >= n is
#      ALREADY TRUE so the inner loop body NEVER runs again.
#
# TRACE (n=3, buggy version):
#   outer_i=1, j=1 → inner runs: j=1,2,3 → j becomes 4
#   outer_i=2, j=4 → condition j<=3 is FALSE immediately → skip
#   outer_i=3, j=4 → condition j<=3 is FALSE immediately → skip
#   → Only 1 row printed instead of 3!
#
# VISUAL:
#   Expected (3×3 grid):      Buggy output (1×3 only):
#     * * *                     * * *
#     * * *
#     * * *

print("\n--- Examples 2-7/8/9: Nested While Loop Bug ---")

# *** BUG: j initialized outside outer loop — inner loop runs only once ***
# n_pyramid = 5
# j = 1                     ← BUG: j never reset per outer iteration
# i = 1
# while i <= n_pyramid:
#     while j <= n_pyramid:
#         print("*", end=" ")
#         j += 1            ← after first outer pass j == n_pyramid+1
#     i += 1
#     print()
# *** END BUG block ***

# *** FIX: reset j = 1 INSIDE the outer loop, at the top of each iteration ***
print("BUGGY OUTPUT (only 1 row would print):")
# Demonstrate the bug with n=3 so we can show it:
n_demo = 3
j = 1                     # *** BUG: j set here — outside outer loop ***
i = 1
while i <= n_demo:
    while j <= n_demo:    # j is already > n_demo after 1st outer pass
        print("*", end=" ")
        j += 1
    print()
    i += 1
# Output: * * *
#         (blank)
#         (blank)   — inner loop skipped on outer i=2 and i=3

print("\nFIXED OUTPUT (all rows print correctly):")
n_demo = 3
i = 1
while i <= n_demo:
    j = 1                 # *** FIX: j reset to 1 inside the outer loop ***
    while j <= n_demo:
        print("*", end=" ")
        j += 1
    print()
    i += 1
# Output: * * *
#         * * *
#         * * *

# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)


# =============================================================================
# SECTION 3: FOR LOOPS
# =============================================================================
#
# range() produces values LAZILY — O(1) memory regardless of n.
# It is a generator-like object, not a physical list.
#
# FORMS:
#   range(stop)             → 0, 1, ..., stop-1
#   range(start, stop)      → start, ..., stop-1
#   range(start, stop, step)→ start, start+step, ... (< stop)

print("\n" + "="*65)
print("  SECTION 3 — FOR LOOPS")
print("="*65)

# ------------------------------------------------------------------
# EXAMPLE 3-1: Even numbers 0 to 8 using step=2
# ------------------------------------------------------------------
print("\n--- Example 3-1: Even numbers 0–8 ---")
for i in range(0, 9, 2):
    print(i, end=" ")          # Output: 0 2 4 6 8
print()
# TIME COMPLEXITY: O(n/2) = O(n)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# EXAMPLE 3-2: All three range() forms
# ------------------------------------------------------------------
print("\n--- Example 3-2: Three forms of range() ---")
print("range(5)         →", list(range(5)))           # Output: [0, 1, 2, 3, 4]
print("range(1,6)       →", list(range(1, 6)))         # Output: [1, 2, 3, 4, 5]
print("range(0,10,2)    →", list(range(0, 10, 2)))     # Output: [0, 2, 4, 6, 8]
print("range(10,0,-2)   →", list(range(10, 0, -2)))    # Output: [10, 8, 6, 4, 2]

# ------------------------------------------------------------------
# EXAMPLE 3-3: OPERATOR PRECEDENCE WARNING — i >> 2 + 1
# ------------------------------------------------------------------
# ⚠️  i >> 2 + 1  is evaluated as  i >> (2+1)  = i >> 3  = i // 8
#     NOT as  (i >> 2) + 1
#
# + has HIGHER precedence than >>. So + is evaluated first.
# ------------------------------------------------------------------
print("\n--- Example 3-3: Precedence  i>>2+1 vs (i>>2)+1 ---")
for i in [8, 16, 24]:
    wrong   = i >> 2 + 1       # i >> 3 = i // 8
    correct = (i >> 2) + 1     # (i // 4) + 1
    print(f"  i={i:2d}: i>>2+1 (wrong intent)={wrong}  |  (i>>2)+1 (correct)={correct}")
# Output:
#   i= 8: i>>2+1 (wrong intent)=1  |  (i>>2)+1 (correct)=3
#   i=16: i>>2+1 (wrong intent)=2  |  (i>>2)+1 (correct)=5
#   i=24: i>>2+1 (wrong intent)=3  |  (i>>2)+1 (correct)=7

# ------------------------------------------------------------------
# EXAMPLE 3-4: NESTED FOR LOOPS — Grid mental model
# ------------------------------------------------------------------
#
#   Outer loop picks ROW    (i = 0 to n-1)
#   Inner loop sweeps COLUMN (j = 0 to n-1)
#
#   ASCII GRID (n=4):
#   ┌─────────────────────────────┐
#   │  j→  0     1     2     3   │
#   │ i↓                         │
#   │  0  (0,0) (0,1) (0,2) (0,3)│
#   │  1  (1,0) (1,1) (1,2) (1,3)│
#   │  2  (2,0) (2,1) (2,2) (2,3)│
#   │  3  (3,0) (3,1) (3,2) (3,3)│
#   └─────────────────────────────┘
# ------------------------------------------------------------------
print("\n--- Example 3-4: Nested for loops + modulo ---")
n = 4
for i in range(n):              # outer: rows
    for j in range(n):          # inner: columns
        cell = (i * n + j) % 3  # arbitrary formula for demo
        print(f"{cell}", end=" ")   # Output: 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0
    print()
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# EXAMPLE 3-5: Nested with conditional + bitwise
# ------------------------------------------------------------------
print("\n--- Example 3-5: Nested with conditional + bitwise ---")
for i in range(1, 5):
    for j in range(1, i + 1):
        val = (i ^ j) & 0xFF    # XOR then mask to 8 bits
        if val % 2 == 0:
            print(f"E{val:02d}", end=" ")   # Output: even XOR values
        else:
            print(f"O{val:02d}", end=" ")   # Output: odd  XOR values
    print()
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# EXAMPLE 3-6: TRIPLE NESTED LOOP — O(n³) WARNING
# ------------------------------------------------------------------
print("\n--- Example 3-6: Triple nested loop — O(n³) ---")
# ⚠️  For n=100, this would run 1,000,000 iterations.
# Keep n small for demonstration.
triple_sum = 0
n_small = 5
for i in range(n_small):
    for j in range(n_small):
        for k in range(n_small):
            triple_sum += 1
print(f"n={n_small}, triple_sum (iterations)={triple_sum}")  # Output: 125
# TIME COMPLEXITY: O(n³)  ← CUBIC! Avoid for large n.
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# EXAMPLE 3-7: FOR-ELSE — else runs only when no break occurred
# ------------------------------------------------------------------
print("\n--- Example 3-7: for-else / while-else ---")

def search_for(target, lst):
    """Return True if target found (using for-else pattern)."""
    for item in lst:
        if item == target:
            print(f"  Found {target}! Breaking...")  # Output if found
            break                                     # skip else block
    else:
        # This block runs ONLY if the loop completed without break
        print(f"  {target} NOT found — else block executed")  # Output if not found
    return item == target if lst else False

search_for(3, [1, 2, 3, 4, 5])   # Output: Found 3! Breaking...
search_for(9, [1, 2, 3, 4, 5])   # Output: 9 NOT found — else block executed
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)


# =============================================================================
# SECTION 4: PRACTICE PROBLEMS (from 06_loop_practice_problems.py)
# =============================================================================

print("\n" + "="*65)
print("  SECTION 4 — PRACTICE PROBLEMS")
print("="*65)

# ------------------------------------------------------------------
# PROBLEM 4-1: Sum of EVEN numbers from 1 to N
# ------------------------------------------------------------------
# APPROACH 1 (Loop)   — O(n) time, O(1) space
# APPROACH 2 (Formula)— O(1) time, O(1) space  →  n//2 * (n//2 + 1)
#   For n=10: evens are 2,4,6,8,10 → sum = 2+4+6+8+10 = 30
#   Formula: floor(n/2) * (floor(n/2) + 1) = 5 * 6 = 30  ✓
# ------------------------------------------------------------------
n = 10
print(f"\n--- Problem 4-1: Sum of even numbers 1 to {n} ---")

# Approach 1 — Loop
even_sum_loop = 0
for i in range(1, n + 1):
    if i % 2 == 0:
        even_sum_loop += i
print(f"  Loop approach  : {even_sum_loop}")        # Output: 30

# Approach 2 — Formula  O(1)
k = n // 2
even_sum_formula = k * (k + 1)
print(f"  Formula O(1)   : {even_sum_formula}")     # Output: 30

# TIME COMPLEXITY: O(n) loop / O(1) formula
# SPACE COMPLEXITY: O(1) both

# ------------------------------------------------------------------
# PROBLEM 4-2: Sum of |even - odd| digits-style difference
# ------------------------------------------------------------------
# For 1 to n: split into even_sum and odd_sum, return absolute diff.
# n=10: even_sum=2+4+6+8+10=30, odd_sum=1+3+5+7+9=25, diff=5
# ------------------------------------------------------------------
print(f"\n--- Problem 4-2: |sum_even - sum_odd| for 1 to {n} ---")
sum_even = sum_odd = 0
for i in range(1, n + 1):
    if i % 2 == 0:
        sum_even += i
    else:
        sum_odd += i
diff = abs(sum_even - sum_odd)
print(f"  sum_even={sum_even}, sum_odd={sum_odd}, |diff|={diff}")  # Output: 30, 25, 5
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PROBLEM 4-3: Sum of Digits  — TWO approaches
# ------------------------------------------------------------------
# number = 123 → digits: 1, 2, 3 → sum = 6
#
# APPROACH 1 — Mathematical (mod / div)   O(log₁₀ n) time, O(1) space
#   123 % 10 = 3  → add 3, number = 123//10 = 12
#    12 % 10 = 2  → add 2, number =  12//10 =  1
#     1 % 10 = 1  → add 1, number =   1//10 =  0
#   → stop when number == 0
#
# APPROACH 2 — String conversion  O(d) time, O(d) space (d = digit count)
# ------------------------------------------------------------------
number_digit = 123
print(f"\n--- Problem 4-3: Sum of digits of {number_digit} ---")

# Approach 1 — Mathematical
temp = number_digit
digit_sum_math = 0
while temp > 0:
    digit_sum_math += temp % 10    # extract last digit
    temp //= 10                    # remove last digit
print(f"  Math approach  : {digit_sum_math}")       # Output: 6

# Approach 2 — String
digit_sum_str = sum(int(d) for d in str(number_digit))
print(f"  String approach: {digit_sum_str}")        # Output: 6

# TIME COMPLEXITY: O(log₁₀ n) math / O(d) string where d = len(str(n))
# SPACE COMPLEXITY: O(1) math / O(d) string

# ------------------------------------------------------------------
# PROBLEM 4-4: Sum of EVEN digits only
# ------------------------------------------------------------------
# number = 123: digits 1(odd), 2(even), 3(odd) → even digit sum = 2
# ------------------------------------------------------------------
print(f"\n--- Problem 4-4: Sum of EVEN digits of {number_digit} ---")
temp = number_digit
even_digit_sum = 0
while temp > 0:
    d = temp % 10
    if d % 2 == 0:
        even_digit_sum += d
    temp //= 10
print(f"  Even digit sum : {even_digit_sum}")       # Output: 2
# TIME COMPLEXITY: O(log₁₀ n)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PROBLEM 4-5: Factorial with iteration trace table
# ------------------------------------------------------------------
# FACTORIAL of n:  n! = n × (n-1) × ... × 1
# n=5: 5! = 5×4×3×2×1 = 120
#
# Trace table:
#   i  | factorial before | factorial after
#   1  |       1          |     1
#   2  |       1          |     2
#   3  |       2          |     6
#   4  |       6          |    24
#   5  |      24          |   120
# ------------------------------------------------------------------
n_factorial = 5
print(f"\n--- Problem 4-5: Factorial of {n_factorial} with trace ---")
factorial = 1
for i in range(1, n_factorial + 1):
    factorial_before = factorial
    factorial *= i
    print(f"  i={i} | before={factorial_before:4d} | after={factorial:4d}")
print(f"  {n_factorial}! = {factorial}")            # Output: 5! = 120
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PROBLEM 4-6: Pyramid of Stars
# ------------------------------------------------------------------
# Row i (1-indexed, 1..n): n-i spaces, then 2i-1 stars, then n-i spaces
# For n=5, row 3: 2 spaces · 5 stars · 2 spaces
#
# Pattern (n=5):
#     *
#    ***
#   *****
#  *******
# *********
#
# ANATOMY:
#   row i → (n-i) leading spaces + (2i-1) stars + (n-i) trailing spaces
# ------------------------------------------------------------------
n_pyramid = 5
print(f"\n--- Problem 4-6: Pyramid of Stars (n={n_pyramid}) ---")
for i in range(1, n_pyramid + 1):
    # Inner loop 1: leading spaces
    j = 1
    while j <= n_pyramid - i:
        print(" ", end=" ")
        j += 1
    # Inner loop 2: stars (2i-1 per row)
    j = 1
    while j <= 2 * i - 1:
        print("*", end=" ")
        j += 1
    # Inner loop 3: trailing spaces (same as leading)
    j = 1
    while j <= n_pyramid - i:
        print(" ", end=" ")
        j += 1
    print()
# Expected Output (n=5):
#         *
#        * * *
#       * * * * *
#      * * * * * * *
#     * * * * * * * * *
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)


# =============================================================================
# SECTION 5: DSA NOTEBOOK PROBLEMS
# =============================================================================

print("\n" + "="*65)
print("  SECTION 5 — DSA NOTEBOOK PROBLEMS")
print("="*65)

# ------------------------------------------------------------------
# DSA-1: Print First N Natural Numbers (Notebook 4)
# ------------------------------------------------------------------
# Given n, print 1, 2, ..., n
# APPROACH 1 — for loop (clean)
# APPROACH 2 — while loop (explicit)
# ------------------------------------------------------------------
n = 10
print(f"\n--- DSA-1: First {n} natural numbers ---")

# Approach 1 — for loop  O(n) / O(1)
print("  for loop  :", end=" ")
for i in range(1, n + 1):
    print(i, end=" ")           # Output: 1 2 3 4 5 6 7 8 9 10
print()

# Approach 2 — while loop  O(n) / O(1)
print("  while loop:", end=" ")
i = 1
while i > 0 and i <= n:
    print(i, end=" ")
    i += 1
print()
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# DSA-2: Print Even Numbers from 2 to N (Notebook 5)
# ------------------------------------------------------------------
# APPROACH 1 — while + if check
# APPROACH 2 — for loop with step=2 (optimal)
# ------------------------------------------------------------------
n = 10
print(f"\n--- DSA-2: Even numbers 2 to {n} ---")

# Approach 1 — while with modulo check  O(n) / O(1)
print("  while+if:", end=" ")
i = 2
while i <= n and i >= 2:
    if i % 2 == 0:
        print(i, end=" ")       # Output: 2 4 6 8 10
    i += 1
print()

# Approach 2 — step=2 (optimal) O(n/2) / O(1)
print("  step=2  :", end=" ")
for i in range(2, n + 1, 2):
    print(i, end=" ")           # Output: 2 4 6 8 10
print()
# TIME COMPLEXITY: O(n) Approach 1 / O(n/2) Approach 2
# SPACE COMPLEXITY: O(1) both

# ------------------------------------------------------------------
# DSA-3: Sum of First N Natural Numbers (Notebook 6)
# ------------------------------------------------------------------
# APPROACH 1 — for loop accumulator
# APPROACH 2 — while loop accumulator
# APPROACH 3 — Gauss formula O(1): n*(n+1)//2
# ------------------------------------------------------------------
n = 10
print(f"\n--- DSA-3: Sum of first {n} natural numbers ---")

# Approach 1 — for loop  O(n) / O(1)
sum_n_for = 0
for i in range(1, n + 1):
    sum_n_for += i
print(f"  for loop accumulator : {sum_n_for}")      # Output: 55

# Approach 2 — while loop  O(n) / O(1)
i = 1
sum_n_while = 0
while i > 0 and i <= n:
    sum_n_while += i
    i += 1
print(f"  while loop accumulator: {sum_n_while}")   # Output: 55

# Approach 3 — Gauss formula O(1) / O(1)
sum_n_gauss = n * (n + 1) // 2
print(f"  Gauss formula O(1)    : {sum_n_gauss}")   # Output: 55

# TIME COMPLEXITY: O(n) loops / O(1) Gauss
# SPACE COMPLEXITY: O(1) all

# ------------------------------------------------------------------
# DSA-4: Sum of N Given Numbers (Notebook 7)
# ------------------------------------------------------------------
# Given a list of n numbers, compute their sum.
# Hardcoded: n=5, lst=[10, 20, 30, 40, 50]  → sum=150
# Also: lst=[23, 43, 67, 86, 12]            → sum=231
# ------------------------------------------------------------------
n = 5
lst = [10, 20, 30, 40, 50]
print(f"\n--- DSA-4: Sum of n given numbers (n={n}, lst={lst}) ---")

# Approach 1 — index-based for loop  O(n) / O(1)
total_index = 0
for i in range(n):
    total_index += lst[i]
print(f"  Index loop: {total_index}")               # Output: 150

# Approach 2 — direct iteration  O(n) / O(1)
total_direct = 0
for val in lst:
    total_direct += val
print(f"  Direct iteration: {total_direct}")        # Output: 150

# Approach 3 — built-in sum()  O(n) / O(1)
print(f"  Built-in sum(): {sum(lst)}")              # Output: 150
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1) (excluding input storage)

# ------------------------------------------------------------------
# DSA-5: Print Arithmetic Series (Notebook 3)
# ------------------------------------------------------------------
# Given a, b, n: print [a+b, a+2b, a+3b, ..., a+nb]
# Hardcoded: a=10, b=12, n=4
# Expected: [22, 34, 46, 58]
# ------------------------------------------------------------------
a, b, n = 10, 12, 4
print(f"\n--- DSA-5: Arithmetic series a={a}, b={b}, n={n} ---")

# Approach 1 — list accumulator  O(n) / O(n)
series = []
for i in range(1, n + 1):
    series.append(a + b * i)
print(f"  List: {series}")                           # Output: [22, 34, 46, 58]

# Approach 2 — list comprehension  O(n) / O(n)
series_lc = [a + b * i for i in range(1, n + 1)]
print(f"  Comprehension: {series_lc}")               # Output: [22, 34, 46, 58]
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n)

# ------------------------------------------------------------------
# DSA-6: Check Prime Number (Notebook 8)
# ------------------------------------------------------------------
# A prime has no divisors from 2 to sqrt(n).
# for-else: else block runs only when no break occurred (no divisor found) → prime!
#
# APPROACH 1 (Brute force)     — O(n) — check all divisors up to n-1
# APPROACH 2 (Square root opt) — O(√n) — only check up to √n
#
# Trace for n=7 (prime):
#   sqrt(7) ≈ 2.65, range(2,3) = [2]
#   7 % 2 = 1 ≠ 0 → no break → else runs → PRIME ✓
#
# Trace for n=27 (not prime):
#   sqrt(27) ≈ 5.19, range(2,6) = [2,3,4,5]
#   27 % 2 = 1, 27 % 3 = 0 → break → NOT PRIME ✓
# ------------------------------------------------------------------
print(f"\n--- DSA-6: Prime Check ---")

def is_prime_brute(n):
    """Brute force O(n) prime check."""
    if n <= 1:
        return False
    for i in range(2, n):         # check all divisors
        if n % i == 0:
            return False
    return True

def is_prime_sqrt(n):
    """Optimal O(√n) prime check using for-else."""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False           # divisor found → not prime
    else:
        return True                # loop completed without break → prime

# Test hardcoded values
for test_num in [7, 27]:
    brute  = is_prime_brute(test_num)
    sqrt_r = is_prime_sqrt(test_num)
    print(f"  n={test_num:2d} | brute O(n)={str(brute):5s} | sqrt O(√n)={str(sqrt_r):5s}")
# Output:
#   n= 7 | brute O(n)=True  | sqrt O(√n)=True
#   n=27 | brute O(n)=False | sqrt O(√n)=False

# TIME COMPLEXITY: O(n) brute / O(√n) optimal
# SPACE COMPLEXITY: O(1) both

# Bonus: primes in range
lower_limit, upper_limit = 10, 30
primes_in_range = [x for x in range(lower_limit, upper_limit + 1) if is_prime_sqrt(x)]
print(f"  Primes in [{lower_limit},{upper_limit}]: {primes_in_range}")  # Output: [11, 13, 17, 19, 23, 29]

# ------------------------------------------------------------------
# DSA-7: Palindrome Check (Notebook 10)
# ------------------------------------------------------------------
# A string/number reads the same forward and backward.
# "121" reversed = "121" → PALINDROME
# "123" reversed = "321" → NOT palindrome
#
# APPROACH 1 — String slicing reversal  O(n) / O(n)
# APPROACH 2 — Loop-based (two pointers) O(n) / O(1)
# APPROACH 3 — Number reversal math     O(log₁₀ n) / O(1)
#
# Trace (number=121, math approach):
#   original=121, reversed=0
#   121 % 10 = 1  → reversed=1,  temp=12
#    12 % 10 = 2  → reversed=12, temp=1
#     1 % 10 = 1  → reversed=121, temp=0
#   reversed(121) == original(121) → PALINDROME ✓
# ------------------------------------------------------------------
number_palin = 121
s_palin = str(number_palin)
print(f"\n--- DSA-7: Palindrome Check (number={number_palin}) ---")

# Approach 1 — String slicing  O(n) / O(n)
def is_palindrome_slice(s):
    return s == s[::-1]

result = is_palindrome_slice(s_palin)
print(f"  String slicing [{s_palin}]: {result}")        # Output: True
print(f"  String slicing ['hello']: {is_palindrome_slice('hello')}")  # Output: False

# Approach 2 — Two pointers  O(n) / O(1)
def is_palindrome_two_ptr(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(f"  Two pointers   [{s_palin}]: {is_palindrome_two_ptr(s_palin)}")  # Output: True
print(f"  Two pointers   ['racecar']: {is_palindrome_two_ptr('racecar')}")# Output: True

# Approach 3 — Math (number reversal)  O(log₁₀ n) / O(1)
def is_palindrome_math(num):
    if num < 0:
        return False
    original = num
    reversed_num = 0
    temp = num
    while temp > 0:
        digit = temp % 10
        reversed_num = reversed_num * 10 + digit
        temp //= 10
    return original == reversed_num

print(f"  Math reversal  [{number_palin}]: {is_palindrome_math(number_palin)}")   # Output: True
print(f"  Math reversal  [123]: {is_palindrome_math(123)}")                       # Output: False

# TIME COMPLEXITY: O(n) / O(n) / O(log₁₀ n)
# SPACE COMPLEXITY: O(n) / O(1) / O(1)


# =============================================================================
# SECTION 6: NUMBER PATTERNS (from Notebooks 12.1–12.6)
# =============================================================================

print("\n" + "="*65)
print("  SECTION 6 — NUMBER PATTERNS")
print("="*65)

n_pyramid = 5   # All patterns use n=5

# ------------------------------------------------------------------
# PATTERN 6-1: Right-angled triangle of stars (Notebook 12.1)
# ------------------------------------------------------------------
# Row i (1..n): print i stars
#   *
#   * *
#   * * *
#   * * * *
#   * * * * *
# ------------------------------------------------------------------
print(f"\n--- Pattern 6-1: Right-angled star triangle (n={n_pyramid}) ---")

# Approach 1 — while loops  O(n²) / O(1)
i = 1
while i <= n_pyramid:
    j = 1
    while j <= i:
        print("*", end=" ")
        j += 1
    print()
    i += 1
print()

# Approach 2 — for loops  O(n²) / O(1)
for i in range(1, n_pyramid + 1):
    for j in range(1, i + 1):
        print("*", end=" ")
    print()

# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PATTERN 6-2: Counting triangle (Notebook 12.2)
# ------------------------------------------------------------------
# Row i: print 1, 2, ..., i
#   1
#   1 2
#   1 2 3
#   1 2 3 4
#   1 2 3 4 5
# ------------------------------------------------------------------
print(f"\n--- Pattern 6-2: Counting triangle (n={n_pyramid}) ---")
i = 1
while i <= n_pyramid:
    j = 1
    while j <= i:
        print(j, end=" ")
        j += 1
    print()
    i += 1
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PATTERN 6-3: Global counter triangle (Notebook 12.3)
# ------------------------------------------------------------------
# Numbers count globally across all rows:
#   1
#   2 3
#   4 5 6
#   7 8 9 10
#   11 12 13 14 15
# Key insight: num persists across outer iterations
# ------------------------------------------------------------------
print(f"\n--- Pattern 6-3: Global counter triangle (n={n_pyramid}) ---")
i = 1
num = 1
while i <= n_pyramid:
    j = 1
    while j <= i:
        print(num, end=" ")
        j += 1
        num += 1          # num continues from where it left off
    print()
    i += 1
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PATTERN 6-4: Alternating 0/1 triangle (Notebook 12.4)
# ------------------------------------------------------------------
# Row parity determines starting bit:
#   odd row  → starts with 1 (1, 0, 1, 0, ...)
#   even row → starts with 0 (0, 1, 0, 1, ...)
#
#   1
#   0 1
#   1 0 1
#   0 1 0 1
#   1 0 1 0 1
#
# Trick: num = 1 - num  toggles between 0 and 1.
#        Starting value: 1 if row is odd else 0
# ------------------------------------------------------------------
print(f"\n--- Pattern 6-4: Alternating 0/1 triangle (n={n_pyramid}) ---")
i = 1
while i <= n_pyramid:
    num = 0 if i % 2 == 0 else 1   # Pythonic ternary for starting value
    j = 1
    while j <= i:
        print(num, end=" ")
        num = 1 - num               # toggle  0↔1
        j += 1
    print()
    i += 1
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PATTERN 6-5: Right-aligned star triangle (Notebook 12.5)
# ------------------------------------------------------------------
# Row i: (n-i) spaces then i stars (right-aligned)
#         *
#       * *
#     * * *
#   * * * *
# * * * * *
# ------------------------------------------------------------------
print(f"\n--- Pattern 6-5: Right-aligned star triangle (n={n_pyramid}) ---")
for i in range(1, n_pyramid + 1):
    for _ in range(n_pyramid - i):    # leading spaces
        print(" ", end=" ")
    for _ in range(i):                # stars
        print("*", end=" ")
    print()
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PATTERN 6-6: Right-aligned number triangle (Notebook 12.6)
# ------------------------------------------------------------------
# Row i: (n-i) spaces, then i numbers starting from i
#           1
#         2 3
#       3 4 5
#     4 5 6 7
#   5 6 7 8 9
# ------------------------------------------------------------------
print(f"\n--- Pattern 6-6: Right-aligned number triangle (n={n_pyramid}) ---")
for i in range(1, n_pyramid + 1):
    for _ in range(n_pyramid - i):    # leading spaces
        print(" ", end=" ")
    num = i
    for _ in range(i):                # i numbers starting from i
        print(num, end=" ")
        num += 1
    print()
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)


# =============================================================================
# SECTION 7: CHARACTER PATTERNS (from Notebooks 13, 13.1–13.4)
# =============================================================================

print("\n" + "="*65)
print("  SECTION 7 — CHARACTER PATTERNS")
print("="*65)

# Key insight: characters are integers under the hood.
# chr(65) = 'A', ord('A') = 65, ord('Z') = 90, ord('z') = 122
# chr(ord(ch) + 1) advances to the next character in ASCII.
print("\n--- ASCII reminders ---")
print(f"  ord('A')={ord('A')}, chr(65)={chr(65)}")     # Output: 65, A
print(f"  ord('z')={ord('z')}, chr(122)={chr(122)}")   # Output: 122, z

n_char = 4  # all character patterns use n=4

# ------------------------------------------------------------------
# PATTERN 7-1: Decreasing alphabet triangle (Notebook 13.1)
# ------------------------------------------------------------------
# Row i: print (n-i+1) letters A, B, C, ...  (shrinking each row)
#   A B C D
#   A B C
#   A B
#   A
# ------------------------------------------------------------------
print(f"\n--- Pattern 7-1: Decreasing alphabet triangle (n={n_char}) ---")
for i in range(1, n_char + 1):
    ch = "A"
    for _ in range(n_char - i + 1):
        print(ch, end=" ")
        ch = chr(ord(ch) + 1)   # advance to next letter via ASCII
    print()
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PATTERN 7-2: Mirror alphabet triangle (Notebook 13.2)
# ------------------------------------------------------------------
# Row i: n-i+1 ascending letters, then same letters descending
#   A B C D E E D C B A
#   A B C D D C B A
#   A B C C B A
#   A B B A
#   A A
# Trick: step back one position (ch - 1) before the mirror loop.
# ------------------------------------------------------------------
print(f"\n--- Pattern 7-2: Mirror alphabet triangle (n={n_char}) ---")
for i in range(1, n_char + 1):
    ch = "A"
    for _ in range(n_char - i + 1):       # ascending half
        print(ch, end=" ")
        ch = chr(ord(ch) + 1)
    ch = chr(ord(ch) - 1)                  # step back (ch was over-incremented)
    for _ in range(n_char - i + 1):       # descending half
        print(ch, end=" ")
        ch = chr(ord(ch) - 1)
    print()
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PATTERN 7-3: Diamond of stars (ODD n) (Notebook 13.3)
# ------------------------------------------------------------------
# n must be ODD. We derive m = n - n//2 (ceiling half).
# n=9: m=5  → 5 rows ascending, 4 rows descending
#
#   *
#   * *
#   * * *
#   * * * *
#   * * * * *    ← peak
#   * * * *
#   * * *
#   * *
#   *
# ------------------------------------------------------------------
n_odd = 9   # must be odd
m = n_odd - n_odd // 2     # ceiling half = 5
print(f"\n--- Pattern 7-3: Diamond of stars (n={n_odd}, m={m}) ---")
# Upper half (ascending)
for i in range(1, m + 1):
    for _ in range(i):
        print("*", end=" ")
    print()
# Lower half (descending, m-1 rows)
for i in range(1, m):
    for _ in range(m - i):
        print("*", end=" ")
    print()
# TIME COMPLEXITY: O(n²) (O(m²) where m ≈ n/2)
# SPACE COMPLEXITY: O(1)

# ------------------------------------------------------------------
# PATTERN 7-4: Centered diamond (ODD n) (Notebook 13.4)
# ------------------------------------------------------------------
# Upper half row i: (m-i) spaces + (2i-1) stars
# Lower half row i: i spaces + (2*(m-i)-1) stars
#
#         *
#       * * *
#     * * * * *    ← peak
#       * * *
#         *
# ------------------------------------------------------------------
n_odd = 5
m = n_odd - n_odd // 2     # m=3
print(f"\n--- Pattern 7-4: Centered diamond (n={n_odd}, m={m}) ---")
# Upper half
for i in range(1, m + 1):
    for _ in range(m - i):
        print(" ", end=" ")
    for _ in range(2 * i - 1):
        print("*", end=" ")
    print()
# Lower half
for i in range(1, m):
    for _ in range(i):
        print(" ", end=" ")
    for _ in range(2 * (m - i) - 1):
        print("*", end=" ")
    print()
# TIME COMPLEXITY: O(n²) (O(m²) where m ≈ n/2)
# SPACE COMPLEXITY: O(1)


# =============================================================================
# SECTION 8: REAL-WORLD USE CASES
# =============================================================================

print("\n" + "="*65)
print("  SECTION 8 — REAL-WORLD USE CASES")
print("="*65)

# ------------------------------------------------------------------
# USE CASE 8-1: Rate Limiting with while loop
# ------------------------------------------------------------------
# while is ideal when you don't know ahead of time how many
# iterations you need — you stop when a condition is met.
# ------------------------------------------------------------------
print("\n--- Use Case 8-1: Rate Limiting (while) ---")
import time  # noqa: E402
MAX_REQUESTS = 5
RATE_LIMIT   = 10       # max requests allowed in window
requests_sent = 0

while requests_sent < MAX_REQUESTS:
    if requests_sent < RATE_LIMIT:
        print(f"  Request {requests_sent + 1} sent OK")    # Output: up to MAX_REQUESTS sent
        requests_sent += 1
    else:
        print("  Rate limit hit — waiting...")
        break                                               # would sleep in real code

# ------------------------------------------------------------------
# USE CASE 8-2: Pagination with for loop
# ------------------------------------------------------------------
# for is ideal when you know the iteration range (e.g., page 1 to N).
# ------------------------------------------------------------------
print("\n--- Use Case 8-2: Pagination (for) ---")
total_pages = 4
for page in range(1, total_pages + 1):
    items_on_page = [f"item_{(page-1)*3+j}" for j in range(1, 4)]
    print(f"  Page {page}: {items_on_page}")  # Output: Page 1: ['item_1', 'item_2', 'item_3'] ...

# ------------------------------------------------------------------
# USE CASE 8-3: Event Polling with while
# ------------------------------------------------------------------
# Polling: keep checking until an event occurs (hardcoded tick count).
# ------------------------------------------------------------------
print("\n--- Use Case 8-3: Event Polling (while) ---")
tick = 0
EVENT_AT_TICK = 3

while tick < 6:
    if tick == EVENT_AT_TICK:
        print(f"  Tick {tick}: EVENT RECEIVED — breaking")   # Output: at tick 3
        break
    print(f"  Tick {tick}: polling...")
    tick += 1


# =============================================================================
# SECTION 9: BIG O COMPLEXITY SUMMARY
# =============================================================================

print("\n" + "="*65)
print("  SECTION 9 — BIG O COMPLEXITY SUMMARY")
print("="*65)

print("""
  ┌──────────────────────────────────┬──────────────┬───────────────┐
  │  Pattern / Algorithm             │  Time        │  Space        │
  ├──────────────────────────────────┼──────────────┼───────────────┤
  │  Single while/for loop           │  O(n)        │  O(1)         │
  │  Single loop with step k         │  O(n/k)=O(n) │  O(1)         │
  │  Nested 2 loops                  │  O(n²)       │  O(1)         │
  │  Nested 3 loops                  │  O(n³)       │  O(1)         │
  │  Sum of naturals (Gauss)         │  O(1)        │  O(1)         │
  │  Sum of even (formula)           │  O(1)        │  O(1)         │
  │  Digit sum (math)                │  O(log n)    │  O(1)         │
  │  Digit sum (string)              │  O(d)        │  O(d)         │
  │  Prime check (brute)             │  O(n)        │  O(1)         │
  │  Prime check (sqrt)              │  O(√n)       │  O(1)         │
  │  Palindrome (slice)              │  O(n)        │  O(n)         │
  │  Palindrome (two pointers)       │  O(n)        │  O(1)         │
  │  Palindrome (math reversal)      │  O(log n)    │  O(1)         │
  │  All triangle patterns           │  O(n²)       │  O(1)         │
  │  Arithmetic series (list)        │  O(n)        │  O(n)         │
  └──────────────────────────────────┴──────────────┴───────────────┘
""")


# =============================================================================
# === PRACTICE ZONE ===
# =============================================================================
# Try these challenges. All must work WITHOUT modifying the test values.
#
# 1. WHILE LOOP: Print all numbers from 100 DOWN to 1.
#    (Hint: INIT i=100, CONDITION i>=1, UPDATE i-=1)
#
# 2. FOR LOOP: Print all multiples of 7 between 1 and 100.
#    (Hint: range(7, 101, 7))
#
# 3. NESTED LOOPS: Print an inverted right-angled star triangle for n=5:
#    * * * * *
#    * * * *
#    * * *
#    * *
#    *
#
# 4. DIGIT SUM: For number=456789, compute sum of digits two ways
#    (math and string) and verify they match.
#
# 5. PRIME RANGE: Using is_prime_sqrt(), print all primes from 1 to 50.
#
# 6. PALINDROME: Check if "racecar" and "python" are palindromes
#    using is_palindrome_two_ptr().
#
# 7. PATTERN: For n=5 print Floyd's triangle (row i has i numbers
#    starting from the global count, same as Pattern 6-3).
#
# 8. CHARACTER PATTERN: Print A to Z on separate lines using a for loop
#    and chr()/ord() — no hardcoded letters.
#
# 9. BUG HUNT: Fix this buggy nested loop so it prints a 4×4 grid:
#    j = 1
#    for i in range(4):
#        while j <= 4:
#            print("*", end=" ")
#            j += 1
#        print()
#
# 10. ADVANCED: Implement FizzBuzz from 1 to 30 using a while loop.
#     (Fizz for multiples of 3, Buzz for multiples of 5, FizzBuzz for both)
# =============================================================================
