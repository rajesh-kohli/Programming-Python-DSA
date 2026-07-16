# 11 - Kadane's Algorithm and Subarray Patterns

## Why This Module Matters

Kadane's Algorithm is the **canonical O(n) answer** to the Maximum Subarray Sum problem — arguably the most commonly asked array question in technical interviews. It is also the foundation for the harder Circular Subarray variant. This module covers:

1. Kadane's — standard (sum only)
2. Kadane's — with actual subarray tracking (3-pointer variant)
3. Maximum Circular Subarray Sum (the `total - min` trick)
4. Maximum Product of a Triplet (sorting + two candidates)

---

## 1. The "Extend or Reset" Mental Model

At every index `i`, Kadane's asks one question in plain English:

> **"Is it more profitable to attach `arr[i]` to the subarray I've been building, or to throw everything away and start a brand-new subarray at `arr[i]`?"**

```
x[i] = max(  x[i-1] + arr[i],    arr[i]  )
              ↑ EXTEND             ↑ RESET
```

### Why does a negative running sum hurt?

Suppose the running sum `x` has gone negative (e.g., `x = -5`). If the next element is `arr[i] = 4`:

- **EXTEND:** `-5 + 4 = -1`
- **RESET:** `4`

The reset wins. Carrying a negative prefix can **only drag down** every future element. Any future sum that includes the negative prefix would have been better off starting fresh. So Kadane's simply throws it away.

**The rule, summarised:**
- If `x` (running sum) is **positive** → extending helps (or is neutral): always extend.
- If `x` is **negative** → it's dead weight: reset to `arr[i]`.

This is equivalent to `x = max(x + arr[i], arr[i])`, which is O(1) per step.

---

## 2. Standard Kadane's — Full Step Trace

For `arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]` — answer is `6` (subarray `[4,-1,2,1]`):

| `i` | `arr[i]` | `x + arr[i]` | `arr[i]` alone | `x` (chosen) | Decision | `max_so_far` |
|---|---|---|---|---|---|---|
| 0 | -2 | — | — | -2 | Base case | -2 |
| 1 | 1 | -2+1 = **-1** | **1** | 1 | RESET (`-1 < 1`) | 1 |
| 2 | -3 | 1-3 = **-2** | -3 | -2 | EXTEND (`-2 > -3`) | 1 |
| 3 | 4 | -2+4 = **2** | **4** | 4 | RESET (`2 < 4`) | 4 |
| 4 | -1 | 4-1 = **3** | -1 | 3 | EXTEND (`3 > -1`) | 4 |
| 5 | 2 | 3+2 = **5** | 2 | 5 | EXTEND | 5 |
| 6 | 1 | 5+1 = **6** | 1 | 6 | EXTEND | **6** |
| 7 | -5 | 6-5 = **1** | -5 | 1 | EXTEND (`1 > -5`) | 6 |
| 8 | 4 | 1+4 = **5** | 4 | 5 | EXTEND | 6 |

**Answer: 6** → `[4, -1, 2, 1]` (indices 3–6).

Visual bar:
```
arr:  [-2,  1, -3,  4, -1,  2,  1, -5,  4]
  x:  [-2,  1, -2,  4,  3,  5,  6,  1,  5]
       ↑    ↑RESET  ↑RESET ←— EXTEND ——→
 max:  [-2,  1,  1,  4,  4,  5,  6,  6,  6]
```

---

## 3. The Two-Version Evolution

| Version | Space | When to use |
|---|---|---|
| Array-based: `x[i] = max(x[i-1]+arr[i], arr[i])` | O(n) | Pedagogically clearer — each slot is explicit |
| Scalar-based: `x = max(x+arr[i], arr[i])` | **O(1)** | **Write this in interviews** — only previous value needed |

The scalar version works because `x[i]` only depends on `x[i-1]`. The array can be replaced with a single variable without losing any information.

---

## 4. Kadane's with Subarray Tracking — 3-Pointer State Machine

To return the actual subarray, track three pointers:

```
temp_start  — where the current candidate subarray BEGINS
             (updated whenever we RESET to a new start)

start       — where the overall BEST subarray begins
end         — where the overall BEST subarray ends
             (both updated whenever we find a new max_so_far)
```

**State machine rules:**

```
At each i:
  if arr[i] > x + arr[i]:      ← RESET condition
      x = arr[i]
      temp_start = i            ← the new candidate starts HERE

  else:                         ← EXTEND condition
      x += arr[i]

  if x > max_so_far:            ← new global best
      max_so_far = x
      start = temp_start        ← lock in the candidate start
      end = i                   ← and current index as end
```

> [!WARNING]
> **All-negative edge case:** If all numbers are negative, `temp_start` resets at every step. The algorithm correctly returns the single largest element (the "least negative") with start=end=index_of_that_element. Make sure your assertions test this!

---

## 5. Maximum Circular Subarray Sum — The `total − min` Trick

### The Problem

A **circular** array lets subarrays wrap: for `[5, -3, 5]`, the subarray `[5, 5]` (indices 2 then 0) is valid and sums to 10.

### Key Insight: Only Two Cases Exist

```
Case 1 — subarray does NOT wrap:
   [ ← selected → ]
   → Standard Kadane's gives you this.

Case 2 — subarray DOES wrap:
   [ selected | not selected | selected ]
     left part  middle part    right part
```

For Case 2, note that the **not-selected middle** is a contiguous subarray. To **maximise** the selected part, you must **minimise** the middle part:

$$\text{max\_circular} = \text{total\_sum} - \text{min\_subarray\_sum}$$

To find `min_subarray_sum`, negate every element and run Kadane's max on the negated array (the max of the negated is the min of the original).

**Full formula:**
$$\text{answer} = \max(\text{max\_normal},\; \text{total} - \text{min\_normal})$$

### Step-by-Step Proof — `arr = [5, -3, 5]`

```
total = 5 + (-3) + 5 = 7

Case 1 (no wrap) — standard Kadane's:
  i=0: x=5,   max=5
  i=1: x=max(5-3,-3)=2,  max=5
  i=2: x=max(2+5,5)=7,   max=7
  max_normal = 7

Case 2 (wrap) — negate and run Kadane's:
  negated = [-5, 3, -5]
  i=0: x=-5,           max=-5
  i=1: x=max(-5+3,3)=3,  max=3
  i=2: x=max(3-5,-5)=-2, max=3
  max_of_negated = 3  → min_subarray = -3  (un-negate)
  max_wrap = total - min_subarray = 7 - (-3) = 10

Answer = max(7, 10) = 10 ✓  (subarray [5, 5] wrapping around)
```

### Critical Edge Case: All Numbers Negative

```
arr = [-3, -1, -2],  total = -6

Case 1: max_normal = -1  (the least-negative element)

Case 2: min_subarray = total = -6  (the whole array is the minimum)
        max_wrap = -6 - (-6) = 0

But 0 is WRONG — we must select at least one element!
```

**Guard:** If `max_normal < 0`, skip Case 2 entirely and return `max_normal`. The all-negative case degenerates because the "minimum subarray" IS the entire array, leaving nothing selected on the outside.

---

## 6. Maximum Product of a Triplet

**Problem:** Find three elements whose product is maximum (can include negatives).

**Key insight:** After sorting, only **two candidates** exist:
1. `arr[-1] × arr[-2] × arr[-3]` — the three largest (all positive scenario)
2. `arr[0] × arr[1] × arr[-1]` — two most-negative × the largest (two negatives make a positive)

No other combination can beat these two. Proof: the most negative pair is always `arr[0], arr[1]` because `arr[1] ≤ arr[2]` in a sorted array, so `arr[1]` has a larger absolute value.

**Time: O(n log n) | Space: O(1)**

---

## 7. Complexity Summary

| Algorithm | Time | Space | Key Idea |
|---|---|---|---|
| Brute Force (3 loops) | O(n³) | O(1) | Recompute every subarray sum |
| Optimised Brute (2 loops) | O(n²) | O(1) | Extend sum incrementally |
| Prefix Sum + running min | O(n) | O(n) | `sum(i..j) = prefix[j] - prefix[i-1]` |
| **Kadane's (scalar)** | **O(n)** | **O(1)** | **Extend or reset — no arrays needed** |
| Kadane's (with subarray) | O(n) | O(1) | Same + 3-pointer state tracking |
| Max Circular | O(n) | O(1) | `total - min_subarray` (two Kadane passes) |
| Max Product Triplet | O(n log n) | O(1) | Sort + 2 candidates |

---

## 8. When to Apply Each Pattern

> [!TIP]
> | Symptom | Pattern |
> |---|---|
> | Max/Min contiguous subarray sum | Kadane's `x = max(x+a, a)` |
> | Need the actual subarray, not just the sum | 3-pointer Kadane's |
> | Array is circular (can wrap) | `max(kadane_max, total - kadane_min)` |
> | Max product of 3 elements (negatives present) | Sort → check 2 candidates |
> | Many range sum queries on same array | Prefix sum array |

> [!WARNING]
> **All-negative guard** — always check `if max_normal < 0: return max_normal` before computing the circular case. Forgetting this returns `0` which violates the constraint that ≥1 element must be selected.
