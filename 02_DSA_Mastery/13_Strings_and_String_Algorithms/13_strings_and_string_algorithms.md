# 13 - Strings and String Algorithms

## Why This Module Matters

Strings appear in nearly every technical interview. They look simple, but they conceal a dense set of tricks: immutability, ASCII arithmetic, the two-pointer skip pattern for messy input, and the "expand-around-center" technique that turns an O(n²) palindrome search into an elegant linear-pass algorithm. This module builds from foundational mechanics all the way to a homework-level interview problem.

---

## 1. String Mechanics

### 1.1 Immutability — The Most Important Rule

A Python string is a **fixed sequence of characters that cannot be modified in place**.

```python
s = "coding"
s[0] = "x"     # TypeError: 'str' object does not support item assignment
```

**What this means for algorithms:**
- You can **read** `s[i]` in O(1).
- You **cannot write** `s[i] = c`.
- To "build" a modified string, accumulate into a list and call `"".join(lst)` at the end — this is O(n) and the canonical pattern.
- Every slice `s[i:j]` creates a **new string** (a copy). `s[::-1]` is O(n) time and O(n) space.

**Why it matters for interviews:** Never say "sort the string in-place." Always sort `sorted(s)` (returns a list) and rejoin. This is the source of half the bugs in string-based interview solutions.

### 1.2 Indexing and Slicing

```python
s = "coding"            # indices: 0 1 2 3 4 5
                        #          c o d i n g
print(s[0])             # 'c'   — first character
print(s[-1])            # 'g'   — last character (negative indexing)
print(s[1:4])           # 'odi' — s[1], s[2], s[3] (end index is exclusive)
print(s[::-1])          # 'gnidoc' — full reverse; step = -1
print(s[::2])           # 'cdn'   — every other character
```

**Slice rule:** `s[start:end:step]` — end is **exclusive**, step defaults to 1.

### 1.3 Looping Over Strings

```python
# for-each (most common in interviews)
for ch in s:
    print(ch)

# index-based (needed when you want position)
for i in range(len(s)):
    print(s[i])

# while loop (needed for two-pointer patterns)
i, j = 0, len(s) - 1
while i < j:
    ...
```

### 1.4 Lexicographical Comparison (ASCII Order)

Python compares strings **character by character**, left to right, using ASCII values.

```
'a' = 97,  'b' = 98,  ...  'z' = 122
'A' = 65,  'B' = 66,  ...  'Z' = 90
'0' = 48,  '1' = 49,  ...  '9' = 57
```

**Rules:**
1. Compare `s1[0]` vs `s2[0]`. If different → the one with the smaller ASCII value is "less".
2. If equal, compare the next character.
3. If all characters match up to the shorter string's length → the **shorter** string is "less".

```python
"abc" < "abd"   # True: 'c'(99) < 'd'(100)
"abc" < "abcd"  # True: "abc" is a prefix of "abcd" and shorter
"abcd" < "x"    # True: 'a'(97) < 'x'(120)
"Hello" < "World"  # True: 'H'(72) < 'W'(87)
```

**Time complexity of string comparison:** O(n) where n is the length of the shorter string.

### 1.5 Essential String Methods

| Method | What it does | Example |
|---|---|---|
| `len(s)` | Length | `len("abc")` → 3 |
| `s.upper()` / `s.lower()` | Case conversion | `"Hello".lower()` → `"hello"` |
| `s.strip()` | Remove leading/trailing whitespace | `"  hi  ".strip()` → `"hi"` |
| `s.find(sub)` | Index of first occurrence, -1 if not found | `"abcabc".find("c")` → 2 |
| `s.replace(old, new)` | Replace all occurrences | `"aab".replace("a","x")` → `"xxb"` |
| `s.isalnum()` | True if all chars are letters or digits | `"abc123".isalnum()` → True |
| `s.isalpha()` | True if all chars are letters | `"abc".isalpha()` → True |
| `s.isdigit()` | True if all chars are digits | `"123".isdigit()` → True |
| `s.islower()` / `s.isupper()` | Case check | `"abc".islower()` → True |
| `"sub" in s` | Membership test | `"bc" in "abcd"` → True |

**Prefer `find` over `index`:** `index` raises a `ValueError` if the substring is missing; `find` returns `-1`. Always prefer `find` to avoid needing a try-except block.

---

## 2. Split and Join

### 2.1 Splitting — String → List

`s.split(delimiter)` splits a string on the delimiter and returns a **list of strings**.
- No delimiter → splits on **any whitespace** and discards empty strings.

```python
s = "a b c d"
s.split()           # ['a', 'b', 'c', 'd']    ← whitespace split

sports = "badminton,cricket,football,tennis"
sports.split(",")   # ['badminton', 'cricket', 'football', 'tennis']

fruits = "apple, banana, orange, kiwi"
fruits.split(", ")  # ['apple', 'banana', 'orange', 'kiwi']

# Input parsing pattern (from your L16 notes):
# "10 20 30 40 50"
# input().split()  →  ['10', '20', '30', '40', '50']
# list(map(int, input().split()))  →  [10, 20, 30, 40, 50]
```

### 2.2 Joining — List → String

`delimiter.join(list_of_strings)` merges a list of strings with the delimiter.

```python
chars = ['a', 'e', 's', 't', 't']      # sorted chars of "state"
"".join(chars)      # 'aestt'   ← anagram comparison idiom

words = ["apple", "banana", "cherry"]
", ".join(words)    # 'apple, banana, cherry'
" ".join(words)     # 'apple banana cherry'
```

> [!IMPORTANT]
> `"".join(list)` is the canonical way to build a string from characters. It runs in **O(n)** total. Never concatenate strings in a loop (`s += ch`) — each `+=` creates a new string object, making it O(n²) total.

---

## 3. String Interpolation

**Three approaches — same output, different readability:**

```python
country = "India"
year = 1947

# ❌ Old: string concatenation — requires explicit str() conversion
result = country + " gained its independence in " + str(year) + "."

# ⚠️  Old: .format() — positional, readable but verbose
result = "{} gained its independence in {}.".format(country, year)

# ✅ Modern: f-strings — evaluated at runtime, fastest, most readable
result = f"{country} gained its independence in {year}."
# Output: "India gained its independence in 1947."

# f-strings can embed full expressions:
a, b = 10, 20
print(f"{a} + {b} = {a + b}")   # "10 + 20 = 30"
```

**f-strings are the interview and production standard.** They are:
- Available since Python 3.6
- Faster than `%` formatting and `.format()` (evaluated at parse time, no function call overhead)
- More readable — the variable is right next to its placeholder

---

## 4. Algorithm 1 — Check Palindrome

**Problem:** Given a string, determine if it reads the same forwards and backwards.

**Definition:** A string `s` is a palindrome if `s[i] == s[n-1-i]` for all `i` from `0` to `n//2 - 1`.

```
"racecar" → r-a-c-e-c-a-r ✓
"rotator" → r-o-t-a-t-o-r ✓
"abcdba" → a-b-c-d-b-a → 'c' ≠ 'b' → False ✗
```

### V1 — Slice Reversal: O(n) Time / O(n) Space

```python
def is_palindrome_v1(s: str) -> bool:
    return s == s[::-1]   # s[::-1] creates a reversed COPY of the full string
```

- `s[::-1]` allocates a new string of length n → **O(n) space**.
- String comparison `s == s[::-1]` walks both strings → **O(n) time** (2n comparisons).
- Simple, elegant, but **wastes memory** — a concern in memory-limited systems.

### V2 — Two-Pointer: O(n) Time / O(1) Space ← **OPTIMAL**

**Mental model from your whiteboard:** Place pointer `i` at the left end and `j` at the right end. Walk them toward the center, comparing `s[i]` and `s[j]`. Stop if they mismatch. Stop if `i >= j` (all comparisons passed).

```
"abcdba"
 i         j       s[0]='a' == s[5]='a' ✓ → i++, j--
  i       j        s[1]='b' == s[4]='b' ✓ → i++, j--
   i     j         s[2]='c' != s[3]='d' → return False ✗

"racecar"
 i      j          s[0]='r' == s[6]='r' ✓
  i    j           s[1]='a' == s[5]='a' ✓
   i  j            s[2]='c' == s[4]='c' ✓
    ij             i == j (center 'e') → loop exits → return True ✓
```

- **n/2 comparisons** (half the work of V1's 2n comparisons), still O(n) asymptotically.
- **O(1) space** — only two integer variables.

> [!TIP]
> In interviews, always present V2. The space complexity difference from O(n) to O(1) is the entire point of the question. Your whiteboard note says it perfectly: "n/2 comp: const → O(n) space: O(1)".

**Complexity:**
- V1: Time O(n) | Space **O(n)** (reversed copy)
- V2: Time O(n) | Space **O(1)** ← optimal

---

## 5. Algorithm 2 — Valid Palindrome (LeetCode 125)

**Problem:** A phrase is a palindrome if, after lowercasing and removing all non-alphanumeric characters, it reads the same forwards and backwards.

```
"A man, a plan, a canal: Panama"  →  "amanaplanacanalpanama"  →  True ✓
"race a car"                      →  "raceacar"               →  False ✗
```

### Two-Pointer Skip Logic

The key insight: **skip non-alphanumeric characters on the fly** using `.isalnum()`.

```
i → right if s[i] is non-alphanumeric
j ← left  if s[j] is non-alphanumeric
compare s[i].lower() vs s[j].lower() only when BOTH are alphanumeric
```

**Three-state logic of the inner `while`:**
1. `not s[i].isalnum()` → skip: `i += 1`
2. `not s[j].isalnum()` → skip: `j -= 1`
3. Both are alphanumeric → compare lowercased:
   - Equal → `i += 1`, `j -= 1`
   - Unequal → `return False`

**Complexity:** Time O(n) | Space O(1) — no cleaned copy is ever built.

> [!NOTE]
> The `14_strings.py` source has a subtle bug: `return True` is indented inside the `while` loop, causing it to return True after just one iteration. The correct placement is **after** the loop exits. The fix is shown in the `.py` file.

---

## 6. Algorithm 3 — Check Anagrams (3-Step Evolution)

**Problem:** Given two strings of lowercase letters, determine if one is an anagram of the other. (An anagram uses exactly the same characters with the same frequencies.)

```
"state" and "taste"    →  True  (same chars, same counts)
"abacbac" and "aabbbcc" →  False (different counts)
```

### V1 — Sorting: O(n log n) Time / O(n) Space

```python
def is_anagram_v1(s1, s2):
    return "".join(sorted(s1)) == "".join(sorted(s2))
    # "state" → sorted → ['a','e','s','t','t'] → "".join → "aestt"
    # "taste" → "aestt"  →  "aestt" == "aestt" → True ✓
```

- `sorted(s)` returns a list → `"".join(...)` builds a new string → **O(n) space** per string.
- Total: O(n log n) sort + O(n) compare. Space: O(n).

### V2 — Hash Map (defaultdict): O(n) Time / O(1)* Space

```python
# V2a: two defaultdicts
f1 = defaultdict(int)
for ch in s1: f1[ch] += 1
f2 = defaultdict(int)
for ch in s2: f2[ch] += 1
return f1 == f2

# V2b: single dict, increment for s1, decrement for s2, check all zeros
freq = {}
for ch in s1: freq[ch] = freq.get(ch, 0) + 1
for ch in s2: freq[ch] = freq.get(ch, 0) - 1
return all(v == 0 for v in freq.values())
```

*Space is O(1) in practice because the dict holds at most 26 keys (lowercase letters). But technically it's O(k) where k is the alphabet size.

### V3 — 26-Element Frequency Array: O(n) Time / O(1) Space ← **OPTIMAL**

**The key insight from your whiteboard:** Map each lowercase letter to an array index using `ord(ch) - ord('a')`.

```
ord('a') = 97,  ord('a') - ord('a') = 0  → index 0
ord('b') = 98,  ord('b') - ord('a') = 1  → index 1
ord('c') = 99,  ord('c') - ord('a') = 2  → index 2
...
ord('z') = 122, ord('z') - ord('a') = 25 → index 25
```

```python
# s1="abbc", freq array trace:
freq = [0]*26
# 'a' → idx=0 → freq[0]+=1 → [1,0,0,...]
# 'b' → idx=1 → freq[1]+=1 → [1,1,0,...]
# 'b' → idx=1 → freq[1]+=1 → [1,2,0,...]
# 'c' → idx=2 → freq[2]+=1 → [1,2,1,...]

# s2="bbac", freq2 array:
# 'b'→1, 'b'→1, 'a'→0, 'c'→2
# freq2 = [1,2,1,...] → freq1 == freq2 → True ✓
```

**Why freq array beats dict:**
- Fixed size (26) → no hashing overhead, no dynamic resizing
- Array element access is direct memory offset → faster than hash lookup
- Comparing two 26-element arrays is a fixed O(26) = O(1) operation

**Complexity:**
| Version | Time | Space |
|---|---|---|
| V1 — Sort | O(n log n) | O(n) |
| V2 — Hash Map | O(n) | O(1)* |
| V3 — Freq Array | **O(n)** | **O(1)** ← optimal |

---

## 7. Algorithm 4 — Count Palindromic Substrings [Homework]

**Problem:** Given a string `s`, count the number of substrings that are palindromes.

```
Input:  s = "abaaba"   (indices 0..5)
Output: 11
```

**All 11 palindromic substrings of "abaaba":**
```
Single chars (6): "a"[0], "b"[1], "a"[2], "a"[3], "b"[4], "a"[5]
Length 3  (3):    "aba"[0:3], "aab"? No → "aba"[1:4]? No → "aba"[3:6]
                  Actually: "aba"[0:3], "a"→"aa"[2:4], "aba"[3:6]
Length 4  (1):    "baab"[1:5]
Length 6  (1):    "abaaba"[0:6]
Total = 6 + 2 + 1 + 1 + 1 = 11 ✓
```

### Brute Force: O(n²) substrings × O(n) palindrome check = **O(n³)**

Generate all `O(n²)` substrings, check each with a full scan. Too slow for n > 1000.

### Optimal: Expand Around Center — O(n²) Time / O(1) Space

**Core insight:** Every palindrome has a **center**. Expand outward from each possible center, counting palindromes as you go.

**Two types of centers:**
1. **Odd-length palindromes** — center is a **single character** (e.g., "aba" centered at 'b')
2. **Even-length palindromes** — center is a **gap between two characters** (e.g., "aa" centered between the two 'a's)

For a string of length n:
- There are **n** odd centers (each character: index 0, 1, ..., n-1)
- There are **n-1** even centers (each gap: between 0-1, 1-2, ..., (n-2)-(n-1))
- Total: **2n-1** centers

**The expand function:**

```
Given center (L, R):
  • Odd  center: L = R = i         (single char, always a palindrome)
  • Even center: L = i, R = i+1    (two adjacent chars, palindrome only if equal)

While L >= 0 and R < n and s[L] == s[R]:
    count += 1          ← this is a valid palindrome
    L -= 1              ← expand outward
    R += 1
```

**Visual trace for "abaaba" at center i=2 (odd, 'a'):**
```
s = a  b  a  a  b  a
    0  1  2  3  4  5

Start: L=2, R=2  → s[2]='a'=='a' → count++ (palindrome "a")
                   L=1, R=3
       L=1, R=3  → s[1]='b'!=s[3]='a' → stop
Total from center 2: 1 palindrome

Center i=2, even (L=2, R=3):
Start: L=2, R=3  → s[2]='a'==s[3]='a' → count++ (palindrome "aa")
                   L=1, R=4
       L=1, R=4  → s[1]='b'==s[4]='b' → count++ (palindrome "baab")
                   L=0, R=5
       L=0, R=5  → s[0]='a'==s[5]='a' → count++ (palindrome "abaaba")
                   L=-1 → stop
Total from even center 2: 3 palindromes
```

**Full center table for "abaaba":**

| Center | Type | Start L,R | Palindromes found |
|---|---|---|---|
| 0 | odd | (0,0) | "a" → 1 |
| 0→1 | even | (0,1) | 'a'≠'b' → 0 |
| 1 | odd | (1,1) | "b", expand: 'a'='a' → "aba" → 2 |
| 1→2 | even | (1,2) | 'b'≠'a' → 0 |
| 2 | odd | (2,2) | "a" → 1 |
| 2→3 | even | (2,3) | "aa", "baab", "abaaba" → 3 |
| 3 | odd | (3,3) | "a" → 1 |
| 3→4 | even | (3,4) | 'a'≠'b' → 0 |
| 4 | odd | (4,4) | "b", expand: 'a'='a' → "aba" → 2 |
| 4→5 | even | (4,5) | 'b'≠'a' → 0 |
| 5 | odd | (5,5) | "a" → 1 |

**Total = 1+0+2+0+1+3+1+0+2+0+1 = 11 ✓**

**Complexity:** Time O(n²) | Space O(1) — no DP table, no extra array.

> [!TIP]
> The O(n) Manacher's algorithm also solves this, but it's a graduate-level technique not expected in standard FAANG interviews. **Expand Around Center is the expected answer.** Mention Manacher's if asked about further optimization.

---

## 8. Complexity Cheat Sheet

| Algorithm | Time | Space | Key technique |
|---|---|---|---|
| Check Palindrome V1 (slice) | O(n) | **O(n)** | Reverse copy |
| Check Palindrome V2 (two-ptr) | O(n) | **O(1)** | Two-pointer ← optimal |
| Valid Palindrome (skip) | O(n) | O(1) | Two-ptr + `.isalnum()` skip |
| Check Anagram V1 (sort) | O(n log n) | O(n) | Sort + compare |
| Check Anagram V2 (hashmap) | O(n) | O(1) | `defaultdict` / `Counter` |
| Check Anagram V3 (freq arr) | O(n) | **O(1)** | `ord(ch)-ord('a')` ← optimal |
| Count Palindromic Substrings | O(n²) | O(1) | Expand Around Center ← optimal |

---

## 9. Interview Decision Guide

> [!TIP]
> | Situation | Pattern |
> |---|---|
> | "Is this string a palindrome?" | Two-pointer O(1) space |
> | "Handle spaces/punctuation in palindrome" | Two-pointer + `.isalnum()` skip |
> | "Are these anagrams?" | 26-element freq array (no dict needed) |
> | "Count palindromic substrings" | Expand around 2n-1 centers |
> | "Build modified string" | Accumulate in list, `"".join()` at end |
> | "Sort a string" | `"".join(sorted(s))` — sorted() returns a list |
