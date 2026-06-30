# =============================================================================
# FOR LOOPS IN PYTHON
# =============================================================================
# A for loop lets you repeat a block of code a known number of times.
# It has three logical parts (similar to other languages like C/Java):
#   1. Initialization  -- where the loop variable starts
#   2. Condition        -- when the loop should stop
#   3. Updation         -- how the loop variable changes each iteration
#
# In Python, the `range()` function bundles all three into one call.


# =============================================================================
# SECTION 1: The range() Function
# =============================================================================
# Syntax:  range(start, stop, step)
#
#   start     --> the first value (inclusive). Default is 0.
#   stop      --> where to end (EXCLUSIVE -- this value is never included).
#   step      --> how much to add each time. Default is 1.
#
# Key points:
#   - range(n)          --> 0, 1, 2, ..., n-1           (n items)
#   - range(a, b)       --> a, a+1, a+2, ..., b-1       (b-a items)
#   - range(a, b, s)    --> a, a+s, a+2s, ... up to (not including) b
#   - range() produces values lazily (one at a time), so it uses O(1) memory
#     regardless of how large the range is.
#
# Quick examples:
#   range(5)        --> 0, 1, 2, 3, 4
#   range(2, 7)     --> 2, 3, 4, 5, 6
#   range(0, 10, 3) --> 0, 3, 6, 9
#   range(10, 0, -1)--> 10, 9, 8, 7, 6, 5, 4, 3, 2, 1  (counting down)
#   range(10, 0, -2)--> 10, 8, 6, 4, 2                  (counting down by 2)
#
# Mental model: think of range(start, stop, step) as a number line walk.
# You stand at `start`, take `step`-sized hops, and stop the instant you
# would land on or past `stop` -- that landing spot is NEVER printed.
#
#   range(2, 7):
#   0   1   [2]  3   4   5   6  (7)
#               ^start          ^stop (excluded, walk stops here)
#   visited: 2, 3, 4, 5, 6


# =============================================================================
# SECTION 2: Basic for Loop Examples
# =============================================================================

# ---- Example 1: Even numbers from 0 to 8 ----
# range(0, 10, 2) starts at 0, goes up to (not including) 10, steps by 2
print("Example 1")
for i in range(0, 10, 2):
    print(i)
# Expected Output:
# 0
# 2
# 4
# 6
# 8
# Time Complexity: O(n/2) = O(n), where n = stop value
# Space Complexity: O(1) -- range produces values one at a time
#
# Iteration trace table (loop variable only, no accumulator here):
#   iteration #   i
#   -----------   --
#       1          0
#       2          2
#       3          4
#       4          6
#       5          8


# ---- Example 2: Default start and step ----
# range(10) is shorthand for range(0, 10, 1)
# When you only give one argument, start defaults to 0 and step defaults to 1
print("Example 2")
for i in range(10):  # start=0, step=1 by default
    print(i)
# Expected Output:
# 0
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9


# =============================================================================
# SECTION 3: Bitwise Operators Inside Loops
# =============================================================================
# Quick refresher on bitwise operators:
#   >>  (right shift): shifts bits to the right, equivalent to integer division by 2^n
#       e.g., 8 >> 1 = 4  (8 / 2^1 = 4)
#            12 >> 2 = 3  (12 / 2^2 = 3)
#   <<  (left shift):  shifts bits to the left, equivalent to multiplying by 2^n
#       e.g., 3 << 1 = 6  (3 * 2^1 = 6)
#            3 << 2 = 12  (3 * 2^2 = 12)

# ---- Example 3: Operator Precedence Warning ----
# WARNING: `i >> 2 + 1` does NOT mean `(i >> 2) + 1`
# It means `i >> (2 + 1)` = `i >> 3` because:
#   - Addition (+) has HIGHER precedence than bitwise shift (>>)
#   - So Python evaluates 2+1=3 first, then shifts i right by 3
#   - i >> 3 is the same as i // 8 (integer division by 2^3 = 8)
#
# If the intention was (i >> 2) + 1 = (i // 4) + 1, use parentheses!
# This is a common gotcha. Always use parentheses with bitwise operators
# to make your intent clear.
print("Example 3")

for i in range(10):
    if i % 2 == 0:
        print(i >> 2 + 1)  # This is i >> 3 = i // 8 (see warning above)
# Expected Output (only even i values):
# i=0: 0 >> 3 = 0
# i=2: 2 >> 3 = 0   (2 in binary is 10, shifting right 3 gives 0)
# i=4: 4 >> 3 = 0   (4 in binary is 100, shifting right 3 gives 0)
# i=6: 6 >> 3 = 0   (6 in binary is 110, shifting right 3 gives 0)
# i=8: 8 >> 3 = 1   (8 in binary is 1000, shifting right 3 gives 1)
# So output is: 0, 0, 0, 0, 1
#
# Compare: if it were (i >> 2) + 1 = (i // 4) + 1:
#   i=0: (0//4)+1 = 1
#   i=2: (2//4)+1 = 1
#   i=4: (4//4)+1 = 2
#   i=6: (6//4)+1 = 2
#   i=8: (8//4)+1 = 3
# Very different results! Operator precedence matters.


# =============================================================================
# SECTION 4: Nested for Loops
# =============================================================================
# When you put one loop inside another, the INNER loop runs completely
# for EACH iteration of the OUTER loop.
#
# Execution flow for nested loops:
#   outer loop iteration 1:
#       inner loop iteration 1
#       inner loop iteration 2
#       ...
#       inner loop finishes
#   outer loop iteration 2:
#       inner loop iteration 1 (starts over!)
#       inner loop iteration 2
#       ...
#       inner loop finishes
#   ... and so on
#
# Total iterations = (outer count) * (inner count)
#
# Mental model: the outer loop picks a ROW, the inner loop walks every
# COLUMN in that row before moving to the next row -- like reading a grid
# left-to-right, top-to-bottom.
#
#   for i in range(3):        j-> 0    1    2
#       for j in range(3):  i=0 [0,0][0,1][0,2]   <- inner loop sweeps
#           ...              i=1 [1,0][1,1][1,2]     across before i
#                             i=2 [2,0][2,1][2,2]     advances to next row

# ---- Example 4: Two nested loops with modulo ----
# Outer: i goes 0,1,2,3,4  (5 iterations)
# Inner: j goes 1,2,3,4    (4 iterations)
# Total prints: 5 * 4 = 20
print("Example 4")

for i in range(5):
    for j in range(1, 5, 1):
        print(i % j)
# Execution trace (first few iterations):
# i=0: j=1 -> 0%1=0, j=2 -> 0%2=0, j=3 -> 0%3=0, j=4 -> 0%4=0
# i=1: j=1 -> 1%1=0, j=2 -> 1%2=1, j=3 -> 1%3=1, j=4 -> 1%4=1
# i=2: j=1 -> 2%1=0, j=2 -> 2%2=0, j=3 -> 2%3=2, j=4 -> 2%4=2
# i=3: j=1 -> 3%1=0, j=2 -> 3%2=1, j=3 -> 3%3=0, j=4 -> 3%4=3
# i=4: j=1 -> 4%1=0, j=2 -> 4%2=0, j=3 -> 4%3=1, j=4 -> 4%4=0
# Time Complexity: O(n * m) where n=5, m=4 --> O(20) = O(1) since constant
# In general for nested loops: O(outer_count * inner_count)


# ---- Example 5: Nested loops with conditional + bitwise ----
# Outer: i goes 0..9 (10 iterations)
# Inner: j goes 1..4 (4 iterations)
# Total prints: 10 * 4 = 40
print("Example 5")

for i in range(10):
    for j in range(1, 5, 1):
        if i % j == 0:
            print(i >> 2)   # i // 4 (right shift by 2)
        else:
            print(i << 1)   # i * 2  (left shift by 1)
# Execution trace (first few):
# i=0: j=1 -> 0%1==0 -> 0>>2=0 | j=2 -> 0%2==0 -> 0>>2=0 | j=3 -> 0%3==0 -> 0>>2=0 | j=4 -> 0%4==0 -> 0>>2=0
# i=1: j=1 -> 1%1==0 -> 1>>2=0 | j=2 -> 1%2!=0 -> 1<<1=2 | j=3 -> 1%3!=0 -> 1<<1=2 | j=4 -> 1%4!=0 -> 1<<1=2
# i=2: j=1 -> 2%1==0 -> 2>>2=0 | j=2 -> 2%2==0 -> 2>>2=0 | j=3 -> 2%3!=0 -> 2<<1=4 | j=4 -> 2%4!=0 -> 2<<1=4
# Time Complexity: O(n * m) where n=10, m=4


# ---- Example 6: Triple nested loop ----
# Outer:  i goes 0..9  (10 iterations)
# Middle: j goes 0..4  (5 iterations)
# Inner:  k goes 0..2  (3 iterations)
# Total prints: 10 * 5 * 3 = 150
print("Example 6")

for i in range(10):
    for j in range(5):
        for k in range(3):
            print(i + j - k)
# Execution trace (i=0 only):
# i=0, j=0: k=0 -> 0+0-0=0, k=1 -> 0+0-1=-1, k=2 -> 0+0-2=-2
# i=0, j=1: k=0 -> 0+1-0=1, k=1 -> 0+1-1=0,  k=2 -> 0+1-2=-1
# i=0, j=2: k=0 -> 0+2-0=2, k=1 -> 0+2-1=1,  k=2 -> 0+2-2=0
# ... and so on for all values of i
# Time Complexity: O(n * m * p) -- for 3 nested loops, complexity multiplies
# This is why deeply nested loops can be slow for large inputs!
# Space Complexity: O(1) -- only loop variables are stored


# =============================================================================
# SECTION 7: Key Takeaways
# =============================================================================
# 1. range(stop) / range(start, stop) / range(start, stop, step)
#    - stop is ALWAYS exclusive (not included in the sequence)
#    - step can be negative for counting down
#
# 2. Nested loops: inner loop completes fully for each outer iteration
#    - 2 nested loops of size n --> O(n^2) iterations
#    - 3 nested loops of size n --> O(n^3) iterations
#    - Be careful with large ranges in nested loops!
#
# 3. Operator precedence with bitwise operators:
#    - Arithmetic (+, -, *, /) has HIGHER precedence than bitwise (>>, <<, &, |, ^)
#    - Always use parentheses to make your intent clear
#    - Example: (i >> 2) + 1  vs  i >> (2 + 1)  -- very different results!
#
# 4. Common bitwise shortcuts:
#    - x >> n  is the same as  x // (2**n)   (integer division by power of 2)
#    - x << n  is the same as  x * (2**n)    (multiply by power of 2)
