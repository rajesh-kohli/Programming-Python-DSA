###############################################################################
#                   13 - Strings and String Algorithms                         #
###############################################################################
#
# SOURCES:
#   Coding_Python/1. Python - Intro/14_strings.py        (439 lines)
#   LPLV26MAY/L16 - Strings/001stringOperations.py
#   LPLV26MAY/L16 - Strings/007stringInterpolation.py
#   LPLV26MAY/L16 - Strings/008checkPalindrome.py
#   LPLV26MAY/L16 - Strings/009ValidPalindrome.py
#   LPLV26MAY/L16 - Strings/010checkAnagram.py  (V1 sort)
#   LPLV26MAY/L16 - Strings/011checkAnagram2.py (V2 defaultdict)
#   LPLV26MAY/L16 - Strings/012checkAnagram3.py (V2b Counter)
#   LPLV26MAY/L16 - Strings/013checkAnagrams4.py (V3 freq array)
#   Whiteboard screenshot: Count Palindromic Substrings ("abaaba" → 11)
#
# TOPICS:
#   1. String Mechanics & I/O (immutability, indexing, split/join, interpolation)
#   2. Check Palindrome  — V1 slice O(n) space → V2 two-pointer O(1) space
#   3. Valid Palindrome  — two-pointer + .isalnum() skip logic
#   4. Check Anagram     — V1 sort → V2 hashmap → V3 26-element freq array
#   5. Count Palindromic Substrings — Expand Around Center O(n²)/O(1)
#   6. Practice Skeletons + Verified Driver (40 assertions)

from typing import List
from collections import defaultdict, Counter


# =============================================================================
# SECTION 1: String Mechanics & I/O
# =============================================================================
#
# IMMUTABILITY — THE MOST IMPORTANT RULE:
#   s[i] = 'x'  →  TypeError: 'str' object does not support item assignment
#   Every slice s[i:j] creates a NEW string. s[::-1] is O(n) time + O(n) space.
#   To build a modified string: accumulate chars in a list, "".join(lst) at end.
#   NEVER concatenate in a loop (s += ch) — that's O(n²) total.
#
# LEXICOGRAPHIC COMPARISON (ASCII-based, left to right):
#   'a'=97 .. 'z'=122  |  'A'=65 .. 'Z'=90  |  '0'=48 .. '9'=57
#   Compare char by char; if all match up to shorter length → shorter is less.
#
# SPLIT & JOIN:
#   s.split()        → split on whitespace, returns list of strings
#   s.split(",")     → split on delimiter
#   "".join(lst)     → canonical O(n) string builder from a list
#
# STRING INTERPOLATION — three generations, f-string is the modern standard:
#   OLD:  country + " gained independence in " + str(year) + "."
#   OLD:  "{} gained independence in {}.".format(country, year)
#   NEW:  f"{country} gained independence in {year}."  ← use this

def string_mechanics_demo():
    print("=" * 60)
    print("SECTION 1: String Mechanics & I/O")
    print("=" * 60)

    # ── Immutability ──
    s = "coding"
    print(f"\n  s = {repr(s)}")
    print(f"  s[0]   = {repr(s[0])}    ← O(1) read access")
    print(f"  s[-1]  = {repr(s[-1])}    ← last character (negative index)")
    print(f"  s[1:4] = {repr(s[1:4])}   ← slice creates a NEW string")
    print(f"  s[::-1]= {repr(s[::-1])}  ← full reverse, O(n) space")
    print(f"  s[::2] = {repr(s[::2])}    ← every-other-char")
    print(f"  Attempting s[0]='x': TypeError → strings are IMMUTABLE")

    # ── Lexicographic comparison ──
    print(f"\n  Lexicographic comparisons:")
    pairs = [("abc", "abd"), ("abc", "abcd"), ("abcd", "x"), ("Hello", "World")]
    for a, b in pairs:
        print(f"  {repr(a)} < {repr(b)} → {a < b}   "
              f"(first diff: {repr(next((x for x,y in zip(a,b) if x!=y),(None,None)[0]))})")

    # ── Split & Join ──
    print(f"\n  Split & Join (from your L16 whiteboard):")
    s2 = "a b c d"
    print(f"  {repr(s2)}.split()        → {s2.split()}")
    sports = "badminton,cricket,football,tennis"
    print(f"  sports.split(',')          → {sports.split(',')}")
    fruits = "apple, banana, orange, kiwi"
    print(f"  fruits.split(', ')         → {fruits.split(', ')}")
    chars = ['a', 'e', 's', 't', 't']
    print(f"  ''.join({chars})    → {repr(''.join(chars))}   ← anagram idiom")

    # ── String Interpolation ──
    print(f"\n  String interpolation (from your L16 whiteboard):")
    country, year = "India", 1947
    old_concat = country + " gained its independence in " + str(year) + "."
    old_format  = "{} gained its independence in {}.".format(country, year)
    new_fstring = f"{country} gained its independence in {year}."
    print(f"  concat:  {repr(old_concat)}")
    print(f"  format:  {repr(old_format)}")
    print(f"  f-string:{repr(new_fstring)}  ← standard")
    a, b = 10, 20
    print(f"  f'{{a}} + {{b}} = {{a+b}}' → {repr(f'{a} + {b} = {a+b}')}")

    # ── Essential methods ──
    print(f"\n  Essential methods on 'hi today is 8th July':")
    t = "hi today is 8th July"
    print(f"  .isalnum() = {t.isalnum()}   (False: has spaces)")
    print(f"  .isalpha() = {t.isalpha()}   (False: has digits+spaces)")
    print(f"  .islower() = {t.islower()}    (False: 'J' is upper)")
    print(f"  'today' in t = {'today' in t}")
    print(f"  .find('today') = {t.find('today')}")


# =============================================================================
# SECTION 2: Check Palindrome — V1 Slice vs V2 Two-Pointer
# =============================================================================
#
# PROBLEM: Given a string, determine if it reads the same forwards and backwards.
#   "racecar" → r a c e c a r → True  ✓
#   "abcdba"  → a b c d b a   → 'c' ≠ 'b' → False ✗
#
# V1 — SLICE REVERSAL: O(n) Time / O(n) Space
#   s == s[::-1]
#   s[::-1] allocates a COPY of the entire string (n chars) → O(n) space.
#   Then string comparison walks both strings → O(n) time (2n comparisons).
#
# V2 — TWO-POINTER: O(n) Time / O(1) Space  ← OPTIMAL
#   Whiteboard note: "n/2 comp: const → O(n)  space: O(1)"
#   Place i at left end, j at right end, walk toward the center:
#     - s[i] != s[j] → return False (not a palindrome)
#     - s[i] == s[j] → i++, j-- (keep checking)
#     - i >= j       → loop exits → return True
#
# Visual for "racecar":
#   i=0,j=6: 'r'=='r' ✓ → i=1,j=5
#   i=1,j=5: 'a'=='a' ✓ → i=2,j=4
#   i=2,j=4: 'c'=='c' ✓ → i=3,j=3
#   i=3,j=3: i==j → exit → True ✓
#
# Time: O(n) | Space V1: O(n)  Space V2: O(1)
# Source: Coding_Python/14_strings.py lines 237-261
#         LPLV26MAY/L16/008checkPalindrome.py

def is_palindrome_v1(s: str) -> bool:
    """
    V1: Slice reversal.
    Time: O(n) | Space: O(n) — allocates a reversed copy.
    Simple but wastes memory.
    """
    return s == s[::-1]


def is_palindrome_v2(s: str) -> bool:
    """
    V2: Two-pointer (OPTIMAL).
    Time: O(n) | Space: O(1) — only two index variables.
    n/2 comparisons (vs 2n for V1), same O(n) asymptotically but more efficient.
    Source: LPLV26MAY/L16/008checkPalindrome.py
    """
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False        # mismatch → not a palindrome
        i += 1
        j -= 1
    return True                 # all n/2 pairs matched → palindrome


def palindrome_demo():
    print("\n" + "=" * 60)
    print("SECTION 2: Check Palindrome")
    print("=" * 60)

    s_demo = "racecar"
    print(f"\n  s = {repr(s_demo)}")
    print(f"\n  V1 (slice): s == s[::-1]")
    print(f"    s[::-1]  = {repr(s_demo[::-1])}   ← new string (O(n) space)")
    print(f"    {repr(s_demo)} == {repr(s_demo[::-1])} → {s_demo == s_demo[::-1]}")
    print(f"\n  V2 (two-pointer): i=0, j=n-1, walk inward:")
    i, j = 0, len(s_demo) - 1
    while i < j:
        print(f"    i={i},j={j}: s[{i}]={repr(s_demo[i])} == s[{j}]={repr(s_demo[j])} "
              f"→ {'✓ advance' if s_demo[i]==s_demo[j] else '✗ mismatch → False'}")
        if s_demo[i] != s_demo[j]:
            break
        i += 1; j -= 1
    print(f"    i={i} >= j={j} → loop exits → True")

    bad = "abcdba"
    print(f"\n  s = {repr(bad)} (not a palindrome):")
    i2, j2 = 0, len(bad) - 1
    while i2 < j2:
        print(f"    i={i2},j={j2}: s[{i2}]={repr(bad[i2])} {'==' if bad[i2]==bad[j2] else '!='} "
              f"s[{j2}]={repr(bad[j2])} → {'advance' if bad[i2]==bad[j2] else 'return False ✗'}")
        if bad[i2] != bad[j2]:
            break
        i2 += 1; j2 -= 1

    tests = [
        ("racecar",  True),
        ("rotator",  True),
        ("wow",      True),
        ("abcba",    True),
        ("a",        True),
        ("abcdba",   False),
        ("hello",    False),
        ("abacaba",  True),
    ]
    print(f"\n  Verification (V1 == V2 for all cases):")
    print(f"  {'s':<15} {'V1':>5} {'V2':>5} {'exp':>5} {'ok':>3}")
    print("  " + "─" * 35)
    for s, exp in tests:
        v1 = is_palindrome_v1(s)
        v2 = is_palindrome_v2(s)
        ok = "✓" if v1 == exp and v2 == exp else "✗"
        print(f"  {repr(s):<15} {str(v1):>5} {str(v2):>5} {str(exp):>5} {ok:>3}")


# =============================================================================
# SECTION 3: Valid Palindrome — Two-Pointer + .isalnum() Skip
# =============================================================================
#
# PROBLEM (LeetCode 125): A phrase is a palindrome after lowercasing and
# removing non-alphanumeric characters.
#   "A man, a plan, a canal: Panama"  → "amanaplanacanalpanama" → True
#   "race a car"                      → "raceacar"              → False
#
# SKIP LOGIC — three-state while loop:
#   1. not s[i].isalnum() → skip: i += 1
#   2. not s[j].isalnum() → skip: j -= 1
#   3. both alphanumeric  → compare s[i].lower() vs s[j].lower()
#        - equal:   i++, j--
#        - unequal: return False
#   After loop exits (i >= j) → return True
#
# NOTE: The source in 14_strings.py line 307-308 has a bug:
#   "return True" is INDENTED INSIDE the while loop, causing it to return
#   True after just one matching iteration. The correct fix: return True
#   must be OUTSIDE the while loop (after it exits). Fixed below.
#
# Time: O(n) | Space: O(1) — no cleaned copy is ever built.
# Source: Coding_Python/14_strings.py lines 291-308 (with bug fix)
#         LPLV26MAY/L16/009ValidPalindrome.py (correct version)

def is_valid_palindrome(s: str) -> bool:
    """
    Valid palindrome ignoring non-alphanumeric characters and case.
    Time: O(n) | Space: O(1)
    Three-state skip logic: skip non-alnum on i, skip on j, then compare lower.
    Source: LPLV26MAY/L16/009ValidPalindrome.py
    """
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():
            i += 1              # State 1: skip non-alnum at left pointer
        elif not s[j].isalnum():
            j -= 1              # State 2: skip non-alnum at right pointer
        else:
            if s[i].lower() != s[j].lower():
                return False    # State 3a: both alnum, mismatch
            i += 1              # State 3b: both alnum, match → advance both
            j -= 1
    return True                 # ← OUTSIDE the loop (source had this bug inside)


def valid_palindrome_demo():
    print("\n" + "=" * 60)
    print("SECTION 3: Valid Palindrome (.isalnum() Skip Logic)")
    print("=" * 60)

    s_demo = "A man, a plan, a canal: Panama"
    print(f"\n  s = {repr(s_demo)}")
    print(f"  After cleaning: {''.join(c.lower() for c in s_demo if c.isalnum())!r}")
    print(f"\n  Three-state skip logic (first few steps):")
    i, j = 0, len(s_demo) - 1
    steps = 0
    while i < j and steps < 7:
        if not s_demo[i].isalnum():
            print(f"    i={i}:{repr(s_demo[i])} not alnum → skip i, i={i+1}")
            i += 1
        elif not s_demo[j].isalnum():
            print(f"    j={j}:{repr(s_demo[j])} not alnum → skip j, j={j-1}")
            j -= 1
        else:
            cmp = "✓" if s_demo[i].lower() == s_demo[j].lower() else "✗"
            print(f"    i={i}:{repr(s_demo[i].lower())} == j={j}:{repr(s_demo[j].lower())} {cmp}")
            if s_demo[i].lower() != s_demo[j].lower():
                break
            i += 1; j -= 1
        steps += 1
    print(f"    ... continues until i>=j → True")

    print(f"\n  BUG NOTE from 14_strings.py line 307:")
    print(f"    'return True' was INDENTED inside the while loop →")
    print(f"    would return True after just 1 matching iteration!")
    print(f"    FIX: 'return True' must be OUTSIDE (after) the while loop.")

    tests = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car",                     False),
        ("",                               True),   # empty string
        (" ",                              True),   # only whitespace
        (".,",                             True),   # only punctuation
        ("Was it a car or a cat I saw?",   True),
        ("No lemon, no melon",             True),
    ]
    print(f"\n  Verification:")
    print(f"  {'s':<37} {'result':>6} {'exp':>6} {'ok':>3}")
    print("  " + "─" * 55)
    for s, exp in tests:
        result = is_valid_palindrome(s)
        ok = "✓" if result == exp else "✗"
        print(f"  {repr(s):<37} {str(result):>6} {str(exp):>6} {ok:>3}")


# =============================================================================
# SECTION 4: Check Anagram — 3-Step Evolution
# =============================================================================
#
# PROBLEM: Given two strings of lowercase letters, check if they are anagrams
# (same characters with same frequencies).
#   "state" & "taste"    → True   (same chars, same counts)
#   "abacbac" & "aabbbcc" → False
#
# ── V1: Sorting ── O(n log n) Time / O(n) Space
#   sorted(s) → returns a list of chars in sorted order
#   "".join(sorted(s)) → builds sorted string
#   Compare sorted strings: if equal → anagram
#   Cost: nlogn (sort s1) + nlogn (sort s2) + n (compare) = O(nlogn)
#   Space: O(n) for each sorted copy
#
# ── V2: Hash Map (defaultdict / Counter) ── O(n) Time / O(1)* Space
#   Build frequency map for each string, compare maps.
#   *O(1) in practice (at most 26 keys for lowercase letters)
#   Counter(s1) == Counter(s2) is the most concise form.
#
# ── V3: 26-Element Frequency Array ── O(n) Time / O(1) Space ← OPTIMAL
#   Map each letter to index via: ord(ch) - ord('a')
#     'a' → 0,  'b' → 1,  'c' → 2,  ...  'z' → 25
#   Build freq1[26] for s1, freq2[26] for s2, compare.
#   WHY FASTER THAN DICT:
#     - Fixed size (26) → no dynamic resizing / hashing
#     - Direct memory offset lookup (O(1) with smaller constant)
#     - Comparison is always exactly 26 operations = O(1)
#   From your whiteboard: ord(ch)-ord('a') → idx
#     ch='a' → 97-97=0,  ch='b' → 98-97=1,  ch='c' → 99-97=2
#
# Source: Coding_Python/14_strings.py lines 331-431
#         LPLV26MAY/L16/010..013checkAnagram*.py

def is_anagram_v1(s1: str, s2: str) -> bool:
    """
    V1: Sort both strings and compare.
    Time: O(n log n) | Space: O(n)
    Source: LPLV26MAY/L16/010checkAnagram.py
    """
    return "".join(sorted(s1)) == "".join(sorted(s2))


def is_anagram_v2_dict(s1: str, s2: str) -> bool:
    """
    V2a: Two defaultdicts (frequency maps).
    Time: O(n) | Space: O(1)* — at most 26 keys for lowercase letters.
    Source: LPLV26MAY/L16/011checkAnagram2.py
    """
    f1: defaultdict = defaultdict(int)
    for ch in s1:
        f1[ch] += 1
    f2: defaultdict = defaultdict(int)
    for ch in s2:
        f2[ch] += 1
    return f1 == f2


def is_anagram_v2_counter(s1: str, s2: str) -> bool:
    """
    V2b: Counter — most concise hash-map form.
    Time: O(n) | Space: O(1)*
    Source: LPLV26MAY/L16/012checkAnagram3.py
    """
    return Counter(s1) == Counter(s2)


def is_anagram_v3(s1: str, s2: str) -> bool:
    """
    V3: 26-element frequency array (OPTIMAL).
    Time: O(n) | Space: O(1) — exactly 26 integers, always.
    Key: idx = ord(ch) - ord('a')  maps 'a'→0, 'b'→1, ..., 'z'→25
    Source: LPLV26MAY/L16/013checkAnagrams4.py
    """
    if len(s1) != len(s2):         # early exit: different lengths → not anagram
        return False
    f1 = [0] * 26
    f2 = [0] * 26
    for ch in s1:
        f1[ord(ch) - ord('a')] += 1    # shift by ord('a')=97 → zero-indexed
    for ch in s2:
        f2[ord(ch) - ord('a')] += 1
    return f1 == f2                # compare exactly 26 elements → O(1)


def anagram_demo():
    print("\n" + "=" * 60)
    print("SECTION 4: Check Anagram (3-Step Evolution)")
    print("=" * 60)

    s1_demo, s2_demo = "state", "taste"
    print(f"\n  s1={repr(s1_demo)}, s2={repr(s2_demo)}")

    # V1 trace
    sorted1 = "".join(sorted(s1_demo))
    sorted2 = "".join(sorted(s2_demo))
    print(f"\n  V1 (Sort): O(n log n) / O(n)")
    print(f"    sorted(s1) → {sorted(s1_demo)} → join → {repr(sorted1)}")
    print(f"    sorted(s2) → {sorted(s2_demo)} → join → {repr(sorted2)}")
    print(f"    {repr(sorted1)} == {repr(sorted2)} → {sorted1 == sorted2}")

    # V2 trace
    print(f"\n  V2 (defaultdict): O(n) / O(1)*")
    f1_d: defaultdict = defaultdict(int)
    for ch in s1_demo: f1_d[ch] += 1
    f2_d: defaultdict = defaultdict(int)
    for ch in s2_demo: f2_d[ch] += 1
    print(f"    f1 = {dict(f1_d)}")
    print(f"    f2 = {dict(f2_d)}")
    print(f"    f1 == f2 → {f1_d == f2_d}")

    # V3 trace
    print(f"\n  V3 (26-element freq array): O(n) / O(1)  ← OPTIMAL")
    print(f"  ord(ch) - ord('a') mapping:")
    for ch in sorted(set(s1_demo)):
        print(f"    '{ch}' → ord('{ch}')={ord(ch)} - ord('a')={ord('a')} = {ord(ch)-ord('a')}")
    f1_arr = [0] * 26
    f2_arr = [0] * 26
    for ch in s1_demo: f1_arr[ord(ch) - ord('a')] += 1
    for ch in s2_demo: f2_arr[ord(ch) - ord('a')] += 1
    non_zero1 = {chr(i+97): f1_arr[i] for i in range(26) if f1_arr[i]}
    non_zero2 = {chr(i+97): f2_arr[i] for i in range(26) if f2_arr[i]}
    print(f"    f1 (non-zero) = {non_zero1}")
    print(f"    f2 (non-zero) = {non_zero2}")
    print(f"    f1 == f2 → {f1_arr == f2_arr}")

    print(f"\n  Why freq array beats dict:")
    print(f"    Dict: hashing + dynamic sizing + pointer indirection")
    print(f"    Array: direct memory offset, fixed 26 slots, constant-size compare")
    print(f"    Use array as map when key space is small and known (a-z = 26 keys)")

    tests = [
        ("state",   "taste",   True),
        ("abacbac", "aabbbcc", False),
        ("anagram", "nagaram", True),
        ("rat",     "car",     False),
        ("a",       "a",       True),
        ("ab",      "ba",      True),
        ("ab",      "abc",     False),   # different lengths
        ("",        "",        True),
    ]
    print(f"\n  Verification (all 3 versions must agree):")
    print(f"  {'s1':<10} {'s2':<10} {'V1':>5} {'V2':>5} {'V3':>5} {'exp':>5} {'ok':>3}")
    print("  " + "─" * 47)
    for s1, s2, exp in tests:
        v1 = is_anagram_v1(s1, s2)
        v2 = is_anagram_v2_dict(s1, s2)
        v3 = is_anagram_v3(s1, s2)
        ok = "✓" if v1 == exp and v2 == exp and v3 == exp else "✗"
        print(f"  {repr(s1):<10} {repr(s2):<10} {str(v1):>5} {str(v2):>5} "
              f"{str(v3):>5} {str(exp):>5} {ok:>3}")


# =============================================================================
# SECTION 5: Count Palindromic Substrings — Expand Around Center
# =============================================================================
#
# PROBLEM (from whiteboard screenshot):
#   Given string s, count the number of substrings that are palindromes.
#   Input: s = "abaaba"   Output: 11
#
# ALL 11 palindromic substrings of "abaaba":
#   Single chars (6): "a"[0], "b"[1], "a"[2], "a"[3], "b"[4], "a"[5]
#   Length 2 (1): "aa"[2:4]
#   Length 3 (2): "aba"[0:3], "aba"[3:6]
#   Length 4 (1): "baab"[1:5]
#   Length 6 (1): "abaaba"[0:6]
#   Total = 6 + 1 + 2 + 1 + 1 = 11 ✓
#
# BRUTE FORCE: O(n³)
#   Generate all O(n²) substrings, check each in O(n) → total O(n³). Too slow.
#
# OPTIMAL: EXPAND AROUND CENTER — O(n²) Time / O(1) Space
#
# CORE INSIGHT:
#   Every palindrome has a center. Expand outward from each center, counting
#   palindromes as the expansion succeeds.
#
# TWO TYPES OF CENTERS:
#   1. ODD-LENGTH palindromes: center is a single character
#      "aba" → center = 'b' at index 1 → L=R=1
#   2. EVEN-LENGTH palindromes: center is a gap between two characters
#      "aa"  → center = gap between idx 0 and 1 → L=0, R=1
#
# For string of length n: n odd centers + (n-1) even centers = 2n-1 total centers.
#
# THE EXPAND FUNCTION:
#   Given (L, R):
#     while L >= 0 and R < n and s[L] == s[R]:
#         count += 1      ← this is a valid palindrome
#         L -= 1          ← expand outward
#         R += 1
#
# VISUAL TRACE for "abaaba" — even center between idx 2 and 3:
#   L=2,R=3: s[2]='a'==s[3]='a' → count++ ("aa"), L=1,R=4
#   L=1,R=4: s[1]='b'==s[4]='b' → count++ ("baab"), L=0,R=5
#   L=0,R=5: s[0]='a'==s[5]='a' → count++ ("abaaba"), L=-1 → stop
#   → 3 palindromes from this one center ✓
#
# FULL CENTER TABLE for "abaaba" (n=6, 11 centers):
#   Center 0 (odd):  "a"                             → 1
#   Center 0→1 (even): 'a'≠'b'                      → 0
#   Center 1 (odd):  "b", "aba"                      → 2
#   Center 1→2 (even): 'b'≠'a'                      → 0
#   Center 2 (odd):  "a"                             → 1
#   Center 2→3 (even): "aa","baab","abaaba"          → 3
#   Center 3 (odd):  "a"                             → 1
#   Center 3→4 (even): 'a'≠'b'                      → 0
#   Center 4 (odd):  "b", "aba"                      → 2
#   Center 4→5 (even): 'b'≠'a'                      → 0
#   Center 5 (odd):  "a"                             → 1
#   Total = 1+0+2+0+1+3+1+0+2+0+1 = 11 ✓
#
# Time: O(n²) | Space: O(1)
# Source: Coding_Python/14_strings.py line 435-439 (problem stated, not solved)
#         Whiteboard screenshot — "Count Palindromic Substrings" hw problem

def count_palindromic_substrings(s: str) -> int:
    """
    Count all palindromic substrings using Expand Around Center.
    Time: O(n²) | Space: O(1)
    For each of the 2n-1 centers, expand outward while s[L]==s[R].
    Each successful expansion = 1 new palindrome found.
    """
    n = len(s)
    count = 0

    def expand(L: int, R: int) -> int:
        """Expand from center (L,R), return count of palindromes found."""
        found = 0
        while L >= 0 and R < n and s[L] == s[R]:
            found += 1      # [s[L]..s[R]] is a palindrome
            L -= 1          # expand outward
            R += 1
        return found

    for i in range(n):
        count += expand(i, i)       # ODD-length centers: single char
        count += expand(i, i + 1)   # EVEN-length centers: gap between i and i+1

    return count


def palindromic_substrings_demo():
    print("\n" + "=" * 60)
    print("SECTION 5: Count Palindromic Substrings")
    print("=" * 60)

    s = "abaaba"
    n = len(s)
    print(f"\n  s = {repr(s)}")
    print(f"  n = {n}  →  {n} odd centers + {n-1} even centers = {2*n-1} total centers")

    # Full center trace
    print(f"\n  Expand-Around-Center trace (each row = one center):")
    print(f"  {'center':<16} {'type':<8} {'L,R start':<12} {'palindromes':<30} {'count':>5}")
    print("  " + "─" * 73)
    total = 0
    for i in range(n):
        # Odd center
        L, R = i, i
        pals = []
        while L >= 0 and R < n and s[L] == s[R]:
            pals.append(repr(s[L:R+1]))
            L -= 1; R += 1
        cnt = len(pals)
        total += cnt
        print(f"  i={i} '{s[i]}'          {'odd':<8} L=R={i:<8}   {', '.join(pals) or '(none)':<30} {cnt:>5}")

        # Even center
        if i < n - 1:
            L, R = i, i + 1
            pals_e = []
            while L >= 0 and R < n and s[L] == s[R]:
                pals_e.append(repr(s[L:R+1]))
                L -= 1; R += 1
            cnt_e = len(pals_e)
            total += cnt_e
            print(f"  i={i}→{i+1} gap         {'even':<8} L={i},R={i+1:<5}   "
                  f"{', '.join(pals_e) or '(none)':<30} {cnt_e:>5}")

    print(f"  {'─'*73}")
    print(f"  {'TOTAL':<61} {total:>5}")
    print(f"\n  Answer = {total} ✓  (matches whiteboard screenshot Output: 11)")

    # List all palindromes via brute force for verification
    all_pals = [s[i:j] for i in range(n) for j in range(i+1, n+1)
                if s[i:j] == s[i:j][::-1]]
    print(f"\n  Brute-force verification: {len(all_pals)} palindromes found")
    print(f"  Palindromes: {all_pals}")

    tests = [
        ("abaaba", 11),     # ← from whiteboard screenshot
        ("a",       1),     # single char
        ("aa",      3),     # "a","a","aa"
        ("abc",     3),     # only single chars
        ("aaa",     6),     # "a","a","a","aa","aa","aaa"
        ("aba",     4),     # "a","b","a","aba"
        ("racecar", 10),
    ]
    print(f"\n  Verification:")
    print(f"  {'s':<12} {'result':>6} {'exp':>6} {'ok':>3}")
    print("  " + "─" * 28)
    for s_t, exp in tests:
        result = count_palindromic_substrings(s_t)
        ok = "✓" if result == exp else "✗"
        print(f"  {repr(s_t):<12} {result:>6} {exp:>6} {ok:>3}")


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_is_palindrome(s: str) -> bool:
    """
    Check if s is a palindrome using the O(1) space two-pointer approach.
    Time: O(n) | Space: O(1)
    Hint: i=0, j=len(s)-1; while i<j: compare s[i] vs s[j]; advance or return False
    """
    pass


def practice_is_valid_palindrome(s: str) -> bool:
    """
    Valid palindrome: ignore non-alphanumeric, case-insensitive.
    Time: O(n) | Space: O(1)
    Hint: three-state while loop — skip non-alnum on i, skip on j, compare lower
    """
    pass


def practice_is_anagram_v1(s1: str, s2: str) -> bool:
    """
    Check anagram via sorting.
    Time: O(n log n) | Space: O(n)
    Hint: "".join(sorted(s)) creates a sorted string; compare both
    """
    pass


def practice_is_anagram_v3(s1: str, s2: str) -> bool:
    """
    Check anagram via 26-element frequency array (optimal).
    Time: O(n) | Space: O(1)
    Hint: idx = ord(ch) - ord('a'); build f1[] for s1, f2[] for s2; return f1==f2
    """
    pass


def practice_count_palindromic_substrings(s: str) -> int:
    """
    Count palindromic substrings via Expand Around Center.
    Time: O(n²) | Space: O(1)
    Hint: for each i, expand(i,i) for odd + expand(i,i+1) for even centers
    """
    pass


# =============================================================================
# DRIVER — Verifies all optimal implementations + shows skeleton stubs
# =============================================================================
if __name__ == "__main__":
    string_mechanics_demo()
    palindrome_demo()
    valid_palindrome_demo()
    anagram_demo()
    palindromic_substrings_demo()

    print("\n" + "=" * 60)
    print("OPTIMAL SOLUTION VERIFICATION")
    print("=" * 60)

    # ── Check Palindrome (V1 + V2) ──
    pal_tests = [
        ("racecar",  True),
        ("rotator",  True),
        ("wow",      True),
        ("abcba",    True),
        ("a",        True),
        ("abcdba",   False),
        ("hello",    False),
        ("abacaba",  True),
    ]
    for s, exp in pal_tests:
        assert is_palindrome_v1(s) == exp, f"v1 failed on {repr(s)}"
        assert is_palindrome_v2(s) == exp, f"v2 failed on {repr(s)}"
    print(f"\n  is_palindrome_v1: {len(pal_tests)} assertions ✓")
    print(f"  is_palindrome_v2: {len(pal_tests)} assertions ✓")

    # ── Valid Palindrome ──
    valid_pal_tests = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car",                     False),
        ("",                               True),
        (" ",                              True),
        (".,",                             True),
        ("Was it a car or a cat I saw?",   True),
        ("No lemon, no melon",             True),
    ]
    for s, exp in valid_pal_tests:
        assert is_valid_palindrome(s) == exp, f"valid_pal failed on {repr(s)}"
    print(f"  is_valid_palindrome: {len(valid_pal_tests)} assertions ✓")

    # ── Check Anagram (all 3 versions) ──
    anagram_tests = [
        ("state",   "taste",   True),
        ("abacbac", "aabbbcc", False),
        ("anagram", "nagaram", True),
        ("rat",     "car",     False),
        ("a",       "a",       True),
        ("ab",      "ba",      True),
        ("ab",      "abc",     False),
        ("",        "",        True),
    ]
    for s1, s2, exp in anagram_tests:
        assert is_anagram_v1(s1, s2)       == exp, f"v1 failed on ({s1},{s2})"
        assert is_anagram_v2_dict(s1, s2)  == exp, f"v2_dict failed on ({s1},{s2})"
        assert is_anagram_v2_counter(s1,s2)== exp, f"v2_counter failed on ({s1},{s2})"
        assert is_anagram_v3(s1, s2)       == exp, f"v3 failed on ({s1},{s2})"
    print(f"  is_anagram_v1:        {len(anagram_tests)} assertions ✓")
    print(f"  is_anagram_v2_dict:   {len(anagram_tests)} assertions ✓")
    print(f"  is_anagram_v2_counter:{len(anagram_tests)} assertions ✓")
    print(f"  is_anagram_v3:        {len(anagram_tests)} assertions ✓")

    # ── Count Palindromic Substrings ──
    cps_tests = [
        ("abaaba", 11),     # ← from whiteboard screenshot
        ("a",       1),
        ("aa",      3),
        ("abc",     3),
        ("aaa",     6),
        ("aba",     4),
        ("racecar", 10),
    ]
    for s, exp in cps_tests:
        assert count_palindromic_substrings(s) == exp, \
            f"count_pal_substrings failed on {repr(s)}: got {count_palindromic_substrings(s)}"
    print(f"  count_palindromic_substrings: {len(cps_tests)} assertions ✓")
    print(f"    ↳ 'abaaba' == 11 ✓  (your homework problem)")

    total_assertions = (len(pal_tests) * 2 + len(valid_pal_tests) +
                        len(anagram_tests) * 4 + len(cps_tests))
    print(f"\n  {'─'*40}")
    print(f"  Total verified assertions: {total_assertions} ✓")
    print(f"  {'─'*40}")

    # ── Practice skeleton stubs ──
    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS (return None until implemented)")
    print("=" * 60)
    print(f"\n  practice_is_palindrome('racecar')         = "
          f"{practice_is_palindrome('racecar')}")
    print(f"  practice_is_valid_palindrome('A man...')   = "
          f"{practice_is_valid_palindrome('A man, a plan, a canal: Panama')}")
    print(f"  practice_is_anagram_v1('state','taste')    = "
          f"{practice_is_anagram_v1('state','taste')}")
    print(f"  practice_is_anagram_v3('state','taste')    = "
          f"{practice_is_anagram_v3('state','taste')}")
    print(f"  practice_count_palindromic_substrings('abaaba') = "
          f"{practice_count_palindromic_substrings('abaaba')}")
    print("=" * 60)
    print("Fill in the skeletons above and re-run to verify.")
