###############################################################################
#       13 - Pattern Problems: 20 Competitive Programming Challenges          #
###############################################################################
#
# All 20 patterns from your practice list, ordered from simplest to hardest.
# Each pattern includes:
#   - Exact visual output for n=5
#   - The mental model (how to THINK about it)
#   - Row-by-row breakdown with the key formula
#   - Clean solution code
#   - Notes on where beginners get stuck
#
# ─── HOW TO CRACK ANY PATTERN PROBLEM ────────────────────────────────────────
#
#  Step 1:  DRAW it for n=4 or n=5 on paper.
#           (you can't code what you can't see)
#
#  Step 2:  Count the ROWS.
#           - n rows? 2n-1 rows? Something else?
#
#  Step 3:  For EACH row i (1-indexed), break the row into PARTS:
#           - Leading spaces (for alignment)
#           - Left content  (stars, numbers)
#           - Right content (sometimes a mirror of left)
#
#  Step 4:  Find the FORMULA for each part using i and n:
#
#  Common formulas ─────────────────────────────────────────────────────────────
#
#   Part                    │ Formula (row i, size n)
#   ────────────────────────┼─────────────────────────────────────────────────
#   Stars in right triangle │ i
#   Stars in inverted tri.  │ n - i + 1
#   Stars in pyramid (odd)  │ 2*i - 1
#   Leading spaces (pyramid)│ n - i
#   Stars in diamond top    │ 2*i - 1 (i = 1..n)
#   Stars in diamond bottom │ 2*(n-i+1) - 1 (i = n+1..2n-1)
#   Hollow: print star only │ when j == 1 OR j == count (first/last column)
#
#  Step 5:  Write the loops:
#           Outer loop → rows (i from 1 to num_rows)
#           Inner loops → one per PART in each row
#
# ─── TIME & SPACE (applies to ALL patterns below) ────────────────────────────
#
#   Time:  O(n²)  — n rows × O(n) work per row
#   Space: O(1)   — only loop variables; no arrays; printing directly
#
# ─── THE TWO BIG TRICKS ──────────────────────────────────────────────────────
#
#   1. Spaces ARE content.
#      When printing with end=" ", a space takes the same width as a star.
#      `print(" ", end=" ")` → "  " (2 chars)
#      `print("*", end=" ")` → "* " (2 chars)
#      They line up perfectly. Treat spaces as invisible stars.
#
#   2. Hollow = only print first & last item in the row.
#      Instead of a loop printing every item, check: if j == 1 or j == count
#      print "*", else print " ".
#
###############################################################################

n = 5   # change this to test any pattern below


# =============================================================================
# ──────────────── TIER 1: FOUNDATIONS (Easy) ─────────────────────────────────
# =============================================================================

# =============================================================================
# PATTERN 01: Square Pattern
# =============================================================================
#
# Output (n=5):
#   * * * * *
#   * * * * *
#   * * * * *
#   * * * * *
#   * * * * *
#
# Mental Model:
#   n rows, n stars per row. Nothing changes between rows.
#   The simplest possible pattern — just two loops both running n times.
#
# Formula:
#   Row i → always print n stars.
#
# Common mistake:
#   Making the inner loop depend on i (that would give a triangle, not a square).
#   Both loops must run exactly n times independently.

def square_pattern(n):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            print("*", end=" ")
        print()

print("=== Pattern 01: Square Pattern ===")
square_pattern(n)


# =============================================================================
# PATTERN 02: Half Pyramid Pattern
# =============================================================================
#
# Output (n=5):
#   *
#   * *
#   * * *
#   * * * *
#   * * * * *
#
# Mental Model:
#   The "base" pattern — every other triangle/pyramid is a variation of this.
#   Row i has exactly i stars.
#   The outer loop variable (i) IS the number of stars in that row.
#
# Formula:
#   Row i → print i stars
#
# Breakdown:
#   i=1: 1 star     i=2: 2 stars   i=3: 3 stars   i=4: 4   i=5: 5
#
# Insight:
#   When inner loop runs "for j in range(1, i+1)", it runs i times.
#   i is both the row number AND the star count. That's the elegance here.

def half_pyramid(n):
    for i in range(1, n + 1):
        for j in range(1, i + 1):    # j runs from 1 to i → i iterations
            print("*", end=" ")
        print()

print("\n=== Pattern 02: Half Pyramid Pattern ===")
half_pyramid(n)


# =============================================================================
# PATTERN 03: Downward Triangle Pattern
# =============================================================================
#
# Output (n=5):
#   * * * * *
#   * * * *
#   * * *
#   * *
#   *
#
# Mental Model:
#   The inverse of Half Pyramid. Row i has (n - i + 1) stars.
#   Row 1 starts full (n stars), row n ends with 1 star.
#
# Formula:
#   Row i → print (n - i + 1) stars
#
# Visual derivation:
#   i=1: n-1+1 = n = 5 stars
#   i=2: n-2+1 = 4 stars
#   i=3: n-3+1 = 3 stars
#   i=4: n-4+1 = 2 stars
#   i=5: n-5+1 = 1 star
#
# Easy check: at i=1, formula gives n (full row). At i=n, formula gives 1. ✓

def downward_triangle(n):
    for i in range(1, n + 1):
        for j in range(1, n - i + 2):    # n-i+1 stars per row
            print("*", end=" ")
        print()

print("\n=== Pattern 03: Downward Triangle Pattern ===")
downward_triangle(n)


# =============================================================================
# PATTERN 04: Manmohan Loves Patterns - I
# =============================================================================
#
# Output (n=5):
#   1
#   2 1
#   3 2 1
#   4 3 2 1
#   5 4 3 2 1
#
# Mental Model:
#   Same shape as Half Pyramid (row i has i items),
#   but instead of printing stars, we print numbers COUNTING DOWN from i to 1.
#
# Formula:
#   Row i → start num at i, print num, then num-1, num-2, ..., 1
#
# Breakdown:
#   Row 1: num starts at 1 → print: 1
#   Row 2: num starts at 2 → print: 2, 1
#   Row 3: num starts at 3 → print: 3, 2, 1
#   Row i: num starts at i → print: i, i-1, i-2, ..., 1
#
# Key insight:
#   Set num = i at the start of each row, then decrement inside the inner loop.
#   The inner loop runs i times, so num goes from i down to 1.

def manmohan_pattern_1(n):
    for i in range(1, n + 1):
        num = i                       # start of each row = row number
        for j in range(1, i + 1):
            print(num, end=" ")
            num -= 1                  # count down each step
        print()

print("\n=== Pattern 04: Manmohan Loves Patterns - I ===")
manmohan_pattern_1(n)


# =============================================================================
# PATTERN 05: Fibonacci Pattern (Pattern 4)
# =============================================================================
#
# Output (n=5):
#   1
#   1 1
#   1 1 2
#   1 1 2 3
#   1 1 2 3 5
#
# ─── What is Fibonacci? ───────────────────────────────────────────────────────
#
#   The Fibonacci sequence: each number = sum of the two before it.
#   Starting values: F(1)=1, F(2)=1, then F(k) = F(k-1) + F(k-2)
#
#   Position:   1   2   3   4   5   6   7    8    9 ...
#   Value:      1   1   2   3   5   8  13   21   34 ...
#               ↑   ↑   ↑
#              1+0 1+0 1+1
#
#   Why does it appear in nature? Fibonacci numbers describe branching patterns
#   in trees, spiral shells, sunflower seeds, and pinecone scales.
#
# ─────────────────────────────────────────────────────────────────────────────
#
# Mental Model:
#   Row i shows the FIRST i Fibonacci numbers.
#   Row 1 → just 1 number.  Row 2 → first 2.  Row n → first n.
#
# Strategy:
#   1. Pre-generate the first n Fibonacci numbers into a list.
#   2. Row i: slice and print fibs[0 .. i-1].
#
# Breakdown (n=5):
#   fibs = [1, 1, 2, 3, 5]
#   Row 1: fibs[0]               → 1
#   Row 2: fibs[0..1]            → 1 1
#   Row 3: fibs[0..2]            → 1 1 2
#   Row 4: fibs[0..3]            → 1 1 2 3
#   Row 5: fibs[0..4]            → 1 1 2 3 5

def fibonacci_pattern(n):
    # Step 1: generate first n Fibonacci numbers
    fibs = [0] * n
    if n >= 1:
        fibs[0] = 1
    if n >= 2:
        fibs[1] = 1
    for k in range(2, n):
        fibs[k] = fibs[k - 1] + fibs[k - 2]

    # Step 2: row i → print first i fibs
    for i in range(1, n + 1):
        for j in range(i):            # j runs 0, 1, ..., i-1
            print(fibs[j], end=" ")
        print()

print("\n=== Pattern 05: Fibonacci Pattern ===")
fibonacci_pattern(n)


# =============================================================================
# PATTERN 06: Pattern Numbers & Stars - 1
# =============================================================================
#
# Output (n=5):
#   1
#   * *
#   1 2 3
#   * * * *
#   1 2 3 4 5
#
# Mental Model:
#   Odd rows (1, 3, 5, ...) → print numbers 1, 2, ..., i
#   Even rows (2, 4, 6, ...) → print i stars
#   Both cases: row i has exactly i items.
#
# Formula:
#   if i % 2 != 0 → print numbers
#   if i % 2 == 0 → print stars
#
# Breakdown:
#   i=1 (odd):  1             → numbers 1..1
#   i=2 (even): * *           → 2 stars
#   i=3 (odd):  1 2 3         → numbers 1..3
#   i=4 (even): * * * *       → 4 stars
#   i=5 (odd):  1 2 3 4 5     → numbers 1..5
#
# Key trick:
#   The if/else goes OUTSIDE the inner loop.
#   Choose what to print first, then run the inner loop.

def numbers_and_stars_1(n):
    for i in range(1, n + 1):
        if i % 2 != 0:                # ODD row → numbers
            for j in range(1, i + 1):
                print(j, end=" ")
        else:                         # EVEN row → stars
            for j in range(1, i + 1):
                print("*", end=" ")
        print()

print("\n=== Pattern 06: Pattern Numbers & Stars - 1 ===")
numbers_and_stars_1(n)


# =============================================================================
# ──────────────── TIER 2: INTRODUCING ALIGNMENT (Easy-Medium) ────────────────
# =============================================================================

# =============================================================================
# PATTERN 07: Pattern Triangle (Isoceles / Centered Triangle)
# =============================================================================
#
# Output (n=5):
#           *
#         * * *
#       * * * * *
#     * * * * * * *
#   * * * * * * * * *
#
# Mental Model:
#   Centered / isoceles triangle. Each row has two parts:
#   PART 1 → leading spaces to push the stars to the center
#   PART 2 → an ODD number of stars (1, 3, 5, 7, 9, ...)
#
# Why ODD stars?
#   Each row, we add ONE star on the LEFT and ONE on the RIGHT.
#   Start with 1. Then +2 = 3. Then +2 = 5. Odd numbers only.
#   Row i → 2*i - 1 stars.
#
# Space formula:
#   We want the triangle centered. Row 1 has the most spaces.
#   Row i → (n - i) leading spaces.
#   At i=1: n-1 spaces. At i=n: 0 spaces (full base, no indent).
#
# Breakdown (n=5):
#   i=1: 4 spaces,  1 star   → "        *"
#   i=2: 3 spaces,  3 stars  → "      * * *"
#   i=3: 2 spaces,  5 stars  → "    * * * * *"
#   i=4: 1 space,   7 stars  → "  * * * * * * *"
#   i=5: 0 spaces,  9 stars  → "* * * * * * * * *"
#
# ─── "Space is invisible content" ─────────────────────────────────────────────
#
#   print(" ", end=" ")  →  "  " (2 chars: the space + the end separator)
#   print("*", end=" ")  →  "* " (2 chars: the star + the end separator)
#   They take equal width. Spaces and stars are interchangeable in terms of layout.

def pattern_triangle(n):
    for i in range(1, n + 1):
        # Part 1: (n - i) leading spaces for centering
        for s in range(n - i):
            print(" ", end=" ")
        # Part 2: (2*i - 1) stars
        for j in range(2 * i - 1):
            print("*", end=" ")
        print()

print("\n=== Pattern 07: Pattern Triangle (Isoceles) ===")
pattern_triangle(n)


# =============================================================================
# PATTERN 08: Pattern Number Ladder
# =============================================================================
#
# Output (n=5):
#   1
#   2 2
#   3 3 3
#   4 4 4 4
#   5 5 5 5 5
#
# Mental Model:
#   "Each rung of the ladder shows its own row number."
#   Row i: print the number i exactly i times.
#   Shape is the same as Half Pyramid, but we print i (not j or 1) in each cell.
#
# Formula:
#   Row i → print the value i, exactly i times.
#
# Key insight — the common mistake:
#   Half Pyramid:   inner loop prints j  → gives 1, 2, 3, ...
#   Pattern 1:      inner loop prints 1  → gives 1, 1, 1, ...
#   Number Ladder:  inner loop prints i  → gives 2, 2, 2, ... (the ROW NUMBER)
#   The only difference is WHAT the inner print statement outputs.

def number_ladder(n):
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print(i, end=" ")         # print i (row number), NOT j
        print()

print("\n=== Pattern 08: Pattern Number Ladder ===")
number_ladder(n)


# =============================================================================
# PATTERN 09: Pattern with Zeros (Checkerboard)
# =============================================================================
#
# Output (n=5):
#   1 0 1 0 1
#   0 1 0 1 0
#   1 0 1 0 1
#   0 1 0 1 0
#   1 0 1 0 1
#
# Mental Model:
#   Like a chessboard. If (row + col) is even → print 1. If odd → print 0.
#
# Why does (i + j) % 2 work?
#   (i+j) flips between even and odd as i or j changes by 1.
#   Even sum → 1.  Odd sum → 0.  So neighbours always differ. ✓
#
# ─── Worked example (1-indexed) ────────────────────────────────────────────
#
#   (i=1, j=1): 1+1=2 even  → 1
#   (i=1, j=2): 1+2=3 odd   → 0
#   (i=1, j=3): 1+3=4 even  → 1
#   (i=2, j=1): 2+1=3 odd   → 0
#   (i=2, j=2): 2+2=4 even  → 1
#   ...
#
# Alternative: use XOR or a flip variable,
#   but (i + j) % 2 is the cleanest one-liner.

def pattern_with_zeros(n):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if (i + j) % 2 == 0:
                print(1, end=" ")
            else:
                print(0, end=" ")
        print()

print("\n=== Pattern 09: Pattern with Zeros (Checkerboard) ===")
pattern_with_zeros(n)


# =============================================================================
# PATTERN 10: Hollow Rhombus Pattern (Slanted Hollow Rectangle)
# =============================================================================
#
# Output (n=5):
#     * * * * *     ← row 1: (n-1) leading spaces, all n stars
#    *         *    ← rows 2..n-1: (n-i) spaces, first star, gaps, last star
#   *           *
#  *             *
# * * * * * * * * * ← row n: no spaces, all 9 stars (n + n-1 + ... SHIFTED)
#
# Wait — a slanted rhombus (parallelogram) is NOT a diamond.
# It's a RECTANGLE that's been tilted:
#
#     * * * * *    ← row 1: 4 leading spaces, 5 stars (filled)
#    *       *     ← row 2: 3 leading spaces, star, 3 inner spaces, star
#   *       *      ← row 3: 2 leading spaces, star, 3 inner spaces, star
#  *       *       ← row 4: 1 leading space, star, 3 inner spaces, star
# * * * * *        ← row 5: 0 leading spaces, 5 stars (filled)
#
# Mental Model:
#   - n rows, each row has n stars TOTAL width.
#   - Row i has (n - i) leading spaces (so the shape tilts).
#   - Row 1 and row n are SOLID (all stars).
#   - Middle rows are HOLLOW (only first and last star, spaces in between).
#
# Inner gap = n - 2 spaces (constant regardless of row, because total width = n)
#
# Formula:
#   Leading spaces: n - i
#   If first or last row → all n stars
#   Otherwise → "*" + (n-2) spaces + "*"

def hollow_rhombus(n):
    for i in range(1, n + 1):
        # Part 1: leading spaces for the slant
        for s in range(n - i):
            print(" ", end=" ")

        # Part 2: star content
        if i == 1 or i == n:              # first and last row → solid
            for j in range(n):
                print("*", end=" ")
        else:                              # middle rows → hollow
            print("*", end=" ")
            for gap in range(n - 2):
                print(" ", end=" ")
            print("*", end=" ")

        print()

print("\n=== Pattern 10: Hollow Rhombus Pattern ===")
hollow_rhombus(n)


# =============================================================================
# ──────────────── TIER 3: TWO-PART SHAPES (Medium) ───────────────────────────
# =============================================================================

# =============================================================================
# PATTERN 11: Pattern Mountain (Number Mountain — Peaks at Center)
# =============================================================================
#
# Output (n=5):
#         1
#       2 1 2
#     3 2 1 2 3
#   4 3 2 1 2 3 4
# 5 4 3 2 1 2 3 4 5
#
# Mental Model:
#   Row i has 2i-1 numbers, peaking at 1 in the center and counting up to i on
#   both sides. Like a valley of numbers that dips to 1 at the center.
#
# Each row has THREE parts:
#   1. Leading spaces: (n - i) spaces for centering
#   2. LEFT side: count DOWN from i to 1
#   3. RIGHT side: count UP from 2 to i   (mirror of left, but skipping 1)
#
# Breakdown (n=5):
#   i=1: [4 spaces] [1]               → "        1"
#   i=2: [3 spaces] [2 1] [2]         → "      2 1 2"
#   i=3: [2 spaces] [3 2 1] [2 3]     → "    3 2 1 2 3"
#   i=4: [1 space ] [4 3 2 1] [2 3 4] → "  4 3 2 1 2 3 4"
#   i=5: [0 spaces] [5 4 3 2 1] [2 3 4 5]
#
# Note: RIGHT side starts at 2 (not 1) because 1 is already printed in the left.

def pattern_mountain(n):
    for i in range(1, n + 1):
        # Part 1: leading spaces
        for s in range(n - i):
            print(" ", end=" ")
        # Part 2: left side — count DOWN from i to 1
        for j in range(i, 0, -1):
            print(j, end=" ")
        # Part 3: right side — count UP from 2 to i (skip the center 1)
        for j in range(2, i + 1):
            print(j, end=" ")
        print()

print("\n=== Pattern 11: Pattern Mountain (Number Valley) ===")
pattern_mountain(n)


# =============================================================================
# PATTERN 12: Pattern Rhombus (Filled Parallelogram)
# =============================================================================
#
# Output (n=5):
#     * * * * *    ← 4 leading spaces (most spaces at top)
#    * * * * *     ← 3 spaces
#   * * * * *      ← 2 spaces
#  * * * * *       ← 1 space
# * * * * *        ← 0 spaces (bottom-left corner)
#
# Mental Model:
#   A rectangle of stars that's been TILTED to the left.
#   Every row still has exactly n stars — the only change is the indent.
#   Row i has (n - i) leading spaces. Stars never change (always n).
#
# This creates the parallelogram / rhombus shape.
#
# Formula:
#   Leading spaces: n - i  (decrements from n-1 to 0 as i goes 1 to n)
#   Stars per row: n       (constant)
#
# Visual explanation:
#   Row 1 → 4 spaces + 5 stars  (pushed RIGHT by 4)
#   Row 5 → 0 spaces + 5 stars  (all the way LEFT)
#   The left edge slides left by 1 each row → creates the diagonal left side.

def pattern_rhombus(n):
    for i in range(1, n + 1):
        # Part 1: leading spaces (creates the slant)
        for s in range(n - i):
            print(" ", end=" ")
        # Part 2: always n stars (no change per row)
        for j in range(n):
            print("*", end=" ")
        print()

print("\n=== Pattern 12: Pattern Rhombus (Filled Parallelogram) ===")
pattern_rhombus(n)


# =============================================================================
# PATTERN 13: Pattern Numbers & Stars - 2  (Palindrome Number Rows)
# =============================================================================
#
# Output (n=5):
#   1
#   1 2 1
#   1 2 3 2 1
#   1 2 3 4 3 2 1
#   1 2 3 4 5 4 3 2 1
#
# Mental Model:
#   Row i prints a PALINDROME sequence of numbers:
#   go UP from 1 to i, then come BACK DOWN from i-1 to 1.
#   The peak (i) appears exactly once in the center.
#
# Row-by-row:
#   i=1: [1]               → 1
#   i=2: [1 2] [1]         → 1 2 1
#   i=3: [1 2 3] [2 1]     → 1 2 3 2 1
#   i=4: [1..4] [3 2 1]    → 1 2 3 4 3 2 1
#   i=5: [1..5] [4 3 2 1]  → 1 2 3 4 5 4 3 2 1
#
# Three-part structure:
#   Left part:  1, 2, ..., i          (i numbers ascending)
#   Right part: i-1, i-2, ..., 1     (i-1 numbers descending)
#   NOTE: the peak (i) is already printed in left; right starts at i-1.
#
# Total numbers in row i: i + (i-1) = 2i - 1  (same as Pattern 07 stars!)

def numbers_and_stars_2(n):
    for i in range(1, n + 1):
        # Part 1: ascending from 1 to i
        for j in range(1, i + 1):
            print(j, end=" ")
        # Part 2: descending from i-1 back to 1 (the mirror)
        for j in range(i - 1, 0, -1):
            print(j, end=" ")
        print()

print("\n=== Pattern 13: Pattern Numbers & Stars - 2 (Palindrome) ===")
numbers_and_stars_2(n)


# =============================================================================
# PATTERN 14: Pattern HourGlass
# =============================================================================
#
# Output (n=5)  [total rows = 2n-1 = 9]:
#   * * * * * * * * *    ← row 1: widest (2n-1 = 9 stars)
#     * * * * * * *      ← row 2: shrinks by 1 space each side
#       * * * * *
#         * * *
#           *            ← row n=5: narrowest (1 star)
#         * * *          ← row n+1: growing again
#       * * * * *
#     * * * * * * *
#   * * * * * * * * *    ← row 2n-1: widest again
#
# Mental Model:
#   Like a sand timer (⧗) — wide at top, narrows to a point, then widens again.
#   Upper half: rows 1..n  — stars SHRINK (2n-1 down to 1)
#   Lower half: rows n+1..2n-1 — stars GROW (3 up to 2n-1)
#
# ─── UPPER HALF ──────────────────────────────────────────────────────────────
#
#   Row i (i = 1..n):
#   Stars: 2*(n-i)+1    → at i=1: 2(n-1)+1 = 2n-1. At i=n: 2(0)+1 = 1. ✓
#   Leading spaces: i-1 → at i=1: 0. At i=n: n-1 spaces. ✓
#
# ─── LOWER HALF ──────────────────────────────────────────────────────────────
#
#   Row i (i = n+1..2n-1):
#   Let k = i - n  (k goes from 1 to n-1)
#   Stars: 2*k+1  → at k=1: 3 stars. At k=n-1: 2n-1 stars. ✓
#   Leading spaces: n-k-1  → at k=1: n-2. At k=n-1: 0. ✓
#
# Diagram showing the star count progression (n=5):
#
#   Row 1: 9 stars   (0 spaces)
#   Row 2: 7 stars   (1 space)
#   Row 3: 5 stars   (2 spaces)
#   Row 4: 3 stars   (3 spaces)
#   Row 5: 1 star    (4 spaces)   ← narrowest
#   Row 6: 3 stars   (3 spaces)
#   Row 7: 5 stars   (2 spaces)
#   Row 8: 7 stars   (1 space)
#   Row 9: 9 stars   (0 spaces)

def pattern_hourglass(n):
    # Upper half (wide → narrow): row i = 1 to n
    for i in range(1, n + 1):
        stars = 2 * (n - i) + 1       # starts at 2n-1, shrinks to 1
        spaces = i - 1                # starts at 0, grows to n-1

        for s in range(spaces):
            print(" ", end=" ")
        for j in range(stars):
            print("*", end=" ")
        print()

    # Lower half (narrow → wide): row i = n+1 to 2n-1
    for i in range(n + 1, 2 * n):
        k = i - n                     # k = 1, 2, ..., n-1
        stars = 2 * k + 1             # grows from 3 to 2n-1
        spaces = n - k - 1            # shrinks from n-2 to 0

        for s in range(spaces):
            print(" ", end=" ")
        for j in range(stars):
            print("*", end=" ")
        print()

print("\n=== Pattern 14: Pattern HourGlass ===")
pattern_hourglass(n)


# =============================================================================
# PATTERN 15: Pattern InvertedHourGlass (Star Diamond)
# =============================================================================
#
# Output (n=5)  [total rows = 2n-1 = 9]:
#           *            ← row 1: 1 star (narrowest)
#         * * *          ← row 2: 3 stars
#       * * * * *        ← row 3: 5 stars
#     * * * * * * *      ← row 4: 7 stars
#   * * * * * * * * *    ← row n=5: widest (9 stars)
#     * * * * * * *      ← row 6: shrinks
#       * * * * *
#         * * *
#           *            ← row 9: narrowest again
#
# Mental Model:
#   The INVERSE of the HourGlass — narrow at top and bottom, wide in middle.
#   Upper half: starts at 1 star, grows to 2n-1 stars.
#   Lower half: shrinks back from 2n-3 stars to 1 star.
#
# This is also called a STAR DIAMOND or RHOMBUS.
#
# ─── UPPER HALF ──────────────────────────────────────────────────────────────
#
#   Row i (i = 1..n):
#   Stars:  2*i - 1     → at i=1: 1 star. At i=n: 2n-1 stars. ✓
#   Spaces: n - i       → at i=1: n-1 spaces. At i=n: 0 spaces. ✓
#
# ─── LOWER HALF ──────────────────────────────────────────────────────────────
#
#   Row i (i = n+1..2n-1):
#   Let k = 2*n - i     (k counts DOWN: at i=n+1, k=n-1; at i=2n-1, k=1)
#   Stars:  2*k - 1
#   Spaces: n - k
#
# Diagram (n=5):
#
#   Row 1: 1 star    (4 spaces)
#   Row 2: 3 stars   (3 spaces)
#   Row 3: 5 stars   (2 spaces)
#   Row 4: 7 stars   (1 space)
#   Row 5: 9 stars   (0 spaces)  ← widest
#   Row 6: 7 stars   (1 space)
#   Row 7: 5 stars   (2 spaces)
#   Row 8: 3 stars   (3 spaces)
#   Row 9: 1 star    (4 spaces)

def inverted_hourglass(n):
    # Upper half (narrow → wide): row i = 1 to n
    for i in range(1, n + 1):
        stars = 2 * i - 1             # 1, 3, 5, ..., 2n-1
        spaces = n - i                # n-1, n-2, ..., 0

        for s in range(spaces):
            print(" ", end=" ")
        for j in range(stars):
            print("*", end=" ")
        print()

    # Lower half (wide → narrow): row i = n+1 to 2n-1
    for i in range(n + 1, 2 * n):
        k = 2 * n - i                 # k = n-1, n-2, ..., 1
        stars = 2 * k - 1             # 2n-3, 2n-5, ..., 1
        spaces = n - k                # 1, 2, ..., n-1

        for s in range(spaces):
            print(" ", end=" ")
        for j in range(stars):
            print("*", end=" ")
        print()

print("\n=== Pattern 15: Pattern InvertedHourGlass (Star Diamond) ===")
inverted_hourglass(n)


# =============================================================================
# ──────────────── TIER 4: COMBINING TECHNIQUES (Medium-Hard) ─────────────────
# =============================================================================

# =============================================================================
# PATTERN 16: Mirror Star Pattern (Pattern 5) — Butterfly / X Shape
# =============================================================================
#
# Output (n=5)  [total rows = 2n-1 = 9]:
#   *               *    ← row 1: 1 star, 7 inner spaces, 1 star
#   * *           * *    ← row 2: 2 stars, 5 inner spaces, 2 stars
#   * * *       * * *    ← row 3
#   * * * *   * * * *    ← row 4
#   * * * * * * * * *    ← row n=5: full row (2n-1 = 9 stars, no gap)
#   * * * *   * * * *    ← row 6 (mirror of row 4)
#   * * *       * * *    ← row 7 (mirror of row 3)
#   * *           * *    ← row 8 (mirror of row 2)
#   *               *    ← row 9 (mirror of row 1)
#
# Mental Model:
#   TWO TRIANGLES growing toward each other from the left and right edges,
#   meeting in the middle. The shape looks like a butterfly or the letter X.
#
# ─── UPPER HALF (rows 1..n) ──────────────────────────────────────────────────
#
#   Row i:
#   Total width: 2n-1 positions.
#   Left stars:  i
#   Right stars: i
#   Inner gap:   (2n-1) - 2i    (gap shrinks as i grows)
#
#   When gap < 0 (i.e., i = n): just print 2n-1 stars (no gap; full row).
#
# ─── LOWER HALF (rows n+1..2n-1) ─────────────────────────────────────────────
#
#   Let k = 2*n - i    (k = n-1, n-2, ..., 1 as i = n+1, n+2, ..., 2n-1)
#   Left stars: k
#   Right stars: k
#   Inner gap: (2n-1) - 2k

def _mirror_star_row(i, n):
    """Print one row of the mirror star pattern."""
    gap = (2 * n - 1) - 2 * i
    if gap <= 0:                      # middle row → no gap, just fill all stars
        for j in range(2 * n - 1):
            print("*", end=" ")
    else:
        # Left stars
        for j in range(i):
            print("*", end=" ")
        # Inner gap (invisible middle)
        for g in range(gap):
            print(" ", end=" ")
        # Right stars
        for j in range(i):
            print("*", end=" ")
    print()

def mirror_star_pattern(n):
    # Upper half (rows 1..n): stars grow inward
    for i in range(1, n + 1):
        _mirror_star_row(i, n)
    # Lower half (rows n+1..2n-1): stars shrink outward
    for i in range(n - 1, 0, -1):
        _mirror_star_row(i, n)

print("\n=== Pattern 16: Mirror Star Pattern (Butterfly / X) ===")
mirror_star_pattern(n)


# =============================================================================
# PATTERN 17: Pattern Double Sided Arrow  (Vertical Double Arrow ↕)
# =============================================================================
#
# Output (n=5)  [total rows = 2n-1 = 9]:
#   *                ← row 1: 1 star (arrowhead top, pointing up)
#   * *
#   * * *
#   * * * *
#   * * * * *        ← row n=5: widest middle
#   * * * *
#   * * *
#   * *
#   *                ← row 9: 1 star (arrowhead bottom, pointing down)
#
# Mental Model:
#   Two right-angled triangles placed base-to-base, growing up from the top
#   and then shrinking back. The shape resembles a ↕ double-headed arrow.
#
# This is a LEFT-ALIGNED diamond (no centering — no leading spaces).
#
# ─── UPPER HALF (rows 1..n) ──────────────────────────────────────────────────
#
#   Row i: i stars   → 1, 2, 3, ..., n
#
# ─── LOWER HALF (rows n+1..2n-1) ─────────────────────────────────────────────
#
#   Row i: (2n - i) stars → n-1, n-2, ..., 1
#
# Contrast with Pattern 15 (InvertedHourGlass):
#   Pattern 15 is CENTERED (leading spaces for each row)
#   Pattern 17 is LEFT-ALIGNED (no leading spaces)
#   The star count formula is the same, but the visual is very different.

def double_sided_arrow(n):
    # Upper half: 1 → n stars
    for i in range(1, n + 1):
        for j in range(i):
            print("*", end=" ")
        print()
    # Lower half: n-1 → 1 stars
    for i in range(n - 1, 0, -1):
        for j in range(i):
            print("*", end=" ")
        print()

print("\n=== Pattern 17: Pattern Double Sided Arrow ===")
double_sided_arrow(n)


# =============================================================================
# PATTERN 18: Pattern Magic (Hollow Square)
# =============================================================================
#
# Output (n=5):
#   * * * * *    ← top border: all stars
#   *       *    ← middle rows: only first and last star
#   *       *
#   *       *
#   * * * * *    ← bottom border: all stars
#
# Mental Model:
#   A square frame. The OUTSIDE is stars, the INSIDE is hollow (spaces).
#
# Rules:
#   - First row (i=1): all n stars
#   - Last row (i=n): all n stars
#   - Middle rows: first star, (n-2) spaces, last star
#
# ─── The "HOLLOW" technique ──────────────────────────────────────────────────
#
#   This is the foundational technique for ALL hollow patterns:
#
#   For a row with `count` items:
#   - If first row or last row → print all items normally.
#   - Otherwise → only print if j == 1 (first item) or j == count (last item).
#     In between: print spaces.
#
#   Code structure:
#
#     if i == 1 or i == n:           ← border rows: all filled
#         print("*") × n times
#     else:                          ← interior rows: hollow
#         print("*")                 ← left border
#         print(" ") × (n-2) times  ← hollow interior
#         print("*")                 ← right border
#
#   This same logic is used in Hollow Rhombus (Pattern 10), Hollow Diamond
#   (Pattern 20), and any other "hollow" pattern.

def pattern_magic(n):
    for i in range(1, n + 1):
        if i == 1 or i == n:           # top and bottom borders → all stars
            for j in range(n):
                print("*", end=" ")
        else:                           # middle rows → hollow
            print("*", end=" ")
            for gap in range(n - 2):
                print(" ", end=" ")
            print("*", end=" ")
        print()

print("\n=== Pattern 18: Pattern Magic (Hollow Square) ===")
pattern_magic(n)


# =============================================================================
# PATTERN 19: Ganesha's Pattern (Cross / Hash Grid)
# =============================================================================
#
# Output (n=5):
#   * *     * *    ← first n//2 rows: two blocks of n//2 stars, gap in middle
#   * *     * *
#   * * * * * *    ← middle row: full row of stars
#   * *     * *    ← last n//2 rows: mirror of top
#   * *     * *
#
# For n=6:
#   * * *   * * *
#   * * *   * * *
#   * * *   * * *
#   * * * * * * *  ← middle row
#   * * *   * * *
#   * * *   * * *
#   * * *   * * *
#
# Mental Model:
#   Based on the auspicious Hindu Ganesha symbol (resembles a simplified form).
#   The pattern divides the row into two halves separated by a gap EXCEPT on
#   the middle row, which is a full solid bar of stars.
#
# ─── Row types ───────────────────────────────────────────────────────────────
#
#   Middle row (i == n//2 + 1 for even n, or i == n//2 + 1 for odd n):
#     → print n+1 stars (full bar)
#
#   All other rows:
#     → Left block:  n//2 stars
#     → Gap:         n//2 - 1 spaces (or 1 space for simplicity)
#     → Right block: n//2 stars
#
# Note: This pattern scales differently based on odd vs even n.
#       We'll implement for even n (n//2 * 2 == n).

def ganesha_pattern(n):
    half = n // 2
    middle = half + 1                 # the full bar row (1-indexed)
    total_rows = 2 * half + 1         # always odd number of rows

    for i in range(1, total_rows + 1):
        if i == middle:               # full horizontal bar of stars
            for j in range(n + 1):
                print("*", end=" ")
        else:                         # two blocks with a gap
            # Left block: half stars
            for j in range(half):
                print("*", end=" ")
            # Gap: half-1 spaces (or 1 space minimum)
            for g in range(max(1, half - 1)):
                print(" ", end=" ")
            # Right block: half stars
            for j in range(half):
                print("*", end=" ")
        print()

print("\n=== Pattern 19: Ganesha's Pattern (Cross Grid) ===")
ganesha_pattern(n)


# =============================================================================
# PATTERN 6 / PATTERN 20: Hollow Diamond Pattern
# =============================================================================
# Note: this problem is often called Pattern 6 in the prompt, but in this file
# it is placed later as Pattern 20 to keep the pattern sequence organized.
#
# Output (n=5)  [total rows = 2n-1 = 9]:
#           *            ← only 1 star (first & last = same)
#         *   *          ← 2 stars with a gap
#       *       *
#     *           *
#   *               *    ← widest row (row n): 1 star, 2n-3 gap, 1 star
#     *           *
#       *       *
#         *   *
#           *
#
# Mental Model:
#   Take Pattern 15 (InvertedHourGlass / filled star diamond) and make it HOLLOW.
#   Same centering and row structure, but inside each row only print the
#   FIRST and LAST star. Everything in between is spaces.
#
# ─── Upper half (rows 1..n) ──────────────────────────────────────────────────
#
#   Row i:
#   Leading spaces: n - i            (same as filled diamond)
#   Stars: 2*i - 1 total (in filled) → only print position 1 and 2i-1
#   Inner gap: (2*i - 1) - 2 = 2*i - 3 spaces between the two border stars
#
#   Special case: i == 1 → only 1 star (both first=last), print just "*"
#
# ─── Lower half (rows n+1..2n-1) ─────────────────────────────────────────────
#
#   Mirror of upper half. Row i maps to upper-half row k = 2*n - i.
#
# ─── Hollow technique applied ─────────────────────────────────────────────────
#
#   In a row with `stars` stars total (from the filled version):
#   - If stars == 1 → just print one star.
#   - Otherwise → print "*", then (stars - 2) spaces, then "*".

def _hollow_diamond_row(i, n):
    """Print one row of the hollow diamond pattern."""
    leading_spaces = abs(n - i)       # works for both halves
    stars = 2 * min(i, 2 * n - i) - 1   # total star count in filled version
    # (this formula gives the same result as the two-half approach)

    # Recalculate properly using position in the diamond
    # Upper half: i = 1..n → stars = 2i-1, spaces = n-i
    # Lower half: i = n+1..2n-1 → mirror
    if i <= n:
        filled_stars = 2 * i - 1
        spaces_lead = n - i
    else:
        k = 2 * n - i
        filled_stars = 2 * k - 1
        spaces_lead = n - k

    # Print leading spaces
    for s in range(spaces_lead):
        print(" ", end=" ")

    # Print the row content (hollow)
    if filled_stars == 1:
        print("*", end=" ")
    else:
        print("*", end=" ")
        for g in range(filled_stars - 2):
            print(" ", end=" ")
        print("*", end=" ")

    print()

def hollow_diamond(n):
    for i in range(1, 2 * n):       # rows 1 to 2n-1
        _hollow_diamond_row(i, n)

print("\n=== Pattern 20: Hollow Diamond Pattern ===")
hollow_diamond(n)


# =============================================================================
# PATTERN 6: Hollow Diamond Pattern (Prompt version)
# =============================================================================
# Output (n=5):
#   * * * * *
#   * *   * *
#   *   *   *
#   * *   * *
#   * * * * *
#
# Explanation:
#   - First and last rows are full of stars.
#   - The rows between form a hollow diamond shape inside the square.
#   - For row i (2..n-1), the stars are at positions:
#       1, i, n-i+1, n   if i is in the top half,
#       1, n-i+1, i, n   if i is in the bottom half (mirror symmetry).
#
#   This creates the diamond points at the center row and the two side
#   edges of the hollow diamond.
#
#   Each '*' is separated from the next by a tab, matching the prompt format.
#
# Visual row positions for n=5:
#   Row 1: 1 2 3 4 5         → * * * * *
#   Row 2: 1 2   4 5         → * *   * *
#   Row 3: 1   3   5         → *   *   *
#   Row 4: 1 2   4 5         → * *   * *
#   Row 5: 1 2 3 4 5         → * * * * *


def pattern_6_hollow_diamond(n):
    mid = (n + 1) // 2
    for i in range(1, n + 1):
        if i == 1 or i == n:
            for _ in range(n):
                print("*", end="\t")
        else:
            # Middle row should show only two stars (one at each end).
            if i == mid:
                for j in range(1, n + 1):
                    if j == 1 or j == n:
                        print("*", end="\t")
                    else:
                        print(" ", end="\t")
            else:
                if i <= mid:
                    left = i
                else:
                    left = n - i + 1
                right = n - left + 1
                for j in range(1, n + 1):
                    if j == 1 or j == left or j == right or j == n:
                        print("*", end="\t")
                    else:
                        print(" ", end="\t")
        print()


print("\n=== Pattern 6: Hollow Diamond Pattern ===")
pattern_6_hollow_diamond(n)


# =============================================================================
# ──────────────────── PRACTICE PROBLEMS ──────────────────────────────────────
# =============================================================================
#
# Solve these yourself using the mental model from above.
# Cover the solution before attempting. Work through Step 1-5 on paper.
#
# ─── PRACTICE 1: Inverted Half Pyramid ───────────────────────────────────────
#
#   * * * * *
#     * * * *     ← Notice: this one has LEADING SPACES (right-aligned)
#       * * *
#         * *
#           *
#
#   Hint: Row i has (n - i + 1) stars AND (i - 1) leading spaces.
#
# ─── PRACTICE 2: Number Right Triangle (Like Pattern 4 but right-aligned) ────
#
#           1
#         2 1
#       3 2 1
#     4 3 2 1
#   5 4 3 2 1
#
#   Hint: Same as Pattern 04 (Manmohan I) + (n-i) leading spaces.
#
# ─── PRACTICE 3: Alphabet Triangle ──────────────────────────────────────────
#
#   A
#   B B
#   C C C
#   D D D D
#   E E E E E
#
#   Hint: Row i → print chr(64 + i) exactly i times.
#         chr(65) = 'A', chr(66) = 'B', chr(67) = 'C', ...
#
# ─── PRACTICE 4: Hollow Hourglass ────────────────────────────────────────────
#
#   * * * * * * * * *    ← solid top border
#     *           *      ← hollow middle rows (only first & last star)
#       *       *
#         *   *
#           *            ← tip (only 1 star)
#         *   *
#       *       *
#     *           *
#   * * * * * * * * *    ← solid bottom border
#
#   Hint: Same structure as Pattern 14 (HourGlass), but hollow.
#         Row 1 and row 2n-1 are solid. Others: only first and last star.
#
# ─── PRACTICE 5: Spiral-border Square ───────────────────────────────────────
#
#   For n=5, output shows decreasing distance from border:
#
#   1 1 1 1 1
#   1 2 2 2 1
#   1 2 3 2 1
#   1 2 2 2 1
#   1 1 1 1 1
#
#   Formula: cell (i, j) value = min(i, j, n-i+1, n-j+1)
#   (the minimum distance from any of the 4 edges + 1)
#
#   Hint: Two nested loops, compute min(i, j, n-i+1, n-j+1) for each cell.


# ─── Solutions ────────────────────────────────────────────────────────────────
# (try them yourself first — then check here)

print("\n\n=== Practice 1: Inverted Half Pyramid (Right-Aligned) ===")
for i in range(1, n + 1):
    for s in range(i - 1):           # leading spaces increase each row
        print(" ", end=" ")
    for j in range(1, n - i + 2):    # stars decrease each row
        print("*", end=" ")
    print()

print("\n=== Practice 2: Number Right Triangle (Right-Aligned) ===")
for i in range(1, n + 1):
    for s in range(n - i):
        print(" ", end=" ")
    num = i
    for j in range(1, i + 1):
        print(num, end=" ")
        num -= 1
    print()

print("\n=== Practice 3: Alphabet Triangle ===")
for i in range(1, n + 1):
    ch = chr(64 + i)                  # 65='A', 66='B', ...
    for j in range(i):
        print(ch, end=" ")
    print()

print("\n=== Practice 4: Hollow HourGlass ===")
for i in range(1, 2 * n):
    # Reuse hourglass star/space counts from Pattern 14
    if i <= n:
        stars = 2 * (n - i) + 1
        spaces = i - 1
    else:
        k = i - n
        stars = 2 * k + 1
        spaces = n - k - 1
    # Print leading centering spaces
    for s in range(spaces):
        print(" ", end=" ")
    # Print hollow row
    if stars == 1 or i == 1 or i == 2 * n - 1:
        for j in range(stars):
            print("*", end=" ")
    else:
        print("*", end=" ")
        for g in range(stars - 2):
            print(" ", end=" ")
        print("*", end=" ")
    print()

print("\n=== Practice 5: Spiral-Border Square ===")
for i in range(1, n + 1):
    for j in range(1, n + 1):
        val = min(i, j, n - i + 1, n - j + 1)
        print(val, end=" ")
    print()
