# 12 - Classical Sorting Algorithms

## Why This Module Matters

Sorting is the most studied problem in Computer Science. You will almost always use Python's built-in `list.sort()` (Timsort, O(n log n)) in real code — but interviewers test the algorithms because each one illustrates a different algorithmic technique: selection, bubble propagation, insertion, partitioning, and counting. The linear-time sorts (DNF, Counting) break the O(n log n) comparison barrier entirely.

---

## 1. Core Vocabulary

### Stability

A sorting algorithm is **stable** if it preserves the **relative order of equal elements**.

```
Input:  [(A, 3), (B, 1), (C, 3)]   sorted by number

Stable:   [(B, 1), (A, 3), (C, 3)]   ← A still before C (original order kept)
Unstable: [(B, 1), (C, 3), (A, 3)]   ← C before A (original order BROKEN)
```

**Why it matters:** Imagine you first sort employees by name, then sort by department. A stable sort guarantees employees within the same department remain alphabetically ordered. An unstable sort can destroy a prior sort.

### In-Place

An algorithm is **in-place** if it sorts the array by modifying it directly, **without allocating a new array proportional to n**.

- `O(1)` extra space = in-place (only a few variables)
- `O(n)` extra space = **not** in-place (e.g., merge sort, counting sort)

All three O(n²) sorts in this module are **in-place**. DNF sort is **in-place**. Counting sort is **not** (uses `O(K)` extra space for the frequency array).

---

## 2. The O(n²) Comparison Sorts

### Selection Sort

**Core idea:** In each pass, **find the minimum** in the unsorted portion and **swap it to the frontier**.

**Mental model:** A growing boundary. Everything left of `|` is final. Each pass scans right of `|`, finds the minimum, and places it at `|`.

```
arr = [50, 20, 30, 10, 40]

Pass 1 (i=0): scan [50,20,30,10,40] → min=10 at idx 3 → swap arr[0]↔arr[3]
  [10, 20, 30, 50, 40]   10 is FINAL

Pass 2 (i=1): scan [20,30,50,40]    → min=20 at idx 1 → swap arr[1]↔arr[1] (no-op)
  [10, 20, 30, 50, 40]   20 is FINAL

Pass 3 (i=2): scan [30,50,40]       → min=30 at idx 2 → no-op
  [10, 20, 30, 50, 40]   30 is FINAL

Pass 4 (i=3): scan [50,40]          → min=40 at idx 4 → swap arr[3]↔arr[4]
  [10, 20, 30, 40, 50]   DONE ✓
```

**Why NOT stable:** Consider `[4a, 4b, 1]` (4a and 4b are both value 4, subscript shows original order):
- Pass 1: min=1 at idx 2, swap arr[0]↔arr[2] → `[1, 4b, 4a]`
- Now 4b precedes 4a — **original order of equal elements is broken!**

**Why minimum swaps:** Selection sort does at most `n-1` swaps total (one per pass). Bubble sort can do `O(n²)` swaps. Use Selection Sort when **writing** (swapping) is expensive.

**Complexity:**
- Best / Worst / Average: **O(n²)** — always scans full unsorted portion
- Space: **O(1)** | Stable: **No** | In-place: **Yes**

---

### Bubble Sort (with Early-Termination Flag)

**Core idea:** Walk through the array, **swap adjacent pairs** that are out of order. The largest unsorted element "bubbles" to the end each pass.

**Mental model:** Like air bubbles rising through water — the heaviest (largest) element floats one step right at a time until it reaches the surface (end of array).

```
arr = [50, 40, 30, 20, 10]

Pass 1: compare all adjacent pairs in [50,40,30,20,10]
  j=0: 50>40? swap → [40,50,30,20,10]
  j=1: 50>30? swap → [40,30,50,20,10]
  j=2: 50>20? swap → [40,30,20,50,10]
  j=3: 50>10? swap → [40,30,20,10,50]   ← 50 bubbled to its final position

Pass 2: compare in [40,30,20,10 | 50]
  → [30,20,10,40,50]   ← 40 in place

Pass 3: compare in [30,20,10 | 40,50]
  → [20,10,30,40,50]   ← 30 in place

Pass 4: compare in [20,10 | 30,40,50]
  → [10,20,30,40,50]   DONE ✓
```

**The `flag` Early-Termination Optimization:**
- Before each pass, set `flag = False`
- If a swap happens, set `flag = True`
- If the pass ends with `flag == False` → **no swaps happened → array is already sorted → STOP**

```python
# Best case: arr=[10,20,30,40,50] (already sorted)
# Pass 1: compare 4 pairs, zero swaps → flag=False → break
# Total work: n-1 comparisons = O(n)
```

**Why IS stable:** The only swap condition is `arr[j] > arr[j+1]` (strictly greater). If `arr[j] == arr[j+1]`, **no swap occurs** — equal elements never cross each other.

**Why O(n²):** Without the flag:
```
Pass 1: n-1 comparisons
Pass 2: n-2 comparisons
...
Total = (n-1)+(n-2)+...+1 = n(n-1)/2 = O(n²)
```

**Complexity:**
- Best: **O(n)** (sorted — flag fires on pass 1) | Worst/Average: **O(n²)**
- Space: **O(1)** | Stable: **Yes** | In-place: **Yes**

---

### Insertion Sort

**Core idea:** Pick each element (the "key") and **insert** it into its correct position in the already-sorted portion to its left by shifting larger elements right.

**Mental model:** Sorting playing cards in your hand. You pick up one card at a time and slide it left into the correct slot among the cards you're already holding.

```
arr = [50, 40, 30, 20, 10]

Pass 1 (i=1): key=40, sorted=[50]
  j=0: arr[0]=50 > 40? YES → shift 50 right → [50,50,30,20,10]
  j=-1: stop. Place key at j+1=0 → [40,50,30,20,10]

Pass 2 (i=2): key=30, sorted=[40,50]
  j=1: 50>30? YES → shift → [40,50,50,20,10]
  j=0: 40>30? YES → shift → [40,40,50,20,10]
  j=-1: stop. Place key at 0 → [30,40,50,20,10]

Pass 3 (i=3): key=20, sorted=[30,40,50]
  All > 20, shift all → Place at 0 → [20,30,40,50,10]

Pass 4 (i=4): key=10, shift all → [10,20,30,40,50]  DONE ✓
```

**Why `j+1` is always the correct slot:** The `while` loop stops when either `j < 0` (key is smaller than everything) or `arr[j] <= key` (found the right neighbor). In both cases, the key belongs at `j+1`.

**Best case — already sorted:**
```
arr=[10,20,30,40,50]
Pass 1: key=20, compare with 10 → 10 <= 20 → no shift → O(1)
Each of n-1 passes does exactly 1 comparison → total = n-1 = O(n)
```

**Why IS stable:** We only shift elements that are **strictly greater** than the key. Equal elements are never shifted past the key.

**Complexity:**
- Best: **O(n)** (sorted) | Worst/Average: **O(n²)** (reverse sorted)
- Space: **O(1)** | Stable: **Yes** | In-place: **Yes**

---

## 3. O(n²) Comparison Table

| Algorithm | Best | Worst | Avg | Space | Stable | In-place | Key operation |
|---|---|---|---|---|---|---|---|
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | **No** | Yes | Find min, swap |
| Bubble Sort | **O(n)** | O(n²) | O(n²) | O(1) | **Yes** | Yes | Swap adjacent |
| Insertion Sort | **O(n)** | O(n²) | O(n²) | O(1) | **Yes** | Yes | Shift and insert |

**When to use which:**
- **Selection:** fewest write operations (only n-1 swaps). Use when writes are expensive.
- **Bubble:** simplest, detects already-sorted fastest with flag. Good for teaching.
- **Insertion:** best for nearly-sorted or small arrays. Python's Timsort uses insertion sort for subarrays of length ≤ 64.

---

## 4. The O(n log n) Comparison Lower Bound

Any algorithm that sorts by **comparing elements** requires at least **Ω(n log n)** comparisons in the worst case.

**Why?** With `n` elements there are `n!` possible orderings. A comparison tree has 2^h leaves at depth h. To distinguish all orderings: `2^h ≥ n!` → `h ≥ log₂(n!) ≈ n log n` (Stirling's approximation).

This means Selection/Bubble/Insertion (O(n²)) are provably suboptimal. Timsort (O(n log n)) hits the lower bound. **The only way to beat O(n log n) is to stop comparing elements** — which Counting Sort and DNF Sort do.

---

## 5. DNF Sort (Dutch National Flag) — O(n)

**Problem:** Sort an array containing only `0`, `1`, `2` in a single pass.

**Why the name?** The Dutch flag has three horizontal bands (red/white/blue), like three value categories.

**Four-Region Invariant:**

At any moment, the array is divided into **four regions** by three pointers:

```
index:   [  0 .. low-1 ]  [ low .. mid-1 ]  [ mid .. high ]  [ high+1 .. n-1 ]
content:    zeros zone       ones zone          unknown zone      twos zone
```

- `low`: first index of the ones zone (everything left of `low` = confirmed 0s)
- `mid`: current element being examined (start of unknown zone)
- `high`: last element of unknown zone (everything right = confirmed 2s)

**The three cases:**
1. `arr[mid] == 0` → belongs in zeros zone: swap `arr[low]↔arr[mid]`, `low++`, `mid++`
   - Safe to advance `mid`: the element at `arr[low]` was already processed (in 0s or 1s zone)
2. `arr[mid] == 1` → already in the right zone: `mid++`
3. `arr[mid] == 2` → belongs in twos zone: swap `arr[mid]↔arr[high]`, `high--`
   - **Do NOT advance `mid`!** The element that came from `arr[high]` is from the unknown zone and must be re-examined on the next iteration.

**Complexity:** O(n) Time | O(1) Space | In-place: **Yes** | Stable: **No**

---

## 6. Counting Sort — Breaking the O(n log n) Barrier

**Core idea:** Instead of comparing elements, **count how many times each value appears**, then reconstruct the array from the counts.

**How it breaks the comparison barrier:**
- Comparison sorts must distinguish n! orderings via binary decisions → at least Ω(n log n).
- Counting sort **never compares two array elements against each other**. It uses the value as a direct array index: `freq[x] += 1`. This sidesteps the comparison lower bound entirely.

**The freq array as an O(1) dictionary:**
```
arr = [4, 2, 2, 8, 3, 3, 1]
K = max(arr) = 8
freq = [0, 0, 0, 0, 0, 0, 0, 0, 0]  ← size K+1

After counting:
freq[1]=1, freq[2]=2, freq[3]=2, freq[4]=1, freq[8]=1

Think of it as: freq[x] = "how many times does value x appear?"
Direct index access: O(1) per lookup, O(n) total.

Reconstruct: iterate i=0..K, write value i exactly freq[i] times.
Result: [1, 2, 2, 3, 3, 4, 8] ✓
```

**Limitation:** Only works for **non-negative integers** in a small, known range K. If K >> n (sparse values), the freq array wastes space and time.

**Complexity:** O(n+K) Time | O(K) Space | In-place: **No** | Stable: **Yes** (if done via cumulative freq; basic version below is stable by construction)

---

## 7. Generalized Counting Sort — Handles Negatives

**Problem:** What if the array contains negative numbers?

**Trick: shift by `min_val`** so the range starts at 0:
```
arr = [-3, -1, -2, 0, -1]
min_val = -3, max_val = 0, range = 0 - (-3) = 3

Shifted indices:
  -3 → freq[-3 - (-3)] = freq[0]
  -1 → freq[-1 - (-3)] = freq[2]
  -2 → freq[-2 - (-3)] = freq[1]
   0 → freq[0  - (-3)] = freq[3]

freq = [1, 1, 2, 1]  ← size = max-min+1 = 4

Reconstruct: value at shifted index i = i + min_val
  i=0: write -3  (1 time)
  i=1: write -2  (1 time)
  i=2: write -1  (2 times)
  i=3: write  0  (1 time)
Result: [-3, -2, -1, -1, 0] ✓
```

**Complexity:** O(n + (max-min)) Time | O(max-min+1) Space

---

## 8. Python's Built-in Sorting — Timsort

Python provides two ways to sort:

```python
sorted(list)    # returns a NEW sorted list; original unchanged; O(n log n)
list.sort()     # sorts IN-PLACE; returns None; O(n log n)
```

Both accept `key=` (function applied to each element before comparison) and `reverse=True`.

**Timsort** is a hybrid of Merge Sort + Insertion Sort:
- Divides array into "runs" (already-sorted chunks)
- Sorts small runs with Insertion Sort (fast for small/nearly-sorted data)
- Merges runs with Merge Sort (O(n log n) worst case)
- **Stable** and O(n log n) worst case — hits the comparison lower bound

---

## 9. Algorithm Decision Guide

> [!TIP]
> | Situation | Best Choice | Why |
> |---|---|---|
> | Array of only 0s, 1s, 2s | **DNF Sort** O(n)/O(1) | 3-pointer single pass |
> | Integer range `[0..K]`, K is small | **Counting Sort** O(n+K)/O(K) | No comparisons |
> | Integer range `[L..R]`, includes negatives | **Generalized Counting Sort** | Shift by min |
> | Nearly sorted, small array | **Insertion Sort** O(n) best | Minimal shifts |
> | Fewest memory writes needed | **Selection Sort** | Only n-1 swaps |
> | General purpose | **`arr.sort()`** Timsort | O(n log n) proven optimal |

> [!WARNING]
> **Counting Sort K trap:** If K is very large (e.g., values up to 10⁹), the O(K) space and time is catastrophic. Always ask: "What is the range of values?" before choosing counting sort.
