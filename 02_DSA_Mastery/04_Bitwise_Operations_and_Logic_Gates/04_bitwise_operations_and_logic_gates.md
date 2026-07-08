# 04 - Bitwise Operations and Logic Gates

## 1. Why Bitwise Operations Matter

Bitwise operations evaluate data at the **binary level** (individual 0s and 1s). They matter for three reasons:

1. **Speed**: They map directly to single CPU instructions (one clock cycle). `n << 1` is one instruction; `n * 2` may take several.
2. **Space**: They let you pack multiple boolean flags into a single integer — a common system programming and interview pattern.
3. **Interview prevalence**: A significant category of LeetCode problems (unique elements, power checks, bit counting) have O(n) solutions with O(n) space that reduce to O(n) time and **O(1) space** with bit tricks.

### Real-World Applications

| Domain | Bitwise Use |
|---|---|
| OS Permissions | Linux `rwx` = `111₂` = 7. `chmod 644` = `110 100 100₂` |
| Feature Flags | Enable/disable features by flipping individual bits in a config int |
| Networking | Subnet masks: `IP & mask` uses AND to determine network address |
| Cryptography | XOR is fundamental to stream ciphers and one-time pads |
| Graphics | RGBA pixel: 4 bytes packed into one 32-bit int (8 bits per channel) |
| Compression | Huffman coding reads and writes individual bits |

---

## 2. Binary Number System Refresher

Every bit position represents a power of 2, read **right to left**:

```
Position:   7    6    5    4    3    2    1    0
Value:    128   64   32   16    8    4    2    1
```

**Decimal → Binary conversion of 25:**
$$25 = 16 + 8 + 1 = 2^4 + 2^3 + 2^0 = \texttt{11001}_2$$

**Python formatting:**
```python
bin(25)       # '0b11001'   (with prefix)
f"{25:08b}"   # '00011001'  (zero-padded to 8 bits, no prefix — use in diagrams)
```

---

## 3. The Six Bitwise Operators

For all diagrams, using `a = 25 = 11001₂` and `b = 19 = 10011₂`.

### 3.1 AND (`&`) — Both bits must be 1 (masking, extracting bits)

```
  25 = 1 1 0 0 1
  19 = 1 0 0 1 1
  ─────────────
  &  = 1 0 0 0 1  = 17
```

### 3.2 OR (`|`) — At least one bit is 1 (setting bits, combining flags)

```
  25 = 1 1 0 0 1
  19 = 1 0 0 1 1
  ─────────────
  |  = 1 1 0 1 1  = 27
```

### 3.3 XOR (`^`) — Exactly one bit is 1 / bits differ (toggling, unique-element problems)

```
  25 = 1 1 0 0 1
  19 = 1 0 0 1 1
  ─────────────
  ^  = 0 1 0 1 0  = 10
```

**XOR properties to memorize:**
- `a ^ a = 0` — any number XOR itself cancels to 0
- `a ^ 0 = a` — any number XOR 0 is unchanged
- Commutative: `a ^ b = b ^ a`
- Associative: `(a ^ b) ^ c = a ^ (b ^ c)`

### Side-by-side Truth Table

| Bit A | Bit B | A AND B | A OR B | A XOR B |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

### 3.4 NOT (`~`) — Flip all bits

Python uses **two's complement** with **arbitrary precision** integers.

> [!IMPORTANT]
> For any integer `n`:  `~n = -(n + 1)`
>
> **Why?** Python integers are conceptually infinite-precision. `~n` flips every bit,
> including the infinitely many leading 0s. The result is the two's complement negative:
> ```
>   ~0 = -(0+1) = -1
>   ~5 = -(5+1) = -6
>   ~25 = -(25+1) = -26
> ```
> This differs from 32-bit languages (Java/C++) where `~5` gives `0xFFFFFFFA`.

### 3.5 Left Shift (`<<`) — Multiply by 2^k

Each left shift slides all bits left by 1 position and fills the rightmost slot with `0`.

```
5 = 1 0 1
5 << 1 = 1 0 1 0   → 10   (5 × 2¹)
5 << 2 = 1 0 1 0 0 → 20   (5 × 2²)
```

**Formula:** `n << k = n × 2^k`

### 3.6 Right Shift (`>>`) — Floor divide by 2^k

Each right shift slides bits right, the rightmost bits **fall off and are lost**.

```
8 = 1 0 0 0
8 >> 1 = 0 1 0 0 → 4    (8 ÷ 2¹)
8 >> 2 = 0 0 1 0 → 2    (8 ÷ 2²)
7 >> 1 = 0 0 1 1 → 3    (7 // 2 = 3, floor division)
```

**Formula:** `n >> k = n // 2^k` (always floor, remainder is discarded)

---

## 4. The Four Bit Manipulation Idioms (k is 0-indexed from the right)

These four operations are the foundation of all advanced bit tricks. All are **O(1)** — a single expression, single CPU instruction.

| Goal | Expression | Mask used | Operator |
|---|---|---|---|
| **Set** bit k to 1 | `n \| (1 << k)` | `1 << k` has only bit k set | OR forces it to 1 |
| **Clear** bit k to 0 | `n & ~(1 << k)` | `~(1 << k)` has all bits set *except* k | AND forces it to 0 |
| **Check** if bit k is set | `(n >> k) & 1` | Shift k to position 0, then AND with 1 | Returns 0 or 1 |
| **Flip/Toggle** bit k | `n ^ (1 << k)` | `1 << k` has only bit k set | XOR flips it |

**Worked example for n = 21 (`00010101₂`), k = 2:**

```
Set   bit 2:  00010101 | 00000100 = 00010101  (bit 2 already set → stays 1)
Clear bit 2:  00010101 & 11111011 = 00010001  (bit 2 cleared → 17)
Check bit 2:  (21 >> 2) & 1 = 5 & 1 = 1      (bit 2 IS set)
Flip  bit 2:  00010101 ^ 00000100 = 00010001  (bit 2 flipped 1→0 → 17)
```

---

## 5. Count Set Bits (Hamming Weight / Popcount)

### Method 1: Right-shift loop — O(log n) time

Check the LSB (`n & 1`), add it, then shift right. Iterates once per **bit position**.

For n = 25 = `11001₂` → 5 bits → 5 iterations. Complexity: **O(log n)** = O(number of bits).

### Method 2: Brian Kernighan's Algorithm — O(k) time (k = set bits)

`n & (n - 1)` removes the **rightmost set bit** in one operation.

**Why?** Subtracting 1 flips all bits from the rightmost set bit onwards:
```
n   = 1 0 1 0 0  (20)
n-1 = 1 0 0 1 1  (19)   ← rightmost set bit and everything right flipped
n & (n-1) = 1 0 0 0 0  (16)  ← rightmost set bit GONE
```

**Advantage**: For n = 25 (`11001₂`, 3 set bits), only **3 iterations** instead of 5.

**Walkthrough for n = 25:**

| Step | n (binary) | n-1 (binary) | n & (n-1) |
|---|---|---|---|
| 1 | `00011001` | `00011000` | `00011000` = 24 |
| 2 | `00011000` | `00010111` | `00010000` = 16 |
| 3 | `00010000` | `00001111` | `00000000` = 0 → done |

3 iterations → 3 set bits ✅

---

## 6. Power of 2 Check — O(1)

Powers of 2 have **exactly one set bit**: `1, 2, 4, 8, 16 → 00000001, 00000010, 00000100...`

`n & (n-1)` removes the single set bit → result is `0`. This is the check.

```
n = 16 = 10000,  n-1 = 01111,  n & (n-1) = 00000  → IS power of 2 ✅
n = 20 = 10100,  n-1 = 10011,  n & (n-1) = 10000  → NOT power of 2 ❌
```

> [!CAUTION]
> Edge case: `n = 0` returns `True` without the guard check (`n & -1 == 0`).
> Always check `n > 0 and (n & (n-1)) == 0`.

---

## 7. XOR Unique Element Pattern — O(n) time, O(1) space

Given an array where every element appears **twice** except one, XOR all elements.

Pairs cancel: `a ^ a = 0`. Unique remains: `0 ^ unique = unique`.

This pattern extends to:
- **Two unique elements** (LeetCode 260): XOR all → get `u1 ^ u2`. Find any set bit. Partition array by that bit. XOR each partition to get each unique element.
- **Missing number** (LeetCode 268): XOR `0..n` against all array elements.

---

## 8. Advanced Tricks

### Isolate rightmost set bit — `n & (-n)`

`-n` in two's complement = `~n + 1`. This flips all bits then adds 1, which preserves the rightmost set bit position and zeros everything else:

```
n    = 0 1 0 1 0 0  (20)
-n   = 1 0 1 1 0 0  (two's complement)
n&-n = 0 0 0 1 0 0  (4)  ← only the rightmost set bit survives
```

### XOR Swap — no temp variable

```python
x ^= y   # x = x ^ y  (x "stores" the difference)
y ^= x   # y = y ^ (x^y) = x  (y recovers original x)
x ^= y   # x = (x^y) ^ x = y  (x recovers original y)
```

### Opposite signs check — `(a ^ b) < 0`

The MSB (sign bit) is 1 for negative numbers. XOR of opposite-sign numbers gives MSB=1 (negative result).

---

## 9. Python-Specific Notes

> [!WARNING]
> Python integers have **arbitrary precision** — no 32-bit overflow. When solving LeetCode problems with fixed 32-bit constraints (e.g., "Reverse Bits"), manually mask with `& 0xFFFFFFFF`.

> [!TIP]
> **Compound assignment operators**: `&=`, `|=`, `^=`, `<<=`, `>>=`
> Work exactly like `+=` and `*=`.
> Precedence: `a &= b - 1` means `a = a & (b - 1)`, NOT `(a & b) - 1`.

> [!NOTE]
> **Python 3.10+**: `int.bit_count()` is a built-in popcount — equivalent to Brian Kernighan but implemented in C. Use it in production; use the manual version in interviews to show you understand the algorithm.

---

## 10. Interview Quick-Reference Table

All single-expression bitwise operations are **O(1)** — they translate to **one CPU instruction**.

| Operation | Expression | Time |
|---|---|---|
| Check even | `(n & 1) == 0` | O(1) |
| Check odd | `(n & 1) == 1` | O(1) |
| Multiply by 2^k | `n << k` | O(1) |
| Divide by 2^k (floor) | `n >> k` | O(1) |
| Set k-th bit | `n \| (1 << k)` | O(1) |
| Clear k-th bit | `n & ~(1 << k)` | O(1) |
| Check k-th bit | `(n >> k) & 1` | O(1) |
| Flip k-th bit | `n ^ (1 << k)` | O(1) |
| Turn off rightmost set bit | `n & (n - 1)` | O(1) |
| Isolate rightmost set bit | `n & (-n)` | O(1) |
| Check power of 2 | `n > 0 and (n & (n-1)) == 0` | O(1) |
| Count set bits (shift loop) | loop: `n & 1`, `n >>= 1` | O(log n) |
| Count set bits (Kernighan) | loop: `n &= (n-1)` | O(k) |
| Swap without temp | XOR swap | O(1) |
| Find unique in pairs array | XOR all elements | O(n) |
| Opposite signs | `(a ^ b) < 0` | O(1) |

**Why O(1)?** A single bitwise expression is one CPU ALU instruction — independent of the value of `n`. No loops, no memory allocation, no recursion. The CPU evaluates it in one clock cycle at the hardware level, regardless of whether `n` is 5 or 5,000,000,000.
