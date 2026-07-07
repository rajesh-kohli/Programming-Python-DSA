# =============================================================================
# MODULE 07: DATA STRUCTURES — ARRAYS & STACKS
# =============================================================================
# A comprehensive guide to arrays (Python lists), the stack data structure,
# and real-world applications. Every section is fully executable.
#
# SOURCE NOTEBOOKS:
#   16. Arrays_1.ipynb through 16. Arrays_8_Max 3.ipynb
#   2. Largest of n numbers.ipynb
#   Usecase_1.ipynb  Usecase_2_FB_friend_recommedation_graph.ipynb
#   Usecase_3_Browser_stack.ipynb  Usecase_4_Parenthesis_matching.ipynb
#   Usecase_4_polish_notation.ipynb
#
# TEST VALUES USED THROUGHOUT:
#   arr    = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
#   target = 5
#   k      = 3
#   a, b, c (Max-3) = 7, 2, 9
# =============================================================================

print("=" * 78)
print("  MODULE 07 — DATA STRUCTURES: ARRAYS & STACKS")
print("=" * 78)


# =============================================================================
# SECTION 1: What Is an Array?
# =============================================================================
# An ARRAY is a linear data structure that stores a sequence of values in
# contiguous memory, all referenced by a single name.
#
# In Python the two built-in array-like types are:
#   • list  — mutable (can change after creation)
#   • tuple — immutable (cannot change after creation)
#
# Python lists behave as dynamic arrays; they resize automatically.
#
# INDEXING RULES:
#   Positive index:  arr[0]  is the first element (front)
#   Negative index:  arr[-1] is the last element  (back)
#
#   arr  = [ 3,  1,  4,  1,  5,  9,  2,  6,  5,  3,  5 ]
#   pos  =   0   1   2   3   4   5   6   7   8   9  10
#   neg  = -11 -10  -9  -8  -7  -6  -5  -4  -3  -2  -1
# =============================================================================

print("\n" + "=" * 78)
print("  SECTION 1: Array Basics — Declaration, Indexing, Traversal")
print("=" * 78)

# --- Declaration ---
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]   # our main test array
empty_list  = []                             # empty via literal
empty_list2 = list()                         # empty via constructor
chars       = list("coding")                 # string → list of characters

print(f"\nMain array      : {arr}")           # Output: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(f"Length          : {len(arr)}")        # Output: 11
print(f"First element   : {arr[0]}")          # Output: 3
print(f"Last element    : {arr[-1]}")         # Output: 5
print(f"Same last (pos) : {arr[len(arr)-1]}") # Output: 5
print(f"String to list  : {chars}")           # Output: ['c', 'o', 'd', 'i', 'n', 'g']

# --- Traversal: while loop ---
print("\n[Traversal via while loop]")
nums = [10, 20, 30, 40, 50]
i, n = 0, len(nums)
while i < n:
    print(f"  index {i}: {nums[i]}")          # Output: index 0: 10 … index 4: 50
    i += 1

# --- Traversal: for-in loop (Pythonic, no index needed) ---
print("\n[Traversal via for-in]")
for num in nums:
    print(f"  {num}", end=" ")                # Output: 10 20 30 40 50
print()

# --- Traversal: for with range (when index is needed) ---
print("\n[Traversal via range(len())]")
for i in range(len(nums)):
    print(f"  nums[{i}] = {nums[i]}")         # Output: nums[0]=10 … nums[4]=50

# --- Traversal: enumerate (index + value together) ---
print("\n[Traversal via enumerate]")
for i, num in enumerate(nums):
    print(f"  ({i}, {num})")                  # Output: (0,10) (1,20) … (4,50)

# --- Slicing ---
sub = arr[2:6]                                 # extract sub-array
print(f"\nSlice arr[2:6]  : {sub}")            # Output: [4, 1, 5, 9]


# =============================================================================
# SECTION 2: Sum, Max, Min — Traversal Problems
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 2: Sum, Max, Min of an Array")
print("=" * 78)

# TIME COMPLEXITY: O(n)  — single pass through every element
# SPACE COMPLEXITY: O(1) — only a few scalar variables

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# ----- APPROACH 1 (Brute Force): Manual loops -----
print("\n[APPROACH 1 — Manual Loops]")

# Sum
total = 0
for num in arr:
    total += num                               # accumulate each element
print(f"  Sum (manual)   : {total}")           # Output: 44

# Max
max_so_far = float('-inf')                     # start at −∞ so any value beats it
for num in arr:
    if num > max_so_far:
        max_so_far = num
print(f"  Max (manual)   : {max_so_far}")      # Output: 9

# Min
min_so_far = float('inf')                      # start at +∞ so any value beats it
for num in arr:
    if num < min_so_far:
        min_so_far = num
print(f"  Min (manual)   : {min_so_far}")      # Output: 1

# ----- APPROACH 2 (Optimal): Python built-ins — same O(n) but cleaner -----
print("\n[APPROACH 2 — Python Built-ins]")
print(f"  sum(arr)  = {sum(arr)}")             # Output: 44
print(f"  max(arr)  = {max(arr)}")             # Output: 9
print(f"  min(arr)  = {min(arr)}")             # Output: 1

# Membership test (is target in array?)
target = 5
print(f"\n  Is {target} in arr? {target in arr}")  # Output: True
print(f"  Is 99 in arr? {99 in arr}")              # Output: False


# =============================================================================
# SECTION 3: First Occurrence of an Element
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 3: First Occurrence of Element")
print("=" * 78)

# Problem: Given array and target T, return INDEX of first occurrence.
#          Return -1 if T is not present.
#
# Example: arr=[3,1,4,1,5,9,2,6,5,3,5], T=5  → index 4

arr    = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
target = 5

# ----- APPROACH 1 (Brute Force): Linear scan from the left -----
# Walk every element left → right, stop at first match.
# TIME COMPLEXITY: O(n)  — worst case, target is last or absent
# SPACE COMPLEXITY: O(1)

def first_occurrence_linear(arr: list, target: int) -> int:
    """Linear scan — return index of first occurrence, or -1."""
    for i, num in enumerate(arr):
        # Step-by-step trace for arr=[3,1,4,1,5,...], target=5:
        #   i=0: 3 ≠ 5 → skip
        #   i=1: 1 ≠ 5 → skip
        #   i=2: 4 ≠ 5 → skip
        #   i=3: 1 ≠ 5 → skip
        #   i=4: 5 == 5 → RETURN 4 ✓
        if num == target:
            return i
    return -1

# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

result_linear = first_occurrence_linear(arr, target)
print(f"\n[APPROACH 1 — Linear Scan] O(n)")
print(f"  arr    : {arr}")
print(f"  target : {target}")
print(f"  First occurrence index : {result_linear}")             # Output: 4
print(f"  Target 99 (not found)  : {first_occurrence_linear(arr, 99)}")  # Output: -1

# ----- APPROACH 2 (Optimal for sorted arrays): Binary Search -----
# If the array is SORTED, binary search finds the first occurrence in O(log n).
# General array → linear scan is already the best we can do at O(n).
#
# TIME COMPLEXITY: O(log n)  — halve search space each step
# SPACE COMPLEXITY: O(1)

def first_occurrence_binary(sorted_arr: list, target: int) -> int:
    """Binary search on a SORTED array — finds leftmost occurrence."""
    left, right = 0, len(sorted_arr) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if sorted_arr[mid] == target:
            result = mid           # record match, but keep searching LEFT
            right = mid - 1        # ← move left to find earlier occurrence
        elif sorted_arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

sorted_arr = sorted(arr)           # [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
print(f"\n[APPROACH 2 — Binary Search on Sorted Array] O(log n)")
print(f"  sorted_arr : {sorted_arr}")
print(f"  First occurrence of {target} : {first_occurrence_binary(sorted_arr, target)}")  # Output: 6

# ----- Built-in shortcut -----
try:
    built_in_idx = arr.index(target)
except ValueError:
    built_in_idx = -1
print(f"\n[Built-in .index()] : {built_in_idx}")                # Output: 4


# =============================================================================
# SECTION 4: Last Occurrence of an Element
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 4: Last Occurrence of Element")
print("=" * 78)

# Problem: Return the INDEX of the LAST occurrence of target.
#
# Key idea: iterate BACKWARDS with range(n-1, -1, -1).
#           The first match going right-to-left IS the last occurrence.
#
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

arr    = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
target = 5
n      = len(arr)

def last_occurrence(arr: list, n: int, target: int) -> int:
    """Scan from the back — return index of last occurrence, or -1."""
    for i in range(n - 1, -1, -1):
        # Trace for arr=[3,1,4,1,5,9,2,6,5,3,5], target=5:
        #   i=10: arr[10]=5 == 5 → RETURN 10 ✓
        if arr[i] == target:
            return i
    return -1

# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

result = last_occurrence(arr, n, target)
print(f"\n  arr    : {arr}")
print(f"  target : {target}")
print(f"  Last occurrence index  : {result}")                    # Output: 10
print(f"  Target 99 (not found)  : {last_occurrence(arr, n, 99)}")  # Output: -1


# =============================================================================
# SECTION 5: All Occurrences of an Element
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 5: All Occurrences of Element")
print("=" * 78)

# Problem: Return a list of ALL indices where target appears.
#          Print -1 if target not found.
#
# TIME COMPLEXITY: O(n)  — single pass
# SPACE COMPLEXITY: O(k) — k = number of occurrences (result list)

arr    = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
target = 5

def all_occurrences(arr: list, target: int) -> list:
    """Return list of all indices where target appears."""
    indices = []
    for i, num in enumerate(arr):
        if num == target:
            indices.append(i)      # collect every matching index
    return indices if indices else [-1]

# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(k)

result = all_occurrences(arr, target)
print(f"\n  arr    : {arr}")
print(f"  target : {target}")
print(f"  All occurrence indices : {result}")           # Output: [4, 8, 10]
print(f"  Count  : {len(result)}")                      # Output: 3
print(f"  Target 99 not found    : {all_occurrences(arr, 99)}")  # Output: [-1]


# =============================================================================
# SECTION 6: Reverse an Array
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 6: Reverse an Array")
print("=" * 78)

# Problem: Given array of N integers, reverse it.
#
# Visual of the two-pointer technique:
#
#   arr = [ 3,  1,  4,  1,  5,  9,  2,  6,  5,  3,  5 ]
#           ^                                           ^
#         left=0                                    right=10
#         swap(arr[0], arr[10]) → arr[0]=5, arr[10]=3
#
#   arr = [ 5,  1,  4,  1,  5,  9,  2,  6,  5,  3,  3 ]  ← wrong trace, see below
#
#   Step-by-step for arr=[1, 2, 3, 4, 5]:
#   Before: [1, 2, 3, 4, 5]   left=0, right=4
#   Swap 1↔5 → [5, 2, 3, 4, 1]   left=1, right=3
#   Swap 2↔4 → [5, 4, 3, 2, 1]   left=2, right=2  → STOP (left==right)
#   After:  [5, 4, 3, 2, 1] ✓

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# ----- APPROACH 1 (Brute Force): Create a new reversed list -----
# Collect elements in reverse into a new list.
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n) — needs extra storage for the copy

def reverse_brute(arr: list) -> list:
    """Return a NEW reversed list — original unchanged."""
    result = []
    for i in range(len(arr) - 1, -1, -1):
        result.append(arr[i])
    return result

print(f"\n[APPROACH 1 — Brute Force: Create New List] O(n) time, O(n) space")
original = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
reversed_copy = reverse_brute(original)
print(f"  Original : {original}")          # Output: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(f"  Reversed : {reversed_copy}")     # Output: [5, 3, 5, 6, 2, 9, 5, 1, 4, 1, 3]

# ----- APPROACH 2 (Optimal): Two-pointer in-place swap -----
# Use two pointers: one at each end, swap and move inward.
# No extra list needed.
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1) — in-place, no extra storage

def reverse_inplace(arr: list) -> None:
    """Reverse arr in-place using two pointers."""
    i, j = 0, len(arr) - 1
    while i < j:
        arr[i], arr[j] = arr[j], arr[i]   # swap left ↔ right
        i += 1                             # move left pointer inward →
        j -= 1                             # move right pointer inward ←

# TIME COMPLEXITY: O(n) — exactly n//2 swaps
# SPACE COMPLEXITY: O(1)

print(f"\n[APPROACH 2 — Two-Pointer In-Place Swap] O(n) time, O(1) space")
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(f"  Before   : {arr}")               # Output: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
reverse_inplace(arr)
print(f"  After    : {arr}")               # Output: [5, 3, 5, 6, 2, 9, 5, 1, 4, 1, 3]

# ----- Python built-ins -----
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
arr.reverse()                              # in-place, returns None
print(f"\n[Built-in .reverse()]      : {arr}")  # Output: [5, 3, 5, 6, 2, 9, 5, 1, 4, 1, 3]

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
sliced = arr[::-1]                         # slice syntax creates a new list
print(f"[Slice arr[::-1]]          : {sliced}")   # Output: [5, 3, 5, 6, 2, 9, 5, 1, 4, 1, 3]


# =============================================================================
# SECTION 7: Rotate Array by 1 Position (Clockwise / Right Rotate)
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 7: Rotate Array by 1 Position")
print("=" * 78)

# Problem: Right-rotate the array by 1 position (clockwise).
#          Last element moves to the front, everything else shifts right.
#
# Example:
#   Before: [3, 1, 4, 1, 5]
#   After:  [5, 3, 1, 4, 1]   ← last element 5 goes to index 0
#
# Algorithm:
#   1. Save the last element → temp = arr[-1]
#   2. Shift every element one position to the right (from back to front)
#   3. Place temp at arr[0]
#
# TIME COMPLEXITY: O(n)  — each element shifts once
# SPACE COMPLEXITY: O(1) — only one extra variable (temp)

def rotate_by_1(arr: list, n: int) -> None:
    """Right-rotate array by 1 position in-place."""
    temp = arr[-1]                     # Step 1: save the last element
    for i in range(n - 1, 0, -1):
        arr[i] = arr[i - 1]            # Step 2: shift right
    arr[0] = temp                      # Step 3: place saved element at front

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(f"\n  Before : {arr}")            # Output: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
rotate_by_1(arr, len(arr))
print(f"  After  : {arr}")             # Output: [5, 3, 1, 4, 1, 5, 9, 2, 6, 5, 3]


# =============================================================================
# SECTION 8: Rotate Array by K Positions (Right Rotate)
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 8: Rotate Array by K Positions")
print("=" * 78)

# Problem: Right-rotate the array by k positions.
#          k=3: last 3 elements move to the front.
#
# Example:   arr=[1,2,3,4,5], k=2
#   Before:  [1, 2, 3, 4, 5]
#   After:   [4, 5, 1, 2, 3]
#
# ----- APPROACH 1 (Brute Force): Rotate by 1, k times -----
# Call rotate_by_1 k times.
# TIME COMPLEXITY: O(n × k)  — can be O(n²) if k≈n — NOT efficient!
# SPACE COMPLEXITY: O(1)

def k_rotate_brute(arr: list, n: int, k: int) -> None:
    """Brute force: call rotate-by-1 a total of k times."""
    k = k % n                          # handle k > n (full rotations cancel)
    for _ in range(k):
        rotate_by_1(arr, n)

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
k   = 3
print(f"\n[APPROACH 1 — Brute Force: Rotate by 1, k times]  O(n×k) time, O(1) space")
print(f"  Before (k={k}) : {arr}")     # Output: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
k_rotate_brute(arr, len(arr), k)
print(f"  After  (k={k}) : {arr}")     # Output: [5, 3, 5, 3, 1, 4, 1, 5, 9, 2, 6]

# ----- APPROACH 2 (Optimal): Three-Reversal Trick -----
# Discovered by Juggling / Reversal algorithm — O(n) with O(1) space.
#
# Idea for right-rotate by k:
#   Step 1: Reverse the last k elements
#   Step 2: Reverse the first (n-k) elements
#   Step 3: Reverse the entire array
#
# TRACE: arr=[1,2,3,4,5], k=2, n=5
#   Initial:                [1, 2, 3, 4, 5]
#   Step 1: rev last k=2:   [1, 2, 3, 5, 4]
#   Step 2: rev first n-k=3:[3, 2, 1, 5, 4]
#   Step 3: rev entire:      [4, 5, 1, 2, 3] ✓
#
# TIME COMPLEXITY: O(n)  — three passes, each O(n)
# SPACE COMPLEXITY: O(1) — all reversals in-place

def reverse_segment(arr: list, left: int, right: int) -> None:
    """Reverse arr[left..right] in-place using two pointers."""
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left  += 1
        right -= 1

def k_rotate_optimal(arr: list, k: int) -> None:
    """Right-rotate array by k positions using three-reversal trick."""
    n = len(arr)
    k = k % n                          # handle k > n
    # Step 1: Reverse the last k elements  [n-k .. n-1]
    reverse_segment(arr, n - k, n - 1)
    # Step 2: Reverse the first (n-k) elements  [0 .. n-k-1]
    reverse_segment(arr, 0, n - k - 1)
    # Step 3: Reverse the entire array  [0 .. n-1]
    reverse_segment(arr, 0, n - 1)

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
k   = 3
print(f"\n[APPROACH 2 — Three-Reversal Trick]  O(n) time, O(1) space")
print(f"  Before (k={k}) : {arr}")     # Output: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
k_rotate_optimal(arr, k)
print(f"  After  (k={k}) : {arr}")     # Output: [5, 3, 5, 3, 1, 4, 1, 5, 9, 2, 6]

# ----- Pythonic one-liner (slicing) -----
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
k   = 3
n   = len(arr)
arr_rotated = arr[n - k:] + arr[:n - k]   # O(n) time, O(n) space
print(f"\n[Pythonic Slice]  O(n) time, O(n) space")
print(f"  arr[n-k:] + arr[:n-k] = {arr_rotated}")   # Output: [5, 3, 5, 3, 1, 4, 1, 5, 9, 2, 6]


# =============================================================================
# SECTION 9: Maximum of 3 Numbers
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 9: Maximum of 3 Numbers")
print("=" * 78)

# Problem: Given three numbers a, b, c — find the largest.
#
# TIME COMPLEXITY: O(1)  — fixed number of comparisons, independent of input
# SPACE COMPLEXITY: O(1)

a, b, c = 7, 2, 9

# ----- Manual if-elif-else -----
def max_of_3(a: int, b: int, c: int) -> int:
    """Return the maximum of three integers."""
    if a > b and a > c:
        return a           # a wins
    elif b > c:
        return b           # b wins
    else:
        return c           # c wins (includes the case b == c)

# TIME COMPLEXITY: O(1)
# SPACE COMPLEXITY: O(1)

result = max_of_3(a, b, c)
print(f"\n  a={a}, b={b}, c={c}")
print(f"  max_of_3({a}, {b}, {c})  = {result}")      # Output: 9

# ----- Built-in max() -----
print(f"  max({a}, {b}, {c})       = {max(a, b, c)}")    # Output: 9
print(f"  max([{a},{b},{c}]) = {max([a, b, c])}")        # Output: 9


# =============================================================================
# SECTION 10: Largest of N Numbers
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 10: Largest of N Numbers")
print("=" * 78)

# Problem: Given an array of N numbers, find the largest element.
#
# TIME COMPLEXITY: O(n)  — must look at every element at least once
# SPACE COMPLEXITY: O(1)

numbers = [44, 33, 96, 1, 3, 5, 903, 234, 999, 123, 22, 35, 67, 83]
print(f"\n  numbers = {numbers}")

# ----- Approach 1: Index-based loop -----
largest = numbers[0]                   # assume first is largest
for i in range(len(numbers)):
    if numbers[i] > largest:
        largest = numbers[i]
print(f"  Largest (index loop) : {largest}")  # Output: 999

# ----- Approach 2: Direct iteration (no index) -----
largest = numbers[0]
for num in numbers:
    if num > largest:
        largest = num
print(f"  Largest (for-in)     : {largest}")  # Output: 999

# ----- Approach 3: float('-inf') initialisation (handles empty-safe) -----
largest = float('-inf')
for num in numbers:
    if num > largest:
        largest = num
print(f"  Largest (-inf init)  : {largest}")  # Output: 999

# ----- Built-in -----
print(f"  max(numbers)         : {max(numbers)}")  # Output: 999


# =============================================================================
# SECTION 11: The Stack Data Structure
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 11: Stack Data Structure — LIFO")
print("=" * 78)

# A STACK is a linear data structure that follows:
#   LIFO = Last In, First Out
#   (Like a stack of plates — you take from the TOP)
#
# Two fundamental operations:
#   push(item) — add item to the TOP            O(1) amortized
#   pop()      — remove & return item from TOP  O(1)
#
# Additional helpers:
#   peek()     — view top without removing      O(1)
#   is_empty() — check if stack has no items    O(1)
#   size()     — number of items                O(1)
#
# Python list works perfectly as a stack:
#   push  → list.append()
#   pop   → list.pop()  (removes last = top)
#
# Visual:
#   push(10) push(20) push(30)
#   ┌──────┐
#   │  30  │  ← TOP (most recently pushed)
#   │  20  │
#   │  10  │  ← BOTTOM (first pushed)
#   └──────┘
#   pop() → returns 30, stack becomes [10, 20]

class Stack:
    """A clean Stack implementation backed by a Python list."""

    def __init__(self):
        self.items = []                 # internal storage

    def push(self, item):
        """Push item onto the top of the stack. O(1) amortized."""
        self.items.append(item)

    def pop(self):
        """Remove and return top item. Returns None if empty. O(1)."""
        if self.is_empty():
            print("  ⚠  Stack underflow — cannot pop from empty stack")
            return None
        return self.items.pop()        # list.pop() removes the LAST element

    def peek(self):
        """Return top item WITHOUT removing it. Returns None if empty. O(1)."""
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self) -> bool:
        """Return True if stack has no items. O(1)."""
        return len(self.items) == 0

    def size(self) -> int:
        """Return number of items in the stack. O(1)."""
        return len(self.items)

    def __str__(self) -> str:
        """String representation — top of stack is shown on the right."""
        return f"Stack(bottom → top): {self.items}"


# Demonstration
print()
s = Stack()
print(f"  Empty?      : {s.is_empty()}")    # Output: True

s.push(10)
s.push(20)
s.push(30)
s.push(40)
print(f"  After push 10,20,30,40 : {s}")   # Output: Stack(...): [10, 20, 30, 40]
print(f"  Size        : {s.size()}")        # Output: 4
print(f"  Peek (top)  : {s.peek()}")        # Output: 40

popped = s.pop()
print(f"  pop() → {popped}, now: {s}")      # Output: 40, Stack: [10, 20, 30]

s.pop()
s.pop()
s.pop()
print(f"  After 3 more pops: {s}")          # Output: Stack(...): []
s.pop()                                     # Output: ⚠ Stack underflow


# =============================================================================
# SECTION 12: USE CASE 1 — Browser History (Stack)
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 12: Use Case 1 — Browser History (Stack)")
print("=" * 78)

# Real-world analogy: your browser's ← Back and → Forward buttons.
#
# When you visit a page:
#   • push the URL onto a "back stack"
#   • clear the "forward stack" (new navigation kills forward history)
#
# When you press ← Back:
#   • pop from back stack → push to forward stack
#
# When you press → Forward:
#   • pop from forward stack → push to back stack
#
# Sequence diagram (simplified):
#   visit(google.com)      → back=[google.com]        forward=[]
#   visit(github.com)      → back=[google,github]     forward=[]
#   visit(stackoverflow)   → back=[google,github,so]  forward=[]
#   back()                 → back=[google,github]      forward=[so]
#   back()                 → back=[google]             forward=[so,github]
#   forward()              → back=[google,github]      forward=[so]

class BrowserHistory:
    """Browser history manager using two stacks."""

    def __init__(self, homepage: str):
        self._back    = Stack()        # pages we can go back to
        self._forward = Stack()        # pages we can go forward to
        self._current = homepage
        print(f"  🌐 Opened browser on: {homepage}")

    def visit(self, url: str) -> None:
        """Navigate to a new URL."""
        self._back.push(self._current) # current page goes onto back stack
        self._current = url
        # clear forward history — just like a real browser
        self._forward = Stack()
        print(f"  📄 Visited  : {url}  | back={self._back.items} | fwd={self._forward.items}")

    def back(self) -> str:
        """Go back one page. Returns current page after action."""
        if self._back.is_empty():
            print(f"  ⬅  Can't go back — already at beginning")
            return self._current
        self._forward.push(self._current)
        self._current = self._back.pop()
        print(f"  ⬅  Back to : {self._current}  | back={self._back.items} | fwd={self._forward.items}")
        return self._current

    def forward(self) -> str:
        """Go forward one page. Returns current page after action."""
        if self._forward.is_empty():
            print(f"  ➡  Can't go forward — no forward history")
            return self._current
        self._back.push(self._current)
        self._current = self._forward.pop()
        print(f"  ➡  Fwd to  : {self._current}  | back={self._back.items} | fwd={self._forward.items}")
        return self._current

    def current_page(self) -> str:
        """Return the currently displayed URL."""
        return self._current


# TIME COMPLEXITY: O(1) per operation (push/pop are O(1))
# SPACE COMPLEXITY: O(n) — n = total pages visited

print()
browser = BrowserHistory("about:blank")
browser.visit("https://google.com")
browser.visit("https://github.com")
browser.visit("https://stackoverflow.com")
browser.back()                              # stackoverflow → github
browser.back()                              # github → google
browser.forward()                           # google → github
browser.back()                              # try going back from about:blank? No:
browser.back()
browser.back()                              # already at beginning
print(f"\n  Current page: {browser.current_page()}")  # Output: about:blank


# =============================================================================
# SECTION 13: USE CASE 2 — Valid Parentheses (Stack)
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 13: Use Case 2 — Valid Parentheses (Stack)")
print("=" * 78)

# Problem: Given a string of (), {}, [] — check if all brackets are matched.
#
# ----- APPROACH 1 (Brute Force): Count opens and closes -----
# Count opening brackets → must equal closing brackets.
# PROBLEM: does NOT catch `)(` ordering errors!
#
# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(1)

def is_valid_brute(s: str) -> bool:
    """
    BRUTE FORCE — count approach.
    FAILS for: ')(' (count matches but order is wrong!)
    """
    open_count  = s.count('(') + s.count('{') + s.count('[')
    close_count = s.count(')') + s.count('}') + s.count(']')
    return open_count == close_count

print("\n[APPROACH 1 — Brute Force: Count Opens vs Closes]")
print(f"  '({{[]}})' → {is_valid_brute('({[]})')}")     # Output: True  (correct)
print(f"  '({{[}})'  → {is_valid_brute('({[})')}")      # Output: True  ← WRONG! Should be False
print(f"  ')('       → {is_valid_brute(')(')}")          # Output: True  ← WRONG!
print(f"  '(('       → {is_valid_brute('((')}")          # Output: False (correct)

# ----- APPROACH 2 (Optimal): Stack-based matching -----
# Rule:
#   • Opening bracket  → PUSH onto stack
#   • Closing bracket  → POP from stack; check if it matches
#   • At the end, stack must be EMPTY (every open has a close)
#
# TRACE for "({[]})":
#   char='(' → push → stack=['(']
#   char='{' → push → stack=['(', '{']
#   char='[' → push → stack=['(', '{', '[']
#   char=']' → pop → top='[' matches ']' ✓ → stack=['(', '{']
#   char='}' → pop → top='{' matches '}' ✓ → stack=['(']
#   char=')' → pop → top='(' matches ')' ✓ → stack=[]
#   stack empty → True ✓
#
# TIME COMPLEXITY: O(n)  — single pass
# SPACE COMPLEXITY: O(n) — stack can hold all opening brackets in worst case

def is_valid_parentheses(s: str) -> bool:
    """
    OPTIMAL — Stack approach.
    Correctly handles all cases including ordering errors.
    """
    bracket_map = {')': '(', '}': '{', ']': '['}  # closing → its expected opener
    stack = []
    for char in s:
        if char in bracket_map:
            # It's a closing bracket
            top = stack.pop() if stack else '#'    # '#' = dummy if stack empty
            if bracket_map[char] != top:
                return False                       # mismatch!
        else:
            stack.append(char)                     # it's an opening bracket → push
    return len(stack) == 0                         # True only if all opens were matched

# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n)

print("\n[APPROACH 2 — Optimal: Stack-Based Matching]")
test_cases = [
    ("({[]})",  True),
    ("({[})",   False),
    ("((",      False),
    (")()",     False),
    ("()[]{}", True),
    ("",        True),
]
for expr, expected in test_cases:
    got = is_valid_parentheses(expr)
    status = "✓" if got == expected else "✗"
    print(f"  {status} is_valid('{expr}') → {got}  (expected {expected})")
    # Outputs: ✓ True / ✓ False for each case


# =============================================================================
# SECTION 14: USE CASE 3 — Reverse Polish Notation / Postfix Evaluation (Stack)
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 14: Use Case 3 — Reverse Polish Notation (Postfix Evaluation)")
print("=" * 78)

# Postfix (Reverse Polish Notation) puts operators AFTER their operands.
# No parentheses needed — operator precedence is explicit in position.
#
# Examples:
#   Infix:   2 + 3      →  Postfix: "2 3 +"
#   Infix:   (2+3)*4    →  Postfix: "2 3 + 4 *"
#   Infix:   2 + 3 * 4  →  Postfix: "2 3 4 * +"  (multiplication first)
#
# ALGORITHM (stack-based):
#   Scan tokens left → right:
#     • If token is a NUMBER → push onto stack
#     • If token is an OPERATOR (+,-,*,/) →
#           pop op2 (top),  pop op1 (below top)
#           compute op1 <operator> op2
#           push result back onto stack
#   Final answer = single item remaining on stack
#
# TRACE for ["2", "1", "+", "3", "*"]:
#   "2"  → push → stack=[2]
#   "1"  → push → stack=[2, 1]
#   "+"  → pop 1 (op2), pop 2 (op1), push 2+1=3 → stack=[3]
#   "3"  → push → stack=[3, 3]
#   "*"  → pop 3 (op2), pop 3 (op1), push 3*3=9 → stack=[9]
#   Result = 9 ✓   (= (2+1)*3 = 9)
#
# TIME COMPLEXITY: O(n)  — one pass through all tokens
# SPACE COMPLEXITY: O(n) — stack holds at most n/2 numbers at once

def evaluate_postfix(tokens: list) -> int | float:
    """
    Evaluate a Reverse Polish Notation expression.
    tokens: list of strings, e.g. ["2", "1", "+", "3", "*"]
    Returns: computed integer or float result.
    """
    stack = []
    operators = {'+', '-', '*', '/'}

    for token in tokens:
        if token not in operators:
            stack.append(int(token))   # it's a number → push
        else:
            op2 = stack.pop()          # second operand (top)
            op1 = stack.pop()          # first operand  (below top)
            if   token == '+': stack.append(op1 + op2)
            elif token == '-': stack.append(op1 - op2)
            elif token == '*': stack.append(op1 * op2)
            elif token == '/': stack.append(int(op1 / op2))  # integer division
    return stack.pop()

# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n)

tests = [
    (["2", "1", "+", "3", "*"],     9),    # (2+1)*3 = 9
    (["4", "13", "5", "/", "+"],    6),    # 4 + (13/5) = 4+2 = 6
    (["2", "3", "+", "4", "*"],    20),    # (2+3)*4 = 20
    (["5", "1", "2", "+", "4", "*", "+", "3", "-"], 14),  # 5+(1+2)*4-3=14
]
print()
for tokens, expected in tests:
    result = evaluate_postfix(tokens)
    status = "✓" if result == expected else "✗"
    print(f"  {status} {' '.join(tokens):35s} → {result}  (expected {expected})")


# =============================================================================
# SECTION 15: USE CASE 4 — FB Friend Recommendation (Graph + Adjacency List)
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 15: Use Case 4 — FB Friend Recommendation (Graph)")
print("=" * 78)

# A social network can be modelled as an UNDIRECTED GRAPH:
#   • Each person = a VERTEX (node)
#   • Each friendship = an EDGE (bidirectional)
#
# We store the graph as an ADJACENCY LIST:
#   graph = { "alice": ["bob", "carol"], "bob": ["alice", "dave"], ... }
#
# FRIEND RECOMMENDATION RULE:
#   "People your friends know that you don't already know"
#   i.e., friends-of-friends who are NOT already your friends (and not yourself)
#
# ----- APPROACH 1 (Brute Force): Nested loop with list membership -----
# For each friend, iterate over that friend's friends.
# Check if each friend-of-friend is already in your friend list using `in`.
# List `in` is O(n) → total is O(n²) for a person with n friends.
#
# TIME COMPLEXITY: O(n²)
# SPACE COMPLEXITY: O(n)

def build_graph() -> dict:
    """Build a small social network adjacency list."""
    graph = {}

    def add_node(name: str):
        if name not in graph:
            graph[name] = []

    def add_edge(n1: str, n2: str):
        graph[n1].append(n2)
        graph[n2].append(n1)

    # Add people
    for name in ["alice", "bob", "carol", "dave", "eve"]:
        add_node(name)

    # Friendships (undirected edges)
    add_edge("alice", "bob")
    add_edge("alice", "carol")
    add_edge("bob",   "dave")
    add_edge("carol", "dave")
    add_edge("dave",  "eve")

    return graph

graph = build_graph()
print(f"\n  Graph (adjacency list):")
for person, friends in graph.items():
    print(f"    {person:6s} → {friends}")

def recommend_brute(graph: dict, person: str) -> list:
    """
    BRUTE FORCE — O(n²): uses list membership check inside nested loop.
    """
    recommendations = []
    my_friends = graph[person]

    for friend in my_friends:
        for fof in graph[friend]:          # friend-of-friend
            if fof != person and fof not in my_friends:
                if fof not in recommendations:
                    recommendations.append(fof)  # O(n) check each time

    return sorted(recommendations)

# TIME COMPLEXITY: O(n²) where n = average number of friends
# SPACE COMPLEXITY: O(n)

print(f"\n[APPROACH 1 — Brute Force: O(n²) list membership]")
person = "alice"
recs = recommend_brute(graph, person)
print(f"  Recommendations for '{person}': {recs}")  # Output: ['dave']

# ----- APPROACH 2 (Optimal): Use Python sets for O(1) lookup -----
# Convert friend list to a set → `in` check is O(1).
# Total: O(n) for a person with n friends.
#
# TIME COMPLEXITY: O(n)  — n = total friends + friends-of-friends
# SPACE COMPLEXITY: O(n) — the set of current friends

def recommend_optimal(graph: dict, person: str) -> list:
    """
    OPTIMAL — O(n): uses set for O(1) membership test.
    """
    my_friends = set(graph[person])       # O(1) lookup instead of O(n)
    recommendations = set()

    for friend in my_friends:
        for fof in graph[friend]:
            if fof != person and fof not in my_friends:
                recommendations.add(fof)  # O(1) add & membership check

    return sorted(recommendations)

# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n)

print(f"\n[APPROACH 2 — Optimal: O(n) set-based lookup]")
for person in graph:
    recs = recommend_optimal(graph, person)
    print(f"  Recommendations for '{person:6s}': {recs}")
    # alice  → ['dave']
    # bob    → ['carol', 'eve']
    # carol  → ['bob', 'eve']
    # dave   → ['alice']
    # eve    → ['bob', 'carol']


# =============================================================================
# SECTION 16: BIG-O SUMMARY
# =============================================================================
print("\n" + "=" * 78)
print("  SECTION 16: Big-O Summary — All Algorithms in This Module")
print("=" * 78)

summary = """
  ┌────────────────────────────────────────────┬───────────┬───────────┐
  │ Algorithm                                  │   Time    │   Space   │
  ├────────────────────────────────────────────┼───────────┼───────────┤
  │ Array traversal / sum / max / min          │   O(n)    │   O(1)    │
  │ First occurrence — linear scan             │   O(n)    │   O(1)    │
  │ First occurrence — binary search (sorted)  │  O(log n) │   O(1)    │
  │ Last occurrence — scan from back           │   O(n)    │   O(1)    │
  │ All occurrences — single pass              │   O(n)    │   O(k)    │
  │ Reverse — brute force (new list)           │   O(n)    │   O(n)    │
  │ Reverse — two-pointer in-place             │   O(n)    │   O(1)    │
  │ Rotate by 1                                │   O(n)    │   O(1)    │
  │ K-rotate — brute force (k × rotate-by-1)  │  O(n×k)   │   O(1)    │
  │ K-rotate — three-reversal trick            │   O(n)    │   O(1)    │
  │ Maximum of 3                               │   O(1)    │   O(1)    │
  │ Largest of n                               │   O(n)    │   O(1)    │
  │ Stack push / pop / peek                    │   O(1)    │   O(1)    │
  │ Valid parentheses (stack)                  │   O(n)    │   O(n)    │
  │ Postfix evaluation (stack)                 │   O(n)    │   O(n)    │
  │ Friend recommendation — brute force        │   O(n²)   │   O(n)    │
  │ Friend recommendation — optimal (sets)     │   O(n)    │   O(n)    │
  └────────────────────────────────────────────┴───────────┴───────────┘
"""
print(summary)


# =============================================================================
# === PRACTICE ZONE ===
# =============================================================================
print("=" * 78)
print("  === PRACTICE ZONE ===")
print("  Uncomment each challenge, implement it, and run the file.")
print("=" * 78)

# ─── Challenge 1 ────────────────────────────────────────────────────────────
# Find the SECOND largest element in an array (without sorting).
# Hint: track two variables: largest and second_largest.
# Test: arr = [3, 1, 4, 1, 5, 9, 2, 6]  →  Expected: 6
# TIME COMPLEXITY: O(?)  SPACE COMPLEXITY: O(?)

# def second_largest(arr):
#     pass
#
# arr = [3, 1, 4, 1, 5, 9, 2, 6]
# print(f"\n[Challenge 1] Second largest: {second_largest(arr)}")  # Expected: 6


# ─── Challenge 2 ────────────────────────────────────────────────────────────
# Given a sorted array, remove duplicates IN-PLACE and return the new length.
# (Like LeetCode #26)
# Test: arr = [1, 1, 2, 3, 3, 4, 5, 5, 5]  →  Expected length: 5, arr[:5]=[1,2,3,4,5]
# Hint: Two-pointer technique — slow and fast pointers.
# TIME COMPLEXITY: O(?)  SPACE COMPLEXITY: O(?)

# def remove_duplicates_inplace(arr):
#     pass
#
# arr = [1, 1, 2, 3, 3, 4, 5, 5, 5]
# length = remove_duplicates_inplace(arr)
# print(f"\n[Challenge 2] Unique length: {length}, Array: {arr[:length]}")


# ─── Challenge 3 ────────────────────────────────────────────────────────────
# Implement a stack that supports push(), pop(), and get_min() all in O(1).
# Hint: maintain a parallel "min stack".
# Test:
#   s.push(5); s.push(3); s.push(7); s.push(2)
#   s.get_min() → 2
#   s.pop()     (removes 2)
#   s.get_min() → 3

# class MinStack:
#     def __init__(self): ...
#     def push(self, val): ...
#     def pop(self): ...
#     def get_min(self): ...
#
# ms = MinStack()
# ms.push(5); ms.push(3); ms.push(7); ms.push(2)
# print(f"\n[Challenge 3] Min after push(5,3,7,2): {ms.get_min()}")  # Expected: 2
# ms.pop()
# print(f"[Challenge 3] Min after pop()         : {ms.get_min()}")  # Expected: 3


# ─── Challenge 4 ────────────────────────────────────────────────────────────
# Left-rotate an array by k positions (instead of right-rotate).
# Approach: use the three-reversal trick — think about what changes!
# Test: arr=[1,2,3,4,5], k=2  →  Expected: [3, 4, 5, 1, 2]
# TIME COMPLEXITY: O(?)  SPACE COMPLEXITY: O(?)

# def left_rotate_k(arr, k):
#     pass
#
# arr = [1, 2, 3, 4, 5]
# left_rotate_k(arr, 2)
# print(f"\n[Challenge 4] Left-rotate by 2: {arr}")  # Expected: [3, 4, 5, 1, 2]


# ─── Challenge 5 ────────────────────────────────────────────────────────────
# Evaluate a PREFIX expression (Polish Notation) using a stack.
# Prefix: operator comes BEFORE operands.  Read RIGHT → LEFT.
# Example: ["*", "+", "2", "3", "4"]  means  (2+3)*4 = 20
# Hint: scan tokens from right to left; push numbers, apply op on two pops.
# TIME COMPLEXITY: O(?)  SPACE COMPLEXITY: O(?)

# def evaluate_prefix(tokens):
#     pass
#
# tokens = ["*", "+", "2", "3", "4"]
# print(f"\n[Challenge 5] Prefix eval: {evaluate_prefix(tokens)}")  # Expected: 20


# ─── Challenge 6 ────────────────────────────────────────────────────────────
# Extend the BrowserHistory class with a clear_history() method that empties
# both the back and forward stacks (like "Clear All History" in a browser).
# After clearing, current_page() should still return the current URL.

# class ExtendedBrowserHistory(BrowserHistory):
#     def clear_history(self):
#         pass
#
# b = ExtendedBrowserHistory("google.com")
# b.visit("github.com"); b.visit("stackoverflow.com")
# b.back()
# b.clear_history()
# print(f"\n[Challenge 6] After clear, back attempt:")
# b.back()    # Should print: Can't go back — already at beginning


print("\n" + "=" * 78)
print("  END OF MODULE 07 — DATA STRUCTURES: ARRAYS & STACKS")
print("=" * 78)
