###############################################################################
#                 03 - Pattern Printing and Pattern Problems                  #
###############################################################################
#
# Time:  O(n^2) for ALL triangle/pyramid/butterfly patterns
#        1 + 2 + 3 + ... + n = n*(n+1)/2 total characters printed = O(n^2)
#        You CANNOT beat this — you must print O(n^2) characters.
# Space: O(1) for nested loop versions (only loop variables)
#        O(n) transient for string-multiply versions ("* " * k creates a temp string)
#
# The universal row structure: [ spaces(i) ][ content_part_1 ][ content_part_2 ]
# Every pattern only varies WHAT goes in those parts and HOW MANY of each.

# =============================================================================
# SECTION 1: Star Triangles (One-liners with string multiply)
# =============================================================================
# "* " * k  →  "* * * "  (k stars, each followed by a space)
# This uses Python string multiplication as a shorthand for an inner loop.
# Limitation: ONLY works when every position prints the SAME character.
# When content varies per position (numbers, toggles), you MUST use inner loops.

def star_right_triangle(n: int):
    """
    *
    * *
    * * *
    Row i (1-indexed): 0 spaces + i stars
    """
    for i in range(1, n + 1):
        print("* " * i)           # string multiply: O(n) string creation per row

# Time: O(n^2) total, O(n) per row | Space: O(n) transient per row

def star_inverted_triangle(n: int):
    """
    * * * * *
    * * * *
    * * *
    Row i (0-indexed): 0 spaces + (n-i) stars
    """
    for i in range(n):
        print("* " * (n - i))

# Time: O(n^2) | Space: O(n) transient per row

def star_right_aligned_triangle(n: int):
    """
        *
      * *
    * * *
    Row i (0-indexed): (n-i-1) spaces + (i+1) stars
    Derivation:
      i=0: 4 spaces + 1 star    → n-0-1=4, 0+1=1
      i=1: 3 spaces + 2 stars   → n-1-1=3, 1+1=2
      i=4: 0 spaces + 5 stars   → n-4-1=0, 4+1=5
    """
    for i in range(n):
        print(" " * (n - i - 1) + "* " * (i + 1))

# Time: O(n^2) | Space: O(n) transient per row

def star_right_aligned_triangle_loops(n: int):
    """Same as above but using nested for loops — portable to any language."""
    for i in range(n):
        for _ in range(n - i - 1):    # spaces
            print(" ", end=" ")
        for _ in range(i + 1):        # stars
            print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1) — no temporary string objects

def star_right_aligned_inverted(n: int):
    """
    * * * * *
      * * * *
        * * *
          * *
            *
    Row i (0-indexed): i spaces + (n-i) stars
    """
    for i in range(n):
        print(" " * i + "* " * (n - i))

# Time: O(n^2) | Space: O(n) transient per row

def star_pyramid(n: int):
    """
        *
      * * *
    * * * * *
    Row i (1-indexed): (n-i) spaces + (2*i-1) stars
    Derivation of star count formula:
      Row 1: 1 star  = 2*1-1
      Row 2: 3 stars = 2*2-1
      Row 3: 5 stars = 2*3-1  →  always odd numbers (1, 3, 5, 7...)
    """
    for i in range(1, n + 1):
        for _ in range(n - i):        # leading spaces
            print(" ", end=" ")
        for _ in range(2 * i - 1):   # stars: formula 2i-1
            print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1)

def star_inverted_pyramid(n: int):
    """
    * * * * * * * * *
      * * * * * * *
        * * * * *
          * * *
            *
    Row i (0-indexed): i spaces + (2*(n-i)-1) stars
    """
    for i in range(n):
        for _ in range(i):                  # spaces grow as stars shrink
            print(" ", end=" ")
        for _ in range(2 * (n - i) - 1):   # stars formula
            print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 2: Number Triangle (print var RESETS each row)
# =============================================================================
#
# KEY CONCEPT: The print counter resets to 1 at the START of each row.
# Compare this directly to Pattern 2 (Continuous) where it does NOT reset.
#
# Row i prints: 1 2 3 ... i  (always starts from 1)
#
# Method 1 (for loop — j IS the value printed):
# Method 2 (while loop — j is loop control, n is print value separately):
#   This separation is IMPORTANT: when the printed value ≠ the loop variable,
#   you need a separate counter. Method 2 generalizes to all later patterns.

def number_triangle(n: int):
    """
    1
    1 2
    1 2 3
    1 2 3 4
    Method 1: j serves as both loop control AND the value to print.
    """
    for i in range(1, n + 1):       # row i
        for j in range(1, i + 1):   # j = 1, 2, ..., i
            print(j, end=" ")       # j IS the value printed
        print()

# Time: O(n^2) | Space: O(1)

def number_triangle_separate_counter(n: int):
    """
    Method 2: separate loop control (j) from print value (val).
    This is the generalized approach — essential for patterns where
    the printed value doesn't directly equal the loop variable.
    """
    i = 1
    while i <= n:
        j = 1
        val = 1             # val resets to 1 at the start of EACH row
        while j <= i:
            print(val, end=" ")
            j += 1
            val += 1        # val and j move in lockstep but are independent
        i += 1
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 3: Continuous Number Triangle (print var CARRIES FORWARD)
# =============================================================================
#
# KEY DIFFERENCE from Pattern 2:
#   - Pattern 2: num = 1 is INSIDE the outer loop → resets every row
#   - This pattern: num = 1 is OUTSIDE the outer loop → persists across rows
#
# Output:
#   1         ← row 1: num starts at 1, increments to 2
#   2 3       ← row 2: num starts at 2 (from where row 1 left off), increments to 4
#   4 5 6     ← row 3: num starts at 4, increments to 7
#   7 8 9 10  ← row 4: num starts at 7
#
# Detailed trace:
#   num=1 (set once before loop)
#   i=1: print num=1,  num→2
#   i=2: print num=2, num→3; print num=3, num→4
#   i=3: print num=4, num→5; print num=5, num→6; print num=6, num→7

def continuous_number_triangle(n: int):
    """
    1
    2 3
    4 5 6
    7 8 9 10
    """
    num = 1             # ← initialized ONCE, outside the outer loop
    for i in range(1, n + 1):
        for _ in range(i):
            print(num, end=" ")
            num += 1    # carries forward into the next row automatically
        print()

# Time: O(n^2) | Space: O(1)
# This is also known as Floyd's Triangle.


# =============================================================================
# SECTION 4: Binary Triangle (0/1 toggle with row-parity seed)
# =============================================================================
#
# Output:
#   1
#   0 1
#   1 0 1
#   0 1 0 1
#   1 0 1 0 1
#
# Two things to determine per row:
#   1) What does the row START with?
#      - Odd rows start with 1, even rows start with 0
#      - Formula: num = 0 if i % 2 == 0 else 1
#   2) How do values ALTERNATE within the row?
#      - After printing, flip: num = 1 - num
#      - 1 - 1 = 0,  1 - 0 = 1  →  bounces between 0 and 1
#
# The flip idiom: num = 1 - num
#   This is cleaner than if/else and is a standard competitive programming trick.
#   Think of it as a 2-state toggle: the two states are 0 and 1, and `1 - x`
#   maps each to the other.
#
# Walkthrough for row i=3 (odd):
#   num starts at 1
#   j=1: print 1, num = 1-1 = 0
#   j=2: print 0, num = 1-0 = 1
#   j=3: print 1, num = 1-1 = 0
#   Output: 1 0 1  ✓

def binary_triangle(n: int):
    """
    1
    0 1
    1 0 1
    0 1 0 1
    1 0 1 0 1
    """
    for i in range(1, n + 1):
        num = 0 if i % 2 == 0 else 1   # seed: even rows start 0, odd rows start 1
        for _ in range(i):
            print(num, end=" ")
            num = 1 - num               # flip the toggle: 0↔1
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 5: Right-Aligned Number Triangle (spaces + ascending start value)
# =============================================================================
#
# Output (n=5):
#         1
#       2 3
#     3 4 5
#   4 5 6 7
# 5 6 7 8 9
#
# Structure per row i:
#   Part 1: (n - i) spaces
#   Part 2: i numbers starting from i (ascending)
#
# Derivation of "starts from i":
#   Row 1: starts at 1 → prints 1
#   Row 2: starts at 2 → prints 2, 3
#   Row 3: starts at 3 → prints 3, 4, 5
#
# Note the print variable here CANNOT equal the loop variable j — they diverge.
# We need a SEPARATE `num` that initializes to `i` at the start of each row.

def right_aligned_number_triangle(n: int):
    """
            1
          2 3
        3 4 5
      4 5 6 7
    5 6 7 8 9
    """
    for i in range(1, n + 1):
        # Loop 1: leading spaces for right-alignment
        for _ in range(n - i):
            print(" ", end=" ")

        # Loop 2: i numbers starting from i
        num = i                     # num RESETS to i at the start of each row
        for _ in range(i):
            print(num, end=" ")
            num += 1                # increment within the row

        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 6: Number Mountain (ascending + descending with global state carry)
# =============================================================================
#
# Output (n=5):
#         1
#       2 3 2
#     3 4 5 4 3
#   4 5 6 7 6 5 4
# 5 6 7 8 9 8 7 6 5
#
# Structure per row i:
#   Part 1: (n - i) leading spaces
#   Part 2: i ascending numbers  (n += 1 BEFORE printing, i times)
#   Part 3: (i - 1) descending numbers  (n -= 1 BEFORE printing, i-1 times)
#
# CRITICAL: The counter `ctr` is initialized ONCE (= 0) before the outer loop
# and CARRIES FORWARD across all rows. It self-corrects between rows.
#
# Net change per row = (ascending adds i) - (descending subtracts i-1) = +1
# So ctr after row i = i. This means row i+1 starts with ctr = i, and the
# first ascending step makes ctr = i+1, which is exactly the first number
# of row i+1. The carry-forward is perfectly self-calibrating.
#
# Detailed trace (n=5):
#   ctr=0 initially
#
#   Row i=1: Ascending (1 time):  ctr 0→1, print 1
#            Descending (0 times): nothing
#            Output: "        1"   |  ctr ends at 1
#
#   Row i=2: Ascending (2 times): ctr 1→2 print 2, ctr 2→3 print 3
#            Descending (1 time): ctr 3→2 print 2
#            Output: "      2 3 2" |  ctr ends at 2
#
#   Row i=3: Ascending (3 times): ctr 2→3 print 3, →4 print 4, →5 print 5
#            Descending (2 times): ctr 5→4 print 4, →3 print 3
#            Output: "    3 4 5 4 3" |  ctr ends at 3
#
#   Row i=4: Ascending: ctr 3→4,5,6,7  →  print 4 5 6 7
#            Descending: ctr 7→6,5,4   →  print 6 5 4
#            Output: "  4 5 6 7 6 5 4"  |  ctr ends at 4
#
#   Row i=5: Ascending: ctr 4→5,6,7,8,9  →  print 5 6 7 8 9
#            Descending: ctr 9→8,7,6,5   →  print 8 7 6 5
#            Output: "5 6 7 8 9 8 7 6 5" |  ctr ends at 5

def number_mountain(n: int):
    """
            1
          2 3 2
        3 4 5 4 3
      4 5 6 7 6 5 4
    5 6 7 8 9 8 7 6 5
    """
    ctr = 0     # global counter, initialized ONCE, carries across all rows

    for i in range(1, n + 1):
        # Part 1: leading spaces
        for _ in range(n - i):
            print(" ", end=" ")

        # Part 2: ascending numbers (i times)
        # ctr is incremented BEFORE printing, so it steps up through each value
        for _ in range(i):
            ctr += 1
            print(ctr, end=" ")

        # Part 3: descending numbers (i - 1 times)
        # ctr is decremented BEFORE printing — first decrement undoes the peak
        # overshoot and brings us to peak-1, then peak-2, etc.
        for _ in range(i - 1):
            ctr -= 1
            print(ctr, end=" ")

        print()

# Time: O(n^2) | Space: O(1)
# The 3 inner loops are SEQUENTIAL (not nested), so each row is still O(n),
# and n rows × O(n) per row = O(n^2) total.


# =============================================================================
# SECTION 7: Butterfly Pattern (upper + lower halves)
# =============================================================================
#
# Upper half (n=5):
#   *                 *
#   * *             * *
#   * * *         * * *
#   * * * *     * * * *
#   * * * * * * * * * *
#
# Each row has THREE parts:
#   Left stars:   i stars
#   Middle gap:   2*(n-i) spaces
#   Right stars:  i stars
#
# Space count derivation:
#   Row 1: 1 left + 8 middle + 1 right  →  2*(5-1) = 8
#   Row 2: 2 left + 6 middle + 2 right  →  2*(5-2) = 6
#   Row 5: 5 left + 0 middle + 5 right  →  2*(5-5) = 0
#
# Lower half (n=5):
#   * * * * * * * * * *
#   * * * *     * * * *
#   * * *         * * *
#   * *             * *
#   *                 *
#
# Row i (0-indexed): (n-i) left + 2*i middle + (n-i) right

def butterfly_upper(n: int):
    """Upper half of the butterfly."""
    for i in range(1, n + 1):
        for _ in range(i):          # left stars
            print("*", end=" ")
        for _ in range(2 * (n - i)):  # middle gap
            print(" ", end=" ")
        for _ in range(i):          # right stars (mirror)
            print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1)

def butterfly_lower(n: int):
    """Lower half of the butterfly (inverted)."""
    for i in range(n):
        for _ in range(n - i):          # left stars (decreasing)
            print("*", end=" ")
        for _ in range(2 * i):          # middle gap (growing)
            print(" ", end=" ")
        for _ in range(n - i):          # right stars (mirror)
            print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1)

def butterfly_oneliner(n: int):
    """Compact versions using string multiplication."""
    print("-- Upper half --")
    for i in range(1, n + 1):
        print("* " * i + "  " * (2 * (n - i)) + "* " * i)

    print("-- Lower half --")
    for i in range(n):
        print("* " * (n - i) + "  " * (2 * i) + "* " * (n - i))

# Time: O(n^2) | Space: O(n) transient per row


# =============================================================================
# SECTION 8: Star Diamond (conditional branch in outer loop)
# =============================================================================
#
# Output (n=5, must be odd):
#   *
#   * *
#   * * *    ← peak: middle row = n//2 + 1
#   * *
#   *
#
# The outer loop runs ALL n rows. Inside:
#   - If i <= n//2: we're in the top half → print i stars
#   - Otherwise: we're in the bottom half → print (n-i+1) stars
#
# Derivation:
#   n=5, n//2 = 2
#   i=1: 1 <= 2? YES → print 1 star
#   i=2: 2 <= 2? YES → print 2 stars
#   i=3: 3 <= 2? NO  → print 5-3+1 = 3 stars  (peak)
#   i=4: 4 <= 2? NO  → print 5-4+1 = 2 stars
#   i=5: 5 <= 2? NO  → print 5-5+1 = 1 star
#
# "* " * k trick: Python string multiplication repeats the pattern.
# This collapses the inner loop to a single expression.

def star_diamond(n: int):
    """n must be a positive odd number for a symmetric diamond."""
    for i in range(1, n + 1):
        if i <= n // 2:
            print("* " * i)             # top half: stars increase
        else:
            print("* " * (n - i + 1))  # bottom half: stars decrease

# Time: O(n^2) total (O(n) per row from string multiply) | Space: O(n) transient


# =============================================================================
# COMPLEXITY SUMMARY TABLE
# =============================================================================
# Pattern                     | Time   | Space    | Inner loops
# ----------------------------|--------|----------|------------------
# Star triangles              | O(n^2) | O(1)/O(n)| 1-2 (loops/string)
# Star pyramid/inv. pyramid   | O(n^2) | O(1)     | 2 sequential
# Butterfly (upper+lower)     | O(n^2) | O(1)     | 3 sequential
# Number triangle (reset)     | O(n^2) | O(1)     | 1 + reset counter
# Continuous triangle         | O(n^2) | O(1)     | 1 + global counter
# Binary triangle             | O(n^2) | O(1)     | 1 + toggle var
# Right-aligned number        | O(n^2) | O(1)     | 2 (spaces + nums)
# Number mountain             | O(n^2) | O(1)     | 3 sequential
# Star diamond (str multiply) | O(n^2) | O(n)     | 1 (string expr)
#
# KEY: "3 sequential" means 3 inner loops that run ONE AFTER ANOTHER per row.
# They are NOT nested — total per row is still O(n), not O(n^2) or O(n^3).


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_number_triangle(n: int):
    """
    Print Pattern 1: Number Triangle that RESETS each row.
    1
    1 2
    1 2 3
    Hint: inner loop variable j IS the value to print.
    """
    pass

def practice_continuous_triangle(n: int):
    """
    Print Pattern 2: Continuous Number Triangle (carries forward).
    1
    2 3
    4 5 6
    Hint: initialize counter ONCE before the outer loop.
    """
    pass

def practice_binary_triangle(n: int):
    """
    Print Pattern 3: Binary Triangle (alternating 0s and 1s).
    1
    0 1
    1 0 1
    Hint: seed = 1 if odd row, 0 if even row. Then flip with num = 1 - num.
    """
    pass

def practice_right_aligned_numbers(n: int):
    """
    Print Pattern 4: Right-Aligned Number Triangle.
            1
          2 3
        3 4 5
    Hint: (n-i) spaces first, then i numbers starting from i.
    """
    pass

def practice_number_mountain(n: int):
    """
    Print Pattern 5: Number Mountain (ascending + descending per row).
            1
          2 3 2
        3 4 5 4 3
    Hint: single counter ctr=0 before outer loop.
          Ascending: ctr += 1 then print (i times).
          Descending: ctr -= 1 then print (i-1 times).
    """
    pass

def practice_diamond(n: int):
    """
    Print a full centered star diamond using pyramid + inverted pyramid.
      *
     ***
    *****
     ***
      *
    """
    pass


# =============================================================================
# SECTION 9: Countdown Triangle (Manmohan I) — descending per row
# =============================================================================
# Output (n=5):
#   1
#   2 1
#   3 2 1
#   4 3 2 1
#   5 4 3 2 1
#
# Row i: num starts at i, then decrements. i IS the starting value.
# Classic confusion: beginners set num=1 and increment — that gives Pattern 1,
# not this. You MUST set num=i at the start of each row.

def countdown_triangle(n: int):
    """Row i: prints i, i-1, i-2, ..., 1"""
    for i in range(1, n + 1):
        num = i                   # reset to i at the start of EACH row
        for _ in range(i):
            print(num, end=" ")
            num -= 1              # count DOWN each step
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 10: Number Ladder — row number repeated i times
# =============================================================================
# Output (n=5):
#   1
#   2 2
#   3 3 3
#   4 4 4 4
#   5 5 5 5 5
#
# Common mistake: printing j (which increments) instead of i (which stays fixed).
# The ONLY value printed in row i is i itself, repeated i times.
# This is NOT the same as printing 1, 2, 3, ... in each row.

def number_ladder(n: int):
    """Row i: prints the value i exactly i times."""
    for i in range(1, n + 1):
        for _ in range(i):
            print(i, end=" ")   # print i (the row number), NOT the inner loop variable
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 11: Fibonacci Pattern — row i shows first i Fibonacci numbers
# =============================================================================
# Output (n=5):
#   1
#   1 1
#   1 1 2
#   1 1 2 3
#   1 1 2 3 5
#
# Strategy:
#   1. Pre-generate the first n Fibonacci numbers into a list  → O(n) time, O(n) space
#   2. Row i: print fibs[0..i-1]
#
# This is the FIRST pattern that uses an array. The O(n) space is necessary
# because Fibonacci values depend on two previous values — you cannot
# regenerate cheaply mid-row without the stored list.

def fibonacci_pattern(n: int):
    """Row i: prints the first i Fibonacci numbers."""
    # Pre-compute first n Fibonacci numbers
    fibs = [0] * n
    if n >= 1:
        fibs[0] = 1
    if n >= 2:
        fibs[1] = 1
    for k in range(2, n):
        fibs[k] = fibs[k - 1] + fibs[k - 2]

    # Print triangle using pre-computed list
    for i in range(1, n + 1):
        for j in range(i):      # j = 0, 1, ..., i-1
            print(fibs[j], end=" ")
        print()

# Time: O(n^2) total (O(n) for pre-compute + O(n^2) to print) | Space: O(n)


# =============================================================================
# SECTION 12: Numbers & Stars Alternating — row-level if/else
# =============================================================================
# Output (n=5):
#   1
#   * *
#   1 2 3
#   * * * *
#   1 2 3 4 5
#
# Row i has i items. ODD rows print numbers 1..i. EVEN rows print i stars.
# The if/else goes OUTSIDE the inner loop — choose mode FIRST, then iterate.
# This is fundamentally different from toggling inside the inner loop.

def numbers_and_stars_alternating(n: int):
    """Odd rows: numbers. Even rows: stars. Each row has i items."""
    for i in range(1, n + 1):
        if i % 2 != 0:                # ODD row → numbers
            for j in range(1, i + 1):
                print(j, end=" ")
        else:                          # EVEN row → stars
            for _ in range(i):
                print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 13: Checkerboard (0s and 1s by coordinate parity)
# =============================================================================
# Output (n=5):
#   1 0 1 0 1
#   0 1 0 1 0
#   1 0 1 0 1
#   0 1 0 1 0
#   1 0 1 0 1
#
# KEY INSIGHT: (i + j) % 2 tells you parity of the sum of coordinates.
# Even sum → print 1.  Odd sum → print 0.
# Neighbours always differ (flipping i OR j by 1 changes parity) → checkerboard.
#
# This is a SQUARE pattern (n×n), not a triangle.

def checkerboard(n: int):
    """A square grid where cell (i,j) = 1 if (i+j) is even, else 0."""
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            print(1 if (i + j) % 2 == 0 else 0, end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 14: Palindrome Number Rows — ascend then descend within each row
# =============================================================================
# Output (n=5):
#   1
#   1 2 1
#   1 2 3 2 1
#   1 2 3 4 3 2 1
#   1 2 3 4 5 4 3 2 1
#
# Row i has 2i-1 numbers (same count as a pyramid of i stars).
# Structure: [1..i ascending] then [i-1..1 descending]
# The peak (i) is printed once — the right side starts from i-1, not i.

def palindrome_rows(n: int):
    """Row i: 1 2 ... i ... 2 1 (palindrome of length 2i-1)."""
    for i in range(1, n + 1):
        for j in range(1, i + 1):     # ascending: 1, 2, ..., i
            print(j, end=" ")
        for j in range(i - 1, 0, -1): # descending: i-1, i-2, ..., 1
            print(j, end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 15: Pattern Mountain (numbers peak at 1 in center) — valley pattern
# =============================================================================
# Output (n=5):
#         1
#       2 1 2
#     3 2 1 2 3
#   4 3 2 1 2 3 4
# 5 4 3 2 1 2 3 4 5
#
# CONTRAST with Number Mountain (Section 6):
#   Number Mountain: ascending values peak at the HIGH number in center
#   Pattern Mountain: counts DOWN to 1 at center, then back UP → peak is ALWAYS 1
#
# Row structure:
#   Part 1: (n-i) leading spaces
#   Part 2: count DOWN from i to 1  (left side)
#   Part 3: count UP from 2 to i    (right side — skip 1 already printed)

def pattern_mountain_valley(n: int):
    """Row i: i, i-1, ..., 1, ..., i-1, i (with 1 at the center peak)."""
    for i in range(1, n + 1):
        for _ in range(n - i):          # leading spaces
            print(" ", end=" ")
        for j in range(i, 0, -1):      # left: count DOWN to 1
            print(j, end=" ")
        for j in range(2, i + 1):      # right: count UP from 2 (skip center 1)
            print(j, end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 16: Filled Rhombus / Parallelogram — slant with constant stars
# =============================================================================
# Output (n=5):
#     * * * * *     ← 4 leading spaces
#    * * * * *      ← 3 leading spaces
#   * * * * *       ← 2 leading spaces
#  * * * * *        ← 1 leading space
# * * * * *         ← 0 leading spaces
#
# Every row has EXACTLY n stars. The only variable is the indent (leading spaces).
# Indent = n - i → shrinks by 1 each row → the shape tilts left = parallelogram.

def filled_rhombus(n: int):
    """A rectangle of stars tilted left (parallelogram). n stars per row."""
    for i in range(1, n + 1):
        for _ in range(n - i):    # leading spaces create the slant
            print(" ", end=" ")
        for _ in range(n):        # always n stars (constant)
            print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 17: Hollow Square — the canonical "hollow" technique
# =============================================================================
# Output (n=5):
#   * * * * *    ← top border: all stars
#   *       *    ← hollow row: only first and last
#   *       *
#   *       *
#   * * * * *    ← bottom border: all stars
#
# THE HOLLOW TECHNIQUE (applies to ALL hollow patterns):
#   - If it's a border row (first or last) → print all items normally.
#   - Otherwise → only print the FIRST and LAST item of the row.
#     Everything between is spaces.
#
# Code structure:
#   if i == 1 or i == n:        ← border: solid
#       print n stars
#   else:                       ← interior: hollow
#       print "*" + spaces + "*"

def hollow_square(n: int):
    """Square with filled border, hollow interior."""
    for i in range(1, n + 1):
        if i == 1 or i == n:           # top/bottom border → all stars
            for _ in range(n):
                print("*", end=" ")
        else:                           # interior rows → hollow
            print("*", end=" ")         # left border
            for _ in range(n - 2):
                print(" ", end=" ")     # hollow interior
            print("*", end=" ")         # right border
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 18: Hourglass — wide top, narrow to 1, wide again (2n-1 rows)
# =============================================================================
# Output (n=5):  [total rows = 2n-1 = 9]
#   * * * * * * * * *    ← row 1: widest (2n-1 = 9 stars, 0 spaces)
#     * * * * * * *      ← row 2: shrinks by 1 star each side
#       * * * * *
#         * * *
#           *            ← row n: narrowest (1 star, n-1 spaces)
#         * * *          ← row n+1: growing again
#       * * * * *
#     * * * * * * *
#   * * * * * * * * *    ← row 2n-1: widest again
#
# The 2n-1 row structure:
#   Upper half (rows 1..n):    stars = 2*(n-i)+1,  spaces = i-1
#   Lower half (rows n+1..2n-1): let k = i-n,
#                                stars = 2*k+1,     spaces = n-k-1
#
# Why 2n-1? The tip (1 star) is the midpoint. n rows above + n-1 rows below = 2n-1.

def hourglass(n: int):
    """Sand timer: wide at top, narrow at center, wide at bottom."""
    # Upper half: rows 1..n (stars shrink)
    for i in range(1, n + 1):
        stars  = 2 * (n - i) + 1   # 2n-1, 2n-3, ..., 1
        spaces = i - 1              # 0, 1, ..., n-1
        for _ in range(spaces):
            print(" ", end=" ")
        for _ in range(stars):
            print("*", end=" ")
        print()

    # Lower half: rows n+1..2n-1 (stars grow)
    for i in range(n + 1, 2 * n):
        k      = i - n              # k = 1, 2, ..., n-1
        stars  = 2 * k + 1         # 3, 5, ..., 2n-1
        spaces = n - k - 1         # n-2, n-3, ..., 0
        for _ in range(spaces):
            print(" ", end=" ")
        for _ in range(stars):
            print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 19: Inverted Hourglass / Full Star Diamond — 2n-1 rows, narrow to wide
# =============================================================================
# Output (n=5):  [total rows = 2n-1 = 9]
#           *            ← row 1: narrowest (1 star, n-1 spaces)
#         * * *
#       * * * * *
#     * * * * * * *
#   * * * * * * * * *    ← row n: widest (2n-1 stars, 0 spaces)
#     * * * * * * *      ← starts shrinking
#       * * * * *
#         * * *
#           *            ← row 2n-1: narrowest again
#
# This is the INVERSE of the Hourglass.
# Upper half: rows 1..n → stars grow,   spaces shrink
# Lower half: rows n+1..2n-1 → stars shrink, spaces grow
#
# Upper formula:   stars = 2i-1,  spaces = n-i
# Lower formula:   let k = 2n-i,  stars = 2k-1,  spaces = n-k

def inverted_hourglass(n: int):
    """Narrow at top/bottom, wide at center — full star diamond."""
    # Upper half: rows 1..n (stars grow)
    for i in range(1, n + 1):
        stars  = 2 * i - 1         # 1, 3, 5, ..., 2n-1
        spaces = n - i             # n-1, n-2, ..., 0
        for _ in range(spaces):
            print(" ", end=" ")
        for _ in range(stars):
            print("*", end=" ")
        print()

    # Lower half: rows n+1..2n-1 (stars shrink)
    for i in range(n + 1, 2 * n):
        k      = 2 * n - i         # k = n-1, n-2, ..., 1
        stars  = 2 * k - 1         # 2n-3, ..., 1
        spaces = n - k             # 1, 2, ..., n-1
        for _ in range(spaces):
            print(" ", end=" ")
        for _ in range(stars):
            print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 20: Double-Sided Arrow — left-aligned diamond (no centering)
# =============================================================================
# Output (n=5):  [total rows = 2n-1 = 9]
#   *
#   * *
#   * * *
#   * * * *
#   * * * * *    ← widest
#   * * * *
#   * * *
#   * *
#   *
#
# CONTRAST with Inverted Hourglass (Section 19):
#   Pattern 19 is CENTERED (leading spaces create the centered diamond shape)
#   Pattern 20 is LEFT-ALIGNED (no leading spaces — looks like a ↕ arrow)
# The star count formula is identical; only the alignment differs.

def double_sided_arrow(n: int):
    """Left-aligned diamond — two triangles base-to-base."""
    for i in range(1, n + 1):          # upper half: 1 → n stars
        for _ in range(i):
            print("*", end=" ")
        print()
    for i in range(n - 1, 0, -1):     # lower half: n-1 → 1 stars
        for _ in range(i):
            print("*", end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 21: Hollow Rhombus — hollow technique on a slanted rectangle
# =============================================================================
# Output (n=5):
#     * * * * *    ← row 1: (n-1) spaces + all n stars (solid border)
#    *       *     ← row 2: (n-2) spaces + hollow row
#   *       *
#  *       *
# * * * * * * * * * ← row n: 0 spaces + all stars (solid border) [note: wider due to spacing]
#
# This combines TWO techniques:
#   1. Slant via leading spaces: spaces = n - i (same as filled rhombus)
#   2. Hollow interior: only print border stars in middle rows

def hollow_rhombus(n: int):
    """Slanted rectangle with hollow interior (border only)."""
    for i in range(1, n + 1):
        for _ in range(n - i):         # slant spaces
            print(" ", end=" ")
        if i == 1 or i == n:           # top/bottom border → solid
            for _ in range(n):
                print("*", end=" ")
        else:                           # interior → hollow
            print("*", end=" ")         # left border star
            for _ in range(n - 2):
                print(" ", end=" ")     # hollow gap
            print("*", end=" ")         # right border star
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 22: Hollow Diamond — hollow technique on a full 2n-1 diamond
# =============================================================================
# Output (n=5):  [total rows = 2n-1 = 9]
#           *            ← only 1 star (first = last, special case)
#         *   *
#       *       *
#     *           *
#   *               *    ← widest row: 1 star, 2n-3 spaces, 1 star
#     *           *
#       *       *
#         *   *
#           *
#
# Built on Inverted Hourglass (Section 19) but made hollow:
#   - Same leading spaces and total-star count per row
#   - Instead of filling all stars: only print FIRST and LAST star
#   - Special case: when filled_stars == 1, print just one star

def _hollow_diamond_row(i: int, n: int):
    """Print one row of the hollow diamond."""
    if i <= n:
        filled_stars = 2 * i - 1
        spaces_lead  = n - i
    else:
        k            = 2 * n - i
        filled_stars = 2 * k - 1
        spaces_lead  = n - k

    for _ in range(spaces_lead):
        print(" ", end=" ")

    if filled_stars == 1:              # tip: only one star
        print("*", end=" ")
    else:
        print("*", end=" ")            # left border star
        for _ in range(filled_stars - 2):
            print(" ", end=" ")        # hollow interior
        print("*", end=" ")            # right border star

    print()

def hollow_diamond(n: int):
    """Centered diamond outline only (no fill)."""
    for i in range(1, 2 * n):         # rows 1 to 2n-1
        _hollow_diamond_row(i, n)

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 23: Alphabet Triangle — first use of chr() in patterns
# =============================================================================
# Output (n=5):
#   A
#   B B
#   C C C
#   D D D D
#   E E E E E
#
# chr(65) = 'A', chr(66) = 'B', chr(67) = 'C', ...
# General formula: chr(64 + i) gives the i-th letter (1-indexed)
# This pattern is the Number Ladder (Section 10) but with letters instead of numbers.

def alphabet_triangle(n: int):
    """Row i: print the i-th letter of the alphabet, i times."""
    for i in range(1, n + 1):
        ch = chr(64 + i)              # 64 + 1 = 65 = 'A', 64 + 2 = 66 = 'B', ...
        for _ in range(i):
            print(ch, end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# SECTION 24: Spiral-Border Square — the most elegant formula in patterns
# =============================================================================
# Output (n=5):
#   1 1 1 1 1
#   1 2 2 2 1
#   1 2 3 2 1
#   1 2 2 2 1
#   1 1 1 1 1
#
# Formula for cell (i, j):  val = min(i, j, n-i+1, n-j+1)
#
# WHY this works:
#   min(i, j, n-i+1, n-j+1) = the MINIMUM distance from any of the 4 edges + 0
#   - i         = distance from top edge (rows counted from 1)
#   - n-i+1     = distance from bottom edge
#   - j         = distance from left edge
#   - n-j+1     = distance from right edge
#   The minimum of these 4 values = which "shell" the cell is in.
#   Shell 1 = outermost border, shell 2 = next ring, etc.
#
# This is a 2D coordinate problem — no inner loops over i alone, just compute per cell.

def spiral_border_square(n: int):
    """Each cell shows which concentric border layer it belongs to."""
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            val = min(i, j, n - i + 1, n - j + 1)
            print(val, end=" ")
        print()

# Time: O(n^2) | Space: O(1)


# =============================================================================
# PRACTICE SKELETONS (TIER 2 — from 13_pattern_problems.py)
# =============================================================================

def practice_countdown_triangle(n: int):
    """
    Row i prints: i, i-1, i-2, ..., 1
    5
    4 3 2 1
    Hint: set num = i at the start of each row, decrement inside.
    """
    pass

def practice_checkerboard(n: int):
    """
    1 0 1 0 1
    0 1 0 1 0
    Hint: print 1 if (i+j) % 2 == 0, else 0.
    """
    pass

def practice_hollow_square(n: int):
    """
    * * * * *
    *       *
    *       *
    * * * * *
    Hint: if i==1 or i==n: all stars. Else: star + spaces + star.
    """
    pass

def practice_hourglass(n: int):
    """
    * * * * * * * * *
          *
    * * * * * * * * *
    Hint: upper half stars = 2*(n-i)+1, spaces = i-1.
          Lower: k=i-n, stars=2k+1, spaces=n-k-1.
    """
    pass

def practice_hollow_diamond(n: int):
    """
    Hollow centered diamond over 2n-1 rows.
        *
      *   *
    *       *
      *   *
        *
    Hint: filled_stars = 2i-1 (upper) or 2k-1 (lower).
          If stars==1: print one star. Else: star + spaces + star.
    """
    pass

def practice_spiral_border(n: int):
    """
    1 1 1 1 1
    1 2 2 2 1
    1 2 3 2 1
    Formula: min(i, j, n-i+1, n-j+1)
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    SEP = "=" * 50
    n = 5

    # --- Sections 1-8 (original) ---

    print(f"\n{SEP}")
    print("1a. Right Triangle (incr)")
    print(SEP)
    star_right_triangle(n)

    print(f"\n{SEP}")
    print("1b. Right Triangle (decr)")
    print(SEP)
    star_inverted_triangle(n)

    print(f"\n{SEP}")
    print("1c. Right-Aligned Triangle (string multiply)")
    print(SEP)
    star_right_aligned_triangle(n)

    print(f"\n{SEP}")
    print("1d. Right-Aligned Triangle (nested loops)")
    print(SEP)
    star_right_aligned_triangle_loops(n)

    print(f"\n{SEP}")
    print("1e. Right-Aligned Inverted Triangle")
    print(SEP)
    star_right_aligned_inverted(n)

    print(f"\n{SEP}")
    print("1f. Pyramid")
    print(SEP)
    star_pyramid(n)

    print(f"\n{SEP}")
    print("1g. Inverted Pyramid")
    print(SEP)
    star_inverted_pyramid(n)

    print(f"\n{SEP}")
    print("2. Number Triangle (RESETS each row)")
    print(SEP)
    number_triangle(n)

    print(f"\n{SEP}")
    print("2b. Number Triangle (separate counter)")
    print(SEP)
    number_triangle_separate_counter(n)

    print(f"\n{SEP}")
    print("3. Continuous Number Triangle (CARRIES FORWARD)")
    print(SEP)
    continuous_number_triangle(n)

    print(f"\n{SEP}")
    print("4. Binary Triangle (0/1 toggle)")
    print(SEP)
    binary_triangle(n)

    print(f"\n{SEP}")
    print("5. Right-Aligned Number Triangle")
    print(SEP)
    right_aligned_number_triangle(n)

    print(f"\n{SEP}")
    print("6. Number Mountain (ascending + descending with carry)")
    print(SEP)
    number_mountain(n)

    print(f"\n{SEP}")
    print("7a. Butterfly upper + lower (loops)")
    print(SEP)
    butterfly_upper(n)
    butterfly_lower(n)

    print(f"\n{SEP}")
    print("7b. Butterfly (one-liners)")
    print(SEP)
    butterfly_oneliner(n)

    print(f"\n{SEP}")
    print("8. Star Diamond (string multiply, n must be odd)")
    print(SEP)
    star_diamond(5)

    # --- Sections 9-24 (new) ---

    print(f"\n{SEP}")
    print("9. Countdown Triangle (Manmohan I)")
    print(SEP)
    countdown_triangle(n)

    print(f"\n{SEP}")
    print("10. Number Ladder (row number repeated)")
    print(SEP)
    number_ladder(n)

    print(f"\n{SEP}")
    print("11. Fibonacci Pattern")
    print(SEP)
    fibonacci_pattern(n)

    print(f"\n{SEP}")
    print("12. Numbers & Stars Alternating")
    print(SEP)
    numbers_and_stars_alternating(n)

    print(f"\n{SEP}")
    print("13. Checkerboard (coordinate parity)")
    print(SEP)
    checkerboard(n)

    print(f"\n{SEP}")
    print("14. Palindrome Number Rows")
    print(SEP)
    palindrome_rows(n)

    print(f"\n{SEP}")
    print("15. Pattern Mountain Valley (peak=1 at center)")
    print(SEP)
    pattern_mountain_valley(n)

    print(f"\n{SEP}")
    print("16. Filled Rhombus / Parallelogram")
    print(SEP)
    filled_rhombus(n)

    print(f"\n{SEP}")
    print("17. Hollow Square")
    print(SEP)
    hollow_square(n)

    print(f"\n{SEP}")
    print("18. Hourglass (2n-1 rows)")
    print(SEP)
    hourglass(n)

    print(f"\n{SEP}")
    print("19. Inverted Hourglass / Full Star Diamond (2n-1 rows)")
    print(SEP)
    inverted_hourglass(n)

    print(f"\n{SEP}")
    print("20. Double-Sided Arrow (left-aligned diamond)")
    print(SEP)
    double_sided_arrow(n)

    print(f"\n{SEP}")
    print("21. Hollow Rhombus")
    print(SEP)
    hollow_rhombus(n)

    print(f"\n{SEP}")
    print("22. Hollow Diamond (2n-1 rows)")
    print(SEP)
    hollow_diamond(n)

    print(f"\n{SEP}")
    print("23. Alphabet Triangle")
    print(SEP)
    alphabet_triangle(n)

    print(f"\n{SEP}")
    print("24. Spiral-Border Square")
    print(SEP)
    spiral_border_square(n)

    # --- Original Practice Skeletons ---
    print(f"\n{SEP}")
    print("PRACTICE SKELETONS (Tier 1)")
    print(SEP)
    practice_number_triangle(4)
    practice_continuous_triangle(4)
    practice_binary_triangle(4)
    practice_right_aligned_numbers(4)
    practice_number_mountain(4)
    practice_diamond(5)

    # --- New Practice Skeletons ---
    print(f"\n{SEP}")
    print("PRACTICE SKELETONS (Tier 2)")
    print(SEP)
    practice_countdown_triangle(4)
    practice_checkerboard(4)
    practice_hollow_square(4)
    practice_hourglass(4)
    practice_hollow_diamond(4)
    practice_spiral_border(4)
