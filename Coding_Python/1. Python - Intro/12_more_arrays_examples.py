###############################################################################
#                    More Array Problems — Patterns & Techniques               #
###############################################################################

"""
Each problem below builds on concepts already covered:
  - Sorting           (file 09)
  - Binary Search     (file 10)
  - Prefix/Suffix     (file 10)
  - Kadane's Algorithm(file 11)
  - Two Pointers      (file 11)

Problems in this file:
  Section 1:  Maximum Product of a Triplet
  Section 2:  Maximum Circular Subarray Sum
  Section 3:  Counting Smaller Elements (two sorted arrays)
  Section 4:  Rain-Water Trapping
  Section 5:  Product of Array Except Self
  Section 6:  DNF Sort (Dutch National Flag)
  Section 7:  Counting Sort
  Section 8:  Generalized Counting Sort
"""

"""
Here's a quick summary of the core concept behind each problem — 
the "one sentence intuition" for each:

Problem:	                            The key trick
Max Product Triplet:	After sorting, only 2 candidates matter — 3 biggest, or 2 most-negative × biggest

Circular Subarray Sum: 	A wrapping subarray = total − the minimum subarray in the middle

Counting Smaller Elements:	Array B is sorted, so binary search tells you the count in O(log n) instead of scanning

Rain-Water Trapping:	Water at each spot = shorter of (tallest-left, tallest-right) minus the building height

Product Except Self: 	Build left-products in one pass, multiply by right-products in a second pass — no division

DNF Sort:	Three pointers carve out three zones (0s, unknowns, 2s) and shrink the unknown zone

Counting Sort: 	Don't compare — just count how many times each value appears, then reconstruct

Generalized Counting Sort: 	Shift values so the range starts at 0, apply counting sort, shift back

"""


# =============================================================================
# SECTION 1: Maximum Product of a Triplet
# =============================================================================

# ----- Problem -----
# Given an array of N integers (can include negatives), find the maximum
# product you can get by multiplying any 3 elements.
#
# Example:  arr = [-10, -10, 1, 3, 2]
# Answer:   (-10) × (-10) × 3 = 300   ← two negatives make a positive!
#
# ----- Why is this not trivial? -----
# If all numbers were positive, the answer would simply be the 3 largest.
# But NEGATIVE numbers change everything.
# Negative × Negative = Positive.
# So two large negatives multiplied by the largest positive can beat
# the product of the three largest positives.
#
# ----- Key Insight: Only Two Candidates -----
# After sorting, there are exactly TWO possible answers:
#
#   Candidate A:  arr[n-1] × arr[n-2] × arr[n-3]
#                 (the three largest elements)
#
#   Candidate B:  arr[0] × arr[1] × arr[n-1]
#                 (two smallest, which may be large negatives, × the largest)
#
# The true maximum is whichever is bigger.
# No other combination can beat these two.
#
# Why not consider other pairs of negatives?
#   arr[0] × arr[2] would give a smaller product than arr[0] × arr[1]
#   because arr[1] ≤ arr[2] in a sorted array — and since both are likely
#   negative, arr[1] is MORE negative → larger absolute value → bigger product.
#   So the most extreme pair is always arr[0] and arr[1].
#
# ----- Visual Walkthrough -----
#
#   arr = [-10, -10, 1, 3, 2]
#   After sorting: [-10, -10, 1, 2, 3]
#
#     idx:    0    1   2  3  4
#            [-10,-10,  1, 2, 3]
#              ↑   ↑            ↑
#             arr[0] arr[1]   arr[4] (largest)
#
#   Candidate A: arr[4] × arr[3] × arr[2] = 3 × 2 × 1 = 6
#   Candidate B: arr[0] × arr[1] × arr[4] = -10 × -10 × 3 = 300
#
#   Answer: max(6, 300) = 300  ✓
#
# ----- Brute Force: O(n³) -----
# Try all combinations of 3 elements and track the maximum.
# For n=1000, that's ~166 million checks — too slow.
#
# ----- Optimal: O(n log n) -----
# Sort + check exactly 2 candidates.
# For n=1,000,000, sorting takes ~20M operations — fast.

def max_product_triplet(arr: list[int]) -> int:
    arr.sort()                          # O(n log n)
    n = len(arr)

    candidate_a = arr[n-1] * arr[n-2] * arr[n-3]   # three largest
    candidate_b = arr[0]   * arr[1]   * arr[n-1]   # two smallest × largest

    return max(candidate_a, candidate_b)


# --- Examples ---
print("===== SECTION 1: Max Product of a Triplet =====")
print(max_product_triplet([-10, -10, 1, 3, 2]))  # 300
print(max_product_triplet([1, 2, 3, 4, 5]))       # 60  (3×4×5)
print(max_product_triplet([-5, -4, -3, -2, -1]))  # -6  (-3×-2×-1, all negative)


# =============================================================================
# SECTION 2: Maximum Circular Subarray Sum
# =============================================================================

# ----- Problem -----
# Given an array of N integers arranged in a CIRCLE, find the subarray
# (contiguous sequence) with the maximum sum. The subarray can wrap around
# from the end back to the beginning.
#
# Example:
#   arr = [5, -3, 5]
#   Normal max subarray:  5 + (-3) + 5 = 7  (no wrap)
#   Circular max subarray: 5 + 5 = 10        (wrap: index 2 then index 0)
#   Answer: 10
#
# ----- What does "circular" mean? -----
# Imagine the array printed on a circular ring:
#
#         5
#       ↗   ↘
#     5       -3
#
# You can start reading from any position and wrap around.
# "5, 5" (taking index 2 and index 0) is a valid subarray here.
#
# ----- Key Insight: Two Cases -----
#
# Any circular subarray falls into one of two cases:
#
#   Case 1 — Does NOT wrap around:
#     This is just a normal max subarray problem → Kadane's Algorithm (file 11).
#
#   Case 2 — DOES wrap around:
#     The elements selected are at BOTH ends of the array.
#     The elements NOT selected form a contiguous block in the MIDDLE.
#
#     Visual:
#       [  selected  | not selected |  selected  ]
#        ^^^^^^^^^^^   ^^^^^^^^^^^^   ^^^^^^^^^^^
#        left part     middle part    right part
#
#     So:  circular_sum = total_sum - sum(middle part)
#     To maximise circular_sum, we minimise the middle part.
#     The middle part is a contiguous subarray → find the MINIMUM subarray sum.
#     Run Kadane's on the NEGATED array to find the minimum subarray.
#
# ----- Formula -----
#   max_circular = total_sum - min_subarray_sum
#
# ----- Visual Walkthrough -----
#
#   arr = [5, -3, 5]   total = 7
#
#   Case 1 (no wrap): Kadane's on arr
#     Running: 5 → 5+(-3)=2 vs -3, take 2 → 2+5=7 vs 5, take 7
#     max_no_wrap = 7
#
#   Case 2 (wrap): find min subarray, subtract from total
#     Negate arr: [-5, 3, -5]
#     Kadane's on negated: -5 → -5+3=-2 vs 3, take 3 → 3+(-5)=-2 vs -5, take -2
#     max of negated = 3  → min_subarray_sum = -3
#     max_wrap = total - min_subarray_sum = 7 - (-3) = 10
#
#   Answer: max(7, 10) = 10  ✓  (the subarray [5, 5] wrapping around)
#
# ----- Edge Case: All Negative -----
#   arr = [-3, -1, -2]
#   If all elements are negative, Case 2 would give: total - total = 0
#   (the "minimum subarray" is the whole array, leaving nothing selected)
#   But we need at least one element, so 0 is wrong.
#   Guard: if max_no_wrap < 0, return max_no_wrap (pick the least negative number).
#
# ----- Time & Space -----
#   Time:  O(n)   — two passes (Kadane's forward + Kadane's on negated)
#   Space: O(1)   — only tracking running sums, no extra arrays

def kadane_max(arr: list[int]) -> int:
    """Standard Kadane's — maximum subarray sum."""
    best = running = arr[0]
    for x in arr[1:]:
        running  = max(x, running + x)
        best     = max(best, running)
    return best

def max_circular_subarray_sum(arr: list[int]) -> int:
    max_no_wrap = kadane_max(arr)

    # Guard: all elements negative → circular wrap adds nothing
    if max_no_wrap < 0:
        return max_no_wrap

    total        = sum(arr)
    negated      = [-x for x in arr]
    min_subarray = -kadane_max(negated)  # negate result to get minimum

    max_wrap = total - min_subarray
    return max(max_no_wrap, max_wrap)


# --- Examples ---
print("\n===== SECTION 2: Maximum Circular Subarray Sum =====")
print(max_circular_subarray_sum([5, -3, 5]))          # 10  (wrap: 5+5)
print(max_circular_subarray_sum([8, -8, 9, -9, 10]))  # 27  (wrap: 10+8+9)
print(max_circular_subarray_sum([-3, -1, -2]))         # -1  (all negative)


# =============================================================================
# SECTION 3: Counting Smaller Elements
# =============================================================================

# ----- Problem -----
# Given TWO sorted arrays A and B, for each element in A, count how many
# elements in B are strictly LESS THAN that element.
#
# Example:
#   A = [1, 4, 7]
#   B = [2, 3, 6, 8]
#
#   For 1: elements in B less than 1 → none  → count = 0
#   For 4: elements in B less than 4 → 2, 3  → count = 2
#   For 7: elements in B less than 7 → 2,3,6 → count = 3
#   Answer: [0, 2, 3]
#
# ----- Brute Force: O(n × m) -----
# For each element in A (n elements), scan all of B (m elements).
# If n=10,000 and m=10,000 that's 100 million comparisons — slow.
#
# ----- Key Insight: B is Already Sorted — Use Binary Search -----
# Since B is sorted, we don't need to scan it.
# We can use BINARY SEARCH to find exactly where element A[i] would
# sit in B. The index of that position = count of elements smaller than A[i].
#
# This is called finding the "left boundary" or "lower bound":
#   → Find the first index in B where arr[index] >= A[i]
#   → Everything to the LEFT of that index is < A[i]
#   → So the index itself = count of smaller elements
#
# ----- Visual: Binary Search for Lower Bound -----
#
#   B = [2, 3, 6, 8],  looking for elements < 4
#
#   idx:   0   1   2   3
#   B:   [ 2,  3,  6,  8 ]
#
#   lo=0, hi=4   mid=2   B[2]=6 >= 4  → go LEFT  → hi=2
#   lo=0, hi=2   mid=1   B[1]=3 <  4  → go RIGHT → lo=2
#   lo=2, hi=2   → STOP
#
#   Answer: lo=2 means 2 elements (at index 0 and 1) are < 4  ✓
#
# ----- Why does this give the count? -----
# In a sorted array, if the first element >= target is at index k,
# then indices 0, 1, ..., k-1 are ALL less than target.
# So count = k = the index where we stopped.
#
# ----- Time & Space -----
#   Brute force:   O(n × m)
#   Binary search: O(n × log m)   — for each of n elements, binary search in B
#   Space: O(n) for the result array

def lower_bound(arr: list[int], target: int) -> int:
    """Return index of first element >= target in sorted arr."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1   # target is to the right
        else:
            hi = mid       # found a candidate, but keep searching left
    return lo              # lo = count of elements strictly less than target

def count_smaller_elements(A: list[int], B: list[int]) -> list[int]:
    return [lower_bound(B, a) for a in A]


# --- Examples ---
print("\n===== SECTION 3: Counting Smaller Elements =====")
print(count_smaller_elements([1, 4, 7], [2, 3, 6, 8]))    # [0, 2, 3]
print(count_smaller_elements([2, 5, 10], [1, 3, 4, 7]))   # [1, 3, 4]


# =============================================================================
# SECTION 4: Rain-Water Trapping
# =============================================================================

# ----- Problem -----
# You have N buildings of different heights standing next to each other.
# Each building has width 1. It rains. How much water gets trapped between
# the buildings?
#
# Example:  heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
# Answer:   6 units of water
#
# ----- Visualising the Problem -----
#
#   idx:  0  1  2  3  4  5  6  7  8  9 10 11
#   h:    0  1  0  2  1  0  1  3  2  1  2  1
#
#                              ┌──┐
#                              │  │           ┌──┐
#               ┌──┐           │  │  ┌──┐    │  │
#            ┌──┤  ├───────────┤  ├──┤  ├────┤  │
#            │  │  │~~~~~~~~~~~│  │~~│  │~~~~│  │  ← trapped water (~~~)
#            │  │  │  ┌──┐    │  │  │  │    │  │
#   ┌──┐     │  │  │  │  │    │  │  │  │    │  │
#   └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘
#
#   Water sits in the "valleys" — it only stays if there's a taller building
#   on BOTH sides to hold it in.
#
# ----- The Core Formula: Water at a Single Building -----
#
#   wi = min(li, ri) - hi
#
#   where:
#     hi = height of building i
#     li = max(height[0 .. i])    tallest building from LEFT up to i (inclusive)
#     ri = max(height[i .. n-1])  tallest building from RIGHT down to i (inclusive)
#
# Why min(li, ri)?
#   The water level is bounded by the SHORTER of the two walls.
#   Think of it as a bucket: the water spills over the lower edge first.
#   If left wall = 5 and right wall = 3, the water level can only reach 3.
#
# Why subtract hi?
#   The building itself takes up space. If the water level is 3 and the
#   building is 2 tall, only 3-2 = 1 unit of water sits ON TOP of it.
#
# Why is wi always >= 0?
#   Because li and ri are both computed INCLUDING height[i] itself.
#   So min(li, ri) >= height[i] always → wi >= 0. No need to clamp.
#
# ----- Visual: Step-by-Step for heights = [3, 0, 2, 0, 4] -----
#
#   idx:  0    1    2    3    4
#   h:    3    0    2    0    4
#
#   li (max from left, inclusive):
#     l[0] = 3
#     l[1] = max(l[0], h[1]) = max(3, 0) = 3
#     l[2] = max(l[1], h[2]) = max(3, 2) = 3
#     l[3] = max(l[2], h[3]) = max(3, 0) = 3
#     l[4] = max(l[3], h[4]) = max(3, 4) = 4
#   l = [3, 3, 3, 3, 4]
#
#   ri (max from right, inclusive):
#     r[4] = 4
#     r[3] = max(r[4], h[3]) = max(4, 0) = 4
#     r[2] = max(r[3], h[2]) = max(4, 2) = 4
#     r[1] = max(r[2], h[1]) = max(4, 0) = 4
#     r[0] = max(r[1], h[0]) = max(4, 3) = 4
#   r = [4, 4, 4, 4, 4]
#
#   wi = min(l[i], r[i]) - h[i]:
#     w[0] = min(3,4) - 3 = 0   (wall itself, no water on top)
#     w[1] = min(3,4) - 0 = 3   ✓
#     w[2] = min(3,4) - 2 = 1   ✓
#     w[3] = min(3,4) - 0 = 3   ✓
#     w[4] = min(4,4) - 4 = 0   (wall itself, no water on top)
#
#   Total = 0+3+1+3+0 = 7 ✓
#
# ----- The recurrence (how we build l and r arrays efficiently) -----
#
#   l[0]   = h[0]               (base case: first building, nothing to the left)
#   l[i]   = max(l[i-1], h[i])  (either the previous max, or this building)
#
#   r[n-1] = h[n-1]             (base case: last building, nothing to the right)
#   r[i]   = max(r[i+1], h[i])  (either the previous max, or this building)
#
#   This is the prefix/suffix max pattern from file 10.
#
# =============================================================================
# SOLUTION 1 (Brute Force) — O(n²) time, O(1) space
# =============================================================================
#
# For each building i, scan LEFT to find li, scan RIGHT to find ri.
# Straightforward but slow — two nested loops.
#
# Time: O(n²) — for each of n buildings, we scan up to n buildings
# This gives TLE (Time Limit Exceeded) on large inputs on LeetCode.

def trap_1(height: list[int]) -> int:
    n   = len(height)
    ans = 0

    for i in range(n):
        # li = tallest building from 0 to i (scan LEFT from i)
        li = height[i]
        for j in range(i - 1, -1, -1):
            li = max(li, height[j])

        # ri = tallest building from i to n-1 (scan RIGHT from i)
        ri = height[i]
        for j in range(i + 1, n):
            ri = max(ri, height[j])

        wi   = min(li, ri) - height[i]
        ans += wi

    return ans

# =============================================================================
# SOLUTION 2 — O(n) time, O(n) space  (precompute both l[] and r[])
# =============================================================================
#
# Problem with Solution 1: we re-scan left and right for EVERY building.
# The key observation: instead of scanning fresh each time, we can precompute
# ALL the li values in ONE left-to-right pass, and ALL the ri values in ONE
# right-to-left pass. Then compute wi in a third pass.
#
# Total: 3 × n operations = O(n) time.
#
# The recurrence makes each value O(1) to compute:
#   l[i] = max(l[i-1], height[i])  ← one comparison, not a scan
#   r[i] = max(r[i+1], height[i])  ← one comparison, not a scan
#
# Space: O(n) for the two arrays l[] and r[].

def trap_2(height: list[int]) -> int:
    n = len(height)

    # Pass 1 (left → right): precompute l[i] = max(height[0..i])
    l    = [0] * n
    l[0] = height[0]
    for i in range(1, n):
        l[i] = max(l[i - 1], height[i])

    # Pass 2 (right → left): precompute r[i] = max(height[i..n-1])
    r        = [0] * n
    r[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        r[i] = max(r[i + 1], height[i])

    # Pass 3: compute water at each building
    ans = 0
    for i in range(n):
        wi   = min(l[i], r[i]) - height[i]
        ans += wi

    return ans

# =============================================================================
# SOLUTION 3 — O(n) time, O(n) space  (precompute only r[], compute l on-the-fly)
# =============================================================================
#
# Observation: we scan left-to-right in pass 3 anyway.
# We can MERGE pass 1 (building l[]) into pass 3, computing li on-the-fly
# using a single variable maxSoFar instead of a full array.
#
# We still need r[] precomputed because we need r[i] in the FORWARD pass,
# but the full right array isn't available until we've scanned from the right.
#
# Space improvement: O(n) → O(n/2) in practice (only one array instead of two),
# but still O(n) asymptotically.
#
# NOTE: There was a bug in the original version of this function —
# it referenced l[i] which doesn't exist. The fix is to use maxSoFar
# (the running left max) instead of l[i].

def trap_3(height: list[int]) -> int:
    n = len(height)

    # Precompute r[i] = max(height[i..n-1]) — still need the full array
    r        = [0] * n
    r[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        r[i] = max(r[i + 1], height[i])

    ans        = 0
    maxSoFar   = 0        # this IS l[i], computed on-the-fly (replaces the l[] array)
    for i in range(n):
        maxSoFar = max(maxSoFar, height[i])   # l[i] = max(l[i-1], height[i])
        wi       = min(maxSoFar, r[i]) - height[i]   # ← was bug: l[i] → maxSoFar
        ans     += wi

    return ans

# =============================================================================
# SOLUTION 4 (Best) — O(n) time, O(1) space  — Two Pointers
# =============================================================================
#
# This is the solution the instructor highlighted as the BEST approach.
#
# ----- The Question -----
# Solution 3 still needs O(n) space for the r[] array.
# Can we eliminate that and compute both li and ri on-the-fly?
#
# ----- The Key Insight -----
# We don't actually need the EXACT value of ri to compute wi.
# We only need to know which side (left or right) is the LIMITING wall.
#
# Use two pointers: i starts at the LEFT end, j starts at the RIGHT end.
# They move INWARD toward each other.
# Track l = running max from the left, r = running max from the right.
#
# At any point:
#   l = max(height[0 .. i])    (the tallest wall i has passed on the left)
#   r = max(height[j .. n-1])  (the tallest wall j has passed on the right)
#
# Decision rule:
#   If l < r:
#     The left wall is SHORTER. For building i, we KNOW the left wall (l)
#     is the limiting factor — because r >= l, and the right wall can only
#     get taller as j moves inward. So wi = l - height[i]. Move i forward.
#
#   If r <= l:
#     The right wall is SHORTER. For building j, we KNOW the right wall (r)
#     is the limiting factor. wj = r - height[j]. Move j backward.
#
# ----- Why is this correct? -----
# For position i when l < r:
#   We know l = max(height[0..i])  → true left max for i ✓
#   We know r >= l, and r = max(height[j..n-1]).
#   The TRUE ri = max(height[i..n-1]) >= r >= l.
#   So min(li, ri) = min(l, ri) = l  (left is always the smaller one here).
#   Therefore wi = l - height[i] is EXACT, not an approximation.
#
# We never needed to know the exact value of ri — we just needed to know it
# was >= l, which r already guarantees.
#
# ----- Visual Walkthrough -----
#
#   height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
#   i=0, j=11, l=0, r=0
#
#   Step 1: l=max(0,h[0])=0, r=max(0,h[11])=1
#     l(0) < r(1) → wi = 0-0=0, ans=0, i=1
#
#   Step 2: l=max(0,h[1])=1, r=1
#     l(1) == r(1) → use else: wj = 1-1=0, ans=0, j=10
#
#   Step 3: l=1, r=max(1,h[10])=2
#     l(1) < r(2) → wi = 1-h[1]=1-1=0, ans=0, i=2
#
#   Step 4: l=max(1,h[2])=1, r=2
#     l(1) < r(2) → wi = 1-h[2]=1-0=1, ans=1, i=3
#
#   Step 5: l=max(1,h[3])=2, r=2
#     l(2) == r(2) → wj = 2-h[10]=2-2=0, ans=1, j=9
#
#   ... (continuing) ...  final ans = 6 ✓
#
# ----- Initialisation -----
# Start l = 0 and r = 0 (not height[0] and height[n-1]).
# At the START of each loop iteration, update l and r FIRST, THEN compute water.
# This way l always includes height[i] and r always includes height[j]
# before we calculate wi or wj.

def trap_4(height: list[int]) -> int:
    n = len(height)
    i, j = 0, n - 1
    l, r  = 0, 0       # running max from left and right
    ans   = 0

    while i <= j:
        l = max(l, height[i])   # update left max to include current i
        r = max(r, height[j])   # update right max to include current j

        if l < r:
            # Left wall is shorter → wi is determined by l
            wi   = l - height[i]
            ans += wi
            i   += 1
        else:
            # Right wall is shorter (or equal) → wj is determined by r
            wj   = r - height[j]
            ans += wj
            j   -= 1

    return ans

# ----- Comparing All Four Solutions -----
#
#   Solution   Time     Space   Key idea
#   ─────────────────────────────────────────────────────────────────────
#   trap_1     O(n²)    O(1)    Brute force: scan left+right for each i / EVERY building
#   trap_2     O(n)     O(n)    Precompute both l[] and r[] arrays upfront
#   trap_3     O(n)     O(n)    Drop l[] - Only precompute r[], compute l on-the-fly / compute left max on-the-fly with one variable
#   trap_4     O(n)     O(1)    Two pointers — best solution ✓ - drop r[] too, no extra arrays at all
#
# The progression from 1→2→3→4 is a classic interview pattern:
#   start with the obvious solution, then ask "what's redundant?" each time.

# Why the two-pointer works (the tricky part from these 4 solutions):
# When l < r at position i: you know r >= l, and whatever the TRUE right max is,
# it's at least r (which is already >= l). So the left wall (l) is definitely the
# limiting factor — wi = l - height[i] is exact. You never needed the full right array.
# Same logic applies to j from the right when r <= l.


# --- Examples ---
print("\n===== SECTION 4: Rain-Water Trapping =====")
h1 = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
h2 = [3, 0, 2, 0, 4]
h3 = [4, 2, 0, 3, 2, 5]
for h in [h1, h2, h3]:
    r1 = trap_1(h)
    r2 = trap_2(h)
    r3 = trap_3(h)
    r4 = trap_4(h)
    print(f"  heights={h}")
    print(f"  trap_1={r1}  trap_2={r2}  trap_3={r3}  trap_4(best)={r4}")
    assert r1 == r2 == r3 == r4, "Solutions disagree!"
    print()


# =============================================================================
# SECTION 5: Product of Array Except Self
# =============================================================================

# ----- Problem -----
# Given an array, return a new array where each element at index i is the
# product of ALL elements in the original array EXCEPT the element at index i.
#
# Constraint: do NOT use division. Do it in O(n) time.
#
# Example:
#   nums   = [1, 2, 3, 4]
#   answer = [24, 12, 8, 6]
#            (2×3×4, 1×3×4, 1×2×4, 1×2×3)
#
# ----- Why no division? -----
# The obvious approach would be:
#   total_product = product of all elements
#   answer[i] = total_product / nums[i]
# But division fails if any element is 0 (division by zero).
# Also, the problem explicitly forbids it to make you think harder.
#
# ----- Key Insight: Left Products × Right Products -----
# For each index i, the product of everything except nums[i] is:
#   (product of everything to the LEFT of i)
#   ×
#   (product of everything to the RIGHT of i)
#
# ----- Visual -----
#
#   nums = [1, 2, 3, 4]
#           ↑  ↑  ↑  ↑
#   idx:    0  1  2  3
#
#   LEFT products (prefix):
#     index 0: nothing to the left  → 1   (empty product = 1 by convention)
#     index 1: 1                    → 1
#     index 2: 1×2                  → 2
#     index 3: 1×2×3                → 6
#   prefix = [1, 1, 2, 6]
#
#   RIGHT products (suffix), scanning right-to-left:
#     index 3: nothing to the right → 1
#     index 2: 4                    → 4
#     index 1: 3×4                  → 12
#     index 0: 2×3×4                → 24
#   suffix = [24, 12, 4, 1]
#
#   answer[i] = prefix[i] × suffix[i]:
#     index 0:  1  × 24 = 24  ✓
#     index 1:  1  × 12 = 12  ✓
#     index 2:  2  ×  4 =  8  ✓
#     index 3:  6  ×  1 =  6  ✓
#
# ----- Space-Optimised Version -----
# Instead of two separate arrays, use the result array for prefix pass,
# then a running variable for suffix pass — reduces extra space to O(1).
#
# ----- Time & Space -----
#   Time:  O(n)   — two passes
#   Space: O(1)   — only the output array (which doesn't count as extra)

def product_except_self(nums: list[int]) -> list[int]:
    n      = len(nums)
    result = [1] * n

    # Pass 1 (left → right): result[i] holds product of everything to LEFT of i
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix   *= nums[i]   # update AFTER writing, so nums[i] itself isn't included

    # Pass 2 (right → left): multiply in product of everything to RIGHT of i
    suffix = 1
    for i in range(n-1, -1, -1):
        result[i] *= suffix
        suffix    *= nums[i]  # update AFTER multiplying, so nums[i] itself isn't included

    return result


# --- Examples ---
print("\n===== SECTION 5: Product of Array Except Self =====")
print(product_except_self([1, 2, 3, 4]))    # [24, 12, 8, 6]
print(product_except_self([2, 3, 4, 5]))    # [60, 40, 30, 24]
print(product_except_self([-1, 1, 0, -3]))  # [0, 0, 3, 0]  (any product with 0 is 0)


# =============================================================================
# SECTION 6: DNF Sort (Dutch National Flag)
# =============================================================================

# ----- Problem -----
# Given an array containing only 0s, 1s, and 2s, sort it in-place in O(n).
#
# Example:
#   Input:  [2, 0, 2, 1, 1, 0]
#   Output: [0, 0, 1, 1, 2, 2]
#
# ----- Why "Dutch National Flag"? -----
# The Netherlands flag has three horizontal bands: red, white, blue.
# The algorithm groups elements into three categories (0, 1, 2) —
# just like sorting three colours. Named by computer scientist Edsger Dijkstra.
#
# ----- Why not just use sort()? -----
# Python's sort() works in O(n log n). But since we know the values are
# ONLY 0, 1, or 2, we can exploit that knowledge to sort in O(n) — faster.
# Also useful in interviews to show you understand pointers.
#
# ----- Four-Region Invariant (from class notes) -----
# At any point during the algorithm, the array is split into FOUR regions:
#
#   [ 0..low-1 ] [ low..mid-1 ] [ mid..high ] [ high+1..n-1 ]
#      zeros          ones         unknown         twos
#
#   low  — first index of the "ones" region (everything left of low = 0s)
#   mid  — current element being examined (start of "unknown" region)
#   high — last index of "unknown" region (everything right of high = 2s)
#
#   Initialisation:
#     low = 0, mid = 0, high = n-1
#     (entire array starts as "unknown")
#
#   Goal: shrink the unknown region to zero by moving mid forward (or high backward)
#
# ----- The Three Cases (from class notes) -----
#
#   Case 1 — arr[mid] == 0:
#     "arr[mid] is 0, put it in the zeros region"
#     1. Swap arr[mid] and arr[low]
#     2. low  = low + 1    (zeros region grows right)
#     3. mid  = mid + 1    (unknown region shrinks left)
#     We can safely advance mid because the swapped element from arr[low]
#     was already processed (it was in the zeros or ones region).
#
#   Case 2 — arr[mid] == 1:
#     "arr[mid] is 1, put it in ones → mid + 1"
#     Just advance mid — the 1 is already between low and mid, correct position.
#
#   Case 3 — arr[mid] == 2:
#     "arr[mid] is 2, swap with arr[high] → high - 1"
#     1. Swap arr[mid] and arr[high]
#     2. high = high - 1   (twos region grows left)
#     DO NOT advance mid — the element that came from arr[high] is unknown,
#     we must examine it on the next iteration.
#
# ----- Visual Walkthrough (class example: N=9) -----
#
#   arr = [1, 0, 1, 2, 0, 1, 2, 0, 1]
#   low=0, mid=0, high=8
#
#   Regions:   zeros  ones  unknown                        twos
#   Initial:  [             1, 0, 1, 2, 0, 1, 2, 0, 1          ]
#
#   mid=0: arr[0]=1 → case 2 → mid=1
#   arr:   [1, 0, 1, 2, 0, 1, 2, 0, 1]   low=0, mid=1, high=8
#
#   mid=1: arr[1]=0 → case 1 → swap(low=0,mid=1) → [0,1,...], low=1, mid=2
#   arr:   [0, 1, 1, 2, 0, 1, 2, 0, 1]   low=1, mid=2, high=8
#
#   mid=2: arr[2]=1 → case 2 → mid=3
#   arr:   [0, 1, 1, 2, 0, 1, 2, 0, 1]   low=1, mid=3, high=8
#
#   mid=3: arr[3]=2 → case 3 → swap(mid=3,high=8) → [...0,1,...,2], high=7
#   arr:   [0, 1, 1, 1, 0, 1, 2, 0, 2]   low=1, mid=3, high=7
#
#   mid=3: arr[3]=1 → case 2 → mid=4
#   arr:   [0, 1, 1, 1, 0, 1, 2, 0, 2]   low=1, mid=4, high=7
#
#   mid=4: arr[4]=0 → case 1 → swap(low=1,mid=4) → [0,0,1,1,1,...], low=2, mid=5
#   arr:   [0, 0, 1, 1, 1, 1, 2, 0, 2]   low=2, mid=5, high=7
#
#   mid=5: arr[5]=1 → case 2 → mid=6
#   arr:   [0, 0, 1, 1, 1, 1, 2, 0, 2]   low=2, mid=6, high=7
#
#   mid=6: arr[6]=2 → case 3 → swap(mid=6,high=7) → [...,0,2,2], high=6
#   arr:   [0, 0, 1, 1, 1, 1, 0, 2, 2]   low=2, mid=6, high=6
#
#   mid=6: arr[6]=0 → case 1 → swap(low=2,mid=6) → [0,0,0,1,1,1,1,...], low=3, mid=7
#   arr:   [0, 0, 0, 1, 1, 1, 1, 2, 2]   low=3, mid=7, high=6
#
#   mid=7 > high=6 → STOP
#
#   Result: [0, 0, 0, 1, 1, 1, 1, 2, 2]  ✓
#
# ----- Time & Space -----
#   Time:  O(n)   — mid starts at 0 and only moves forward; high only moves backward.
#                   Together they traverse the array at most once.
#   Space: O(1)   — three pointer variables only, sorts in-place

# ── Instructor-style (variable names: low, mid, high — exactly as in class) ──

def dnf_sort_instructor(nums: list[int]) -> None:
    """Sorts in-place, same as instructor's LeetCode solution (sortColors)."""
    n = len(nums)
    low, mid, high = 0, 0, n - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:                  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            # do NOT increment mid

# ── Our version (returns a new list, same logic) ──────────────────────────────

def dnf_sort(arr: list[int]) -> list[int]:
    arr = arr[:]               # copy so we don't mutate caller's list
    low, mid, high = 0, 0, len(arr) - 1
    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
    return arr


# --- Examples ---
print("\n===== SECTION 6: DNF Sort =====")
print(dnf_sort([1, 0, 1, 2, 0, 1, 2, 0, 1]))  # class example → [0,0,0,1,1,1,1,2,2]
print(dnf_sort([2, 0, 2, 1, 1, 0]))            # [0, 0, 1, 1, 2, 2]
print(dnf_sort([0, 1, 2, 0, 1, 2]))            # [0, 0, 1, 1, 2, 2]
print(dnf_sort([2, 2, 0, 0, 1, 1]))            # [0, 0, 1, 1, 2, 2]


# =============================================================================
# SECTION 7: Counting Sort
# =============================================================================

# ----- Problem -----
# Given an array of N non-negative integers where every element is <= K,
# sort the array.
#
# Example:  arr = [4, 2, 2, 8, 3, 3, 1],  K = 8
# Output:   [1, 2, 2, 3, 3, 4, 8]
#
# ----- Why not just use sort()? -----
# Comparison-based sorting (like Python's sort) has a theoretical lower bound
# of O(n log n). You CANNOT sort by comparing elements faster than that.
#
# Counting Sort BREAKS this barrier — it runs in O(n + K) — because it
# doesn't COMPARE elements. It counts them instead.
# The trade-off: it only works when elements are non-negative integers
# in a known, bounded range [0, K].
#
# ----- Key Idea: "Array as a Map" -----
# The instructor's central point: we use the ARRAY ITSELF as a dictionary.
#
# A dictionary maps keys → values.
# In counting sort, we need to map:  element value → how many times it appears
#
# We create freq[] of size K+1 where:
#   KEY   = the index  (the element value)
#   VALUE = freq[index] (the count of that element)
#
#   Example:
#     arr = [1, 0, 3, 2, 3, 1, 2, 0, 2]  (all values in [0, 3])
#     freq[0] = 2  (0 appears twice)
#     freq[1] = 2  (1 appears twice)
#     freq[2] = 3  (2 appears three times)
#     freq[3] = 2  (3 appears twice)
#
#   index (key):  0  1  2  3
#   freq (value): 2  2  3  2
#
#   Output: 0 0 1 1 2 2 2 3 3   ← print index i exactly freq[i] times ✓
#
# This works because indices are integers in a known range [0, K].
# Each index directly encodes the value — no comparison needed at all.
# This is why we beat O(n log n): we're not comparing, just COUNTING.
#
# ----- Visual Walkthrough -----
#
#   arr = [4, 2, 2, 8, 3, 3, 1],  K = 8
#
#   Step 1 — Build freq array of size K+1 = 9:
#
#   Scan arr left to right, increment freq[element] for each element:
#     element 4 → freq[4]++
#     element 2 → freq[2]++
#     element 2 → freq[2]++
#     element 8 → freq[8]++
#     element 3 → freq[3]++
#     element 3 → freq[3]++
#     element 1 → freq[1]++
#
#   index:  0  1  2  3  4  5  6  7  8
#   freq:  [0, 1, 2, 2, 1, 0, 0, 0, 1]
#
#   Step 2 — Reconstruct: for i in 0..K, print i exactly freq[i] times:
#     i=0: freq[0]=0 → (skip)
#     i=1: freq[1]=1 → print 1      → output: 1
#     i=2: freq[2]=2 → print 2 2    → output: 1 2 2
#     i=3: freq[3]=2 → print 3 3    → output: 1 2 2 3 3
#     i=4: freq[4]=1 → print 4      → output: 1 2 2 3 3 4
#     i=5..7: freq=0 → (skip)
#     i=8: freq[8]=1 → print 8      → output: 1 2 2 3 3 4 8  ✓
#
# ----- Time & Space -----
#   Time:  O(n + K)
#     - O(n)     — scan arr to build freq
#     - O(n + K) — reconstruct (loop K+1 slots, output n elements total)
#   Space: O(K) for the freq array
#
# When K is small relative to n (K=100, n=1,000,000) → effectively O(n).
# When K >> n (K=1 billion, n=5) → use comparison sort instead.

# ── Instructor-style (uses freq, prints output) ──────────────────────────────

def counting_sort_instructor(arr: list[int], k: int):
    freq = [0] * (k + 1)
    for x in arr:           # O(n): count each element
        freq[x] += 1

    result = []
    for i in range(k + 1): # O(n+k): print i exactly freq[i] times
        for _ in range(freq[i]):
            result.append(i)
    return result

# ── Our version (same logic, Pythonic style) ─────────────────────────────────

def counting_sort(arr: list[int], k: int) -> list[int]:
    freq = [0] * (k + 1)
    for num in arr:
        freq[num] += 1
    result = []
    for value, count in enumerate(freq):
        result.extend([value] * count)
    return result

# Counting sort key concept from class: 
# the freq[] array IS a dictionary — index = element value (the key), freq[index] = count (the value).
# No comparisons needed, which is how it breaks the O(n log n) barrier.


# --- Examples ---
print("\n===== SECTION 7: Counting Sort =====")
print(counting_sort([4, 2, 2, 8, 3, 3, 1], k=8))  # [1, 2, 2, 3, 3, 4, 8]
print(counting_sort([3, 0, 2, 1, 3, 2], k=3))      # [0, 1, 2, 2, 3, 3]
print(counting_sort([1, 0, 3, 2, 3, 1, 2, 0, 2], k=3))  # [0,0,1,1,2,2,2,3,3]


# =============================================================================
# SECTION 8: Generalized Counting Sort
# =============================================================================

# ----- Problem -----
# Same as Counting Sort, but elements can be in any range [l, r]
# (not necessarily starting from 0).
#
# Example:  arr = [7, 5, 9, 6, 8, 5],  l = 5,  r = 9
# Output:   [5, 5, 6, 7, 8, 9]
#
# ----- Why doesn't plain Counting Sort work? -----
# If l = 5 and r = 9, plain counting sort needs an array of size r+1 = 10,
# but indices 0..4 are always 0 — wasted space.
# Worse, if l = 1000 and r = 1010, you'd allocate 1011 slots for 11 values.
#
# ----- Fix: Shift (the "n → idx = n - l" trick from class) -----
# The instructor wrote:  n → idx = n - l
# Meaning: element value n maps to index (n - l) in the freq array.
#
# Subtract l from every element so the range becomes [0, r-l].
# Freq array size = r - l + 1  (just big enough to cover the range)
# When reconstructing, add l back: element = index + l.
#
# ----- Visual Walkthrough (instructor's example: n=10, l=2, r=5) -----
#
#   arr = [4, 3, 2, 2, 4, 3, 5, 4, 5, 2]    (n=10, l=2, r=5)
#
#   Step 1 — Shift each element: idx = element - l = element - 2
#     element 2 → idx 0
#     element 3 → idx 1
#     element 4 → idx 2
#     element 5 → idx 3
#
#   Step 2 — Build freq array of size r-l+1 = 4:
#   idx:  0  1  2  3
#   freq:[3, 2, 3, 2]
#         ↑        ↑
#     2 appears 3 times  5 appears 2 times
#
#   Step 3 — Reconstruct: for i in range(4), print (i + l) freq[i] times
#     i=0: freq[0]=3 → print (0+2)=2 three times   → 2 2 2
#     i=1: freq[1]=2 → print (1+2)=3 twice          → 2 2 2 3 3
#     i=2: freq[2]=3 → print (2+2)=4 three times    → 2 2 2 3 3 4 4 4
#     i=3: freq[3]=2 → print (3+2)=5 twice          → 2 2 2 3 3 4 4 4 5 5  ✓
#
# ----- Visual Walkthrough (our example) -----
#
#   arr = [7, 5, 9, 6, 8, 5],  l=5, r=9
#   freq size = r - l + 1 = 5
#
#   Shift (subtract l=5):
#     7→2, 5→0, 9→4, 6→1, 8→3, 5→0
#
#   idx:  0  1  2  3  4
#   freq:[2, 1, 1, 1, 1]
#
#   Reconstruct (add l=5 back):
#     i=0: (0+5)=5, ×2  → [5, 5]
#     i=1: (1+5)=6, ×1  → [5, 5, 6]
#     i=2: (2+5)=7, ×1  → [5, 5, 6, 7]
#     i=3: (3+5)=8, ×1  → [5, 5, 6, 7, 8]
#     i=4: (4+5)=9, ×1  → [5, 5, 6, 7, 8, 9]  ✓
#
# ----- Time & Space -----
#   Time:  O(n + (r-l))   — same structure as counting sort
#   Space: O(r - l + 1)   — freq array sized to the RANGE, not the max value

# ── Instructor-style ──────────────────────────────────────────────────────────

def generalized_counting_sort_instructor(arr: list[int], lo: int, hi: int):
    freq = [0] * (hi - lo + 1)
    for x in arr:
        freq[x - lo] += 1           # n → idx = n - l

    result = []
    for i in range(hi - lo + 1):   # print (i + l) exactly freq[i] times
        for _ in range(freq[i]):
            result.append(i + lo)
    return result

# ── Our version (Pythonic) ────────────────────────────────────────────────────

def generalized_counting_sort(arr: list[int], lo: int, hi: int) -> list[int]:
    freq = [0] * (hi - lo + 1)
    for num in arr:
        freq[num - lo] += 1
    result = []
    for i, count in enumerate(freq):
        result.extend([i + lo] * count)
    return result


# --- Examples ---
print("\n===== SECTION 8: Generalized Counting Sort =====")
print(generalized_counting_sort([7, 5, 9, 6, 8, 5], lo=5, hi=9))           # [5, 5, 6, 7, 8, 9]
print(generalized_counting_sort([4,3,2,2,4,3,5,4,5,2], lo=2, hi=5))        # instructor's example
print(generalized_counting_sort([3, 1, 4, 1, 5, 9, 2, 6], lo=1, hi=9))     # [1,1,2,3,4,5,6,9]
print(generalized_counting_sort([-3, -1, -2, 0], lo=-3, hi=0))              # [-3, -2, -1, 0]


# =============================================================================
# SUMMARY: When to Use Which Algorithm
# =============================================================================

# ----- Choosing the right approach -----
#
#   Problem type                   Best approach          Time
#   ──────────────────────────────────────────────────────────────────
#   Sort general values            sort() / merge sort    O(n log n)
#   Sort 0s, 1s, 2s               DNF Sort               O(n)
#   Sort bounded non-neg integers  Counting Sort          O(n + K)
#   Sort bounded any-range ints    Generalized Count Sort O(n + range)
#   Max product of 3 elements      Sort + 2 candidates    O(n log n)
#   Max subarray (linear)          Kadane's Algorithm     O(n)
#   Max subarray (circular)        2× Kadane's            O(n)
#   Count smaller in sorted arr    Binary search          O(n log m)
#   Water trapped between buildings Prefix+Suffix arrays  O(n)
#   Product except self            Prefix+Suffix running  O(n)
#
# ----- A Pattern You'll Notice -----
# Many O(n) solutions use one of:
#   1. Prefix/Suffix arrays — precompute from left then right
#   2. Two/Three pointers   — use multiple indices to avoid nested loops
#   3. Counting/Hashing     — trade space for time by remembering what you've seen
