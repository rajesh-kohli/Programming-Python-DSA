###############################################################################
#                    12 - Classical Sorting Algorithms                         #
###############################################################################
#
# SOURCES:
#   Coding_Python/1. Python - Intro/09_sorting_algorithms.py  (420 lines)
#   LPLV26MAY/L11 - Intro to Arrays (Sorting)/001bubbleSort.py
#   LPLV26MAY/L11 - Intro to Arrays (Sorting)/002selectionSort.py
#   LPLV26MAY/L11 - Intro to Arrays (Sorting)/003insertionSort.py
#   LPLV26MAY/L11 - Intro to Arrays (Sorting)/004sorted.py
#   LPLV26MAY/L14 - Intro to Arrays/005dnfSort.py
#   LPLV26MAY/L14 - Intro to Arrays/006countingSort.py
#   LPLV26MAY/L14 - Intro to Arrays/007generalizedCountingSort.py
#
# TOPICS IN THIS MODULE:
#   1.  Selection Sort   — O(n²) / O(1) / Unstable / in-place
#   2.  Bubble Sort      — O(n²) worst, O(n) best / Stable / in-place + flag
#   3.  Insertion Sort   — O(n²) worst, O(n) best / Stable / in-place
#   4.  DNF Sort         — O(n) / O(1) / in-place  (3-pointer partitioning)
#   5.  Counting Sort    — O(n+K) / O(K)            (breaks comparison barrier)
#   6.  Generalized Counting Sort — handles negatives via shifting
#   7.  Python Timsort   — built-in sort(), sorted()
#   8.  Practice Skeletons + Verified Driver (36 assertions)

from typing import List


# =============================================================================
# SECTION 1: Selection Sort
# =============================================================================
#
# CORE IDEA: In each pass, FIND the minimum in the unsorted portion and
#            SWAP it into the frontier (the first unsorted slot).
#
# MENTAL MODEL: A growing sorted boundary.
#   [ sorted | unsorted ]
#   Each pass scans the unsorted side, finds the minimum, and swaps it
#   to the frontier. The frontier moves one step right per pass.
#
# VISUAL WALKTHROUGH — arr=[50, 20, 30, 10, 40]:
#
#   Pass 1 (i=0): scan [50,20,30,10,40] → min=10 at idx 3 → swap arr[0]↔arr[3]
#     [10, 20, 30, 50, 40]   10 is FINAL
#
#   Pass 2 (i=1): scan [20,30,50,40] → min=20 at idx 1 → no-op swap
#     [10, 20, 30, 50, 40]   20 is FINAL
#
#   Pass 3 (i=2): scan [30,50,40] → min=30 at idx 2 → no-op
#     [10, 20, 30, 50, 40]   30 is FINAL
#
#   Pass 4 (i=3): scan [50,40] → min=40 at idx 4 → swap arr[3]↔arr[4]
#     [10, 20, 30, 40, 50]   DONE ✓
#
# WHY NOT STABLE — counterexample with equal elements:
#   arr=[4a, 4b, 1]  (4a and 4b are both value 4, subscript = original order)
#   Pass 1: min=1 at idx 2, swap arr[0]↔arr[2] → [1, 4b, 4a]
#   Now 4b precedes 4a — ORIGINAL ORDER OF EQUAL ELEMENTS IS BROKEN.
#
# MINIMUM SWAPS PROPERTY:
#   Selection sort does at most n-1 swaps (one per pass).
#   Bubble sort can do O(n²) swaps. Use Selection when WRITES are expensive.
#
# WHY O(n²) always:
#   Pass 1: n-1 comparisons (scan whole unsorted portion)
#   Pass 2: n-2 comparisons
#   ...
#   Total = (n-1)+(n-2)+...+1 = n(n-1)/2 = O(n²)
#   No early termination possible — must always scan to find the true minimum.
#
# Time (Best/Avg/Worst): O(n²) | Space: O(1) | Stable: No | In-place: Yes
# From Coding_Python/09 & L11/002selectionSort.py

def selection_sort(arr: List[int]) -> None:
    """
    In-place selection sort.
    Time: O(n²) always | Space: O(1) | Stable: No
    Pass i: find min in arr[i..n-1], swap to position i.
    """
    n = len(arr)
    for i in range(n):                      # i = frontier (first unsorted slot)
        min_idx = i                         # assume frontier element is minimum
        for j in range(i + 1, n):          # scan unsorted portion
            if arr[j] < arr[min_idx]:
                min_idx = j                 # found a smaller element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]   # swap min to frontier

def selection_sort_demo():
    print("=" * 60)
    print("SECTION 1: Selection Sort")
    print("=" * 60)

    arr_orig = [50, 20, 30, 10, 40]
    arr = arr_orig[:]
    print(f"\n  arr = {arr}")
    print(f"\n  Pass-by-pass trace:")
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        swap_desc = (f"swap arr[{i}]({arr[i]})↔arr[{min_idx}]({arr[min_idx]})"
                     if min_idx != i else "no-op (already min)")
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        print(f"  Pass {i+1}: {swap_desc} → {arr}   (arr[:{i+1}] locked)")

    print(f"\n  Min-swaps property: at most n-1={n-1} swaps total (cheapest writer)")
    print(f"  Stability counterexample: [4a,4b,1]")
    print(f"    Pass 1: min=1@idx2, swap idx0↔idx2 → [1,4b,4a]")
    print(f"    4b now precedes 4a → original order of equals BROKEN → UNSTABLE ✗")

    tests = [
        ([50, 20, 30, 10, 40], [10, 20, 30, 40, 50]),
        ([1],                  [1]),
        ([3, 1, 2],            [1, 2, 3]),
        ([-5, 3, -1, 0, 2],   [-5, -1, 0, 2, 3]),
        ([5, 4, 3, 2, 1],     [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5],     [1, 2, 3, 4, 5]),
    ]
    print(f"\n  Verification (in-place → sort copy, compare):")
    print(f"  {'arr':<30} {'result':<30} {'exp':<30} {'ok':>3}")
    print("  " + "─" * 93)
    for a_orig, exp in tests:
        a = a_orig[:]
        selection_sort(a)
        ok = "✓" if a == exp else "✗"
        print(f"  {str(a_orig):<30} {str(a):<30} {str(exp):<30} {ok:>3}")


# =============================================================================
# SECTION 2: Bubble Sort (with early-termination flag)
# =============================================================================
#
# CORE IDEA: Walk through the array, SWAP ADJACENT elements in the wrong order.
#            The largest unsorted element "bubbles" to the end each pass.
#
# MENTAL MODEL: Like air bubbles rising through water — the heaviest value
#               floats one step right per comparison until it reaches the end.
#
# VISUAL WALKTHROUGH — arr=[50, 40, 30, 20, 10]:
#
#   Pass 1: compare all adjacent pairs in [50,40,30,20,10]
#     j=0: 50>40? swap → [40,50,30,20,10]
#     j=1: 50>30? swap → [40,30,50,20,10]
#     j=2: 50>20? swap → [40,30,20,50,10]
#     j=3: 50>10? swap → [40,30,20,10,50]    50 in final position
#
#   Pass 2: compare in [40,30,20,10 | 50]    → [30,20,10,40,50]  40 done
#   Pass 3: compare in [30,20,10 | 40,50]    → [20,10,30,40,50]  30 done
#   Pass 4: compare in [20,10 | 30,40,50]    → [10,20,30,40,50]  DONE ✓
#
# THE 'flag' EARLY-TERMINATION OPTIMIZATION (from L11/001bubbleSort.py):
#   Before each pass: flag = False
#   Any swap: flag = True
#   End of pass: if NOT flag → no swaps → array is already sorted → STOP
#
#   Best case (already sorted):
#     Pass 1: n-1 comparisons, 0 swaps → flag=False → break
#     Total = n-1 comparisons = O(n)
#
# WHY IS IT STABLE:
#   Swap condition: arr[j] > arr[j+1]   (STRICTLY greater)
#   If arr[j] == arr[j+1]: NO swap → equal elements NEVER cross each other.
#
# WHY O(n²) worst case:
#   Pass 1: n-1 comparisons
#   Pass 2: n-2 comparisons (last element already settled)
#   ...
#   Total = (n-1)+(n-2)+...+1 = n(n-1)/2 = O(n²)
#
# Time Best: O(n) (sorted+flag) | Worst/Avg: O(n²) | Space: O(1)
# Stable: Yes | In-place: Yes
# From Coding_Python/09 & L11/001bubbleSort.py

def bubble_sort(arr: List[int]) -> None:
    """
    In-place bubble sort with early-termination flag.
    Time: O(n) best (sorted) | O(n²) worst | Space: O(1) | Stable: Yes
    """
    n = len(arr)
    for i in range(n):
        flag = False                    # flag: did any swap happen this pass?
        for j in range(n - i - 1):     # last i elements already in final position
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                flag = True
        if not flag:                    # no swaps → already sorted → stop early
            break

def bubble_sort_demo():
    print("\n" + "=" * 60)
    print("SECTION 2: Bubble Sort (with flag)")
    print("=" * 60)

    arr_orig = [50, 40, 30, 20, 10]
    arr = arr_orig[:]
    n = len(arr)
    print(f"\n  arr = {arr}")
    print(f"\n  Pass-by-pass trace:")
    for i in range(n):
        flag = False
        swaps = []
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                swaps.append(f"j={j}: {arr[j]}↔{arr[j+1]}")
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                flag = True
        note = "STOP (no swaps)" if not flag else f"{len(swaps)} swap(s)"
        print(f"  Pass {i+1}: {note} → {arr}   (arr[{n-i-1}:] locked)")
        if not flag:
            break

    print(f"\n  Stability proof:")
    print(f"    Swap only when arr[j] > arr[j+1] (STRICTLY greater)")
    print(f"    If arr[j]==arr[j+1]: no swap → equal elements never cross → STABLE ✓")

    already = [10, 20, 30, 40, 50]
    a_already = already[:]
    passes = 0
    for i in range(len(a_already)):
        flag = False
        for j in range(len(a_already) - i - 1):
            if a_already[j] > a_already[j+1]:
                a_already[j], a_already[j+1] = a_already[j+1], a_already[j]
                flag = True
        passes += 1
        if not flag:
            break
    print(f"\n  Early-termination demo: arr={already}")
    print(f"    Pass 1: 0 swaps → flag=False → break after {passes} pass → O(n) ✓")

    tests = [
        ([50, 40, 30, 20, 10], [10, 20, 30, 40, 50]),
        ([1],                  [1]),
        ([3, 1, 2],            [1, 2, 3]),
        ([-5, 3, -1, 0, 2],   [-5, -1, 0, 2, 3]),
        ([5, 4, 3, 2, 1],     [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5],     [1, 2, 3, 4, 5]),   # flag triggers on pass 1
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<30} {'result':<30} {'exp':<30} {'ok':>3}")
    print("  " + "─" * 93)
    for a_orig, exp in tests:
        a = a_orig[:]
        bubble_sort(a)
        ok = "✓" if a == exp else "✗"
        print(f"  {str(a_orig):<30} {str(a):<30} {str(exp):<30} {ok:>3}")


# =============================================================================
# SECTION 3: Insertion Sort
# =============================================================================
#
# CORE IDEA: Pick each element (the "key") and INSERT it into its correct
#            position in the already-sorted left portion by shifting larger
#            elements one step right to make room.
#
# MENTAL MODEL: Sorting playing cards in your hand.
#   You pick up one card at a time and slide it left into the correct slot
#   among the cards you're already holding.
#
# VISUAL WALKTHROUGH — arr=[50, 40, 30, 20, 10]:
#
#   Pass 1 (i=1): key=40, sorted=[50]
#     j=0: 50>40? shift 50 right → [50,50,30,20,10]
#     j=-1: stop. Place key at j+1=0 → [40,50,30,20,10]
#
#   Pass 2 (i=2): key=30, sorted=[40,50]
#     j=1: 50>30? shift → j=0: 40>30? shift → [40,40,50,20,10] → place → [30,40,50,20,10]
#
#   Pass 3 (i=3): key=20 — all 3 elements > 20, all shift → [20,30,40,50,10]
#   Pass 4 (i=4): key=10 — all 4 elements > 10, all shift → [10,20,30,40,50] DONE ✓
#
# WHY j+1 IS ALWAYS CORRECT:
#   The while loop stops when EITHER:
#     j < 0             → key is smaller than everything → goes to index 0 = j+1
#     arr[j] <= key     → found right neighbor → key goes RIGHT AFTER arr[j] = j+1
#   In both cases, the correct position is j+1. ✓
#
# BEST CASE — already sorted:
#   arr=[10,20,30,40,50]
#   Pass 1: key=20, compare 10 ≤ 20 → no shift → O(1)
#   Each of n-1 passes: exactly 1 comparison → total = n-1 = O(n)
#
# WHY IS IT STABLE:
#   Shift condition: arr[j] > key (STRICTLY greater)
#   If arr[j] == key: while loop exits → key placed AFTER arr[j] → equal elements keep order.
#
# WHY O(n²) worst case (reverse sorted):
#   Pass i shifts i elements → 1+2+...+(n-1) = n(n-1)/2 = O(n²)
#
# Time Best: O(n) | Worst/Avg: O(n²) | Space: O(1) | Stable: Yes | In-place: Yes
# From Coding_Python/09 & L11/003insertionSort.py

def insertion_sort(arr: List[int]) -> None:
    """
    In-place insertion sort.
    Time: O(n) best (sorted) | O(n²) worst | Space: O(1) | Stable: Yes
    """
    n = len(arr)
    for i in range(1, n):
        key = arr[i]            # element to be inserted
        j = i - 1
        while j >= 0 and arr[j] > key:   # strictly greater → stable
            arr[j + 1] = arr[j]          # shift larger element right
            j -= 1
        arr[j + 1] = key        # place key in the gap (j+1 is always correct)

def insertion_sort_demo():
    print("\n" + "=" * 60)
    print("SECTION 3: Insertion Sort")
    print("=" * 60)

    arr_orig = [50, 40, 30, 20, 10]
    arr = arr_orig[:]
    n = len(arr)
    print(f"\n  arr = {arr}")
    print(f"\n  Pass-by-pass trace (card analogy):")
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        shifts = 0
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            shifts += 1
        arr[j + 1] = key
        print(f"  Pass {i}: key={key}, shifts={shifts}, placed at idx={j+1} → {arr}")

    print(f"\n  j+1 correctness proof:")
    print(f"    Loop exits when j<0 (key is minimum) or arr[j]<=key (found neighbor)")
    print(f"    In both cases, correct slot = j+1 ✓")
    print(f"\n  Stability proof:")
    print(f"    Shift condition: arr[j] > key (STRICTLY greater)")
    print(f"    If arr[j]==key: loop exits → key placed AFTER equal element → STABLE ✓")

    tests = [
        ([50, 40, 30, 20, 10], [10, 20, 30, 40, 50]),
        ([1],                  [1]),
        ([3, 1, 2],            [1, 2, 3]),
        ([-5, 3, -1, 0, 2],   [-5, -1, 0, 2, 3]),
        ([5, 4, 3, 2, 1],     [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5],     [1, 2, 3, 4, 5]),
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<30} {'result':<30} {'exp':<30} {'ok':>3}")
    print("  " + "─" * 93)
    for a_orig, exp in tests:
        a = a_orig[:]
        insertion_sort(a)
        ok = "✓" if a == exp else "✗"
        print(f"  {str(a_orig):<30} {str(a):<30} {str(exp):<30} {ok:>3}")


# =============================================================================
# SECTION 4: DNF Sort (Dutch National Flag) — Sort Colors
# =============================================================================
#
# PROBLEM: Sort an array containing only 0, 1, 2 in a single O(n) pass.
#
# FOUR-REGION INVARIANT at any point during the algorithm:
#
#   index:   [ 0..low-1  ]  [ low..mid-1 ]  [ mid..high ]  [ high+1..n-1 ]
#   content:   zeros zone     ones zone        unknown zone    twos zone
#
#   low  = first index of ones zone (everything left of low = confirmed 0s)
#   mid  = current element being examined (start of unknown zone)
#   high = last element of unknown zone (everything right = confirmed 2s)
#   Goal: shrink unknown zone to zero by moving mid forward or high backward.
#
# THREE CASES:
#
#   Case 1 — arr[mid] == 0: belongs in zeros zone
#     swap arr[low]↔arr[mid], low++, mid++
#     WHY advance mid? The element that came from arr[low] was already in the
#     ones or zeros zone (it was to the left of mid), so it's already processed.
#
#   Case 2 — arr[mid] == 1: already in the ones zone
#     mid++ only (no swap needed)
#
#   Case 3 — arr[mid] == 2: belongs in twos zone
#     swap arr[mid]↔arr[high], high--
#     DO NOT ADVANCE MID! The element that came from arr[high] is from the
#     unknown zone — it must be re-examined on the next iteration.
#
# VISUAL WALKTHROUGH — arr=[2,0,2,1,1,0], low=mid=0, high=5:
#
#   mid=0: arr[0]=2 → Case 3: swap arr[0]↔arr[5] → [0,0,2,1,1,2], high=4
#   mid=0: arr[0]=0 → Case 1: swap arr[0]↔arr[0], low=1, mid=1 → [0,0,2,1,1,2]
#   mid=1: arr[1]=0 → Case 1: swap arr[1]↔arr[1], low=2, mid=2 → [0,0,2,1,1,2]
#   mid=2: arr[2]=2 → Case 3: swap arr[2]↔arr[4] → [0,0,1,1,2,2], high=3
#   mid=2: arr[2]=1 → Case 2: mid=3
#   mid=3: arr[3]=1 → Case 2: mid=4
#   mid=4 > high=3: STOP → [0,0,1,1,2,2] ✓
#
# Time: O(n) | Space: O(1) | In-place: Yes | Stable: No
# From Coding_Python/12 & L14/005dnfSort.py

def dnf_sort(arr: List[int]) -> None:
    """
    Dutch National Flag sort for arrays containing only 0, 1, 2.
    Time: O(n) | Space: O(1)
    Maintains 4-region invariant: [zeros|ones|unknown|twos]
    """
    lo, mid, hi = 0, 0, len(arr) - 1
    while mid <= hi:
        if arr[mid] == 0:
            arr[lo], arr[mid] = arr[mid], arr[lo]
            lo  += 1
            mid += 1              # safe: element from lo was already processed
        elif arr[mid] == 1:
            mid += 1              # already in ones zone
        else:                     # arr[mid] == 2
            arr[mid], arr[hi] = arr[hi], arr[mid]
            hi -= 1               # do NOT advance mid: swapped element is unknown

def dnf_demo():
    print("\n" + "=" * 60)
    print("SECTION 4: DNF Sort (Dutch National Flag)")
    print("=" * 60)

    arr_orig = [2, 0, 2, 1, 1, 0]
    arr = arr_orig[:]
    lo, mid, hi = 0, 0, len(arr) - 1
    print(f"\n  arr = {arr}   (lo={lo}, mid={mid}, hi={hi})")
    print(f"\n  Step-by-step trace:")
    print(f"  [zeros | ones | unknown | twos]")
    step = 0
    while mid <= hi:
        step += 1
        if arr[mid] == 0:
            arr[lo], arr[mid] = arr[mid], arr[lo]
            action = f"Case 1 (0): swap lo={lo}↔mid={mid}, lo={lo+1}, mid={mid+1}"
            lo += 1; mid += 1
        elif arr[mid] == 1:
            action = f"Case 2 (1): mid++ → {mid+1}"
            mid += 1
        else:
            arr[mid], arr[hi] = arr[hi], arr[mid]
            action = f"Case 3 (2): swap mid={mid}↔hi={hi}, hi={hi-1}  [mid STAYS]"
            hi -= 1
        print(f"  Step {step}: {action} → {arr}   lo={lo},mid={mid},hi={hi}")

    print(f"\n  Key rule: Case 3 does NOT advance mid.")
    print(f"    The element swapped in from arr[hi] came from the unknown zone")
    print(f"    and must be re-examined. Advancing mid would skip it.")

    tests = [
        ([2, 0, 2, 1, 1, 0],       [0, 0, 1, 1, 2, 2]),
        ([0],                      [0]),
        ([1, 0, 2],                [0, 1, 2]),
        ([2, 2, 0, 0],             [0, 0, 2, 2]),
        ([0, 0, 0],                [0, 0, 0]),
        ([2, 1, 0],                [0, 1, 2]),
        ([1, 1, 1],                [1, 1, 1]),
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<30} {'result':<20} {'exp':<20} {'ok':>3}")
    print("  " + "─" * 73)
    for a_orig, exp in tests:
        a = a_orig[:]
        dnf_sort(a)
        ok = "✓" if a == exp else "✗"
        print(f"  {str(a_orig):<30} {str(a):<20} {str(exp):<20} {ok:>3}")


# =============================================================================
# SECTION 5: Counting Sort — Breaking the O(n log n) Barrier
# =============================================================================
#
# CORE IDEA: Instead of COMPARING elements, COUNT how many times each value
#            appears, then RECONSTRUCT the array from the counts.
#
# HOW IT BREAKS THE COMPARISON LOWER BOUND:
#   Comparison sorts must handle n! possible orderings via binary decisions.
#   A comparison tree needs at least log₂(n!) ≈ n·log n levels → Ω(n log n).
#   Counting sort NEVER compares two array elements against each other.
#   It uses each value as a DIRECT ARRAY INDEX: freq[x] += 1.
#   This sidesteps the comparison lower bound entirely.
#
# THE FREQ ARRAY AS AN O(1) DICTIONARY:
#   arr = [4, 2, 2, 8, 3, 3, 1]   K = max(arr) = 8
#
#   freq = [0]*9   ← size K+1; think of freq as a mapping: value → count
#
#   Counting pass (O(n)):
#     freq[4]+=1, freq[2]+=1, freq[2]+=1, freq[8]+=1, ...
#     freq = [0, 1, 2, 2, 1, 0, 0, 0, 1]
#            idx: 0  1  2  3  4  5  6  7  8
#
#   Read as: "value 1 appears 1 time, value 2 appears 2 times, ..."
#   freq[x] = "how many times does value x appear?" — O(1) lookup by index.
#
#   Reconstruction pass (O(n+K)):
#     For i = 0..K:  write value i exactly freq[i] times
#     Result: [1, 2, 2, 3, 3, 4, 8] ✓
#
# TOTAL: O(n) count + O(n+K) reconstruct = O(n+K)
#
# LIMITATION: Only works for non-negative integers in a small range K.
#             If K >> n (sparse), the freq array wastes space and time.
#
# Time: O(n+K) | Space: O(K) | Stable: Yes | In-place: No (uses freq array)
# From Coding_Python/09 & L14/006countingSort.py

def counting_sort(arr: List[int]) -> None:
    """
    Counting sort for non-negative integers with small range K.
    Time: O(n+K) | Space: O(K) — breaks comparison lower bound via direct indexing.
    """
    if not arr:
        return
    k = max(arr)                    # K = range of values
    freq = [0] * (k + 1)           # freq[x] = count of value x  (O(1) lookup)

    for num in arr:                 # counting pass: O(n)
        freq[num] += 1

    idx = 0
    for num in range(k + 1):       # reconstruction pass: O(n+K)
        while freq[num] > 0:
            arr[idx] = num
            idx += 1
            freq[num] -= 1

def counting_sort_demo():
    print("\n" + "=" * 60)
    print("SECTION 5: Counting Sort")
    print("=" * 60)

    arr = [4, 2, 2, 8, 3, 3, 1]
    k = max(arr)
    freq = [0] * (k + 1)
    for x in arr:
        freq[x] += 1

    print(f"\n  arr = {arr}   K = max(arr) = {k}")
    print(f"\n  Freq array after counting pass (O(n)):")
    print(f"  idx:  {list(range(k+1))}")
    print(f"  freq: {freq}")
    print(f"\n  Read as: freq[x] = 'how many times does value x appear?'")
    print(f"  This is an O(1) dictionary lookup via direct indexing — no comparisons.")
    print(f"\n  Reconstruction pass (O(n+K)):")
    result = []
    for num in range(k + 1):
        for _ in range(freq[num]):
            result.append(num)
    print(f"  Write each value i exactly freq[i] times:")
    print(f"  Result: {result}")
    print(f"\n  Barrier-breaking: freq[x]+=1 uses values as indices (no element comparisons)")
    print(f"  Comparison lower bound Ω(n log n) does NOT apply → O(n+K) is valid")

    tests = [
        ([4, 2, 2, 8, 3, 3, 1], [1, 2, 2, 3, 3, 4, 8]),
        ([1],                    [1]),
        ([3, 1, 2],              [1, 2, 3]),
        ([0, 0, 0],              [0, 0, 0]),
        ([5, 1, 3, 5, 1],       [1, 1, 3, 5, 5]),
        ([10, 0, 5],             [0, 5, 10]),
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<30} {'result':<25} {'exp':<25} {'ok':>3}")
    print("  " + "─" * 82)
    for a_orig, exp in tests:
        a = a_orig[:]
        counting_sort(a)
        ok = "✓" if a == exp else "✗"
        print(f"  {str(a_orig):<30} {str(a):<25} {str(exp):<25} {ok:>3}")


# =============================================================================
# SECTION 6: Generalized Counting Sort — Handles Negatives
# =============================================================================
#
# PROBLEM: Counting sort requires freq[x] where x is a valid array index (≥0).
#          Negative numbers can't be used as indices.
#
# TRICK: Shift by min_val so the range starts at 0.
#
#   freq[x - min_val] += 1   ← shifted index (always ≥ 0)
#   freq array size = max_val - min_val + 1 = K
#
# STEP-BY-STEP — arr=[-3, -1, -2, 0, -1]:
#
#   min_val=-3, max_val=0, K = 0-(-3)+1 = 4
#   freq = [0, 0, 0, 0]   ← size 4
#
#   Counting pass:
#     -3 → freq[-3-(-3)]=freq[0]+=1 → freq[0]=1
#     -1 → freq[-1-(-3)]=freq[2]+=1 → freq[2]=1
#     -2 → freq[-2-(-3)]=freq[1]+=1 → freq[1]=1
#      0 → freq[0-(-3)] =freq[3]+=1 → freq[3]=1
#     -1 → freq[2]+=1                → freq[2]=2
#   freq = [1, 1, 2, 1]
#
#   Reconstruction pass (un-shift: value = shifted_index + min_val):
#     i=0: write 0+(-3) = -3  (1 time)
#     i=1: write 1+(-3) = -2  (1 time)
#     i=2: write 2+(-3) = -1  (2 times)
#     i=3: write 3+(-3) =  0  (1 time)
#   Result: [-3, -2, -1, -1, 0] ✓
#
# WHY THIS WORKS:
#   Shifting maps [min_val .. max_val] to [0 .. K-1] — a valid index range.
#   The sort is identical to standard counting sort on the shifted values.
#   Un-shifting on reconstruction restores original values.
#
# Time: O(n + K) where K = max_val - min_val | Space: O(K)
# From L14/007generalizedCountingSort.py

def generalized_counting_sort(arr: List[int]) -> None:
    """
    Counting sort for any integer range (including negatives).
    Time: O(n+K), K = max_val - min_val | Space: O(K)
    Trick: shift all values by min_val so indices start at 0.
    """
    if not arr:
        return
    min_val = min(arr)
    max_val = max(arr)
    k       = max_val - min_val

    freq = [0] * (k + 1)

    for num in arr:                     # count with shifted index
        freq[num - min_val] += 1

    idx = 0
    for i in range(k + 1):             # reconstruct with un-shifted value
        while freq[i] > 0:
            arr[idx] = i + min_val      # un-shift: i + min_val = original value
            idx += 1
            freq[i] -= 1

def generalized_demo():
    print("\n" + "=" * 60)
    print("SECTION 6: Generalized Counting Sort (Handles Negatives)")
    print("=" * 60)

    arr = [-3, -1, -2, 0, -1]
    mn, mx = min(arr), max(arr)
    k = mx - mn
    freq_d = [0] * (k + 1)
    for x in arr:
        freq_d[x - mn] += 1

    print(f"\n  arr = {arr}")
    print(f"  min_val={mn}, max_val={mx}, K={k+1} slots needed")
    print(f"\n  Shift derivation:")
    for x in arr:
        print(f"    {x:>3} → freq[{x} - ({mn})] = freq[{x-mn}]  (shifted index)")
    print(f"\n  freq = {freq_d}   (indices 0..{k})")
    print(f"\n  Reconstruction (un-shift: value = i + min_val):")
    result = []
    for i in range(k + 1):
        for _ in range(freq_d[i]):
            result.append(i + mn)
            print(f"    i={i}: write {i}+({mn}) = {i+mn}")
    print(f"  Result: {result} ✓")

    tests = [
        ([-3, -1, -2, 0, -1],   [-3, -2, -1, -1, 0]),
        ([-5, -5, -5],           [-5, -5, -5]),
        ([-2, 0, -1],            [-2, -1, 0]),
        ([0, 0, 0],              [0, 0, 0]),
        ([-10, 5, -3, 2, -7],   [-10, -7, -3, 2, 5]),
        ([1, -1, 0],             [-1, 0, 1]),
    ]
    print(f"\n  Verification:")
    print(f"  {'arr':<35} {'result':<25} {'exp':<25} {'ok':>3}")
    print("  " + "─" * 88)
    for a_orig, exp in tests:
        a = a_orig[:]
        generalized_counting_sort(a)
        ok = "✓" if a == exp else "✗"
        print(f"  {str(a_orig):<35} {str(a):<25} {str(exp):<25} {ok:>3}")


# =============================================================================
# SECTION 7: Python Built-in Sorting — Timsort
# =============================================================================
#
# Python provides two ways to sort:
#   sorted(lst)  → returns a NEW sorted list; original unchanged; O(n log n)
#   lst.sort()   → sorts IN-PLACE; returns None; O(n log n)
#
# Both accept:
#   reverse=True          → sort in descending order
#   key=func              → apply func to each element before comparison
#
# TIMSORT (Python's algorithm):
#   Hybrid of Merge Sort + Insertion Sort.
#   - Divides array into "runs" (already-sorted sub-sequences)
#   - Sorts small runs (length ≤ 64) with Insertion Sort
#   - Merges runs with Merge Sort
#   - O(n log n) worst case, O(n) best case (already sorted)
#   - STABLE: preserves order of equal elements
#
# From Coding_Python/09 & L11/004sorted.py

def timsort_demo():
    print("\n" + "=" * 60)
    print("SECTION 7: Python Built-in Sorting (Timsort)")
    print("=" * 60)

    nums  = [30, 10, 20, 50, 40]
    print(f"\n  sorted() — returns new list, original unchanged:")
    print(f"  nums = {nums}")
    print(f"  sorted(nums)             = {sorted(nums)}")
    print(f"  sorted(nums, reverse=True) = {sorted(nums, reverse=True)}")
    print(f"  nums after sorted()      = {nums}  ← unchanged ✓")

    temp = [87, 90, 95, 76, 98]
    temp.sort(reverse=True)
    print(f"\n  .sort() — in-place, returns None:")
    print(f"  [87,90,95,76,98].sort(reverse=True) → {temp}")

    animals = ["ch", "ze", "al", "be", "ti"]
    print(f"\n  Lexicographic (alphabetical) sort:")
    print(f"  sorted({animals}) = {sorted(animals)}")

    names = ["ifrah", "aryan", "avi", "aditya", "yash"]
    print(f"\n  key= parameter (sort by length):")
    print(f"  sorted({names}, key=len) = {sorted(names, key=len)}")

    pairs = [(3, 1), (2, 0), (1, 3), (4, 2)]
    print(f"\n  Lambda key (sort tuples by second element, descending):")
    print(f"  sorted({pairs}, key=lambda p: p[1], reverse=True)")
    print(f"  = {sorted(pairs, key=lambda p: p[1], reverse=True)}")

    print(f"\n  Timsort = Merge Sort + Insertion Sort hybrid")
    print(f"  O(n log n) worst | O(n) best (already sorted) | Stable: Yes")
    print(f"  Uses Insertion Sort for subarrays ≤ 64 elements (highly cache-friendly)")


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_selection_sort(arr: List[int]) -> None:
    """
    In-place selection sort.
    Time: O(n²) | Space: O(1) | Stable: No
    Hint: for i in range(n): find min_idx in arr[i..n-1]; swap arr[i]↔arr[min_idx]
    """
    pass

def practice_bubble_sort(arr: List[int]) -> None:
    """
    In-place bubble sort with early-termination flag.
    Time: O(n²) worst, O(n) best | Space: O(1) | Stable: Yes
    Hint: flag=False per pass; swap if arr[j]>arr[j+1]; break if not flag
    """
    pass

def practice_insertion_sort(arr: List[int]) -> None:
    """
    In-place insertion sort.
    Time: O(n²) worst, O(n) best | Space: O(1) | Stable: Yes
    Hint: key=arr[i]; while j>=0 and arr[j]>key: shift right; arr[j+1]=key
    """
    pass

def practice_dnf_sort(arr: List[int]) -> None:
    """
    Dutch National Flag sort (0,1,2 only).
    Time: O(n) | Space: O(1)
    Hint: lo=mid=0, hi=n-1; 3 cases on arr[mid]; Case 3 does NOT advance mid
    """
    pass

def practice_counting_sort(arr: List[int]) -> None:
    """
    Counting sort for non-negative integers, small range K.
    Time: O(n+K) | Space: O(K)
    Hint: freq[x]+=1; then write each value freq[x] times
    """
    pass

def practice_generalized_counting_sort(arr: List[int]) -> None:
    """
    Counting sort for any integer range (including negatives).
    Time: O(n+K), K=max-min | Space: O(K)
    Hint: shift: freq[x-min_val]; un-shift: write i+min_val
    """
    pass


# =============================================================================
# DRIVER — Verifies all optimal implementations + shows skeleton stubs
# =============================================================================
if __name__ == "__main__":
    selection_sort_demo()
    bubble_sort_demo()
    insertion_sort_demo()
    dnf_demo()
    counting_sort_demo()
    generalized_demo()
    timsort_demo()

    print("\n" + "=" * 60)
    print("OPTIMAL SOLUTION VERIFICATION")
    print("=" * 60)

    # Shared test cases for comparison sorts (all sorts must produce same output)
    comparison_tests = [
        ([50, 20, 30, 10, 40], [10, 20, 30, 40, 50]),
        ([1],                  [1]),
        ([3, 1, 2],            [1, 2, 3]),
        ([-5, 3, -1, 0, 2],   [-5, -1, 0, 2, 3]),
        ([5, 4, 3, 2, 1],     [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5],     [1, 2, 3, 4, 5]),
    ]

    # ── Selection Sort ──
    for a_orig, exp in comparison_tests:
        a = a_orig[:]
        selection_sort(a)
        assert a == exp, f"selection_sort failed on {a_orig}: got {a}"
    print(f"\n  selection_sort: {len(comparison_tests)} assertions ✓")

    # ── Bubble Sort ──
    for a_orig, exp in comparison_tests:
        a = a_orig[:]
        bubble_sort(a)
        assert a == exp, f"bubble_sort failed on {a_orig}: got {a}"
    print(f"  bubble_sort:    {len(comparison_tests)} assertions ✓")

    # ── Insertion Sort ──
    for a_orig, exp in comparison_tests:
        a = a_orig[:]
        insertion_sort(a)
        assert a == exp, f"insertion_sort failed on {a_orig}: got {a}"
    print(f"  insertion_sort: {len(comparison_tests)} assertions ✓")

    # ── DNF Sort ──
    dnf_tests = [
        ([2, 0, 2, 1, 1, 0],  [0, 0, 1, 1, 2, 2]),
        ([0],                  [0]),
        ([1, 0, 2],            [0, 1, 2]),
        ([2, 2, 0, 0],        [0, 0, 2, 2]),
        ([0, 0, 0],            [0, 0, 0]),
        ([2, 1, 0],            [0, 1, 2]),
        ([1, 1, 1],            [1, 1, 1]),
    ]
    for a_orig, exp in dnf_tests:
        a = a_orig[:]
        dnf_sort(a)
        assert a == exp, f"dnf_sort failed on {a_orig}: got {a}"
    print(f"  dnf_sort:       {len(dnf_tests)} assertions ✓")

    # ── Counting Sort ──
    counting_tests = [
        ([4, 2, 2, 8, 3, 3, 1], [1, 2, 2, 3, 3, 4, 8]),
        ([1],                    [1]),
        ([3, 1, 2],              [1, 2, 3]),
        ([0, 0, 0],              [0, 0, 0]),
        ([5, 1, 3, 5, 1],       [1, 1, 3, 5, 5]),
        ([10, 0, 5],             [0, 5, 10]),
    ]
    for a_orig, exp in counting_tests:
        a = a_orig[:]
        counting_sort(a)
        assert a == exp, f"counting_sort failed on {a_orig}: got {a}"
    print(f"  counting_sort:  {len(counting_tests)} assertions ✓")

    # ── Generalized Counting Sort ──
    gen_tests = [
        ([-3, -1, -2, 0, -1],   [-3, -2, -1, -1, 0]),
        ([-5, -5, -5],           [-5, -5, -5]),
        ([-2, 0, -1],            [-2, -1, 0]),
        ([0, 0, 0],              [0, 0, 0]),
        ([-10, 5, -3, 2, -7],   [-10, -7, -3, 2, 5]),
        ([1, -1, 0],             [-1, 0, 1]),
    ]
    for a_orig, exp in gen_tests:
        a = a_orig[:]
        generalized_counting_sort(a)
        assert a == exp, f"generalized_counting_sort failed on {a_orig}: got {a}"
    print(f"  generalized_counting_sort: {len(gen_tests)} assertions ✓")

    total = len(comparison_tests) * 3 + len(dnf_tests) + len(counting_tests) + len(gen_tests)
    print(f"\n  {'─'*40}")
    print(f"  Total verified assertions: {total} ✓")
    print(f"  {'─'*40}")

    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS (return None until implemented)")
    print("=" * 60)

    arr_test  = [3, 1, 4, 1, 5, 9, 2, 6]
    dnf_test  = [2, 0, 1, 2, 0, 1]
    cnt_test  = [4, 2, 2, 8, 3, 3, 1]
    gen_test  = [-3, -1, -2, 0, -1]

    a1 = arr_test[:]
    practice_selection_sort(a1)
    print(f"\n  practice_selection_sort({arr_test})  = {a1}")

    a2 = arr_test[:]
    practice_bubble_sort(a2)
    print(f"  practice_bubble_sort({arr_test})     = {a2}")

    a3 = arr_test[:]
    practice_insertion_sort(a3)
    print(f"  practice_insertion_sort({arr_test})  = {a3}")

    a4 = dnf_test[:]
    practice_dnf_sort(a4)
    print(f"\n  practice_dnf_sort({dnf_test}) = {a4}")

    a5 = cnt_test[:]
    practice_counting_sort(a5)
    print(f"  practice_counting_sort({cnt_test}) = {a5}")

    a6 = gen_test[:]
    practice_generalized_counting_sort(a6)
    print(f"  practice_generalized_counting_sort({gen_test}) = {a6}")

    print("=" * 60)
    print("Fill in the skeletons above and re-run to verify.")
    print("\n" + "=" * 60)
    print("  CURRICULUM COMPLETE: Modules 01 - 12 ✓")
    print("=" * 60)
