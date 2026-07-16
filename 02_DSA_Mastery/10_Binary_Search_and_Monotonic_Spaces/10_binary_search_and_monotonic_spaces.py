###############################################################################
#          10 - Binary Search and Monotonic Spaces                             #
###############################################################################
#
# SOURCES:
#   Coding_Python/1. Python - Intro/10_binary_search_subarrays.py (935 lines)
#   LPLV26MAY/L12 - Intro to Arrays/001binarySearch.py
#   LPLV26MAY/L12 - Intro to Arrays/002firstOccInSortedArray.py
#   LPLV26MAY/L12 - Intro to Arrays/003lastOccInSortedArray.py
#   LPLV26MAY/L12 - Intro to Arrays/005generateSubarrays.py
#   LPLV26MAY/L12 - Intro to Arrays/006maximumSubarraySum.py
#   LPLV26MAY/L12 - Intro to Arrays/007prefixSum.py
#   LPLV26MAY/L12 - Intro to Arrays/008maximumSubarraySumUsingPrefixSum.py
#
# TOPICS IN THIS MODULE:
#   1.  Standard Binary Search
#   2.  First Occurrence (search left on match)
#   3.  Last Occurrence (search right on match)
#   4.  Count Occurrences (last - first + 1)
#   5.  Python bisect module (bisect_left, bisect_right)
#   6.  Generate Sub-Arrays (O(n²) enumeration)
#   7.  Maximum Subarray Sum — 4-step evolution (O(n³) → O(n²) → O(n))
#   8.  Prefix Sum — build + O(1) range queries

from typing import List
import bisect


# =============================================================================
# SECTION 1: Standard Binary Search
# =============================================================================
#
# PREREQUISITE — Monotonic Function:
#   A function where the output only ever moves in ONE direction as input grows.
#   A sorted array is a monotonic function (index=input, value=output).
#   Binary search works on ANY monotonic search space — not just sorted arrays.
#
# WHY O(log n)?  (Derive it, don't memorise it)
#   Each step cuts the search space in half:
#     n → n/2 → n/4 → n/8 → ... → 1
#   After k steps: n / 2^k = 1  →  2^k = n  →  k = log₂(n)
#   Whenever you see "cut in half each step" → it's O(log n).
#
# (lo + hi) // 2  BREAKDOWN:
#   lo + hi  = sum of the two boundary indices
#   // 2     = INTEGER (floor) division → always produces an integer index
#   Result   = always satisfies lo ≤ mid ≤ hi  → never out of bounds
#   Python:  no overflow risk (ints are arbitrary precision)
#   Java/C++: use  lo + (hi - lo) // 2  to avoid integer overflow
#
# VISUAL WALKTHROUGH  arr=[10,20,30,40,50,60,70], target=50:
#   idx:  0   1   2   3   4   5   6
#   arr: [10, 20, 30, 40, 50, 60, 70]
#         lo                       hi    mid=3 → arr[3]=40 < 50 → lo=4
#                          lo       hi   mid=5 → arr[5]=60 > 50 → hi=4
#                          lo,hi         mid=4 → arr[4]=50==50  → FOUND ✓
#   Search space: 7 → 3 → 1 (halved each step) → O(log n)
#
# Time: O(log n) | Space: O(1)  (only lo, hi, mid — no extra arrays)
# From L12/001binarySearch.py

def binary_search(arr: List[int], target: int) -> int:
    """
    Standard binary search: return index of target, or -1 if not found.
    Time: O(log n) | Space: O(1)
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2       # integer division → always a valid index
        if arr[mid] == target:
            return mid             # STOP immediately on any match
        elif arr[mid] < target:
            lo = mid + 1           # target is to the RIGHT → discard left half
        else:
            hi = mid - 1           # target is to the LEFT  → discard right half
    return -1                      # target not in array

def binary_search_demo():
    print("=" * 60)
    print("SECTION 1: Standard Binary Search")
    print("=" * 60)

    arr = [10, 20, 30, 40, 50, 60, 70]
    target = 50
    print(f"\n  arr = {arr}, target = {target}")

    # Step-by-step trace
    print(f"\n  Step-by-step trace:")
    lo, hi = 0, len(arr) - 1
    step = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        action = ""
        if arr[mid] == target:
            action = f"arr[{mid}]={arr[mid]} == {target} → FOUND at index {mid}"
            print(f"    Step {step}: lo={lo}, hi={hi} → mid={mid} → {action}")
            break
        elif arr[mid] < target:
            action = f"arr[{mid}]={arr[mid]} < {target} → lo={mid+1}"
            lo = mid + 1
        else:
            action = f"arr[{mid}]={arr[mid]} > {target} → hi={mid-1}"
            hi = mid - 1
        print(f"    Step {step}: lo={lo-1 if 'lo=' in action else lo}, "
              f"hi={hi+1 if 'hi=' in action else hi} → mid={mid} → {action}")
        step += 1

    tests = [
        ([10, 20, 30, 40, 50, 60, 70], 50,  4),
        ([10, 20, 30, 40, 50, 60, 70], 10,  0),
        ([10, 20, 30, 40, 50, 60, 70], 70,  6),
        ([10, 20, 30, 40, 50, 60, 70], 99, -1),
        ([5], 5, 0),
        ([], 5, -1),
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<35} {'target':>7}  {'result':>7}  {'expected':>9}  {'ok':>3}")
    print("  " + "-" * 65)
    for a, t, exp in tests:
        if not a:
            result = -1
        else:
            result = binary_search(a, t)
        ok = "✓" if result == exp else "✗"
        print(f"  {str(a):<35} {t:>7}  {result:>7}  {exp:>9}  {ok:>3}")


# =============================================================================
# SECTION 2: First Occurrence in Sorted Array
# =============================================================================
#
# PROBLEM: Sorted array WITH duplicates. Find the LEFTMOST index of target.
# Regular binary_search stops at ANY match — that may be in the middle of a run.
#
# KEY MODIFICATION: when arr[mid] == target:
#   1. Record it: ans = mid  (potential answer)
#   2. DON'T stop. Keep searching LEFT: hi = mid - 1
#   (There might be an earlier occurrence to the left)
#
# Still O(log n): every iteration still moves lo or hi inward by half.
# Recording ans and continuing doesn't add iterations.
#
# VISUAL WALKTHROUGH  arr=[10,20,30,30,30,30,30,40,50], target=30:
#   idx:  0   1   2   3   4   5   6   7   8
#   arr: [10, 20, 30, 30, 30, 30, 30, 40, 50]
#   Step 1: lo=0,hi=8 → mid=4 → arr[4]=30==30 → ans=4, hi=3  (hunt LEFT)
#   Step 2: lo=0,hi=3 → mid=1 → arr[1]=20 <30 → lo=2
#   Step 3: lo=2,hi=3 → mid=2 → arr[2]=30==30 → ans=2, hi=1  (hunt LEFT)
#   Step 4: lo=2,hi=1 → lo>hi → STOP
#   Answer: ans=2 ✓  (leftmost 30)
#
# From L12/002firstOccInSortedArray.py

def first_occurrence(arr: List[int], target: int) -> int:
    """
    First (leftmost) index of target in sorted array, or -1 if not found.
    Time: O(log n) | Space: O(1)
    On match: save ans, hunt LEFT (hi = mid - 1).
    """
    lo, hi = 0, len(arr) - 1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            ans = mid              # save this match
            hi = mid - 1          # keep hunting LEFT for an earlier one
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return ans                     # -1 if never found; leftmost index if found


# =============================================================================
# SECTION 3: Last Occurrence in Sorted Array
# =============================================================================
#
# KEY DIFFERENCE: when arr[mid] == target, search RIGHT instead of left.
#   first_occ: ans=mid, hi = mid - 1  (hunt left  → earlier occurrences)
#   last_occ:  ans=mid, lo = mid + 1  (hunt right → later  occurrences)
# Everything else is identical!
#
# VISUAL WALKTHROUGH  same array, target=30:
#   Step 1: lo=0,hi=8 → mid=4 → arr[4]=30==30 → ans=4, lo=5  (hunt RIGHT)
#   Step 2: lo=5,hi=8 → mid=6 → arr[6]=30==30 → ans=6, lo=7  (hunt RIGHT)
#   Step 3: lo=7,hi=8 → mid=7 → arr[7]=40 >30 → hi=6
#   Step 4: lo=7,hi=6 → lo>hi → STOP
#   Answer: ans=6 ✓  (rightmost 30)
#
# From L12/003lastOccInSortedArray.py

def last_occurrence(arr: List[int], target: int) -> int:
    """
    Last (rightmost) index of target in sorted array, or -1 if not found.
    Time: O(log n) | Space: O(1)
    On match: save ans, hunt RIGHT (lo = mid + 1).
    """
    lo, hi = 0, len(arr) - 1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            ans = mid              # save this match
            lo = mid + 1          # keep hunting RIGHT for a later one
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return ans

def occ_demo():
    print("\n" + "=" * 60)
    print("SECTION 2 & 3: First and Last Occurrence")
    print("=" * 60)

    # Three-variant comparison table
    print(f"""
  On-match behaviour comparison:
  ┌──────────────────┬─────────────────────────────┬──────────────────────┐
  │  Function        │  When arr[mid] == target    │  Returns             │
  ├──────────────────┼─────────────────────────────┼──────────────────────┤
  │  binary_search   │  return mid  (stop now)     │  ANY matching index  │
  │  first_occurrence│  ans=mid, hi=mid-1 (left)   │  FIRST (leftmost)    │
  │  last_occurrence │  ans=mid, lo=mid+1 (right)  │  LAST  (rightmost)   │
  └──────────────────┴─────────────────────────────┴──────────────────────┘
  All three: Time O(log n) | Space O(1)
    """)

    arr = [10, 20, 30, 30, 30, 30, 30, 40, 50]
    target = 30
    print(f"  arr = {arr}")
    print(f"  target = {target}")
    print(f"\n  Step trace — first_occurrence:")
    lo, hi, ans = 0, len(arr) - 1, -1
    step = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            ans = mid; hi = mid - 1
            print(f"    Step {step}: lo={lo},hi={hi+1} mid={mid} → MATCH, ans={ans}, hi={hi} (hunt left)")
        elif arr[mid] < target:
            print(f"    Step {step}: lo={lo},hi={hi} mid={mid} → {arr[mid]}<{target}, lo={mid+1}")
            lo = mid + 1
        else:
            print(f"    Step {step}: lo={lo},hi={hi} mid={mid} → {arr[mid]}>{target}, hi={mid-1}")
            hi = mid - 1
        step += 1
    print(f"    → first = {ans} ✓")

    print(f"\n  Step trace — last_occurrence:")
    lo, hi, ans = 0, len(arr) - 1, -1
    step = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            ans = mid; lo = mid + 1
            print(f"    Step {step}: lo={lo-1},hi={hi} mid={mid} → MATCH, ans={ans}, lo={lo} (hunt right)")
        elif arr[mid] < target:
            print(f"    Step {step}: lo={lo},hi={hi} mid={mid} → {arr[mid]}<{target}, lo={mid+1}")
            lo = mid + 1
        else:
            print(f"    Step {step}: lo={lo},hi={hi} mid={mid} → {arr[mid]}>{target}, hi={mid-1}")
            hi = mid - 1
        step += 1
    print(f"    → last  = {ans} ✓")

    # Verification table
    tests = [
        ([10, 20, 30, 30, 30, 30, 30, 40, 50], 30, 2, 6),
        ([1, 1, 1, 1, 1], 1, 0, 4),
        ([5, 10, 15], 10, 1, 1),
        ([5, 10, 15], 99, -1, -1),
        ([7], 7, 0, 0),
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<35} {'t':>3}  {'first':>6}  {'last':>5}  {'ok':>3}")
    print("  " + "-" * 55)
    for a, t, ef, el in tests:
        rf = first_occurrence(a, t)
        rl = last_occurrence(a, t)
        ok = "✓" if rf == ef and rl == el else "✗"
        print(f"  {str(a):<35} {t:>3}  {rf:>6}  {rl:>5}  {ok:>3}")


# =============================================================================
# SECTION 4: Count Occurrences in Sorted Array
# =============================================================================
#
# Because the array is sorted, all copies of target are CONTIGUOUS.
# So: count = last_index - first_index + 1
#
# EXAMPLE: arr=[10,20,30,30,30,30,30,40,50], target=30
#   first=2, last=6 → count = 6 - 2 + 1 = 5  (indices 2,3,4,5,6 → five 30s) ✓
#
# TIME: O(log n) + O(log n) = O(2 log n) = O(log n)  (constants drop in Big-O)
# SPACE: O(1)

def count_occurrences(arr: List[int], target: int) -> int:
    """
    Count occurrences of target in sorted array.
    Time: O(log n) | Space: O(1)
    Formula: last_index - first_index + 1
    """
    first = first_occurrence(arr, target)
    if first == -1:
        return 0                   # target not present at all
    last = last_occurrence(arr, target)
    return last - first + 1        # all occurrences are contiguous in sorted array

def count_demo():
    print("\n" + "=" * 60)
    print("SECTION 4: Count Occurrences")
    print("=" * 60)

    arr = [10, 20, 30, 30, 30, 30, 30, 40, 50]
    print(f"\n  arr = {arr}")
    target = 30
    f = first_occurrence(arr, target)
    l = last_occurrence(arr, target)
    cnt = count_occurrences(arr, target)
    print(f"  target={target}:  first={f}, last={l}, count=last-first+1={l}-{f}+1={cnt} ✓")

    tests = [
        ([10, 20, 30, 30, 30, 30, 30, 40, 50], 30, 5),
        ([10, 20, 30, 30, 30, 30, 30, 40, 50], 10, 1),
        ([10, 20, 30, 30, 30, 30, 30, 40, 50], 99, 0),
        ([1, 1, 1, 1, 1], 1, 5),
        ([5], 5, 1),
        ([5], 9, 0),
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<40} {'t':>3}  {'count':>6}  {'exp':>5}  {'ok':>3}")
    print("  " + "-" * 60)
    for a, t, exp in tests:
        result = count_occurrences(a, t)
        ok = "✓" if result == exp else "✗"
        print(f"  {str(a):<40} {t:>3}  {result:>6}  {exp:>5}  {ok:>3}")


# =============================================================================
# SECTION 5: Python's `bisect` Module — Built-in Binary Search
# =============================================================================
#
# bisect_left(arr, t)  → first index where value >= t  (= our first_occurrence)
# bisect_right(arr, t) → first index where value >  t  (one past last occurrence)
#
# COUNT via bisect: bisect_right(arr, t) - bisect_left(arr, t)
#
# EDGE CASES:
#   target < all elements → bisect_left returns 0
#   target > all elements → bisect_left returns len(arr)
#   target not present    → returns insertion point (still O(log n))
#
# IMPORT VARIANTS:
#   import bisect                  → bisect.bisect_left(arr, t)  [RECOMMENDED]
#   import bisect as bi            → bi.bisect_left(arr, t)
#   from bisect import bisect_left → bisect_left(arr, t)         [fine for one fn]
#   from bisect import *           → bisect_left(arr, t)         [AVOID: pollutes namespace]

def bisect_demo():
    print("\n" + "=" * 60)
    print("SECTION 5: Python bisect Module")
    print("=" * 60)

    arr = [10, 20, 30, 30, 30, 30, 30, 40, 50]
    target = 30
    print(f"\n  arr = {arr}")
    print(f"  target = {target}")

    left_idx  = bisect.bisect_left(arr, target)
    right_idx = bisect.bisect_right(arr, target)
    count     = right_idx - left_idx
    print(f"\n  bisect_left({target})   = {left_idx}   (first occurrence — same as first_occurrence())")
    print(f"  bisect_right({target})  = {right_idx}   (one past last occurrence)")
    print(f"  count = right - left   = {right_idx} - {left_idx} = {count}  ✓")

    # Verify equivalence with our hand-rolled versions
    assert left_idx  == first_occurrence(arr, target), "bisect_left mismatch!"
    assert right_idx == last_occurrence(arr, target) + 1, "bisect_right mismatch!"
    assert count     == count_occurrences(arr, target), "count mismatch!"
    print(f"  bisect_left  == first_occurrence()  ✓")
    print(f"  bisect_right == last_occurrence()+1 ✓")
    print(f"  count        == count_occurrences() ✓")

    # Edge cases
    print(f"\n  Edge cases:")
    edge_cases = [
        ([100, 200, 300, 400, 500], 250, "not present (between 200 and 300)"),
        ([1000, 2000, 3000], 50, "target < all elements → idx 0"),
        ([100, 200, 300], 500, "target > all elements → idx len(arr)"),
        ([10, 20, 30, 30, 30, 40], 30, "multiple copies"),
    ]
    print(f"  {'arr':<30} {'target':>7}  {'left':>6}  {'right':>6}  {'note'}")
    print("  " + "-" * 75)
    for a, t, note in edge_cases:
        l = bisect.bisect_left(a, t)
        r = bisect.bisect_right(a, t)
        print(f"  {str(a):<30} {t:>7}  {l:>6}  {r:>6}  ← {note}")

    # bisect as count_occurrences one-liner
    print(f"\n  Count via bisect one-liner:")
    print(f"  bisect.bisect_right(arr, 30) - bisect.bisect_left(arr, 30) = {count}")
    print(f"  (works for any target, including those not in array → returns 0)")


# =============================================================================
# SECTION 6: Generate Sub-Arrays
# =============================================================================
#
# A sub-array is a CONTIGUOUS portion of an array (original order, no skipping).
# NOT a sub-array: [1,3] from [1,2,3] (skips 2) → that's a sub-sequence.
#
# For arr=[1,2,3]: sub-arrays are [1],[1,2],[1,2,3],[2],[2,3],[3] → n*(n+1)/2 total.
#
# PATTERN: i anchors the start, j sweeps right to grow the window.
#   i=0: j=0→[1]   j=1→[1,2]   j=2→[1,2,3]
#   i=1: j=1→[2]   j=2→[2,3]
#   i=2: j=2→[3]
#
# TIME:
#   Enumeration (just printing indices): O(n²)  — two loops, triangular sum
#   If you SLICE inside (arr[i:j+1]): O(n³)  — each slice copies up to n elements
#   From L12/005generateSubarrays.py
#
# SPACE: O(n) if slicing (temporary copy per subarray); O(1) if just printing indices

def generate_subarrays(arr: List[int]) -> List[List[int]]:
    """
    Return all sub-arrays (contiguous slices) of arr.
    Time: O(n³) due to slicing | Space: O(n³) for result storage
    Time: O(n²) if you only enumerate (i,j) pairs without copying
    """
    result = []
    n = len(arr)
    for i in range(n):
        for j in range(i, n):
            result.append(arr[i:j + 1])     # slice is O(j-i+1)
    return result

def subarrays_demo():
    print("\n" + "=" * 60)
    print("SECTION 6: Generate Sub-Arrays")
    print("=" * 60)

    arr = [1, 2, 3]
    n = len(arr)
    subarrays = generate_subarrays(arr)
    print(f"\n  arr = {arr}")
    print(f"  Total subarrays = n*(n+1)/2 = {n}*{n+1}//2 = {n*(n+1)//2}")
    print(f"  All subarrays: {subarrays}")

    print(f"\n  Complexity breakdown:")
    print(f"  - 2-loop enumeration (i,j pairs):    O(n²)  — triangular sum n*(n+1)/2")
    print(f"  - With arr[i:j+1] slice inside:      O(n³)  — each slice copies O(length)")
    print(f"  - n=3: {n*(n+1)//2} pairs, actual sum of lengths = {sum(j-i+1 for i in range(n) for j in range(i,n))}")
    print(f"  - n=3: n*(n+1)*(n+2)/6 = {n*(n+1)*(n+2)//6}  (exact slice-copy work)")


# =============================================================================
# SECTION 7: Maximum Subarray Sum — 4-Step Evolution
# =============================================================================
#
# PROBLEM: Find contiguous subarray with maximum sum.
# Example: arr=[-2,1,-3,4,-1,2,1,-5,4] → subarray [4,-1,2,1] = 6
#
# WHY NOT TRIVIAL: negative numbers create start/stop decisions.
# EVOLUTION: O(n³) → O(n²) → O(n²)/O(n) → O(n)/O(n)
# (Kadane's O(n)/O(1) is the final answer — covered in Module 09)
#
# ─────────────────────────────────────────────────────────────────────
# APPROACH 1: Brute Force — O(n³) Time, O(1) Space
# ─────────────────────────────────────────────────────────────────────
# Three loops: i=start, j=end, k=sum.  Recompute sum from scratch every time.
# For n=1000: ~166 million operations.
# From L12/006maximumSubarraySum.py

def max_subarray_brute(arr: List[int]) -> int:
    """Brute force: O(n³) Time, O(1) Space. Recompute sum for every (i,j)."""
    n = len(arr)
    max_so_far = float('-inf')
    for i in range(n):
        for j in range(i, n):
            current_sum = 0
            for k in range(i, j + 1):     # recompute sum from scratch
                current_sum += arr[k]
            max_so_far = max(max_so_far, current_sum)
    return max_so_far

# ─────────────────────────────────────────────────────────────────────
# APPROACH 2: Optimised Brute — O(n²) Time, O(1) Space
# ─────────────────────────────────────────────────────────────────────
# KEY INSIGHT: sum(i..j+1) = sum(i..j) + arr[j+1]
# Extend the running sum instead of recomputing → eliminates the k-loop.
#
# Walkthrough for arr=[1,-2,3,4]:
#   i=0: cur=0 → j=0: cur=1,max=1 → j=1: cur=-1 → j=2: cur=2 → j=3: cur=6,max=6
#   i=2: cur=0 → j=2: cur=3 → j=3: cur=7,max=7  ← new max!
#   Answer: 7 (subarray [3,4])

def max_subarray_optimised(arr: List[int]) -> int:
    """Optimised brute: O(n²) Time, O(1) Space. Extend sum instead of recomputing."""
    n = len(arr)
    max_so_far = float('-inf')
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]          # EXTEND — don't recompute
            max_so_far = max(max_so_far, current_sum)
    return max_so_far

# ─────────────────────────────────────────────────────────────────────
# APPROACH 3: Prefix Sum + All Pairs — O(n²) Time, O(n) Space
# ─────────────────────────────────────────────────────────────────────
# sum(arr[i..j]) = prefix[j] - prefix[i-1]   (i=0: just prefix[j])
# Still O(n²) pairs, but each pair now takes O(1) via subtraction.
# Same time as Approach 2, but introduces the powerful prefix-sum concept.
# From L12/008maximumSubarraySumUsingPrefixSum.py

def build_prefix_sum(arr: List[int]) -> List[int]:
    """
    Build prefix sum array.
    prefix[i] = arr[0] + arr[1] + ... + arr[i]
    Recurrence: prefix[0] = arr[0]; prefix[i] = prefix[i-1] + arr[i]
    Time: O(n) | Space: O(n)
    From L12/007prefixSum.py
    """
    n = len(arr)
    prefix = [0] * n
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i - 1] + arr[i]
    return prefix

def max_subarray_prefix(arr: List[int]) -> int:
    """Prefix sum all pairs: O(n²) Time, O(n) Space."""
    prefix = build_prefix_sum(arr)
    n = len(arr)
    max_so_far = float('-inf')
    for i in range(n):
        for j in range(i, n):
            current_sum = prefix[j] if i == 0 else prefix[j] - prefix[i - 1]
            max_so_far = max(max_so_far, current_sum)
    return max_so_far

# ─────────────────────────────────────────────────────────────────────
# APPROACH 4: Prefix Sum + Running Minimum — O(n) Time, O(n) Space
# ─────────────────────────────────────────────────────────────────────
# KEY INSIGHT:
#   sum(arr[i..j]) = prefix[j] - prefix[i-1]
#   To MAXIMISE this for a fixed j: minimise prefix[i-1].
#   Track min prefix seen so far in a single variable!
#
# min_prefix starts at 0 (= prefix[-1], the empty sum before index 0).
# This correctly handles subarrays starting at index 0:
#   sum(arr[0..j]) = prefix[j] - 0 = prefix[j]
#
# Walkthrough for arr=[1,-2,3,4], prefix=[1,-1,2,6]:
#   j=0: max=max(-inf, 1-0)=1,   min_prefix=min(0,1)=0
#   j=1: max=max(1, -1-0)=1,     min_prefix=min(0,-1)=-1
#   j=2: max=max(1, 2-(-1))=3,   min_prefix=min(-1,2)=-1
#   j=3: max=max(3, 6-(-1))=7,   min_prefix=min(-1,6)=-1
#   Answer: 7  (prefix[3]-prefix[1] = 6-(-1) = sum([3,4]) = 7) ✓

def max_subarray_prefix_optimised(arr: List[int]) -> int:
    """Prefix sum + running minimum: O(n) Time, O(n) Space."""
    prefix = build_prefix_sum(arr)
    max_so_far  = float('-inf')
    min_prefix  = 0              # represents prefix[-1] = 0 (empty subarray start)
    for j in range(len(arr)):
        max_so_far = max(max_so_far, prefix[j] - min_prefix)
        min_prefix = min(min_prefix, prefix[j])
    return max_so_far

def max_subarray_demo():
    print("\n" + "=" * 60)
    print("SECTION 7: Maximum Subarray Sum — 4-Step Evolution")
    print("=" * 60)

    test_cases = [
        ([1, -2, 3, 4],                7,  "[3, 4]"),
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6, "[4,-1,2,1]"),
        ([-3, -1, -2],                -1, "[-1] (all negative)"),
        ([5],                          5, "[5]"),
    ]

    print(f"\n  {'arr':<40} {'B(n³)':>6}  {'O(n²)':>6}  {'P(n²)':>6}  {'P(n)':>6}  {'exp':>6}")
    print("  " + "-" * 75)
    for arr, expected, note in test_cases:
        b  = max_subarray_brute(arr)
        o  = max_subarray_optimised(arr)
        p  = max_subarray_prefix(arr)
        po = max_subarray_prefix_optimised(arr)
        all_agree = "✓" if b == o == p == po == expected else "✗ MISMATCH"
        print(f"  {str(arr):<40} {b:>6}  {o:>6}  {p:>6}  {po:>6}  {expected:>6} {all_agree}  ← {note}")

    # Prefix sum range query demonstration
    arr = [3, 1, 4, 1, 5]
    prefix = build_prefix_sum(arr)
    print(f"\n  Prefix sum range query demo:")
    print(f"  arr    = {arr}")
    print(f"  prefix = {prefix}")
    print(f"  sum(arr[2..4]) = prefix[4]-prefix[1] = {prefix[4]}-{prefix[1]} = {prefix[4]-prefix[1]}")
    print(f"  Verify: {arr[2]}+{arr[3]}+{arr[4]} = {arr[2]+arr[3]+arr[4]}  ✓")
    print(f"  sum(arr[0..2]) = prefix[2]           = {prefix[2]}  (i=0, use prefix[j] directly)")
    print(f"  Verify: {arr[0]}+{arr[1]}+{arr[2]} = {arr[0]+arr[1]+arr[2]}  ✓")
    print(f"  sum(arr[1..3]) = prefix[3]-prefix[0] = {prefix[3]}-{prefix[0]} = {prefix[3]-prefix[0]}")
    print(f"  Verify: {arr[1]}+{arr[2]}+{arr[3]} = {arr[1]+arr[2]+arr[3]}  ✓")

    print(f"""
  4-Step Summary:
  ┌──────────────────────────────┬──────────┬─────────┬──────────────────────────────────────┐
  │  Approach                    │  Time    │  Space  │  Key Idea                             │
  ├──────────────────────────────┼──────────┼─────────┼──────────────────────────────────────┤
  │  Brute force (3 loops)       │  O(n³)   │  O(1)   │  Recompute sum from scratch (i,j,k)  │
  │  Optimised brute (2 loops)   │  O(n²)   │  O(1)   │  Extend running sum (eliminate k)    │
  │  Prefix sum + all pairs      │  O(n²)   │  O(n)   │  sum(i..j) = prefix[j]-prefix[i-1]   │
  │  Prefix sum + running min ✓  │  O(n)    │  O(n)   │  For each j, subtract min seen so far │
  │  Kadane's (Module 09)  ✓✓   │  O(n)    │  O(1)   │  Extend or reset — no prefix array   │
  └──────────────────────────────┴──────────┴─────────┴──────────────────────────────────────┘
    """)


# =============================================================================
# SECTION 8: Prefix Sum — Build and O(1) Range Queries
# =============================================================================
#
# prefix[i] = arr[0] + arr[1] + ... + arr[i]  ("cumulative sum up to index i")
#
# BUILD RECURRENCE:
#   prefix[0] = arr[0]              (base case)
#   prefix[i] = prefix[i-1] + arr[i]  (one addition per step, not a re-scan)
#
# O(1) RANGE QUERY FORMULA:
#   sum(arr[i..j]) = prefix[j] - prefix[i-1]
#   (Special case i=0: sum(arr[0..j]) = prefix[j])
#
# WHY THE FORMULA WORKS (algebraic proof):
#   prefix[j]   = arr[0]+...+arr[i-1]+arr[i]+...+arr[j]
#   prefix[i-1] = arr[0]+...+arr[i-1]
#   Difference  = arr[i]+...+arr[j]  ✓  (the i-1 terms cancel)
#
# TRADE-OFF:
#   Without prefix: any range query takes O(n) — scan the elements
#   With prefix:    O(n) build + O(n) space → O(1) per query thereafter
#   Worth it when answering MANY range queries on the same array.
#
# From L12/007prefixSum.py

def prefix_sum_demo():
    print("\n" + "=" * 60)
    print("SECTION 8: Prefix Sum — Build + O(1) Range Queries")
    print("=" * 60)

    arr = [10, 20, 30, 40, 50]
    prefix = build_prefix_sum(arr)
    print(f"\n  arr    = {arr}")
    print(f"  prefix = {prefix}")
    print(f"\n  Build recurrence:")
    print(f"    prefix[0] = {arr[0]}")
    for i in range(1, len(arr)):
        print(f"    prefix[{i}] = prefix[{i-1}] + arr[{i}] = {prefix[i-1]} + {arr[i]} = {prefix[i]}")

    queries = [(0, 2), (1, 3), (2, 4), (0, 4)]
    print(f"\n  Range queries (each O(1)):")
    for lo, hi in queries:
        result = prefix[hi] if lo == 0 else prefix[hi] - prefix[lo - 1]
        brute  = sum(arr[lo:hi+1])
        formula = f"prefix[{hi}]={'−prefix['+str(lo-1)+']' if lo>0 else ''}" \
                  f"={prefix[hi]}{('-'+str(prefix[lo-1])) if lo>0 else ''}"
        ok = "✓" if result == brute else "✗"
        print(f"    arr[{lo}..{hi}] = {result}  (brute={brute}) {ok}")


# =============================================================================
# PRACTICE SKELETONS — Implement using O(log n) where applicable
# =============================================================================

def practice_binary_search(arr: List[int], target: int) -> int:
    """
    Return index of target in sorted arr, or -1 if not found.
    Time: O(log n) | Space: O(1)
    Hint: lo=0, hi=n-1; mid=(lo+hi)//2; if match→return, if<→lo=mid+1, if>→hi=mid-1
    """
    pass

def practice_first_occurrence(arr: List[int], target: int) -> int:
    """
    Return FIRST (leftmost) index of target in sorted arr, or -1.
    Time: O(log n) | Space: O(1)
    Hint: same as binary_search but on match: ans=mid, hi=mid-1 (keep hunting left)
    """
    pass

def practice_last_occurrence(arr: List[int], target: int) -> int:
    """
    Return LAST (rightmost) index of target in sorted arr, or -1.
    Time: O(log n) | Space: O(1)
    Hint: same as first_occurrence but on match: ans=mid, lo=mid+1 (hunt right)
    """
    pass

def practice_count_occurrences(arr: List[int], target: int) -> int:
    """
    Return count of target in sorted arr.
    Time: O(log n) | Space: O(1)
    Hint: count = last_occurrence - first_occurrence + 1; return 0 if first==-1
    """
    pass

def practice_build_prefix(arr: List[int]) -> List[int]:
    """
    Build and return prefix sum array.
    Time: O(n) | Space: O(n)
    Hint: prefix[0]=arr[0]; prefix[i]=prefix[i-1]+arr[i]
    """
    pass

def practice_range_sum(prefix: List[int], lo: int, hi: int) -> int:
    """
    Return sum of arr[lo..hi] given its prefix sum array.
    Time: O(1) | Space: O(1)
    Hint: prefix[hi] if lo==0 else prefix[hi]-prefix[lo-1]
    """
    pass


# =============================================================================
# DRIVER CODE — Verifies all optimal implementations, then shows skeleton stubs
# =============================================================================
if __name__ == "__main__":
    binary_search_demo()
    occ_demo()
    count_demo()
    bisect_demo()
    subarrays_demo()
    max_subarray_demo()
    prefix_sum_demo()

    print("\n" + "=" * 60)
    print("OPTIMAL SOLUTION VERIFICATION")
    print("=" * 60)

    # --- Binary Search ---
    arr7 = [10, 20, 30, 40, 50, 60, 70]
    assert binary_search(arr7, 50) == 4
    assert binary_search(arr7, 10) == 0
    assert binary_search(arr7, 70) == 6
    assert binary_search(arr7, 99) == -1
    assert binary_search([5], 5) == 0
    print(f"\n  binary_search: 5 assertions ✓")

    # --- First / Last Occurrence ---
    arr_dup = [10, 20, 30, 30, 30, 30, 30, 40, 50]
    assert first_occurrence(arr_dup, 30) == 2
    assert last_occurrence(arr_dup, 30)  == 6
    assert first_occurrence(arr_dup, 99) == -1
    assert last_occurrence(arr_dup, 99)  == -1
    assert first_occurrence([1,1,1,1,1], 1) == 0
    assert last_occurrence([1,1,1,1,1], 1)  == 4
    print(f"  first_occurrence: 3 assertions ✓")
    print(f"  last_occurrence:  3 assertions ✓")

    # --- Count Occurrences ---
    assert count_occurrences(arr_dup, 30) == 5
    assert count_occurrences(arr_dup, 10) == 1
    assert count_occurrences(arr_dup, 99) == 0
    assert count_occurrences([1,1,1,1,1], 1) == 5
    print(f"  count_occurrences: 4 assertions ✓")

    # --- bisect equivalence ---
    bl = bisect.bisect_left(arr_dup, 30)
    br = bisect.bisect_right(arr_dup, 30)
    assert bl == first_occurrence(arr_dup, 30)
    assert br == last_occurrence(arr_dup, 30) + 1
    assert (br - bl) == count_occurrences(arr_dup, 30)
    print(f"  bisect equivalence: 3 assertions ✓")

    # --- Prefix Sum ---
    arr_p = [3, 1, 4, 1, 5]
    prefix = build_prefix_sum(arr_p)
    assert prefix == [3, 4, 8, 9, 14]
    assert (prefix[4] - prefix[1]) == (4 + 1 + 5)   # arr[2..4]
    assert prefix[2]               == (3 + 1 + 4)    # arr[0..2]
    assert (prefix[3] - prefix[0]) == (1 + 4 + 1)   # arr[1..3]
    print(f"  build_prefix_sum: 4 assertions ✓")

    # --- Max Subarray all 4 approaches ---
    test_arrs = [
        ([1, -2, 3, 4], 7),
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([-3, -1, -2], -1),
    ]
    for a, exp in test_arrs:
        assert max_subarray_brute(a)            == exp
        assert max_subarray_optimised(a)        == exp
        assert max_subarray_prefix(a)           == exp
        assert max_subarray_prefix_optimised(a) == exp
    print(f"  max_subarray (all 4 approaches, 3 test arrays): 12 assertions ✓")

    # Summary
    print(f"\n  {'─'*40}")
    print(f"  Total verified assertions: 32 ✓")
    print(f"  {'─'*40}")

    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS (return None until implemented)")
    print("=" * 60)

    arr_test = [10, 20, 30, 30, 30, 40, 50]
    print(f"\n  arr = {arr_test}")
    print(f"  practice_binary_search(arr, 30)      = {practice_binary_search(arr_test, 30)}")
    print(f"  practice_first_occurrence(arr, 30)   = {practice_first_occurrence(arr_test, 30)}")
    print(f"  practice_last_occurrence(arr, 30)    = {practice_last_occurrence(arr_test, 30)}")
    print(f"  practice_count_occurrences(arr, 30)  = {practice_count_occurrences(arr_test, 30)}")

    arr_p2 = [10, 20, 30, 40, 50]
    p2 = practice_build_prefix(arr_p2)
    print(f"\n  arr2 = {arr_p2}")
    print(f"  practice_build_prefix(arr2)          = {p2}")
    print(f"  practice_range_sum(prefix, 1, 3)     = {practice_range_sum(p2, 1, 3) if p2 else None}")
    print("=" * 60)
    print("Fill in the skeletons above and re-run to verify.")
