# 03 - Pattern Printing and Pattern Problems

## Core Concepts

Pattern printing problems are the ultimate test of your understanding of **nested loops**. While you will rarely print stars (`*`) in a production codebase, the structural thinking required translates directly to matrix operations, image processing, and complex multi-dimensional array traversal.

### The Anatomy of a Pattern
Every pattern problem is a 2D grid.
- **Outer Loop (`i`)**: Controls the **Rows** (typically the y-axis, moving down).
- **Inner Loop (`j`)**: Controls the **Columns** (typically the x-axis, moving across the current row).

### Three Questions for Every Pattern
When analyzing a pattern to write code for it, ask yourself:
1. **How many rows are there?** (This defines the outer loop).
2. **For the $i$-th row, how many columns/characters are there?** (This defines the inner loop's condition).
3. **What is being printed?** (Stars, numbers, characters, spaces?).

## Diagram: Outer vs Inner Loop Relationship

```mermaid
graph LR
    subgraph Row i=1
        A[j=1: *] --- B[j=2: *] --- C[j=3: *]
    end
    subgraph Row i=2
        D[j=1: *] --- E[j=2: *]
    end
    subgraph Row i=3
        F[j=1: *]
    end
    
    A -.-> D
    D -.-> F
```
*Example of a decreasing triangle pattern.*

## Cheat Sheet: Common Structural Formulas

Let $N$ be the total number of rows.
> [!TIP]
> - **Square Grid**: `for i in range(N): for j in range(N):`
> - **Increasing Triangle**: `for i in range(N): for j in range(i + 1):` (Row 0 has 1 item, Row 1 has 2 items...)
> - **Decreasing Triangle**: `for i in range(N): for j in range(N - i):` (Row 0 has N items, Row 1 has N-1 items...)
> - **Pyramids**: Usually require an extra inner loop to print leading spaces `for s in range(N - i - 1):` before the stars.

> [!WARNING]
> In Python, `print()` automatically adds a newline `\n` at the end. 
> To print multiple characters on the *same line*, you MUST use `print("*", end="")`.
> To move to the next row, use an empty `print()` at the end of the outer loop iteration.
