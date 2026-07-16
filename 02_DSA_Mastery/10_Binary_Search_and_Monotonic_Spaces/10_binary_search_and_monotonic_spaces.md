# 10 - Binary Search and Monotonic Spaces

## Why This Module Matters

Linear search checks every element → **O(n)**. Binary search eliminates **half the remaining search space** at every step → **O(log n)**. For an array of 1,000,000 elements:

| Algorithm | Worst-case comparisons |
|---|---|
| Linear Search | 1,000,000 |
| Binary Search | **~20** (log₂(1,000,000) ≈ 20) |

---

## 1. Monotonic Functions — The Prerequisite

> **Definition:** A function is **monotonic** if its output only ever moves in **one direction** as the input increases — never reversing.

Two flavours:

| Name | Behaviour | Example |
|---|---|---|
| **Monotonically non-decreasing** | Each value ≥ the previous | `[1, 2, 2, 3, 5]` (sorted ascending) |
| **Monotonically non-increasing** | Each value ≤ the previous | `[9, 7, 4, 4, 1]` (sorted descending) |

**Why this matters for Binary Search:**

A sorted array is a monotonic function where the index is the input and the value is the output. Because the function only moves in one direction, at every step we can ask *"Is the target to the left or right of mid?"* and immediately **discard the half that cannot contain it**. This is impossible on unsorted data — any element could be anywhere.

> [!IMPORTANT]
> Binary search works on any **monotonic search space** — not just sorted arrays. It can be applied to any problem where there is a clear YES/NO boundary that only crosses once.

---

## 2. Why O(log n)? — The Derivation (Not Just Memorisation)

At each iteration, the search space is **cut in half**:

$$n \;\to\; \frac{n}{2} \;\to\; \frac{n}{4} \;\to\; \frac{n}{8} \;\to\; \cdots \;\to\; 1$$

After $k$ steps, the search space is $\frac{n}{2^k}$. It reaches 1 when:

$$\frac{n}{2^k} = 1 \;\;\Longrightarrow\;\; 2^k = n \;\;\Longrightarrow\;\; k = \log_2 n$$

That is the number of iterations — **O(log n)**.

**How to recognise O(log n) in code:**
- `lo` and `hi` converge toward each other by **halving** (`mid = (lo + hi) // 2`)
- Or a variable **doubles or halves** each iteration (`i *= 2` or `i //= 2`)

---

## 3. The `(lo + hi) // 2` Breakdown

```python
mid = (lo + hi) // 2
```

| Piece | Meaning |
|---|---|
| `lo + hi` | Sum of the two boundary indices |
| `// 2` | **Integer** (floor) division — result is always an integer index |
| Result | Always satisfies `lo ≤ mid ≤ hi` — never goes out of bounds |

> [!WARNING]
> In **Python**, integer arithmetic never overflows, so `(lo + hi) // 2` is always safe. In **Java/C++**, `lo + hi` can overflow for very large indices — use `lo + (hi - lo) // 2` there.

---

## 4. Standard Binary Search

**Condition to enter loop:** `lo <= hi` (search space has at least one element).

**Three cases on each iteration:**

```
arr[mid] == target  →  FOUND — return mid
arr[mid] <  target  →  target is to the RIGHT → lo = mid + 1  (discard left half)
arr[mid] >  target  →  target is to the LEFT  → hi = mid - 1  (discard right half)
```

**Visual walkthrough** for `arr = [10, 20, 30, 40, 50, 60, 70]`, `target = 50`:

```
idx:   0   1   2   3   4   5   6
arr:  [10, 20, 30, 40, 50, 60, 70]
       lo                       hi    mid=3 → arr[3]=40 < 50 → lo=4  (discard [0..3])

                        lo       hi   mid=5 → arr[5]=60 > 50 → hi=4  (discard [5..6])

                        lo,hi         mid=4 → arr[4]=50 == 50 → FOUND at index 4 ✓

Search space: 7 → 3 → 1  (halved each step) → O(log n)
```

**Time: O(log n) | Space: O(1)** (only `lo`, `hi`, `mid` — no extra arrays)

---

## 5. First Occurrence in Sorted Array

**Problem:** Array has duplicates. Find the **leftmost** (smallest index) occurrence.

**Key modification:** When `arr[mid] == target`, do **NOT** return immediately. Instead:
1. Save `ans = mid` (potential answer)
2. Keep searching **LEFT** → `hi = mid - 1`

**Visual walkthrough** for `arr = [10, 20, 30, 30, 30, 30, 30, 40, 50]`, `target = 30`:

```
idx:   0   1   2   3   4   5   6   7   8
arr:  [10, 20, 30, 30, 30, 30, 30, 40, 50]

Step 1: lo=0, hi=8 → mid=4 → arr[4]=30 == 30 → ans=4, hi=3  (search LEFT)
Step 2: lo=0, hi=3 → mid=1 → arr[1]=20 <  30 → lo=2          (go right)
Step 3: lo=2, hi=3 → mid=2 → arr[2]=30 == 30 → ans=2, hi=1  (search LEFT)
Step 4: lo=2, hi=1 → lo > hi → STOP

Answer: ans = 2 ✓  (the first 30 is at index 2)
```

> [!NOTE]
> Still O(log n): every iteration still moves either `lo` or `hi` by halving. Recording `ans` and continuing does not add any extra iterations.

---

## 6. Last Occurrence in Sorted Array

**Key difference from First Occurrence:** On a match, search **RIGHT** → `lo = mid + 1`.

**Visual walkthrough** for same array, `target = 30`:

```
Step 1: lo=0, hi=8 → mid=4 → arr[4]=30 == 30 → ans=4, lo=5  (search RIGHT)
Step 2: lo=5, hi=8 → mid=6 → arr[6]=30 == 30 → ans=6, lo=7  (search RIGHT)
Step 3: lo=7, hi=8 → mid=7 → arr[7]=40 >  30 → hi=6          (go left)
Step 4: lo=7, hi=6 → lo > hi → STOP

Answer: ans = 6 ✓  (the last 30 is at index 6)
```

---

## 7. Comparison Table: All Three Variants

| Function | On `arr[mid] == target` | Returns |
|---|---|---|
| `binary_search` | `return mid` (stop immediately) | **Any** matching index |
| `first_occurrence` | `ans = mid`, then `hi = mid - 1` (hunt left) | **First** (leftmost) index |
| `last_occurrence` | `ans = mid`, then `lo = mid + 1` (hunt right) | **Last** (rightmost) index |

All three: **Time O(log n) | Space O(1)**

---

## 8. Count Occurrences

Since the array is sorted, all copies of `target` are **contiguous**. The count formula is:

$$\text{count} = \text{last\_index} - \text{first\_index} + 1$$

Two binary searches: `first_occurrence` + `last_occurrence` = O(log n) + O(log n) = **O(log n)** total (constants drop in Big-O).

**Example:** `arr = [10, 20, 30, 30, 30, 30, 30, 40, 50]`, `target = 30`
- `first = 2`, `last = 6`
- `count = 6 - 2 + 1 = 5` ✓

---

## 9. Python's `bisect` Module

Python provides optimised, C-level binary search via the `bisect` module. Use it in interviews when you don't need to write it from scratch.

### `bisect_left(arr, target)` — equivalent to `first_occurrence`

Returns the **first index where value ≥ target** (left boundary of target range):

```python
import bisect
arr = [10, 20, 30, 30, 30, 30, 30, 40, 50]

bisect.bisect_left(arr, 30)   # → 2  (first occurrence of 30)
bisect.bisect_left(arr, 250)  # → 7  (would insert between 40 and 50 if not present)
bisect.bisect_left([100, 200, 300], 50)   # → 0  (smaller than all → index 0)
bisect.bisect_left([100, 200, 300], 500)  # → 3  (larger than all → len(arr))
```

### `bisect_right(arr, target)` — index **after** last occurrence

Returns the **first index where value > target** (right boundary of target range):

```python
bisect.bisect_right(arr, 30)  # → 7  (one past the last 30)
```

### Count via bisect (one-liner)

```python
count = bisect.bisect_right(arr, target) - bisect.bisect_left(arr, target)
# For target=30: 7 - 2 = 5 ✓
```

### Import Variants

```python
import bisect                  # → bisect.bisect_left(arr, t)  [recommended]
import bisect as bi            # → bi.bisect_left(arr, t)
from bisect import bisect_left # → bisect_left(arr, t)  [fine for one function]
from bisect import *           # → bisect_left(arr, t)  [AVOID — pollutes namespace]
```

> [!WARNING]
> `from bisect import *` imports everything into your global namespace. If you define a function with the same name, it silently overwrites the built-in. Prefer `import bisect` or explicit named imports.

---

## 10. Generate Sub-Arrays

A **sub-array** is a **contiguous** portion of an array (original order, no skipping).

For `arr = [1, 2, 3]`: sub-arrays are `[1]`, `[1,2]`, `[1,2,3]`, `[2]`, `[2,3]`, `[3]` — **n*(n+1)/2** total.

Pattern: `i` anchors the start, `j` sweeps right to grow the window:

```
i=0: [1] → [1,2] → [1,2,3]
i=1:        [2]  →  [2,3]
i=2:                 [3]
```

**Time:** O(n²) for *enumeration* (two loops). O(n³) if you *print/copy* each subarray with `arr[i:j+1]` (the slice itself is O(length)).

---

## 11. Maximum Subarray Sum — 4-Step Evolution

| Step | Algorithm | Time | Space | Key Idea |
|---|---|---|---|---|
| 1 | Brute force (3 loops) | O(n³) | O(1) | Recompute sum from scratch for every (i,j) |
| 2 | Optimised brute (2 loops) | O(n²) | O(1) | Extend running sum instead of recomputing |
| 3 | Prefix sum + all pairs | O(n²) | O(n) | `sum(i..j) = prefix[j] - prefix[i-1]` |
| 4 | Prefix sum + running min | **O(n)** | O(n) | For each j, subtract the min prefix seen so far |

Kadane's Algorithm (O(n) / O(1)) is the ultimate answer — covered in Module 09.

---

## 12. Prefix Sum

Build `prefix[i] = arr[0] + arr[1] + ... + arr[i]` in one pass.

**Recurrence:**
```
prefix[0] = arr[0]
prefix[i] = prefix[i-1] + arr[i]   ← one addition, not a re-scan
```

**O(1) range query formula:**
$$\text{sum}(arr[i..j]) = \text{prefix}[j] - \text{prefix}[i-1]$$

*(When i=0: just `prefix[j]`)*

**Why it works:**
```
prefix[j]   = arr[0] + ... + arr[i-1] + arr[i] + ... + arr[j]
prefix[i-1] = arr[0] + ... + arr[i-1]
                                       ↑ cancels  ↑
Difference  =                           arr[i] + ... + arr[j]  ✓
```

**Trade-off:** O(n) build cost + O(n) space → O(1) per query thereafter. Worth it for many range sum queries.

---

## 13. Complexity Reference Guide

### Code Pattern → Complexity

| Code pattern | Complexity | Why |
|---|---|---|
| `while lo <= hi: mid = (lo+hi)//2` | O(log n) | Search space halves each step |
| `for i in range(n):` | O(n) | One pass |
| `for i... for j in range(i, n):` | O(n²) | All pairs — triangular sum |
| `for i... for j... for k in range(i, j+1):` | O(n³) | All pairs + sum each pair |
| `prefix[j] - prefix[i-1]` | O(1) | Precomputed — just subtraction |
| `track min/max "so far"` | O(n) | One pass, O(1) work per step |

### The "Double the Input" Test

If I double n, the runtime changes by:

| Complexity | Effect of doubling n |
|---|---|
| O(1) | No change |
| O(log n) | Adds ~1 step |
| O(n) | Doubles |
| O(n log n) | Slightly more than 2× |
| O(n²) | Quadruples (4×) |
| O(n³) | 8× |

### The Optimisation Mindset

1. *"Am I recomputing something I already know?"* → Use incremental computation (O(n³) → O(n²))
2. *"Can I precompute answers to subproblems?"* → Prefix sums, memoization
3. *"Do I need to check ALL possibilities?"* → Binary search, two pointers, sorting
4. *"Can I track just what I need?"* → Running min/max/sum instead of full arrays

---

## 14. When to Apply Binary Search

> [!TIP]
> | Symptom | Apply Binary Search |
> |---|---|
> | Sorted array + find element | Standard binary search |
> | Find first/last occurrence of duplicate | Modified binary search (hunt left/right on match) |
> | Count occurrences in sorted array | `last - first + 1` |
> | O(log n) required | Almost certainly binary search or a tree |
> | Answer lies in a monotonic range | Binary search on answer space |
