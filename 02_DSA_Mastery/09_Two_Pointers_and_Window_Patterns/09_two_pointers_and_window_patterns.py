###############################################################################
#            09 - Two Pointers and Window Patterns                             #
###############################################################################
#
# SOURCES:
#   Coding_Python/1. Python - Intro/11_two_pointers_and_kadane.py (564 lines)
#   Coding_Python/1. Python - Intro/12_more_arrays_examples.py (1108 lines)
#   LPLV26MAY/L13 - Intro to Arrays/003targetSumPair.py
#   LPLV26MAY/L13 - Intro to Arrays/004ContainerWithMostWater.py
#   LPLV26MAY/L13 - Intro to Arrays/005ContainerWithMostWaterOptimised.py
#   LPLV26MAY/L13 - Intro to Arrays/006mergeSortedArrays.py
#   LPLV26MAY/L14 - Intro to Arrays/001-004rainwaterTrapping.py
#   LPLV26MAY/L14 - Intro to Arrays/005dnfSort.py
#
# PATTERNS IN THIS MODULE:
#   1.  Opposite-End Convergence (target sum pair, container, rainwater)
#   2.  Same-Direction Fast/Slow (remove duplicates, has_pair_with_sum)
#   3.  Multi-Array Parallel Pointers (merge sorted arrays)
#   4.  Three-Pointer Partition (DNF Sort)
#   5.  Kadane's Extend-or-Reset (max subarray)

from typing import List


# =============================================================================
# SECTION 1: Generate All Pairs — The O(n²) Baseline
# =============================================================================
#
# Every two-pointer problem replaces THIS pattern. Recognise it first.
# Time: O(n²)  — n*(n-1)/2 pairs
# Space: O(1)

def generate_pairs(arr: List[int]) -> List[tuple]:
    """
    Return all pairs (arr[i], arr[j]) where i < j.
    O(n²) — the shape that two pointers optimises away.
    From L13/002generatePairs.py.
    """
    result = []
    n = len(arr)
    for i in range(n - 1):
        for j in range(i + 1, n):
            result.append((arr[i], arr[j]))
    return result

def pairs_demo():
    print("=" * 60)
    print("SECTION 1: Generate All Pairs (O(n²) Baseline)")
    print("=" * 60)
    arr = [10, 20, 30]
    pairs = generate_pairs(arr)
    print(f"\n  arr = {arr}")
    print(f"  All {len(pairs)} pairs: {pairs}")
    n = len(arr)
    print(f"  Formula: n*(n-1)/2 = {n}*{n-1}//2 = {n*(n-1)//2}")
    print(f"  → This is what two-pointer replaces with O(n) per problem")


# =============================================================================
# SECTION 2: Target Sum Pair — Opposite-End Convergence
# =============================================================================
#
# PROBLEM: Given SORTED arr and target t, count pairs (i,j) where arr[i]+arr[j]==t.
#
# BRUTE O(n²): check every pair.
# OPTIMAL O(n): two pointers start at opposite ends, converge inward.
#
# Why it works: At any step:
#   - sum < target: only moving i right (to a bigger value) can help. j left makes worse.
#   - sum > target: only moving j left (to a smaller value) can help. i right makes worse.
#   - sum == target: record match, move BOTH inward.
# Each step eliminates one element permanently. Together, i and j take at most n steps.
#
# Visual convergence for [1,2,3,4,5,6], target=7:
#   i=0,j=5: 1+6=7 == t → MATCH(cnt=1), i++, j--
#   i=1,j=4: 2+5=7 == t → MATCH(cnt=2), i++, j--
#   i=2,j=3: 3+4=7 == t → MATCH(cnt=3), i++, j--
#   i=3,j=2: i >= j → STOP
#   Result: 3 pairs

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
    Optimal two-pointer: O(n) Time, O(1) Space.
    REQUIRES sorted arr. From L13/003targetSumPair.py (optimised version).
    """
    i, j, cnt = 0, len(arr) - 1, 0
    while i < j:
        pair_sum = arr[i] + arr[j]
        if pair_sum == target:
            cnt += 1
            i += 1
            j -= 1
        elif pair_sum > target:
            j -= 1          # sum too big → shrink right end
        else:
            i += 1          # sum too small → grow left end
    return cnt

def has_pair_with_sum(arr: List[int], target: int) -> bool:
    """
    Bool variant: return True if any pair sums to target.
    Sorts internally — works on unsorted input.
    O(n log n) for sort + O(n) for two-pointer = O(n log n) total, O(1) extra.
    """
    arr_sorted = sorted(arr)
    i, j = 0, len(arr_sorted) - 1
    while i < j:
        s = arr_sorted[i] + arr_sorted[j]
        if s == target:
            return True
        elif s > target:
            j -= 1
        else:
            i += 1
    return False

def target_sum_demo():
    print("\n" + "=" * 60)
    print("SECTION 2: Target Sum Pair")
    print("=" * 60)

    arr = [1, 2, 3, 4, 5, 6]
    target = 7
    print(f"\n  arr={arr}, target={target}")

    # Convergence trace
    print(f"\n  Two-pointer trace:")
    i, j = 0, len(arr) - 1
    cnt = 0
    while i < j:
        s = arr[i] + arr[j]
        action = ""
        if s == target:
            cnt += 1
            action = f"MATCH(cnt={cnt}), i++, j--"
            i += 1; j -= 1
        elif s > target:
            action = "too big → j--"
            j -= 1
        else:
            action = "too small → i++"
            i += 1
        print(f"    i={i-1 if 'i++' not in action else i},j={j+1 if 'j--' not in action else j}: "
              f"sum={s}  → {action}")
    print(f"\n  Brute={target_sum_pair_brute(arr, target)}, Optimal={target_sum_pair_optimal(arr, target)}")

    # Has pair
    tests_bool = [([1, 4, 45, 6, 10, 8], 16, True), ([1, 2, 3], 100, False)]
    print(f"\n  has_pair_with_sum tests:")
    for a, t, exp in tests_bool:
        result = has_pair_with_sum(a, t)
        ok = "✓" if result == exp else "✗"
        print(f"    {a}, target={t} → {result}  {ok}")


# =============================================================================
# SECTION 3: Container With Most Water — Opposite-End + Boundary Logic
# =============================================================================
#
# PROBLEM: arr height[], find two lines forming a container holding max water.
# Area = (j - i) * min(height[i], height[j])
#
# BRUTE O(n²): try every pair of lines.
# OPTIMAL O(n): start with max width, shrink toward the center by moving the SHORTER line.
#
# === WHY MOVE THE SHORTER LINE? (Key Interview Insight) ===
# At any position: area = width × min(height[i], height[j]).
# The height is CAPPED by the shorter line (water spills over the short side).
#
# If you move the TALLER line inward:
#   → width decreases by 1
#   → height cap is STILL limited by the same shorter line
#   → area can only get WORSE or equal. This move is provably useless.
#
# If you move the SHORTER line inward:
#   → width decreases by 1
#   → BUT the height cap MIGHT increase if the new line is taller
#   → area might improve.
#
# Conclusion: Only moving the shorter pointer could ever help. Always do it.
# If heights are equal, move either (they're symmetric).
#
# Visual for [1, 8, 6, 2, 5, 4, 8, 3, 7]:
#  i=0,j=8: area=8×min(1,7)=8    h[0]=1 < h[8]=7 → move i (shorter)
#  i=1,j=8: area=7×min(8,7)=49  h[1]=8 > h[8]=7 → move j (shorter)
#  i=1,j=7: area=6×min(8,3)=18  h[7]=3 < h[1]=8 → move j
#  i=1,j=6: area=5×min(8,8)=40  equal → move j
#  ...
#  Answer: 49 ✓

def max_area_brute(height: List[int]) -> int:
    """Brute: O(n²) Time, O(1) Space. From L13/004ContainerWithMostWater.py."""
    n = len(height)
    max_so_far = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            w = j - i
            h = min(height[i], height[j])
            max_so_far = max(max_so_far, w * h)
    return max_so_far

def max_area_optimal(height: List[int]) -> int:
    """
    Optimal two-pointer: O(n) Time, O(1) Space.
    From L13/005ContainerWithMostWaterOptimised.py.
    Always move the pointer at the shorter wall.
    """
    i, j = 0, len(height) - 1
    max_so_far = 0
    while i < j:
        w = j - i
        h = min(height[i], height[j])
        max_so_far = max(max_so_far, w * h)
        if height[i] < height[j]:
            i += 1          # left is shorter → move left
        else:
            j -= 1          # right is shorter (or equal) → move right
    return max_so_far

def container_demo():
    print("\n" + "=" * 60)
    print("SECTION 3: Container With Most Water")
    print("=" * 60)

    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"\n  height = {height}")
    print(f"  Brute:   {max_area_brute(height)}")
    print(f"  Optimal: {max_area_optimal(height)}")

    # Step trace
    print(f"\n  Two-pointer step trace:")
    i, j = 0, len(height) - 1
    max_so_far = 0
    step = 0
    while i < j:
        w = j - i
        h = min(height[i], height[j])
        area = w * h
        max_so_far = max(max_so_far, area)
        move = f"h[{i}]={height[i]} < h[{j}]={height[j]} → i++" if height[i] < height[j] else f"h[{j}]={height[j]} ≤ h[{i}]={height[i]} → j--"
        print(f"    [{step}] i={i},j={j}: w={w}, h={h}, area={area}, max={max_so_far}  |  {move}")
        if height[i] < height[j]:
            i += 1
        else:
            j -= 1
        step += 1
        if step > 8: print("    ..."); break

    # Edge cases
    tests = [
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
    ]
    print(f"\n  Edge case verification:")
    for h, expected in tests:
        result = max_area_optimal(h)
        ok = "✓" if result == expected else "✗"
        print(f"    {h} → {result}  (expected {expected}) {ok}")


# =============================================================================
# SECTION 4: Rainwater Trapping — 4-Step Evolution
# =============================================================================
#
# PROBLEM: Given height[] (building heights), compute total trapped water.
#
# Core formula: water at building i = min(l[i], r[i]) - height[i]
#   l[i] = max height from LEFT up to and including i
#   r[i] = max height from RIGHT down to and including i
#   Why min? Water level = shorter containing wall. Why subtract h[i]? Building takes space.
#   wi >= 0 guaranteed: l[i] and r[i] include height[i], so min >= height[i].
#
# ============================================================
# SOLUTION 1 (Brute Force) — O(n²) Time, O(1) Space
# ============================================================
# For each building i, scan all the way LEFT to find l[i], all the way RIGHT for r[i].
# Two nested loops per building. From L14/001rainwaterTrapping.py.

def trap_brute(height: List[int]) -> int:
    """
    Brute force: O(n²) Time, O(1) Space.
    Re-scan left and right for EVERY building — very inefficient.
    """
    n = len(height)
    ans = 0
    for i in range(n):
        li = height[i]
        for j in range(i - 1, -1, -1):      # scan left from i
            li = max(li, height[j])
        ri = height[i]
        for j in range(i + 1, n):           # scan right from i
            ri = max(ri, height[j])
        ans += min(li, ri) - height[i]
    return ans

# ============================================================
# SOLUTION 2 — O(n) Time, O(n) Space  (precompute both l[] and r[])
# ============================================================
# Observation: we're re-scanning the same elements in trap_1.
# Pre-compute ALL l[i] in ONE left-to-right pass using:
#   l[i] = max(l[i-1], height[i])  ← O(1) per step, not a scan
# Pre-compute ALL r[i] in ONE right-to-left pass similarly.
# Then compute water in a third pass. Total: 3n operations = O(n).
# From L14/002rainwaterTrapping2.py.

def trap_prefix_suffix(height: List[int]) -> int:
    """
    Prefix/suffix arrays: O(n) Time, O(n) Space.
    Three passes: build l[], build r[], compute water.
    """
    n = len(height)
    if n <= 2: return 0

    l = [0] * n
    l[0] = height[0]
    for i in range(1, n):
        l[i] = max(l[i - 1], height[i])    # include height[i] itself

    r = [0] * n
    r[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        r[i] = max(r[i + 1], height[i])    # include height[i] itself

    ans = 0
    for i in range(n):
        ans += min(l[i], r[i]) - height[i]
    return ans

# ============================================================
# SOLUTION 3 — O(n) Time, O(n) Space  (drop l[], compute left on-the-fly)
# ============================================================
# We scan left→right in pass 3 anyway. Merge pass 1 (building l[]) into
# pass 3 using a single max_so_far variable instead of the full array.
# Still need r[] precomputed (we need r[i] in the forward pass).
# Space improvement: one array instead of two (but still O(n)).
# From L14/003rainwaterTrapping3.py.

def trap_one_array(height: List[int]) -> int:
    """
    Half-space: O(n) Time, O(n) Space.
    Precompute r[] only; compute left max on-the-fly with max_so_far.
    """
    n = len(height)
    if n <= 2: return 0

    r = [0] * n
    r[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        r[i] = max(r[i + 1], height[i])

    ans = 0
    max_so_far = 0                          # this replaces l[] — the running left max
    for i in range(n):
        max_so_far = max(max_so_far, height[i])
        ans += min(max_so_far, r[i]) - height[i]
    return ans

# ============================================================
# SOLUTION 4 (Best) — O(n) Time, O(1) Space  — Two Pointers
# ============================================================
# Question: Solution 3 still needs O(n) for r[]. Can we eliminate it?
#
# Key insight: We don't need the EXACT value of r[i]. We just need to know
# which side is the LIMITING wall.
#
# Two pointers: i from left, j from right.
# l = running max seen so far from the LEFT (including height[i])
# r = running max seen so far from the RIGHT (including height[j])
#
# Decision rule:
#   If l < r:
#     Left wall is the limiting factor for building i.
#     The TRUE right max >= r >= l, so min(l, true_r) = l.
#     Therefore wi = l - height[i] is EXACT (not an approximation).
#     We never needed to know the exact right array value.
#     Advance i.
#
#   If r <= l:
#     Right wall is the limiting factor for building j by symmetric argument.
#     wj = r - height[j] is EXACT.
#     Advance j.
#
# Initialise l=0, r=0 (not height[0], height[n-1]).
# Update l and r FIRST at the START of each iteration, then compute water.
# From L14/004rainwaterTrapping4.py.

def trap_two_pointer(height: List[int]) -> int:
    """
    Optimal two-pointer: O(n) Time, O(1) Space.
    The definitive solution. From L14/004rainwaterTrapping4.py.
    """
    n = len(height)
    if n <= 2: return 0

    i, j = 0, n - 1
    l, r = 0, 0                             # running max from left and right
    ans = 0

    while i <= j:
        l = max(l, height[i])               # update BEFORE computing water
        r = max(r, height[j])               # update BEFORE computing water

        if l < r:
            # Left wall shorter → wi is exact
            ans += l - height[i]
            i += 1
        else:
            # Right wall shorter (or equal) → wj is exact
            ans += r - height[j]
            j -= 1

    return ans

def rainwater_demo():
    print("\n" + "=" * 60)
    print("SECTION 4: Rainwater Trapping — 4-Step Evolution")
    print("=" * 60)

    test_cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([3, 0, 2, 0, 4], 7),
        ([4, 2, 0, 3, 2, 5], 9),
        ([1, 0, 1], 1),
        ([3, 1, 2, 4], 2),
    ]

    print(f"\n  {'heights':<45} {'B':>5} {'P/S':>5} {'1A':>5} {'2P':>5} {'Exp':>5}")
    print("  " + "-" * 70)
    for h, expected in test_cases:
        b  = trap_brute(h)
        ps = trap_prefix_suffix(h)
        oa = trap_one_array(h)
        tp = trap_two_pointer(h)
        ok = "✓" if tp == expected else "✗"
        all_agree = "✓" if b == ps == oa == tp else "✗ MISMATCH"
        print(f"  {str(h):<45} {b:>5} {ps:>5} {oa:>5} {tp:>5} {expected:>5} {ok} {all_agree}")

    # Detailed column trace for [3, 0, 2, 0, 4]
    h = [3, 0, 2, 0, 4]
    n = len(h)
    l_arr = [0]*n; l_arr[0] = h[0]
    for i in range(1, n): l_arr[i] = max(l_arr[i-1], h[i])
    r_arr = [0]*n; r_arr[n-1] = h[n-1]
    for i in range(n-2, -1, -1): r_arr[i] = max(r_arr[i+1], h[i])
    print(f"\n  Detailed column trace for {h}:")
    print(f"  {'i':>3}  {'h[i]':>5}  {'l[i]':>6}  {'r[i]':>6}  {'min(l,r)':>9}  {'wi':>5}")
    print("  " + "-" * 43)
    total = 0
    for i in range(n):
        wi = min(l_arr[i], r_arr[i]) - h[i]
        total += wi
        print(f"  {i:>3}  {h[i]:>5}  {l_arr[i]:>6}  {r_arr[i]:>6}  {min(l_arr[i],r_arr[i]):>9}  {wi:>5}")
    print(f"  Total = {total}  ✓")

    # Two-pointer step trace
    h2 = [3, 0, 2, 0, 4]
    print(f"\n  Two-pointer step trace for {h2}:")
    i, j = 0, len(h2) - 1
    l = r = ans = 0
    print(f"  {'step':>5}  {'i':>3}  {'j':>3}  {'l':>4}  {'r':>4}  {'wi/wj':>6}  {'ans':>5}")
    print("  " + "-" * 42)
    step = 0
    while i <= j:
        l = max(l, h2[i])
        r = max(r, h2[j])
        if l < r:
            wi = l - h2[i]
            ans += wi
            print(f"  {step:>5}  {i:>3}  {j:>3}  {l:>4}  {r:>4}  wi={wi:>4}  {ans:>5}  (i++)")
            i += 1
        else:
            wj = r - h2[j]
            ans += wj
            print(f"  {step:>5}  {i:>3}  {j:>3}  {l:>4}  {r:>4}  wj={wj:>4}  {ans:>5}  (j--)")
            j -= 1
        step += 1
    print(f"  Final ans = {ans}  ✓")

    # Summary table
    print(f"""
  Progression Summary:
  ┌──────────────┬──────────┬─────────┬────────────────────────────────────────┐
  │  Solution    │  Time    │  Space  │  Key Idea                               │
  ├──────────────┼──────────┼─────────┼────────────────────────────────────────┤
  │  trap_brute  │  O(n²)   │  O(1)   │  Re-scan left+right for every building │
  │  trap_ps     │  O(n)    │  O(n)   │  Precompute both l[] and r[] arrays    │
  │  trap_oa     │  O(n)    │  O(n)   │  Drop l[]; compute left max on-the-fly │
  │  trap_tp ✓   │  O(n)    │  O(1)   │  Two pointers; drop r[] too — BEST     │
  └──────────────┴──────────┴─────────┴────────────────────────────────────────┘
    """)


# =============================================================================
# SECTION 5: Merge Two Sorted Arrays — Parallel Multi-Array Pointers
# =============================================================================
#
# PROBLEM: Merge two sorted arrays a and b into one sorted array c.
# This is the core building block of Merge Sort.
#
# Three pointers: i walks a, j walks b, k fills c.
# At each step: compare a[i] and b[j], take the smaller into c[k], advance that pointer.
# When one pointer exhausts its array, copy the remaining elements from the other.
# Only ONE of the two tail-copy while loops will run.
#
# Walkthrough for a=[10,30,50,60], b=[20,40,70]:
#   i=0,j=0: 10 ≤ 20 → c=[10],         i=1
#   i=1,j=0: 30 > 20 → c=[10,20],       j=1
#   i=1,j=1: 30 ≤ 40 → c=[10,20,30],    i=2
#   i=2,j=1: 50 > 40 → c=[10,20,30,40], j=2
#   i=2,j=2: 50 ≤ 70 → c=[...,50],      i=3
#   i=3,j=2: 60 ≤ 70 → c=[...,60],      i=4
#   i exhausted → copy b[2]=70 → [10,20,30,40,50,60,70] ✓
#
# Time: O(n+m) — each element visited exactly once.
# Space: O(n+m) — the merged array c.
# From L13/006mergeSortedArrays.py.

def merge_sorted_arrays(a: List[int], b: List[int]) -> List[int]:
    """
    Merge two sorted arrays. Time: O(n+m), Space: O(n+m).
    """
    n, m = len(a), len(b)
    c = [0] * (n + m)
    i = j = k = 0

    while i < n and j < m:
        if a[i] <= b[j]:
            c[k] = a[i]; i += 1
        else:
            c[k] = b[j]; j += 1
        k += 1

    # Tail-copy: only ONE of these runs
    while i < n:
        c[k] = a[i]; i += 1; k += 1
    while j < m:
        c[k] = b[j]; j += 1; k += 1

    return c

def merge_demo():
    print("\n" + "=" * 60)
    print("SECTION 5: Merge Two Sorted Arrays")
    print("=" * 60)

    a = [10, 30, 50, 60]
    b = [20, 40, 70]
    print(f"\n  a = {a}")
    print(f"  b = {b}")

    # Step trace
    print(f"\n  Step-by-step trace:")
    n, m = len(a), len(b)
    c = [0] * (n + m)
    i = j = k = 0
    while i < n and j < m:
        if a[i] <= b[j]:
            action = f"a[{i}]={a[i]} ≤ b[{j}]={b[j]} → take a"
            c[k] = a[i]; i += 1
        else:
            action = f"a[{i}]={a[i]} > b[{j}]={b[j]} → take b"
            c[k] = b[j]; j += 1
        print(f"    k={k}: {action}")
        k += 1
    while i < n:
        print(f"    k={k}: a exhausted, copy b[{j}]... actually copy remaining a")
        c[k] = a[i]; i += 1; k += 1
    while j < m:
        print(f"    k={k}: b remaining, copy b[{j}]={b[j]}")
        c[k] = b[j]; j += 1; k += 1

    result = merge_sorted_arrays(a, b)
    print(f"\n  Merged: {result}")

    tests = [
        ([1, 3, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3], [], [1, 2, 3]),
        ([], [4, 5], [4, 5]),
    ]
    print(f"\n  Verification:")
    for a_t, b_t, expected in tests:
        result_t = merge_sorted_arrays(a_t, b_t)
        ok = "✓" if result_t == expected else "✗"
        print(f"    merge({a_t}, {b_t}) = {result_t}  {ok}")


# =============================================================================
# SECTION 6: Remove Duplicates (Sorted) — Fast/Slow Same-Direction
# =============================================================================
#
# PROBLEM: Given SORTED arr, remove duplicates in-place. Return count of unique elements.
#
# Slow marks the last confirmed-unique position.
# Fast scouts ahead for new unique values.
# When fast finds arr[fast] != arr[slow], slow advances and overwrites with arr[fast].
#
# Visual trace for [1,1,2,2,2,3]:
#   arr = [1, 1, 2, 2, 2, 3]
#          s
#             f               arr[f]=arr[s]=1 → skip (f++)
#                f             arr[f]=2 != arr[s]=1 → s++, arr[s]=2
#          s        f
#                      f       dup → skip
#                         f    dup → skip
#                            f arr[f]=3 != arr[s]=2 → s++, arr[s]=3
#                s           f (f past end)
#   arr[:s+1] = [1, 2, 3]  ← unique elements

def remove_duplicates_optimal(arr: List[int]) -> int:
    """
    Fast/slow two pointers: O(n) Time, O(1) Space.
    Works on sorted arrays. Returns count of unique elements.
    """
    if not arr:
        return 0
    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1

def remove_dup_demo():
    print("\n" + "=" * 60)
    print("SECTION 6: Remove Duplicates (Sorted) — Fast/Slow Pointers")
    print("=" * 60)

    # Step trace
    arr = [1, 1, 2, 2, 2, 3]
    print(f"\n  arr = {arr}")
    print(f"\n  Trace (slow=s, fast=f):")
    print(f"  {'fast':>5}  {'arr[fast]':>10}  {'arr[slow]':>10}  {'action':>25}  {'arr (current)':>25}")
    print("  " + "-" * 80)

    demo = arr[:]
    slow = 0
    for fast in range(1, len(demo)):
        action = ""
        if demo[fast] != demo[slow]:
            slow += 1
            demo[slow] = demo[fast]
            action = f"NEW: s++={slow}, arr[s]={demo[fast]}"
        else:
            action = f"DUP: skip"
        print(f"  {fast:>5}  {demo[fast]:>10}  {demo[slow-1 if action.startswith('N') else slow]:>10}  {action:>25}  {demo}")

    count = remove_duplicates_optimal(arr[:])
    print(f"\n  unique count = {count}, unique elements = {arr[:count]}")

    tests = [
        ([1, 1, 2, 2, 3, 3, 3, 4], 4, [1, 2, 3, 4]),
        ([1, 1, 1, 1], 1, [1]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([], 0, []),
    ]
    print(f"\n  Verification:")
    for a, exp_count, exp_arr in tests:
        a_copy = a[:]
        cnt = remove_duplicates_optimal(a_copy)
        ok = "✓" if cnt == exp_count and a_copy[:cnt] == exp_arr else "✗"
        print(f"    {a} → count={cnt}, unique={a_copy[:cnt]}  {ok}")


# =============================================================================
# SECTION 7: DNF Sort (Dutch National Flag) — Three-Pointer Partition
# =============================================================================
#
# PROBLEM: Given arr of only {0, 1, 2}, sort it in-place in O(n), O(1).
# Named after the Dutch flag which has three coloured bands.
#
# Three-pointer invariant — at all times, the array has four regions:
#   [ 0..low-1 ] [ low..mid-1 ] [ mid..high ] [ high+1..n-1 ]
#      zeros          ones         unknown         twos
#
# Three cases for arr[mid]:
#   0: swap(arr[low], arr[mid]), low++, mid++
#      (element from arr[low] was already processed — safe to advance mid)
#   1: mid++ (1 is already in the "ones" region — nothing to do)
#   2: swap(arr[mid], arr[high]), high--
#      (DO NOT advance mid — element from arr[high] is unknown, must examine it)
#
# From L14/005dnfSort.py.
# Time: O(n) — mid advances monotonically, high decreases monotonically.
# Space: O(1) — in-place swaps.

def dnf_sort(nums: List[int]) -> None:
    """
    Dutch National Flag sort: O(n) Time, O(1) Space.
    Sorts array of 0s, 1s, 2s in a single pass.
    From L14/005dnfSort.py — identical logic.
    """
    n = len(nums)
    low, mid, high = 0, 0, n - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:   # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            # DO NOT advance mid — swapped-in element is unknown

def dnf_demo():
    print("\n" + "=" * 60)
    print("SECTION 7: DNF Sort (Dutch National Flag)")
    print("=" * 60)

    # Live trace
    nums = [2, 0, 2, 1, 1, 0]
    print(f"\n  Input: {nums}")
    print(f"\n  Trace (invariant: [zeros | ones | unknown | twos]):")
    arr = nums[:]
    n = len(arr)
    low, mid, high = 0, 0, n - 1
    step = 0
    print(f"  {'step':>5}  {'low':>4}  {'mid':>4}  {'high':>5}  {'arr[mid]':>9}  {'action':>20}  {'arr':>25}")
    print("  " + "-" * 78)
    while mid <= high:
        val = arr[mid]
        if val == 0:
            action = f"0→swap(low,mid),low++,mid++"
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1; mid += 1
        elif val == 1:
            action = f"1→mid++"
            mid += 1
        else:
            action = f"2→swap(mid,high),high--"
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
        print(f"  {step:>5}  {low:>4}  {mid:>4}  {high:>5}  {val:>9}  {action:>20}  {arr}")
        step += 1

    result = nums[:]
    dnf_sort(result)
    print(f"\n  Final: {result}")

    tests = [
        ([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]),
        ([0], [0]),
        ([1, 0, 2], [0, 1, 2]),
        ([0, 0, 0], [0, 0, 0]),
        ([2, 2, 2], [2, 2, 2]),
    ]
    print(f"\n  Verification:")
    for n_in, expected in tests:
        n_copy = n_in[:]
        dnf_sort(n_copy)
        ok = "✓" if n_copy == expected else "✗"
        print(f"    {n_in} → {n_copy}  {ok}")


# =============================================================================
# SECTION 8: Kadane's Algorithm — Maximum Subarray Sum
# =============================================================================
#
# PROBLEM: Find the contiguous subarray with the maximum sum.
# Example: [-2, 1, -3, 4, -1, 2, 1, -5, 4] → 6 (subarray [4,-1,2,1])
#
# FROM THE PROGRESSION (Coding_Python/11 §4 and §7):
#   Brute force (3 loops):           O(n³) Time, O(1) Space
#   Optimised brute (extend sum):    O(n²) Time, O(1) Space
#   Prefix sum + all pairs:          O(n²) Time, O(n) Space
#   Kadane's (with x[] array):       O(n)  Time, O(n) Space
#   Kadane's (single variable):      O(n)  Time, O(1) Space  ← BEST
#
# Core idea at each index i: ask "Should I extend the previous subarray, or start fresh?"
#   x = max(x + arr[i], arr[i])
#   If the running sum x is negative, it can only DRAG DOWN future subarrays.
#   Reset to arr[i] — start a brand-new subarray here.
#
# Visual trace for [-2, 1, -3, 4, -1, 2, 1, -5, 4]:
#   arr:    -2    1   -3    4   -1    2    1   -5    4
#   x:      -2    1   -2    4    3    5    6    1    5
#             |   |reset|reset|extend...............|
#   max:    -2    1    1    4    4    5    6    6    6
#   Best subarray: [4, -1, 2, 1] = 6

def kadane_array(arr: List[int], n: int) -> int:
    """
    Kadane's with x[] array (educational): O(n) Time, O(n) Space.
    x[i] = max subarray sum ending EXACTLY at index i.
    """
    x = [0] * n
    x[0] = arr[0]
    max_so_far = x[0]
    for i in range(1, n):
        x[i] = max(x[i - 1] + arr[i], arr[i])
        max_so_far = max(max_so_far, x[i])
    return max_so_far

def kadane_optimal(arr: List[int]) -> int:
    """
    Kadane's single-variable: O(n) Time, O(1) Space.
    x[i] only depends on x[i-1] → replace array with single variable.
    THE answer interviewers expect.
    """
    x = arr[0]
    max_so_far = x
    for i in range(1, len(arr)):
        x = max(x + arr[i], arr[i])
        max_so_far = max(max_so_far, x)
    return max_so_far

def kadane_with_subarray(arr: List[int]) -> tuple:
    """
    Kadane's + track actual subarray: O(n) Time, O(1) Space.
    Returns (max_sum, subarray).
    From Coding_Python/11 §7 Exercise 2.
    """
    x = arr[0]
    max_so_far = x
    start = end = temp_start = 0

    for i in range(1, len(arr)):
        if arr[i] > x + arr[i]:
            x = arr[i]
            temp_start = i              # potential new start
        else:
            x = x + arr[i]

        if x > max_so_far:
            max_so_far = x
            start = temp_start
            end = i

    return max_so_far, arr[start:end + 1]

def kadane_demo():
    print("\n" + "=" * 60)
    print("SECTION 8: Kadane's Algorithm — Max Subarray Sum")
    print("=" * 60)

    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    n = len(arr)
    print(f"\n  arr = {arr}")

    # Step trace
    print(f"\n  Step trace:")
    print(f"  {'i':>3}  {'arr[i]':>7}  {'x (extend)':>12}  {'x (reset)':>11}  {'x (chosen)':>11}  {'max':>6}")
    print("  " + "-" * 60)
    x = arr[0]; max_sf = x
    print(f"  {0:>3}  {arr[0]:>7}  {'—':>12}  {'—':>11}  {x:>11}  {max_sf:>6}  (base case)")
    for i in range(1, n):
        extend = x + arr[i]
        reset  = arr[i]
        x = max(extend, reset)
        max_sf = max(max_sf, x)
        tag = "reset" if reset > extend else "extend"
        print(f"  {i:>3}  {arr[i]:>7}  {extend:>12}  {reset:>11}  {x:>11}  {max_sf:>6}  ({tag})")

    print(f"\n  kadane_array:     {kadane_array(arr, n)}")
    print(f"  kadane_optimal:   {kadane_optimal(arr)}")
    ms, sub = kadane_with_subarray(arr)
    print(f"  with subarray:    sum={ms}, subarray={sub}")

    # Edge cases
    tests = [
        ([-3, -1, -2], -1),             # all negative: pick least negative
        ([1], 1),
        ([5, -4, 8], 9),
        ([-2, -3, 4, -1, -2, 1, 5, -3], 7),
    ]
    print(f"\n  Edge case verification:")
    for a, expected in tests:
        result = kadane_optimal(a)
        ok = "✓" if result == expected else "✗"
        print(f"    {a} → {result}  (expected {expected}) {ok}")


# =============================================================================
# PRACTICE SKELETONS — Implement using the OPTIMAL approach
# =============================================================================

def practice_target_sum_pair(arr: List[int], target: int) -> int:
    """
    Count pairs (i,j) in sorted arr where arr[i]+arr[j]==target.
    Time: O(n) | Space: O(1)
    Hint: i=0, j=n-1; sum<target→i++; sum>target→j--; sum==target→cnt++,i++,j--
    """
    pass

def practice_max_area(height: List[int]) -> int:
    """
    Max water area between two lines. area = width * min(h[i], h[j]).
    Time: O(n) | Space: O(1)
    Hint: start wide; move the shorter pointer inward each step.
    """
    pass

def practice_trap_water(height: List[int]) -> int:
    """
    Total trapped rainwater (two-pointer O(1) space solution).
    Time: O(n) | Space: O(1)
    Hint: l=r=0; update l/r first; if l<r: ans+=l-h[i], i++; else: ans+=r-h[j], j--
    """
    pass

def practice_merge_sorted_arrays(a: List[int], b: List[int]) -> List[int]:
    """
    Merge two sorted arrays into one sorted array.
    Time: O(n+m) | Space: O(n+m)
    Hint: three pointers i,j,k; always take the smaller current element.
    """
    pass

def practice_remove_duplicates(arr: List[int]) -> int:
    """
    Remove duplicates from sorted array in-place. Return unique count.
    Time: O(n) | Space: O(1)
    Hint: slow=0; for fast in range(1,n): if arr[fast]!=arr[slow]: slow++, arr[slow]=arr[fast]
    """
    pass

def practice_dnf_sort(nums: List[int]) -> None:
    """
    Sort array of {0,1,2} in-place. No use of sort().
    Time: O(n) | Space: O(1)
    Hint: low=mid=0, high=n-1; three cases for nums[mid].
    """
    pass

def practice_kadane(arr: List[int]) -> int:
    """
    Maximum subarray sum (contiguous).
    Time: O(n) | Space: O(1)
    Hint: x=arr[0]; for i in 1..n: x=max(x+arr[i], arr[i]); track max_so_far.
    """
    pass

def practice_has_pair(arr: List[int], target: int) -> bool:
    """
    Return True if any two elements sum to target. Array may be unsorted.
    Time: O(n log n) | Space: O(1)
    Hint: sort first, then two pointers.
    """
    pass


# =============================================================================
# DRIVER CODE — Verifies optimal implementations, then prints skeleton stubs
# =============================================================================
if __name__ == "__main__":
    pairs_demo()
    target_sum_demo()
    container_demo()
    rainwater_demo()
    merge_demo()
    remove_dup_demo()
    dnf_demo()
    kadane_demo()

    print("\n" + "=" * 60)
    print("OPTIMAL SOLUTION VERIFICATION")
    print("=" * 60)

    # Target sum pair
    tsp = target_sum_pair_optimal([1, 2, 3, 4, 5, 6], 7)
    assert tsp == 3, f"Target sum pair failed: {tsp}"
    print(f"\n  target_sum_pair([1..6], 7)        = {tsp} ✓")

    tsp2 = target_sum_pair_optimal([1, 2, 3, 4, 5, 6], 100)
    assert tsp2 == 0, f"Target sum pair (no match) failed: {tsp2}"
    print(f"  target_sum_pair([1..6], 100)       = {tsp2} ✓")

    # Has pair
    hp1 = has_pair_with_sum([1, 4, 45, 6, 10, 8], 16)
    hp2 = has_pair_with_sum([1, 2, 3], 100)
    assert hp1 == True and hp2 == False
    print(f"  has_pair([..], 16)                 = {hp1} ✓")
    print(f"  has_pair([1,2,3], 100)             = {hp2} ✓")

    # Container
    ca = max_area_optimal([1, 8, 6, 2, 5, 4, 8, 3, 7])
    assert ca == 49, f"Container failed: {ca}"
    print(f"  max_area([1,8,6,2,5,4,8,3,7])      = {ca} ✓")

    # Rainwater — all 4 solutions agree
    h = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    rb  = trap_brute(h)
    rps = trap_prefix_suffix(h)
    roa = trap_one_array(h)
    rtp = trap_two_pointer(h)
    assert rb == rps == roa == rtp == 6
    print(f"  trap([0,1,0,2,1,0,1,3,2,1,2,1])   = {rtp} ✓ (all 4 agree)")

    # Merge
    mg = merge_sorted_arrays([1, 3, 5], [2, 4, 6])
    assert mg == [1, 2, 3, 4, 5, 6], f"Merge failed: {mg}"
    print(f"  merge([1,3,5], [2,4,6])            = {mg} ✓")

    # Remove duplicates
    arr_rd = [1, 1, 2, 2, 3]
    cnt_rd = remove_duplicates_optimal(arr_rd)
    assert cnt_rd == 3 and arr_rd[:3] == [1, 2, 3]
    print(f"  remove_dup([1,1,2,2,3])            = count={cnt_rd}, {arr_rd[:cnt_rd]} ✓")

    # DNF
    arr_dnf = [2, 0, 2, 1, 1, 0]
    dnf_sort(arr_dnf)
    assert arr_dnf == [0, 0, 1, 1, 2, 2]
    print(f"  dnf_sort([2,0,2,1,1,0])            = {arr_dnf} ✓")

    # Kadane
    kd = kadane_optimal([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert kd == 6, f"Kadane failed: {kd}"
    print(f"  kadane([-2,1,-3,4,-1,2,1,-5,4])    = {kd} ✓")

    kd_neg = kadane_optimal([-3, -1, -2])
    assert kd_neg == -1
    print(f"  kadane([-3,-1,-2])                 = {kd_neg} ✓  (all negative)")

    ms, sub = kadane_with_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert ms == 6 and sub == [4, -1, 2, 1]
    print(f"  kadane_with_subarray               = sum={ms}, arr={sub} ✓")

    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS (return None until implemented)")
    print("=" * 60)
    print(f"\n  practice_target_sum_pair([1..6], 7)  = {practice_target_sum_pair([1,2,3,4,5,6], 7)}")
    print(f"  practice_max_area([1,8,6,2,5,4,8,3,7]) = {practice_max_area([1,8,6,2,5,4,8,3,7])}")
    print(f"  practice_trap_water([0,1,0,2,...])     = {practice_trap_water([0,1,0,2,1,0,1,3,2,1,2,1])}")
    print(f"  practice_merge([1,3,5], [2,4,6])       = {practice_merge_sorted_arrays([1,3,5], [2,4,6])}")
    arr_sk = [1, 1, 2, 2, 3]
    cnt_sk = practice_remove_duplicates(arr_sk)
    print(f"  practice_remove_dup([1,1,2,2,3])       = count={cnt_sk}")
    arr_dnf_sk = [2, 0, 2, 1, 1, 0]
    practice_dnf_sort(arr_dnf_sk)
    print(f"  practice_dnf_sort([2,0,2,1,1,0])       = {arr_dnf_sk}")
    print(f"  practice_kadane([-2,1,-3,4,-1,2,1,-5,4]) = {practice_kadane([-2,1,-3,4,-1,2,1,-5,4])}")
    print(f"  practice_has_pair([1,4,45,6,10,8], 16)  = {practice_has_pair([1,4,45,6,10,8], 16)}")
    print("=" * 60)
    print("Fill in the skeletons above and re-run to verify.")
