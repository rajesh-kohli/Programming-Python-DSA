###############################################################################
#               05 - Characters and ASCII Manipulation                        #
###############################################################################
#
# COMPLEXITY OVERVIEW:
#   ord() / chr()          : O(1) — single CPU instruction
#   Case conversion        : O(1) — one addition/subtraction/XOR
#   Fixed-size freq array  : O(1) space (26 slots, constant)
#   String scan problems   : O(n) time, O(1) or O(n) space
#
# KEY INSIGHT: Python has NO separate char type.
# A character is simply a str of length 1.
# In C/Java: char c = 'A';   →   In Python: c = "A"  (still type str)
# This means ALL string operations apply to single characters.

from typing import List


# =============================================================================
# SECTION 1: Python Characters — No Separate Char Type
# =============================================================================

def character_type_demo():
    """Show that Python characters are just strings of length 1."""
    print("=" * 60)
    print("SECTION 1: Python Characters")
    print("=" * 60)

    ch = "A"
    print(f"\n  ch = '{ch}'")
    print(f"  type(ch) = {type(ch)}")          # <class 'str'>
    print(f"  len(ch)  = {len(ch)}")            # 1
    print(f"  isinstance(ch, str) = {isinstance(ch, str)}")  # True

    word = "Hello"
    print(f"\n  word = '{word}'")
    print(f"  word[0] = '{word[0]}'   (still type str, NOT a special char type)")
    print(f"  'A' < 'B' = {'A' < 'B'}   (lexicographic — based on ASCII)")
    print(f"  'a' > 'Z' = {'a' > 'Z'}   (97 > 90 — lowercase > uppercase in ASCII)")


# =============================================================================
# SECTION 2: ASCII — ord() and chr() Functions
# =============================================================================
#
# Every character is stored as an integer internally.
# ASCII defines the mapping for the first 128 characters.
#
# Two essential functions:
#   ord(char) -> int   :  character to its ASCII integer
#   chr(num)  -> str   :  ASCII integer back to character
#
# Memory aid:
#   ord = "ordinal" — what number does this character have?
#   chr = "character" — what character does this number represent?
#
# They are EXACT inverses:
#   chr(ord(c)) == c   and   ord(chr(n)) == n
#
# MENTAL MODEL — number line:
#
#  48   49  ...  57   58  ...  65   66  ...  90  ...  97   98  ... 122
#   0    1        9    :        A    B        Z        a    b        z
#   ^── digits ──^              ^─── uppercase ─^     ^─── lowercase ──^
#
# ord(char) walks character → number (left to right)
# chr(num)  walks number → character (right to left)

def ascii_reference_demo():
    """Print all key ASCII boundary values and full alphabet table."""
    print("\n" + "=" * 60)
    print("SECTION 2: ASCII Reference")
    print("=" * 60)

    print("\n--- Core boundary values (MEMORIZE THESE) ---")
    print(f"  ord('0') = {ord('0')}   ord('9') = {ord('9')}   (digits: 48-57, count=10)")
    print(f"  ord('A') = {ord('A')}   ord('Z') = {ord('Z')}   (uppercase: 65-90, count=26)")
    print(f"  ord('a') = {ord('a')}   ord('z') = {ord('z')}  (lowercase: 97-122, count=26)")
    print(f"\n  Critical gap: ord('a') - ord('A') = {ord('a') - ord('A')}")
    print(f"  This single number (32) powers ALL case conversion.")

    print("\n--- chr() round-trips ---")
    print(f"  chr(65) = '{chr(65)}'   chr(97) = '{chr(97)}'   chr(48) = '{chr(48)}'   chr(122) = '{chr(122)}'")

    print("\n--- Full uppercase alphabet with ASCII values ---")
    for i in range(26):
        ch = chr(65 + i)
        print(f"  {ch}={ord(ch)}", end="")
        if (i + 1) % 9 == 0:
            print()
    print()

    print("\n--- Full lowercase alphabet with ASCII values ---")
    for i in range(26):
        ch = chr(97 + i)
        print(f"  {ch}={ord(ch)}", end="")
        if (i + 1) % 9 == 0:
            print()
    print()


# =============================================================================
# SECTION 3: Character Arithmetic — The Round-Trip Pattern
# =============================================================================
#
# KEY RULE: You cannot add an integer directly to a string.
#   'a' + 1  →  TypeError!
#
# You MUST round-trip: ord() → integer math → chr()
#
# Pattern: chr(ord(ch) + offset)
#
# 'a' ─ord()─> 97 ─(+1)─> 98 ─chr()─> 'b'
# 'A' ─ord()─> 65 ─(+32)─> 97 ─chr()─> 'a'

def next_prev_char_demo():
    """Show next/previous character via the ord-math-chr round-trip."""
    print("\n" + "=" * 60)
    print("SECTION 3: Character Arithmetic")
    print("=" * 60)

    print("\n--- Next / Previous character (ord-math-chr round-trip) ---")
    ch = 'A'
    print(f"  Next after '{ch}':  chr(ord('{ch}') + 1) = chr({ord(ch) + 1}) = '{chr(ord(ch) + 1)}'")
    ch = 'M'
    print(f"  Before '{ch}':      chr(ord('{ch}') - 1) = chr({ord(ch) - 1}) = '{chr(ord(ch) - 1)}'")

    print("\n--- Digit value without int() ---")
    digit_ch = '7'
    val = ord(digit_ch) - ord('0')
    print(f"  ord('{digit_ch}') - ord('0') = {ord(digit_ch)} - {ord('0')} = {val}")
    print(f"  This converts '0'-'9' to 0-9 using only ASCII math.")


# =============================================================================
# SECTION 4: Case Conversion — THREE Techniques
# =============================================================================
#
# TECHNIQUE 1: Add/Subtract 32 (arithmetic, with boundary guard)
# TECHNIQUE 2: XOR with 32  (bitwise, branchless toggle)
# TECHNIQUE 3: Fixed-range check (guard without using .isupper()/.islower())
#
# WHY XOR 32 WORKS:
#   32 = 0b00100000  — only bit 5 is set.
#   Uppercase 'A' = 0b01000001  → XOR 32 → 0b01100001 = 97 = 'a'
#   Lowercase 'a' = 0b01100001  → XOR 32 → 0b01000001 = 65 = 'A'
#   Bit 5 is EXACTLY the bit that separates uppercase (0) from lowercase (1)
#   in ASCII. XOR flips it → branchless, O(1) toggle.
#   This works for ALL 26 letter pairs (A/a through Z/z).
#
# Time: O(1) for all three techniques | Space: O(1)

def to_lower_add32(ch: str) -> str:
    """
    Convert uppercase → lowercase by ADDING 32.
    Technique 1: arithmetic — requires a boundary guard.
    Guards ensure non-letters pass through unchanged.
    """
    if 65 <= ord(ch) <= 90:         # guard: only uppercase letters (A-Z)
        return chr(ord(ch) + 32)    # 65+32=97='a', 90+32=122='z'
    return ch                        # non-letter unchanged

def to_upper_subtract32(ch: str) -> str:
    """
    Convert lowercase → uppercase by SUBTRACTING 32.
    Technique 1: arithmetic — requires a boundary guard.
    """
    if 97 <= ord(ch) <= 122:        # guard: only lowercase letters (a-z)
        return chr(ord(ch) - 32)    # 97-32=65='A', 122-32=90='Z'
    return ch

def toggle_case_xor32(ch: str) -> str:
    """
    Toggle case (upper↔lower) using XOR 32.
    Technique 2: BITWISE — branchless single instruction.

    32 = 0b00100000  (only bit 5 set)
    XOR flips bit 5 only:
      'A' = 01000001 ^ 00100000 = 01100001 = 97 = 'a'
      'a' = 01100001 ^ 00100000 = 01000001 = 65 = 'A'
    Works for all 26 letter pairs. Non-letters also get flipped
    but we guard first to avoid corrupting digits/spaces.
    """
    if 65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122:
        return chr(ord(ch) ^ 32)    # flip bit 5 = swap case
    return ch

def case_conversion_demo():
    print("\n" + "=" * 60)
    print("SECTION 4: Case Conversion — 3 Techniques")
    print("=" * 60)

    test = ['A', 'Z', 'a', 'z', 'M', 'm', '5', '!']
    print(f"\n  {'Char':>6} | +32(→lower) | -32(→upper) | XOR32(toggle)")
    print(f"  {'─'*6}-+-{'─'*12}-+-{'─'*12}-+-{'─'*13}")
    for ch in test:
        lo = to_lower_add32(ch)
        up = to_upper_subtract32(ch)
        xr = toggle_case_xor32(ch)
        print(f"  {ch!r:>6} | {lo!r:^12} | {up!r:^12} | {xr!r:^13}")

    print("\n  XOR 32 bit-level proof:")
    for pair in [('A', 'a'), ('Z', 'z'), ('M', 'm')]:
        u, l = pair
        print(f"    '{u}'={ord(u):08b} XOR 00100000 = {ord(u)^32:08b} = {ord(u)^32} = '{chr(ord(u)^32)}'")
        print(f"    '{l}'={ord(l):08b} XOR 00100000 = {ord(l)^32:08b} = {ord(l)^32} = '{chr(ord(l)^32)}'")

def toggle_case_string_manual(s: str) -> str:
    """
    Toggle case for every letter in a string — no .swapcase().
    Uses XOR 32 trick on each letter.
    Non-letter characters pass through unchanged.
    Time: O(n) | Space: O(n)
    """
    result = []
    for ch in s:
        result.append(toggle_case_xor32(ch))
    return "".join(result)


# =============================================================================
# SECTION 5: Character Type Checks (without built-ins)
# =============================================================================
#
# Interview rule: implement is_upper/lower/digit using only ord() + boundaries.
# Never use .isupper(), .islower(), .isdigit() in a white-board setting unless
# explicitly allowed.
#
# Time: O(1) each | Space: O(1) each

def is_uppercase(ch: str) -> bool:
    """Return True if ch is A-Z. O(1)."""
    return 65 <= ord(ch) <= 90

def is_lowercase(ch: str) -> bool:
    """Return True if ch is a-z. O(1)."""
    return 97 <= ord(ch) <= 122

def is_digit_char(ch: str) -> bool:
    """Return True if ch is 0-9. O(1)."""
    return 48 <= ord(ch) <= 57

def is_letter(ch: str) -> bool:
    """Return True if ch is A-Z or a-z. O(1)."""
    return is_uppercase(ch) or is_lowercase(ch)

def is_alphanumeric_manual(ch: str) -> bool:
    """Return True if ch is a letter or digit. O(1). No .isalnum()."""
    return is_letter(ch) or is_digit_char(ch)

def char_checks_demo():
    print("\n" + "=" * 60)
    print("SECTION 5: Character Type Checks (no built-ins)")
    print("=" * 60)
    print(f"\n  {'Char':>6} | upper | lower | digit | letter | alnum")
    print(f"  {'─'*6}-+-------+-------+-------+--------+------")
    for c in ['A', 'z', '5', '!', 'M', 'q', '0', ' ']:
        print(f"  {c!r:>6} | {is_uppercase(c)!s:^5} | {is_lowercase(c)!s:^5} "
              f"| {is_digit_char(c)!s:^5} | {is_letter(c)!s:^6} | {is_alphanumeric_manual(c)!s:^5}")


# =============================================================================
# SECTION 6: Alphabet Index — 0-indexed position mapping
# =============================================================================
#
# ord(ch) - ord('A') → 0-indexed position for uppercase (0='A', 25='Z')
# ord(ch) - ord('a') → 0-indexed position for lowercase (0='a', 25='z')
# ord(ch) - ord('0') → digit value without int()        (0='0',  9='9')
#
# This formula is the FOUNDATION of the 26-element frequency array trick.
# Time: O(1) | Space: O(1)

def alphabet_index_demo():
    print("\n" + "=" * 60)
    print("SECTION 6: Alphabet Index (0-indexed letter positions)")
    print("=" * 60)
    print("\n  Uppercase positions (ord(ch) - ord('A')):")
    for ch in ['A', 'C', 'M', 'Z']:
        idx = ord(ch) - ord('A')
        print(f"    '{ch}' → ord({ord(ch)}) - 65 = {idx}  (letter #{idx+1} in alphabet)")
    print("\n  Lowercase positions (ord(ch) - ord('a')):")
    for ch in ['a', 'f', 'm', 'z']:
        idx = ord(ch) - ord('a')
        print(f"    '{ch}' → ord({ord(ch)}) - 97 = {idx}")
    print("\n  Digit values (ord(ch) - ord('0')):")
    for ch in ['0', '3', '7', '9']:
        val = ord(ch) - ord('0')
        print(f"    '{ch}' → ord({ord(ch)}) - 48 = {val}")


# =============================================================================
# SECTION 7: Fixed-Size Frequency Array — The Key Interview Optimization
# =============================================================================
#
# PROBLEM: Count character frequencies in a string.
#
# ── APPROACH 1: Dictionary (naive) ──────────────────────────────────────────
#   freq = {}
#   for ch in s:
#       freq[ch] = freq.get(ch, 0) + 1
#
#   Time : O(n)
#   Space: O(k) where k = number of unique characters (grows dynamically)
#   Hash : hash function computed per insertion (multiple ops)
#
# ── APPROACH 2: Fixed-Size Array (optimal for constrained input) ─────────────
#   freq = [0] * 26
#   for ch in s:
#       freq[ord(ch) - ord('a')] += 1
#
#   Time : O(n)
#   Space: O(1) ← ALWAYS exactly 26 integers, independent of input size
#   Index: single subtraction — no hashing, direct memory address
#
# WHY THE ARRAY IS BETTER:
#   1. O(1) SPACE: 26 integers = 26×8 bytes = 208 bytes, ALWAYS.
#      A dict can grow unboundedly.
#   2. NO HASH OVERHEAD: `ord(ch) - ord('a')` is ONE subtraction → one
#      instruction. A dict lookup computes a hash (multiple ops) + probing.
#   3. CACHE-FRIENDLY: Array elements are contiguous in memory.
#      Dict entries may be scattered (pointer chasing = cache misses).
#   4. INTERVIEW SIGNAL: Using a 26-element array shows you understand the
#      constant-space optimization that HashMap cannot achieve.
#
# CONSTRAINT: Only works when input is LIMITED to a known character set
# (e.g., "lowercase English letters" — the most common LeetCode constraint).
# If input can be arbitrary Unicode, you must use a dict.
#
# Time: O(n) | Space: O(1) — 26 is a constant, not input-dependent

def build_freq_array(s: str) -> List[int]:
    """
    Build a 26-element frequency array for lowercase letters.
    Index formula: ord(ch) - ord('a')  → 0..25
    Non-lowercase characters are skipped.
    O(n) time | O(1) space
    """
    freq = [0] * 26                      # 26 slots, always O(1) space
    for ch in s:
        if is_lowercase(ch):
            freq[ord(ch) - ord('a')] += 1  # direct index — no hashing
    return freq

def freq_array_demo():
    print("\n" + "=" * 60)
    print("SECTION 7: Fixed-Size Frequency Array  [O(1) space]")
    print("=" * 60)

    s = "hello world"
    freq = build_freq_array(s)
    print(f"\n  String: '{s}'")
    print(f"  Frequency array (26 slots, 0-indexed by letter):")
    for i in range(26):
        if freq[i] > 0:
            ch = chr(ord('a') + i)
            print(f"    freq[{i:>2}] = freq[ord('{ch}')-97] = {freq[i]}  ('{ch}' appears {freq[i]}×)")

    # Comparison: dict approach
    freq_dict = {}
    for ch in s:
        if is_lowercase(ch):
            freq_dict[ch] = freq_dict.get(ch, 0) + 1
    print(f"\n  Dictionary approach (same result, but O(k) space): {freq_dict}")
    print(f"  Array approach: O(1) fixed space — always exactly 26 integers")


# =============================================================================
# SECTION 8: String Immutability and Building
# =============================================================================
#
# Strings in Python are IMMUTABLE. s[0] = 'J' raises TypeError.
# Pattern to "modify" a string: list(s) → mutate → "".join(result)
#
# STRING BUILDING PERFORMANCE:
#   result = ""
#   result += ch      (in a loop)  →  O(n²) TOTAL
#   Why? Each += creates a new string object (allocate, copy all, discard old).
#   For n chars: 1 + 2 + 3 + ... + n = n(n+1)/2 = O(n²) copies.
#
#   list.append(ch)  then  "".join(result)  →  O(n) TOTAL
#   Why? append is O(1) amortised. join does ONE pass allocation + one copy.
#
# ALWAYS use list + "".join() when building strings character by character.

def string_immutability_demo():
    print("\n" + "=" * 60)
    print("SECTION 8: String Immutability and Building")
    print("=" * 60)

    s = "Hello"
    print(f"\n  s = '{s}'")
    print(f"  s[0] = 'J'  →  Would raise TypeError: 'str' object does not support item assignment")

    # Correct pattern: list → mutate → join
    s_list = list(s)
    s_list[0] = 'J'
    s_new = "".join(s_list)
    print(f"\n  Correct: list(s)[0] = 'J'  →  \"\".join(...)  →  '{s_new}'")

    # Also: slice concatenation
    s_new2 = 'J' + s[1:]
    print(f"  Also OK: 'J' + s[1:]  →  '{s_new2}'")

    print("\n  String building: list+join (O(n)) vs concatenation (O(n²))")
    # O(n) — list + join
    chars_list = [chr(ord('A') + i) for i in range(5)]
    result = "".join(chars_list)
    print(f"  list+join: {chars_list} → '{result}'")

    # O(n) — generator join (even cleaner)
    result2 = "".join(chr(ord('a') + i) for i in range(5))
    print(f"  generator join: '{result2}'")


# =============================================================================
# SECTION 9: String-to-Integer Without int()
# =============================================================================
#
# Algorithm: process digits left to right.
# At each step: result = result * 10 + digit_value
# This "shifts" the existing digits left by one decimal place and adds the new digit.
#
# Example: "4096"
#   Start:      result = 0
#   After '4':  result = 0 * 10 + 4 = 4
#   After '0':  result = 4 * 10 + 0 = 40
#   After '9':  result = 40 * 10 + 9 = 409
#   After '6':  result = 409 * 10 + 6 = 4096  ← done
#
# Time: O(n) | Space: O(1)

def string_to_integer(s: str) -> int:
    """
    Convert a string of digit characters to an integer — no int() allowed.
    Formula: result = result * 10 + (ord(ch) - ord('0'))
    """
    result = 0
    for ch in s:
        if not is_digit_char(ch):
            break                              # stop at first non-digit
        digit_val = ord(ch) - ord('0')         # e.g. '7' → 55 - 48 = 7
        result = result * 10 + digit_val       # shift + add
    return result


# =============================================================================
# SECTION 10: Character Pattern Problems
# =============================================================================
#
# Character patterns reuse all the loop structures from Module 03.
# The ONLY change: instead of printing stars/numbers, you print chr(ord('A')+i).

def char_pattern_alphabet_triangle(n: int):
    """
    Pattern 1: Alphabet triangle (row i shows A B C ... up to i-th letter)
    A
    A B
    A B C
    A B C D
    Loop: start ch='A' each row, increment via chr(ord(ch)+1) each column.
    """
    for i in range(1, n + 1):
        ch = "A"
        for _ in range(i):
            print(ch, end=" ")
            ch = chr(ord(ch) + 1)   # ord('A')=65 → 66 → 67 ... same round-trip pattern
        print()

def char_pattern_same_letter_rows(n: int):
    """
    Pattern 2: Same letter repeated per row (A, BB, CCC, DDDD)
    Row i uses the i-th letter: chr(ord('A') + i - 1).
    Key insight: the letter for each row is ord('A') + row_index - 1.
    """
    for i in range(1, n + 1):
        ch = chr(ord('A') + i - 1)    # row 1→'A', row 2→'B', row 3→'C'
        for _ in range(i):
            print(ch, end=" ")
        print()

def char_pattern_decreasing(n: int):
    """
    Pattern 3: Decreasing alphabet rows
    A B C D
    A B C
    A B
    A
    Row i has (n-i+1) characters starting from 'A'.
    """
    for i in range(1, n + 1):
        ch = "A"
        for _ in range(n - i + 1):
            print(ch, end=" ")
            ch = chr(ord(ch) + 1)
        print()

def char_pattern_mountain(n: int):
    """
    Pattern 4: Alphabet mountain (increase then decrease per row)
    A B C D D C B A
    A B C C B A
    A B B A
    A A
    Ascending: go up to the turning point.
    Descending: step back one, then count down.
    """
    for i in range(1, n + 1):
        ch = "A"
        # Ascending part
        for _ in range(n - i + 1):
            print(ch, end=" ")
            ch = chr(ord(ch) + 1)
        # Step back one for the descending mirror
        ch = chr(ord(ch) - 1)
        # Descending part
        for _ in range(n - i + 1):
            print(ch, end=" ")
            ch = chr(ord(ch) - 1)
        print()

def char_pattern_diamond(n: int):
    """
    Pattern 5: Character diamond (centered)
        A
       A B
      A B C
       A B
        A
    Upper half (rows 1..m): (m-i) leading spaces, then i letters.
    Lower half (rows 1..m-1): i leading spaces, then m-i letters.
    """
    m = n - n // 2   # rows in first half (including middle)
    # Upper half
    for i in range(1, m + 1):
        print("  " * (m - i), end="")
        ch = "A"
        for _ in range(i):
            print(ch, end=" ")
            ch = chr(ord(ch) + 1)
        print()
    # Lower half
    for i in range(1, m):
        print("  " * i, end="")
        ch = "A"
        for _ in range(m - i):
            print(ch, end=" ")
            ch = chr(ord(ch) + 1)
        print()

def char_patterns_demo(n: int = 4):
    print("\n" + "=" * 60)
    print("SECTION 10: Character Pattern Problems")
    print("=" * 60)
    print(f"\n--- Pattern 1: Alphabet Triangle (n={n}) ---")
    char_pattern_alphabet_triangle(n)
    print(f"\n--- Pattern 2: Same Letter Rows (n={n}) ---")
    char_pattern_same_letter_rows(n)
    print(f"\n--- Pattern 3: Decreasing Rows (n={n}) ---")
    char_pattern_decreasing(n)
    print(f"\n--- Pattern 4: Alphabet Mountain (n={n}) ---")
    char_pattern_mountain(n)
    print(f"\n--- Pattern 5: Character Diamond (n=5) ---")
    char_pattern_diamond(5)


# =============================================================================
# SECTION 11: Interview Problems
# =============================================================================

# --- 11.1 Count Vowels and Consonants — O(n) time, O(1) space ---
#
# Approach: convert to lowercase for uniform comparison.
# Check vowel membership, then is_letter() for consonants.
# Crucially: use is_letter() via ord() — not .isalpha() — to keep it pure ASCII.

def count_vowels_consonants(s: str):
    """
    Return (vowel_count, consonant_count) in string s.
    Uses pure ord()-based character checks. O(n) time, O(1) space.
    """
    vowels = "aeiou"
    v_count, c_count = 0, 0
    for ch in s:
        # Convert to lowercase for uniform comparison (using our manual toggle)
        lch = to_lower_add32(ch)
        if lch in vowels:
            v_count += 1
        elif is_letter(ch):          # letter but not a vowel → consonant
            c_count += 1
    return v_count, c_count


# --- 11.2 Palindrome Check — O(n) time, O(n) for cleaned string ---
#
# Two-pointer approach:
# 1. Filter to letters only, convert to lowercase (pure ASCII).
# 2. Compare from both ends moving inward.
#
# Time: O(n) | Space: O(n) for cleaned string

def is_palindrome(s: str) -> bool:
    """
    Return True if s is a palindrome (letters only, case-insensitive).
    Uses ord() checks — no .isalpha(), no .lower().
    """
    # Build cleaned string using only ASCII tools
    cleaned = []
    for ch in s:
        if is_letter(ch):
            cleaned.append(to_lower_add32(ch))

    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True


# --- 11.3 Caesar Cipher — O(n) time, O(n) space ---
#
# FORMULA: (ord(ch) - ord('A') + k) % 26
#
# Step-by-step for 'X' with shift k=5:
#   1. ord('X') - ord('A') = 88 - 65 = 23   (position in alphabet, 0-indexed)
#   2. 23 + 5 = 28
#   3. 28 % 26 = 2                            (wrapped: position 2 = 'C')
#   4. chr(ord('A') + 2) = 'C'
#
# % 26 naturally handles:
#   - POSITIVE shift (encrypt): wrap forward past 'Z'
#   - NEGATIVE shift (decrypt): Python's % is always non-negative, so -k works too
#
# Case is preserved: uppercase shifts within 'A'-'Z', lowercase within 'a'-'z'.
# Non-letters pass through unchanged.

def caesar_cipher(text: str, k: int) -> str:
    """
    Encrypt/decrypt text by shifting each letter by k positions.
    k > 0: encrypt. k < 0: decrypt.
    Wraps around using % 26. O(n) time, O(n) space.
    """
    result = []
    for ch in text:
        if is_uppercase(ch):
            # Uppercase: map to 0-25, shift, wrap, map back
            pos = (ord(ch) - ord('A') + k) % 26  # step 1+2+3
            result.append(chr(ord('A') + pos))    # step 4
        elif is_lowercase(ch):
            # Same formula, but anchored to 'a' = 97
            pos = (ord(ch) - ord('a') + k) % 26
            result.append(chr(ord('a') + pos))
        else:
            result.append(ch)                     # non-letter: unchanged
    return "".join(result)


# --- 11.4 Alternating Case — O(n) time, O(n) space ---
#
# Even-indexed letters → uppercase. Odd-indexed letters → lowercase.
# The "letter index" counter tracks only letters — spaces and digits don't count.

def alternating_case(s: str) -> str:
    """
    Even-positioned letters → uppercase, odd-positioned → lowercase.
    Non-letter characters are kept but don't count toward the letter index.
    O(n) time, O(n) space.
    """
    result = []
    letter_idx = 0           # separate counter for LETTERS ONLY
    for ch in s:
        if is_letter(ch):
            if letter_idx % 2 == 0:
                result.append(to_upper_subtract32(ch))   # even → upper
            else:
                result.append(to_lower_add32(ch))        # odd → lower
            letter_idx += 1
        else:
            result.append(ch)                            # keep unchanged
    return "".join(result)


# --- 11.5 Frequency Array Anagram Check — O(n) time, O(1) space ---
#
# Two strings are anagrams if they have the same character frequencies.
# NAIVE: sort both strings → O(n log n).
# OPTIMAL: frequency array → O(n) time, O(1) space.
#
# Build freq for s1, subtract for s2. If all slots are 0 → anagram.
# This avoids a second array: one array, add for s1, subtract for s2.

def are_anagrams(s1: str, s2: str) -> bool:
    """
    Return True if s1 and s2 are anagrams (same letters, different order).
    Uses a 26-element fixed array. O(n) time, O(1) space.
    Assumes lowercase English letters only.
    """
    if len(s1) != len(s2):
        return False
    freq = [0] * 26                         # one array serves both strings
    for i in range(len(s1)):
        freq[ord(s1[i]) - ord('a')] += 1    # +1 for s1
        freq[ord(s2[i]) - ord('a')] -= 1    # -1 for s2
    return all(f == 0 for f in freq)        # all zeros → same frequencies


def interview_problems_demo():
    print("\n" + "=" * 60)
    print("SECTION 11: Interview Problems")
    print("=" * 60)

    # 11.1 Count vowels/consonants
    print("\n--- 11.1 Count Vowels and Consonants [O(n), O(1)] ---")
    for s in ["Hello World", "Python", "aeiou", "Hi 123!"]:
        v, c = count_vowels_consonants(s)
        print(f"  '{s}' → vowels={v}, consonants={c}")

    # 11.2 Palindrome
    print("\n--- 11.2 Palindrome Check [O(n)] ---")
    for word in ["Racecar", "hello", "Madam", "A", "Was it a car or a cat I saw"]:
        print(f"  '{word}' → {is_palindrome(word)}")

    # 11.3 Caesar cipher
    print("\n--- 11.3 Caesar Cipher [O(n)] ---")
    print(f"  'ABC' + k=3  → '{caesar_cipher('ABC', 3)}'")
    print(f"  'XYZ' + k=3  → '{caesar_cipher('XYZ', 3)}'  (wraps X→A, Y→B, Z→C)")
    print(f"  'Hello World' + k=5  → '{caesar_cipher('Hello World', 5)}'")
    original = "Attack at Dawn!"
    enc = caesar_cipher(original, 13)
    dec = caesar_cipher(enc, -13)
    print(f"\n  Round-trip (k=13 then k=-13):")
    print(f"    Original:  '{original}'")
    print(f"    Encrypted: '{enc}'")
    print(f"    Decrypted: '{dec}'")
    print(f"    Match: {original == dec}")

    # 11.4 Alternating case
    print("\n--- 11.4 Alternating Case [O(n)] ---")
    for s in ["hello world", "abcdef", "Hi There!"]:
        print(f"  '{s}' → '{alternating_case(s)}'")

    # 11.5 Anagram check
    print("\n--- 11.5 Anagram Check via Frequency Array [O(n), O(1)] ---")
    pairs = [("listen", "silent"), ("hello", "world"), ("anagram", "nagaram"), ("rat", "car")]
    for s1, s2 in pairs:
        print(f"  '{s1}' & '{s2}' → anagram={are_anagrams(s1, s2)}")


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_is_alphanumeric(ch: str) -> bool:
    """
    Return True if ch is a letter (a-z, A-Z) or a digit (0-9).
    Use ONLY ASCII boundaries — no .isalnum().
    Hint: is_letter(ch) or is_digit_char(ch)
    """
    pass

def practice_caesar_cipher(s: str, shift: int) -> str:
    """
    Caesar cipher: shift each lowercase letter by `shift` positions.
    Wrap 'z' back to 'a'. Leave non-lowercase unchanged.
    Hint: pos = (ord(ch) - ord('a') + shift) % 26
    """
    pass

def practice_toggle_case_xor(ch: str) -> str:
    """
    Toggle case of ch using XOR 32.
    Guard: only apply to letters (A-Z or a-z), pass others through.
    Hint: chr(ord(ch) ^ 32)
    """
    pass

def practice_string_to_int(s: str) -> int:
    """
    Convert a decimal string like '1234' to integer 1234 without int().
    Hint: result = result * 10 + (ord(ch) - ord('0'))
    """
    pass

def practice_freq_array(s: str) -> List[int]:
    """
    Build a 26-element frequency array for lowercase letters in s.
    Return a list of 26 ints where index i = count of chr(ord('a') + i).
    Hint: freq[ord(ch) - ord('a')] += 1
    """
    pass

def practice_are_anagrams(s1: str, s2: str) -> bool:
    """
    Return True if s1 and s2 are anagrams of each other.
    Use a single 26-element frequency array. O(n) time, O(1) space.
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    character_type_demo()
    ascii_reference_demo()
    next_prev_char_demo()
    case_conversion_demo()
    char_checks_demo()
    alphabet_index_demo()
    freq_array_demo()
    string_immutability_demo()

    print("\n" + "=" * 60)
    print("SECTION 9: String-to-Integer (no int())")
    print("=" * 60)
    for s in ["4096", "0", "123", "999"]:
        print(f"  string_to_integer('{s}') = {string_to_integer(s)}")

    char_patterns_demo(n=4)
    interview_problems_demo()

    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS")
    print("=" * 60)
    print("is_alphanumeric('x'):", practice_is_alphanumeric('x'))
    print("is_alphanumeric('3'):", practice_is_alphanumeric('3'))
    print("is_alphanumeric('!'):", practice_is_alphanumeric('!'))
    print("caesar_cipher('abc', 2):", practice_caesar_cipher('abc', 2))
    print("toggle_case_xor('A'):", practice_toggle_case_xor('A'))
    print("toggle_case_xor('a'):", practice_toggle_case_xor('a'))
    print("string_to_int('4096'):", practice_string_to_int('4096'))
    print("freq_array('hello'):", practice_freq_array('hello'))
    print("are_anagrams('listen','silent'):", practice_are_anagrams('listen', 'silent'))
    print("=" * 60)
    print("Fill in the skeletons above and re-run to verify.")
