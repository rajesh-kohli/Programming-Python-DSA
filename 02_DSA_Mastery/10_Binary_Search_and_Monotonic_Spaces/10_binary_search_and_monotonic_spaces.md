# 10 - Binary Search and Monotonic Spaces

## Core Concepts

Binary Search is an immensely powerful algorithm that operates in $O(\log n)$ time, making it vastly superior to $O(n)$ Linear Search for large datasets. 

### Prerequisites
The search space must be **monotonic**. This usually means the array must be **sorted** (either non-decreasing or non-increasing). If a function's output always moves in one direction as the input increases, binary search can be applied.

### How it Works
Instead of checking every element, binary search checks the `mid` point. Because the array is sorted:
- If `target == arr[mid]`, you found it.
- If `target > arr[mid]`, the target *must* be to the right. You eliminate the entire left half.
- If `target < arr[mid]`, the target *must* be to the left. You eliminate the entire right half.

Every step cuts the search space in half ($n \to n/2 \to n/4 \to \dots \to 1$), resulting in $O(\log n)$ operations.

## Diagram: Narrowing the Search Space

```mermaid
graph TD
    subgraph Iteration 1
        A[lo=0] --- B(...) --- C[mid=3<br>arr_mid < target] --- D(...) --- E[hi=6]
    end
    Iteration 1 --> |Target is greater| Iteration2
    
    subgraph Iteration2
        F[lo=4] --- G[mid=5<br>arr_mid > target] --- H[hi=6]
    end
    Iteration2 --> |Target is smaller| Iteration3
    
    subgraph Iteration3
        I[lo=4] --- J[mid=4<br>arr_mid == target] --- K[hi=4]
    end
    Iteration3 --> |Found!| Result((Index 4))
```

## Python `bisect` Module

Python provides built-in binary search via the `bisect` module. It's highly optimized and you should use it in interviews if you aren't explicitly asked to write binary search from scratch.

### `bisect_left(arr, target)`
Returns the **first** index where `target` should be inserted to maintain sorted order. 
- Conceptually: It finds the **first occurrence** of the target.
- If the target is not in the array, it returns the index of the first element *greater* than the target.

### `bisect_right(arr, target)` (or just `bisect(arr, target)`)
Returns the index **after** the last occurrence where `target` should be inserted.
- Conceptually: It finds the index immediately after the **last occurrence** of the target.
- `bisect_right - bisect_left` gives you the exact **count** of how many times `target` appears in the array.

## Cheat Sheet: When to apply Binary Search?

> [!TIP]
> - Is the array **sorted** and you need to find an element? -> Binary Search.
> - Do you need to find the **first or last occurrence** of a duplicate element? -> Modify Binary Search to keep searching left/right after finding a match.
> - Are you asked for an $O(\log n)$ time complexity solution? -> It almost certainly involves Binary Search or a Tree.
> - "Find the minimum in a rotated sorted array" -> Binary search.

> [!WARNING]
> Always be careful calculating `mid`. `mid = (lo + hi) // 2` is standard in Python because integers don't overflow like in Java/C++. In Java, you must use `mid = lo + (hi - lo) // 2`.
