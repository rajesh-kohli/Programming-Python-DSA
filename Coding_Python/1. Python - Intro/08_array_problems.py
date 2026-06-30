# ============================================================================
#  09 - ARRAY PROBLEM-SOLVING: SEARCH, REVERSE, ROTATE, AND CLASSIC PATTERNS
# ============================================================================
# A comprehensive guide to fundamental array algorithms commonly asked in
# coding interviews. Every section is runnable — execute this file to see
# all outputs.
# ============================================================================


# ===== SECTION 1: Array Problem-Solving Patterns (Overview) =================
# Before diving into specific problems, here are the four most common
# approaches you will see again and again in array questions:
#
# 1. TWO POINTERS
#    - Use two index variables (often i at start, j at end) moving toward
#      each other or in the same direction.
#    - Examples: reverse array, remove duplicates, partition around pivot.
#    - Why it works: reduces a nested-loop O(n^2) scan to a single O(n) pass.
#
# 2. SLIDING WINDOW
#    - Maintain a "window" [left..right] over the array, expanding or
#      shrinking it as needed.
#    - Examples: max sum of k consecutive elements, longest substring
#      without repeating characters.
#    - Why it works: avoids recalculating the entire window from scratch;
#      each element enters and leaves the window at most once.
#
# 3. PREFIX SUM
#    - Build a helper array where prefix[i] = sum of arr[0..i].
#    - Then sum of any subarray arr[l..r] = prefix[r] - prefix[l-1].
#    - Examples: range sum queries, subarray sum equals k.
#    - Why it works: O(n) precomputation lets you answer each query in O(1).
#
# 4. FREQUENCY COUNTING (Hash Map)
#    - Use a dictionary to count how many times each element appears.
#    - Examples: two-sum, find duplicates, majority element.
#    - Why it works: dictionary lookup is O(1) on average, so scanning +
#      looking up stays O(n).
#
# This file focuses on two-pointer and single-pass techniques. Sliding
# window and prefix sum are covered in later modules.
# ============================================================================

print("=" * 70)
print("  09 - ARRAY PROBLEMS: SEARCH, REVERSE, ROTATE, AND MORE")
print("=" * 70)


# ===== SECTION 2: Linear Search — First Occurrence ========================
print("\n" + "=" * 70)
print("  SECTION 2: Linear Search — First Occurrence")
print("=" * 70)

# Problem: Given an array and a target value, return the INDEX of the first
#          element that equals the target. Return -1 if not found.
#
# Approach: Walk from left to right. The moment we find a match, return
#           immediately (early return). If we finish the loop without
#           finding anything, return -1.
#
# Time : O(n) — in the worst case we visit every element.
# Space: O(1) — we only use a few variables, no extra data structures.


# --- Method 1: Using enumerate() (Pythonic) ---
def first_occurrence(arr, target):
    """Return index of first occurrence of target, or -1 if not found."""
    for i, num in enumerate(arr):
        if num == target:
            return i          # early return — stop as soon as we find it
    return -1                 # reached end without finding target


# --- Method 2: Using a plain index variable ---
def first_occurrence_v2(arr, target):
    """Same logic, using range() instead of enumerate()."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


# --- Method 3: Using built-in list.index() ---
def first_occurrence_v3(arr, target):
    """Wraps the built-in .index() which raises ValueError if not found."""
    try:
        return arr.index(target)
    except ValueError:
        return -1


# Demonstration
arr = [10, 20, 30, 20, 40, 20]
target = 20

print(f"\nArray : {arr}")
print(f"Target: {target}")
print(f"first_occurrence       -> index {first_occurrence(arr, target)}")
print(f"first_occurrence_v2    -> index {first_occurrence_v2(arr, target)}")
print(f"first_occurrence_v3    -> index {first_occurrence_v3(arr, target)}")
print(f"Target 99 (not found)  -> index {first_occurrence(arr, 99)}")


# ===== SECTION 3: Linear Search — Last Occurrence =========================
print("\n" + "=" * 70)
print("  SECTION 3: Linear Search — Last Occurrence")
print("=" * 70)

# Problem: Return the INDEX of the LAST occurrence of target.
#
# Key idea: iterate BACKWARDS. The first match we hit while going right-to-
# left IS the last occurrence.
#
# range(n-1, -1, -1) explained:
#   start = n-1   (last valid index)
#   stop  = -1    (we go down to 0; stop is exclusive, so -1 means "include 0")
#   step  = -1    (decrement by 1 each iteration)
#   Produces: n-1, n-2, n-3, ..., 2, 1, 0
#
# Time : O(n)
# Space: O(1)


def last_occurrence(arr, target):
    """Return index of last occurrence of target, or -1 if not found."""
    n = len(arr)
    for i in range(n - 1, -1, -1):   # walk backwards from end to start
        if arr[i] == target:
            return i                  # first match going backwards = last occ
    return -1


# Demonstration
arr = [10, 20, 30, 20, 40, 20]
target = 20

print(f"\nArray : {arr}")
print(f"Target: {target}")
print(f"last_occurrence -> index {last_occurrence(arr, target)}")
print(f"Target 99       -> index {last_occurrence(arr, 99)}")

# Visual trace for arr = [10, 20, 30, 20, 40, 20], target = 20:
#   i=5: arr[5]=20 == 20 -> return 5  (done!)
# We never even check indices 4, 3, 2, 1, 0.


# ===== SECTION 4: Find All Occurrences =====================================
print("\n" + "=" * 70)
print("  SECTION 4: Find All Occurrences")
print("=" * 70)

# Problem: Return a LIST of all indices where target appears.
#
# Time : O(n) — must check every element.
# Space: O(k) — where k is the number of matches (the result list).


# --- Method 1: Loop with a flag ---
def all_occurrences_v1(arr, target):
    """Print all indices; print -1 if none found. (Mirrors source style)"""
    found = False
    indices = []
    for i, num in enumerate(arr):
        if num == target:
            found = True
            indices.append(i)
    return indices if found else [-1]


# --- Method 2: List comprehension (Pythonic one-liner) ---
def all_occurrences(arr, target):
    """Return list of all indices where arr[i] == target."""
    result = [i for i, num in enumerate(arr) if num == target]
    return result if result else [-1]


# Demonstration
arr = [10, 20, 30, 20, 40, 20]
target = 20

print(f"\nArray : {arr}")
print(f"Target: {target}")
print(f"all_occurrences (loop)          -> {all_occurrences_v1(arr, target)}")
print(f"all_occurrences (comprehension) -> {all_occurrences(arr, target)}")
print(f"Target 99 (not found)           -> {all_occurrences(arr, 99)}")


# ===== SECTION 5: Reverse Array In-Place (Two Pointer Technique) ===========
print("\n" + "=" * 70)
print("  SECTION 5: Reverse Array In-Place (Two Pointer Technique)")
print("=" * 70)

# Problem: Reverse the array WITHOUT creating a new array.
#
# Algorithm:
#   1. Place pointer i at the start, pointer j at the end.
#   2. Swap arr[i] and arr[j].
#   3. Move i forward, j backward.
#   4. Stop when i >= j (pointers have crossed).
#
# Visual diagram for [10, 20, 30, 40, 50]:
#
#   Step 0:  [10, 20, 30, 40, 50]
#              i               j       swap 10 <-> 50
#
#   Step 1:  [50, 20, 30, 40, 10]
#                  i       j           swap 20 <-> 40
#
#   Step 2:  [50, 40, 30, 20, 10]
#                      ij              i >= j, STOP. 30 stays in place.
#
# Time : O(n/2) ~ O(n) — we do n/2 swaps.
# Space: O(1) — only two index variables and a temp (Python swap is built-in).
#
# COMPARISON WITH OTHER METHODS:
#   arr[::-1]       -> creates a NEW reversed list -> O(n) extra space
#   arr.reverse()   -> in-place, O(1) space (uses the same two-pointer idea)
#   list(reversed(arr)) -> creates a NEW list -> O(n) extra space
#
# NOTE: This reverse function is the FOUNDATION for the rotation algorithm
#       in Section 7. Make sure you understand it well!


def reverse_array(arr, start, end):
    """Reverse arr[start..end] in-place using two pointers."""
    i, j = start, end
    while i < j:
        arr[i], arr[j] = arr[j], arr[i]   # Pythonic swap, no temp needed
        i += 1
        j -= 1


# Demonstration with step-by-step trace
arr = [10, 20, 30, 40, 50]
print(f"\nOriginal: {arr}")

# Step-by-step walkthrough
demo = arr.copy()
i, j = 0, len(demo) - 1
step = 0
while i < j:
    print(f"  Step {step}: swap arr[{i}]={demo[i]} <-> arr[{j}]={demo[j]}", end="")
    demo[i], demo[j] = demo[j], demo[i]
    i += 1
    j -= 1
    print(f"  -> {demo}")
    step += 1

print(f"Reversed: {demo}")

# Using our function
arr2 = [10, 20, 30, 40, 50]
reverse_array(arr2, 0, len(arr2) - 1)
print(f"Using reverse_array(): {arr2}")

# Compare with built-in
arr3 = [10, 20, 30, 40, 50]
print(f"Using [::-1]:          {arr3[::-1]}  (creates new list, O(n) space)")


# ===== SECTION 6: Rotate Array Right by 1 ==================================
print("\n" + "=" * 70)
print("  SECTION 6: Rotate Array Right by 1")
print("=" * 70)

# Problem: Move every element one position to the right. The last element
#          wraps around to the front.
#
# Example: [1, 2, 3, 4, 5] -> [5, 1, 2, 3, 4]
#
# Algorithm:
#   1. Save the last element in a variable (temp).
#   2. Shift every element one position to the right, starting from the end.
#      (We go right-to-left so we don't overwrite values we still need.)
#   3. Place temp at index 0.
#
# Walkthrough for [1, 2, 3, 4, 5]:
#   temp = 5
#   i=4: arr[4] = arr[3] = 4  -> [1, 2, 3, 4, 4]
#   i=3: arr[3] = arr[2] = 3  -> [1, 2, 3, 3, 4]
#   i=2: arr[2] = arr[1] = 2  -> [1, 2, 2, 3, 4]
#   i=1: arr[1] = arr[0] = 1  -> [1, 1, 2, 3, 4]
#   arr[0] = temp = 5         -> [5, 1, 2, 3, 4]
#
# Time : O(n) — one pass through the array.
# Space: O(1) — only one extra variable (temp).


def rotate_right_by_1(arr):
    """Rotate arr one position to the right in-place."""
    n = len(arr)
    temp = arr[-1]                     # save last element

    for i in range(n - 1, 0, -1):      # shift from right to left
        arr[i] = arr[i - 1]

    arr[0] = temp                      # place saved element at front


# Alternative using adjacent swaps (from source 006rotateArray2.py):
def rotate_right_by_1_v2(arr):
    """Rotate right by 1 using bubble-style adjacent swaps."""
    n = len(arr)
    for i in range(n - 1, 0, -1):
        arr[i], arr[i - 1] = arr[i - 1], arr[i]
    # The last element "bubbles" to the front through n-1 swaps.


# Demonstration
arr = [1, 2, 3, 4, 5]
print(f"\nOriginal:          {arr}")
rotate_right_by_1(arr)
print(f"After rotate by 1: {arr}")

arr2 = [1, 2, 3, 4, 5]
rotate_right_by_1_v2(arr2)
print(f"Using swap method: {arr2}")


# ===== SECTION 7: Rotate Array Right by K (Reversal Algorithm) =============
print("\n" + "=" * 70)
print("  SECTION 7: Rotate Array Right by K (Reversal Algorithm)")
print("  *** MOST IMPORTANT ALGORITHM IN THIS FILE ***")
print("=" * 70)

# Problem: Rotate the array to the right by K positions.
#
# Example: [1, 2, 3, 4, 5], k=2  ->  [4, 5, 1, 2, 3]
#
# ---------- THE NAIVE APPROACH (too slow) ----------
# Call rotate_right_by_1() k times.
# Time: O(n * k) — each rotation is O(n), done k times.
# If k is close to n, this becomes O(n^2). Not acceptable for large arrays.
#
# ---------- THE REVERSAL ALGORITHM (optimal) ----------
# Three reverses:
#   Step 1: Reverse the ENTIRE array.
#   Step 2: Reverse the FIRST k elements.
#   Step 3: Reverse the REMAINING n-k elements.
#
# Time : O(n) — three passes, each at most O(n).
# Space: O(1) — all reverses are in-place.
#
# Handle edge case: if k > n, use k = k % n
#   (rotating by n gives the same array, so only the remainder matters)
#
# ---------- FULL VISUAL WALKTHROUGH ----------
# arr = [1, 2, 3, 4, 5], k = 2, n = 5
#
# Step 0 (original):
#   [1, 2, 3, 4, 5]
#    ^-----------^
#    n-k=3 elems   k=2 elems
#
# Step 1: Reverse entire array [0..4]:
#   [5, 4, 3, 2, 1]
#
# Step 2: Reverse first k=2 elements [0..1]:
#   [4, 5, 3, 2, 1]
#    ^--^
#
# Step 3: Reverse remaining n-k=3 elements [2..4]:
#   [4, 5, 1, 2, 3]
#          ^-----^
#
# Result: [4, 5, 1, 2, 3]  -- correct!
#
# ---------- WHY DOES THIS WORK? (Mathematical Explanation) ----------
# Think of the array as two parts:
#   A = [1, 2, 3]  (first n-k elements)
#   B = [4, 5]     (last k elements)
#   Original = A + B
#   Goal     = B + A
#
# Reverse entire array:  reverse(A+B) = B_rev + A_rev = [5,4] + [3,2,1]
# Reverse first k:       B_rev -> B  = [4,5] + [3,2,1]
# Reverse remaining n-k: A_rev -> A  = [4,5] + [1,2,3]
# Final = B + A. Exactly what we wanted!
#
# The key insight: reversing twice gives back the original, but by splitting
# the double-reversal at position k, we effectively "cut and paste" the two
# halves into the desired order.
# ============================================================================


def rotate_right_by_k(arr, k):
    """Rotate arr right by k positions in-place using the reversal algorithm."""
    n = len(arr)
    k = k % n                          # handle k > n

    if k == 0:                          # no rotation needed
        return

    # We reuse our reverse_array function from Section 5
    reverse_array(arr, 0, n - 1)        # Step 1: reverse entire array
    reverse_array(arr, 0, k - 1)        # Step 2: reverse first k elements
    reverse_array(arr, k, n - 1)        # Step 3: reverse remaining n-k


# Naive approach for comparison (DO NOT use for large inputs)
def rotate_right_by_k_naive(arr, k):
    """Rotate right by k using k single rotations. O(n*k) — slow!"""
    n = len(arr)
    k = k % n
    for _ in range(k):
        rotate_right_by_1(arr)


# Demonstration with detailed trace
print("\n--- Reversal Algorithm Step-by-Step ---")
arr = [1, 2, 3, 4, 5]
k = 2
n = len(arr)
k_eff = k % n

print(f"Original array: {arr}")
print(f"k = {k}, n = {n}, k % n = {k_eff}")

arr_demo = arr.copy()
print(f"\nStep 0 (original):        {arr_demo}")
reverse_array(arr_demo, 0, n - 1)
print(f"Step 1 (reverse all):     {arr_demo}")
reverse_array(arr_demo, 0, k_eff - 1)
print(f"Step 2 (reverse 0..{k_eff-1}):   {arr_demo}")
reverse_array(arr_demo, k_eff, n - 1)
print(f"Step 3 (reverse {k_eff}..{n-1}):   {arr_demo}")
print(f"Result:                   {arr_demo}")

# Verify with a different example
print("\n--- Another example: arr=[1,2,3,4,5,6,7], k=3 ---")
arr2 = [1, 2, 3, 4, 5, 6, 7]
print(f"Original: {arr2}")
rotate_right_by_k(arr2, 3)
print(f"Rotated:  {arr2}")

# Edge case: k > n
print("\n--- Edge case: k > n ---")
arr3 = [1, 2, 3, 4, 5]
print(f"Original: {arr3}, k=7")
print(f"k % n = 7 % 5 = {7 % 5}, so effectively rotating by 2")
rotate_right_by_k(arr3, 7)
print(f"Result:   {arr3}")


# ===== SECTION 8: Find Three Largest Elements ==============================
print("\n" + "=" * 70)
print("  SECTION 8: Find Three Largest Elements")
print("=" * 70)

# Problem: Find the three largest elements in a single pass.
#
# Algorithm:
#   Maintain three variables: first, second, third — all initialized to -inf.
#   For each number in the array:
#     if num > first:     it beats everything — cascade down
#     elif num > second:  it beats second and third — cascade
#     elif num > third:   it only beats third
#
# THE CONDITIONAL CASCADE (critical to understand):
#   When a new number is larger than first:
#     - old first becomes second (it's no longer #1, but it's still #2)
#     - old second becomes third
#     - new number becomes first
#   This cascade must happen in the right ORDER: third = second, THEN
#   second = first, THEN first = num. Otherwise you overwrite values
#   before saving them.
#
# Time : O(n) — single pass, constant work per element.
# Space: O(1) — only three variables.
#
# Compare with sorting approach:
#   Sort the array, take last 3. Time: O(n log n). This is worse!
#   Our single-pass approach is O(n), which is optimal since we must
#   look at every element at least once.


def three_largest(arr):
    """Return the three largest elements as (first, second, third)."""
    first = second = third = float("-inf")

    for num in arr:
        if num > first:
            # num is the new champion — cascade everything down
            third = second
            second = first
            first = num
        elif num > second:
            # num is second-best — push old second to third
            third = second
            second = num
        elif num > third:
            # num is third-best
            third = num

    return first, second, third


# Detailed trace
arr = [12, 35, 1, 10, 34, 1]
print(f"\nArray: {arr}")
print(f"Three largest: {three_largest(arr)}")

# Full trace walkthrough
print("\n--- Step-by-step trace ---")
print(f"{'num':>5}  {'first':>8}  {'second':>8}  {'third':>8}")
print("-" * 37)

f = s = t = float("-inf")
for num in arr:
    if num > f:
        t = s
        s = f
        f = num
    elif num > s:
        t = s
        s = num
    elif num > t:
        t = num
    print(f"{num:>5}  {f:>8}  {s:>8}  {t:>8}")

# Another example
print(f"\nArray: [3, 3, 3]")
print(f"Three largest: {three_largest([3, 3, 3])}")

print(f"\nArray: [7, 1, 9, 2, 8, 3]")
print(f"Three largest: {three_largest([7, 1, 9, 2, 8, 3])}")


# ===== SECTION 9: Two Sum Problem (Bonus — Classic Interview Question) =====
print("\n" + "=" * 70)
print("  SECTION 9: Two Sum Problem")
print("=" * 70)

# Problem: Given an array and a target sum, find TWO numbers in the array
#          that add up to the target. Return their indices.
#
# Example: arr = [2, 7, 11, 15], target = 9  ->  (0, 1) because 2+7=9


# --- Method 1: Brute Force ---
# Try every pair (i, j) where i < j.
# Time : O(n^2) — two nested loops.
# Space: O(1)

def two_sum_brute(arr, target):
    """Find two indices whose values sum to target. O(n^2)."""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return (i, j)
    return None                         # no pair found


# --- Method 2: Hash Map (Optimal) ---
# For each number, calculate its "complement" = target - num.
# Check if complement was already seen (stored in a dictionary).
# Time : O(n) — single pass, O(1) dictionary lookup.
# Space: O(n) — the dictionary can store up to n entries.

def two_sum_hashmap(arr, target):
    """Find two indices whose values sum to target. O(n)."""
    seen = {}                           # value -> index
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i                   # store current number and its index
    return None


# Walkthrough of hash map approach:
# arr = [2, 7, 11, 15], target = 9
#
#   i=0: num=2,  complement=9-2=7,  seen={}          -> 7 not in seen -> seen={2:0}
#   i=1: num=7,  complement=9-7=2,  seen={2:0}       -> 2 IS in seen! -> return (0,1)
#
# We found the answer in just 2 iterations!

arr = [2, 7, 11, 15]
target = 9
print(f"\nArray:  {arr}")
print(f"Target: {target}")
print(f"Brute force: {two_sum_brute(arr, target)}")
print(f"Hash map:    {two_sum_hashmap(arr, target)}")

# Trace the hash map approach
print("\n--- Hash map trace ---")
seen = {}
for i, num in enumerate(arr):
    complement = target - num
    status = f"complement={complement}"
    if complement in seen:
        status += f" FOUND at index {seen[complement]}"
    else:
        status += f" not in seen"
    seen[num] = i
    print(f"  i={i}: num={num}, {status}, seen={dict(list(seen.items()))}")

# Another example
arr2 = [3, 5, 1, 8, 4, 6]
target2 = 9
print(f"\nArray:  {arr2}, Target: {target2}")
print(f"Brute force: {two_sum_brute(arr2, target2)}")
print(f"Hash map:    {two_sum_hashmap(arr2, target2)}")


# ===== SECTION 10: Practice Exercises (5 Problems with Solutions) ===========
print("\n" + "=" * 70)
print("  SECTION 10: Practice Exercises")
print("=" * 70)


# ---------- Exercise 1: Move All Zeros to End ----------
# Move all 0s to the end of the array while maintaining the relative order
# of the non-zero elements. Do it in-place.
#
# Example: [0, 1, 0, 3, 12] -> [1, 3, 12, 0, 0]
#
# Approach (Two Pointer):
#   - Use a pointer 'write_pos' for where the next non-zero should go.
#   - Walk through the array. Every non-zero element gets placed at write_pos.
#   - After the loop, fill the remaining positions with zeros.
#
# Time : O(n)
# Space: O(1)

def move_zeros_to_end(arr):
    """Move all zeros to the end, preserving order of non-zeros. In-place."""
    write_pos = 0
    for num in arr:
        if num != 0:
            arr[write_pos] = num
            write_pos += 1
    # Fill remaining positions with zeros
    while write_pos < len(arr):
        arr[write_pos] = 0
        write_pos += 1


print("\n--- Exercise 1: Move Zeros to End ---")
arr = [0, 1, 0, 3, 12]
print(f"Before: {arr}")
move_zeros_to_end(arr)
print(f"After:  {arr}")

arr = [0, 0, 1]
print(f"Before: {arr}")
move_zeros_to_end(arr)
print(f"After:  {arr}")


# ---------- Exercise 2: Find Missing Number in 1..n ----------
# Given an array of n-1 distinct integers in the range [1, n], find the
# one number that is missing.
#
# Example: [1, 2, 4, 5] (n=5) -> missing = 3
#
# Approach: Sum of 1..n is n*(n+1)//2. Subtract the array sum.
#
# Time : O(n)
# Space: O(1)

def find_missing_number(arr, n):
    """Find missing number in range [1, n] given n-1 elements."""
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum


print("\n--- Exercise 2: Find Missing Number ---")
arr = [1, 2, 4, 5]
n = 5
print(f"Array: {arr}, n={n}")
print(f"Missing number: {find_missing_number(arr, n)}")

arr = [3, 7, 1, 2, 8, 4, 5]
n = 8
print(f"Array: {arr}, n={n}")
print(f"Missing number: {find_missing_number(arr, n)}")


# ---------- Exercise 3: Check if Array is Sorted ----------
# Return True if the array is sorted in non-decreasing order.
#
# Approach: Check every consecutive pair. If any arr[i] > arr[i+1], not sorted.
#
# Time : O(n)
# Space: O(1)

def is_sorted(arr):
    """Return True if arr is sorted in non-decreasing order."""
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


print("\n--- Exercise 3: Check if Array is Sorted ---")
print(f"[1, 2, 3, 4, 5] -> {is_sorted([1, 2, 3, 4, 5])}")
print(f"[1, 3, 2, 4, 5] -> {is_sorted([1, 3, 2, 4, 5])}")
print(f"[1, 1, 1, 1]    -> {is_sorted([1, 1, 1, 1])}")
print(f"[5]             -> {is_sorted([5])}")
print(f"[]              -> {is_sorted([])}")


# ---------- Exercise 4: Remove Duplicates from Sorted Array ----------
# Given a SORTED array, remove duplicates in-place and return the count of
# unique elements. The first 'count' elements of the array should hold the
# unique values.
#
# Example: [1, 1, 2, 2, 3] -> count=3, arr becomes [1, 2, 3, ...]
#
# Approach (Two Pointer):
#   - write_pos starts at 1 (first element is always unique).
#   - For each element from index 1 onward, if it differs from the previous
#     element, write it at write_pos and advance.
#
# Time : O(n)
# Space: O(1)

def remove_duplicates_sorted(arr):
    """Remove duplicates in-place from sorted array. Return unique count."""
    if not arr:
        return 0

    write_pos = 1
    for i in range(1, len(arr)):
        if arr[i] != arr[i - 1]:       # new unique element found
            arr[write_pos] = arr[i]
            write_pos += 1

    return write_pos


print("\n--- Exercise 4: Remove Duplicates from Sorted Array ---")
arr = [1, 1, 2, 2, 3, 3, 3, 4]
print(f"Before: {arr}")
count = remove_duplicates_sorted(arr)
print(f"Unique count: {count}")
print(f"After:  {arr[:count]}")

arr = [1, 1, 1, 1]
count = remove_duplicates_sorted(arr)
print(f"[1,1,1,1] -> count={count}, unique={arr[:count]}")


# ---------- Exercise 5: Maximum Difference Between Two Elements ----------
# Find the maximum value of arr[j] - arr[i] where j > i.
# In other words, find the best "buy low, sell high" pair where the buy
# comes before the sell.
#
# Example: [2, 3, 10, 6, 4, 8, 1] -> max diff = 10 - 2 = 8
#
# Approach:
#   - Track the minimum element seen so far (min_so_far).
#   - At each position, the best possible difference ending here is
#     arr[i] - min_so_far.
#   - Update the global maximum difference.
#
# Time : O(n)
# Space: O(1)

def max_difference(arr):
    """Find max arr[j] - arr[i] where j > i. Returns 0 if no positive diff."""
    if len(arr) < 2:
        return 0

    min_so_far = arr[0]
    max_diff = 0                       # or arr[1] - arr[0] to allow negatives

    for i in range(1, len(arr)):
        diff = arr[i] - min_so_far
        max_diff = max(max_diff, diff)
        min_so_far = min(min_so_far, arr[i])

    return max_diff


print("\n--- Exercise 5: Maximum Difference ---")
arr = [2, 3, 10, 6, 4, 8, 1]
print(f"Array: {arr}")
print(f"Max difference: {max_difference(arr)}")

# Trace
print("\n--- Trace ---")
min_sf = arr[0]
mx = 0
print(f"{'i':>3}  {'arr[i]':>6}  {'min_so_far':>10}  {'diff':>6}  {'max_diff':>8}")
print("-" * 42)
for i in range(1, len(arr)):
    diff = arr[i] - min_sf
    mx = max(mx, diff)
    print(f"{i:>3}  {arr[i]:>6}  {min_sf:>10}  {diff:>6}  {mx:>8}")
    min_sf = min(min_sf, arr[i])

arr2 = [7, 9, 5, 6, 3, 2]
print(f"\nArray: {arr2}")
print(f"Max difference: {max_difference(arr2)}")


# ===== SECTION 10.5: Insert Into a Sorted Array (Keeping It Sorted) ========
print("\n" + "=" * 70)
print("  SECTION 10.5: Insert Into a Sorted Array")
print("=" * 70)

# ----- Problem -----
# You're given a SORTED array with one extra empty slot at the end
# (marked with a placeholder, usually 0), and a value x to insert.
# Insert x into its correct position so the array STAYS sorted.
#
# Example: arr = [1, 4, 7, 8, 9, 0],  x = 6
#          The trailing 0 is just "empty space" reserved for the new element.
#          Expected result: [1, 4, 6, 7, 8, 9]
#
# This shows up in interviews as a precursor to "merge two sorted arrays"
# (LeetCode 88) — that problem is just this one applied repeatedly.

# ----- Approach 1: Shift from the back -----
#
# Idea: start from the second-to-last slot (the last real element) and
# shift elements RIGHT one at a time until we find x's correct spot.
# This avoids overwriting data — we always shift before we write.
#
# Walkthrough: arr = [3, 5, 10, 14, 0], x = 7
#   i = 3 (arr[3]=14): 7 < 14  → shift: arr = [3, 5, 10, 14, 14], i = 2
#   i = 2 (arr[2]=10): 7 < 10  → shift: arr = [3, 5, 10, 10, 14], i = 1
#   i = 1 (arr[1]=5):  7 >= 5  → stop, place x at i+1 = 2
#   Result: [3, 5, 7, 10, 14]

def insert_sorted(arr, x):
    """Insert x into a sorted array (last slot is the empty placeholder)."""
    if x <= 0:
        return False
    if arr[-1] != 0:          # no empty slot available
        return False

    i = len(arr) - 2          # start at the last REAL element (skip the empty slot)
    while i >= 0 and x < arr[i]:
        arr[i + 1] = arr[i]   # shift this element one position right
        i -= 1
    arr[i + 1] = x            # place x in the gap we just made
    return True

# Time:  O(n) — worst case, x is the smallest and shifts everything
# Space: O(1) — modifies the array in place, no extra storage

print("\n--- Approach 1: Shift from the back ---")
arr1 = [3, 5, 10, 14, 0]
x1 = 7
print(f"Before: {arr1}, inserting {x1}")
insert_sorted(arr1, x1)
print(f"After:  {arr1}")

# ----- Approach 2: Swap while moving forward -----
#
# Idea: walk LEFT to RIGHT. The moment we find a slot that should hold
# a SMALLER value than what's currently there (or we hit the empty 0),
# swap x into that slot and carry the displaced value forward as the
# new x. Keep going until x lands in the empty slot at the end.
#
# Walkthrough: arr = [3, 5, 10, 14, 0], x = 1
#   i=0: arr[0]=3, x=1 < 3        → swap: arr=[1, 5, 10, 14, 0], x becomes 3
#   i=1: arr[1]=5, x=3 < 5        → swap: arr=[1, 3, 10, 14, 0], x becomes 5
#   i=2: arr[2]=10, x=5 < 10      → swap: arr=[1, 3, 5, 14, 0], x becomes 10
#   i=3: arr[3]=14, x=10 < 14     → swap: arr=[1, 3, 5, 10, 0], x becomes 14
#   i=4: arr[4]=0,  x=14, arr[i]==0 → swap: arr=[1, 3, 5, 10, 14]
#   Result: [1, 3, 5, 10, 14]

def insert_sorted_swap(arr, x):
    """Insert x by repeatedly swapping it forward until it reaches the empty slot."""
    if x <= 0:
        return False
    if arr[-1] != 0:
        return False

    for i in range(len(arr)):
        if x < arr[i] or arr[i] == 0:
            arr[i], x = x, arr[i]   # swap: place x here, carry old value forward
    return True

# Time:  O(n) — single forward pass
# Space: O(1)

print("\n--- Approach 2: Swap while moving forward ---")
arr2 = [3, 5, 10, 14, 0]
x2 = 1
print(f"Before: {arr2}, inserting {x2}")
insert_sorted_swap(arr2, x2)
print(f"After:  {arr2}")

# ----- Comparing the two approaches -----
# Both are O(n) time, O(1) space. The difference is DIRECTION:
#   Approach 1 (shift): scans from the END, only touches elements
#     that need to move — slightly fewer writes if x is large.
#   Approach 2 (swap):  scans from the START, always does exactly
#     n swaps — simpler to reason about, same cost regardless of x.
#
# Both return False if x <= 0 or the array has no empty slot (arr[-1] != 0) —
# always validate inputs before mutating in DSA interview code.

print()


# ===== SECTION 11: Interview Quick Reference — Common Array Patterns =======
print("\n" + "=" * 70)
print("  SECTION 11: Interview Quick Reference")
print("=" * 70)

print("""
+----------------------------+------------------+------------------+
|  Problem Pattern           |  Technique       |  Time / Space    |
+----------------------------+------------------+------------------+
|  Find element              |  Linear scan     |  O(n) / O(1)    |
|  Find element (sorted)     |  Binary search   |  O(log n) / O(1)|
|  Two Sum                   |  Hash map        |  O(n) / O(n)    |
|  Reverse array             |  Two pointers    |  O(n) / O(1)    |
|  Rotate by k               |  3 reverses      |  O(n) / O(1)    |
|  Remove duplicates (sorted)|  Two pointers    |  O(n) / O(1)    |
|  Max subarray sum          |  Kadane's algo   |  O(n) / O(1)    |
|  k-th largest              |  Track top-k     |  O(n) / O(1)    |
|  Subarray sum = target     |  Prefix sum      |  O(n) / O(n)    |
|  Sliding window max        |  Deque           |  O(n) / O(k)    |
|  Merge sorted arrays       |  Two pointers    |  O(n+m) / O(n+m)|
|  Dutch National Flag       |  Three pointers  |  O(n) / O(1)    |
+----------------------------+------------------+------------------+

KEY TAKEAWAYS:
  1. If the array is SORTED, think binary search or two pointers.
  2. If you need O(1) space, think two pointers or in-place swaps.
  3. If you can trade space for time, think hash maps.
  4. Reverse is a building block — rotation, palindrome checks, etc.
  5. Always ask: "Can I do this in a single pass?" Often, yes.
""")

print("=" * 70)
print("  END OF FILE 09 — Array Problems Tutorial")
print("=" * 70)
