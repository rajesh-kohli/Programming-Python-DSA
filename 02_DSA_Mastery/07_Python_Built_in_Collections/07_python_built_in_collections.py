###############################################################################
#               07 - Python Built-in Collections                              #
###############################################################################
#
# SOURCES:
#   Coding_Python/1. Python - Intro/07_lists_tuples_slicing.py (1251 lines)
#   LPLV26MAY/L15 - Maps/ (001-007)
#
# KEY COMPLEXITY REFERENCE:
#   list[i]          O(1)          list.append(x)    O(1) amortised
#   list.insert(0,x) O(n)          x in list         O(n)
#   dict[key]        O(1) avg      key in dict        O(1) avg
#   x in set         O(1) avg      set.add(x)         O(1) avg

from collections import Counter, defaultdict, namedtuple
from typing import List, Dict, Set, Tuple, Optional
import copy


# =============================================================================
# SECTION 1: Lists — Dynamic Arrays Under the Hood
# =============================================================================
#
# A Python list is a DYNAMIC ARRAY:
#   - Contiguous block of memory holding REFERENCES (pointers) to objects
#   - NOT a linked list — indexing is O(1) because it's a direct pointer offset
#
# RESIZE MECHANISM (amortised O(1) append):
#   When the internal array fills up, Python allocates ~1.125× more space
#   and copies all existing references to the new block.
#   This O(n) copy happens rarely — averaged over n appends, cost = O(1)/append.
#
# MENTAL MODEL:
#   lst = [10, 20, 30]
#
#   Memory: [ *ref0, *ref1, *ref2, _free_, _free_, _free_ ]
#                 ↓       ↓       ↓
#               obj10   obj20   obj30
#
#   append(40): fill the _free_ slot — O(1)  (no copy needed)
#   insert(0,5): shift ref0, ref1, ref2 right — O(n)

def list_internals_demo():
    print("=" * 60)
    print("SECTION 1: Lists — Dynamic Array Internals")
    print("=" * 60)

    # --- Creating lists (4 ways) ---
    nums_lit     = [10, 20, 30, 40, 50]          # literal
    from_range   = list(range(1, 6))             # constructor
    from_str     = list("hello")                 # iterable → chars
    squares      = [x**2 for x in range(6)]      # comprehension
    empty        = []

    print(f"\n  Literal:         {nums_lit}")
    print(f"  From range:      {from_range}")
    print(f"  From string:     {from_str}")
    print(f"  Squares comp:    {squares}")
    print(f"  Empty list:      {empty}")

    # --- Indexing: O(1) direct pointer offset ---
    arr = [10, 20, 30, 40, 50]
    print(f"\n  arr      = {arr}")
    print(f"  arr[0]   = {arr[0]}   (first)")
    print(f"  arr[-1]  = {arr[-1]}  (last — most Pythonic)")
    print(f"  arr[-2]  = {arr[-2]}  (second to last)")
    # arr[5] → IndexError (beyond valid range)
    # arr[-6]→ IndexError

    print(f"  len(arr) = {len(arr)}  ← O(1), cached internally")

    # --- Complete method showcase with Time/Space ---
    print("\n  --- List methods with complexities ---")
    lst = [30, 10, 50, 20, 40]
    print(f"  Start:                  {lst}")

    lst.append(60)                              # O(1) amortised
    print(f"  append(60)  [O(1)]:     {lst}")

    lst.insert(0, 5)                            # O(n) — shifts everything right
    print(f"  insert(0,5) [O(n)]:     {lst}")

    last = lst.pop()                            # O(1) — from end
    print(f"  pop()       [O(1)]:     {lst}  removed {last}")

    idx2 = lst.pop(1)                           # O(n) — shift left
    print(f"  pop(1)      [O(n)]:     {lst}  removed {idx2}")

    lst.remove(5)                               # O(n) — scan + shift
    print(f"  remove(5)   [O(n)]:     {lst}")

    lst.extend([70, 80])                        # O(k), k=2
    print(f"  extend([70,80]) [O(k)]: {lst}")

    lst.sort()                                  # O(n log n) Timsort
    print(f"  sort()      [O(nlogn)]: {lst}")

    lst.reverse()                               # O(n)
    print(f"  reverse()   [O(n)]:     {lst}")

    backup = lst.copy()                         # O(n) shallow copy
    print(f"  copy()      [O(n)]:     {backup}")

    print(f"  count(80)   [O(n)]:     {lst.count(80)}")
    print(f"  index(70)   [O(n)]:     {lst.index(70)}")

    # --- Searching: O(n) for lists ---
    nums_search = [10, 20, 30, 40, 50, 30]
    print(f"\n  Searching in {nums_search}:")
    print(f"    30 in lst          : {30 in nums_search}      ← O(n) linear scan")
    print(f"    lst.index(30)      : {nums_search.index(30)}     ← first occurrence")
    print(f"    lst.index(30, 3)   : {nums_search.index(30, 3)}     ← search from idx 3")
    print(f"    lst.count(30)      : {nums_search.count(30)}     ← count occurrences O(n)")

    # for-else pattern: else runs only if loop completes without break
    target = 40
    for num in nums_search:
        if num == target:
            print(f"    for-else: Found {target}!")
            break
    else:
        print(f"    for-else: {target} not found")

    # find_max / find_min using float('-inf') / float('inf') sentinels
    def find_max(arr: List[int]) -> int:
        """Time: O(n) | Space: O(1)"""
        max_val = float('-inf')   # guaranteed smaller than any real value
        for x in arr:
            if x > max_val:
                max_val = x
        return max_val

    def find_min(arr: List[int]) -> int:
        """Time: O(n) | Space: O(1)"""
        min_val = float('inf')    # guaranteed larger than any real value
        for x in arr:
            if x < min_val:
                min_val = x
        return min_val

    sample = [30, 10, 50, 20, 40]
    print(f"\n  find_max({sample}) = {find_max(sample)}")
    print(f"  find_min({sample}) = {find_min(sample)}")


# =============================================================================
# SECTION 2: List Slicing — lst[start:stop:step]
# =============================================================================
#
# start: inclusive (default 0)
# stop:  EXCLUSIVE (default len)
# step:  stride, sign decides direction (+ = left→right, - = right→left)
#
# Out-of-range slice indices are SILENTLY CLAMPED — no IndexError.
# Slicing ALWAYS returns a NEW list (shallow copy).
#
# FULL INDEX MAP for [10, 20, 30, 40, 50, 60, 70, 80]:
#
#   Pos idx:  0    1    2    3    4    5    6    7
#   Neg idx: -8   -7   -6   -5   -4   -3   -2   -1
#           +----+----+----+----+----+----+----+----+
#           | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 |
#           +----+----+----+----+----+----+----+----+

def slicing_demo():
    print("\n" + "=" * 60)
    print("SECTION 2: Slicing")
    print("=" * 60)

    arr = [10, 20, 30, 40, 50, 60, 70, 80]
    print(f"\n  arr = {arr}")
    print(f"\n  arr[1:4]    = {arr[1:4]}      (idx 1,2,3 — stop exclusive)")
    print(f"  arr[:3]     = {arr[:3]}         (first 3)")
    print(f"  arr[5:]     = {arr[5:]}         (from 5 to end)")
    print(f"  arr[:]      = {arr[:]}  (full shallow copy)")
    print(f"  arr[1:6:2]  = {arr[1:6:2]}      (step=2: idx 1,3,5)")
    print(f"  arr[::2]    = {arr[::2]}     (even indices)")
    print(f"  arr[1::2]   = {arr[1::2]}     (odd indices)")
    print(f"  arr[::-1]   = {arr[::-1]}  (reversed)")
    print(f"  arr[5:1:-1] = {arr[5:1:-1]}      (right→left from 5 down to 2)")
    print(f"  arr[-3:]    = {arr[-3:]}         (last 3)")
    print(f"  arr[-5:-2]  = {arr[-5:-2]}      (negative range)")

    # --- Shallow copy vs Deep copy (CRITICAL gotcha) ---
    # Slicing copies the OUTER list but the INNER objects are SHARED.
    print("\n  --- Shallow copy vs Deep copy ---")

    original = [[1, 2], [3, 4], [5, 6]]
    sliced   = original[:]              # shallow copy — same inner list refs

    sliced[0][0] = 999                  # modifies the SHARED inner list
    print(f"  After sliced[0][0]=999:")
    print(f"    original[0] = {original[0]}  ← ALSO changed (shared reference!)")
    print(f"    sliced[0]   = {sliced[0]}")
    print(f"\n  Mental model:")
    print(f"    original → [ref0, ref1, ref2]")
    print(f"    sliced   → [ref0, ref1, ref2]  ← same inner objects!")
    print(f"    Fix: copy.deepcopy(original) clones every nested object.")

    deep = copy.deepcopy([[10, 20], [30, 40]])
    deep[0][0] = 999
    original2 = [[10, 20], [30, 40]]
    print(f"\n  deepcopy proof: original2={original2}, deep after mod={deep}")

    # --- Slice assignment — powerful resizing ---
    print("\n  --- Slice assignment (modifies in place, can resize) ---")
    colors = ["red", "green", "blue", "white"]
    print(f"  Before:              {colors}")

    colors[1:3] = ["pink", "black"]    # same-size replace
    print(f"  [1:3] = 2 items:     {colors}")

    colors[1:3] = ["orange"]          # shrink — 2 replaced by 1
    print(f"  [1:3] = 1 item:      {colors}")

    colors[0:2] = ["yellow", "a", "b"]  # grow — 2 replaced by 3
    print(f"  [0:2] = 3 items:     {colors}")

    nums2 = [1, 2, 5, 6]
    nums2[2:2] = [3, 4]               # empty slice = pure insert
    print(f"  Insert [3,4] at 2:   {nums2}")

    nums2[2:4] = []                   # delete elements at 2,3
    print(f"  Delete [2:4]:        {nums2}")


# =============================================================================
# SECTION 3: List Initialization Traps
# =============================================================================
#
# TRAP: [[0]] * n creates n REFERENCES to the SAME inner list.
# Mutating one mutates all — verified with id().
#
# SAFE:  [[0] for _ in range(n)] creates n INDEPENDENT inner lists.
# WHY SAFE for immutable: [0]*n — integers are immutable, so reassignment
# creates a new object. Shared reference only matters for mutation.

def initialization_demo():
    print("\n" + "=" * 60)
    print("SECTION 3: List Initialization Traps")
    print("=" * 60)

    # ❌ WRONG WAY: shared reference
    wrong = [[0]] * 3
    wrong[0].append(1)
    print(f"\n  [[0]] * 3 then wrong[0].append(1):")
    print(f"    wrong = {wrong}   ← ALL three changed!")
    print(f"    id(wrong[0]) == id(wrong[1]): {id(wrong[0]) == id(wrong[1])}")

    # ✅ RIGHT WAY: independent objects
    right = [[0] for _ in range(3)]
    right[0].append(1)
    print(f"\n  [[0] for _ in range(3)] then right[0].append(1):")
    print(f"    right = {right}  ← only first changed ✓")
    print(f"    id(right[0]) == id(right[1]): {id(right[0]) == id(right[1])}")

    # [0]*n is SAFE for immutables
    safe = [0] * 5
    safe[0] = 99
    print(f"\n  [0]*5, safe[0]=99: {safe}  ← OK (int is immutable)")

    # 2D matrix initialisation — always use comprehension
    rows, cols = 3, 4
    matrix = [[0] * cols for _ in range(rows)]
    print(f"\n  3×4 zero matrix: {matrix}")


# =============================================================================
# SECTION 4: 4 Loop Patterns — When to Use Each
# =============================================================================
#
# | Pattern                   | Use case                                    |
# |---------------------------|---------------------------------------------|
# | for item in lst           | Only need values, no index                  |
# | for i in range(len(lst))  | Need index to modify in place or compare adj|
# | for i, v in enumerate(lst)| Need BOTH index and value (PREFERRED)       |
# | while i < n               | Non-standard step, early termination        |

def loop_patterns_demo():
    print("\n" + "=" * 60)
    print("SECTION 4: 4 Loop Patterns")
    print("=" * 60)

    nums = [10, 20, 30, 40, 50]
    print(f"\n  nums = {nums}")

    # Method 1: for-each (simplest, no index)
    print("\n  Method 1 — for item in lst:")
    result = []
    for num in nums:
        result.append(num * 2)
    print(f"    doubled: {result}")

    # Method 2: index-based (when you need index for in-place modification)
    print("\n  Method 2 — for i in range(len(lst)):")
    copy_lst = nums[:]
    for i in range(len(copy_lst)):
        copy_lst[i] += 1
    print(f"    incremented: {copy_lst}")

    # Method 3: enumerate (PREFERRED for index + value)
    print("\n  Method 3 — for i, val in enumerate(lst):  [PREFERRED]")
    for i, val in enumerate(nums):
        print(f"    index={i}, value={val}")

    # enumerate with custom start
    print("  enumerate(start=1):")
    for rank, val in enumerate(nums, start=1):
        print(f"    rank={rank}, value={val}")

    # Method 4: while loop (custom step, early termination)
    print("\n  Method 4 — while loop (every 3rd element):")
    i = 0
    while i < len(nums):
        print(f"    nums[{i}] = {nums[i]}")
        i += 3


# =============================================================================
# SECTION 5: List Comprehensions (5 Forms)
# =============================================================================

def comprehensions_demo():
    print("\n" + "=" * 60)
    print("SECTION 5: List Comprehensions")
    print("=" * 60)

    # 1. Basic
    squares = [x**2 for x in range(1, 8)]
    print(f"\n  Basic  [x²]:           {squares}")

    # 2. Filtered (if AFTER for)
    evens = [x for x in range(10) if x % 2 == 0]
    print(f"  Filtered [evens]:      {evens}")

    # 3. If-else expression (BEFORE for — note order!)
    labels = ["even" if x % 2 == 0 else "odd" for x in range(6)]
    print(f"  If-else [labels]:      {labels}")
    print(f"  Rule: filter 'if' → AFTER for | conditional value → BEFORE for")

    # 4. Nested / flatten
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [val for row in matrix for val in row]
    print(f"  Nested (flatten):      {flat}")

    # 5. Dict / Set / Generator
    names = ["alice", "bob", "charlie"]
    name_len = {name: len(name) for name in names}
    print(f"  Dict comprehension:    {name_len}")

    nums_dup = [1, 2, 2, 3, 3, 3]
    unique_sq = {x**2 for x in nums_dup}      # set — no duplicates
    print(f"  Set comprehension:     {unique_sq}")

    gen = (x**2 for x in range(1_000_000))    # generator — lazy O(1) memory
    print(f"  Generator object:      {gen}  ← lazy, call next()")
    print(f"  First 5 squares:       {[next(gen) for _ in range(5)]}")

    # Invert a dict
    d = {"a": 1, "b": 2, "c": 3}
    inv = {v: k for k, v in d.items()}
    print(f"  Dict inversion:        {d} → {inv}")


# =============================================================================
# SECTION 6: Tuples — Immutable Sequences
# =============================================================================
#
# MENTAL MODEL:
#   LIST   (mutable):  lst[0] = 99   → OK, in-place mutation
#   TUPLE  (immutable): tup[0] = 99  → TypeError immediately
#
# Because tuples never change, they are HASHABLE → usable as dict keys / set elements.
#
# SINGLE-ELEMENT GOTCHA: the COMMA makes a tuple, not the parentheses:
#   (42,)  → <class 'tuple'>
#   (42)   → <class 'int'>

def tuples_demo():
    print("\n" + "=" * 60)
    print("SECTION 6: Tuples")
    print("=" * 60)

    # Creation
    t1 = (10, 20, 30)
    t2 = 10, 20, 30           # packing — comma creates tuple, NOT parens
    t3 = tuple([1, 2, 3])
    t4 = tuple("hello")
    print(f"\n  (10,20,30):       {t1}  type={type(t1).__name__}")
    print(f"  10, 20, 30:       {t2}  ← comma makes it a tuple!")
    print(f"  tuple([1,2,3]):   {t3}")
    print(f"  tuple('hello'):   {t4}")

    # Single-element gotcha
    single = (42,)             # ← tuple
    not_tup = (42)             # ← just int
    print(f"\n  (42,) → {type(single).__name__}   (42) → {type(not_tup).__name__}")
    print(f"  The COMMA is what makes a single-element tuple, NOT the parentheses!")

    # Immutability proof
    t = (10, 20, 30)
    print(f"\n  t = {t}")
    try:
        t[0] = 99
    except TypeError as e:
        print(f"  t[0] = 99 → TypeError: {e}")

    # BUT: mutable objects INSIDE a tuple CAN change (tuple holds the reference)
    mutable_in_tuple = ([1, 2], [3, 4])
    mutable_in_tuple[0].append(99)
    print(f"  Mutable inside tuple: {mutable_in_tuple}  ← inner list changed!")

    # Unpacking
    point = (3, 7)
    x, y = point
    print(f"\n  Tuple unpacking: x={x}, y={y}")

    # Extended unpacking with *
    first, *rest = [1, 2, 3, 4, 5]
    print(f"  first, *rest = [1..5]: first={first}, rest={rest}")

    *rest2, last = [1, 2, 3, 4, 5]
    print(f"  *rest2, last = [1..5]: rest={rest2}, last={last}")

    a, *mid, b = [1, 2, 3, 4, 5]
    print(f"  a, *mid, b   = [1..5]: a={a}, mid={mid}, b={b}")

    # Swap without temp variable
    a, b = 10, 20
    a, b = b, a          # Python evaluates RHS as a tuple (20,10) first
    print(f"\n  Swap: a={a}, b={b}  (tuple packing/unpacking under the hood)")

    # Tuple as dict key (list cannot be a key — not hashable)
    location = {(28.6, 77.2): "Delhi", (19.0, 72.8): "Mumbai"}
    print(f"\n  Tuple dict keys: {location[(28.6, 77.2)]}")

    # namedtuple — readable field access, still immutable, still a tuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 7)
    print(f"  namedtuple: {p}, x={p.x}, y={p.y}  type={type(p).__name__}")


# =============================================================================
# SECTION 7: Dictionaries — How O(1) Works
# =============================================================================
#
# HASH TABLE MECHANICS:
#   1. Compute h = hash(key)              — deterministic, fast
#   2. bucket = h % table_size            — direct array index
#   3. Read/write at that slot            — O(1) array access
#
# WHY WORST-CASE O(n):
#   COLLISION: two different keys produce the same bucket index.
#   CPython uses OPEN ADDRESSING (probe next slot).
#   Adversarial/pathological keys → all land in same bucket → O(n) scan.
#
# Python 3.7+ guarantees INSERTION ORDER during iteration.
# From Python 3.9+, dict supports `|` merge operator.

def dictionaries_demo():
    print("\n" + "=" * 60)
    print("SECTION 7: Dictionaries")
    print("=" * 60)

    # Creation patterns
    d1 = {"India": "Delhi", "Japan": "Tokyo"}     # literal
    d2 = dict(India="Delhi", Japan="Tokyo")        # keyword constructor
    d3 = dict([("a", 1), ("b", 2)])                # from list of pairs
    d4 = {}                                        # empty dict (NOT set!)
    print(f"\n  Literal:           {d1}")
    print(f"  dict() keyword:    {d2}")
    print(f"  dict(list pairs):  {d3}")
    print(f"  Empty {{}}:          {d4}  type={type(d4).__name__}")

    # Core operations — all O(1) average
    cap = {"India": "Delhi", "Russia": "Moscow", "Japan": "Tokyo", "France": "Paris"}
    print(f"\n  Initial: {cap}")

    cap["USA"] = "Washington"           # insert
    print(f"  After insert USA:  {cap}")

    cap["Russia"] = "St. Petersburg"   # update
    print(f"  After update Russia: {cap}")

    del cap["France"]                   # delete — KeyError if missing
    print(f"  After del France:  {cap}")

    # Safe lookup — .get() prevents KeyError
    found = cap.get("India")           # "Delhi"
    missing = cap.get("Spain")         # None (no error!)
    default = cap.get("Spain", "N/A")  # "N/A" fallback
    print(f"\n  .get('India')        = {found}")
    print(f"  .get('Spain')        = {missing}   ← None, no KeyError")
    print(f"  .get('Spain', 'N/A') = {default}   ← default fallback")

    # Membership: O(1) via hash
    print(f"\n  'Japan' in cap: {('Japan' in cap)}   ← O(1) hash lookup")
    print(f"  'Spain' in cap: {('Spain' in cap)}  ← O(1) hash lookup")

    # Guard pattern — check before access
    key = "Spain"
    if key in cap:
        print(f"  {cap[key]}")
    else:
        print(f"  {key} not found (checked with 'in' to avoid KeyError)")

    # Iteration — .keys(), .values(), .items() — all return VIEW objects O(1)
    print(f"\n  .keys()   (view): {list(cap.keys())}")
    print(f"  .values() (view): {list(cap.values())}")
    print(f"  .items()  (view, O(n) to iterate):")
    for country, capital in cap.items():
        print(f"    {country}: {capital}")

    # defaultdict — auto-initialises missing keys
    print("\n  --- defaultdict(int) ---")
    freq = defaultdict(int)        # missing keys auto-init to int() = 0
    for ch in "hello world":
        freq[ch] += 1              # no KeyError, no .get() needed
    print(f"  Frequency of 'hello world': {dict(freq)}")

    # Dict comprehension
    nums = [1, 2, 3, 4, 5]
    sq_dict = {x: x**2 for x in nums}
    print(f"\n  Dict comprehension {{x: x²}}: {sq_dict}")

    # Sort by value
    by_val = sorted(sq_dict.items(), key=lambda kv: kv[1])
    print(f"  Sorted by value: {by_val}")


# =============================================================================
# SECTION 8: Sets — Hash Sets
# =============================================================================
#
# A set is a DICTIONARY with only keys, no values.
# Same O(1) average hash mechanism — no linear scan needed for membership.
#
# CRUCIAL DISTINCTION:
#   {}    → empty DICT
#   set() → empty SET
#
# REMOVE vs DISCARD:
#   .remove(x)  → KeyError if x not found
#   .discard(x) → silent, safe if x not found

def sets_demo():
    print("\n" + "=" * 60)
    print("SECTION 8: Sets")
    print("=" * 60)

    # Creation
    s1 = {1, 2, 3, 4, 5}           # literal (at least one element)
    s2 = set([1, 2, 2, 3, 3, 3])   # from list — deduplicates automatically
    empty_set = set()               # MUST use set(), not {} (that's a dict!)
    country_set = set(["India", "Russia", "India", "Japan"])
    print(f"\n  Literal {{1..5}}:            {s1}")
    print(f"  set([1,2,2,3,3,3]):        {s2}  (duplicates removed)")
    print(f"  set():                     {empty_set}  type={type(empty_set).__name__}")
    empty_dict_type = type({}).__name__
    print(f"  {{}} type:                  {empty_dict_type}  ← DICT, not set!")
    print(f"  country_set:               {country_set}")

    # Core operations
    s = {1, 2, 3}
    s.add(4)
    print(f"\n  s.add(4): {s}")

    s.add(2)                        # duplicate — silently ignored
    print(f"  s.add(2) [dup]: {s}   ← unchanged")

    s.remove(4)                     # KeyError if 4 not present
    print(f"  s.remove(4): {s}")

    s.discard(99)                   # safe — no error even though 99 not in set
    print(f"  s.discard(99) [safe]: {s}  ← no KeyError")

    s.update([10, 20, 30])          # O(k) add multiple elements
    print(f"  s.update([10,20,30]): {s}")

    # O(1) membership — THE key advantage over list
    print(f"\n  3 in s  : {3 in s}   ← O(1) hash lookup (vs O(n) for list!)")
    print(f"  99 in s : {99 in s}  ← O(1)")

    # Deduplication
    arr = [1, 1, 2, 2, 3, 3, 3, 4]
    unique = list(set(arr))
    print(f"\n  Deduplicate {arr} → {unique}")
    print(f"  Note: set() does NOT preserve order. For order-preserving dedup,")
    print(f"  use: seen=set(); [x for x in lst if not (x in seen or seen.add(x))]")

    # Set mathematics
    a = {1, 2, 3, 4, 5}
    b = {3, 4, 5, 6, 7}
    print(f"\n  a = {a}, b = {b}")
    print(f"  Union      a | b : {a | b}")
    print(f"  Intersect  a & b : {a & b}")
    print(f"  Difference a - b : {a - b}")
    print(f"  Sym. diff  a ^ b : {a ^ b}")

    # Set comprehension
    nums_dup = [1, 2, 2, 3, 3, 3]
    sq_set = {x**2 for x in nums_dup}
    print(f"\n  Set comprehension {{x² for x in {nums_dup}}}: {sq_set}")


# =============================================================================
# SECTION 9: Frequency Counting — 4 Tools Compared
# =============================================================================
#
# COMMON INTERVIEW TASK: count occurrences, find most common, detect duplicates.
#
# TOOL COMPARISON:
#   Tool                         Time     Space  Use when
#   set(lst)                     O(n)     O(k)   Unique values only, no counts
#   Manual dict loop             O(n)     O(k)   Educational / interviews
#   {x: lst.count(x) ...}        O(n·k)   O(k)   ⚠️ AVOID for large data
#   collections.Counter(lst)     O(n)     O(k)   ALWAYS prefer for frequency work

def frequency_demo():
    print("\n" + "=" * 60)
    print("SECTION 9: Frequency Counting — 4 Tools")
    print("=" * 60)

    items = ["shoes", "shirts", "shoes", "jackets", "shirts", "shoes"]
    print(f"\n  items = {items}")

    # Tool 1: set() — unique values, no counts
    unique = set(items)
    print(f"\n  Tool 1: set()   = {unique}  ← unique only, O(n)")

    # Tool 2: manual dict (educational — shows what Counter does internally)
    freq_manual: Dict[str, int] = {}
    for item in items:
        freq_manual[item] = freq_manual.get(item, 0) + 1
    print(f"  Tool 2: manual dict = {freq_manual}  O(n)")

    # Tool 3: dict comprehension + .count() — O(n·k) TRAP
    # .count() re-scans the ENTIRE list for EVERY unique item
    unique_set = set(items)
    freq_comp = {x: items.count(x) for x in unique_set}  # O(n * k) — slow!
    print(f"  Tool 3: dict comp  = {freq_comp}  ⚠️ O(n·k) — avoid for large data")

    # Tool 4: Counter — THE right tool
    c = Counter(items)
    print(f"\n  Tool 4: Counter    = {c}")
    print(f"    c['shoes']          = {c['shoes']}   ← direct access")
    print(f"    c['pants'] (missing)= {c['pants']}   ← 0, no KeyError! (unlike dict)")
    print(f"    .most_common()      = {c.most_common()}")
    print(f"    .most_common(1)     = {c.most_common(1)}  ← top 1")
    print(f"    top item name       = {c.most_common(1)[0][0]}")

    # Counter arithmetic
    more = Counter(["shoes", "hats", "hats"])
    combined = c + more
    print(f"    Counter + Counter   = {combined}")

    # max(dict, key=dict.get) — find key with largest value without Counter
    top_manual = max(freq_manual, key=freq_manual.get)
    print(f"\n  max(dict, key=dict.get) = {top_manual!r}  ← O(k) after O(n) build")


# =============================================================================
# SECTION 10: L15 Maps — Brute to Optimal Evolutions (From Lecture Notes)
# =============================================================================

# --- Problem 1: Contains Duplicate ---
# Given an array, return True if any value appears more than once.
#
# BRUTE FORCE: O(n²) — compare every pair
# OPTIMAL:     O(n)  — use set or defaultdict(int)
#              Key insight: a set lookup is O(1) vs O(n) for list scan.
#              First time we see a value we add it; second time → duplicate.

def contains_duplicate_brute(arr: List[int]) -> bool:
    """Brute force: O(n²) time, O(1) space. Compare every pair."""
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False

def contains_duplicate_optimal(arr: List[int]) -> bool:
    """
    Optimal: O(n) time, O(n) space.
    Use defaultdict(int) — same as lecture L15/004containsDuplicate.py.
    The moment any frequency exceeds 1, return True immediately.
    """
    freq_map = defaultdict(int)
    for x in arr:
        freq_map[x] += 1
        if freq_map[x] > 1:         # early exit — first duplicate found
            return True
    return False

def contains_duplicate_set(arr: List[int]) -> bool:
    """
    Cleanest variant: O(n) time, O(n) space.
    A set enforces uniqueness — len(set) < len(arr) means a duplicate exists.
    """
    return len(set(arr)) < len(arr)


# --- Problem 2: Longest Consecutive Sequence ---
# Given unsorted array, find length of longest consecutive sequence.
# Example: [100, 4, 200, 1, 3, 2] → 4  (sequence: 1, 2, 3, 4)
#
# BRUTE FORCE: O(n²) — for each element, scan for next consecutive
# NAIVE SORT:  O(n log n) — sort, then walk
# OPTIMAL:     O(n)  — dict as "start-map"
#              Mark each number True/False for whether it is a sequence start.
#              A number x is NOT a start if x-1 is in the dict.

def longest_consecutive_brute(nums: List[int]) -> int:
    """Brute: O(n²) time, O(1) space."""
    if not nums:
        return 0
    best = 0
    for x in nums:
        length = 1
        current = x + 1
        while current in nums:       # O(n) set/list scan for each element
            length += 1
            current += 1
        best = max(best, length)
    return best

def longest_consecutive_optimal(nums: List[int]) -> int:
    """
    Optimal: O(n) time (amortized), O(n) space.
    From L15/005longestConsecutiveSequence.py — dict as start-map.

    Step 1: Build a dict. x is a 'start' (True) unless x-1 also exists.
    Step 2: For each start, walk forward counting consecutive elements.

    Each element is visited at most twice → O(n) total.
    """
    if not nums:
        return 0

    start_map: Dict[int, bool] = {}

    # Mark which numbers are sequence starters
    for x in nums:
        if x - 1 in start_map:
            start_map[x] = False    # x has a predecessor, not a start
        else:
            start_map[x] = True     # no predecessor — x IS a start

        if x + 1 in start_map:
            start_map[x + 1] = False  # x+1 has a predecessor now (x)

    # Walk from each start
    max_so_far = 0
    for k, is_start in start_map.items():
        if is_start:
            cnt = 0
            while k in start_map:
                cnt += 1
                k += 1
            max_so_far = max(max_so_far, cnt)

    return max_so_far


# --- Problem 3: Longest Palindrome (from character frequency) ---
# Given a string, find the length of the longest palindrome you can build.
# Example: "abccccdd" → 7  ("dccaccd")
#
# KEY INSIGHT:
#   - Every character appearing an EVEN number of times contributes fully.
#   - At most ONE character appearing an ODD number of times can sit in the centre.
#
# OPTIMAL APPROACH: O(n) time, O(52) = O(1) space
# Use a SET as a character TOGGLE.
# When we see a character the 2nd time, we can form a pair → remove from set, +2.
# Any characters remaining in the set at the end → at most 1 can be the centre.
# (From L15/007longestPalindrome.py)

def longest_palindrome_brute(s: str) -> int:
    """
    Brute (conceptual): O(n) time but uses full Counter dict.
    Count each char; add all even counts, add 1 if any odd count exists.
    """
    freq = Counter(s)
    length = 0
    has_odd = False
    for count in freq.values():
        length += count - (count % 2)  # use the largest even portion
        if count % 2 == 1:
            has_odd = True
    return length + (1 if has_odd else 0)

def longest_palindrome_optimal(s: str) -> int:
    """
    Optimal: O(n) time, O(52) ≈ O(1) space.
    From L15/007longestPalindrome.py — set toggle approach.

    Toggle: first occurrence → add to set.
            second occurrence → we have a PAIR → remove from set, ans += 2.
    After loop: any chars left in set are unpaired; add 1 for the centre.

    Space: O(1) because the set holds at most 52 distinct characters (a-z, A-Z).
    """
    seen: Set[str] = set()
    ans = 0

    for ch in s:
        if ch in seen:
            ans += 2          # paired → contributes fully to palindrome
            seen.remove(ch)   # toggle back off
        else:
            seen.add(ch)      # first occurrence — not yet paired

    if len(seen) > 0:
        ans += 1              # at most one unpaired char can sit in the centre

    return ans


# --- Problem 4: Word Frequency Counter ---
# Classic dict interview problem: count occurrences of each word.
# Time: O(n) | Space: O(k), k = unique words

def word_frequency(text: str) -> Dict[str, int]:
    """
    Count occurrences of each word (case-insensitive).
    Uses .get(word, 0) safe lookup — no KeyError.
    Equivalent to defaultdict(int) approach.
    """
    freq: Dict[str, int] = {}
    for word in text.lower().split():
        freq[word] = freq.get(word, 0) + 1
    return freq


# --- Problem 5: Remove Duplicates Preserving Order ---
# list(set(lst)) removes duplicates but does NOT preserve order.
# Use a seen-set alongside the output list for order-preserving O(n) dedup.
# Time: O(n) | Space: O(n)

def remove_duplicates_ordered(lst: List[int]) -> List[int]:
    """
    Remove duplicates preserving first-occurrence order.
    Time: O(n) | Space: O(n)
    """
    seen: Set[int] = set()
    result: List[int] = []
    for x in lst:
        if x not in seen:    # O(1) set lookup
            seen.add(x)
            result.append(x)
    return result


# --- Problem 6: Rotate List ---
# Rotate array k positions to the right using slicing.
# Time: O(n) | Space: O(n)

def rotate_right(lst: List[int], k: int) -> List[int]:
    """
    Rotate right by k using slice concatenation.
    k %= n handles k > len(lst).
    """
    n = len(lst)
    if n == 0:
        return lst
    k %= n
    return lst[-k:] + lst[:-k]


def l15_problems_demo():
    print("\n" + "=" * 60)
    print("SECTION 10: L15 Maps — Brute → Optimal")
    print("=" * 60)

    # --- Contains Duplicate ---
    print("\n  Problem 1: Contains Duplicate")
    tests_dup = [([1, 2, 3, 1], True), ([1, 2, 3, 4], False), ([1, 1, 1, 3, 3, 4, 3], True)]
    for arr, expected in tests_dup:
        brute = contains_duplicate_brute(arr)
        opt   = contains_duplicate_optimal(arr)
        s     = contains_duplicate_set(arr)
        print(f"    {arr} → brute={brute} | dict={opt} | set={s}  (expected {expected})")

    # --- Longest Consecutive Sequence ---
    print("\n  Problem 2: Longest Consecutive Sequence")
    tests_seq = [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([], 0),
    ]
    for nums, expected in tests_seq:
        brute = longest_consecutive_brute(nums[:])
        opt   = longest_consecutive_optimal(nums[:])
        print(f"    {nums}")
        print(f"      brute={brute} | optimal={opt}  (expected {expected})")

    # --- Longest Palindrome ---
    print("\n  Problem 3: Longest Palindrome (from string)")
    tests_pal = [("abccccdd", 7), ("a", 1), ("Aa", 1), ("aababab", 5), ("bb", 2)]
    for s, expected in tests_pal:
        brute = longest_palindrome_brute(s)
        opt   = longest_palindrome_optimal(s)
        print(f"    '{s}' → brute={brute} | optimal(set-toggle)={opt}  (expected {expected})")

    # --- Word Frequency ---
    print("\n  Problem 4: Word Frequency")
    sentence = "the cat sat on the mat the cat"
    freq = word_frequency(sentence)
    print(f"    '{sentence}'")
    print(f"    → {freq}")

    # --- Remove Duplicates Ordered ---
    print("\n  Problem 5: Remove Duplicates Preserving Order")
    lst_dup = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    print(f"    {lst_dup} → {remove_duplicates_ordered(lst_dup)}")

    # --- Rotate Right ---
    print("\n  Problem 6: Rotate Right")
    print(f"    rotate_right([1,2,3,4,5], k=2) = {rotate_right([1,2,3,4,5], 2)}")
    print(f"    rotate_right([1,2,3,4,5], k=7) = {rotate_right([1,2,3,4,5], 7)}  (k>n handled)")


# =============================================================================
# PRACTICE SKELETONS
# =============================================================================

def practice_frequency_counter(arr: List[int]) -> Dict[int, int]:
    """
    Return a frequency map of arr using a manual dict + .get().
    Do NOT use Counter. Time: O(n) | Space: O(k)
    """
    pass

def practice_find_unique_ordered(arr: List[int]) -> List[int]:
    """
    Return unique elements preserving first-occurrence order.
    Use a set for O(1) membership checks. Time: O(n) | Space: O(n)
    """
    pass

def practice_contains_duplicate_set(arr: List[int]) -> bool:
    """
    Return True if arr has any duplicate. Use a set.
    Hint: compare len(set(arr)) to len(arr). Time: O(n) | Space: O(n)
    """
    pass

def practice_top_k_frequent(arr: List[int], k: int) -> List[int]:
    """
    Return the k most frequent elements.
    Hint: Counter(arr).most_common(k). Time: O(n log k) | Space: O(n)
    """
    pass

def practice_longest_palindrome(s: str) -> int:
    """
    Find the length of the longest palindrome buildable from s.
    Use the set-toggle approach from L15.
    Time: O(n) | Space: O(1) — max 52 chars
    """
    pass

def practice_two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Return (i, j) such that nums[i] + nums[j] == target.
    Use a dict {value: index} for O(1) complement lookup.
    Time: O(n) | Space: O(n)
    """
    pass

def practice_group_even_odd(lst: List[int]) -> Dict[str, List[int]]:
    """
    Return {"even": [...], "odd": [...]} using list comprehensions.
    Time: O(n) | Space: O(n)
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    list_internals_demo()
    slicing_demo()
    initialization_demo()
    loop_patterns_demo()
    comprehensions_demo()
    tuples_demo()
    dictionaries_demo()
    sets_demo()
    frequency_demo()
    l15_problems_demo()

    print("\n" + "=" * 60)
    print("PRACTICE SKELETONS")
    print("=" * 60)
    print("frequency_counter([1,2,2,3,3,3]):", practice_frequency_counter([1, 2, 2, 3, 3, 3]))
    print("find_unique_ordered([3,1,4,1,5,9]):", practice_find_unique_ordered([3, 1, 4, 1, 5, 9]))
    print("contains_dup_set([1,2,3,1]):", practice_contains_duplicate_set([1, 2, 3, 1]))
    print("top_k_frequent([1,1,1,2,2,3], k=2):", practice_top_k_frequent([1, 1, 1, 2, 2, 3], 2))
    print("longest_palindrome('abccccdd'):", practice_longest_palindrome("abccccdd"))
    print("two_sum([2,7,11,15], target=9):", practice_two_sum([2, 7, 11, 15], 9))
    print("group_even_odd([1..6]):", practice_group_even_odd([1, 2, 3, 4, 5, 6]))
    print("=" * 60)
    print("Fill in the skeletons above and re-run to verify.")
