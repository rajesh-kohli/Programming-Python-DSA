###############################################################################
#        Two Pointers Technique & Kadane's Algorithm — Complete Guide        #
###############################################################################

# This file picks up where 10_binary_search_subarrays.py left off — that file
# promised "Kadane's Algorithm is O(n) — covered in a later lecture." This is
# that lecture, plus the broader TWO POINTERS technique that powers many of
# the most common array interview questions.


# =============================================================================
# SECTION 1: The Two Pointers Technique
# =============================================================================

# ----- What is it? -----
# Instead of using nested loops (checking every pair → O(n^2)), use TWO
# index variables that move through the array — often from opposite ends,
# sometimes both from the start — to solve the problem in a SINGLE pass O(n).
#
# ----- When does it apply? -----
# Two pointers works when the array is SORTED (or can be sorted) and the
# problem involves finding a PAIR or RANGE of elements that satisfy some
# condition (sum, product, distance, etc.).
#
# ----- The core intuition -----
# With a sorted array and pointers at both ends (i=0, j=n-1):
#   - The pair (arr[i], arr[j]) is currently the "widest" possible pair.
#   - If the pair's sum is too SMALL, the only way to increase it is to
#     move the LEFT pointer right (to a bigger value): i += 1
#   - If the pair's sum is too LARGE, move the RIGHT pointer left
#     (to a smaller value): j -= 1
#   - This eliminates one element from consideration EVERY step — that's
#     why it's O(n) instead of O(n^2).


# =============================================================================
# SECTION 2: Generate All Pairs (the brute-force baseline)
# =============================================================================

# Before optimizing anything, you need to recognize the brute-force shape:
# "for every pair (i, j) where i < j" — this pattern shows up everywhere.

def generate_pairs(arr: list[int], n: int) -> None:
    for i in range(n - 1):
        for j in range(i + 1, n):
            print(arr[i], arr[j])
        print()

print("=" * 70)
print("SECTION 2: Generate All Pairs")
print("=" * 70)
generate_pairs([10, 20, 30], 3)
# Output:
#   10 20
#   10 30
#
#   20 30
#
# Time:  O(n^2) — every pair is visited once: n*(n-1)/2 pairs
# Space: O(1) — no extra storage, just printing


# =============================================================================
# SECTION 3: Target Sum Pair — Count Pairs Summing to a Target
# =============================================================================

# ----- Problem -----
# Given an array and a target t, count how many pairs (i, j) with i < j
# have arr[i] + arr[j] == t.

# ----- Approach 1: Brute Force — check every pair -----

def target_sum_pair(arr: list[int], n: int, t: int) -> int:
    cnt = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            pair_sum = arr[i] + arr[j]
            if pair_sum == t:
                cnt += 1
    return cnt

# Time:  O(n^2) — nested loop over all pairs
# Space: O(1)

# ----- Approach 2: Two Pointers — REQUIRES a sorted array -----
#
# Idea: start with the widest pair (i=0, j=n-1).
#   - If pair_sum == t: found a match! Move BOTH pointers inward to look
#     for the next pair (i += 1, j -= 1).
#   - If pair_sum > t: the sum is too big — the only way to shrink it is
#     to drop the LARGER end, so move j left (j -= 1).
#   - If pair_sum < t: the sum is too small — move i right (i += 1) to
#     pick up a bigger value.

def target_sum_pair_optimised(arr: list[int], n: int, t: int) -> int:
    cnt = 0
    i, j = 0, n - 1
    while i < j:
        pair_sum = arr[i] + arr[j]
        if pair_sum == t:
            cnt += 1
            i += 1
            j -= 1
        elif pair_sum > t:
            j -= 1
        else:  # pair_sum < t
            i += 1
    return cnt

# Time:  O(n) — each step moves i forward or j backward; together they can
#               only take n steps total before i meets j
# Space: O(1)

print("\n" + "=" * 70)
print("SECTION 3: Target Sum Pair")
print("=" * 70)

arr = [1, 2, 3, 4, 5, 6]
t = 7
print(f"Array: {arr}, Target: {t}")
print(f"Brute force count:    {target_sum_pair(arr, len(arr), t)}")
print(f"Two-pointer count:    {target_sum_pair_optimised(arr, len(arr), t)}")

# ----- Walkthrough of the two-pointer version -----
# arr = [1, 2, 3, 4, 5, 6],  t = 7
#
# i=0, j=5: arr[0]+arr[5] = 1+6 = 7  == t  → MATCH! cnt=1, i=1, j=4
# i=1, j=4: arr[1]+arr[4] = 2+5 = 7  == t  → MATCH! cnt=2, i=2, j=3
# i=2, j=3: arr[2]+arr[3] = 3+4 = 7  == t  → MATCH! cnt=3, i=3, j=2
# i=3, j=2: i is NOT < j  → loop ends
#
# Result: 3 pairs found: (1,6), (2,5), (3,4)
#
# ----- IMPORTANT GOTCHA -----
# The two-pointer version ONLY works on a SORTED array. If your input
# isn't sorted, you must sort it first: arr.sort() — which costs O(n log n).
# Even with that sort, O(n log n) is still much better than the brute
# force's O(n^2) for large arrays.


# =============================================================================
# SECTION 4: Kadane's Algorithm — Maximum Subarray Sum in O(n)
# =============================================================================

# ----- Recap from 10_binary_search_subarrays.py -----
# We previously solved "max subarray sum" with:
#   Brute force:          O(n^3)
#   Optimized brute force: O(n^2)
#   Prefix sum:            O(n^2), then O(n) with the running-minimum trick
#
# Kadane's Algorithm reaches O(n) time AND O(1) space with a much simpler
# idea — and it's the algorithm interviewers actually expect you to know.

# ----- The core idea -----
# At each index i, ask: "Is it better to EXTEND the previous subarray by
# including arr[i], or to START FRESH at arr[i]?"
#
#   x[i] = max(x[i-1] + arr[i],   arr[i])
#            ^ extend                ^ start fresh
#
# If the running sum so far (x[i-1]) is NEGATIVE, it can only hurt us to
# carry it forward — so we "reset" and start a new subarray at arr[i].
# If x[i-1] is positive, adding arr[i] to it can only help (or at worst,
# we still compare against starting fresh).

# ----- Version 1: With an array (easier to understand first) -----

def maximum_subarray_sum_using_kadanes(arr: list[int], n: int) -> int:
    x = [None] * n          # x[i] = max subarray sum ENDING exactly at index i
    x[0] = arr[0]
    max_so_far = x[0]

    for i in range(1, n):
        x[i] = max(x[i - 1] + arr[i], arr[i])
        max_so_far = max(max_so_far, x[i])

    return max_so_far

# Time:  O(n) — single pass
# Space: O(n) — the x[] array stores one value per index

# ----- Version 2: Optimized — we only ever need the PREVIOUS value of x -----
# Replace the array with a single variable, since x[i] only depends on x[i-1].

def maximum_subarray_sum_using_kadanes_optimised(arr: list[int], n: int) -> int:
    x = arr[0]               # running max subarray sum ending at current index
    max_so_far = x

    for i in range(1, n):
        x = max(x + arr[i], arr[i])
        max_so_far = max(max_so_far, x)

    return max_so_far

# Time:  O(n)
# Space: O(1)  ← this is the version you should write in an interview

print("\n" + "=" * 70)
print("SECTION 4: Kadane's Algorithm")
print("=" * 70)

arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
n = len(arr)
print(f"Array: {arr}")
print(f"Kadane's (with array):    {maximum_subarray_sum_using_kadanes(arr, n)}")
print(f"Kadane's (optimised):     {maximum_subarray_sum_using_kadanes_optimised(arr, n)}")

# ----- Full Walkthrough -----
# arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
#
# i=0: x=-2,                              max_so_far=-2
# i=1: x=max(-2+1, 1)=max(-1,1)=1         max_so_far=1   (reset! -2+1 < 1)
# i=2: x=max(1-3, -3)=max(-2,-3)=-2       max_so_far=1
# i=3: x=max(-2+4, 4)=max(2,4)=4          max_so_far=4   (reset! -2+4 < 4)
# i=4: x=max(4-1, -1)=max(3,-1)=3         max_so_far=4   (extend: 4-1=3 > -1)
# i=5: x=max(3+2, 2)=max(5,2)=5           max_so_far=5   (extend)
# i=6: x=max(5+1, 1)=max(6,1)=6           max_so_far=6   (extend)
# i=7: x=max(6-5, -5)=max(1,-5)=1         max_so_far=6   (extend, sum drops to 1)
# i=8: x=max(1+4, 4)=max(5,4)=5           max_so_far=6   (extend)
#
# Result: 6  → the subarray [4, -1, 2, 1] sums to 6 ✓
#
# ----- Why does "reset when negative" work? -----
# If the running sum x becomes negative, NO future subarray benefits from
# including it — adding a negative prefix can only make a future sum smaller.
# So Kadane's effectively "throws away" any prefix that's dragging us down
# and starts counting fresh from the current element.

# ----- Comparison Table -----
# | Approach                  | Time   | Space | Notes                        |
# |----------------------------|--------|-------|-------------------------------|
# | Brute force (3 loops)      | O(n^3) | O(1)  | Recompute sum every time     |
# | Optimized brute force      | O(n^2) | O(1)  | Extend sum instead of recompute|
# | Prefix sum (all pairs)     | O(n^2) | O(n)  | Precompute, still all pairs  |
# | Prefix sum + running min   | O(n)   | O(n)  | Track min prefix seen so far |
# | Kadane's (array)           | O(n)   | O(n)  | Same idea, cleaner framing   |
# | Kadane's (optimised)       | O(n)   | O(1)  | THE answer interviewers want |


# =============================================================================
# SECTION 5: Container With Most Water (Classic Two-Pointer Problem)
# =============================================================================

# ----- Problem -----
# Given an array `height` where height[i] is the height of a vertical line
# at position i, find two lines that, together with the x-axis, form a
# container holding the MOST water.
#
# Area = width * min(height[i], height[j])
#   width = distance between the two lines (j - i)
#   height = limited by the SHORTER of the two lines (water spills over the shorter one)

# ----- Approach 1: Brute Force — try every pair -----

def max_area_brute(height: list[int]) -> int:
    n = len(height)
    max_so_far = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            w = j - i
            h = min(height[i], height[j])
            a = w * h
            max_so_far = max(max_so_far, a)
    return max_so_far

# Time:  O(n^2) — TLE (Time Limit Exceeded) on large inputs in coding interviews
# Space: O(1)

# ----- Approach 2: Two Pointers — start wide, shrink smartly -----
#
# Start with the WIDEST possible container (i=0, j=n-1).
# At each step, move the pointer at the SHORTER line inward.
#
# ----- Why move the shorter line? (the key insight) -----
# The container's height is capped by min(height[i], height[j]).
# If we move the TALLER line inward, width shrinks AND the height is
# still capped by the same short line — area can only get worse or equal.
# If we move the SHORTER line inward, width shrinks but there's a CHANCE
# we find a taller line that increases the height cap — area might improve.
# So moving the shorter pointer is the only move that could possibly help.

def max_area_optimised(height: list[int]) -> int:
    n = len(height)
    max_so_far = 0
    i, j = 0, n - 1
    while i < j:
        w = j - i
        h = min(height[i], height[j])
        a = w * h
        max_so_far = max(max_so_far, a)
        if height[i] < height[j]:
            i += 1          # left line is shorter — move it
        else:
            j -= 1          # right line is shorter (or equal) — move it
    return max_so_far

# Time:  O(n) — single pass, i and j together move at most n times
# Space: O(1)

print("\n" + "=" * 70)
print("SECTION 5: Container With Most Water")
print("=" * 70)

heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
print(f"Heights: {heights}")
print(f"Brute force max area: {max_area_brute(heights)}")
print(f"Two-pointer max area: {max_area_optimised(heights)}")

# ----- Walkthrough -----
# heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]   indices: 0 1 2 3 4 5 6 7 8
#
# i=0,j=8: w=8, h=min(1,7)=1,  a=8     max=8    height[0]=1 < height[8]=7 → i=1
# i=1,j=8: w=7, h=min(8,7)=7,  a=49    max=49   height[1]=8 >= height[8]=7 → j=7
# i=1,j=7: w=6, h=min(8,3)=3,  a=18    max=49   height[1]=8 >= height[7]=3 → j=6
# i=1,j=6: w=5, h=min(8,8)=8,  a=40    max=49   height[1]=8 >= height[6]=8 → j=5
# i=1,j=5: w=4, h=min(8,4)=4,  a=16    max=49   ... continues until i meets j
#
# Result: 49 (the container between index 1 and index 8)


# =============================================================================
# SECTION 6: Merge Two Sorted Arrays (Two-Pointer Merge)
# =============================================================================

# ----- Problem -----
# Given two SORTED arrays a and b, merge them into one sorted array c.
# This is the core building block of MERGE SORT (covered in 09_sorting_algorithms.py).

def merge_sorted_arrays(a: list[int], b: list[int], n: int, m: int) -> list[int]:
    i, j, k = 0, 0, 0        # i walks through a, j walks through b, k fills c
    c = [None] * (n + m)

    # Compare current elements of a and b, take the smaller one
    while i <= n - 1 and j <= m - 1:
        if a[i] <= b[j]:
            c[k] = a[i]
            i += 1
            k += 1
        else:
            c[k] = b[j]
            j += 1
            k += 1

    # One of the arrays is exhausted — copy whatever remains from the other.
    # Only ONE of these two while loops will actually run.
    while i <= n - 1:
        c[k] = a[i]
        i += 1
        k += 1

    while j <= m - 1:
        c[k] = b[j]
        j += 1
        k += 1

    return c

# Time:  O(n + m) — each element from both arrays is visited exactly once
# Space: O(n + m) — the new merged array c

print("\n" + "=" * 70)
print("SECTION 6: Merge Two Sorted Arrays")
print("=" * 70)

a = [10, 30, 50, 60]
b = [20, 40, 70]
print(f"a = {a}")
print(f"b = {b}")
merged = merge_sorted_arrays(a, b, len(a), len(b))
print(f"merged = {merged}")

# ----- Walkthrough -----
# a = [10, 30, 50, 60],  b = [20, 40, 70]
#
# i=0,j=0: a[0]=10 <= b[0]=20 → c=[10],          i=1
# i=1,j=0: a[1]=30 >  b[0]=20 → c=[10,20],        j=1
# i=1,j=1: a[1]=30 <= b[1]=40 → c=[10,20,30],     i=2
# i=2,j=1: a[2]=50 >  b[1]=40 → c=[10,20,30,40],  j=2
# i=2,j=2: a[2]=50 >  b[2]=70? No, 50<=70 → c=[...,50], i=3
# i=3,j=2: a[3]=60 <= b[2]=70 → c=[...,60],       i=4
# i=4: i > n-1, exit first loop. j=2: copy remaining b → c=[...,70]
#
# Result: [10, 20, 30, 40, 50, 60, 70]


# =============================================================================
# SECTION 7: Practice Exercises
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 7: Practice Exercises")
print("=" * 70)

# ----- Exercise 1: Check if array has a pair summing to target -----
# (Same as target_sum_pair, but just True/False instead of counting)

def has_pair_with_sum(arr: list[int], t: int) -> bool:
    arr = sorted(arr)
    i, j = 0, len(arr) - 1
    while i < j:
        s = arr[i] + arr[j]
        if s == t:
            return True
        elif s > t:
            j -= 1
        else:
            i += 1
    return False

print("\n--- Exercise 1: Has Pair With Sum ---")
print(has_pair_with_sum([1, 4, 45, 6, 10, 8], 16))   # True (6+10)
print(has_pair_with_sum([1, 2, 3], 100))              # False


# ----- Exercise 2: Maximum subarray — also return the SUBARRAY, not just the sum -----

def kadane_with_subarray(arr: list[int]) -> tuple[int, list[int]]:
    max_so_far = arr[0]
    x = arr[0]
    start = end = temp_start = 0

    for i in range(1, len(arr)):
        if arr[i] > x + arr[i]:
            x = arr[i]
            temp_start = i        # potential new start of subarray
        else:
            x = x + arr[i]

        if x > max_so_far:
            max_so_far = x
            start = temp_start
            end = i

    return max_so_far, arr[start:end + 1]

print("\n--- Exercise 2: Kadane's with Subarray ---")
result_sum, result_arr = kadane_with_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
print(f"Max sum: {result_sum}, Subarray: {result_arr}")
# Max sum: 6, Subarray: [4, -1, 2, 1]


# ----- Exercise 3: Two Sum — return INDICES (not just count) using a hash map -----
# (Different technique than two-pointers — included because it's the most
#  asked variant of this problem and uses a complementary approach)

def two_sum_indices(arr: list[int], target: int) -> list[int]:
    seen = {}   # value -> index
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print("\n--- Exercise 3: Two Sum (indices, unsorted-friendly) ---")
print(two_sum_indices([2, 7, 11, 15], 9))   # [0, 1]  (2+7=9)


# ----- Exercise 4: Remove duplicates from sorted array using two pointers -----

def remove_duplicates(arr: list[int]) -> int:
    if not arr:
        return 0
    slow = 0   # slow points to the last unique element placed
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1   # new length of the deduplicated portion

print("\n--- Exercise 4: Remove Duplicates ---")
nums = [1, 1, 2, 2, 2, 3, 4, 4, 5]
new_len = remove_duplicates(nums)
print(f"New length: {new_len}, Array: {nums[:new_len]}")
# New length: 5, Array: [1, 2, 3, 4, 5]


# =============================================================================
# SECTION 8: Interview Quick Reference — Two Pointer Patterns
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 8: Quick Reference")
print("=" * 70)

print("""
+--------------------------------+------------------------+------------------+
|  Pattern                       |  Pointer Movement       |  Time / Space   |
+--------------------------------+------------------------+------------------+
|  Pair sum on sorted array      |  Opposite ends, inward  |  O(n) / O(1)    |
|  Container with most water     |  Opposite ends, shorter |  O(n) / O(1)    |
|                                 |  side moves             |                  |
|  Merge two sorted arrays       |  Both start at 0,       |  O(n+m) / O(n+m)|
|                                 |  advance independently  |                  |
|  Remove duplicates (sorted)    |  Slow/fast same          |  O(n) / O(1)    |
|                                 |  direction               |                  |
|  Kadane's max subarray         |  Single pointer +        |  O(n) / O(1)    |
|                                 |  running "reset" logic  |                  |
+--------------------------------+------------------------+------------------+

KEY TAKEAWAYS:
  1. Two pointers from OPPOSITE ends → works on SORTED arrays for pair problems.
  2. Two pointers in the SAME direction (slow/fast) → works for in-place
     compaction (remove duplicates, move zeros, partition).
  3. Always ask: "Can I avoid checking every pair by exploiting sorted order?"
  4. Kadane's is technically a SINGLE pointer with smart state tracking
     ("extend or reset") — it's grouped here because it's the natural
     O(n) endpoint of the array problems explored across this series.
  5. These five patterns (pair sum, container, merge, dedup, Kadane's)
     cover the majority of "Easy" and "Medium" array interview questions.
""")

print("=" * 70)
print("  END OF FILE 11 — Two Pointers & Kadane's Algorithm")
print("=" * 70)
