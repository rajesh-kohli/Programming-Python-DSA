# ============================================================================
#  10 - CHARACTERS, ASCII, AND CHARACTER PATTERN PRINTING
# ============================================================================
# A comprehensive guide to working with characters in Python, ASCII encoding,
# character arithmetic, and character-based pattern problems.
# Every section is runnable — execute this file to see all outputs.
# ============================================================================

print("=" * 70)
print("  10 - CHARACTERS, ASCII, AND CHARACTER PATTERNS")
print("=" * 70)


# ===== SECTION 1: Characters in Python =====================================
print("\n" + "=" * 70)
print("  SECTION 1: Characters in Python")
print("=" * 70)

# KEY FACT: Python has NO separate 'char' type.
# A character is simply a string of length 1.
#
# In C/Java, you write:  char ch = 'A';    (a distinct type)
# In Python, you write:  ch = "A"          (it's just a str of length 1)
#
# This means every string operation works on single characters too:
#   - len("A") == 1
#   - "A" + "B" == "AB"  (concatenation)
#   - "A" == "A"         (comparison)
#   - "A" < "B"          (lexicographic comparison, based on ASCII values)

ch = "A"
print(f"\nch = '{ch}'")
print(f"type(ch) = {type(ch)}")      # <class 'str'>
print(f"len(ch)  = {len(ch)}")       # 1
print(f"Is it a string? {isinstance(ch, str)}")  # True

# Characters vs strings: the only difference is length
word = "Hello"
print(f"\nword = '{word}'")
print(f"word[0] = '{word[0]}'  (a character — still type str)")
print(f"type(word[0]) = {type(word[0])}")


# ===== SECTION 2: ASCII — The Number Behind Every Character ================
print("\n" + "=" * 70)
print("  SECTION 2: ASCII — The Number Behind Every Character")
print("=" * 70)

# Every character is stored as a number internally. ASCII (American Standard
# Code for Information Interchange) defines the mapping.
#
# Two essential built-in functions:
#   ord(char) -> int   : character to its ASCII number
#   chr(num)  -> str   : ASCII number back to character
#
# Think of it as:
#   ord = "ordinal" — what number does this character have?
#   chr = "character" — what character does this number represent?

print("\n--- ord() and chr() basics ---")
print(f"ord('A') = {ord('A')}")       # 65
print(f"ord('Z') = {ord('Z')}")       # 90
print(f"ord('a') = {ord('a')}")       # 97
print(f"ord('z') = {ord('z')}")       # 122
print(f"ord('0') = {ord('0')}")       # 48
print(f"ord('9') = {ord('9')}")       # 57

print(f"\nchr(65)  = '{chr(65)}'")    # A
print(f"chr(97)  = '{chr(97)}'")      # a
print(f"chr(48)  = '{chr(48)}'")      # 0
print(f"chr(122) = '{chr(122)}'")     # z

# ASCII TABLE REFERENCE (the ranges you MUST memorize):
#
#   Characters     ASCII Range     Count
#   ──────────     ───────────     ─────
#   '0' to '9'     48  to  57      10
#   'A' to 'Z'     65  to  90      26
#   'a' to 'z'     97  to 122      26
#
# Important relationships:
#   ord('a') - ord('A') = 97 - 65 = 32
#   Uppercase + 32 = Lowercase (and vice versa: Lowercase - 32 = Uppercase)

print("\n--- ASCII Table (printable subset) ---")
print(f"  '0'-'9': {ord('0')}-{ord('9')}  (digits)")
print(f"  'A'-'Z': {ord('A')}-{ord('Z')}  (uppercase letters)")
print(f"  'a'-'z': {ord('a')}-{ord('z')}  (lowercase letters)")
print(f"  Difference between 'a' and 'A': {ord('a') - ord('A')}")

# Print the full uppercase alphabet with ASCII values
print("\n--- Full uppercase alphabet ---")
for i in range(26):
    ch = chr(65 + i)
    print(f"  {ch} = {ord(ch)}", end="")
    if (i + 1) % 9 == 0:
        print()
print()


# ===== SECTION 3: Character Arithmetic =====================================
print("\n" + "=" * 70)
print("  SECTION 3: Character Arithmetic")
print("=" * 70)

# Since characters are numbers under the hood, we can do "arithmetic" on
# them by converting to int, doing math, and converting back.
#
# Pattern: chr(ord(char) + offset)

# --- Getting next / previous character ---
print("\n--- Next and previous characters ---")
ch = "A"
next_ch = chr(ord(ch) + 1)
print(f"Next after '{ch}': '{next_ch}'")      # B

ch = "M"
prev_ch = chr(ord(ch) - 1)
print(f"Before '{ch}':     '{prev_ch}'")       # L

# --- Case conversion WITHOUT built-ins ---
# Uppercase to lowercase: add 32
# Lowercase to uppercase: subtract 32
print("\n--- Manual case conversion (no .upper()/.lower()) ---")
upper = "H"
lower = chr(ord(upper) + 32)
print(f"'{upper}' -> lowercase -> '{lower}'")

lower = "h"
upper = chr(ord(lower) - 32)
print(f"'{lower}' -> uppercase -> '{upper}'")

# --- Character type checking using ord() ---
# These work WITHOUT using .isupper(), .islower(), .isdigit()
print("\n--- Character type checking with ord() ---")

def is_uppercase(ch):
    return 65 <= ord(ch) <= 90       # 'A' to 'Z'

def is_lowercase(ch):
    return 97 <= ord(ch) <= 122      # 'a' to 'z'

def is_digit(ch):
    return 48 <= ord(ch) <= 57       # '0' to '9'

def is_letter(ch):
    return is_uppercase(ch) or is_lowercase(ch)

test_chars = ['A', 'z', '5', '!', 'M', 'q']
for c in test_chars:
    print(f"  '{c}': upper={is_uppercase(c)}, lower={is_lowercase(c)}, "
          f"digit={is_digit(c)}, letter={is_letter(c)}")

# --- Getting the position of a letter in the alphabet (0-indexed) ---
print("\n--- Alphabet position ---")
for ch in ['A', 'C', 'Z', 'a', 'f', 'z']:
    if is_uppercase(ch):
        pos = ord(ch) - ord('A')
    else:
        pos = ord(ch) - ord('a')
    print(f"  '{ch}' is letter #{pos} (0-indexed), #{pos+1} (1-indexed)")


# ===== SECTION 4: String Operations Relevant to Characters ================
print("\n" + "=" * 70)
print("  SECTION 4: String Operations Relevant to Characters")
print("=" * 70)

# --- Iterating over a string character by character ---
print("\n--- Iterating character by character ---")
word = "Python"
print(f"String: '{word}'")

# Method 1: direct iteration
print("Method 1 (for ch in word):")
for ch in word:
    print(f"  '{ch}' (ASCII {ord(ch)})")

# Method 2: index-based
print("Method 2 (index-based):")
for i in range(len(word)):
    print(f"  word[{i}] = '{word[i]}'")

# --- Strings are IMMUTABLE ---
# You CANNOT modify a character in a string directly.
print("\n--- Strings are immutable ---")
s = "Hello"
print(f"s = '{s}'")
print("s[0] = 'J'  -> This would raise TypeError!")
# s[0] = 'J'  # Uncomment to see: TypeError: 'str' object does not support item assignment

# To "change" a character, you must BUILD A NEW STRING:
s_new = "J" + s[1:]
print(f"'J' + s[1:] = '{s_new}'")

# --- Building new strings from characters ---
print("\n--- Building strings from characters ---")

# Method 1: Concatenation (works but slow for large strings)
result = ""
for i in range(5):
    result += chr(ord('A') + i)
print(f"Concatenation: '{result}'")

# Method 2: List + join (preferred for performance)
chars = [chr(ord('A') + i) for i in range(5)]
result = "".join(chars)
print(f"List + join:   '{result}'")

# Method 3: Using join with a generator
result = "".join(chr(ord('a') + i) for i in range(5))
print(f"Generator:     '{result}'")


# ===== SECTION 5: Character Patterns ======================================
print("\n" + "=" * 70)
print("  SECTION 5: Character Patterns")
print("=" * 70)

# These patterns use chr() and ord() to print letters instead of numbers
# or stars. The loop structure is the same as number patterns — only the
# print content changes.


# --- Pattern 1: Alphabet Triangle (increasing) ---
# n=4:
# A
# A B
# A B C
# A B C D
print("\n--- Pattern 1: Alphabet Triangle (increasing) ---")
n = 4
for i in range(1, n + 1):
    ch = "A"
    for _ in range(i):
        print(ch, end=" ")
        ch = chr(ord(ch) + 1)
    print()


# --- Pattern 2: A, BB, CCC, DDDD... ---
# n=4:
# A
# B B
# C C C
# D D D D
print("\n--- Pattern 2: Same character repeated (A, BB, CCC, DDDD) ---")
n = 4
for i in range(1, n + 1):
    ch = chr(ord('A') + i - 1)       # row i uses the i-th letter
    for _ in range(i):
        print(ch, end=" ")
    print()


# --- Pattern 3: Decreasing alphabet rows ---
# n=4:
# A B C D
# A B C
# A B
# A
# (from source 010pattern8.py)
print("\n--- Pattern 3: Decreasing alphabet rows ---")
n = 4
for i in range(1, n + 1):
    ch = "A"
    for _ in range(n - i + 1):
        print(ch, end=" ")
        ch = chr(ord(ch) + 1)
    print()


# --- Pattern 4: Increasing then decreasing (mountain) ---
# n=4:
# A B C D D C B A
# A B C C B A
# A B B A
# A A
# (from source 011pattern9.py)
print("\n--- Pattern 4: Alphabet mountain (increase then decrease) ---")
n = 4
for i in range(1, n + 1):
    # Ascending part: print n-i+1 characters starting from A
    ch = "A"
    for _ in range(n - i + 1):
        print(ch, end=" ")
        ch = chr(ord(ch) + 1)

    # Descending part: go back one step, then print n-i+1 characters
    ch = chr(ord(ch) - 1)
    for _ in range(n - i + 1):
        print(ch, end=" ")
        ch = chr(ord(ch) - 1)

    print()


# --- Pattern 5: Diamond with characters ---
# n=5 (using m = n - n//2 = 3 for first half):
#     A
#    A B
#   A B C
#    A B
#     A
# (adapted from source 012pattern10.py and 013pattern11.py)
print("\n--- Pattern 5: Diamond with characters ---")
n = 5
m = n - n // 2   # rows in first half (including middle)

# First half (expanding)
for i in range(1, m + 1):
    # Print leading spaces
    print("  " * (m - i), end="")
    # Print characters
    ch = "A"
    for _ in range(i):
        print(ch, end=" ")
        ch = chr(ord(ch) + 1)
    print()

# Second half (shrinking)
for i in range(1, m):
    # Print leading spaces
    print("  " * i, end="")
    # Print characters
    ch = "A"
    for _ in range(m - i):
        print(ch, end=" ")
        ch = chr(ord(ch) + 1)
    print()


# ===== SECTION 6: Practice Exercises ======================================
print("\n" + "=" * 70)
print("  SECTION 6: Practice Exercises")
print("=" * 70)


# ---------- Exercise 1: Count Vowels and Consonants ----------
# Given a string, count the number of vowels and consonants.
# Ignore non-letter characters.
#
# Approach:
#   - Convert to lowercase for uniform comparison.
#   - Check if character is in "aeiou" (vowel) or is a letter (consonant).
#
# Time : O(n)
# Space: O(1)

def count_vowels_consonants(s):
    """Return (vowel_count, consonant_count) in string s."""
    vowels = "aeiou"
    v_count = 0
    c_count = 0
    for ch in s.lower():
        if ch in vowels:
            v_count += 1
        elif ch.isalpha():            # it's a letter but not a vowel
            c_count += 1
    return v_count, c_count


print("\n--- Exercise 1: Count Vowels and Consonants ---")
test_strings = ["Hello World", "Python", "aeiou", "bcdfg", "Hi 123!"]
for s in test_strings:
    v, c = count_vowels_consonants(s)
    print(f"  '{s}' -> vowels={v}, consonants={c}")


# ---------- Exercise 2: Check if String is Palindrome (Case-Insensitive) ---
# A palindrome reads the same forwards and backwards.
# "Racecar" -> "racecar" -> True
#
# Approach (Two Pointer):
#   - Convert to lowercase.
#   - Compare characters from both ends moving inward.
#
# Time : O(n)
# Space: O(1) (ignoring the lowercase copy)

def is_palindrome(s):
    """Check if s is a palindrome (case-insensitive, letters only)."""
    # Keep only letters and convert to lowercase
    cleaned = ""
    for ch in s:
        if ch.isalpha():
            cleaned += ch.lower()

    # Two-pointer check
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True


print("\n--- Exercise 2: Palindrome Check ---")
test_words = ["Racecar", "hello", "Madam", "A", "Was it a car or a cat I saw"]
for word in test_words:
    result = is_palindrome(word)
    print(f"  '{word}' -> palindrome={result}")


# ---------- Exercise 3: Caesar Cipher ----------
# Shift each letter by k positions in the alphabet. Wrap around Z -> A.
# Non-letter characters remain unchanged.
#
# Example: "ABC" with k=3 -> "DEF"
#          "XYZ" with k=3 -> "ABC" (wraps around)
#
# Approach:
#   - For each letter, find its position (0-25), add k, take mod 26.
#   - Convert back to a character.
#   - Preserve the original case.
#
# Time : O(n)
# Space: O(n) — building the result string

def caesar_cipher(text, k):
    """Encrypt text by shifting each letter by k positions."""
    result = []
    for ch in text:
        if is_uppercase(ch):
            # Shift within uppercase range
            pos = (ord(ch) - ord('A') + k) % 26
            result.append(chr(ord('A') + pos))
        elif is_lowercase(ch):
            # Shift within lowercase range
            pos = (ord(ch) - ord('a') + k) % 26
            result.append(chr(ord('a') + pos))
        else:
            result.append(ch)          # keep non-letters unchanged
    return "".join(result)


print("\n--- Exercise 3: Caesar Cipher ---")
print(f"  'ABC' shifted by 3:     '{caesar_cipher('ABC', 3)}'")
print(f"  'XYZ' shifted by 3:     '{caesar_cipher('XYZ', 3)}'")
print(f"  'Hello World' shifted by 5: '{caesar_cipher('Hello World', 5)}'")
print(f"  'Mjqqt Btwqi' shifted by -5: '{caesar_cipher('Mjqqt Btwqi', -5)}'")

# Verify: encrypting then decrypting with opposite shift gives original
original = "Attack at Dawn!"
encrypted = caesar_cipher(original, 13)
decrypted = caesar_cipher(encrypted, -13)
print(f"\n  Original:  '{original}'")
print(f"  Encrypted (k=13): '{encrypted}'")
print(f"  Decrypted (k=-13): '{decrypted}'")
print(f"  Round-trip works: {original == decrypted}")


# ---------- Exercise 4: Convert String to Alternating Case ----------
# Convert a string so that even-indexed characters are uppercase and
# odd-indexed characters are lowercase (index of letters only, skip
# non-letter characters in counting).
#
# Example: "hello world" -> "HeLlO wOrLd"
#
# Time : O(n)
# Space: O(n)

def alternating_case(s):
    """Convert to alternating case: even positions uppercase, odd lowercase."""
    result = []
    letter_index = 0
    for ch in s:
        if ch.isalpha():
            if letter_index % 2 == 0:
                result.append(ch.upper())
            else:
                result.append(ch.lower())
            letter_index += 1
        else:
            result.append(ch)          # keep spaces, digits, etc.
    return "".join(result)


print("\n--- Exercise 4: Alternating Case ---")
test_strings = ["hello world", "python programming", "abcdef", "Hi There!"]
for s in test_strings:
    print(f"  '{s}' -> '{alternating_case(s)}'")


print("\n" + "=" * 70)
print("  END OF FILE 10 — Characters, ASCII, and Character Patterns")
print("=" * 70)
