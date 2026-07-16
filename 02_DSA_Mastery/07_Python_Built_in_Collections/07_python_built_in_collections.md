# 07 - Python Built-in Collections

## Why This Module Determines Your Interview Score

Choosing the wrong data structure silently changes your algorithm's complexity:

| Operation | `list` (scan) | `dict`/`set` (hash) |
|---|---|---|
| `x in collection` | O(n) | O(1) avg |
| Insert / Delete | O(n) shift | O(1) avg |
| Lookup by key | O(n) | O(1) avg |

A single swap — `list` → `set` for membership checks — is the difference between an O(n²) TLE and an O(n) accepted solution.

---

## 1. Lists — Dynamic Arrays

### Under the Hood

A Python list is a **contiguous block of memory containing references (pointers) to objects**. It is *not* a linked list.

When the internal array fills up, Python allocates a **new, larger block (~1.125× the old size)** and copies all existing references. This copy is O(n) — but it happens so rarely that averaged across all `append` calls, the cost per append is **O(1) amortised**.

```
Resize events for a list growing to 16 elements:
  Size →  0  1  2  3  4  5  9  10  14  17  ...
  Copy → ─── 1  2  3  4  5  8   9  13  16  ...
                           ↑ capacity doubles/1.125× at each resize
```

### Complete Complexity Table

| Method / Operation | Time | Space | Notes |
|---|---|---|---|
| `lst[i]` | O(1) | O(1) | Direct pointer offset |
| `lst[i] = x` | O(1) | O(1) | Direct assignment |
| `lst.append(x)` | **O(1) amortised** | O(1) | Occasional O(n) resize |
| `lst.pop()` | O(1) | O(1) | Remove from end |
| `lst.pop(i)` | O(n) | O(1) | Shift left after removal |
| `lst.insert(i, x)` | O(n) | O(1) | Shift right from i |
| `lst.remove(x)` | O(n) | O(1) | Scan + shift |
| `lst.extend(iter)` | O(k) | O(k) | k = len of iterable |
| `lst.sort()` | O(n log n) | O(n) | Timsort in-place |
| `sorted(lst)` | O(n log n) | O(n) | Returns new list |
| `lst.reverse()` | O(n) | O(1) | In-place swap |
| `lst.copy()` / `lst[:]` | O(n) | O(n) | Shallow copy |
| `lst.clear()` | O(n) | O(1) | Decrements all refs |
| `x in lst` | O(n) | O(1) | Linear scan |
| `lst.index(x)` | O(n) | O(1) | First occurrence |
| `lst.count(x)` | O(n) | O(1) | Full scan |
| `len(lst)` | O(1) | O(1) | Cached |
| `lst[a:b]` | O(b−a) | O(b−a) | Creates new list |
| `lst1 + lst2` | O(n+m) | O(n+m) | Creates new list |
| `del lst[i]` | O(n) | O(1) | Same as `pop(i)` |

> [!IMPORTANT]
> **Stack vs Queue choice:**
> - Use `list` as a **stack** (LIFO) — `append` and `pop()` are both O(1)
> - **Never** use `list` as a queue — `pop(0)` and `insert(0, x)` are **O(n)**
> - Use `collections.deque` for O(1) queue operations on both ends

---

## 2. Slicing — `lst[start:stop:step]`

```
arr = [10, 20, 30, 40, 50, 60, 70, 80]
idx:   0   1   2   3   4   5   6   7
      -8  -7  -6  -5  -4  -3  -2  -1
```

| Slice | Result | Rule |
|---|---|---|
| `arr[1:4]` | `[20, 30, 40]` | stop is **exclusive** |
| `arr[:3]` | `[10, 20, 30]` | start defaults to 0 |
| `arr[5:]` | `[60, 70, 80]` | stop defaults to end |
| `arr[:]` | full shallow copy | both omitted |
| `arr[::2]` | `[10, 30, 50, 70]` | every 2nd element |
| `arr[::-1]` | reversed | negative step walks right→left |
| `arr[-3:]` | `[60, 70, 80]` | last 3 elements |

**Rule:** sign of `step` dictates walk direction. Out-of-range indices are **silently clamped** (no IndexError in slices).

### Shallow Copy vs Deep Copy 🔑

```
original = [[1, 2], [3, 4], [5, 6]]
sliced   = original[:]        # shallow copy

original ──► [ ref₀, ref₁, ref₂ ]
                │      │      │
sliced   ──► [ ref₀, ref₁, ref₂ ]   ← same inner list objects!
                ▼      ▼      ▼
             [1,2]  [3,4]  [5,6]   ← SHARED

sliced[0][0] = 999   # mutates the SHARED inner list
original[0]          # → [999, 2]  ← original is affected!
```

**Fix:** `import copy; deep = copy.deepcopy(original)` — clones every nested object.

---

## 3. List Initialization Traps

> [!CAUTION]
> **`[[0]] * n` creates n references to the SAME inner list:**
> ```python
> wrong = [[0]] * 3
> wrong[0].append(1)
> print(wrong)   # [[0, 1], [0, 1], [0, 1]]  ← ALL three changed!
>
> right = [[0] for _ in range(3)]
> right[0].append(1)
> print(right)   # [[0, 1], [0], [0]]  ← only first changed ✓
> ```
> `[0] * n` is **safe** for immutable types (int, str, tuple) because reassignment creates a new object.

---

## 4. List Comprehensions

| Pattern | Syntax |
|---|---|
| Basic | `[x**2 for x in range(n)]` |
| Filtered | `[x for x in lst if x % 2 == 0]` |
| If-else | `["even" if x%2==0 else "odd" for x in lst]` |
| Nested / flatten | `[val for row in matrix for val in row]` |
| Dict comprehension | `{name: len(name) for name in names}` |
| Set comprehension | `{x**2 for x in lst}` |
| Generator | `(x**2 for x in lst)` — lazy, O(1) memory |

> [!TIP]
> List comprehensions are ~30% faster than equivalent `for` + `append` loops because the `append` call is optimised at the C level in CPython.

---

## 5. Tuples — Immutable Sequences

| Feature | `list` | `tuple` |
|---|---|---|
| Mutable? | Yes | **No** |
| Hashable? | No | **Yes** (if contents are) |
| Dict key? | ❌ | ✅ |
| Has `.append`? | Yes | No |
| Memory | More (resize buffer) | Less (fixed) |
| Use case | Changing collections | Records, dict keys, function returns |

**Single-element gotcha:** the **comma** makes a tuple, not the parentheses:
```python
(42,)   # ← tuple   type: <class 'tuple'>
(42)    # ← int     type: <class 'int'>
```

**Extended unpacking:**
```python
first, *rest = [1, 2, 3, 4, 5]    # first=1, rest=[2,3,4,5]
*rest, last  = [1, 2, 3, 4, 5]    # rest=[1,2,3,4], last=5
```

---

## 6. Dictionaries — How O(1) Works

### Under the Hood: Hash Tables

```
key = "apple"

Step 1: hash("apple")  →  some large integer h
Step 2: bucket_index = h % table_size    (e.g., h % 1024 = 42)
Step 3: go directly to slot 42 in the array → O(1)!
```

Python's `dict` is a **hash table** — an array of buckets where each bucket's position is derived from the key's hash value. Because array indexing is O(1), lookup is O(1).

**Why worst-case is O(n):** Hash **collisions** occur when two different keys land in the same bucket. CPython uses **open addressing** (probing the next slot). In pathological cases (adversarial keys or very full table), many keys cluster in the same buckets and lookup degrades to O(n).

### All Dictionary Operations

| Operation | Time | Space | Notes |
|---|---|---|---|
| `d[key]` | O(1) avg | O(1) | KeyError if missing |
| `d[key] = val` | O(1) avg | O(1) | Insert or update |
| `d.get(key, default)` | O(1) avg | O(1) | **Safe lookup — no KeyError** |
| `key in d` | O(1) avg | O(1) | Membership via hash |
| `del d[key]` | O(1) avg | O(1) | KeyError if missing |
| `d.pop(key)` | O(1) avg | O(1) | Returns value |
| `d.keys()` | O(1) | O(1) | Returns view object |
| `d.values()` | O(1) | O(1) | Returns view object |
| `d.items()` | O(1) | O(1) | Returns (k, v) view |
| `d.update(other)` | O(len(other)) | O(k) | Merge dicts |
| `len(d)` | O(1) | O(1) | Cached |
| Iterate `for k in d` | O(n) | O(1) | Visits all keys |

> [!NOTE]
> **Python 3.7+ guarantees insertion order.** Dict iteration always yields keys in the order they were first inserted.

### `defaultdict` — Never Write `if key in d` Again

```python
from collections import defaultdict

freq = defaultdict(int)   # missing keys auto-initialise to int() = 0
for ch in "hello":
    freq[ch] += 1         # no KeyError, no .get() needed
```

---

## 7. Sets — Hash Sets

Sets are **dictionaries that store only keys, no values**. Same O(1) average hash mechanism.

| Operation | Time | Notes |
|---|---|---|
| `s.add(x)` | O(1) avg | Duplicates silently ignored |
| `s.remove(x)` | O(1) avg | **KeyError** if x not in set |
| `s.discard(x)` | O(1) avg | **Safe** — no error if missing |
| `s.update(iter)` | O(k) | Add all elements from iterable |
| `x in s` | O(1) avg | vs O(n) for list! |
| `len(s)` | O(1) | Cached |
| `s1 \| s2` | O(n+m) | Union |
| `s1 & s2` | O(min(n,m)) | Intersection |
| `s1 - s2` | O(n) | Difference |
| `s1 ^ s2` | O(n+m) | Symmetric difference |

> [!CAUTION]
> `{}` creates an **empty dict**, not an empty set. Use `set()` for empty sets.

---

## 8. Frequency Counting — The Four Tools

| Tool | Time | Space | Use when |
|---|---|---|---|
| `set(lst)` | O(n) | O(k) | Need unique values, not counts |
| Manual dict loop | O(n) | O(k) | Interviews / educational |
| `{x: lst.count(x) for x in set(lst)}` | **O(n·k)** | O(k) | **⚠️ Avoid for large data** |
| `collections.Counter(lst)` | O(n) | O(k) | **Always prefer this** |

```python
from collections import Counter
c = Counter(["a", "b", "a", "c", "b", "a"])
c.most_common(1)      # [("a", 3)]
c["z"]                # 0  ← no KeyError for missing keys!
```

---

## 9. L15 Maps Problems — Brute → Optimal Evolutions

### Problem 1: Contains Duplicate
- **Brute O(n²):** nested loop — compare every pair
- **Optimal O(n):** `defaultdict(int)` or `set` — return True the moment count > 1

### Problem 2: Longest Consecutive Sequence
- **Brute O(n²):** for each element, scan the array for next-1 values
- **Optimal O(n):** dict as start-map — mark only elements with no predecessor as sequence starts, then walk forward

### Problem 3: Longest Palindrome
- **Core insight:** every character that appears an **even** number of times contributes fully. At most **one** odd-count character can sit in the centre.
- **Optimal O(n):** `set` as a toggle — when a character is seen a second time, remove it and add 2 to the answer (paired). Any remaining characters in the set contribute 1 (centre).

---

## 10. Interview Cheat Sheet

> [!TIP]
> | Pattern | Code |
> |---|---|
> | Deduplicate list | `list(set(lst))` |
> | Deduplicate preserving order | `seen=set(); [x for x in lst if not (x in seen or seen.add(x))]` |
> | Frequency map | `Counter(lst)` or `{x: lst.count(x) for x in set(lst)}` (small only) |
> | Safe dict lookup | `d.get(key, 0)` |
> | Auto-default dict | `defaultdict(int)` |
> | O(1) membership | `x in my_set` not `x in my_list` |
> | Sort by value | `sorted(d.items(), key=lambda kv: kv[1])` |
> | Top-k frequent | `Counter(lst).most_common(k)` |
> | Tuple as dict key | `location[(lat, lon)] = city` |
> | Swap variables | `a, b = b, a` |
> | Max-sentinel | `float('-inf')` |
> | 2D grid init | `[[0]*cols for _ in range(rows)]` |
