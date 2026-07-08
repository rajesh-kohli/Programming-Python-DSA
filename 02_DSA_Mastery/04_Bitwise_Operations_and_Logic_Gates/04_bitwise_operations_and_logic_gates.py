###############################################################################
#               04 - Bitwise Operations and Logic Gates                       #
###############################################################################
#
# ALL single-expression bitwise operations are O(1) — one CPU instruction.
# This file mirrors your source (04_bitwise_operations.py, 698 lines) with
# Principal-level inline comments, complexity proofs, and practice skeletons.
#
# COMPLEXITY OVERVIEW:
#   Single bitwise expression:  O(1)   — 1 CPU ALU instruction, 1 clock cycle
#   Count set bits (shift):     O(log n) — iterates once per bit position
#   Count set bits (Kernighan): O(k)   — iterates once per SET bit (k ≤ log n)
#   Find unique (XOR):          O(n)   — single pass, O(1) space

from typing import List


# =============================================================================
# SECTION 1: Binary Number System Refresher
# =============================================================================
#
# Bit positions (right to left), each worth 2^position:
#
#   Position:   7    6    5    4    3    2    1    0
#   Value:    128   64   32   16    8    4    2    1
#
# To convert 25 to binary:
#   25 = 16 + 8 + 1 = 2^4 + 2^3 + 2^0 = 11001 in binary
#
# To convert 19 to binary:
#   19 = 16 + 2 + 1 = 2^4 + 2^1 + 2^0 = 10011 in binary
#
# Python formatting:
#   bin(25)       → '0b11001'   (with 0b prefix)
#   f"{25:08b}"   → '00011001'  (zero-padded 8-bit, no prefix — best for diagrams)

def binary_system_demo():
    """Formatted binary representation for common numbers."""
    print("=" * 60)
    print("SECTION 1: Binary Number System")
    print("=" * 60)
    for num in [0, 1, 5, 10, 19, 25, 255]:
        print(f"  {num:>3} in binary = {bin(num):>12}  =  {num:08b}")

# WHY BITWISE OPS ARE FASTER:
# Single CPU ALU instruction (one clock cycle) vs arithmetic which may use
# multiple cycles. Example: n << 1 is one shift instruction; n * 2 involves
# the multiplier unit which is slower.
#
# Real-world applications:
#   OS permissions : rwx = 111₂ = 7
#   Feature flags  : enable bit k → set bit k in a config int
#   Networking     : subnet mask — IP & mask extracts network address
#   Cryptography   : XOR is fundamental to stream ciphers
#   Graphics       : RGBA pixel packed as 4×8-bit channels in one 32-bit int


# =============================================================================
# SECTION 2: The 6 Bitwise Operators
# =============================================================================
#
# Worked with a = 25 (11001) and b = 19 (10011) throughout.

def six_operators_demo():
    """Demonstrate all 6 operators with column-aligned binary output."""
    a = 25  # 11001
    b = 19  # 10011
    print("\n" + "=" * 60)
    print("SECTION 2: The 6 Bitwise Operators")
    print("=" * 60)

    # --- 2.1 AND (&): both bits must be 1 ---
    # Use: masking, extracting specific bits, checking if a bit is set
    #
    #   25 = 1 1 0 0 1
    #   19 = 1 0 0 1 1
    #   ─────────────
    #    &  = 1 0 0 0 1 = 17
    print(f"\n--- AND (&): both bits must be 1 ---")
    print(f"  {a} = {a:05b}")
    print(f"  {b} = {b:05b}")
    print(f"  ─────")
    print(f"  {a & b} = {a & b:05b}   ({a} & {b} = {a & b})")

    # --- 2.2 OR (|): at least one bit is 1 ---
    # Use: setting bits, combining flags
    #
    #   25 = 1 1 0 0 1
    #   19 = 1 0 0 1 1
    #   ─────────────
    #    |  = 1 1 0 1 1 = 27
    print(f"\n--- OR (|): at least one bit is 1 ---")
    print(f"  {a} = {a:05b}")
    print(f"  {b} = {b:05b}")
    print(f"  ─────")
    print(f"  {a | b} = {a | b:05b}   ({a} | {b} = {a | b})")

    # --- 2.3 XOR (^): exactly one bit is 1 (bits differ) ---
    # Use: toggling bits, finding unique elements, swapping variables
    #
    #   25 = 1 1 0 0 1
    #   19 = 1 0 0 1 1
    #   ─────────────
    #    ^  = 0 1 0 1 0 = 10
    #
    # XOR PROPERTIES (memorize):
    #   a ^ a = 0   (anything XOR itself = 0)
    #   a ^ 0 = a   (anything XOR 0 = unchanged)
    #   Commutative: a ^ b = b ^ a
    #   Associative: (a ^ b) ^ c = a ^ (b ^ c)
    print(f"\n--- XOR (^): exactly one bit is 1 ---")
    print(f"  {a} = {a:05b}")
    print(f"  {b} = {b:05b}")
    print(f"  ─────")
    print(f"  {a ^ b} = {a ^ b:05b}   ({a} ^ {b} = {a ^ b})")
    print(f"  XOR props: a^a={a}^{a}={a^a}, a^0={a}^0={a^0}")

    # --- Side-by-side truth table ---
    #   Bit A | Bit B | A AND B | A OR B | A XOR B
    #   ──────|───────|─────────|────────|────────
    #     0   |   0   |    0    |   0    |    0
    #     0   |   1   |    0    |   1    |    1
    #     1   |   0   |    0    |   1    |    1
    #     1   |   1   |    1    |   1    |    0
    print(f"\n  Per-bit column comparison of 25 and 19:")
    print(f"    bit: 1 1 0 0 1  (25)")
    print(f"    bit: 1 0 0 1 1  (19)")
    print(f"    ─────────────────────")
    print(f"    AND: 1 0 0 0 1  (17) both must be 1")
    print(f"    OR:  1 1 0 1 1  (27) at least one is 1")
    print(f"    XOR: 0 1 0 1 0  (10) exactly one is 1")

    # --- 2.4 NOT (~): flip all bits ---
    # Python: ~n = -(n + 1)  (two's complement, infinite precision)
    #
    # WHY -(n+1)?
    #   Python ints are infinite precision. Flipping all bits (including
    #   the infinitely many leading 0s) gives the two's complement negative.
    #   n + ~n = all 1s = -1  →  ~n = -1 - n = -(n + 1)
    #
    # Mental model: in a fixed-width 8-bit world, ~5 = 0b11111010 = 250
    # In Python's infinite-precision world, ~5 = -6
    print(f"\n--- NOT (~): flip all bits ---")
    print(f"  ~0 = {~0}   (-(0+1) = -1)")
    print(f"  ~1 = {~1}   (-(1+1) = -2)")
    print(f"  ~5 = {~5}   (-(5+1) = -6)")
    print(f"  ~{a} = {~a}  (-({a}+1) = -{a+1})")

    # --- 2.5 Left Shift (<<): multiply by 2^k ---
    # Slides bits left, fills right with 0s.
    #
    # Bit-pattern diagram: 5 << 2
    #   5      =     1 0 1
    #   5 << 1 =   1 0 1 0    (shift left, new 0 fills right)
    #   5 << 2 = 1 0 1 0 0    (shift left again, another 0 fills in)
    #
    # Formula: n << k = n * 2^k
    print(f"\n--- Left Shift (<<): multiply by 2^k ---")
    for k in range(1, 4):
        print(f"  1 << {k} = {1 << k:>4}    ({1 << k:08b})  → 2^{k}")
    print(f"  5 << 2 = {5 << 2:>4}    ({5 << 2:08b})  → 5 × 4 = 20")

    # --- 2.6 Right Shift (>>): floor divide by 2^k ---
    # Slides bits right, rightmost bits fall off and are LOST (discarded).
    #
    # Bit-pattern diagram: 8 >> 2
    #   8      = 1 0 0 0
    #   8 >> 1 =   1 0 0  (rightmost bit dropped)
    #   8 >> 2 =     1 0  (another bit dropped)
    #
    # Formula: n >> k = n // 2^k (always FLOOR division — remainder discarded)
    print(f"\n--- Right Shift (>>): floor divide by 2^k ---")
    for k in range(1, 4):
        print(f"  8 >> {k} = {8 >> k:>4}    ({8 >> k:08b})")
    print(f"  7 >> 1 = {7 >> 1:>4}    ({7 >> 1:08b})  → 7 // 2 = 3 (floor, remainder lost)")


# =============================================================================
# SECTION 3: Even/Odd Check via LSB — O(1)
# =============================================================================
#
# The Least Significant Bit (LSB, position 0) determines parity:
#   LSB = 1 → number is ODD   (7 = 111, ends in 1)
#   LSB = 0 → number is EVEN  (8 = 1000, ends in 0)
#
# n & 1 extracts the LSB:
#   n & 1 == 1  → odd
#   n & 1 == 0  → even
#
# FASTER than n % 2 because & is a single ALU instruction vs. division.
#
# Time: O(1) | Space: O(1)

def is_odd_bitwise(n: int) -> bool:
    """Return True if n is odd. O(1)."""
    return (n & 1) == 1

def is_even_bitwise(n: int) -> bool:
    """Return True if n is even. O(1)."""
    return (n & 1) == 0

def even_odd_demo():
    """Show LSB parity table for a set of numbers."""
    print("\n" + "=" * 60)
    print("SECTION 3: Even/Odd via LSB  [O(1)]")
    print("=" * 60)
    for n in [0, 1, 7, 8, 42, 99]:
        parity = "odd" if is_odd_bitwise(n) else "even"
        print(f"  {n:>3} = {n:08b}  → LSB = {n & 1}  → {parity}")


# =============================================================================
# SECTION 4: The Four Bit Manipulation Idioms
# =============================================================================
#
# k is 0-indexed from the right (LSB = position 0).
# ALL operations are O(1) — a single expression, single CPU instruction.
#
# ┌─────────────────┬──────────────────────┬──────────────────────────────────┐
# │ Goal            │ Expression           │ How it works                     │
# ├─────────────────┼──────────────────────┼──────────────────────────────────┤
# │ Set bit k       │ n | (1 << k)         │ 1<<k has only bit k set. OR → 1 │
# │ Clear bit k     │ n & ~(1 << k)        │ ~(1<<k) is all 1s except bit k. │
# │                 │                      │ AND forces bit k to 0.           │
# │ Check bit k     │ (n >> k) & 1         │ Shift bit k to pos 0, AND w/ 1  │
# │ Flip bit k      │ n ^ (1 << k)         │ XOR w/ 1 flips; XOR w/ 0 keeps  │
# └─────────────────┴──────────────────────┴──────────────────────────────────┘

def set_bit(n: int, k: int) -> int:
    """
    Set the k-th bit of n to 1.
    Mask = 1 << k has ONLY bit k set.
    OR with that mask forces bit k to 1 regardless of its current value.

    n    = 0 0 0 1 0 1 0 1  (21)
    mask = 0 0 0 0 0 0 1 0  (1 << 1 = 2)
    ─────────────────────────────
    OR   = 0 0 0 1 0 1 1 1  (23)
    """
    return n | (1 << k)

def clear_bit(n: int, k: int) -> int:
    """
    Clear the k-th bit of n to 0.
    ~(1 << k) creates a mask with ALL bits set EXCEPT bit k.
    AND with that mask forces bit k to 0, leaving all others unchanged.

    n        = 0 0 0 1 0 1 0 1  (21)
    1 << 2   = 0 0 0 0 0 1 0 0  (4)
    ~(1 << 2)= 1 1 1 1 1 0 1 1  (all bits set except bit 2)
    ─────────────────────────────
    AND      = 0 0 0 1 0 0 0 1  (17)
    """
    return n & ~(1 << k)

def check_bit(n: int, k: int) -> int:
    """
    Check if the k-th bit of n is set. Returns 1 if set, 0 if not.
    Shift bit k to position 0, then AND with 1 to isolate it.

    n      = 0 0 0 1 0 1 0 1  (21)
    n >> 2 = 0 0 0 0 0 1 0 1  (shifted right by 2)
    & 1    =                1  → bit 2 IS set

    n >> 1 = 0 0 0 0 1 0 1 0
    & 1    =                0  → bit 1 is NOT set
    """
    return (n >> k) & 1

def flip_bit(n: int, k: int) -> int:
    """
    Toggle (flip) the k-th bit of n.
    XOR with 1 flips: 0 ^ 1 = 1, 1 ^ 1 = 0.
    XOR with 0 keeps: 0 ^ 0 = 0, 1 ^ 0 = 1.
    So XOR with (1 << k) flips ONLY bit k, leaves all others unchanged.

    n    = 0 0 0 1 0 1 0 1  (21)
    mask = 0 0 0 0 0 1 0 0  (1 << 2 = 4)
    ─────────────────────────────
    XOR  = 0 0 0 1 0 0 0 1  (17)  ← bit 2 flipped from 1 to 0
    """
    return n ^ (1 << k)

def bit_manipulation_demo():
    """Demonstrate all 4 idioms on n=21."""
    n = 21  # 00010101
    print("\n" + "=" * 60)
    print("SECTION 4: The 4 Bit Manipulation Idioms  [All O(1)]")
    print("=" * 60)
    print(f"\n  n = {n} = {n:08b}")

    print(f"\n  --- Set / Clear / Check / Flip (k=0-indexed from right) ---")
    for k in range(5):
        s = set_bit(n, k)
        c = clear_bit(n, k)
        ch = check_bit(n, k)
        f = flip_bit(n, k)
        print(f"  k={k}:  set={s:>3}({s:08b})  clear={c:>3}({c:08b})"
              f"  check={ch}  flip={f:>3}({f:08b})")

    print(f"\n  Flip-back verification (flip twice = no change):")
    k = 2
    flipped   = flip_bit(n, k)
    unflipped = flip_bit(flipped, k)
    print(f"  n={n}, flip bit {k} → {flipped}, flip again → {unflipped} (back to {n}) ✓")


# =============================================================================
# SECTION 5: Count Set Bits (Popcount / Hamming Weight)
# =============================================================================

def count_set_bits_shift(n: int) -> int:
    """
    Method 1: Check each bit position via right-shift loop.

    Algorithm:
      1. n & 1 extracts the LSB (0 or 1), add it to count.
      2. n >>= 1 shifts n right, bringing next bit to position 0.
      3. Repeat until n == 0.

    Time: O(log n) — a number n has floor(log2(n)) + 1 bits.
          We iterate ONCE PER BIT POSITION (not per set bit).
          For n=25=11001: 5 bit positions → 5 iterations.
    Space: O(1)
    """
    count = 0
    while n != 0:
        count += (n & 1)   # extract LSB: is it 1?
        n >>= 1            # shift right: bring next bit to LSB position
    return count

def count_set_bits_kernighan(n: int) -> int:
    """
    Method 2: Brian Kernighan's Algorithm.

    KEY INSIGHT: n & (n - 1) removes the RIGHTMOST set bit of n.

    WHY does n & (n-1) remove the rightmost set bit?
      When you subtract 1 from n, all bits from the rightmost set bit
      DOWNWARD (toward position 0) flip:
        n   = 1 0 1 0 0  (20)
        n-1 = 1 0 0 1 1  (19)  ← rightmost '1' and everything right flipped
        n & (n-1) = 1 0 0 0 0  ← rightmost set bit GONE

    We count iterations: each iteration removes exactly 1 set bit.

    Time: O(k) where k = number of set bits.
          For n=25=11001 (3 set bits): only 3 iterations vs 5 in Method 1.
          Best case: O(1) for powers of 2 (only 1 set bit).
          Worst case: O(log n) when all bits are set (e.g., n=255=11111111).
    Space: O(1)
    """
    count = 0
    while n != 0:
        n &= (n - 1)   # remove the rightmost set bit
        count += 1
    return count

def count_bits_demo():
    """Compare both methods and show Brian Kernighan walkthrough for n=25."""
    print("\n" + "=" * 60)
    print("SECTION 5: Count Set Bits")
    print("=" * 60)
    print(f"\n  Method 1 [O(log n) — iterates per bit position]:")
    for num in [0, 1, 7, 25, 255]:
        print(f"  {num:>3} = {num:08b}  → set bits = {count_set_bits_shift(num)}")

    print(f"\n  Method 2 [O(k) — Brian Kernighan, iterates per SET bit]:")
    for num in [0, 1, 7, 25, 255]:
        print(f"  {num:>3} = {num:08b}  → set bits = {count_set_bits_kernighan(num)}")

    print(f"\n  Brian Kernighan walkthrough for n = 25 (11001):")
    n_walk = 25
    step = 0
    while n_walk != 0:
        old = n_walk
        n_walk &= (n_walk - 1)
        step += 1
        print(f"    Step {step}: {old:08b} & {old-1:08b} = {n_walk:08b}  ({n_walk})")
    print(f"    n = 0 → done. Total set bits = {step}")

    # Python 3.10+ built-in:
    print(f"\n  Python 3.10+ built-in: (25).bit_count() = {(25).bit_count()}")


# =============================================================================
# SECTION 6: Is Power of 2? — O(1)
# =============================================================================
#
# Powers of 2 have EXACTLY ONE set bit:
#   1  = 00000001
#   2  = 00000010
#   4  = 00000100
#   8  = 00001000
#   16 = 00010000
#
# n & (n-1) removes the single set bit → result = 0.
# For non-powers: at least one bit survives → result ≠ 0.
#
#   n=16: 10000 & 01111 = 00000 → 0 → IS power of 2 ✅
#   n=20: 10100 & 10011 = 10000 → non-zero → NOT power of 2 ❌
#
# EDGE CASE: n=0 must be handled explicitly.
#   0 & (-1) = 0 → would pass the test! But 0 is NOT a power of 2.
#   Guard: n > 0 AND (n & (n-1)) == 0
#
# Time: O(1) | Space: O(1)

def is_power_of_2(n: int) -> bool:
    """Return True if n is a power of 2. O(1)."""
    return n > 0 and (n & (n - 1)) == 0

def power_of_2_demo():
    print("\n" + "=" * 60)
    print("SECTION 6: Is Power of 2?  [O(1)]")
    print("=" * 60)
    for num in [0, 1, 2, 3, 4, 8, 16, 20, 64, 100]:
        result = is_power_of_2(num)
        marker = "✅ YES" if result else "❌ no"
        print(f"  {num:>4} = {num:08b}  → {marker}")


# =============================================================================
# SECTION 7: Find Unique Number via XOR — O(n) time, O(1) space
# =============================================================================
#
# PROBLEM: Array where every element appears TWICE except one. Find it.
#
# NAIVE approaches:
#   Brute force: O(n^2) nested loops, O(1) space
#   Hash map:    O(n) time, O(n) space
#
# XOR TRICK: XOR all elements. Pairs cancel (a^a=0). Unique remains (0^x=x).
#   [3, 5, 3, 7, 5]
#   0 ^ 3 = 3
#   3 ^ 5 = 6
#   6 ^ 3 = 5
#   5 ^ 7 = 2
#   2 ^ 5 = 7   ← answer!
#
# Time: O(n) — single pass | Space: O(1) — just one variable

def find_unique(nums: List[int]) -> int:
    """XOR all elements; pairs cancel to 0, unique survives. O(n), O(1)."""
    result = 0
    for x in nums:
        result ^= x    # a^a=0, so duplicates cancel; 0^x=x, so unique remains
    return result

def find_unique_demo():
    print("\n" + "=" * 60)
    print("SECTION 7: Find Unique Number via XOR  [O(n), O(1) space]")
    print("=" * 60)
    arr = [3, 5, 3, 7, 5]
    print(f"\n  Array: {arr}")
    print(f"  Step-by-step XOR:")
    result = 0
    for x in arr:
        old = result
        result ^= x
        print(f"    {old:08b} ^ {x:08b} ({x}) = {result:08b} ({result})")
    print(f"  Answer: {result}")

    arr2 = [2, 4, 6, 4, 2, 8, 6]
    print(f"\n  Array: {arr2}")
    print(f"  Unique element: {find_unique(arr2)}")


# =============================================================================
# SECTION 8: Compound Assignment Operators
# =============================================================================
#
# Just like +=, *= — Python supports bitwise compound assignments:
#   &=    a &= b   →  a = a & b
#   |=    a |= b   →  a = a | b
#   ^=    a ^= b   →  a = a ^ b
#   <<=   a <<= k  →  a = a << k
#   >>=   a >>= k  →  a = a >> k
#
# PRECEDENCE: RHS is evaluated as a COMPLETE expression first.
#   a &= b - 1   means   a = a & (b - 1)   NOT   (a & b) - 1
#   a *= b - 1   means   a = a * (b - 1)   NOT   (a * b) - 1

def compound_assignment_demo():
    print("\n" + "=" * 60)
    print("SECTION 8: Compound Assignment Operators")
    print("=" * 60)
    a = 0b11001  # 25
    print(f"\n  Initial a = {a} ({a:08b})")

    a_and = a; a_and &= 0b10011  # 19
    print(f"  a &= 19  →  {a_and:08b}  ({a_and})")

    a_or = a;  a_or  |= 0b10011
    print(f"  a |= 19  →  {a_or:08b}   ({a_or})")

    a_xor = a; a_xor ^= 0b10011
    print(f"  a ^= 19  →  {a_xor:08b}  ({a_xor})")

    a_ls = a;  a_ls <<= 2
    print(f"  a <<= 2  →  {a_ls:08b} ({a_ls})")

    a_rs = a;  a_rs >>= 2
    print(f"  a >>= 2  →  {a_rs:08b}  ({a_rs})")

    # Precedence demo
    a2 = 10; b = 20
    a2 *= b - 1   # = 10 * (20-1) = 190, NOT (10*20)-1 = 199
    print(f"\n  a=10, b=20: a *= b-1  →  a = 10 × (20-1) = {a2}  (RHS evaluated first)")


# =============================================================================
# SECTION 9: Advanced Tricks and Interview Problems
# =============================================================================

# --- 9.1 XOR Swap (no temp variable) ---
# a ^= b  →  a = a ^ b             (a "stores" the diff of both values)
# b ^= a  →  b = (a^b) ^ b = a    (b recovers original a, because b^b=0)
# a ^= b  →  a = (a^b) ^ a = b    (a recovers original b, because a^a=0)
#
# Mental model:
#   x=42, y=99
#   x^=y  →  x = 42^99 (combined),    y = 99
#   y^=x  →  x = 42^99,               y = 99 ^ (42^99) = 42  ← y gets original x
#   x^=y  →  x = (42^99) ^ 42 = 99,   y = 42               ← x gets original y
#
# Time: O(1) | Space: O(1) | [CLASSIC INTERVIEW QUESTION]

def xor_swap(x: int, y: int):
    """Swap two integers using XOR — no temp variable."""
    print(f"\n--- 9.1 XOR Swap ---")
    print(f"  Before: x={x}, y={y}")
    x ^= y
    y ^= x
    x ^= y
    print(f"  After:  x={x}, y={y}")
    return x, y

# --- 9.2 Opposite Signs Check ---
# The MSB (sign bit) is 1 for negative numbers.
# XOR of two numbers with opposite signs: MSB will be 1 → result < 0.
# XOR of same-sign numbers: MSB will be 0 → result ≥ 0.
# So: (a ^ b) < 0 means they have opposite signs.
#
# Time: O(1) | Space: O(1)

def have_opposite_signs(a: int, b: int) -> bool:
    """Return True if a and b have opposite signs. O(1)."""
    return (a ^ b) < 0  # MSB of XOR is 1 only when sign bits differ

# --- 9.3 Two Non-Repeating Elements (LeetCode 260) ---
# All elements appear TWICE except TWO. Find both.
#
# Step 1: XOR all → xor_all = u1 ^ u2 (since pairs cancel)
# Step 2: u1 ≠ u2, so xor_all ≠ 0. At least one bit differs between them.
#         Find the RIGHTMOST set bit: xor_all & (-xor_all)
#         (This bit is set in u1 but not u2, or vice versa.)
# Step 3: Partition array into two groups by whether that bit is set.
#         XOR within each group. Duplicates cancel, leaving each unique element.
#
# Time: O(n) | Space: O(1) | [INTERVIEW: harder XOR variant]

def find_two_unique(nums: List[int]):
    """Find two elements that appear exactly once. O(n) time, O(1) space."""
    # Step 1: XOR all → get u1 ^ u2
    xor_all = 0
    for x in nums:
        xor_all ^= x

    # Step 2: isolate rightmost set bit (differs between u1 and u2)
    # n & (-n) gives a number with ONLY the rightmost set bit of n.
    # Why? -n = ~n + 1 (two's complement). All bits right of the rightmost
    # set bit become 0 again, and the rightmost set bit itself stays 1.
    rightmost = xor_all & (-xor_all)

    # Step 3: partition and XOR within each group
    u1, u2 = 0, 0
    for x in nums:
        if x & rightmost:
            u1 ^= x    # group where rightmost bit is set
        else:
            u2 ^= x    # group where rightmost bit is NOT set
    return u1, u2

# --- 9.4 Turn off rightmost set bit ---
# n & (n - 1) — already used in Kernighan, also useful standalone.
# Time: O(1)

def turn_off_rightmost_set_bit(n: int) -> int:
    return n & (n - 1)

# --- 9.5 Isolate rightmost set bit ---
# n & (-n) returns a number with ONLY the rightmost set bit of n.
# Used in Step 2 of find_two_unique above.
# Time: O(1)
#
# Derivation: -n in two's complement = ~n + 1
#   n    = 0 1 0 1 0 0  (20)
#   ~n   = 1 0 1 0 1 1
#   ~n+1 = 1 0 1 1 0 0  (-n)
#   n&-n = 0 0 0 1 0 0  (4) ← only rightmost set bit survives

def isolate_rightmost_set_bit(n: int) -> int:
    return n & (-n)

# --- 9.6 Multiply/divide by arbitrary powers of 2 ---
# n << k = n * 2^k  (left shift = multiply)
# n >> k = n // 2^k (right shift = floor divide)
#
# Practical trick: decompose any multiply into shifts and adds.
# n * 10 = n * 8 + n * 2 = (n << 3) + (n << 1)  → 2 shifts + 1 add
# Time: O(1) | Space: O(1)

def multiply_divide_shifts_demo():
    print("\n--- 9.6 Multiply/Divide by Powers of 2 [O(1)] ---")
    n = 13
    print(f"  n = {n}")
    print(f"  n * 2 = n << 1 = {n << 1}")
    print(f"  n * 4 = n << 2 = {n << 2}")
    print(f"  n * 8 = n << 3 = {n << 3}")
    print(f"  n // 2 = n >> 1 = {n >> 1}")
    print(f"  n // 4 = n >> 2 = {n >> 2}")

    n2 = 7
    result = (n2 << 3) + (n2 << 1)  # n * 8 + n * 2 = n * 10
    print(f"\n  n * 10 via shifts: ({n2} << 3) + ({n2} << 1) = {n2 << 3} + {n2 << 1} = {result}")

def advanced_tricks_demo():
    print("\n" + "=" * 60)
    print("SECTION 9: Advanced Tricks")
    print("=" * 60)

    xor_swap(42, 99)

    print(f"\n--- 9.2 Opposite Signs Check [O(1)] ---")
    for a, b in [(5, -3), (-5, -3), (5, 3), (0, -1)]:
        print(f"  ({a:>3}, {b:>3}) → opposite signs? {have_opposite_signs(a, b)}")

    print(f"\n--- 9.3 Two Non-Repeating Elements [O(n), O(1)] ---")
    arr = [2, 3, 7, 9, 11, 2, 3, 11]
    u1, u2 = find_two_unique(arr)
    print(f"  Array: {arr}")
    print(f"  Two unique elements: {u1} and {u2}")

    print(f"\n--- 9.4 Turn Off Rightmost Set Bit [O(1)] ---")
    for num in [12, 7, 16, 255]:
        result = turn_off_rightmost_set_bit(num)
        print(f"  {num:>3} = {num:08b}  →  {result:08b} = {result}")

    print(f"\n--- 9.5 Isolate Rightmost Set Bit  n & (-n)  [O(1)] ---")
    print(f"  Why n & (-n) works:")
    n = 20
    print(f"    n    = {n:08b}  ({n})")
    print(f"    ~n   = (all bits flipped)")
    print(f"    -n   = ~n + 1 = (two's complement)")
    print(f"    n&-n = {isolate_rightmost_set_bit(n):08b}  ({isolate_rightmost_set_bit(n)}) ← only rightmost set bit survives")
    for num in [12, 20, 7, 16, 255]:
        result = isolate_rightmost_set_bit(num)
        print(f"  {num:>3} = {num:08b}  →  rightmost set bit = {result:08b} = {result}")

    multiply_divide_shifts_demo()


# =============================================================================
# SECTION 10: Interview Quick-Reference Table
# =============================================================================

def print_reference_table():
    print("\n" + "=" * 60)
    print("SECTION 10: Interview Quick-Reference Table")
    print("=" * 60)
    print("""
  ┌──────────────────────────────────────┬───────────────────┬──────────┐
  │ Operation                            │ Expression        │ Time     │
  ├──────────────────────────────────────┼───────────────────┼──────────┤
  │ Check even                           │ (n & 1) == 0      │ O(1)     │
  │ Check odd                            │ (n & 1) == 1      │ O(1)     │
  │ Multiply by 2^k                      │ n << k            │ O(1)     │
  │ Divide by 2^k (floor)               │ n >> k            │ O(1)     │
  │ Set k-th bit                         │ n | (1 << k)      │ O(1)     │
  │ Clear k-th bit                       │ n & ~(1 << k)     │ O(1)     │
  │ Check k-th bit                       │ (n >> k) & 1      │ O(1)     │
  │ Flip k-th bit                        │ n ^ (1 << k)      │ O(1)     │
  │ Turn off rightmost set bit           │ n & (n - 1)       │ O(1)     │
  │ Isolate rightmost set bit            │ n & (-n)          │ O(1)     │
  │ Check power of 2                     │ n>0 and n&(n-1)=0 │ O(1)     │
  │ Count set bits (shift loop)          │ n & 1, n >>= 1    │ O(log n) │
  │ Count set bits (Kernighan)           │ n &= (n-1)        │ O(k)     │
  │ Swap without temp                    │ XOR swap          │ O(1)     │
  │ Find unique in pairs array           │ XOR all elements  │ O(n)     │
  │ Opposite signs check                 │ (a ^ b) < 0       │ O(1)     │
  │ Find two unique elements             │ XOR + partition   │ O(n)     │
  └──────────────────────────────────────┴───────────────────┴──────────┘

  XOR Properties:  a ^ a = 0  |  a ^ 0 = a  |  commutative  |  associative
  NOT Formula:     ~n = -(n + 1)      (Python infinite-precision two's complement)
  Python mask:     n & 0xFFFFFFFF     (constrain to 32-bit for LeetCode problems)

  WHY O(1) FOR SINGLE EXPRESSIONS:
    A single bitwise expression (n & 1, n | (1<<k), etc.) maps to exactly
    ONE CPU ALU instruction, executing in ONE clock cycle at the hardware level.
    The time is independent of the VALUE of n — whether n is 5 or 5 billion,
    the CPU performs the same number of hardware operations.
    This is fundamentally different from a loop (O(n)) or recursion (O(log n)).
""")


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_is_power_of_2(n: int) -> bool:
    """
    Return True if n is a power of 2. O(1).
    Hint: powers of 2 have exactly one set bit.
          n & (n-1) removes the single set bit → 0.
          Don't forget: n=0 is NOT a power of 2.
    """
    pass

def practice_count_set_bits(n: int) -> int:
    """
    Count the number of 1-bits in n using Brian Kernighan's method. O(k).
    Hint: n &= (n-1) removes the rightmost set bit each iteration.
    """
    pass

def practice_find_unique(nums: List[int]) -> int:
    """
    Find the element that appears once (all others appear twice). O(n), O(1).
    Hint: XOR all elements. Pairs cancel. Unique survives.
    """
    pass

def practice_missing_number(nums: List[int]) -> int:
    """
    LeetCode 268: Array contains [0..n] with one number missing. Find it.
    Hint: XOR all numbers 0..n against all elements in the array.
          Missing number won't cancel.
    Example: nums=[3,0,1] → n=3, missing=2
    """
    pass

def practice_set_bit(n: int, k: int) -> int:
    """
    Set the k-th bit of n. O(1).
    Hint: OR with a mask that has only bit k set.
    """
    pass

def practice_clear_bit(n: int, k: int) -> int:
    """
    Clear the k-th bit of n. O(1).
    Hint: AND with a mask that has all bits set EXCEPT bit k.
    """
    pass

def practice_check_bit(n: int, k: int) -> int:
    """
    Return 1 if the k-th bit of n is set, else 0. O(1).
    Hint: shift bit k to position 0, then AND with 1.
    """
    pass

def practice_flip_bit(n: int, k: int) -> int:
    """
    Toggle the k-th bit of n. O(1).
    Hint: XOR with (1 << k). XOR with 1 flips; XOR with 0 keeps.
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    binary_system_demo()
    six_operators_demo()
    even_odd_demo()
    bit_manipulation_demo()
    count_bits_demo()
    power_of_2_demo()
    find_unique_demo()
    compound_assignment_demo()
    advanced_tricks_demo()
    print_reference_table()

    print("=" * 60)
    print("PRACTICE SKELETONS")
    print("=" * 60)
    print("Is 16 power of 2?", practice_is_power_of_2(16))   # None (skeleton)
    print("Count bits in 25:", practice_count_set_bits(25))   # None (skeleton)
    print("Unique in [4,1,2,1,2]:", practice_find_unique([4, 1, 2, 1, 2]))
    print("Missing in [3,0,1]:", practice_missing_number([3, 0, 1]))
    print("Set bit 1 of 21:", practice_set_bit(21, 1))
    print("Clear bit 2 of 21:", practice_clear_bit(21, 2))
    print("Check bit 2 of 21:", practice_check_bit(21, 2))
    print("Flip bit 2 of 21:", practice_flip_bit(21, 2))
    print("=" * 60)
    print("All implemented functions verified above.")
    print("Fill in the skeletons and re-run to test your answers.")
