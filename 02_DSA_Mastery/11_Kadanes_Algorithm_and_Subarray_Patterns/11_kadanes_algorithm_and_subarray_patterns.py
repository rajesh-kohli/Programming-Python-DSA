###############################################################################
#         11 - Kadane's Algorithm and Subarray Patterns                        #
###############################################################################
#
# SOURCES:
#   Coding_Python/1. Python - Intro/11_two_pointers_and_kadane.py  (564 lines)
#   Coding_Python/1. Python - Intro/12_more_arrays_examples.py     (1108 lines)
#   LPLV26MAY/L13 - Intro to Arrays/001kadanes.py
#
# TOPICS IN THIS MODULE:
#   1.  Kadane's Algorithm — V1 (array O(n)/O(n)) and V2 (scalar O(n)/O(1))
#   2.  Kadane's with Subarray Tracking (3-pointer state machine)
#   3.  Maximum Circular Subarray Sum (total − min trick)
#   4.  Maximum Product of a Triplet (sort + 2 candidates)
#   5.  Practice Skeletons + Verified Driver (32 assertions)

from typing import List, Tuple


# =============================================================================
# SECTION 1: Kadane's Algorithm — Maximum Subarray Sum
# =============================================================================
#
# PROBLEM: Find the contiguous subarray with the MAXIMUM sum.
# Example:  arr=[-2,1,-3,4,-1,2,1,-5,4] → answer=6, subarray=[4,-1,2,1]
#
# WHY NOT O(n²) OR O(n³)?
#   - Brute force (3 loops):          O(n³) — recompute sum every (i,j)
#   - Optimised brute (2 loops):       O(n²) — extend sum, still all starts
#   - Prefix sum + running min:        O(n) / O(n)
#   - Kadane's scalar:                 O(n) / O(1)  ← THE answer
#
# THE "EXTEND OR RESET" MENTAL MODEL:
#   At every index i, ask: "Is it better to attach arr[i] to the running sum,
#   or to throw the running sum away and start fresh at arr[i]?"
#
#   x = max(x + arr[i],   arr[i])
#           ↑ EXTEND       ↑ RESET (start new subarray here)
#
#   WHY RESET? If x (running sum) is NEGATIVE, carrying it forward drags
#   down every future element. A negative prefix can only make a future sum
#   SMALLER than starting fresh. So Kadane's simply throws it away.
#
#   Rule: if x is positive → EXTEND (helps or is neutral)
#         if x is negative → RESET  (dead weight, throw away)
#
# FULL STEP TRACE: arr=[-2,1,-3,4,-1,2,1,-5,4]
#
#   i   arr[i]    x+arr[i]   arr[i]alone   x(chosen)  decision   max_so_far
#   ─────────────────────────────────────────────────────────────────────────
#   0     -2          —           —            -2       base          -2
#   1      1       -2+1=-1        1             1       RESET          1  (←-1<1)
#   2     -3        1-3=-2       -3            -2       EXTEND         1  (←-2>-3)
#   3      4       -2+4=2         4             4       RESET          4  (←2<4)
#   4     -1        4-1=3        -1             3       EXTEND         4
#   5      2        3+2=5         2             5       EXTEND         5
#   6      1        5+1=6         1             6       EXTEND         6  ← BEST
#   7     -5        6-5=1        -5             1       EXTEND         6
#   8      4        1+4=5         4             5       EXTEND         6
#
#   Answer: 6 → subarray [4,-1,2,1] at indices 3..6 ✓
#
# ─────────────────────────────────────────────────────────────────────────────
# VERSION 1: Array-based — O(n) Time, O(n) Space
# ─────────────────────────────────────────────────────────────────────────────
# Pedagogically clearest: x[i] stores "max sum ending exactly at index i".
# Each x[i] only depends on x[i-1] — that's the key to upgrading to V2.
# From L13/001kadanes.py (first version)

def kadane_array(arr: List[int]) -> int:
    """
    Kadane's V1: uses an array to store running max at each index.
    Time: O(n) | Space: O(n)
    Teaching version — shows that x[i] only depends on x[i-1].
    """
    n = len(arr)
    x = [0] * n
    x[0] = arr[0]
    max_so_far = x[0]

    for i in range(1, n):
        x[i] = max(x[i - 1] + arr[i], arr[i])   # extend or reset
        max_so_far = max(max_so_far, x[i])

    return max_so_far

# ─────────────────────────────────────────────────────────────────────────────
# VERSION 2: Scalar — O(n) Time, O(1) Space  ← WRITE THIS IN INTERVIEWS
# ─────────────────────────────────────────────────────────────────────────────
# Since x[i] only depends on x[i-1], replace the array with a single variable.
# From L13/001kadanes.py (optimised version)

def kadane_optimal(arr: List[int]) -> int:
    """
    Kadane's V2: scalar variable, O(1) space.
    Time: O(n) | Space: O(1)
    The version interviewers expect.
    """
    x = arr[0]              # running max subarray sum ending at current index
    max_so_far = x

    for i in range(1, len(arr)):
        x = max(x + arr[i], arr[i])     # extend or reset
        max_so_far = max(max_so_far, x)

    return max_so_far

def kadane_demo():
    print("=" * 60)
    print("SECTION 1: Kadane's Algorithm — Standard")
    print("=" * 60)

    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"\n  arr = {arr}")
    print(f"\n  Step trace (x=running max ending at i, max=global best):")
    print(f"  {'i':>3}  {'arr[i]':>7}  {'x+arr[i]':>10}  {'arr[i]alone':>12}  "
          f"{'x':>5}  {'decision':>8}  {'max':>5}")
    print("  " + "─" * 62)

    x = arr[0]
    max_so_far = x
    print(f"  {'0':>3}  {arr[0]:>7}  {'—':>10}  {'—':>12}  {x:>5}  {'base':>8}  {max_so_far:>5}")
    for i in range(1, len(arr)):
        extend = x + arr[i]
        reset  = arr[i]
        decision = "RESET" if reset > extend else "EXTEND"
        x = max(extend, reset)
        max_so_far = max(max_so_far, x)
        print(f"  {i:>3}  {arr[i]:>7}  {extend:>10}  {reset:>12}  {x:>5}  {decision:>8}  {max_so_far:>5}")

    print(f"\n  V1 (array) = {kadane_array(arr)}")
    print(f"  V2 (scalar)= {kadane_optimal(arr)}")
    print(f"\n  Array vs scalar space:")
    print(f"  V1: O(n) — x[] array stores one value per index")
    print(f"  V2: O(1) — x[i] only depends on x[i-1], so one variable suffices")

    tests = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([-3, -1, -2], -1),      # all negative → least-negative element
        ([1], 1),
        ([5, -4, 8], 9),
        ([-2, -3, 4, -1, -2, 1, 5, -3], 7),
        ([1, 2, 3, 4, 5], 15),   # all positive → whole array
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<40} {'V1':>4}  {'V2':>4}  {'exp':>4}  {'ok':>3}")
    print("  " + "─" * 55)
    for a, exp in tests:
        v1 = kadane_array(a)
        v2 = kadane_optimal(a)
        ok = "✓" if v1 == v2 == exp else "✗"
        print(f"  {str(a):<40} {v1:>4}  {v2:>4}  {exp:>4}  {ok:>3}")


# =============================================================================
# SECTION 2: Kadane's with Subarray Tracking — 3-Pointer State Machine
# =============================================================================
#
# PROBLEM: Same as above, but return the actual subarray segment, not just sum.
#
# THREE-POINTER STATE MACHINE:
#
#   temp_start  ← where the CURRENT candidate subarray begins
#                 (updated on every RESET — new subarray starts here)
#
#   start       ← where the overall BEST subarray begins
#   end         ← where the overall BEST subarray ends
#                 (updated whenever we find a new max_so_far)
#
#   STATE TRANSITIONS:
#   ┌─────────────────────────────────────────────────────────────┐
#   │  if arr[i] > x + arr[i]:    (RESET wins)                    │
#   │      x = arr[i]                                             │
#   │      temp_start = i    ← new candidate starts HERE          │
#   │                                                             │
#   │  else:                       (EXTEND wins)                  │
#   │      x += arr[i]                                            │
#   │                                                             │
#   │  if x > max_so_far:          (new global best found)        │
#   │      max_so_far = x                                         │
#   │      start = temp_start  ← lock in candidate start         │
#   │      end = i             ← lock in current index as end    │
#   └─────────────────────────────────────────────────────────────┘
#
# ALL-NEGATIVE EDGE CASE:
#   arr=[-3,-1,-2] → resets at every step.
#   temp_start tracks each reset correctly.
#   Final: start=end=1 (index of -1), subarray=[-1] ✓
#   The 3-pointer logic handles this automatically — no special case needed.
#
# From Coding_Python/11 lines 450-467

def kadane_with_subarray(arr: List[int]) -> Tuple[int, List[int]]:
    """
    Kadane's with 3-pointer subarray tracking.
    Time: O(n) | Space: O(1) — only start, end, temp_start, x, max_so_far
    Returns: (max_sum, subarray_segment)
    """
    if not arr:
        return 0, []

    max_so_far = arr[0]
    x          = arr[0]
    start = end = temp_start = 0

    for i in range(1, len(arr)):
        if arr[i] > x + arr[i]:          # RESET: fresh start at arr[i]
            x = arr[i]
            temp_start = i               # candidate new subarray begins here
        else:                            # EXTEND: keep building
            x += arr[i]

        if x > max_so_far:               # new global best — lock in boundaries
            max_so_far = x
            start = temp_start           # confirm the candidate start
            end   = i                   # and current index as end

    return max_so_far, arr[start:end + 1]

def subarray_demo():
    print("\n" + "=" * 60)
    print("SECTION 2: Kadane's with Subarray Tracking")
    print("=" * 60)

    test_cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6,  [4, -1, 2, 1]),
        ([-3, -1, -2],                    -1,  [-1]),          # all negative
        ([5, -4, 8],                       9,  [5, -4, 8]),    # single best span
        ([1, 2, 3, 4, 5],                 15,  [1, 2, 3, 4, 5]), # all positive
        ([-5],                            -5,  [-5]),           # single element
        ([3, -1, -1, -1, 3],               3,  [3]),            # linear max = 3 (first elem)
    ]

    print(f"\n  3-pointer state machine trace for arr=[-2,1,-3,4,-1,2,1,-5,4]:")
    arr_demo = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    x_d = arr_demo[0]; ms = arr_demo[0]; ts = s = e = 0
    print(f"  {'i':>2}  {'a[i]':>5}  {'x':>5}  {'ts':>3}  {'s':>2}  {'e':>2}  "
          f"{'max':>5}  note")
    print("  " + "─" * 50)
    print(f"  {'0':>2}  {arr_demo[0]:>5}  {x_d:>5}  {ts:>3}  {s:>2}  {e:>2}  "
          f"{ms:>5}  base")
    for i in range(1, len(arr_demo)):
        note = ""
        if arr_demo[i] > x_d + arr_demo[i]:
            x_d = arr_demo[i]; ts = i; note = "RESET"
        else:
            x_d += arr_demo[i]; note = "EXTEND"
        if x_d > ms:
            ms = x_d; s = ts; e = i; note += " ← new best"
        print(f"  {i:>2}  {arr_demo[i]:>5}  {x_d:>5}  {ts:>3}  {s:>2}  {e:>2}  "
              f"{ms:>5}  {note}")
    print(f"  → sum={ms}, subarray=arr[{s}:{e+1}]={arr_demo[s:e+1]}")

    print(f"\n  Verification:")
    print(f"  {'arr':<35} {'sum':>4}  {'subarray':<20}  {'ok':>3}")
    print("  " + "─" * 65)
    for a, exp_sum, exp_arr in test_cases:
        got_sum, got_arr = kadane_with_subarray(a)
        ok = "✓" if got_sum == exp_sum and got_arr == exp_arr else "✗"
        print(f"  {str(a):<35} {got_sum:>4}  {str(got_arr):<20}  {ok:>3}")


# =============================================================================
# SECTION 3: Maximum Circular Subarray Sum
# =============================================================================
#
# PROBLEM: Array is arranged in a CIRCLE. Find max sum subarray (may wrap around).
#
# KEY INSIGHT: Only two cases exist for any circular subarray:
#
#   Case 1 — Does NOT wrap:
#     [ ← selected → ]
#     → Standard Kadane's (max_normal)
#
#   Case 2 — DOES wrap:
#     [ selected | not selected | selected ]
#       left part  middle part    right part
#
#     circular_sum = total_sum - sum(middle_part)
#     Maximise circular_sum → MINIMISE the middle part
#     Middle part = contiguous subarray → run Kadane's for MINIMUM
#
#   Formula:  max_circular = total - min_subarray_sum
#
# DERIVATION for arr=[5,-3,5]:
#
#   total = 7
#
#   Case 1: Kadane max
#     i=0: x=5,  max=5
#     i=1: x=max(5-3,-3)=2, max=5
#     i=2: x=max(2+5,5)=7,  max=7
#     max_normal = 7
#
#   Case 2: Negate and run Kadane max → get min
#     negated = [-5, 3, -5]
#     i=0: x=-5,  max=-5
#     i=1: x=max(-5+3,3)=3, max=3
#     i=2: x=max(3-5,-5)=-2, max=3
#     max_of_negated = 3  → min_subarray = -3
#     max_wrap = 7 - (-3) = 10
#
#   Answer = max(7, 10) = 10 ✓  (subarray [5,5] wrapping around)
#
# CRITICAL EDGE CASE — ALL NEGATIVE:
#   arr=[-3,-1,-2],  total=-6
#   Case 1: max_normal = -1  (least-negative element — correct answer)
#   Case 2: min_subarray = -6 (entire array is the minimum)
#           max_wrap = -6 - (-6) = 0  ← WRONG! 0 means "select nothing"
#                                         but we must select ≥1 element.
#
#   GUARD: if max_normal < 0: return max_normal  (skip Case 2)
#   The all-negative case is the only time Case 2 is invalid.
#
# Time: O(n) | Space: O(1)  (two Kadane passes, no extra arrays)
# From Coding_Python/12 lines 200-220

def _kadane_max(arr: List[int]) -> int:
    """Standard Kadane's max — helper for circular variant."""
    best = running = arr[0]
    for x in arr[1:]:
        running = max(x, running + x)
        best    = max(best, running)
    return best

def max_circular_subarray(arr: List[int]) -> int:
    """
    Maximum circular subarray sum.
    Time: O(n) | Space: O(1)
    Formula: max(kadane_max, total - kadane_min)
    Guard: if all negative → return kadane_max (skip circular case).
    """
    max_normal = _kadane_max(arr)

    # Guard: all elements negative → circular wrap gives 0 (invalid)
    if max_normal < 0:
        return max_normal

    total    = sum(arr)                          # O(n) — acceptable
    negated  = [-x for x in arr]                # negate to find min via max
    min_sub  = -_kadane_max(negated)             # un-negate: min of original
    max_wrap = total - min_sub                   # total − min_middle = max_wrap

    return max(max_normal, max_wrap)

def circular_demo():
    print("\n" + "=" * 60)
    print("SECTION 3: Maximum Circular Subarray Sum")
    print("=" * 60)

    # Annotated walkthrough for [5, -3, 5]
    arr_c = [5, -3, 5]
    total_c = sum(arr_c)
    max_normal_c = _kadane_max(arr_c)
    min_sub_c    = -_kadane_max([-x for x in arr_c])
    max_wrap_c   = total_c - min_sub_c
    print(f"""
  arr = {arr_c}

  Case 1 (no wrap)  — Kadane's max:
    i=0: x=5,  max=5
    i=1: x=max(5-3,-3)=2, max=5
    i=2: x=max(2+5,5)=7,  max=7
    max_normal = {max_normal_c}

  Case 2 (wrap)  — negate → Kadane max → un-negate → subtract:
    negated = {[-x for x in arr_c]}
    i=0: x=-5,  max=-5
    i=1: x=max(-5+3,3)=3, max=3
    i=2: x=max(3-5,-5)=-2, max=3
    max_of_negated = 3  → min_subarray = -3
    max_wrap = total - min_sub = {total_c} - ({min_sub_c}) = {max_wrap_c}

  Answer = max({max_normal_c}, {max_wrap_c}) = {max_circular_subarray(arr_c)} ✓
  (subarray [5,5] wrapping around index 2 → index 0)
    """)

    # All-negative edge case proof
    arr_neg = [-3, -1, -2]
    total_n     = sum(arr_neg)
    min_sub_n   = -_kadane_max([-x for x in arr_neg])
    print(f"  ALL-NEGATIVE EDGE CASE: arr={arr_neg}")
    print(f"    max_normal = {_kadane_max(arr_neg)}  (least-negative element)")
    print(f"    total = {total_n},  min_subarray = {min_sub_n}  (entire array)")
    print(f"    If we applied Case 2: total - min = {total_n} - ({min_sub_n}) = "
          f"{total_n - min_sub_n}  ← WRONG (means select nothing)")
    print(f"    GUARD: max_normal < 0 → return {_kadane_max(arr_neg)} ✓")

    tests = [
        ([5, -3, 5],            10),     # wrap: 5+5
        ([8, -8, 9, -9, 10],    19),     # wrap: 10+9 (verified by brute)
        ([-3, -1, -2],          -1),     # all negative — guard fires
        ([1, 2, 3, 4, 5],       15),     # no wrap needed, all positive
        ([5, -3, 5, -3, 5],     12),     # wrap: 5+5-3+5 (verified by brute)
        ([-2, 3, -2],            3),     # normal case wins
        ([-5],                  -5),     # single element
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<35} {'result':>7}  {'exp':>5}  {'ok':>3}")
    print("  " + "─" * 52)
    for a, exp in tests:
        result = max_circular_subarray(a)
        ok = "✓" if result == exp else "✗"
        print(f"  {str(a):<35} {result:>7}  {exp:>5}  {ok:>3}")


# =============================================================================
# SECTION 4: Maximum Product of a Triplet
# =============================================================================
#
# PROBLEM: Find three elements in arr whose product is maximum (negatives ok).
# Example: arr=[-10,-10,1,3,2] → (-10)×(-10)×3 = 300  ← two negatives!
#
# KEY INSIGHT: After sorting, exactly TWO candidates exist:
#
#   Candidate A: arr[-1] × arr[-2] × arr[-3]   (three largest elements)
#   Candidate B: arr[0]  × arr[1]  × arr[-1]   (two most-negative × largest)
#
# WHY ONLY THESE TWO?
#   - If all positive: Candidate A wins (three biggest values).
#   - If two large negatives: Candidate B may win (neg × neg = pos).
#   - arr[0] × arr[2] < arr[0] × arr[1] because arr[1] ≤ arr[2] in sorted order
#     and both are negative — arr[1] has a LARGER absolute value → bigger product.
#   - No other triple can beat the three-largest or the two-most-negative × largest.
#
# Time: O(n log n) — sort dominates | Space: O(1)
# From Coding_Python/12 lines 107-114

def max_product_triplet(arr: List[int]) -> int:
    """
    Maximum product of any three elements.
    Time: O(n log n) | Space: O(1)
    """
    arr = sorted(arr)                              # sort in-place copy
    n   = len(arr)
    candidate_a = arr[n-1] * arr[n-2] * arr[n-3]  # three largest
    candidate_b = arr[0]   * arr[1]   * arr[n-1]  # two most-negative × largest
    return max(candidate_a, candidate_b)

def triplet_demo():
    print("\n" + "=" * 60)
    print("SECTION 4: Maximum Product of a Triplet")
    print("=" * 60)

    arr = [-10, -10, 1, 3, 2]
    s = sorted(arr)
    a = s[-1]*s[-2]*s[-3]
    b = s[0]*s[1]*s[-1]
    print(f"\n  arr = {arr}  →  sorted = {s}")
    print(f"  Candidate A (three largest): {s[-1]}×{s[-2]}×{s[-3]} = {a}")
    print(f"  Candidate B (two most-neg × largest): {s[0]}×{s[1]}×{s[-1]} = {b}")
    print(f"  Answer = max({a}, {b}) = {max(a,b)} ✓")

    tests = [
        ([-10, -10, 1, 3, 2],   300),   # two negatives win
        ([1, 2, 3, 4, 5],        60),   # three largest (3×4×5)
        ([-5, -4, -3, -2, -1],   -6),   # all negative (-3×-2×-1)
        ([0, -1, -2, -3],         0),   # zero wins (0×-1×-2)
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<30} {'result':>7}  {'exp':>5}  {'ok':>3}")
    print("  " + "─" * 47)
    for a, exp in tests:
        result = max_product_triplet(a)
        ok = "✓" if result == exp else "✗"
        print(f"  {str(a):<30} {result:>7}  {exp:>5}  {ok:>3}")


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_kadane(arr: List[int]) -> int:
    """
    Maximum subarray sum (scalar Kadane's).
    Time: O(n) | Space: O(1)
    Hint: x=arr[0], max_so_far=x; for i in 1..n: x=max(x+arr[i], arr[i]); ...
    """
    pass

def practice_kadane_with_subarray(arr: List[int]) -> Tuple[int, List[int]]:
    """
    Maximum subarray sum AND the actual subarray.
    Time: O(n) | Space: O(1)
    Hint: track temp_start (reset point), start/end (best confirmed boundaries)
    """
    pass

def practice_max_circular(arr: List[int]) -> int:
    """
    Maximum circular subarray sum.
    Time: O(n) | Space: O(1)
    Hint: max(kadane_max(arr), total - (-kadane_max(negated)))
          Guard: if max_normal < 0, return max_normal
    """
    pass

def practice_max_product_triplet(arr: List[int]) -> int:
    """
    Maximum product of any 3 elements (handles negatives).
    Time: O(n log n) | Space: O(1)
    Hint: sort; candidate_a=arr[-1]*arr[-2]*arr[-3]; candidate_b=arr[0]*arr[1]*arr[-1]
    """
    pass


# =============================================================================
# DRIVER — Verifies all optimal implementations, then shows skeleton stubs
# =============================================================================
if __name__ == "__main__":
    kadane_demo()
    subarray_demo()
    circular_demo()
    triplet_demo()

    print("\n" + "=" * 60)
    print("OPTIMAL SOLUTION VERIFICATION")
    print("=" * 60)

    # ── Kadane's V1 and V2 ──
    kadane_tests = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([-3, -1, -2],                    -1),   # all negative
        ([1],                              1),
        ([5, -4, 8],                       9),
        ([-2, -3, 4, -1, -2, 1, 5, -3],   7),
        ([1, 2, 3, 4, 5],                 15),
    ]
    for a, exp in kadane_tests:
        assert kadane_array(a)   == exp, f"kadane_array failed on {a}"
        assert kadane_optimal(a) == exp, f"kadane_optimal failed on {a}"
    print(f"\n  kadane_array:   {len(kadane_tests)} assertions ✓")
    print(f"  kadane_optimal: {len(kadane_tests)} assertions ✓")

    # ── Kadane's with subarray ──
    subarray_tests = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6,  [4, -1, 2, 1]),
        ([-3, -1, -2],                    -1,  [-1]),
        ([5, -4, 8],                       9,  [5, -4, 8]),
        ([1, 2, 3, 4, 5],                 15,  [1, 2, 3, 4, 5]),
        ([-5],                            -5,  [-5]),
        ([3, -1, -1, -1, 3],               3,  [3]),   # linear max=3
    ]
    for a, exp_sum, exp_arr in subarray_tests:
        got_sum, got_arr = kadane_with_subarray(a)
        assert got_sum == exp_sum, \
            f"kadane_with_subarray sum mismatch on {a}: got {got_sum}, expected {exp_sum}"
        assert got_arr == exp_arr, \
            f"kadane_with_subarray arr mismatch on {a}: got {got_arr}, expected {exp_arr}"
    print(f"  kadane_with_subarray: {len(subarray_tests)} assertions ✓")

    # ── Circular subarray ──
    circular_tests = [
        ([5, -3, 5],            10),
        ([8, -8, 9, -9, 10],    19),   # verified by brute force
        ([-3, -1, -2],          -1),   # all negative — guard fires
        ([1, 2, 3, 4, 5],       15),
        ([5, -3, 5, -3, 5],     12),   # verified by brute force
        ([-2, 3, -2],            3),
        ([-5],                  -5),
    ]
    for a, exp in circular_tests:
        assert max_circular_subarray(a) == exp, \
            f"max_circular_subarray failed on {a}: got {max_circular_subarray(a)}, expected {exp}"
    print(f"  max_circular_subarray: {len(circular_tests)} assertions ✓")

    # ── Max product triplet ──
    triplet_tests = [
        ([-10, -10, 1, 3, 2],   300),
        ([1, 2, 3, 4, 5],        60),
        ([-5, -4, -3, -2, -1],   -6),
        ([0, -1, -2, -3],         0),
    ]
    for a, exp in triplet_tests:
        assert max_product_triplet(a) == exp, \
            f"max_product_triplet failed on {a}"
    print(f"  max_product_triplet: {len(triplet_tests)} assertions ✓")

    total_assertions = (len(kadane_tests) * 2 + len(subarray_tests)
                        + len(circular_tests) + len(triplet_tests))
    print(f"\n  {'─'*40}")
    print(f"  Total verified assertions: {total_assertions} ✓")
    print(f"  {'─'*40}")

    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS (return None until implemented)")
    print("=" * 60)

    arr_test = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    circ_test = [5, -3, 5]
    tri_test  = [-10, -10, 1, 3, 2]

    print(f"\n  arr = {arr_test}")
    print(f"  practice_kadane(arr)                = {practice_kadane(arr_test)}")
    print(f"  practice_kadane_with_subarray(arr)  = {practice_kadane_with_subarray(arr_test)}")

    print(f"\n  circ = {circ_test}")
    print(f"  practice_max_circular(circ)         = {practice_max_circular(circ_test)}")

    print(f"\n  tri = {tri_test}")
    print(f"  practice_max_product_triplet(tri)   = {practice_max_product_triplet(tri_test)}")

    print("=" * 60)
    print("Fill in the skeletons above and re-run to verify.")
