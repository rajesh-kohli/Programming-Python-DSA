# 08 - Core Array & Hashing Problems

## Why This Module Matters

Every algorithm in this module is a **direct interview question** at top tech companies. Together, they cover the four core problem-solving patterns that underpin 80% of all array problems:

| Pattern | Core Idea | Complexity |
|---|---|---|
| **Two Pointers** | `i` at start, `j` at end, converge | O(n) Time, O(1) Space |
| **Hash Map / Set** | Swap space for O(1) lookups | O(n) Time, O(n) Space |
| **Prefix Sum** | Pre-compute cumulative sums for O(1) range queries | O(n) Pre, O(1) Query |
| **In-Place Marking** | Use the array itself as auxiliary storage | O(n) Time, O(1) Space |

---

## 1. Array Reversal — Two-Pointer Foundation

```
arr = [10, 20, 30, 40, 50]
       i               j      → swap 10 ↔ 50

arr = [50, 20, 30, 40, 10]
            i       j         → swap 20 ↔ 40

arr = [50, 40, 30, 20, 10]
                ij            → i ≥ j, STOP (middle stays)
```

**Complexity:** Time O(n/2) ≈ O(n) | Space O(1)

> [!TIP]
> `reverse(arr, lo, hi)` is a reusable sub-routine. Rotation, palindrome checks, and the 3-reversal algorithm all call it as a building block.

---

## 2. Array Rotation — The 3-Reversal Algorithm ⭐

### Why O(n·k) brute force fails

Rotating one position at a time costs O(n) per rotation × k rotations = **O(n·k)**. For k ≈ n this is **O(n²)**.

### The Reversal Trick (O(n), O(1) Space)

Given `arr = [1, 2, 3, 4, 5]`, rotate right by k = 2:

```
Think of the array as two parts:
  A = [1, 2, 3]   (first n-k elements)
  B = [4, 5]      (last  k   elements)
  Goal: B + A = [4, 5, 1, 2, 3]

Step 1: reverse(0, n-1)   →  [5, 4, 3, 2, 1]   (= B_rev + A_rev)
Step 2: reverse(0, k-1)   →  [4, 5, 3, 2, 1]   (un-reverse B)
Step 3: reverse(k, n-1)   →  [4, 5, 1, 2, 3]   (un-reverse A) ✓
```

**Mathematical proof:** `rev(rev(A) + rev(B)) = B + A`. By splitting the double-reversal at position k, we "cut and paste" the two halves into the correct order.

> [!IMPORTANT]
> Always apply `k = k % n` first. Rotating by n gives the same array — only the remainder matters.

---

## 3. Linear Search — 3 Variants

| Variant | Approach | Edge case |
|---|---|---|
| First occurrence | Left → right, early return | Not found → -1 |
| Last occurrence | Right → left (range n-1, -1, -1), early return | Not found → -1 |
| All occurrences | Collect all indices, use flag | Not found → [-1] |

---

## 4. Three Largest Elements — Cascade Pattern

Track three variables: `first`, `second`, `third` (all initialised to `float('-inf')`).

```
arr = [12, 35, 1, 10, 34, 1]

 num  first  second  third
  12     12    -inf   -inf    (12 beats all)
  35     35      12   -inf    (35 beats all → cascade 12 down)
   1     35      12   -inf    (1 beats none)
  10     35      12     10    (10 beats third only)
  34     35      34     12    (34 beats second → cascade)
   1     35      34     12    (1 beats none)
```

> [!CAUTION]
> The cascade **order matters**: set `third = second` BEFORE `second = first`. Reversing this overwrites `second` before you save it.

---

## 5. Two Sum — Hash Map Pattern ⭐

```
arr = [2, 7, 11, 15], target = 9

i=0: num=2,  complement=7,   seen={}       7 not in seen → seen={2:0}
i=1: num=7,  complement=2,   seen={2:0}    2 IS in seen! → return (0, 1) ✓
```

> [!TIP]
> **Mental model:** `seen` is a "guest list". Each new element asks "Is my partner (target - me) already here?" before signing in. O(n²) nested loops become O(n) with this one trade: O(n) extra space.

---

## 6. Find Duplicate — Index Mapping (O(1) Space) ⭐

Array of `n+1` integers where each value ∈ [1, n]. One value appears twice.

**Key insight:** In a duplicate-free array of [1..n], value `x` should live at index `x`. We use `nums[0]` as a "buffer slot" and keep swapping values to their correct indices.

```
nums = [2, 3, 1, 3]
  x = nums[0] = 2  →  nums[2] ≠ 2 (it's 1)  →  swap(nums[0], nums[2])
  nums = [1, 3, 2, 3]

  x = nums[0] = 1  →  nums[1] ≠ 1 (it's 3)  →  swap(nums[0], nums[1])
  nums = [3, 1, 2, 3]

  x = nums[0] = 3  →  nums[3] ≠ 3 (it's 3... WAIT, nums[3] == 3)
  → nums[3] == x == 3  →  DUPLICATE FOUND: 3 ✓
```

**Why it terminates:** each swap moves at least one value to its correct index. Except the duplicate — when it tries to go to its "home", that slot is already occupied by an identical value, triggering the return condition.

---

## 7. Product of Array Except Self — Prefix × Suffix ⭐

### Why division fails

Division breaks on `0` in the array (division by zero). Two zeros → all results are 0. Interviewers explicitly ban division.

### The Prefix-Suffix Mental Model

```
nums   = [ 1,  2,  3,  4 ]

         Pass 1 (left→right):  running prefix product BEFORE index i
prefix = [ 1,  1,  2,  6 ]    ans[0]=1, ans[1]=1×1, ans[2]=1×2, ans[3]=1×2×3

         Pass 2 (right→left): multiply each ans[i] by running suffix product AFTER index i
suffix running: starts at 1
  i=3: ans[3] = 6 × 1 = 6,    suffix = 1×4 = 4
  i=2: ans[2] = 2 × 4 = 8,    suffix = 4×3 = 12
  i=1: ans[1] = 1 × 12 = 12,  suffix = 12×2 = 24
  i=0: ans[0] = 1 × 24 = 24,  suffix = 24×1 = 24

Result = [ 24, 12,  8,  6 ]
         2×3×4, 1×3×4, 1×2×4, 1×2×3  ✓
```

**ans[i] = (product of everything LEFT of i) × (product of everything RIGHT of i)**
The two passes compute left and right products without using division or extra arrays.

| Approach | Time | Space | Notes |
|---|---|---|---|
| Division | O(n) | O(1) | Fails on zeros, often banned |
| Explicit prefix[] + suffix[] arrays | O(n) | O(n) | Clear but uses O(n) extra |
| Running prefix/suffix (optimal) | O(n) | **O(1)** | Two passes, output array only |

---

## 8. Prefix Sum — Range Query Pattern

```
arr  = [10, 20, 30, 40, 50]
pSum = [10, 30, 60, 100, 150]

pSum[i] = pSum[i-1] + arr[i]

Range sum arr[l..r] = pSum[r] - pSum[l-1]    (O(1) per query after O(n) build)
Range sum arr[1..3] = pSum[3] - pSum[0] = 100 - 10 = 90
                    = 20 + 30 + 40 = 90 ✓
```

> [!NOTE]
> Prefix sum is the bridge between **brute O(n²) range queries** and **O(1) range queries**. It also underpins the naive O(n²) max subarray (using pSum to compute any subarray sum), which Kadane's Algorithm then reduces to O(n).

---

## 9. Longest Consecutive Sequence — Set-Start Pattern

**Brute O(n²):** for each element, scan the array for the next consecutive value.
**Optimal O(n):** put all elements in a `set`. Only start counting from values where `num - 1` is NOT in the set (i.e., sequence starts). Then walk forward through the set.

```
nums = [100, 4, 200, 1, 3, 2]
set  = {1, 2, 3, 4, 100, 200}

Start at 1 (0 not in set) → walk: 1→2→3→4 (5 not in set) → length=4
Start at 100 → walk: 100 (101 not in set) → length=1
Start at 200 → walk: 200 (201 not in set) → length=1
Answer: 4 ✓
```

---

## 10. Interview Pattern Decision Guide

> [!TIP]
> | Symptom | Reach for... |
> |---|---|
> | "Find pair / check existence" | Hash Set or Dict |
> | "Count frequencies" | `Counter` or `defaultdict(int)` |
> | "O(1) space constraint" | Two Pointers or In-Place |
> | "Sorted array + pairs" | Two Pointers (converge) |
> | "Range sum queries" | Prefix Sum |
> | "Move/partition elements" | Write-pointer technique |
> | "Consecutive sequences" | Hash Set + start-detection |
> | "Rotate array" | 3-Reversal Algorithm |

---

## 11. Master Complexity Table

| Problem | Brute | Optimal | Optimal Space |
|---|---|---|---|
| Reverse Array | O(n) new array | O(n) two-pointer | **O(1)** |
| Rotate by K | O(n·k) | O(n) 3-reversal | **O(1)** |
| Linear Search | — | O(n) scan | O(1) |
| Three Largest | O(n log n) sort | O(n) cascade | **O(1)** |
| Two Sum | O(n²) nested | O(n) hash map | O(n) |
| Find Duplicate | O(n) hash set | O(n) index-map | **O(1)** (modifies arr) |
| Contains Duplicate | O(n²) | O(n) hash set | O(n) |
| Longest Consecutive | O(n²) | O(n) set+start | O(n) |
| Product Except Self | O(n²) naive | O(n) prefix×suffix | **O(1)** extra |
| Prefix Sum | O(n) per query | O(n) build, O(1) query | O(n) |
| Move Zeros | O(n²) | O(n) write-pointer | **O(1)** |
| Find Missing | O(n log n) sort | O(n) Gauss formula | **O(1)** |
| Max Difference | O(n²) | O(n) min_so_far | **O(1)** |
| Target Pair (sorted) | O(n²) | O(n) two-pointer | **O(1)** |
