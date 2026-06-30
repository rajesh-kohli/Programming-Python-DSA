# =============================================================================
# SECTION 1: Bitwise Operators -- Overview
# =============================================================================
#
# Bitwise operators work on the BINARY (bit-level) representation of integers.
# Every integer is stored as a sequence of 0s and 1s in memory.
#
# OPERATOR REFERENCE:
#
#   &   AND    - Both bits must be 1         -->  1 & 1 = 1, else 0
#   |   OR     - At least one bit must be 1  -->  0 | 0 = 0, else 1
#   ^   XOR    - Bits must be DIFFERENT      -->  1 ^ 0 = 1, 0 ^ 0 = 0, 1 ^ 1 = 0
#   ~   NOT    - Flips every bit             -->  ~x = -(x+1)
#   <<  LEFT SHIFT   - Shifts bits left, fills with 0s  (multiplies by 2^n)
#   >>  RIGHT SHIFT  - Shifts bits right, drops rightmost bits (divides by 2^n)
#
# EXAMPLES WITH BINARY:
#
#   6 & 3 :    110          6 | 3 :    110          6 ^ 3 :    110
#            & 011                   | 011                   ^ 011
#            -----                   -----                   -----
#              010 = 2                 111 = 7                 101 = 5
#
#   ~6 :  ~(0...0110) = 1...1001 = -7  (two's complement: -(6+1) = -7)
#
#   6 << 1 :  110 << 1 = 1100 = 12     (6 * 2^1 = 12)
#   6 << 2 :  110 << 2 = 11000 = 24    (6 * 2^2 = 24)
#   6 >> 1 :  110 >> 1 = 11 = 3        (6 // 2^1 = 3)
#
# COLUMN-ALIGNED TRUTH TABLE (using 5 and 3 as a worked example):
#
#       5   =  0 1 0 1
#       3   =  0 0 1 1
#      -----------------
#   5 & 3   =  0 0 0 1   = 1    (AND: 1 only where BOTH are 1)
#   5 | 3   =  0 1 1 1   = 7    (OR:  1 where AT LEAST ONE is 1)
#   5 ^ 3   =  0 1 1 0   = 6    (XOR: 1 where bits DIFFER)
#
# WHY USE BITWISE OPERATORS?
#   - They are extremely fast (direct CPU operations)
#   - Even/odd check: (n & 1) == 0 means even, == 1 means odd
#   - Multiply/divide by powers of 2: n << k = n * 2^k, n >> k = n // 2^k
#   - Swapping without a temp variable (XOR trick)
#   - Low-level programming, cryptography, image processing, networking
#
# TIME COMPLEXITY: O(1) for all bitwise operations on fixed-size integers.
# =============================================================================


# =============================================================================
# SECTION 2: Bitwise Operator Expressions
# =============================================================================
#
# Below are compound expressions combining bitwise operators with conditionals.
# Let's trace through each one with x = 6 (binary: 110).
# =============================================================================

x = 6

# --- Expression 1 ---
# x & 1: checks the last bit.  6 & 1 = 110 & 001 = 000 = 0
# So (x & 1 == 0) is True --> 6 is even.
# BUT x % 2 != 0 means "x is odd", which is False for 6.
# Since True AND False = False, this block does NOT execute.
if x & 1 == 0 and x % 2 != 0:
    # x >> 1 = 6 >> 1 = 3 (divide by 2)
    print(x >> 1)

# --- Expression 2 ---
# (x-1) >> 1 = 5 >> 1 = binary 101 >> 1 = 10 = 2
# 2 < 3 is True, so this block executes.
# x << 2 >> 1 = 6 << 2 >> 1
#   Step 1: 6 << 2 = 110 << 2 = 11000 = 24
#   Step 2: 24 >> 1 = 11000 >> 1 = 1100 = 12
if ((x - 1) >> 1) < 3:
    print(x << 2 >> 1)       # Output: 12

# --- Expression 3 ---
# ((x-1)>>1) = 2 --> truthy (non-zero)
# ((x>>1)<3) = (3 < 3) = False
# (x!=3) = True
# Evaluation (note: 'and' has higher precedence than 'or'):
#   2 or (False and True) --> 2 or False --> 2 (truthy) --> executes
# x >> 1 << 2 = 6 >> 1 << 2
#   Step 1: 6 >> 1 = 3  (binary: 11)
#   Step 2: 3 << 2 = 12 (binary: 1100)
if ((x - 1) >> 1) or ((x >> 1) < 3) and (x != 3):
    print(x >> 1 << 2)       # Output: 12


# =============================================================================
# SECTION 3: Type Casting with input()
# =============================================================================
#
# input() ALWAYS returns a string, even if the user types a number.
# To do math with user input, you must CAST it to the correct type:
#   int()    - convert to integer
#   float()  - convert to float
#   str()    - convert to string
#
# Without casting, the + operator concatenates strings instead of adding.
#
# CASTING DIAGRAM:
#   input() -> "3"  ----int()---->  3   (str object replaced by an int object)
#   "3" + "4" = "34"   (concatenation, no math)
#   int("3") + int("4") = 7   (real addition)
# =============================================================================

# WITHOUT type casting: string concatenation happens
x = input("enter any value:")
y = input("enter any value:")
print(x + y)           # If you enter 3 and 4, output is "34" (string concat!)
print(type(x + y))     # Output: <class 'str'>

## need to do type casting
x = int(input("enter any value:"))  ##type casting
y = int(input("enter any value:"))
print(x + y)           # If you enter 3 and 4, output is 7 (integer addition)
print(type(x + y))     # Output: <class 'int'>


# =============================================================================
# SECTION 4: Even/Odd Check Using Bitwise AND
# =============================================================================
#
# HOW IT WORKS:
# The least significant bit (LSB) of any binary number tells us if it's
# even or odd:
#   - Even numbers end in 0:  4 = 100, 6 = 110, 8 = 1000
#   - Odd numbers end in 1:   3 = 011, 5 = 101, 7 = 111
#
# So: number & 1 extracts just the last bit.
#   - If last bit is 0 --> even
#   - If last bit is 1 --> odd
#
# EXAMPLE:
#   6 & 1 = 110 & 001 = 000 = 0 --> even
#   7 & 1 = 111 & 001 = 001 = 1 --> odd
#
# This is slightly faster than using %, but the real value is understanding
# how binary works.
#
# TIME COMPLEXITY: O(1)
# =============================================================================

### check a number is even or odd using bitwise operator
number = int(input("enter any number:"))

# Version 1: Using two separate if statements (works but inefficient --
# the second condition is checked even if the first was True)
if (number & 1) == 0:
    print("even")
if (number & 1) != 0:
    print("odd")

### the same problem we can solve using else - it will reduce unnecessary conditions
# Version 2: Using if/else (better -- only one check needed)
if (number & 1) == 0:
    print("even")
else:
    print("odd")


# =============================================================================
# SECTION 5: Point Inside/On/Outside a Circle
# =============================================================================
#
# PROBLEM:
# Given a circle centered at the origin (0,0) with radius r, and a point
# (x, y), determine if the point lies INSIDE, ON, or OUTSIDE the circle.
#
# MATH / GEOMETRY:
# The equation of a circle centered at (cx, cy) with radius r is:
#     (x - cx)^2 + (y - cy)^2 = r^2
#
# We compute the distance from the center to the point:
#     distance = sqrt((x - cx)^2 + (y - cy)^2)
#
# Then compare:
#     distance == r  -->  ON the circle
#     distance < r   -->  INSIDE the circle
#     distance > r   -->  OUTSIDE the circle
#
# DIAGRAM (circle centered at origin, radius = 5):
#
#           y
#           |        * (3,4) distance = 5 --> ON the circle
#       5 --+------*-----
#           |    / | \
#       4 --+--*  |  \     * (1,1) distance = 1.41 --> INSIDE
#           | /   |   \
#       3 --+/    |    \
#           |     |     \
#       ----+-----+------+---- x
#          -5     0      5
#
# NOTE: Using **0.5 to compute square root is the same as math.sqrt()
# but avoids importing the math module.
#
# POTENTIAL ISSUE: Floating-point comparison (distance == radius) can be
# unreliable. For production code, use: abs(distance - radius) < epsilon
#
# IF / ELIF / ELSE AS A DECISION TREE:
# -------------------------------------
#                  [ radius == distance ? ]
#                    /yes            \no
#               "on circle"   [ radius > distance ? ]
#                                /yes            \no
#                          "inside circle"   "outside circle"
#
#   Only ONE branch ever runs. Python checks conditions top to bottom and
#   stops at the first True one -- the rest are skipped entirely.
#
# TIME COMPLEXITY: O(1)
# SPACE COMPLEXITY: O(1)
# =============================================================================

## point (x,y) and radius "r" is given.
## write a program to Check whether the point lies inside, on or outside the circle

## compute the distance from the center to the point. If the distance is equal to r, then on the circle

radius = int(input("enter the radius of a circle:"))
x_cor = int(input("enter x_coordinates of a point"))
y_cor = int(input("enter y_coordinates of a point"))
c_x = 0  # center x-coordinate (origin)
c_y = 0  # center y-coordinate (origin)

# Distance formula: sqrt((y2-y1)^2 + (x2-x1)^2)
distance = (((y_cor - c_y) ** 2) + ((x_cor - c_x) ** 2)) ** 0.5

if radius == distance:
    print("point is on the circle")
elif radius > distance:
    print("point is inside the circle")
else:
    print("point is outside the circle")


#### TASK 1 #### WAP to check whether the two vectors are collinear

# =============================================================================
# SECTION 6: XOR Swap Trick (Swapping Without a Temporary Variable)
# =============================================================================
#
# PROBLEM: Swap two numbers without using a third (temporary) variable.
#
# THE XOR TRICK:
# Three XOR operations swap two values. Here's WHY it works:
#
# KEY PROPERTIES OF XOR (^):
#   1. a ^ a = 0        (any number XOR itself is 0)
#   2. a ^ 0 = a        (any number XOR 0 is itself)
#   3. XOR is commutative and associative: a ^ b = b ^ a
#
# STEP-BY-STEP WALKTHROUGH with a=5, b=6:
#
#   Initial: a = 5 (binary: 101), b = 6 (binary: 110)
#
#   Step 1: a = a ^ b
#           a = 5 ^ 6 = 101 ^ 110 = 011 = 3
#           Now: a = 3, b = 6
#
#   Step 2: b = a ^ b
#           b = 3 ^ 6 = 011 ^ 110 = 101 = 5
#           Now: a = 3, b = 5    <-- b now has the original value of a!
#
#   Step 3: a = a ^ b
#           a = 3 ^ 5 = 011 ^ 101 = 110 = 6
#           Now: a = 6, b = 5    <-- a now has the original value of b!
#
# WHY IT WORKS (algebraically):
#   After step 1: a = a ^ b
#   After step 2: b = (a ^ b) ^ b = a ^ (b ^ b) = a ^ 0 = a  (original a!)
#   After step 3: a = (a ^ b) ^ a = (a ^ a) ^ b = 0 ^ b = b  (original b!)
#
# NOTE: In Python, you can simply do: a, b = b, a
# The XOR trick is mainly for learning bitwise operations. It's also useful in
# languages without tuple unpacking (like C) or in embedded systems where
# memory is extremely limited.
#
# TIME COMPLEXITY: O(1)
# SPACE COMPLEXITY: O(1) -- no extra variable needed!
# =============================================================================

### TASK 2 - perform swapping by bitwise operators. ##
# input: a= 5, b = 6 after swapping a = 6, b = 5 --> perform using bitwise operator (hint XOR)
## hack: if you perform 3 XOR operations of bitwise operators, you get numbers swapped

a = int(input("enter first number:"))
b = int(input("enter second number:"))

a = a ^ b   # a now holds XOR of both values
b = a ^ b   # b now holds original a
a = a ^ b   # a now holds original b

print(a, b)  # Values are swapped!
