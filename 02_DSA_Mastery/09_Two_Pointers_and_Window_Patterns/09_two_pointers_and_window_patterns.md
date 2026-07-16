# 09 - Two Pointers and Window Patterns

## Why This Module Matters

Two Pointers is the technique that converts **O(n²) nested loops → O(n) single pass**. Every problem here is a direct interview question at top companies. The key trade: instead of checking every pair, you exploit a property (sorted order, boundary logic, or a fixed constraint) to eliminate possibilities in bulk at each step.

---

## The Three Pointer Configurations

| Configuration | When to Use | How It Terminates |
|---|---|---|
| **Opposite-End Convergence** | Sorted array pair/range problems | `i >= j` |
| **Same-Direction Fast/Slow** | In-place compaction, duplicate removal | `fast >= n` |
| **Multi-Array Parallel** | Merge two sorted arrays | `i >= n and j >= m` |

---

## Why Two Pointers Gives O(n)

With a sorted array and `i=0, j=n-1`:
- Every loop iteration, **at least one pointer moves**.
- Each pointer can move at most `n` steps total.
- Together they take at most `2n` steps → **O(n)**.

Contrast with brute force: `n*(n-1)/2` pairs = **O(n²)**.

The key question to ask yourself: *"Can I avoid checking this pair by knowing it's impossible?"* If sorted order (or some boundary property) lets you say YES — two pointers applies.

---

## 1. Generate All Pairs — The O(n²) Baseline

Before optimizing, recognise the brute-force shape. Every two-pointer problem starts here:

```python
for i in range(n - 1):
    for j in range(i + 1, n):
        process(arr[i], arr[j])
```

This generates every pair exactly once: `n*(n-1)/2` pairs. **Time O(n²), Space O(1).**

---

## 2. Target Sum Pair — Opposite-End Convergence ⭐

**Sorted array required.** Count pairs where `arr[i] + arr[j] == target`.

```
arr = [1, 2, 3, 4, 5, 6],  target = 7

idx:   0  1  2  3  4  5
arr:  [1, 2, 3, 4, 5, 6]
       i              j     sum=1+6=7 == target → MATCH, i++, j--
          i        j        sum=2+5=7 == target → MATCH, i++, j--
             i  j           sum=3+4=7 == target → MATCH, i++, j--
                j  i        i ≥ j → STOP

Result: 3 pairs (1+6, 2+5, 3+4)
```

**Why it works:** When `sum < target`, only moving `i` right (to a larger value) can fix it — moving `j` left would make things worse. When `sum > target`, only moving `j` left helps. Each decision eliminates one element permanently. Total: O(n) steps.

> [!IMPORTANT]
> Requires a sorted array. If unsorted, `sort()` first (O(n log n)) then two-pointer (O(n)). Still beats brute force O(n²).

---

## 3. Container With Most Water — Opposite-End + Boundary Logic ⭐

`area = width × min(height[left], height[right])`

Start with the maximum possible width (`i=0, j=n-1`). At each step, move the **shorter wall** inward.

**Why move the shorter wall? (Plain English proof):**

> At any moment, `area = (j - i) × min(height[i], height[j])`.
> The height is **capped by the shorter wall** — water spills over the short side.
>
> If you move the **taller** wall inward: width decreases by 1, AND the height cap is **still limited by the same shorter wall**. Area can only get worse or equal. This move is provably useless.
>
> If you move the **shorter** wall inward: width decreases by 1, BUT the height cap **might increase** if the new wall is taller. This is the only move that could possibly improve the area.
>
> **Conclusion:** Always move the shorter pointer. If they're equal, move either (both are symmetric).

```
heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
 idx:      0  1  2  3  4  5  6  7  8

i=0,j=8: area=8×min(1,7)=8    → h[0]=1 < h[8]=7 → move i (shorter)
i=1,j=8: area=7×min(8,7)=49  → h[1]=8 > h[8]=7 → move j (shorter)
i=1,j=7: area=6×min(8,3)=18  → h[7]=3 < h[1]=8 → move j
i=1,j=6: area=5×min(8,8)=40  → equal → move j
...
Answer: 49 ✓
```

---

## 4. Rainwater Trapping — 4-Step Evolution ⭐⭐⭐

**This is the most complete evolution sequence in all array problems.**

**Problem:** `height = [0,1,0,2,1,0,1,3,2,1,2,1]` → answer = 6

```
                         ┌──┐
                         │  │        ┌──┐
          ┌──┐           │  │ ┌──┐   │  │
       ┌──┤  ├───────────┤  ├─┤  ├───┤  │
       │  │  │~~~~~~~~~~~│  │~│  │~~~│  │  ← trapped water (~~~)
┌──┐   │  │  │  ┌──┐    │  │ │  │   │  │
└──┘└──┘  └──┘  └──┘  └──┘ └──┘   └──┘└──┘
 0   1   2   3   4   5   6   7   8   9  10  11
```

### The Core Formula

Water trapped at building `i`:

$$w_i = \min(l_i, r_i) - h_i$$

where:
- $l_i$ = tallest building from the **left** up to and including `i`
- $r_i$ = tallest building from the **right** up to and including `i`

**Why `min`?** Water level is bounded by the *shorter* of the two containing walls (it would spill over the shorter one). **Why subtract `h_i`?** The building itself takes up space.

### Solution 1 — Brute Force: O(n²) Time, O(1) Space

For each building `i`, scan left to find `l_i`, scan right to find `r_i`. Two nested loops per building.

```python
for i in range(n):
    li = max(height[:i+1])    # O(n) scan left
    ri = max(height[i:])      # O(n) scan right
    water += min(li, ri) - height[i]
```

### Solution 2 — Precompute Both Arrays: O(n) Time, O(n) Space

Observation: we're re-scanning the same elements. Precompute `l[]` and `r[]` in two passes, then compute water in a third pass.

```
Recurrence:
  l[0]   = h[0]
  l[i]   = max(l[i-1], h[i])    ← one comparison, not a scan

  r[n-1] = h[n-1]
  r[i]   = max(r[i+1], h[i])    ← one comparison, not a scan
```

### Solution 3 — Drop `l[]`, Compute Left On-The-Fly: O(n) Time, O(n) Space

We scan left→right in pass 3 anyway. Merge pass 1 into pass 3 using a single `max_so_far` variable. Still need `r[]` precomputed.

### Solution 4 — Two Pointers: O(n) Time, O(1) Space ✓ (Best)

**Key insight:** We don't need the *exact* value of `r_i` to compute `w_i`. We just need to know which side is the *limiting wall*.

Use `i` from left, `j` from right. Track `l = running max from left`, `r = running max from right`.

**Decision rule:**
- If `l < r`: The left wall is the limiting factor. We **know** the true right max ≥ r ≥ l, so `min(l, true_r) = l`. Therefore `w_i = l - height[i]` is **exact**. Advance `i`.
- If `r ≤ l`: The right wall is the limiting factor by symmetric argument. `w_j = r - height[j]`. Advance `j`.

```
          Solution   Time  Space    Key Idea
          ─────────────────────────────────────────────────────────
          trap_1    O(n²)  O(1)    Brute: re-scan left+right for every i
          trap_2    O(n)   O(n)    Precompute both l[] and r[] arrays
          trap_3    O(n)   O(n)    Drop l[]; compute left max on-the-fly
          trap_4    O(n)   O(1)    Two pointers; drop r[] too ← BEST
```

> [!IMPORTANT]
> The progression `trap_1 → trap_2 → trap_3 → trap_4` is a classic interview pattern. Start obvious, then ask "what's redundant?" each step.

---

## 5. Merge Sorted Arrays — Parallel Multi-Array Pointers

Two pointers `i`, `j` each start at index 0 of their own sorted array. Always take the smaller current element. When one pointer exhausts its array, copy the remainder from the other.

```
a = [10, 30, 50, 60],  b = [20, 40, 70]

i=0,j=0: a[0]=10 ≤ b[0]=20 → c=[10],        i=1
i=1,j=0: a[1]=30 > b[0]=20 → c=[10,20],      j=1
i=1,j=1: a[1]=30 ≤ b[1]=40 → c=[10,20,30],   i=2
i=2,j=1: a[2]=50 > b[1]=40 → c=[10,20,30,40],j=2
i=2,j=2: a[2]=50 ≤ b[2]=70 → c=[...,50],     i=3
i=3,j=2: a[3]=60 ≤ b[2]=70 → c=[...,60],     i=4
i=4: exhausted → copy b[2]=70 → [10,20,30,40,50,60,70] ✓
```

**Time O(n+m): each element is visited exactly once. Space O(n+m).**

---

## 6. Remove Duplicates (Sorted) — Fast/Slow Pointers

`slow` marks the last confirmed-unique slot. `fast` scouts ahead.

```
arr = [1, 1, 2, 2, 2, 3]
       s
          f                arr[f]==arr[s] → skip (f++)
             f              arr[f]!=arr[s] → s++, arr[s]=arr[f]
          s     f
                   f        duplicate → skip
                      f     arr[f]=3 != arr[s]=2 → s++, arr[s]=3
                s       f

Result: arr[:s+1] = [1, 2, 3]   Time O(n), Space O(1)
```

---

## 7. DNF Sort (Dutch National Flag) — Three-Pointer Partition ⭐

Sort an array of `{0, 1, 2}` in O(n), O(1). Three pointers maintain four invariant regions:

```
[ 0..low-1 ] [ low..mid-1 ] [ mid..high ] [ high+1..n-1 ]
   zeros          ones         unknown         twos
```

**Cases:**
- `arr[mid] == 0`: swap with `arr[low]`, `low++`, `mid++`
- `arr[mid] == 1`: `mid++` (already in correct region)
- `arr[mid] == 2`: swap with `arr[high]`, `high--` (do NOT advance `mid` — new element is unknown)

**Time O(n) — single pass. Space O(1) — no extra arrays.**

---

## 8. Kadane's Algorithm — O(n) Max Subarray ⭐

At each index, ask: *"Is it better to extend the previous subarray, or start fresh at arr[i]?"*

$$x_i = \max(x_{i-1} + arr[i],\ arr[i])$$

If the running sum goes negative, it drags any future subarray down — reset.

```
arr:         -2   1  -3   4  -1   2   1  -5   4
current_sum: -2   1  -2   4   3   5   6   1   5
              |   |reset|reset|extend............|
max_sum:     -2   1   1   4   4   5   6   6   6
                                  ^best: [4,-1,2,1]=6^
```

| Version | Time | Space |
|---|---|---|
| With x[] array (educational) | O(n) | O(n) |
| With single variable (optimal) | O(n) | **O(1)** |

---

## 9. Master Complexity Table

| Problem | Brute | Optimal | Space |
|---|---|---|---|
| Generate All Pairs | O(n²) | — (enumerate) | O(1) |
| Target Sum Pair | O(n²) | O(n) two-pointer | **O(1)** |
| Container With Most Water | O(n²) | O(n) two-pointer | **O(1)** |
| Rainwater Trapping | O(n²) | O(n) two-pointer | **O(1)** |
| Merge Sorted Arrays | — | O(n+m) | O(n+m) |
| Remove Duplicates (sorted) | — | O(n) fast/slow | **O(1)** |
| DNF Sort | O(n log n) sort | O(n) 3-pointer | **O(1)** |
| Kadane's Max Subarray | O(n³) naive | O(n) | **O(1)** |

---

## 10. Decision Guide

> [!TIP]
> | Symptom | Reach for... |
> |---|---|
> | Sorted array + find pair/count pairs | Opposite-end two pointers |
> | "Maximum/minimum bounded by two sides" | Opposite-end + move shorter/limiting pointer |
> | In-place remove/compact/partition | Fast/Slow same-direction |
> | Merge two sorted collections | Parallel multi-array pointers |
> | Only 3 distinct values, in-place sort | Dutch National Flag (low/mid/high) |
> | Max subarray sum (contiguous) | Kadane's extend-or-reset |
