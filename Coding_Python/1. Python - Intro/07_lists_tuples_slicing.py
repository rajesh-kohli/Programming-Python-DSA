###############################################################################
#          Lists, Tuples, Slicing & Comprehensions — Complete Guide           #
###############################################################################

"""
Comprehensive tutorial covering Python's core sequence types: lists and tuples.
Includes indexing, slicing, all list methods with time complexities, tuple
immutability, packing/unpacking, list comprehensions, and practice problems.

Reference: LPLV26MAY/L09 - Intro to Arrays (lectures 001-013)
"""


# =============================================================================
# SECTION 1: Lists — Python's Most Versatile Data Structure
# =============================================================================

# Under the hood, a Python list is a DYNAMIC ARRAY — a contiguous block of
# references (pointers) to objects. When the array fills up, Python allocates
# a larger block (typically ~1.125x the old size) and copies the references.
# This is why append() is O(1) AMORTIZED — most calls are O(1), but
# occasionally a resize triggers an O(n) copy.

# --- Creating lists ---

# Method 1: Square bracket literal (most common)
nums = [10, 20, 30, 40, 50]
print("Literal:", nums)                 # [10, 20, 30, 40, 50]

# Method 2: list() constructor — converts any iterable to a list
from_range = list(range(1, 6))
print("From range:", from_range)        # [1, 2, 3, 4, 5]

from_string = list("hello")
print("From string:", from_string)      # ['h', 'e', 'l', 'l', 'o']

# Method 3: List comprehension (covered in detail in Section 11)
squares = [x**2 for x in range(6)]
print("Comprehension:", squares)        # [0, 1, 4, 9, 16, 25]

# Method 4: Empty list
empty1 = []
empty2 = list()
print("Empty lists:", empty1, empty2)   # [] []
print("Lengths:", len(empty1), len(empty2))  # 0 0

# Heterogeneous types — Python allows mixing types (but usually don't)
mixed = [1, "hello", 3.14, True, None, [1, 2]]
print("Mixed:", mixed)
print("Type:", type(mixed))             # <class 'list'>

# WHY usually don't mix types?
# - Harder to reason about, no consistent operations across elements
# - Type hints become messy: list[int | str | float | ...]
# - In practice, lists hold HOMOGENEOUS data (all ints, all strings, etc.)


# =============================================================================
# SECTION 2: Indexing and Accessing
# =============================================================================

arr = [10, 20, 30, 40, 50]

# Positive indexing (0-based, left to right):
#   Index:    0    1    2    3    4
#   Value:   10   20   30   40   50

# Negative indexing (right to left, starts at -1):
#   Index:   -5   -4   -3   -2   -1
#   Value:   10   20   30   40   50

print("\n--- Indexing ---")
print(f"arr[0]  = {arr[0]}")       # 10  (first element)
print(f"arr[4]  = {arr[4]}")       # 50  (last element)
print(f"arr[-1] = {arr[-1]}")      # 50  (last element — most Pythonic)
print(f"arr[-2] = {arr[-2]}")      # 40  (second to last)
print(f"arr[-5] = {arr[-5]}")      # 10  (first element via negative index)

# Positive and negative index of the same element:
# arr[i] == arr[i - len(arr)]  when i >= 0
# arr[0] == arr[-5]  because 0 - 5 = -5

# Time: O(1) — direct pointer lookup (it's an array, not a linked list)
# Space: O(1)

# IndexError — accessing beyond valid range
# arr[5]   -> IndexError: list index out of range
# arr[-6]  -> IndexError: list index out of range

# len() — get the number of elements — O(1) because Python caches the count
print(f"len(arr) = {len(arr)}")    # 5


# =============================================================================
# SECTION 3: Looping Through Lists (4 Ways)
# =============================================================================

nums = [10, 20, 30, 40, 50]
n = len(nums)

print("\n--- Looping Methods ---")

# ----- Method 1: for-each loop (simplest, when you only need values) -----
print("Method 1 — for item in lst:")
for num in nums:
    print(num, end=" ")
print()
# Use when: You don't need the index, just the values
# Time: O(n), Space: O(1)

# ----- Method 2: index-based with range (when you need the index) -----
print("Method 2 — for i in range(len(lst)):")
for i in range(n):
    print(f"  nums[{i}] = {nums[i]}")
# Use when: You need the index to modify elements in place, or compare
# adjacent elements (nums[i] vs nums[i+1])
# Time: O(n), Space: O(1)

# ----- Method 3: enumerate (PREFERRED — gives both index AND value) -----
print("Method 3 — for i, item in enumerate(lst):")
for i, num in enumerate(nums):
    print(f"  index={i}, value={num}")
# WHY PREFERRED:
#   - Cleaner than range(len(lst)) — no manual indexing with nums[i]
#   - Less error-prone — no off-by-one mistakes
#   - More Pythonic and readable
#   - Optional start parameter: enumerate(lst, start=1)
# Time: O(n), Space: O(1)

# enumerate with custom start
print("  Enumerate with start=1:")
for rank, num in enumerate(nums, start=1):
    print(f"    Rank {rank}: {num}")

# ----- Method 4: while loop with manual index -----
print("Method 4 — while loop:")
i = 0
while i < n:
    print(f"  nums[{i}] = {nums[i]}")
    i += 1
# Use when: You need non-standard iteration (e.g., skip elements, go
# backwards, variable step size, or modify the index mid-loop)
# Time: O(n), Space: O(1)

# SUMMARY: When to use which?
# | Method               | Use Case                                        |
# |----------------------|-------------------------------------------------|
# | for item in lst      | Only need values, no index needed               |
# | for i in range(...)  | Need index to modify in place or compare adj.   |
# | for i, v in enum     | Need BOTH index and value (most common)         |
# | while loop           | Non-standard iteration, early termination logic |


# =============================================================================
# SECTION 4: Searching in Lists
# =============================================================================

nums = [10, 20, 30, 40, 50, 30]
target = 30

print("\n--- Searching ---")

# ----- Method 1: `in` operator — returns True/False -----
# Time: O(n) — linear scan under the hood
print(f"{target} in nums: {target in nums}")      # True
print(f"99 in nums: {99 in nums}")                 # False

# ----- Method 2: list.index(value) — returns first index -----
# Time: O(n) — scans left to right until found
# Raises ValueError if not found!
idx = nums.index(30)
print(f"nums.index(30) = {idx}")                   # 2 (first occurrence)

# Optional: index(value, start, stop) — search within a range
idx2 = nums.index(30, 3)  # search starting from index 3
print(f"nums.index(30, 3) = {idx2}")               # 5 (second occurrence)

# Safe pattern to avoid ValueError:
val = 99
if val in nums:           # O(n)
    print(nums.index(val))  # O(n) again — total O(2n) = O(n)
else:
    print(f"{val} not found")

# ----- Method 3: list.count(value) — count occurrences -----
# Time: O(n) — must scan entire list
print(f"nums.count(30) = {nums.count(30)}")        # 2
print(f"nums.count(99) = {nums.count(99)}")        # 0

# ----- Method 4: Manual search with loop (most flexible) -----
# Useful when you need the index, or want custom logic (e.g., first even)

# Linear search returning index (-1 if not found)
def linear_search(lst, target):
    """O(n) time, O(1) space"""
    for i in range(len(lst)):
        if lst[i] == target:
            return i
    return -1

print(f"linear_search(nums, 40) = {linear_search(nums, 40)}")  # 3
print(f"linear_search(nums, 99) = {linear_search(nums, 99)}")  # -1

# for-else pattern (Pythonic — the else runs if the loop completes without break)
target = 40
for num in nums:
    if num == target:
        print(f"Found {target}!")
        break
else:
    print(f"{target} not found")


# =============================================================================
# SECTION 5: List Slicing (DETAILED)
# =============================================================================

# Syntax: lst[start:stop:step]
#   - start: inclusive (default 0)
#   - stop:  exclusive (default len(lst))
#   - step:  stride (default 1)

# CRITICAL: Slicing ALWAYS returns a NEW list (shallow copy)
# Out-of-range indices in slices do NOT raise errors — they are silently clamped

# MENTAL MODEL — index markers above/below the list, start:stop:step:
#
#           0     1     2     3     4     5     6     7
#         -8    -7    -6    -5    -4    -3    -2    -1
#         +----+----+----+----+----+----+----+----+
#         | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 |
#         +----+----+----+----+----+----+----+----+
#
#   nums[1:4]    -> start=1, stop=4 (exclusive), step=1  -> [20, 30, 40]
#   nums[-3:]    -> start=-3 (=index 5), stop=end          -> [60, 70, 80]
#   nums[::2]    -> every 2nd element from the start       -> [10, 30, 50, 70]
#   nums[::-1]   -> step=-1 walks RIGHT to LEFT, reverses   -> [80,70,60,...,10]
#   nums[5:1:-1] -> start=5, walk backwards, stop BEFORE 1 -> [60, 50, 40, 30]
#
#   Rule of thumb: stop is always EXCLUDED, and the SIGN of step decides
#   which direction you walk (positive = left-to-right, negative = right-to-left).

nums = [10, 20, 30, 40, 50, 60, 70, 80]
#  idx:  0   1   2   3   4   5   6   7
# -idx: -8  -7  -6  -5  -4  -3  -2  -1

print("\n--- Slicing ---")

# Example 1: Basic slice [start:stop] — elements from start up to (not including) stop
sl = nums[1:4]
print(f"nums[1:4] = {sl}")
#   Indices 1, 2, 3 -> [20, 30, 40]
#   BEFORE: [10, 20, 30, 40, 50, 60, 70, 80]
#                 ^^^^^^^^^^^^
#   RESULT: [20, 30, 40]  (new list)

# Example 2: Omit start — defaults to 0
print(f"nums[:4]  = {nums[:4]}")
#   [10, 20, 30, 40]  — first 4 elements

# Example 3: Omit stop — defaults to len(lst)
print(f"nums[5:]  = {nums[5:]}")
#   [60, 70, 80]  — from index 5 to end

# Example 4: Omit both — copy the entire list
copy = nums[:]
print(f"nums[:]   = {copy}")
#   [10, 20, 30, 40, 50, 60, 70, 80]  — full shallow copy

# Example 5: With step
print(f"nums[1:6:2]  = {nums[1:6:2]}")
#   Indices 1, 3, 5 -> [20, 40, 60]
#   BEFORE: [10, 20, 30, 40, 50, 60, 70, 80]
#                 ^       ^       ^
#   RESULT: [20, 40, 60]

# Example 6: Every other element
print(f"nums[::2]    = {nums[::2]}")
#   [10, 30, 50, 70]  — even-indexed elements

print(f"nums[1::2]   = {nums[1::2]}")
#   [20, 40, 60, 80]  — odd-indexed elements

# Example 7: Negative step — REVERSE direction
print(f"nums[::-1]   = {nums[::-1]}")
#   [80, 70, 60, 50, 40, 30, 20, 10]  — full reversal

print(f"nums[5:1:-1] = {nums[5:1:-1]}")
#   Start at 5, go backwards to (not including) 1
#   Indices 5, 4, 3, 2 -> [60, 50, 40, 30]

# Example 8: Negative indices in slices
print(f"nums[-3:]    = {nums[-3:]}")
#   [60, 70, 80]  — last 3 elements

print(f"nums[-5:-2]  = {nums[-5:-2]}")
#   Indices -5, -4, -3 -> [40, 50, 60]

# Example 9: Slice creates a SHALLOW COPY (important for nested lists!)
original = [[1, 2], [3, 4], [5, 6]]
sliced = original[:]
sliced[0][0] = 999           # Modifies the inner list
print(f"original after modifying slice: {original}")
#   [[999, 2], [3, 4], [5, 6]]  — inner list is SHARED!
#   For deep copy, use: import copy; deep = copy.deepcopy(original)

# MENTAL MODEL — shallow copy duplicates the OUTER box, not the INNER boxes:
#
#   original = [[1,2], [3,4], [5,6]]
#
#   original ---> [ ref0, ref1, ref2 ]      sliced ---> [ ref0, ref1, ref2 ]
#                    |     |     |                         |     |     |
#                    v     v     v                         v     v     v
#                  [1,2] [3,4] [5,6]   <-- SAME inner list objects, shared!
#
#   sliced[0][0] = 999  walks through ref0 and mutates the SHARED [1,2] list,
#   so original[0][0] changes too — even though sliced and original are
#   different outer list objects. Only copy.deepcopy() also clones the
#   inner lists, giving fully independent nested data.

# Example 10: Slice ASSIGNMENT — modifying list through slices
# This is a POWERFUL feature — can change size of the list!

colors = ["red", "green", "blue", "white"]
print(f"\nBefore:          {colors}")

# Same-size replacement
colors[1:3] = ["pink", "black"]
print(f"After [1:3]=2:   {colors}")
#   ["red", "pink", "black", "white"]

# Shrink — replace 2 elements with 1
colors[1:3] = ["orange"]
print(f"After [1:3]=1:   {colors}")
#   ["red", "orange", "white"]

# Grow — replace 2 elements with 3
colors[0:2] = ["yellow", "mustard", "neon"]
print(f"After [0:2]=3:   {colors}")
#   ["yellow", "mustard", "neon", "white"]

# Insert without removing (empty slice)
nums2 = [1, 2, 5, 6]
nums2[2:2] = [3, 4]           # Insert [3,4] at position 2
print(f"Insert via slice: {nums2}")
#   [1, 2, 3, 4, 5, 6]

# Delete via slice
nums2[2:4] = []                # Remove elements at indices 2,3
print(f"Delete via slice: {nums2}")
#   [1, 2, 5, 6]

# Slice assignment with step — must match the number of elements!
arr = [10, 20, 30, 40, 50]
arr[0:5:2] = [100, 300, 500]  # Replace indices 0, 2, 4
print(f"Step assignment:  {arr}")
#   [100, 20, 300, 40, 500]
# NOTE: arr[0:5:2] = [100, 300] would raise ValueError — size mismatch

# Time: O(k) where k = size of the slice
# Space: O(k) — creates a new list of that size


# =============================================================================
# SECTION 6: List Methods (with Time Complexity)
# =============================================================================

print("\n--- List Methods ---")

# Setup
nums = [30, 10, 50, 20, 40]
print(f"Start: {nums}")

# ----- append(x): Add to end -----
# Time: O(1) amortized (O(n) when resize triggers)
# Space: O(1)
nums.append(60)
print(f"append(60):       {nums}")
#   BEFORE: [30, 10, 50, 20, 40]
#   AFTER:  [30, 10, 50, 20, 40, 60]

# ----- insert(i, x): Insert x at index i, shift everything right -----
# Time: O(n) — must shift n-i elements
# Space: O(1)
nums.insert(0, 5)
print(f"insert(0, 5):     {nums}")
#   BEFORE: [30, 10, 50, 20, 40, 60]
#   AFTER:  [5, 30, 10, 50, 20, 40, 60]
#            ^  shifted right -------->

nums.insert(3, 35)
print(f"insert(3, 35):    {nums}")
#   BEFORE: [5, 30, 10, 50, 20, 40, 60]
#   AFTER:  [5, 30, 10, 35, 50, 20, 40, 60]

# ----- pop(): Remove and return last element -----
# Time: O(1)
# Space: O(1)
last = nums.pop()
print(f"pop():            {nums}  (removed {last})")
#   BEFORE: [5, 30, 10, 35, 50, 20, 40, 60]
#   AFTER:  [5, 30, 10, 35, 50, 20, 40]     removed 60

# ----- pop(i): Remove and return element at index i -----
# Time: O(n) — must shift elements left to fill the gap
# Space: O(1)
second = nums.pop(1)
print(f"pop(1):           {nums}  (removed {second})")
#   BEFORE: [5, 30, 10, 35, 50, 20, 40]
#   AFTER:  [5, 10, 35, 50, 20, 40]      removed 30

# ----- remove(x): Remove first occurrence of x -----
# Time: O(n) — must search, then shift
# Space: O(1)
# Raises ValueError if x not in list!
nums.remove(35)
print(f"remove(35):       {nums}")
#   BEFORE: [5, 10, 35, 50, 20, 40]
#   AFTER:  [5, 10, 50, 20, 40]

# ----- extend(iterable): Append all items from iterable -----
# Time: O(k) where k = len(iterable)
# Space: O(k) amortized (resize may occur)
nums.extend([60, 70, 80])
print(f"extend([60,70,80]): {nums}")
#   BEFORE: [5, 10, 50, 20, 40]
#   AFTER:  [5, 10, 50, 20, 40, 60, 70, 80]

# extend vs concatenation (+):
#   nums.extend(other)  -> modifies in place, O(k)
#   nums = nums + other -> creates NEW list, O(n+k)
#   nums += other       -> same as extend (modifies in place)

# ----- sort(): Sort in place -----
# Time: O(n log n) — uses Timsort (hybrid merge+insertion sort)
# Space: O(n) — Timsort needs auxiliary space
nums.sort()
print(f"sort():           {nums}")
#   BEFORE: [5, 10, 50, 20, 40, 60, 70, 80]
#   AFTER:  [5, 10, 20, 40, 50, 60, 70, 80]

# Sort descending
nums.sort(reverse=True)
print(f"sort(reverse):    {nums}")
#   [80, 70, 60, 50, 40, 20, 10, 5]

# Sort with key function
words = ["banana", "pie", "apple", "kiwi"]
words.sort(key=len)
print(f"sort(key=len):    {words}")
#   ['pie', 'kiwi', 'apple', 'banana']

# sorted() vs .sort():
#   sorted(lst) -> returns NEW sorted list, original unchanged — O(n log n)
#   lst.sort()  -> sorts in place, returns None — O(n log n)

# ----- reverse(): Reverse in place -----
# Time: O(n)
# Space: O(1)
nums.reverse()
print(f"reverse():        {nums}")
#   BEFORE: [80, 70, 60, 50, 40, 20, 10, 5]
#   AFTER:  [5, 10, 20, 40, 50, 60, 70, 80]

# reversed() vs .reverse():
#   reversed(lst)  -> returns iterator (lazy), original unchanged
#   lst.reverse()  -> reverses in place, returns None

# ----- copy(): Shallow copy -----
# Time: O(n)
# Space: O(n)
backup = nums.copy()
print(f"copy():           {backup}")
# Equivalent: backup = nums[:] or backup = list(nums)

# ----- clear(): Remove all elements -----
# Time: O(n) — decrements reference count for each element
# Space: O(1)
backup.clear()
print(f"clear():          {backup}")
#   []

# ----- index(x, start, stop): Find first index of x -----
# Time: O(n)
nums_idx = [10, 20, 30, 20, 40]
print(f"index(20):        {nums_idx.index(20)}")       # 1
print(f"index(20, 2):     {nums_idx.index(20, 2)}")    # 3  (search from idx 2)

# ----- count(x): Count occurrences -----
# Time: O(n)
print(f"count(20):        {nums_idx.count(20)}")        # 2

# ====================== TIME COMPLEXITY TABLE ======================
#
# | Method           | Time           | Space  | Notes                    |
# |------------------|----------------|--------|--------------------------|
# | lst[i]           | O(1)           | O(1)   | Direct index access      |
# | lst[i] = x       | O(1)           | O(1)   | Direct index assignment  |
# | append(x)        | O(1) amortized | O(1)   | Add to end               |
# | pop()            | O(1)           | O(1)   | Remove from end          |
# | pop(i)           | O(n)           | O(1)   | Shift left after removal |
# | insert(i, x)     | O(n)           | O(1)   | Shift right for insert   |
# | remove(x)        | O(n)           | O(1)   | Search + shift           |
# | extend(iter)     | O(k)           | O(k)   | k = len of iterable      |
# | sort()           | O(n log n)     | O(n)   | Timsort                  |
# | reverse()        | O(n)           | O(1)   | In-place swap            |
# | copy()           | O(n)           | O(n)   | Shallow copy             |
# | clear()          | O(n)           | O(1)   | Decrement all refs       |
# | x in lst         | O(n)           | O(1)   | Linear search            |
# | index(x)         | O(n)           | O(1)   | Linear search            |
# | count(x)         | O(n)           | O(1)   | Full scan                |
# | len(lst)         | O(1)           | O(1)   | Cached value             |
# | lst[a:b]         | O(b-a)         | O(b-a) | Creates new list         |
# | del lst[i]       | O(n)           | O(1)   | Same as pop(i)           |
# | lst1 + lst2      | O(n+m)         | O(n+m) | Creates new list         |
# | lst * k          | O(n*k)         | O(n*k) | Creates new list         |
#
# KEY INTERVIEW INSIGHT:
# - append/pop at end = O(1) -> Use list as a STACK (LIFO)
# - insert/pop at front = O(n) -> For queue (FIFO), use collections.deque
# ===================================================================


# =============================================================================
# SECTION 7: List Initialization Patterns
# =============================================================================

print("\n--- Initialization Patterns ---")

# ----- Pattern 1: Repeat operator [value] * n -----
zeros = [0] * 5
print(f"[0] * 5:          {zeros}")
#   [0, 0, 0, 0, 0]

# ----- Pattern 2: List of lists — THE TRAP -----

# WRONG WAY — all inner lists are the SAME OBJECT (shared reference):
wrong = [[0]] * 3
wrong[0].append(1)
print(f"[[0]] * 3 bug:    {wrong}")
#   [[0, 1], [0, 1], [0, 1]]  -- ALL three changed!
#   Because wrong[0], wrong[1], wrong[2] all point to the same list object

# RIGHT WAY — each inner list is a NEW object:
right = [[0] for _ in range(3)]
right[0].append(1)
print(f"Comprehension:    {right}")
#   [[0, 1], [0], [0]]  -- only the first changed

# Verify with id():
wrong2 = [[]] * 3
print(f"Shared reference: id(wrong2[0]) == id(wrong2[1]) -> {id(wrong2[0]) == id(wrong2[1])}")
right2 = [[] for _ in range(3)]
print(f"Separate objects: id(right2[0]) == id(right2[1]) -> {id(right2[0]) == id(right2[1])}")

# WHY [value] * n is SAFE for immutable types:
# Integers, strings, tuples are immutable. Even though all slots reference
# the same object, you can't mutate it — reassignment creates a new object.
safe = [0] * 5
safe[0] = 99
print(f"[0]*5, safe[0]=99: {safe}")  # [99, 0, 0, 0, 0] — only first changed

# ----- Pattern 3: List comprehension -----
squares = [x**2 for x in range(1, 6)]
print(f"Squares:          {squares}")
#   [1, 4, 9, 16, 25]

# ----- Pattern 4: Comprehension with condition -----
evens = [x for x in range(10) if x % 2 == 0]
print(f"Evens:            {evens}")
#   [0, 2, 4, 6, 8]

# ----- Pattern 5: From user input -----
# n = int(input("Enter size: "))
# nums = []
# for _ in range(n):
#     nums.append(int(input()))

# One-liner version:
# nums = [int(input()) for _ in range(n)]

# Space-separated input:
# nums = list(map(int, input().split()))

# ----- Pattern 6: 2D list (matrix) -----
rows, cols = 3, 4
matrix = [[0] * cols for _ in range(rows)]
print(f"3x4 matrix:       {matrix}")
#   [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]


# =============================================================================
# SECTION 8: Lists as Function Arguments
# =============================================================================

print("\n--- Lists as Function Arguments ---")

# CRITICAL CONCEPT: Lists are MUTABLE. When you pass a list to a function,
# you pass a REFERENCE (pointer) to the same object. Changes inside the
# function affect the ORIGINAL list.

# Example 1: Function that reads but doesn't modify (safe)
def compute_sum(nums: list[int]) -> int:
    """Returns the sum. Does not modify the input list.
    Time: O(n), Space: O(1)"""
    s = 0
    for num in nums:
        s += num
    return s

original = [10, 20, 30, 40, 50]
result = compute_sum(original)
print(f"Sum: {result}")                # 150
print(f"Original unchanged: {original}")  # [10, 20, 30, 40, 50]

# Example 2: Function that MODIFIES the list (side effect!)
def increment_all(nums: list[int]) -> None:
    """Adds 1 to every element IN PLACE. Modifies the original!
    Time: O(n), Space: O(1)"""
    for i in range(len(nums)):
        nums[i] += 1

data = [10, 20, 30, 40, 50]
print(f"Before increment: {data}")
increment_all(data)
print(f"After increment:  {data}")     # [11, 21, 31, 41, 51] — ORIGINAL changed!

# HOW TO AVOID unintended modification:
# Option 1: Pass a copy
data2 = [10, 20, 30]
increment_all(data2.copy())       # Pass a copy
print(f"data2 unchanged:  {data2}")    # [10, 20, 30]

# Option 2: Pass a slice copy
increment_all(data2[:])           # Slice copy
print(f"data2 unchanged:  {data2}")    # [10, 20, 30]

# Option 3: Create copy inside the function
def safe_increment(nums: list[int]) -> list[int]:
    """Returns a new incremented list. Original is NOT modified.
    Time: O(n), Space: O(n)"""
    return [x + 1 for x in nums]

data3 = [10, 20, 30]
result = safe_increment(data3)
print(f"Original:         {data3}")    # [10, 20, 30]
print(f"New list:         {result}")   # [11, 21, 31]

# WHY does this happen?
# Python variables are references (like pointers). Assignment (=) copies the
# reference, not the object. So `def f(lst)` receives a copy of the pointer,
# but both pointers reference the same list object in memory.

# Visual:
#   data = [10, 20, 30]       data -----> [10, 20, 30] <----- nums (parameter)
#   increment_all(data)        Both point to the SAME object!

# Finding max and min — common utility functions
def find_max(nums: list[int]) -> int:
    """Time: O(n), Space: O(1)"""
    max_so_far = float("-inf")  # Negative infinity — guaranteed to be smaller
    for num in nums:
        if num > max_so_far:
            max_so_far = num
    return max_so_far

def find_min(nums: list[int]) -> int:
    """Time: O(n), Space: O(1)"""
    min_so_far = float("inf")   # Positive infinity — guaranteed to be larger
    for num in nums:
        if num < min_so_far:
            min_so_far = num
    return min_so_far

sample = [30, 10, 50, 20, 40]
print(f"Max: {find_max(sample)}, Min: {find_min(sample)}")  # 50, 10
print(f"Built-in: max={max(sample)}, min={min(sample)}")    # Same result


# =============================================================================
# SECTION 9: Tuples — Immutable Sequences
# =============================================================================

print("\n--- Tuples ---")

# A tuple is like a list but IMMUTABLE — once created, cannot be changed.
# Under the hood: fixed-size array of references (no resize mechanism).
#
# MENTAL MODEL — mutable (list) vs immutable (tuple) under mutation attempts:
#
#   LIST (mutable)                      TUPLE (immutable)
#   lst = [1, 2, 3]                     tup = (1, 2, 3)
#   lst[0] = 99    -> OK, in-place      tup[0] = 99   -> TypeError!
#   lst.append(4)  -> OK, in-place      tup has no .append at all
#   id(lst) SAME before/after mutation  tup can never change; "changing" it
#                                       means building a brand NEW tuple
#                                       (e.g. tup = tup + (4,) -> new object)
#
#   Because tuples never change, they're hashable (usable as dict keys /
#   set members) and Python can treat them as safe, fixed "records".

# ----- Creating Tuples -----

# Parentheses (most common)
t1 = (10, 20, 30)
print(f"Tuple: {t1}, type: {type(t1)}")

# Without parentheses (tuple packing — the COMMA makes it a tuple, not parens)
t2 = 10, 20, 30
print(f"Packed: {t2}, type: {type(t2)}")

# From a list
t3 = tuple([1, 2, 3])
print(f"From list: {t3}")

# From a string
t4 = tuple("hello")
print(f"From string: {t4}")  # ('h', 'e', 'l', 'l', 'o')

# GOTCHA: Single-element tuple — the COMMA is mandatory!
single_tuple = (42,)           # This IS a tuple
not_a_tuple = (42)             # This is just the integer 42
print(f"(42,) -> type: {type(single_tuple)}")   # <class 'tuple'>
print(f"(42)  -> type: {type(not_a_tuple)}")     # <class 'int'>

# Empty tuple
empty_t = ()
empty_t2 = tuple()
print(f"Empty: {empty_t}, {empty_t2}")

# ----- Tuple Operations -----

t = (10, 20, 30, 40, 50)

# Indexing — same as lists: O(1)
print(f"t[0] = {t[0]}, t[-1] = {t[-1]}")

# Slicing — returns a new TUPLE: O(k)
print(f"t[1:4] = {t[1:4]}")     # (20, 30, 40)
print(f"t[::-1] = {t[::-1]}")   # (50, 40, 30, 20, 10)

# Length: O(1)
print(f"len(t) = {len(t)}")

# Count and index: O(n)
t_dup = (10, 20, 30, 20, 40, 20)
print(f"count(20) = {t_dup.count(20)}")  # 3
print(f"index(30) = {t_dup.index(30)}")  # 2

# Membership test: O(n)
print(f"30 in t = {30 in t}")

# Concatenation and repetition (creates NEW tuples)
print(f"(1,2) + (3,4) = {(1,2) + (3,4)}")  # (1, 2, 3, 4)
print(f"(0,) * 3 = {(0,) * 3}")             # (0, 0, 0)

# IMMUTABILITY — cannot modify elements
# t[0] = 99  -> TypeError: 'tuple' object does not support item assignment
# t.append(60)  -> AttributeError: 'tuple' object has no attribute 'append'

# BUT: if tuple contains mutable objects, THOSE objects can change
mutable_inside = ([1, 2], [3, 4])
mutable_inside[0].append(99)
print(f"Mutable inside tuple: {mutable_inside}")  # ([1, 2, 99], [3, 4])
# The tuple still references the same list objects — you changed the list, not the tuple

# ----- When to Use Tuples vs Lists -----
#
# | Feature          | List            | Tuple              |
# |------------------|-----------------|--------------------|
# | Mutable?         | Yes             | No                 |
# | Syntax           | [1, 2, 3]       | (1, 2, 3)          |
# | Use case         | Collection that | Fixed data, dict   |
# |                  | may change      | keys, func returns |
# | Hashable?        | No              | Yes (if contents   |
# |                  |                 | are also hashable) |
# | Memory           | More (resize    | Less (fixed size)  |
# |                  | buffer)         |                    |
# | Speed            | Slightly slower | Slightly faster    |
#
# RULE OF THUMB:
# - Use LIST when data will change (add/remove/modify)
# - Use TUPLE when data should NOT change (coordinates, RGB, DB records)
# - TUPLES can be dictionary keys, LISTS cannot (because lists aren't hashable)

# Dictionary keys example:
location = {(28.6, 77.2): "Delhi", (19.0, 72.8): "Mumbai"}
print(f"location[(28.6, 77.2)] = {location[(28.6, 77.2)]}")

# ----- Tuple Unpacking -----
point = (3, 7)
x, y = point
print(f"Unpacked: x={x}, y={y}")

# Function returning multiple values (returns a tuple implicitly)
def min_max(lst):
    return min(lst), max(lst)    # Returns a tuple

lo, hi = min_max([5, 2, 8, 1, 9])
print(f"min={lo}, max={hi}")

# ----- Named Tuples (brief mention) -----
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 7)
print(f"Named tuple: {p}, x={p.x}, y={p.y}")
# Benefits: Readable field access by name, still immutable, still a tuple


# =============================================================================
# SECTION 10: Packing and Unpacking
# =============================================================================

print("\n--- Packing and Unpacking ---")

# ----- Tuple Packing -----
# Assigning multiple values creates a tuple (the comma is what makes it a tuple)
packed = 1, 2, 3
print(f"Packed: {packed}, type: {type(packed)}")  # (1, 2, 3) <class 'tuple'>

# ----- Tuple Unpacking -----
# Assign tuple elements to individual variables
a, b, c = (10, 20, 30)
print(f"Unpacked: a={a}, b={b}, c={c}")

# Works with lists too
x, y, z = [100, 200, 300]
print(f"From list: x={x}, y={y}, z={z}")

# Number of variables MUST match number of elements
# a, b = (1, 2, 3)  -> ValueError: too many values to unpack
# a, b, c = (1, 2)  -> ValueError: not enough values to unpack

# ----- Extended Unpacking with * (star/splat operator) -----
# Captures "the rest" into a list

# *rest at the end
first, *rest = [1, 2, 3, 4, 5]
print(f"first={first}, rest={rest}")
#   first=1, rest=[2, 3, 4, 5]

# *rest at the beginning
*rest, last = [1, 2, 3, 4, 5]
print(f"rest={rest}, last={last}")
#   rest=[1, 2, 3, 4], last=5

# *rest in the middle
first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")
#   first=1, middle=[2, 3, 4], last=5

# Edge case: *rest can be empty
a, *rest = [1]
print(f"a={a}, rest={rest}")          # a=1, rest=[]

# ----- Swap Without Temporary Variable -----
a, b = 10, 20
print(f"Before swap: a={a}, b={b}")

a, b = b, a
print(f"After swap:  a={a}, b={b}")

# HOW PYTHON DOES THIS INTERNALLY:
# 1. Right side (b, a) is evaluated first -> creates tuple (20, 10)
# 2. Left side (a, b) unpacks the tuple -> a=20, b=10
# This is why it works — the old values are "saved" in the temporary tuple

# Three-way swap
x, y, z = 1, 2, 3
x, y, z = z, x, y    # Rotate: z->x, x->y, y->z
print(f"Rotated: x={x}, y={y}, z={z}")  # x=3, y=1, z=2

# ----- *args in Function Definitions (Packing) -----
def add(*args, b, c):
    """*args packs positional arguments into a tuple."""
    print(f"  args={args}, type={type(args)}, b={b}, c={c}")
    return sum(args) + b + c

print(f"add(2, b=3, c=5) = {add(2, b=3, c=5)}")
#   args=(2,), b=3, c=5 -> 2+3+5 = 10

print(f"add(2, 3, b=5, c=6) = {add(2, 3, b=5, c=6)}")
#   args=(2, 3), b=5, c=6 -> 2+3+5+6 = 16

# More typical *args usage (no keyword-only params after it)
def flexible_sum(*numbers):
    """Accepts any number of positional arguments."""
    return sum(numbers)

print(f"flexible_sum(1,2,3,4,5) = {flexible_sum(1, 2, 3, 4, 5)}")

# **kwargs — packs keyword arguments into a dictionary
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key} = {value}")

print("show_info:")
show_info(name="Rajesh", age=25, city="Delhi")

# Unpacking into function calls with * and **
def greet(first, last, greeting="Hello"):
    print(f"  {greeting}, {first} {last}!")

args_list = ["John", "Doe"]
kwargs_dict = {"greeting": "Hey"}
greet(*args_list, **kwargs_dict)  # Unpacks list and dict into arguments


# =============================================================================
# SECTION 11: List Comprehensions (Detailed)
# =============================================================================

print("\n--- List Comprehensions ---")

# List comprehensions are a concise way to create lists.
# Syntax: [expression for item in iterable]
# Equivalent to:
#   result = []
#   for item in iterable:
#       result.append(expression)

# ----- Basic Comprehension -----
squares = [x**2 for x in range(1, 8)]
print(f"Squares: {squares}")
#   [1, 4, 9, 16, 25, 36, 49]

# ----- With Filter (if condition) -----
# Only include elements that satisfy the condition
evens = [x for x in range(20) if x % 2 == 0]
print(f"Evens: {evens}")
#   [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Positive numbers from a mixed list
mixed = [-3, 5, -1, 8, 0, -7, 2]
positives = [x for x in mixed if x > 0]
print(f"Positives: {positives}")
#   [5, 8, 2]

# ----- With if-else (conditional expression — goes BEFORE for) -----
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
print(f"Labels: {labels}")
#   ['even', 'odd', 'even', 'odd', 'even']
# NOTE: if-else as expression goes BEFORE for
#        if as filter goes AFTER for

# ----- Nested Comprehension -----
# Flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [val for row in matrix for val in row]
print(f"Flattened: {flat}")
#   [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Equivalent to:
#   flat = []
#   for row in matrix:       <-- outer loop first
#       for val in row:      <-- inner loop second
#           flat.append(val)

# Generate coordinate pairs
pairs = [(i, j) for i in range(3) for j in range(3)]
print(f"Pairs: {pairs}")
#   [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

# Create a 2D matrix using nested comprehension
rows, cols = 3, 4
grid = [[0] * cols for _ in range(rows)]
print(f"3x4 grid: {grid}")

# Multiplication table
mult_table = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(f"Mult table: {mult_table}")
#   [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# ----- String processing with comprehensions -----
sentence = "Hello World Python"
lengths = [len(word) for word in sentence.split()]
print(f"Word lengths: {lengths}")
#   [5, 5, 6]

upper_words = [w.upper() for w in sentence.split()]
print(f"Upper: {upper_words}")
#   ['HELLO', 'WORLD', 'PYTHON']

# ----- Dict Comprehension -----
# Syntax: {key_expr: value_expr for item in iterable}
names = ["alice", "bob", "charlie"]
name_lengths = {name: len(name) for name in names}
print(f"Dict comp: {name_lengths}")
#   {'alice': 5, 'bob': 3, 'charlie': 7}

# Invert a dictionary
original_dict = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original_dict.items()}
print(f"Inverted: {inverted}")
#   {1: 'a', 2: 'b', 3: 'c'}

# ----- Set Comprehension -----
# Syntax: {expr for item in iterable}  — like dict comp but without key:value
nums_with_dups = [1, 2, 2, 3, 3, 3, 4, 4, 5]
unique_squares = {x**2 for x in nums_with_dups}
print(f"Set comp: {unique_squares}")
#   {1, 4, 9, 16, 25}

# ----- Generator Expression (bonus) -----
# Like list comprehension but with () instead of []
# LAZY — doesn't create the whole list in memory
gen = (x**2 for x in range(1000000))
print(f"Generator: {gen}")      # <generator object ...>
print(f"First 5: {[next(gen) for _ in range(5)]}")  # [0, 1, 4, 9, 16]
# Use when: you only need to iterate once, and the data is too large for a list

# Performance: comprehensions are ~30% faster than equivalent for-loops
# because the append call is optimized at the C level in CPython


# =============================================================================
# SECTION 11.5: Frequency Counting — set(), dict, and collections.Counter
# =============================================================================

# A VERY common interview/real-world task: given a list, count how many
# times each item appears, or find the unique items, or find the most
# common one. Python gives you several tools of increasing power.

print("\n--- Frequency Counting ---")

categories = ['shoes', 'shirts', 'shoes', 'jackets', 'shirts', 'shoes']

# ----- Tool 1: set() — just the UNIQUE values, no counts -----
# Use when you only care about "what distinct items exist", not how many times.
unique_categories = set(categories)
print(f"Unique categories: {unique_categories}")   # {'shoes', 'shirts', 'jackets'}
# Time: O(n) to build, Space: O(k) where k = number of unique items

# ----- Tool 2: Manual dict — build the frequency map yourself -----
# This is what's actually happening "under the hood" — good to know for interviews
# even though you'd rarely write this by hand in production code.
counts = {}
for item in categories:
    if item in counts:
        counts[item] += 1
    else:
        counts[item] = 1
print(f"Manual counts: {counts}")          # {'shoes': 3, 'shirts': 2, 'jackets': 1}

top_category_manual = max(counts, key=counts.get)
print(f"Most common (manual): {top_category_manual}")   # shoes
# max(dict, key=dict.get) → finds the KEY whose VALUE is largest.
# Time: O(n) to build counts, O(k) to find the max → overall O(n)

# ----- Tool 3: dict comprehension + .count() — concise but SLOWER -----
# .count() re-scans the whole list for EVERY unique item — O(n*k), not O(n)!
# Fine for small lists, but avoid for large data (use Counter instead).
unique_set = set(categories)
click_counts_comp = {item: categories.count(item) for item in unique_set}
print(f"Dict comprehension counts: {click_counts_comp}")

# ----- Tool 4: collections.Counter — THE RIGHT TOOL for frequency counting -----
# Counter is a specialized dict subclass built exactly for this purpose.
from collections import Counter

click_counts = Counter(categories)
print(f"Counter object: {click_counts}")
# Counter({'shoes': 3, 'shirts': 2, 'jackets': 1})
print(f"Type: {type(click_counts)}")   # <class 'collections.Counter'>

# Counter behaves like a dict — you can index into it:
print(f"Count of 'shoes': {click_counts['shoes']}")     # 3
print(f"Count of 'pants' (missing): {click_counts['pants']}")  # 0 — no KeyError!
#   ^ This is a key advantage over a regular dict: missing keys return 0
#     instead of raising KeyError. Regular dict would need .get(key, 0).

# .most_common(n) — the most useful Counter method.
# Returns a list of (item, count) tuples, sorted by count descending.
print(f"Most common overall: {click_counts.most_common()}")
#   [('shoes', 3), ('shirts', 2), ('jackets', 1)]

top_category = click_counts.most_common(1)[0][0]   # top item's NAME
print(f"Top category: {top_category}")              # shoes
#   most_common(1)  → [('shoes', 3)]   (list with one tuple)
#   most_common(1)[0] → ('shoes', 3)    (the tuple)
#   most_common(1)[0][0] → 'shoes'      (just the name)

# Counter also supports arithmetic — adding/subtracting frequency maps:
more_categories = Counter(['shoes', 'hats', 'hats'])
combined = click_counts + more_categories
print(f"Combined counts: {combined}")
# Counter({'shoes': 4, 'shirts': 2, 'hats': 2, 'jackets': 1})

# ----- Time Complexity Comparison -----
# | Approach              | Time      | When to use                          |
# |------------------------|-----------|---------------------------------------|
# | set()                  | O(n)      | Only need unique values, not counts   |
# | Manual dict loop        | O(n)      | Educational / when Counter isn't available |
# | dict comp + .count()    | O(n*k)    | AVOID for large lists — slow!         |
# | collections.Counter     | O(n)      | ALWAYS prefer this for frequency work |
print()


# =============================================================================
# SECTION 12: Common Operations Reference Table + Practice Exercises
# =============================================================================

print("\n--- Quick Reference ---")

# =================== COMMON OPERATIONS REFERENCE TABLE ===================
#
# | Operation                | Syntax                  | Time     | Returns       |
# |--------------------------|-------------------------|----------|---------------|
# | Create empty             | [] or list()            | O(1)     | list          |
# | Create from range        | list(range(n))          | O(n)     | list          |
# | Access element           | lst[i]                  | O(1)     | element       |
# | Assign element           | lst[i] = x              | O(1)     | None          |
# | Append to end            | lst.append(x)           | O(1)*    | None          |
# | Insert at position       | lst.insert(i, x)        | O(n)     | None          |
# | Remove from end          | lst.pop()               | O(1)     | element       |
# | Remove from position     | lst.pop(i)              | O(n)     | element       |
# | Remove by value          | lst.remove(x)           | O(n)     | None          |
# | Delete by index          | del lst[i]              | O(n)     | N/A           |
# | Check membership         | x in lst                | O(n)     | bool          |
# | Find index               | lst.index(x)            | O(n)     | int           |
# | Count occurrences        | lst.count(x)            | O(n)     | int           |
# | Length                    | len(lst)                | O(1)     | int           |
# | Sort in place            | lst.sort()              | O(nlogn) | None          |
# | Sorted copy              | sorted(lst)             | O(nlogn) | new list      |
# | Reverse in place         | lst.reverse()           | O(n)     | None          |
# | Reversed iterator        | reversed(lst)           | O(1)     | iterator      |
# | Shallow copy             | lst.copy() / lst[:]     | O(n)     | new list      |
# | Deep copy                | copy.deepcopy(lst)      | O(n*k)   | new list      |
# | Concatenate              | lst1 + lst2             | O(n+m)   | new list      |
# | Extend in place          | lst1.extend(lst2)       | O(m)     | None          |
# | Slice                    | lst[a:b:c]              | O(k)     | new list      |
# | Min / Max                | min(lst) / max(lst)     | O(n)     | element       |
# | Sum                      | sum(lst)                | O(n)     | number        |
# | All / Any                | all(lst) / any(lst)     | O(n)     | bool          |
# | Zip                      | zip(lst1, lst2)         | O(1)     | iterator      |
# | Enumerate                | enumerate(lst)          | O(1)     | iterator      |
# | Map                      | map(func, lst)          | O(1)     | iterator      |
# | Filter                   | filter(func, lst)       | O(1)     | iterator      |
#
# * = amortized (occasional O(n) resize)
# =========================================================================

# =================== PRACTICE EXERCISES ===================

print("\n" + "=" * 60)
print("PRACTICE EXERCISES")
print("=" * 60)


# ----- Exercise 1: Rotate a list k positions to the right -----
# Input: [1, 2, 3, 4, 5], k=2
# Output: [4, 5, 1, 2, 3]
# Hint: Use slicing

def rotate_right(lst, k):
    """Rotate list k positions to the right using slicing.
    Time: O(n), Space: O(n)"""
    n = len(lst)
    k = k % n                    # Handle k > n
    return lst[-k:] + lst[:-k]

print("\nExercise 1: Rotate Right")
print(f"  rotate_right([1,2,3,4,5], 2) = {rotate_right([1, 2, 3, 4, 5], 2)}")
#   [4, 5, 1, 2, 3]


# ----- Exercise 2: Remove duplicates while preserving order -----
# Input: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
# Output: [3, 1, 4, 5, 9, 2, 6]

def remove_duplicates(lst):
    """Remove duplicates preserving first occurrence order.
    Time: O(n), Space: O(n)"""
    seen = set()
    result = []
    for x in lst:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result

print("\nExercise 2: Remove Duplicates")
print(f"  {remove_duplicates([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])}")
#   [3, 1, 4, 5, 9, 2, 6]


# ----- Exercise 3: Flatten a nested list (one level deep) -----
# Input: [[1, 2], [3, 4], [5]]
# Output: [1, 2, 3, 4, 5]

def flatten(nested):
    """Flatten one level of nesting using list comprehension.
    Time: O(n) where n = total elements, Space: O(n)"""
    return [item for sublist in nested for item in sublist]

print("\nExercise 3: Flatten")
print(f"  {flatten([[1, 2], [3, 4], [5]])}")
#   [1, 2, 3, 4, 5]


# ----- Exercise 4: Two Sum — find indices of two numbers that add to target -----
# Input: nums=[2, 7, 11, 15], target=9
# Output: (0, 1) because nums[0] + nums[1] = 2 + 7 = 9

def two_sum(nums, target):
    """Find two indices whose values sum to target.
    Time: O(n), Space: O(n) — using a hash map"""
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None

print("\nExercise 4: Two Sum")
print(f"  two_sum([2, 7, 11, 15], 9) = {two_sum([2, 7, 11, 15], 9)}")
#   (0, 1)


# ----- Exercise 5: Group elements by even/odd using comprehensions -----
# Input: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Output: {"even": [2, 4, 6, 8, 10], "odd": [1, 3, 5, 7, 9]}

def group_even_odd(lst):
    """Group numbers into even and odd using comprehensions.
    Time: O(n), Space: O(n)"""
    return {
        "even": [x for x in lst if x % 2 == 0],
        "odd":  [x for x in lst if x % 2 != 0]
    }

print("\nExercise 5: Group Even/Odd")
result = group_even_odd([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"  {result}")
#   {'even': [2, 4, 6, 8, 10], 'odd': [1, 3, 5, 7, 9]}


# =================== KEY TAKEAWAYS ===================
#
# 1. Lists = mutable, dynamic arrays. Tuples = immutable, fixed arrays.
# 2. append/pop at end = O(1). insert/pop at index = O(n). Know this for interviews.
# 3. Slicing creates a NEW list (shallow copy). Slice assignment can resize.
# 4. Passing a list to a function passes a REFERENCE — modifications affect original.
# 5. List comprehensions are faster and more Pythonic than manual for+append loops.
# 6. Use tuples for fixed data, dict keys, and function returns.
# 7. [[]] * n creates SHARED references. Use [[] for _ in range(n)] instead.
# 8. enumerate() is preferred over range(len()) when you need both index and value.
# =====================================================
