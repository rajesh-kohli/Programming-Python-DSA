###############################################################################
#               08 - Core Array & Hashing Problems                            #
###############################################################################
#
# SOURCES:
#   Coding_Python/1. Python - Intro/08_array_problems.py (1001 lines)
#   LPLV26MAY/L10 - Intro to Arrays/
#   LPLV26MAY/L12 - Intro to Arrays/
#   LPLV26MAY/L13 - Intro to Arrays/
#   LPLV26MAY/L15 - Maps/
#
# PATTERNS IN THIS MODULE:
#   1.  Two Pointers (reverse, rotate, target pair, move zeros, remove dup)
#   2.  Hash Map / Set (two sum, contains dup, consecutive sequence)
#   3.  In-Place Index Mapping (find duplicate)
#   4.  Prefix Sum (range queries, max subarray sum via prefix)
#   5.  Single-Pass Tracking (three largest, max difference, missing number)
#   6.  Prefix × Suffix Running Products (product except self)

from typing import List, Optional
from collections import defaultdict, Counter


# =============================================================================
# SECTION 1: Reverse Array
# =============================================================================
#
# PROBLEM: Reverse arr[] in-place without creating a new array.
#
# Two Pointers — i at start, j at end, converge toward the middle:
#
#   [10, 20, 30, 40, 50]
#     i               j   → swap(10,50)
#   [50, 20, 30, 40, 10]
#         i       j       → swap(20,40)
#   [50, 40, 30, 20, 10]
#             ij          → i >= j, STOP (middle stays in place)
#
# NOTE: This helper function is reused by the rotation algorithm below.

def reverse_segment(arr: List[int], lo: int, hi: int) -> None:
    """
    Reverse arr[lo..hi] in-place using two pointers.
    Time: O(hi - lo) ≈ O(n) | Space: O(1)
    """
    while lo < hi:
        arr[lo], arr[hi] = arr[hi], arr[lo]
        lo += 1
        hi -= 1

def reverse_array_brute(arr: List[int]) -> List[int]:
    """
    Brute: O(n) Time, O(n) Space.
    Create a new array and fill it backwards.
    """
    n = len(arr)
    result = [0] * n
    for i in range(n):
        result[n - 1 - i] = arr[i]
    return result

def reverse_array_optimal(arr: List[int]) -> None:
    """
    Optimal: O(n) Time, O(1) Space.
    Two-pointer in-place swap — n/2 swaps total.
    From L10/004reverseArray.py (identical logic).
    """
    reverse_segment(arr, 0, len(arr) - 1)

def reverse_demo():
    print("=" * 60)
    print("SECTION 1: Reverse Array")
    print("=" * 60)

    arr = [10, 20, 30, 40, 50]
    print(f"\n  Original:         {arr}")

    # Step-by-step trace
    demo = arr[:]
    i, j = 0, len(demo) - 1
    step = 0
    while i < j:
        print(f"  Step {step}: swap arr[{i}]={demo[i]} ↔ arr[{j}]={demo[j]}", end="")
        demo[i], demo[j] = demo[j], demo[i]
        i += 1; j -= 1
        print(f"  → {demo}")
        step += 1
    print(f"  Reversed:         {demo}")

    # Brute (new array)
    brute = reverse_array_brute([10, 20, 30, 40, 50])
    print(f"\n  Brute (new arr):  {brute}  [O(n) space]")

    # Optimal (in-place)
    opt = [10, 20, 30, 40, 50]
    reverse_array_optimal(opt)
    print(f"  Optimal (in-place):{opt}  [O(1) space]")

    # Comparison with built-ins
    print(f"  arr[::-1]         — creates new list, O(n) space")
    print(f"  arr.reverse()     — in-place, same two-pointer idea under the hood")


# =============================================================================
# SECTION 2: Rotate Array by 1 and by K
# =============================================================================
#
# PROBLEM: Rotate arr right by K positions. Last element wraps to the front.
# Example: [1, 2, 3, 4, 5], k=2  →  [4, 5, 1, 2, 3]
#
# --- ROTATE BY 1 ---
# Save last element (temp), shift everything right, place temp at front.
# Walkthrough for [1, 2, 3, 4, 5]:
#   temp = 5
#   i=4: arr[4] = arr[3] = 4  → [1, 2, 3, 4, 4]
#   i=3: arr[3] = arr[2] = 3  → [1, 2, 3, 3, 4]
#   i=2: arr[2] = arr[1] = 2  → [1, 2, 2, 3, 4]
#   i=1: arr[1] = arr[0] = 1  → [1, 1, 2, 3, 4]
#   arr[0] = temp = 5         → [5, 1, 2, 3, 4]
#
# --- ROTATE BY K: BRUTE O(n·k) ---
# Call rotate_by_1 k times. O(n) per call × k calls = O(n·k). TLE for large k.
#
# --- ROTATE BY K: OPTIMAL — 3-REVERSAL ALGORITHM O(n), O(1) ---
# Think of array as two parts: A = [1,2,3] (first n-k), B = [4,5] (last k)
# Goal: B + A
#
# Mathematical proof:
#   rev(A+B)      = B_rev + A_rev  → [5,4,3,2,1]
#   rev(B_rev)    = B               → [4,5,3,2,1]
#   rev(A_rev)    = A               → [4,5,1,2,3] ✓
#
# Step 1: reverse(0, n-1)   [5, 4, 3, 2, 1]
# Step 2: reverse(0, k-1)   [4, 5, 3, 2, 1]   ← un-reverse B
# Step 3: reverse(k, n-1)   [4, 5, 1, 2, 3]   ← un-reverse A

def rotate_by_1(arr: List[int]) -> None:
    """
    Rotate arr right by 1 in-place.
    Time: O(n) | Space: O(1)
    """
    n = len(arr)
    if n <= 1:
        return
    temp = arr[-1]                     # save last element
    for i in range(n - 1, 0, -1):
        arr[i] = arr[i - 1]            # shift right
    arr[0] = temp                      # place saved element at front

def rotate_brute(arr: List[int], k: int) -> None:
    """
    Brute: rotate right by k using k single rotations.
    Time: O(n·k) — TLE for large k | Space: O(1)
    """
    n = len(arr)
    if n == 0: return
    k = k % n
    for _ in range(k):
        rotate_by_1(arr)

def rotate_optimal(arr: List[int], k: int) -> None:
    """
    Optimal 3-Reversal Algorithm.
    Time: O(n) | Space: O(1)
    From L10/007kRotate2.py — identical logic wrapped in helper.

    Step 1: reverse entire array
    Step 2: reverse first k elements  (un-reverses B)
    Step 3: reverse remaining n-k     (un-reverses A)
    """
    n = len(arr)
    if n == 0: return
    k = k % n                          # handle k > n
    if k == 0: return
    reverse_segment(arr, 0, n - 1)     # Step 1
    reverse_segment(arr, 0, k - 1)     # Step 2
    reverse_segment(arr, k, n - 1)     # Step 3

def rotation_demo():
    print("\n" + "=" * 60)
    print("SECTION 2: Array Rotation")
    print("=" * 60)

    # Rotate by 1
    arr1 = [1, 2, 3, 4, 5]
    print(f"\n  Original (rotate by 1): {arr1}")
    rotate_by_1(arr1)
    print(f"  After rotate_by_1:      {arr1}")

    # 3-Reversal step trace
    arr = [1, 2, 3, 4, 5]
    k = 2
    n = len(arr)
    k_eff = k % n
    print(f"\n  3-Reversal trace for {arr}, k={k}:")
    demo = arr[:]
    print(f"  Step 0 (original):          {demo}")
    reverse_segment(demo, 0, n - 1)
    print(f"  Step 1 (reverse all):       {demo}")
    reverse_segment(demo, 0, k_eff - 1)
    print(f"  Step 2 (reverse 0..{k_eff-1}):     {demo}")
    reverse_segment(demo, k_eff, n - 1)
    print(f"  Step 3 (reverse {k_eff}..{n-1}):    {demo}  ✓")

    # Verify brute == optimal
    arr_b = [1, 2, 3, 4, 5]; rotate_brute(arr_b, 2)
    arr_o = [1, 2, 3, 4, 5]; rotate_optimal(arr_o, 2)
    print(f"\n  Brute:   {arr_b}")
    print(f"  Optimal: {arr_o}  (same result)")

    # Edge cases
    tests = [
        ([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]),
        ([1, 2, 3, 4, 5],        7, [4, 5, 1, 2, 3]),        # k > n
        ([1],                     0, [1]),                     # single element
    ]
    print("\n  Edge case verification:")
    for arr_in, k_in, expected in tests:
        result = arr_in[:]
        rotate_optimal(result, k_in)
        status = "✓" if result == expected else "✗"
        print(f"    {arr_in}, k={k_in} → {result}  {status}")


# =============================================================================
# SECTION 3: Linear Search — First, Last, and All Occurrences
# =============================================================================
#
# All variants are O(n) Time, O(1) Space (O(k) for all-occurrences result list).
#
# Key trick for LAST occurrence: iterate BACKWARDS with range(n-1, -1, -1).
#   range(n-1, -1, -1) → n-1, n-2, ..., 1, 0  (all valid indices)
#   The FIRST match while going backwards IS the last occurrence.
#
# for-else pattern: else block runs ONLY if the loop completes without break.

def first_occurrence(arr: List[int], target: int) -> int:
    """Return index of first occurrence; -1 if not found. O(n)"""
    for i, num in enumerate(arr):
        if num == target:
            return i     # early return — stop at first match
    return -1

def last_occurrence(arr: List[int], target: int) -> int:
    """Return index of last occurrence; -1 if not found. O(n)"""
    n = len(arr)
    for i in range(n - 1, -1, -1):    # walk backwards
        if arr[i] == target:
            return i                   # first match going backwards = last occ
    return -1

def all_occurrences(arr: List[int], target: int) -> List[int]:
    """Return list of all indices where arr[i] == target; [-1] if none. O(n)"""
    result = [i for i, num in enumerate(arr) if num == target]
    return result if result else [-1]

def linear_search_demo():
    print("\n" + "=" * 60)
    print("SECTION 3: Linear Search")
    print("=" * 60)
    arr = [10, 20, 30, 20, 40, 20]
    print(f"\n  arr = {arr}")
    print(f"  first_occurrence(20)   = {first_occurrence(arr, 20)}")
    print(f"  last_occurrence(20)    = {last_occurrence(arr, 20)}")
    print(f"  all_occurrences(20)    = {all_occurrences(arr, 20)}")
    print(f"  first_occurrence(99)   = {first_occurrence(arr, 99)}")
    print(f"  all_occurrences(99)    = {all_occurrences(arr, 99)}")

    # Trace backwards walk
    print(f"\n  Trace for last_occurrence(20):")
    n = len(arr)
    for i in range(n - 1, -1, -1):
        if arr[i] == 20:
            print(f"    i={i}: arr[{i}]={arr[i]} == 20 → return {i} ✓")
            break
        print(f"    i={i}: arr[{i}]={arr[i]} ≠ 20, continue")


# =============================================================================
# SECTION 4: Find Three Largest Elements — Cascade Pattern
# =============================================================================
#
# PROBLEM: Find the three largest distinct-value elements in a single pass.
# Time: O(n) | Space: O(1)
#
# Algorithm: maintain first, second, third (all float('-inf')).
# For each num:
#   if num > first:   third=second, second=first, first=num  (full cascade)
#   elif num > second: third=second, second=num               (mid cascade)
#   elif num > third:  third=num                              (tip)
#
# CRITICAL ORDER: set third = second BEFORE second = first (or values are lost).
#
# Step trace for [12, 35, 1, 10, 34, 1]:
#   num=12: 12>-inf  → first=12,  second=-inf, third=-inf
#   num=35: 35>12    → first=35,  second=12,   third=-inf
#   num=1:  1<12     → no change
#   num=10: 10>-inf  → third=10
#   num=34: 34>12    → third=12, second=34,  BUT wait: 34>second(12): third=12, second=34
#   num=1:  1<12     → no change
#   Result: (35, 34, 12) ✓

def three_largest(arr: List[int]):
    """
    Return (first, second, third) largest elements.
    Time: O(n) | Space: O(1)
    From L10/009threeLargest.py — same cascade logic, wrapped in function.
    """
    first = second = third = float('-inf')
    for num in arr:
        if num > first:
            third = second     # critical: cascade DOWN before overwriting
            second = first
            first = num
        elif num > second:
            third = second
            second = num
        elif num > third:
            third = num
    return first, second, third

def three_largest_demo():
    print("\n" + "=" * 60)
    print("SECTION 4: Three Largest Elements")
    print("=" * 60)

    arr = [12, 35, 1, 10, 34, 1]
    print(f"\n  arr = {arr}")

    # Live trace table
    f = s = t = float('-inf')
    print(f"\n  {'num':>5}  {'first':>8}  {'second':>8}  {'third':>8}")
    print("  " + "-" * 37)
    for num in arr:
        if num > f:
            t = s; s = f; f = num
        elif num > s:
            t = s; s = num
        elif num > t:
            t = num
        first_str  = str(f)  if f  != float('-inf') else '-inf'
        second_str = str(s)  if s  != float('-inf') else '-inf'
        third_str  = str(t)  if t  != float('-inf') else '-inf'
        print(f"  {num:>5}  {first_str:>8}  {second_str:>8}  {third_str:>8}")

    print(f"\n  three_largest({arr}) = {three_largest(arr)}")
    print(f"  three_largest([7,1,9,2,8,3]) = {three_largest([7,1,9,2,8,3])}")
    print(f"  three_largest([3,3,3])       = {three_largest([3,3,3])}")


# =============================================================================
# SECTION 5: Two Sum — Hash Map Pattern
# =============================================================================
#
# PROBLEM: Given arr and target, return [i, j] such that arr[i]+arr[j]==target.
#
# BRUTE O(n²): try every pair (i,j). Too slow for n > 10^4.
# OPTIMAL O(n): for each num, look up (target - num) in a hash map of seen values.
#
# Mental model — "seen" is a guest list:
#   Each new element asks "Is my complement (target - me) already here?"
#   If YES: pair found. If NO: add self to the list for future elements to find.
#
# Walkthrough for [2, 7, 11, 15], target=9:
#   i=0: num=2,  complement=7,   seen={}      → 7 not in seen → seen={2:0}
#   i=1: num=7,  complement=2,   seen={2:0}   → 2 IS in seen! → return [0,1] ✓

def two_sum_brute(arr: List[int], target: int) -> List[int]:
    """Brute: O(n²) Time, O(1) Space."""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return [i, j]
    return []

def two_sum_optimal(arr: List[int], target: int) -> List[int]:
    """
    Optimal: O(n) Time, O(n) Space.
    Hash map: {value: index} for O(1) complement lookup.
    """
    seen: dict = {}                   # value → index
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

def two_sum_demo():
    print("\n" + "=" * 60)
    print("SECTION 5: Two Sum")
    print("=" * 60)

    arr = [2, 7, 11, 15]
    target = 9
    print(f"\n  arr={arr}, target={target}")
    print(f"  Brute:   {two_sum_brute(arr, target)}")
    print(f"  Optimal: {two_sum_optimal(arr, target)}")

    # Hash map trace
    print(f"\n  Hash map trace:")
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            print(f"    i={i}: num={num}, complement={complement}  → FOUND at idx {seen[complement]}! return [{seen[complement]},{i}]")
            break
        seen[num] = i
        print(f"    i={i}: num={num}, complement={complement}  → not in seen → seen={seen}")

    # Multiple tests
    tests = [
        ([3, 5, 1, 8, 4, 6], 9, [1, 5]),
        ([1, 2, 3, 4, 5],    9, [3, 4]),
        ([1],                2, []),     # no pair
    ]
    print(f"\n  Verification:")
    for a, t, expected in tests:
        result = two_sum_optimal(a, t)
        status = "✓" if result == expected else "✗"
        print(f"    {a}, target={t} → {result}  {status}")


# =============================================================================
# SECTION 6: Contains Duplicate — Hash Set
# =============================================================================
#
# PROBLEM: Return True if any value appears more than once.
#
# BRUTE O(n²): nested loops — compare every pair.
# SORT  O(n log n): sort then compare adjacent pairs.
# OPTIMAL O(n): hash set — O(1) average membership check.
#
# Mental model: set is a "visitor book". If you try to sign in but your
# name's already there → duplicate found.

def contains_duplicate_brute(nums: List[int]) -> bool:
    """Brute: O(n²) Time, O(1) Space."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True
    return False

def contains_duplicate_sort(nums: List[int]) -> bool:
    """Sort: O(n log n) Time, O(1) or O(n) Space (depends on sort impl)."""
    nums_copy = sorted(nums)           # avoid mutating input
    for i in range(1, len(nums_copy)):
        if nums_copy[i] == nums_copy[i - 1]:
            return True
    return False

def contains_duplicate_optimal(nums: List[int]) -> bool:
    """
    Optimal: O(n) Time, O(n) Space.
    First duplicate found → return immediately (early exit).
    """
    seen: set = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

def contains_duplicate_demo():
    print("\n" + "=" * 60)
    print("SECTION 6: Contains Duplicate")
    print("=" * 60)
    tests = [([1, 2, 3, 1], True), ([1, 2, 3, 4], False), ([1, 1, 1, 3, 3], True)]
    print(f"\n  {'Input':<25} {'Brute':>7}  {'Sort':>7}  {'Set':>7}  {'Expected':>9}")
    print("  " + "-" * 60)
    for nums, expected in tests:
        b = contains_duplicate_brute(nums[:])
        s = contains_duplicate_sort(nums[:])
        o = contains_duplicate_optimal(nums[:])
        ok = "✓" if o == expected else "✗"
        print(f"  {str(nums):<25} {str(b):>7}  {str(s):>7}  {str(o):>7}  {str(expected):>9} {ok}")


# =============================================================================
# SECTION 7: Find Duplicate Number — In-Place Index Mapping
# =============================================================================
#
# PROBLEM: Array of n+1 integers, values in [1..n]. Exactly ONE duplicate.
# Constraints: O(1) extra space, do not modify array... (LeetCode 287 relaxes this)
#
# INTERMEDIATE O(n)/O(n): hash set — first repeated element is the duplicate.
# OPTIMAL O(n)/O(1): index mapping (modifies array).
#
# Index Mapping algorithm (from L15/001findDuplicateNumber.py):
#   In a duplicate-free [1..n] array, value x should live at index x.
#   Use nums[0] as a buffer slot. Keep swapping nums[0] to its correct index.
#   When nums[x] == x already (the "home" is occupied by an equal value) → duplicate.
#
# Full trace for nums = [2, 3, 1, 3]:
#   x = nums[0] = 2;  nums[2]=1 ≠ 2 → swap(nums[0], nums[2]) → [1, 3, 2, 3]
#   x = nums[0] = 1;  nums[1]=3 ≠ 1 → swap(nums[0], nums[1]) → [3, 1, 2, 3]
#   x = nums[0] = 3;  nums[3]=3 == 3 → DUPLICATE = 3 ✓
#
# Why it terminates: each swap correctly places at least one element.
# The duplicate can never be "correctly placed" (its slot is already taken).
#
# Find Duplicate II (from L15/002findDuplicateNumberII.py — multiple duplicates):
#   Use modular encoding: nums[x] += n for each element x = nums[i] % n.
#   Elements with count > 1 will have nums[i] // n > 1 after the pass.

def find_duplicate_set(nums: List[int]) -> int:
    """
    Intermediate: O(n) Time, O(n) Space.
    First repeated value encountered.
    """
    seen: set = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
    return -1

def find_duplicate_optimal(nums: List[int]) -> int:
    """
    Optimal: O(n) Time, O(1) Space (modifies input array).
    From L15/001findDuplicateNumber.py — index mapping with nums[0] as buffer.
    """
    while True:
        x = nums[0]
        if nums[x] == x:
            return x                   # home slot occupied by equal value → duplicate
        nums[0], nums[x] = nums[x], nums[0]    # swap x to its correct position

def find_duplicate_demo():
    print("\n" + "=" * 60)
    print("SECTION 7: Find Duplicate Number (Index Mapping)")
    print("=" * 60)

    # Full trace
    nums_trace = [2, 3, 1, 3]
    print(f"\n  Trace for {nums_trace}:")
    arr = nums_trace[:]
    step = 0
    while True:
        x = arr[0]
        print(f"    Step {step}: x=arr[0]={x},  arr[{x}]={arr[x]}", end="")
        if arr[x] == x:
            print(f"  → arr[{x}]==x → DUPLICATE = {x} ✓")
            break
        arr[0], arr[x] = arr[x], arr[0]
        print(f"  → swap(arr[0],arr[{x}]) → {arr}")
        step += 1

    tests = [
        ([1, 3, 4, 2, 2], 2),
        ([3, 1, 3, 4, 2], 3),
        ([2, 3, 1, 3],    3),
    ]
    print(f"\n  Verification:")
    for nums, expected in tests:
        result_set = find_duplicate_set(nums[:])
        result_opt = find_duplicate_optimal(nums[:])
        ok = "✓" if result_opt == expected else "✗"
        print(f"    {nums} → set={result_set}, index-map={result_opt}  {ok}")


# =============================================================================
# SECTION 8: Longest Consecutive Sequence — Set + Start Detection
# =============================================================================
#
# PROBLEM: Given unsorted array, find length of longest consecutive sequence.
# Example: [100, 4, 200, 1, 3, 2] → 4  (sequence 1→2→3→4)
#
# BRUTE O(n²): for each num, scan for next consecutive value.
# SORT  O(n log n): sort then walk and count streaks.
# OPTIMAL O(n): put all elements in a set; only start counting from values
#               where num-1 is NOT in the set (guaranteed sequence starts).
#               Then walk forward through set.
#
# Each element is added to the set once (O(n)) and walked at most once
# across all starting-point loops → O(n) amortized.

def longest_consecutive_sort(nums: List[int]) -> int:
    """Sort: O(n log n) Time, O(1) or O(n) Space."""
    if not nums: return 0
    nums_copy = sorted(set(nums))       # deduplicate + sort
    best = cur = 1
    for i in range(1, len(nums_copy)):
        if nums_copy[i] == nums_copy[i - 1] + 1:
            cur += 1
        else:
            best = max(best, cur)
            cur = 1
    return max(best, cur)

def longest_consecutive_optimal(nums: List[int]) -> int:
    """
    Optimal: O(n) Time, O(n) Space.
    Set + sequence-start detection.
    """
    num_set = set(nums)
    best = 0
    for num in num_set:
        if (num - 1) not in num_set:    # num is a sequence start
            length = 1
            while (num + length) in num_set:
                length += 1
            best = max(best, length)
    return best

def consecutive_demo():
    print("\n" + "=" * 60)
    print("SECTION 8: Longest Consecutive Sequence")
    print("=" * 60)

    tests = [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([], 0),
        ([1], 1),
    ]
    print(f"\n  {'Input':<45} {'Sort':>5}  {'Set':>5}  {'Exp':>5}")
    print("  " + "-" * 62)
    for nums, expected in tests:
        s = longest_consecutive_sort(nums[:])
        o = longest_consecutive_optimal(nums[:])
        ok = "✓" if o == expected else "✗"
        print(f"  {str(nums):<45} {s:>5}  {o:>5}  {expected:>5} {ok}")


# =============================================================================
# SECTION 9: Product of Array Except Self — Prefix × Suffix
# =============================================================================
#
# PROBLEM: Return ans[] where ans[i] = product of every element EXCEPT nums[i].
# Constraints: No division. O(n) Time. Follow-up: O(1) extra space.
#
# --- APPROACH 1: DIVISION (often disallowed) ---
# Total product ÷ nums[i]. Breaks on zeros (ZeroDivisionError).
# Handle: count zeros, special-case one zero and multiple zeros.
# Time: O(n), Space: O(1)
#
# --- APPROACH 2: EXPLICIT PREFIX + SUFFIX ARRAYS O(n) space ---
# prefix[i] = nums[0]*nums[1]*...*nums[i-1]
# suffix[i] = nums[i+1]*...*nums[n-1]
# ans[i] = prefix[i] * suffix[i]
# Time: O(n), Space: O(n) extra
#
# --- APPROACH 3: RUNNING PREFIX×SUFFIX (OPTIMAL) O(1) extra space ---
# PASS 1 (left→right): build prefix running product INTO ans[].
#   ans[i] = product of all elements BEFORE i (prefix product up to i-1).
#
# PASS 2 (right→left): multiply each ans[i] by the running suffix product.
#   suffix = product of all elements AFTER i.
#
# Detailed column trace for [1, 2, 3, 4]:
#   After Pass 1 (prefix):
#     i=0: ans[0]=1         (no elements before 0)   prefix=1*1=1
#     i=1: ans[1]=1         (only nums[0]=1)          prefix=1*2=2
#     i=2: ans[2]=2         (nums[0]*nums[1]=1*2)     prefix=2*3=6
#     i=3: ans[3]=6         (nums[0]*1*2*3=6)         prefix=6*4=24
#     ans = [1, 1, 2, 6]
#
#   After Pass 2 (suffix × ans):
#     suffix=1
#     i=3: ans[3]=6*1=6,    suffix=1*4=4
#     i=2: ans[2]=2*4=8,    suffix=4*3=12
#     i=1: ans[1]=1*12=12,  suffix=12*2=24
#     i=0: ans[0]=1*24=24,  suffix=24*1=24
#     ans = [24, 12, 8, 6]
#
# Verify: 2*3*4=24 ✓  1*3*4=12 ✓  1*2*4=8 ✓  1*2*3=6 ✓

def product_except_self_division(nums: List[int]) -> List[int]:
    """
    Division approach: O(n) Time, O(1) Space.
    Handle zeros explicitly. Often banned by interviewers.
    """
    total_product = 1
    zero_count = 0
    for num in nums:
        if num == 0:
            zero_count += 1
        else:
            total_product *= num

    ans = [0] * len(nums)
    if zero_count > 1:
        return ans                     # two+ zeros: all products are 0
    for i, num in enumerate(nums):
        if zero_count == 1:
            ans[i] = total_product if num == 0 else 0
        else:
            ans[i] = total_product // num
    return ans

def product_except_self_explicit(nums: List[int]) -> List[int]:
    """
    Explicit prefix + suffix arrays: O(n) Time, O(n) Space (extra).
    Educational — shows the concept clearly before the optimised form.
    """
    n = len(nums)
    prefix = [1] * n
    suffix = [1] * n
    for i in range(1, n):
        prefix[i] = prefix[i - 1] * nums[i - 1]
    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i + 1] * nums[i + 1]
    return [prefix[i] * suffix[i] for i in range(n)]

def product_except_self_optimal(nums: List[int]) -> List[int]:
    """
    Optimal running prefix × suffix: O(n) Time, O(1) extra Space.
    Two passes — output array is not counted as extra space.
    Pass 1: fill ans[i] with prefix product (product of everything left of i).
    Pass 2: multiply ans[i] by running suffix product (everything right of i).
    """
    n = len(nums)
    ans = [1] * n

    # Pass 1: prefix products into ans
    prefix = 1
    for i in range(n):
        ans[i] = prefix
        prefix *= nums[i]

    # Pass 2: multiply by suffix products running right-to-left
    suffix = 1
    for i in range(n - 1, -1, -1):
        ans[i] *= suffix
        suffix *= nums[i]

    return ans

def product_demo():
    print("\n" + "=" * 60)
    print("SECTION 9: Product of Array Except Self")
    print("=" * 60)

    nums = [1, 2, 3, 4]
    print(f"\n  nums = {nums}")

    # Column trace
    n = len(nums)
    ans = [1] * n
    prefix = 1
    print("\n  Pass 1 — left→right (prefix into ans):")
    print(f"  {'i':>3}  {'nums[i]':>7}  {'ans[i]=prefix':>14}  {'prefix after':>12}")
    print("  " + "-" * 42)
    for i in range(n):
        ans[i] = prefix
        print(f"  {i:>3}  {nums[i]:>7}  {ans[i]:>14}  {prefix * nums[i]:>12}")
        prefix *= nums[i]
    print(f"  ans after Pass 1 = {ans}")

    suffix = 1
    print("\n  Pass 2 — right→left (multiply suffix into ans):")
    print(f"  {'i':>3}  {'nums[i]':>7}  {'suffix':>8}  {'ans[i] after':>12}")
    print("  " + "-" * 38)
    for i in range(n - 1, -1, -1):
        ans[i] *= suffix
        print(f"  {i:>3}  {nums[i]:>7}  {suffix:>8}  {ans[i]:>12}")
        suffix *= nums[i]
    print(f"  Final ans = {ans}  ✓  (expected [24,12,8,6])")

    tests = [
        ([1, 2, 3, 4],  [24, 12, 8, 6]),
        ([2, 3, 4, 5],  [60, 40, 30, 24]),
        ([1, 0, 3, 4],  [0, 12, 0, 0]),
        ([0, 0, 3, 4],  [0,  0, 0, 0]),
    ]
    print(f"\n  Approach comparison (division | explicit | optimal):")
    for n_in, expected in tests:
        d = product_except_self_division(n_in[:])
        e = product_except_self_explicit(n_in[:])
        o = product_except_self_optimal(n_in[:])
        ok = "✓" if o == expected else "✗"
        print(f"    {n_in} → div={d} | exp={e} | opt={o} {ok}")


# =============================================================================
# SECTION 10: Prefix Sum — Range Queries
# =============================================================================
#
# PROBLEM: Given arr, answer multiple range sum queries [l..r] in O(1) each.
#
# Build: pSum[0] = arr[0]; pSum[i] = pSum[i-1] + arr[i]   → O(n)
# Query: sum(arr[l..r]) = pSum[r] - pSum[l-1]              → O(1)
#        (Special case l=0: sum = pSum[r], since there's no pSum[-1])
#
# From L12/007prefixSum.py:
#   pSum = [None] * n
#   pSum[0] = arr[0]
#   for i in range(1, n): pSum[i] = pSum[i-1] + arr[i]
#
# Prefix sum also underpins the naive O(n²) max subarray (using pSum to
# evaluate any subarray sum in O(1)), which Kadane reduces to O(n).

def build_prefix_sum(arr: List[int]) -> List[int]:
    """Build prefix sum array. Time: O(n) | Space: O(n)"""
    n = len(arr)
    pSum = [0] * n
    pSum[0] = arr[0]
    for i in range(1, n):
        pSum[i] = pSum[i - 1] + arr[i]
    return pSum

def range_sum(pSum: List[int], l: int, r: int) -> int:
    """
    Return sum of arr[l..r] using prefix sum. Time: O(1)
    sum = pSum[r] - pSum[l-1]  (or pSum[r] if l==0)
    """
    if l == 0:
        return pSum[r]
    return pSum[r] - pSum[l - 1]

def max_subarray_prefix(arr: List[int], n: int) -> int:
    """
    O(n²) max subarray via prefix sum — educational bridge to Kadane.
    From L12/008maximumSubarraySumUsingPrefixSum.py.
    Time: O(n²) | Space: O(n)
    """
    pSum = build_prefix_sum(arr)
    max_so_far = float('-inf')
    for i in range(n):
        for j in range(i, n):
            s = pSum[j] if i == 0 else pSum[j] - pSum[i - 1]
            max_so_far = max(max_so_far, s)
    return max_so_far

def prefix_sum_demo():
    print("\n" + "=" * 60)
    print("SECTION 10: Prefix Sum")
    print("=" * 60)

    arr = [10, 20, 30, 40, 50]
    pSum = build_prefix_sum(arr)
    print(f"\n  arr  = {arr}")
    print(f"  pSum = {pSum}")
    print(f"\n  Range queries (O(1) each):")
    queries = [(0, 2), (1, 3), (2, 4), (0, 4)]
    for l, r in queries:
        result = range_sum(pSum, l, r)
        brute  = sum(arr[l:r+1])
        ok = "✓" if result == brute else "✗"
        print(f"    arr[{l}..{r}] = {result}  (brute check: {brute}) {ok}")

    # Max subarray via prefix sum vs naive
    arr2 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    ps_ans = max_subarray_prefix(arr2, len(arr2))
    print(f"\n  Max subarray sum (prefix O(n²)) of {arr2}:")
    print(f"  = {ps_ans}  (subarray [4,-1,2,1] = 6)")
    print(f"  → Kadane's O(n) solution is in Module 11")


# =============================================================================
# SECTION 11: Additional Classic Patterns
# =============================================================================

# --- 11a: Move Zeros to End ---
# Two-pointer write_pos approach. Maintain a "write position" for non-zeros.
# After placing all non-zeros, fill remaining positions with zeros.
# Time: O(n) | Space: O(1)
def move_zeros(arr: List[int]) -> None:
    """Move all zeros to end, preserving relative order of non-zeros."""
    write_pos = 0
    for num in arr:
        if num != 0:
            arr[write_pos] = num
            write_pos += 1
    while write_pos < len(arr):
        arr[write_pos] = 0
        write_pos += 1

# --- 11b: Find Missing Number (Gauss Formula) ---
# Sum of 1..n = n*(n+1)//2. Subtract array sum → missing number.
# Time: O(n) | Space: O(1)
def find_missing(arr: List[int], n: int) -> int:
    """Find missing number in [1..n] given n-1 distinct elements."""
    expected = n * (n + 1) // 2
    return expected - sum(arr)

# --- 11c: Is Sorted ---
# Check every consecutive pair. First pair out of order → return False.
# Time: O(n) | Space: O(1)
def is_sorted(arr: List[int]) -> bool:
    """Return True if arr is non-decreasingly sorted."""
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

# --- 11d: Remove Duplicates from Sorted Array ---
# Two-pointer: write_pos marks next slot for a unique element.
# Time: O(n) | Space: O(1)
def remove_duplicates_sorted(arr: List[int]) -> int:
    """Remove duplicates in-place from sorted array. Return unique count."""
    if not arr:
        return 0
    write_pos = 1
    for i in range(1, len(arr)):
        if arr[i] != arr[i - 1]:
            arr[write_pos] = arr[i]
            write_pos += 1
    return write_pos

# --- 11e: Maximum Difference (Buy Low / Sell High) ---
# Track min_so_far. At each position, best diff ending here = arr[i] - min_so_far.
# Time: O(n) | Space: O(1)
def max_difference(arr: List[int]) -> int:
    """Max arr[j] - arr[i] where j > i. Returns 0 if no positive diff exists."""
    if len(arr) < 2:
        return 0
    min_so_far = arr[0]
    max_diff = 0
    for i in range(1, len(arr)):
        diff = arr[i] - min_so_far
        max_diff = max(max_diff, diff)
        min_so_far = min(min_so_far, arr[i])
    return max_diff

# --- 11f: Target Sum Pair (Sorted Array) — Two Pointers ---
# Count pairs (i,j) where arr[i]+arr[j]==target in a SORTED array.
# BRUTE O(n²): nested loops. OPTIMAL O(n): two pointers converge.
# From L13/003targetSumPair.py.
def target_sum_pair_brute(arr: List[int], target: int) -> int:
    """Brute: O(n²) Time, O(1) Space."""
    cnt = 0
    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                cnt += 1
    return cnt

def target_sum_pair_optimal(arr: List[int], target: int) -> int:
    """
    Optimal: O(n) Time, O(1) Space.
    Two pointers converge: if sum < target → move i right (need bigger left).
                           if sum > target → move j left (need smaller right).
                           if sum == target → count pair, move both.
    Works only on SORTED arrays.
    """
    i, j, cnt = 0, len(arr) - 1, 0
    while i < j:
        pair_sum = arr[i] + arr[j]
        if pair_sum == target:
            cnt += 1
            i += 1; j -= 1
        elif pair_sum > target:
            j -= 1
        else:
            i += 1
    return cnt

def additional_patterns_demo():
    print("\n" + "=" * 60)
    print("SECTION 11: Additional Classic Patterns")
    print("=" * 60)

    # Move zeros
    arr = [0, 1, 0, 3, 12]
    print(f"\n  Move zeros: {arr}", end="")
    move_zeros(arr)
    print(f"  →  {arr}")

    arr2 = [0, 0, 1]
    move_zeros(arr2)
    print(f"  Move zeros: [0,0,1]  →  {arr2}")

    # Find missing
    print(f"\n  Missing in [1,2,4,5], n=5: {find_missing([1,2,4,5], 5)}")
    print(f"  Missing in [3,7,1,2,8,4,5], n=8: {find_missing([3,7,1,2,8,4,5], 8)}")

    # Is sorted
    print(f"\n  is_sorted([1,2,3,4,5]): {is_sorted([1,2,3,4,5])}")
    print(f"  is_sorted([1,3,2,4,5]): {is_sorted([1,3,2,4,5])}")
    print(f"  is_sorted([]):           {is_sorted([])}")

    # Remove duplicates from sorted
    arr = [1, 1, 2, 2, 3, 3, 3, 4]
    count = remove_duplicates_sorted(arr)
    print(f"\n  remove_dup_sorted([1,1,2,2,3,3,3,4]): {count} unique → {arr[:count]}")

    # Max difference
    arr = [2, 3, 10, 6, 4, 8, 1]
    print(f"\n  max_difference({arr}) = {max_difference(arr)}  (10-2=8)")
    print(f"  max_difference([7,9,5,6,3,2]) = {max_difference([7,9,5,6,3,2])}  (9-7=2)")

    # Target sum pair (sorted array required)
    arr_sorted = [1, 2, 3, 4, 5, 6, 7, 8]
    target = 9
    brute = target_sum_pair_brute(arr_sorted, target)
    opt   = target_sum_pair_optimal(arr_sorted, target)
    print(f"\n  target_sum_pair({arr_sorted}, target={target}):")
    print(f"    brute={brute}, optimal={opt}  ✓  (pairs: (1,8),(2,7),(3,6),(4,5))")


# =============================================================================
# PRACTICE SKELETONS — Implement using the OPTIMAL approach
# =============================================================================

def practice_reverse_array(arr: List[int]) -> None:
    """
    Reverse arr in-place using two pointers.
    Time: O(n) | Space: O(1)
    Hint: lo=0, hi=n-1, swap while lo < hi.
    """
    pass

def practice_rotate_array(arr: List[int], k: int) -> None:
    """
    Rotate arr right by k using the 3-reversal algorithm.
    Time: O(n) | Space: O(1)
    Hint: k%=n, reverse all, reverse [0..k-1], reverse [k..n-1].
    """
    pass

def practice_two_sum(arr: List[int], target: int) -> List[int]:
    """
    Return [i, j] such that arr[i]+arr[j]==target. Exactly one solution.
    Time: O(n) | Space: O(n)
    Hint: hash map {value: index}, check complement = target - num.
    """
    pass

def practice_contains_duplicate(nums: List[int]) -> bool:
    """
    Return True if any value appears more than once.
    Time: O(n) | Space: O(n)
    Hint: set, add and check membership simultaneously.
    """
    pass

def practice_find_duplicate(nums: List[int]) -> int:
    """
    Find the duplicate in array of n+1 integers in [1..n].
    Time: O(n) | Space: O(1) — use index mapping (modifies arr).
    Hint: x=nums[0]; if nums[x]==x return x; else swap nums[0], nums[x].
    """
    pass

def practice_longest_consecutive(nums: List[int]) -> int:
    """
    Longest consecutive sequence length.
    Time: O(n) | Space: O(n)
    Hint: set(nums), start only if num-1 not in set, walk with while.
    """
    pass

def practice_product_except_self(nums: List[int]) -> List[int]:
    """
    Product of array except self. No division allowed.
    Time: O(n) | Space: O(1) extra
    Hint: two passes — prefix running product then suffix running product.
    """
    pass

def practice_move_zeros(arr: List[int]) -> None:
    """
    Move all zeros to end, preserving non-zero order. In-place.
    Time: O(n) | Space: O(1)
    Hint: write_pos pointer; place non-zeros, then fill zeros.
    """
    pass

def practice_max_difference(arr: List[int]) -> int:
    """
    Max arr[j]-arr[i] where j > i (best profit).
    Time: O(n) | Space: O(1)
    Hint: track min_so_far, compute diff at each step.
    """
    pass


# =============================================================================
# DRIVER CODE — Tests the OPTIMAL implementations, then prints skeleton results
# =============================================================================
if __name__ == "__main__":
    reverse_demo()
    rotation_demo()
    linear_search_demo()
    three_largest_demo()
    two_sum_demo()
    contains_duplicate_demo()
    find_duplicate_demo()
    consecutive_demo()
    product_demo()
    prefix_sum_demo()
    additional_patterns_demo()

    print("\n" + "=" * 60)
    print("OPTIMAL SOLUTION VERIFICATION")
    print("=" * 60)

    # Reverse
    arr_r = [1, 2, 3, 4, 5]
    reverse_array_optimal(arr_r)
    assert arr_r == [5, 4, 3, 2, 1], f"Reverse failed: {arr_r}"
    print(f"\n  Reverse [1..5]          = {arr_r} ✓")

    # Rotate
    arr_rot = [1, 2, 3, 4, 5]
    rotate_optimal(arr_rot, 2)
    assert arr_rot == [4, 5, 1, 2, 3], f"Rotate failed: {arr_rot}"
    print(f"  Rotate [1..5] k=2       = {arr_rot} ✓")

    # Three Largest
    tl = three_largest([12, 35, 1, 10, 34, 1])
    assert tl == (35, 34, 12), f"Three largest failed: {tl}"
    print(f"  Three largest           = {tl} ✓")

    # Two Sum
    ts = two_sum_optimal([2, 7, 11, 15], 9)
    assert ts == [0, 1], f"Two sum failed: {ts}"
    print(f"  Two sum [2,7,11,15] t=9 = {ts} ✓")

    # Contains Duplicate
    cd = contains_duplicate_optimal([1, 2, 3, 1])
    assert cd == True, f"Contains dup failed"
    print(f"  Contains dup [1,2,3,1]  = {cd} ✓")

    # Find Duplicate
    fd = find_duplicate_optimal([1, 3, 4, 2, 2])
    assert fd == 2, f"Find dup failed: {fd}"
    print(f"  Find duplicate          = {fd} ✓")

    # Longest Consecutive
    lc = longest_consecutive_optimal([100, 4, 200, 1, 3, 2])
    assert lc == 4, f"Longest consecutive failed: {lc}"
    print(f"  Longest consecutive     = {lc} ✓")

    # Product Except Self
    pe = product_except_self_optimal([1, 2, 3, 4])
    assert pe == [24, 12, 8, 6], f"Product failed: {pe}"
    print(f"  Product except self     = {pe} ✓")

    # Prefix Sum
    pSum = build_prefix_sum([10, 20, 30, 40, 50])
    assert range_sum(pSum, 1, 3) == 90, f"Prefix sum range failed"
    print(f"  Prefix sum arr[1..3]    = {range_sum(pSum, 1, 3)} ✓")

    # Move Zeros
    arr_z = [0, 1, 0, 3, 12]
    move_zeros(arr_z)
    assert arr_z == [1, 3, 12, 0, 0], f"Move zeros failed: {arr_z}"
    print(f"  Move zeros              = {arr_z} ✓")

    # Find Missing
    fm = find_missing([1, 2, 4, 5], 5)
    assert fm == 3, f"Find missing failed: {fm}"
    print(f"  Find missing            = {fm} ✓")

    # Max Difference
    md = max_difference([2, 3, 10, 6, 4, 8, 1])
    assert md == 8, f"Max diff failed: {md}"
    print(f"  Max difference          = {md} ✓")

    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS (all return None until implemented)")
    print("=" * 60)
    arr_p = [1, 2, 3]
    practice_reverse_array(arr_p)
    print(f"\n  practice_reverse_array([1,2,3])            = {arr_p}")

    arr_p2 = [1, 2, 3, 4, 5]
    practice_rotate_array(arr_p2, 2)
    print(f"  practice_rotate_array([1,2,3,4,5], k=2)   = {arr_p2}")

    print(f"  practice_two_sum([2,7,11,15], 9)           = {practice_two_sum([2,7,11,15], 9)}")
    print(f"  practice_contains_duplicate([1,2,3,1])     = {practice_contains_duplicate([1,2,3,1])}")
    print(f"  practice_find_duplicate([1,3,4,2,2])       = {practice_find_duplicate([1,3,4,2,2])}")
    print(f"  practice_longest_consecutive([100,4,200,1,3,2]) = {practice_longest_consecutive([100,4,200,1,3,2])}")
    print(f"  practice_product_except_self([1,2,3,4])    = {practice_product_except_self([1,2,3,4])}")

    arr_z2 = [0, 1, 0, 3, 12]
    practice_move_zeros(arr_z2)
    print(f"  practice_move_zeros([0,1,0,3,12])          = {arr_z2}")
    print(f"  practice_max_difference([2,3,10,6,4,8,1]) = {practice_max_difference([2,3,10,6,4,8,1])}")
    print("=" * 60)
    print("Fill in the skeletons above and re-run to verify.")
