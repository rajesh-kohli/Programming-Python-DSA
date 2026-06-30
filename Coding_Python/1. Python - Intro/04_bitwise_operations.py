# ============================================================================
# 06_bitwise_operations.py — Comprehensive Bitwise Operations Tutorial
# ============================================================================
# Covers: binary system, all 6 operators, bit manipulation tricks,
#         counting set bits, power-of-2 check, XOR unique-number,
#         compound assignment, and interview practice problems.
# ============================================================================


# ===== SECTION 1: What Are Bitwise Operations & Why Do They Matter? ==========

# --- Binary number system refresher ---
# Computers store everything as bits (0s and 1s).
# Each bit position represents a power of 2, reading right to left:
#
#   Position:   7    6    5    4    3    2    1    0
#   Value:    128   64   32   16    8    4    2    1
#
# To convert decimal 25 to binary:
#   25 = 16 + 8 + 1 = 2^4 + 2^3 + 2^0 = 11001
#
# To convert decimal 19 to binary:
#   19 = 16 + 2 + 1 = 2^4 + 2^1 + 2^0 = 10011

print("=" * 60)
print("SECTION 1: Binary Number System Refresher")
print("=" * 60)

# Python's bin() function shows binary representation (prefixed with '0b')
for num in [0, 1, 5, 10, 19, 25, 255]:
    print(f"  {num:>3} in binary = {bin(num):>12}  =  {num:08b}")

# --- Why bitwise ops are faster than arithmetic ---
# Bitwise operations map DIRECTLY to CPU instructions (single clock cycle).
# Arithmetic like multiplication/division involves multiple cycles.
# Example: n << 1 (one cycle) vs n * 2 (may take several cycles).
#
# --- Where bitwise ops are used in the real world ---
# 1. Permissions & flags  : Linux file permissions (rwx = 111 = 7)
# 2. Feature flags        : enable/disable features with single bits
# 3. Compression          : Huffman coding manipulates individual bits
# 4. Cryptography         : XOR is fundamental to many ciphers
# 5. Networking           : subnet masks use AND to determine network address
# 6. Graphics             : pixel color channels (RGBA packed into 32 bits)
# 7. DSA interviews       : tons of problems rely on bit tricks


# ===== SECTION 2: The 6 Bitwise Operators ====================================

print("\n" + "=" * 60)
print("SECTION 2: The 6 Bitwise Operators")
print("=" * 60)

a = 25  # binary: 11001
b = 19  # binary: 10011

# --- 2.1 AND (&) : both bits must be 1 ---
# Use case: masking — extract specific bits, check if a bit is set
#
#   25 = 1 1 0 0 1
#   19 = 1 0 0 1 1
#   ----------------
#    &   1 0 0 0 1  = 17

print(f"\n--- AND (&) ---")
print(f"  {a} & {b} = {a & b}")
print(f"  {a:05b}")
print(f"  {b:05b}")
print(f"  -----")
print(f"  {a & b:05b} = {a & b}")

# --- 2.2 OR (|) : at least one bit is 1 ---
# Use case: setting bits, combining flags
#
#   25 = 1 1 0 0 1
#   19 = 1 0 0 1 1
#   ----------------
#    |   1 1 0 1 1  = 27

print(f"\n--- OR (|) ---")
print(f"  {a} | {b} = {a | b}")
print(f"  {a:05b}")
print(f"  {b:05b}")
print(f"  -----")
print(f"  {a | b:05b} = {a | b}")

# --- 2.3 XOR (^) : exactly one bit is 1 ---
# Use case: toggling bits, finding unique elements, swapping variables
#
#   25 = 1 1 0 0 1
#   19 = 1 0 0 1 1
#   ----------------
#    ^   0 1 0 1 0  = 10

print(f"\n--- XOR (^) ---")
print(f"  {a} ^ {b} = {a ^ b}")
print(f"  {a:05b}")
print(f"  {b:05b}")
print(f"  -----")
print(f"  {a ^ b:05b} = {a ^ b}")

# ----- AND / OR / XOR side-by-side truth table (per bit column) -----
#   bit:    1  1  0  0  1   (25)
#   bit:    1  0  0  1  1   (19)
#   --------------------------
#   AND:    1  0  0  0  1   (17)  both must be 1
#   OR:     1  1  0  1  1   (27)  at least one is 1
#   XOR:    0  1  0  1  0   (10)  exactly one is 1 (i.e. they differ)

# --- 2.4 NOT (~) : flip all bits ---
# Python uses two's complement for negative numbers.
# For any integer n:  ~n = -(n + 1)
#
# Why? In two's complement with infinite precision:
#   ~0 = ...1111 1111 = -1
#   ~1 = ...1111 1110 = -2
#   ~5 = ...1111 1010 = -6
#
# Formula: ~n = -(n + 1)  because  n + ~n = all 1s = -1
#
# ----- Mental model: NOT flips every bit, even the "invisible" leading ones -----
#   5  = ...0000 0101
#   ~5 = ...1111 1010  = -6
#   Since Python ints are conceptually infinite-precision, flipping bit-by-bit
#   on a finite display can't show it directly — that's why we reason about it
#   via the formula -(n+1) instead of printing a fixed-width flipped pattern.

print(f"\n--- NOT (~) ---")
print(f"  ~0 = {~0}    (all bits flipped: -(0+1) = -1)")
print(f"  ~1 = {~1}    (-(1+1) = -2)")
print(f"  ~5 = {~5}    (-(5+1) = -6)")
print(f"  ~{a} = {~a}   (-({a}+1) = -{a+1})")

# --- 2.5 Left Shift (<<) : multiply by 2^k ---
# Each left shift pushes bits left, filling with 0 on the right.
# Equivalent to multiplying by 2^k.
#
#   1 << 1 = 10    = 2     (1 * 2^1)
#   1 << 2 = 100   = 4     (1 * 2^2)
#   1 << 3 = 1000  = 8     (1 * 2^3)
#   5 << 2 = 10100 = 20    (5 * 2^2)
#
# ----- Bit-pattern shift diagram: 5 << 2 -----
#   5      =     1 0 1
#   5 << 1 =   1 0 1 0     (shift left, fill new rightmost slot with 0)
#   5 << 2 = 1 0 1 0 0     (shift left again, another 0 fills in)
#   Every bit slides left by k positions; k zeros are appended on the right.

print(f"\n--- Left Shift (<<) ---")
for k in range(1, 4):
    result = 1 << k
    print(f"  1 << {k} = {result:>4}    (binary: {result:08b})")
print(f"  5 << 2 = {5 << 2:>4}    (binary: {5 << 2:08b})  -> 5 * 4 = 20")

# --- 2.6 Right Shift (>>) : divide by 2^k (floor division) ---
# Each right shift pushes bits right, discarding the rightmost bit.
# Equivalent to floor division by 2^k.
#
#   8 >> 1 = 100  = 4    (8 // 2^1)
#   8 >> 2 = 10   = 2    (8 // 2^2)
#   8 >> 3 = 1    = 1    (8 // 2^3)
#   7 >> 1 = 11   = 3    (7 // 2 = 3, remainder lost)
#
# ----- Bit-pattern shift diagram: 8 >> 2 -----
#   8      = 1 0 0 0
#   8 >> 1 =   1 0 0 0  -- drop rightmost bit -->   1 0 0
#   8 >> 2 =     1 0 0  -- drop rightmost bit -->     1 0
#   Every bit slides right by k positions; the k rightmost bits fall off
#   and are discarded (lost), and 0s fill in on the left.

print(f"\n--- Right Shift (>>) ---")
for k in range(1, 4):
    result = 8 >> k
    print(f"  8 >> {k} = {result:>4}    (binary: {result:08b})")
print(f"  7 >> 1 = {7 >> 1:>4}    (binary: {7 >> 1:08b})  -> 7 // 2 = 3 (floor)")


# ===== SECTION 3: Even/Odd Check with Bitwise (n & 1) ========================

print("\n" + "=" * 60)
print("SECTION 3: Even/Odd Check with Bitwise")
print("=" * 60)

# The Least Significant Bit (LSB, bit 0) determines parity:
#   - If LSB = 1, number is ODD    (ends in 1 in binary)
#   - If LSB = 0, number is EVEN   (ends in 0 in binary)
#
#   7 = 111  -> LSB = 1 -> odd
#   8 = 1000 -> LSB = 0 -> even
#
# So: n & 1 extracts the LSB.
#   n & 1 == 1  ->  odd
#   n & 1 == 0  ->  even
#
# This is FASTER than n % 2 because & is a single CPU instruction,
# while % involves division.

def is_even_bitwise(n):
    return (n & 1) == 0

def is_even_modulo(n):
    return n % 2 == 0

test_nums = [0, 1, 7, 8, 42, 99]
for n in test_nums:
    parity = "even" if is_even_bitwise(n) else "odd"
    print(f"  {n:>3} = {n:08b}  ->  LSB = {n & 1}  ->  {parity}")


# ===== SECTION 4: Bit Manipulation Tricks (Interview Gold) ====================

print("\n" + "=" * 60)
print("SECTION 4: Bit Manipulation Tricks")
print("=" * 60)

# Throughout this section, k is 0-indexed from the right (LSB = position 0).

n = 21  # binary: 10101
k = 1   # target bit position 1

print(f"  Working number: n = {n} = {n:08b}")
print(f"  Target bit position: k = {k}\n")

# --- 4.1 Set the kth bit: n | (1 << k) ---
# Forces bit k to 1, leaving all other bits unchanged.
# 1 << k creates a mask with ONLY bit k set.
# OR with that mask sets bit k.
#
#   n    = 0 0 0 1 0 1 0 1  (21)
#   mask = 0 0 0 0 0 0 1 0  (1 << 1 = 2)
#   -------------------------
#   OR     0 0 0 1 0 1 1 1  = 23

mask = 1 << k
result = n | mask
print(f"--- Set bit {k} ---")
print(f"  n    = {n:08b}  ({n})")
print(f"  mask = {mask:08b}  (1 << {k} = {mask})")
print(f"  n|m  = {result:08b}  ({result})")

# --- 4.2 Clear the kth bit: n & ~(1 << k) ---
# Forces bit k to 0, leaving all other bits unchanged.
# ~(1 << k) creates a mask with ALL bits set EXCEPT bit k.
# AND with that mask clears bit k.
#
#   n     = 0 0 0 1 0 1 0 1  (21)
#   1<<k  = 0 0 0 0 0 1 0 0  (1 << 2 = 4)
#  ~(1<<k)= 1 1 1 1 1 0 1 1  (inverted)
#   -------------------------
#   AND    = 0 0 0 1 0 0 0 1  = 17

k2 = 2
mask_clear = ~(1 << k2)
result_clear = n & mask_clear
print(f"\n--- Clear bit {k2} ---")
print(f"  n       = {n:08b}  ({n})")
print(f"  1<<{k2}   = {1 << k2:08b}")
print(f"  ~(1<<{k2}) = (all bits flipped)")
print(f"  n & m   = {result_clear:08b}  ({result_clear})")

# --- 4.3 Check the kth bit: (n >> k) & 1 ---
# Shifts the kth bit to position 0, then AND with 1 to isolate it.
# Returns 1 if set, 0 if not.
#
#   n      = 0 0 0 1 0 1 0 1  (21)
#   n >> 2 = 0 0 0 0 0 1 0 1  (shift right by 2)
#   & 1    =                1  -> bit 2 is SET
#
#   n >> 1 = 0 0 0 0 1 0 1 0  (shift right by 1)
#   & 1    =                0  -> bit 1 is NOT set

print(f"\n--- Check kth bit ---")
for ki in range(5):
    bit_val = (n >> ki) & 1
    status = "SET" if bit_val else "NOT set"
    print(f"  bit {ki} of {n} ({n:08b}):  (n >> {ki}) & 1 = {bit_val}  ->  {status}")

# --- 4.4 Flip (toggle) the kth bit: n ^ (1 << k) ---
# XOR with 1 flips a bit: 0^1=1, 1^1=0.
# XOR with 0 keeps a bit: 0^0=0, 1^0=1.
# So XOR with (1 << k) flips ONLY bit k.
#
#   n    = 0 0 0 1 0 1 0 1  (21)
#   mask = 0 0 0 0 0 1 0 0  (1 << 2 = 4)
#   -------------------------
#   XOR    0 0 0 1 0 0 0 1  = 17  (bit 2 was 1, now 0)

k3 = 2
mask_flip = 1 << k3
result_flip = n ^ mask_flip
print(f"\n--- Flip bit {k3} ---")
print(f"  n    = {n:08b}  ({n})")
print(f"  mask = {mask_flip:08b}  (1 << {k3} = {mask_flip})")
print(f"  n^m  = {result_flip:08b}  ({result_flip})")
# Flip it again to show toggling back:
print(f"  flip again: {result_flip} ^ {mask_flip} = {result_flip ^ mask_flip}  (back to {n})")


# ===== SECTION 5: Count Set Bits (Popcount) ===================================

print("\n" + "=" * 60)
print("SECTION 5: Count Set Bits — Two Methods")
print("=" * 60)

# --- Method 1: Loop with n & 1 and right shift ---
# Check the last bit (n & 1), add it to count, then shift right.
# Repeat until n becomes 0.
#
# Time complexity: O(log n)
# WHY? A number n has ceil(log2(n+1)) bits. We iterate once per bit.
#       For n = 25 = 11001, that's 5 bits = ceil(log2(26)) = 5 iterations.
# Space complexity: O(1) — only a counter variable.

def count_set_bits_loop(n):
    """Count set bits by checking each bit position. O(log n) time."""
    count = 0
    while n != 0:
        count += (n & 1)   # add the last bit (0 or 1)
        n >>= 1            # shift right to check next bit
    return count

print(f"\n--- Method 1: Loop + Right Shift  [O(log n)] ---")
for num in [0, 1, 7, 25, 255]:
    print(f"  {num:>3} = {num:08b}  ->  set bits = {count_set_bits_loop(num)}")

# --- Method 2: Brian Kernighan's Algorithm: n & (n-1) ---
# Key insight: n & (n-1) removes the RIGHTMOST set bit of n.
#
# WHY does n & (n-1) remove the rightmost set bit?
# When you subtract 1 from n, all bits from the rightmost set bit onward flip:
#   n   = 1 0 1 0 0  (20)
#   n-1 = 1 0 0 1 1  (19)   <- rightmost '1' and everything right of it flipped
#   n & (n-1) = 1 0 0 0 0  (16)  <- rightmost set bit is GONE
#
# Another example:
#   n   = 0 1 1 0 0  (12)
#   n-1 = 0 1 0 1 1  (11)
#   n & (n-1) = 0 1 0 0 0  (8)   <- rightmost set bit removed
#
# Time complexity: O(k) where k = number of set bits
# WHY? Each iteration removes exactly one set bit, so we loop k times.
#       For n = 25 = 11001 (3 set bits), only 3 iterations — vs 5 for Method 1.
#       Best case: O(1) for powers of 2. Worst case: O(log n) for all bits set.
# Space complexity: O(1)

def count_set_bits_kernighan(n):
    """Brian Kernighan's algorithm. O(k) where k = number of set bits."""
    count = 0
    while n != 0:
        n = n & (n - 1)    # remove the rightmost set bit
        count += 1
    return count

print(f"\n--- Method 2: Brian Kernighan's  [O(set bits)] ---")
for num in [0, 1, 7, 25, 255]:
    print(f"  {num:>3} = {num:08b}  ->  set bits = {count_set_bits_kernighan(num)}")

# Step-by-step walkthrough for n = 25 (11001):
print(f"\n  Walkthrough for n = 25:")
n_walk = 25
step = 0
while n_walk != 0:
    old = n_walk
    n_walk = n_walk & (n_walk - 1)
    step += 1
    print(f"    Step {step}: {old:08b} & {old - 1:08b} = {n_walk:08b}")
print(f"    n is 0 -> done. Total set bits = {step}")

# Python built-in: int.bit_count() (Python 3.10+)
print(f"\n  Python built-in: (25).bit_count() = {(25).bit_count()}")


# ===== SECTION 6: Check if Power of 2 =========================================

print("\n" + "=" * 60)
print("SECTION 6: Check if Power of 2 — n & (n-1) == 0")
print("=" * 60)

# A power of 2 has EXACTLY one set bit:
#   1   = 00000001
#   2   = 00000010
#   4   = 00000100
#   8   = 00001000
#   16  = 00010000
#
# So n & (n-1) removes that single set bit, leaving 0.
# For non-powers-of-2, at least one bit survives.
#
#   n = 16 = 10000
#   n-1=15 = 01111
#   n&(n-1)= 00000  ->  0  ->  IS power of 2
#
#   n = 20 = 10100
#   n-1=19 = 10011
#   n&(n-1)= 10000  -> 16  ->  NOT power of 2
#
# Edge case: n must be > 0 (0 is NOT a power of 2, but 0 & (-1) = 0).
#
# Time complexity: O(1) — single bitwise AND + comparison.

def is_power_of_2(n):
    """Check if n is a power of 2. O(1) time."""
    return n > 0 and (n & (n - 1)) == 0

print()
for num in [0, 1, 2, 3, 4, 8, 16, 20, 64, 100]:
    result = is_power_of_2(num)
    marker = "YES" if result else "no"
    print(f"  {num:>4} = {num:08b}  ->  power of 2?  {marker}")


# ===== SECTION 7: Find Unique Number Using XOR ================================

print("\n" + "=" * 60)
print("SECTION 7: Find Unique Number Using XOR")
print("=" * 60)

# --- XOR properties (memorize these!) ---
# 1. a ^ a = 0     (any number XOR itself is 0)
# 2. a ^ 0 = a     (any number XOR 0 is itself)
# 3. Commutative:   a ^ b = b ^ a
# 4. Associative:   (a ^ b) ^ c = a ^ (b ^ c)
#
# --- The problem ---
# Given an array where every element appears TWICE except one,
# find the unique element.
#
# Brute force: nested loops O(n^2) or hash map O(n) space.
# XOR trick: XOR all elements. Pairs cancel (a^a=0), unique remains.
#
# Time complexity: O(n) — single pass through the array.
# Space complexity: O(1) — just one variable.
#
# [INTERVIEW] This is a CLASSIC interview question (LeetCode #136).

def find_unique(arr):
    """Find the element that appears exactly once. O(n) time, O(1) space."""
    result = 0
    for x in arr:
        result ^= x
    return result

arr = [3, 5, 3, 7, 5]
print(f"\n  Array: {arr}")
print(f"  Unique element: {find_unique(arr)}")

# Step-by-step walkthrough:
print(f"\n  Step-by-step XOR walkthrough:")
result = 0
for i, x in enumerate(arr):
    old = result
    result ^= x
    print(f"    {old:08b} ^ {x:08b} ({x}) = {result:08b} ({result})")
print(f"  Answer: {result}")

# Another example with larger array
arr2 = [2, 4, 6, 4, 2, 8, 6]
print(f"\n  Array: {arr2}")
print(f"  Unique element: {find_unique(arr2)}")


# ===== SECTION 8: Compound Assignment Operators ===============================

print("\n" + "=" * 60)
print("SECTION 8: Compound Assignment Operators")
print("=" * 60)

# Just like += and *=, Python supports bitwise compound assignments:
#   &=    a &= b   is   a = a & b
#   |=    a |= b   is   a = a | b
#   ^=    a ^= b   is   a = a ^ b
#   <<=   a <<= k  is   a = a << k
#   >>=   a >>= k  is   a = a >> k
#
# NOTE: The RHS is evaluated as a full expression first.
#   a *= b - 1  means  a = a * (b - 1),  NOT  a = (a * b) - 1

a = 0b11001  # 25
print(f"\n  Initial a = {a} ({a:08b})")

a_and = a; a_and &= 0b10011   # 19
print(f"  a &= 19  ->  {a_and:08b} ({a_and})")

a_or = a; a_or |= 0b10011
print(f"  a |= 19  ->  {a_or:08b} ({a_or})")

a_xor = a; a_xor ^= 0b10011
print(f"  a ^= 19  ->  {a_xor:08b} ({a_xor})")

a_ls = a; a_ls <<= 2
print(f"  a <<= 2  ->  {a_ls:08b} ({a_ls})")

a_rs = a; a_rs >>= 2
print(f"  a >>= 2  ->  {a_rs:08b} ({a_rs})")

# Compound assignment precedence demonstration
a = 10; b = 20
a *= b - 1   # a = a * (b - 1) = 10 * 19 = 190, NOT (10 * 20) - 1
print(f"\n  a=10, b=20:  a *= b - 1  ->  a = 10 * (20-1) = {a}")


# ===== SECTION 9: Practice Exercises ==========================================

print("\n" + "=" * 60)
print("SECTION 9: Practice Exercises with Solutions")
print("=" * 60)

# --- Exercise 1: Swap two numbers without a temp variable (XOR swap) ---
# a ^= b  ->  a now holds a^b
# b ^= a  ->  b = b ^ (a^b) = a  (b cancels out)
# a ^= b  ->  a = (a^b) ^ a = b  (a cancels out)
#
# [INTERVIEW] Classic question. Works because XOR is its own inverse.
#
# ----- Mental model: each step "hides" one value inside the other -----
#   x=42      y=99
#   x^=y  -->  x=42^99        y=99            (x now holds the combined diff)
#   y^=x  -->  x=42^99        y=99^(42^99)=42 (y recovers original x)
#   x^=y  -->  x=(42^99)^42=99  y=42           (x recovers original y)
#   No temp variable needed because XOR-ing twice with the same value cancels it.

print("\n--- Ex 1: XOR Swap ---")
x, y = 42, 99
print(f"  Before: x={x}, y={y}")
x ^= y   # x = x ^ y
y ^= x   # y = y ^ (x ^ y) = x
x ^= y   # x = (x ^ y) ^ x = y
print(f"  After:  x={x}, y={y}")

# Walkthrough:
x, y = 42, 99
print(f"\n  Walkthrough (x=42, y=99):")
x ^= y; print(f"    x ^= y  ->  x = {x:08b} ({x})")
y ^= x; print(f"    y ^= x  ->  y = {y:08b} ({y})")
x ^= y; print(f"    x ^= y  ->  x = {x:08b} ({x})")


# --- Exercise 2: Check if two numbers have opposite signs ---
# XOR of two numbers with opposite signs will have MSB = 1 (negative result).
# XOR of same-sign numbers will have MSB = 0 (positive result).
# So: (a ^ b) < 0 means opposite signs.
#
# Time: O(1)  Space: O(1)

print("\n--- Ex 2: Opposite Signs ---")

def have_opposite_signs(a, b):
    return (a ^ b) < 0

test_pairs = [(5, -3), (-5, -3), (5, 3), (0, -1)]
for a, b in test_pairs:
    result = have_opposite_signs(a, b)
    print(f"  ({a:>3}, {b:>3})  ->  opposite signs? {result}")


# --- Exercise 3: Find two non-repeating elements ---
# All elements appear twice except TWO unique elements. Find both.
#
# Step 1: XOR all elements -> xor_all = unique1 ^ unique2
# Step 2: Find any set bit in xor_all (this bit differs between the two)
#         Use xor_all & (-xor_all) to isolate the rightmost set bit.
# Step 3: Partition elements into two groups based on that bit,
#          XOR within each group to find each unique element.
#
# Time: O(n)  Space: O(1)
# [INTERVIEW] This is LeetCode #260 — harder variant of unique number.

print("\n--- Ex 3: Two Non-Repeating Elements ---")

def find_two_unique(arr):
    # Step 1: XOR all to get unique1 ^ unique2
    xor_all = 0
    for x in arr:
        xor_all ^= x

    # Step 2: Isolate rightmost set bit (this bit differs between the two)
    rightmost_set = xor_all & (-xor_all)

    # Step 3: Split into two groups and XOR within each
    group1 = 0
    group2 = 0
    for x in arr:
        if x & rightmost_set:
            group1 ^= x
        else:
            group2 ^= x

    return group1, group2

arr3 = [2, 3, 7, 9, 11, 2, 3, 11]
u1, u2 = find_two_unique(arr3)
print(f"  Array: {arr3}")
print(f"  Two unique elements: {u1} and {u2}")


# --- Exercise 4: Turn off the rightmost set bit ---
# We already know this: n & (n - 1)
# But let's make it a standalone function and verify.
#
# Time: O(1)  Space: O(1)

print("\n--- Ex 4: Turn Off Rightmost Set Bit ---")

def turn_off_rightmost_set_bit(n):
    return n & (n - 1)

for num in [12, 7, 16, 255]:
    result = turn_off_rightmost_set_bit(num)
    print(f"  {num:>3} = {num:08b}  ->  {result:08b} = {result}")


# --- Exercise 5: Multiply and divide by power of 2 using shifts ---
# n << k  =  n * 2^k     (left shift = multiply)
# n >> k  =  n // 2^k    (right shift = integer divide)
#
# These are faster than * and // because shifts are single CPU instructions.
# Time: O(1)  Space: O(1)
#
# CAUTION: right shift of negative numbers is implementation-defined in
# some languages, but Python always does arithmetic right shift (preserves sign).

print("\n--- Ex 5: Multiply/Divide by Powers of 2 ---")

n = 13
print(f"  n = {n}")
print(f"  n * 2   = n << 1 = {n << 1}")
print(f"  n * 4   = n << 2 = {n << 2}")
print(f"  n * 8   = n << 3 = {n << 3}")
print(f"  n // 2  = n >> 1 = {n >> 1}")
print(f"  n // 4  = n >> 2 = {n >> 2}")

# Practical example: compute n * 10 using shifts
# n * 10 = n * 8 + n * 2 = (n << 3) + (n << 1)
n = 7
result = (n << 3) + (n << 1)
print(f"\n  n * 10 using shifts: ({n} << 3) + ({n} << 1) = {n << 3} + {n << 1} = {result}")


# --- Exercise 6: Isolate the rightmost set bit ---
# n & (-n) gives a number with ONLY the rightmost set bit.
#
# Why? -n in two's complement is ~n + 1, which flips all bits then adds 1.
# This makes all bits right of the rightmost set bit become 0 again,
# and the rightmost set bit itself stays 1, while everything left differs.
# AND then isolates just that one bit.
#
#   n    = 0 1 0 1 0 0  (20)
#  -n    = 1 0 1 1 0 0  (two's complement)
#   n&-n = 0 0 0 1 0 0  (4)  <- rightmost set bit isolated!
#
# Time: O(1)  Space: O(1)

print("\n--- Ex 6: Isolate Rightmost Set Bit ---")

def isolate_rightmost_set_bit(n):
    return n & (-n)

for num in [12, 20, 7, 16, 255]:
    result = isolate_rightmost_set_bit(num)
    print(f"  {num:>3} = {num:08b}  ->  rightmost set bit = {result:08b} = {result}")


# ===== SECTION 10: Interview Quick Reference Table ============================

print("\n" + "=" * 60)
print("SECTION 10: Interview Quick Reference Table")
print("=" * 60)

print("""
  +--------------------------------------+---------------------+----------+
  | Operation                            | Expression          | Time     |
  +--------------------------------------+---------------------+----------+
  | Check if even                        | (n & 1) == 0        | O(1)     |
  | Check if odd                         | (n & 1) == 1        | O(1)     |
  | Multiply by 2^k                      | n << k              | O(1)     |
  | Divide by 2^k (floor)               | n >> k              | O(1)     |
  | Set kth bit                          | n | (1 << k)        | O(1)     |
  | Clear kth bit                        | n & ~(1 << k)       | O(1)     |
  | Check kth bit                        | (n >> k) & 1        | O(1)     |
  | Flip kth bit                         | n ^ (1 << k)        | O(1)     |
  | Turn off rightmost set bit           | n & (n - 1)         | O(1)     |
  | Isolate rightmost set bit            | n & (-n)            | O(1)     |
  | Check power of 2                     | n & (n-1) == 0      | O(1)     |
  | Count set bits (loop)               | loop: n & 1, n >>1  | O(log n) |
  | Count set bits (Kernighan)          | loop: n & (n-1)     | O(k)     |
  | Swap without temp                    | XOR swap            | O(1)     |
  | Find unique in pairs array           | XOR all elements    | O(n)     |
  | Opposite signs check                 | (a ^ b) < 0         | O(1)     |
  +--------------------------------------+---------------------+----------+

  XOR Properties:  a ^ a = 0  |  a ^ 0 = a  |  commutative  |  associative
  NOT Formula:     ~n = -(n + 1)
""")

print("=" * 60)
print("End of Bitwise Operations Tutorial")
print("=" * 60)
