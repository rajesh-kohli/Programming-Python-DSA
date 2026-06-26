###############################################################################
#                Lecture 6 - Pattern Printing with Nested Loops               #
###############################################################################

# Pattern printing is about using nested loops to control:
#   - Outer loop (i): which ROW we are on
#   - Inner loop(s) (j, k, ...): what to PRINT in that row (spaces, numbers, stars)
#
# The KEY insight for ALL patterns in this lecture:
#   The outer loop structure is almost always the same (a right-angled triangle).
#   Only WHAT we print in each row changes.
#
# ----- Time & Space Complexity for ALL patterns below -----
#
# Time:  O(n^2) — ALL triangle/pyramid patterns print 1+2+3+...+n = n*(n+1)/2 items
#        Even patterns with spaces: total items per row (spaces + values) is O(n),
#        and there are n rows, so it's O(n) * O(n) = O(n^2).
#
# Space: O(1) — only loop variables and counters. No arrays or lists are created.
#        (We are printing directly, not storing the pattern in memory.)
#
# The key efficiency question for patterns isn't "can we do better than O(n^2)?"
# (we can't — we MUST print n^2 characters), but rather:
#   - Are we doing unnecessary EXTRA work per element?
#   - Are we recomputing values we could derive from the previous iteration?


# =============================================================================
# PATTERN 1: Number Triangle (increasing numbers per row)
# =============================================================================

"""
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5

Same pattern as right angle triangle of stars, meaning the loop condition will stay the same
Except what we are going to print
"""

# ----- Approach -----
# Row i has i numbers: 1, 2, 3, ..., i
# So the inner loop runs from 1 to i, printing j each time.
#
# ----- How the loops map to the output -----
#
#   i=1: j runs 1 to 1  --> prints: 1
#   i=2: j runs 1 to 2  --> prints: 1 2
#   i=3: j runs 1 to 3  --> prints: 1 2 3
#   i=4: j runs 1 to 4  --> prints: 1 2 3 4
#   i=5: j runs 1 to 5  --> prints: 1 2 3 4 5

# ----- Method 1: Using for loops -----

num = int(input("Enter a number:"))

for i in range(1, num+1):          # row number (1 to num)
    for j in range(1, i+1):        # column: print numbers 1 to i
        print(j, end=" ")
    print()                         # newline after each row
print()

# ----- Method 2: Using while loops -----

## While loop
i = 1
while i <= num:
    j = 1
    while j <= i:
        print(j, end=" ")
        j = j + 1
    i = i + 1
    print()
print()

## in the above approach, we are also using the same loop variable j to print as well
## Another strategy is to have a separate variable for printing and
# use i & j only for iterating and controling the loop
# This approach would be useful in the future patterns

# ----- Method 3: While loop with a separate print variable -----
# Here, j controls the loop, and n holds the value to print.
# This separation becomes important in later patterns where the printed value
# doesn't directly match the loop variable.

## While loop with a separate variable to print

num = int(input("Enter a number:"))
i = 1
# for the ith row, print i numbers starting from 1 in the increasing order
while i <= num:
    # for the ith row, print i numbers starting from 1 in the increasing order
    j = 1
    n = 1              # n = what we print (resets to 1 each row)
    while j <= i:
        print(n, end=" ")
        j = j + 1
        n = n + 1      # n increments alongside j, but they are independent
    i = i + 1
    print()
print()

"""
Output:
        1
        1 2
        1 2 3
        1 2 3 4
        1 2 3 4 5
"""


# =============================================================================
# PATTERN 2: Continuous Number Triangle
# =============================================================================

# Pattern

"""
1
2 3
4 5 6
7 8 9 10

## Here we can clearly see the pattern for this question also matches with the previous question
and the right angled triangle of stars
# that means the loop condition is going to be the same, except what we are going to print
"""

# ----- Key Difference from Pattern 1 -----
# In Pattern 1, the print variable (n) resets to 1 at the start of EACH row.
# Here, it does NOT reset - it carries forward across rows.
#
# That's the only change: move `num = 1` OUTSIDE the outer loop.
#
# ----- How it works -----
#
#   num starts at 1 (before the loop, never resets)
#
#   i=1: print num=1, then num becomes 2               --> output: 1
#   i=2: print num=2, num=3                            --> output: 2 3
#   i=3: print num=4, num=5, num=6                     --> output: 4 5 6
#   i=4: print num=7, num=8, num=9, num=10             --> output: 7 8 9 10
#   i=5: print num=11, num=12, num=13, num=14, num=15  --> output: 11 12 13 14 15

n = 5
i = 1
num = 1  # we just moved this number outside, because we only want it to initialize once, not reset every time and this ensures the updates from the previous rows carry forward to the next row
while i <= n:
    j = 1
    while j <= i:
        print(num, end=" ")
        j = j + 1
        num = num + 1
    i = i + 1
    print()
print()

"""
1
2 3
4 5 6
7 8 9 10
11 12 13 14 15
"""


# =============================================================================
# PATTERN 3: Binary Triangle (alternating 0s and 1s)
# =============================================================================

"""
Pattern
1
0 1
1 0 1
0 1 0 1
1 0 1 0 1

Same, the pattern is the same as previous questions, only the values we print are different
# Here we notice, when it's an even row, it starts with 0 and odd rows begin with 1 - we can use index starting with 1 for that
# And here the numbers are only 1's and 0's - need to keep flipping between 1 and 0 in row
# we can flip numbers either using num = ! num OR num = 1 - num (will be used frequently)
If else is another way but not used as often:
if num == 0:
    num = 1
else:
    num = 0

Mostly use num = 1 - num for swapping numbers
"""

# ----- Two things to figure out -----
#
# 1) What does each row START with?
#    - Odd rows (i=1, 3, 5...) start with 1
#    - Even rows (i=2, 4, 6...) start with 0
#    - Formula: num = 1 if i is odd, 0 if i is even
#    - One-liner: num = 0 if i % 2 == 0 else 1
#
# 2) How do values alternate WITHIN a row?
#    - After printing num, flip it: num = 1 - num
#    - This is the cleanest way to toggle between 0 and 1:
#        1 - 1 = 0  (flips 1 to 0)
#        1 - 0 = 1  (flips 0 to 1)
#
# ----- Walkthrough -----
#
#   i=1 (odd):  num starts at 1  --> print 1                       --> 1
#   i=2 (even): num starts at 0  --> print 0, flip to 1, print 1   --> 0 1
#   i=3 (odd):  num starts at 1  --> 1, flip 0, flip 1             --> 1 0 1
#   i=4 (even): num starts at 0  --> 0, 1, 0, 1                   --> 0 1 0 1
#   i=5 (odd):  num starts at 1  --> 1, 0, 1, 0, 1                --> 1 0 1 0 1

n = int(input())

i = 1

while i <= n:
    # if i % 2 == 0:
    #     num = 0
    # else:
    #     num = 1
    num = 0 if i % 2 == 0 else 1    # set starting value based on row parity
    j = 1
    while j <= i:
        print(num, end=" ")
        num = 1 - num               # flip: 1 becomes 0, 0 becomes 1
        j = j + 1
    i = i + 1
    print()

"""
Output:

1
0 1
1 0 1
0 1 0 1
1 0 1 0 1
"""


# =============================================================================
# PATTERN 4: Right-Aligned Number Triangle (with leading spaces)
# =============================================================================

"""
Pattern:
        1
      2 3
    3 4 5
  4 5 6 7
5 6 7 8 9

Everything is straight forward here, except one thing to note in particular:
Everytime you're at the ith row, you need to start printing the numbers starting with i in increasing order

"""

# ----- What's new here: SPACES -----
# This is the first pattern where the output isn't left-aligned.
# We need to print SPACES before the numbers to push them to the right.
#
# ----- How many spaces? -----
# Row i needs (n - i) spaces before the numbers.
#   i=1: 4 spaces, then 1 number    (n-i = 5-1 = 4)
#   i=2: 3 spaces, then 2 numbers   (n-i = 5-2 = 3)
#   i=3: 2 spaces, then 3 numbers   (n-i = 5-3 = 2)
#   i=4: 1 space,  then 4 numbers   (n-i = 5-4 = 1)
#   i=5: 0 spaces, then 5 numbers   (n-i = 5-5 = 0)
#
# ----- What numbers to print? -----
# Row i prints i numbers, starting from i itself in increasing order.
#   i=1: starts at 1 --> 1
#   i=2: starts at 2 --> 2, 3
#   i=3: starts at 3 --> 3, 4, 5
#   i=4: starts at 4 --> 4, 5, 6, 7
#   i=5: starts at 5 --> 5, 6, 7, 8, 9
#
# ----- Structure of each row -----
# [ (n-i) spaces ] [ i numbers starting from i ]
# Two inner loops: one for spaces, one for numbers.

n = int(input())

for i in range(1, n + 1):
    # Loop 1: print (n-i) spaces for right-alignment
    for _ in range(n - i):
        print(" ", end=" ")

    # Loop 2: print i numbers starting from i in inc. order
    num = i
    for _ in range(i):
        print(num, end=" ")
        num = num + 1

    print()


# =============================================================================
# PATTERN 5: Number Mountain (numbers go up, then come back down)
# =============================================================================

"""

        1
      2 3 2
    3 4 5 4 3
  4 5 6 7 6 5 4
5 6 7 8 9 8 7 6 5


"""

# ----- Breaking down each row -----
# Each row has THREE parts:
#   1. Leading SPACES      (to center/right-align the pattern)
#   2. ASCENDING numbers   (numbers going up)
#   3. DESCENDING numbers  (numbers coming back down, mirroring the ascent)
#
# ----- Analysis for n=5 -----
#
#   Row i | Spaces (n-i) | Ascending (i numbers)  | Descending (i-1 numbers) |
#   ------|--------------|------------------------|--------------------------|
#   i=1   | 4 spaces     | 1                      | (none)                   |
#   i=2   | 3 spaces     | 2 3                    | 2                        |
#   i=3   | 2 spaces     | 3 4 5                  | 4 3                      |
#   i=4   | 1 space      | 4 5 6 7                | 6 5 4                    |
#   i=5   | 0 spaces     | 5 6 7 8 9              | 8 7 6 5                  |
#
# ----- How the variable 'n' works -----
# We use a counter 'n' that:
#   - In the ascending part: increments (n = n + 1) for i steps
#   - In the descending part: decrements (n = n - 1) for (i-1) steps
#   - After the ascending part, n is 1 too high, so decrementing gives the mirror
#
# ----- Detailed trace for row 3 (i=3) -----
#   n starts at value after previous row = 3
#   Ascending (k loop, i=3 times):
#     k=0: print n=3, n becomes 4
#     k=1: print n=4, n becomes 5
#     k=2: print n=5, n becomes 6
#   Descending (l loop, i-1=2 times):
#     l=0: n becomes 5, print n=5  --> wait, that gives 5 not 4
#
#   Actually: after ascending, n=6. Then descending:
#     l=0: n becomes 5 (n-1), print 5  ... hmm, but expected output is "4 3"
#
#   Let me re-trace: the code decrements BEFORE printing.
#     l=0: n = 6-1 = 5, print 5? No...
#
#   Looking at the code more carefully:
#     Ascending: n starts at some value, print n, then n += 1 (i times)
#     Descending: n -= 1, then print n (i-1 times)
#
#   BUT n at the end of ascending is 1 past the peak.
#   So first decrement brings it to peak, second decrement to peak-1, etc.
#   The descending loop runs i-1 times, but the first decrement just undoes the peak.
#
#   Actually looking at the expected output for i=3: "3 4 5 4 3"
#   After ascending prints "3 4 5", n = 6
#   Descending (i-1 = 2 times):
#     l=0: n = 6-1 = 5, print 5? But expected is 4!
#
#   Hmm, the code actually does n = n - 1 FIRST then prints. Let me re-read the code:
#     for l in range(i-1):
#         n = n - 1
#         print(n, end = " ")
#
#   i=3 row: after ascending, n=6 (printed 3,4,5 and n incremented each time)
#   Wait, n was a local variable that resets... No, looking at the code, n=0 is set
#   before the outer loop and carries forward. Let me trace from the start:
#
#   n=0 before loop:
#   i=1: ascending 1 time: n=0+1=1, print 1. After: n=1. Descending 0 times.
#   i=2: ascending 2 times: n=1+1=2 print 2, n=2+1=3 print 3. After n=3.
#         Descending 1 time: n=3-1=2, print 2. Output: "2 3 2"
#   i=3: ascending 3 times: n=2+1=3 print 3, n=3+1=4 print 4, n=4+1=5 print 5. After n=5.
#         Descending 2 times: n=5-1=4 print 4, n=4-1=3 print 3. Output: "3 4 5 4 3" ✓
#
# So the trick is: n carries forward AND the ascending part does n += 1 BEFORE printing.

# ----- Full trace (n=5, variable name changed to 'ctr' in notes to avoid confusion) -----
#
# ctr=0 initially
#
# i=1: Ascending: ctr goes 1        --> print: 1
#      Descending: (0 times)        --> print: (nothing)
#      Output: "        1"          (4 spaces + "1")
#      ctr=1 after row
#
# i=2: Ascending: ctr goes 2, 3    --> print: 2 3
#      Descending: ctr goes 2      --> print: 2
#      Output: "      2 3 2"       (3 spaces + "2 3 2")
#      ctr=2 after row
#
# i=3: Ascending: ctr goes 3, 4, 5     --> print: 3 4 5
#      Descending: ctr goes 4, 3       --> print: 4 3
#      Output: "    3 4 5 4 3"         (2 spaces + "3 4 5 4 3")
#      ctr=3 after row
#
# i=4: Ascending: ctr goes 4, 5, 6, 7      --> print: 4 5 6 7
#      Descending: ctr goes 6, 5, 4        --> print: 6 5 4
#      Output: "  4 5 6 7 6 5 4"           (1 space + "4 5 6 7 6 5 4")
#      ctr=4 after row
#
# i=5: Ascending: ctr goes 5, 6, 7, 8, 9       --> print: 5 6 7 8 9
#      Descending: ctr goes 8, 7, 6, 5         --> print: 8 7 6 5
#      Output: "5 6 7 8 9 8 7 6 5"             (0 spaces)
#      ctr=5 after row

num = int(input("Enter a number: "))
n = 0

for i in range(1, num + 1):
    # Part 1: leading spaces for right-alignment
    for j in range(num - i):
        print(" ", end=" ")

    # Part 2: ascending numbers (i numbers going up)
    for k in range(i):
        n = n + 1
        print(n, end=" ")

    # Part 3: descending numbers (i-1 numbers coming back down)
    # First decrement undoes the last increment, so we start from peak-1
    for l in range(i - 1):
        n = n - 1
        print(n, end=" ")

    print()
print()

"""
Output:
        1
      2 3 2
    3 4 5 4 3
  4 5 6 7 6 5 4
5 6 7 8 9 8 7 6 5
"""

# ----- Why does n carry the right value to the next row? -----
# After each row, the descending part brings n back down.
# Row i: ascending adds i, descending subtracts (i-1)
# Net change per row = i - (i-1) = 1
# So after row 1: n=1, after row 2: n=2, after row 3: n=3, ...
# This means row i always starts ascending from n = i-1, and first print is i. Perfect!


# =============================================================================
# PATTERN 6: Star Diamond
# =============================================================================

# ----- Expected Output (for num=5) -----
#
# *
# * *
# * * *
# * *
# *
#
# ----- Approach -----
# The pattern has two halves:
#   - First half (rows 1 to num//2): stars INCREASE  --> print i stars
#   - Second half (rows num//2+1 to num): stars DECREASE --> print (num - i + 1) stars
#
# This only works correctly for ODD numbers (so the diamond is symmetric).
#
# ----- Breakdown for num=5 (num//2 = 2) -----
#
#   i=1: i <= 2? YES  --> print 1 star     --> *
#   i=2: i <= 2? YES  --> print 2 stars    --> * *
#   i=3: i <= 2? NO   --> print 5-3+1 = 3  --> * * *    (peak / middle row)
#   i=4: i <= 2? NO   --> print 5-4+1 = 2  --> * *
#   i=5: i <= 2? NO   --> print 5-5+1 = 1  --> *

num = int(input("Enter any postive odd number:"))

for i in range(1, num + 1):
    if i <= (num // 2):
        print("* " * i)
    else:
        print("* " * (num - i + 1))
print()

# ----- "* " * n trick -----
# In Python, multiplying a string repeats it:
#   "* " * 3  -->  "* * * "
# This is a shortcut to avoid writing an inner loop for stars.


# =============================================================================
# Summary: Pattern-Solving Strategy
# =============================================================================

# 1. OBSERVE the pattern - how many rows? What changes per row?
# 2. Identify the STRUCTURE - is it a right-angled triangle? Pyramid? Diamond?
# 3. Break each row into PARTS - spaces? numbers? stars? ascending then descending?
# 4. Figure out the RELATIONSHIP between row number (i) and what's printed:
#    - How many items per row?
#    - What value does each row START with?
#    - Does the print variable RESET each row or CARRY FORWARD?
# 5. Write the OUTER loop for rows, then INNER loop(s) for each part.
#
# Common tricks:
#   - Separate print variable from loop variable (Pattern 1, Method 3)
#   - Variable outside loop to carry forward (Pattern 2)
#   - num = 1 - num to flip between 0 and 1 (Pattern 3)
#   - (n - i) spaces for right-alignment (Patterns 4, 5)
#   - Ascending then descending with increment/decrement (Pattern 5)
#
# ----- Complexity Recap -----
#
# | Pattern                     | Time   | Space | Inner loops per row    |
# |-----------------------------|--------|-------|------------------------|
# | Pattern 1: Number Triangle  | O(n^2) | O(1)  | 1 loop (j: values)    |
# | Pattern 2: Continuous Nums  | O(n^2) | O(1)  | 1 loop (j: values)    |
# | Pattern 3: Binary Triangle  | O(n^2) | O(1)  | 1 loop (j: values)    |
# | Pattern 4: Right-Aligned    | O(n^2) | O(1)  | 2 loops (spaces+vals) |
# | Pattern 5: Number Mountain  | O(n^2) | O(1)  | 3 loops (spc+asc+desc)|
# | Pattern 6: Star Diamond     | O(n)   | O(1)  | 1 string multiply     |
#
# Pattern 5 has 3 inner loops but they're NOT nested — they run sequentially
# within each row, so total work per row is still O(n), not O(n^2).
# Pattern 6 is O(n) because each row is O(1) work (string multiplication).
