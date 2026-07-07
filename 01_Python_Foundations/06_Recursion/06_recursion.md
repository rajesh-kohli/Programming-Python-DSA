# Module 06: Recursion

Recursion is a method where the solution to a problem depends on solutions to smaller instances of the same problem. A recursive function calls itself until it reaches a base case.

## Analogies
- **Russian Nesting Dolls**: Open a doll, find a smaller one, repeat until you find the solid one (base case).
- **Dictionary Lookup**: Look up a word, its definition has a word you don't know, look up that word... repeat until you find a word you know, then work backwards.

## Memory Segments

When a program runs, it uses memory divided into several segments:

```mermaid
flowchart TD
    subgraph RAM
        Code[Code Segment <br> Compiled instructions]
        Data[Data Segment <br> Global & Static vars]
        Heap[Heap Segment <br> Dynamic memory, Objects]
        Stack[Stack Segment <br> Local vars, Function calls]
    end
    
    Stack -.-> |Grows downwards| Heap
    Heap -.-> |Grows upwards| Stack
```

## The Call Stack

Every time a function is called, an "Activation Record" (or stack frame) is pushed onto the Stack. It stores local variables and where to return to.

```mermaid
sequenceDiagram
    participant Main
    participant fact4 as factorial(4)
    participant fact3 as factorial(3)
    participant fact2 as factorial(2)
    participant fact1 as factorial(1)
    
    Main->>fact4: call
    activate fact4
    fact4->>fact3: call
    activate fact3
    fact3->>fact2: call
    activate fact2
    fact2->>fact1: call
    activate fact1
    Note right of fact1: Base Case hit!
    fact1-->>fact2: returns 1
    deactivate fact1
    fact2-->>fact3: returns 2 * 1
    deactivate fact2
    fact3-->>fact4: returns 3 * 2
    deactivate fact3
    fact4-->>Main: returns 4 * 6 = 24
    deactivate fact4
```

## The Leap of Faith Template

> [!TIP]
> When writing recursive functions, follow this 3-step template:
> 1. **Base Case**: What is the simplest, smallest input that requires no calculation? (Stops the recursion)
> 2. **Recursive Work**: Do the small amount of work for the current step.
> 3. **Leap of Faith**: Call the function itself on a *smaller* input, assuming it will work correctly. Combine the result with step 2.

## Fibonacci Recursion Tree

The naive recursive Fibonacci calculates the same values over and over, leading to $O(2^n)$ time complexity.

```mermaid
flowchart TD
    F4["fib(4)"] --> F3["fib(3)"]
    F4 --> F2A["fib(2)"]
    
    F3 --> F2B["fib(2)"]
    F3 --> F1A["fib(1)"]
    
    F2A --> F1B["fib(1)"]
    F2A --> F0A["fib(0)"]
    
    F2B --> F1C["fib(1)"]
    F2B --> F0B["fib(0)"]
    
    style F2A fill:#f9f,stroke:#333,stroke-width:2px
    style F2B fill:#f9f,stroke:#333,stroke-width:2px
```
*Notice how `fib(2)` is calculated twice!*

## Complexity Table

| Pattern | Calls per level | Depth | Time Complexity | Space Complexity |
| --- | --- | --- | --- | --- |
| `f(n-1)` | 1 | $n$ | $O(n)$ | $O(n)$ |
| `f(n/2)` | 1 | $\log n$ | $O(\log n)$ | $O(\log n)$ |
| `f(n-1) + f(n-2)` | 2 | $n$ | $O(2^n)$ | $O(n)$ |

## Recursion vs Iteration

| Feature | Recursion | Iteration (Loops) |
| --- | --- | --- |
| **Code Length** | Usually shorter, elegant | Usually longer |
| **Memory** | Uses Stack memory $O(n)$, risk of Overflow | Uses $O(1)$ memory, no overflow |
| **Speed** | Slower (function call overhead) | Faster |
| **Best For** | Trees, graphs, divide & conquer | Simple sequences, flat arrays |
