###############################################################################
#                    Lecture 8 - Recursion (Complete Guide)                    #
###############################################################################


# =============================================================================
# SECTION 1: What is Recursion?
# =============================================================================

# Recursion = a function that CALLS ITSELF to solve a smaller version of the same problem.

## Recursion: A function calling itself again and again until some condition is satisfied
# Whenever we have a repetitive problem statement: two solutions exists:
# 1. Iterative approach (loops) 2. Recursive approach
# Dynamic Programming concept uses Recursion

#
# ----- Analogy: Russian Nesting Dolls -----
# Imagine opening a doll, and inside there's a smaller doll.
# You open that one — there's an even smaller doll inside.
# You keep opening until you reach the SMALLEST doll (the base case).
# Then you start closing them back up, one by one (returning values).
#
# ----- Analogy: Looking up a word in the dictionary -----
# You look up "happy" → definition says "feeling joy"
# You look up "joy" → definition says "great happiness"
# You look up "happiness" → you already know this word! STOP.
# Now you trace back: happiness → joy → happy. Done!
#
# ----- The Two Parts Every Recursive Function Needs -----

# To write any code in Recursion, we need to find two steps:
# 1. Anchor / Stop Step (BASE CASE): Where exactly we have to stop.
#    Without this, the function calls itself forever → crashes (stack overflow).
# 2. Inductive / Recursive step (RECURSIVE CASE): The function calls itself with a
#    SMALLER or SIMPLER input, moving toward the base case.
#
# Template:
#   def solve(problem):
#       if problem is simple enough:     # BASE CASE (Anchor Step)
#           return answer directly
#       else:                            # RECURSIVE CASE (Inductive Step)
#           smaller = make problem smaller
#           return combine(solve(smaller))

# Structure:
#   def fun():
#       # anchor step (base case)
#       # recursive step


# =============================================================================
# SECTION 2: How the Call Stack Works (KEY to understanding recursion)
# =============================================================================

# Whenever we are performing recursion, a STACK data structure is getting
# created in the stack segment of memory implicitly.

# ----- Memory Segments (from a Programmer's point of view) -----

# From OS point of view: memory is a collection of frames
# From Computer Architecture point of view: memory is a collection of blocks
# From Programmers point of view: Memory is a collection of segments --> Our focus
# Here Memory means - RAM (Primary memory of a computer)
# Memory is divided into 4 segments:
# 1. Code segment 2. Data Segment 3. Stack segment 4. Heap Segment
#   - Entire code will be stored in code segment. Read only. No modifications allowed
#   - All the global variables, global functions, static variables, constants → Data Segment
#   - Stack segment contains recursive function calls, local variables, etc.
#   - Heap Segment contains dynamic data structures, objects and classes
## These concepts will come up in detail in OOP
## Stack segment will grow → top to down
## Heap segment will grow → down to top

# ----- What is a Stack? -----

## Stack:
#   linear data structure (storing data one after the other)
#   organize data in a way that it gets structure and becomes meaningful
#   Goal: organize data optimally (less space to store, less time to execute)
## Structure of Stack:
#   One side open and one side closed
#   We can insert and delete elements from one side only (the "top")
#   Stack follows LIFO or FILO (Last In First Out or First In Last Out)
#   Two standard operations:
#       Push: Inserting elements onto the stack
#       Pop:  Removing/Deleting elements from the stack (TOS = top of stack)
#   Backend Usecase: Browsing history (visit page = push, Back button = pop)

# ----- How recursion uses the stack -----
# In recursive code, stack is getting created — what do we push and pop?
#   push → recursive function call is pushed onto the stack
#   pop  → after execution, the function returns a value that gets popped
#
# Each recursive call PUSHES a new "activation record" (frame) onto the stack.
# Each frame contains: the function's local variables and the return address.
# When the base case is reached, frames start getting POPPED (returned).

# The elements stored in stack during Recursion are called Activation Records.
# In the context of stack-based recursion, DAG (Directed Acyclic Graph)
# represents the hidden "call graph" or history of recursive calls.
# Recursion Tree is another method to trace the code and output.


# =============================================================================
# SECTION 3: Countdown (Simplest Possible Recursion)
# =============================================================================

# Let's start with the simplest example: counting down from n to 1.

def countdown(n):
    if n == 0:          # BASE CASE: nothing left to count
        print("Go!")
        return
    print(n)
    countdown(n - 1)    # RECURSIVE CASE: count down from n-1

countdown(5)

# ----- What happens when we call countdown(5)? -----
#
# countdown(5) prints 5, then calls countdown(4)
# countdown(4) prints 4, then calls countdown(3)
# countdown(3) prints 3, then calls countdown(2)
# countdown(2) prints 2, then calls countdown(1)
# countdown(1) prints 1, then calls countdown(0)
# countdown(0) prints "Go!" and RETURNS (base case!)
#
# Output: 5 4 3 2 1 Go!
#
# This is a "void" recursion — it doesn't return a value, just prints.
# The next examples return values, which is where the stack matters more.
#
# ----- Call stack snapshot at the deepest point (just before countdown(0)) -----
#   +---------------+
#   | countdown(0)  |  <- top, about to print "Go!" and return
#   +---------------+
#   | countdown(1)  |
#   +---------------+
#   | countdown(2)  |
#   +---------------+
#   | countdown(3)  |
#   +---------------+
#   | countdown(4)  |
#   +---------------+
#   | countdown(5)  |  <- bottom, the original call
#   +---------------+
# Each frame is waiting on the one above it; once countdown(0) returns,
# frames pop off top-down and nothing more happens (no work after the call).


# =============================================================================
# SECTION 4: Factorial (The Classic Example)
# =============================================================================

# factorial(n) = n! = n * (n-1) * (n-2) * ... * 2 * 1
# factorial(0) = 1    (by definition)
# factorial(5) = 5 * 4 * 3 * 2 * 1 = 120
#
# Recursive definition:
#   factorial(0) = 1                         (base case / anchor step)
#   factorial(n) = n * factorial(n - 1)      (recursive case / inductive step)

def factorial(n):
    if n == 0:                  # BASE CASE: 0! = 1
        return 1
    else:
        return n * factorial(n - 1)   # RECURSIVE CASE

print(factorial(5))   # 120

# ----- VISUAL CALL STACK TRACE for factorial(4) -----
#
# Step 1: PUSHING calls onto the stack (going DOWN to base case)
#
#   factorial(4) calls factorial(3)     → will return 4 * factorial(3)
#   factorial(3) calls factorial(2)     → will return 3 * factorial(2)
#   factorial(2) calls factorial(1)     → will return 2 * factorial(1)
#   factorial(1) calls factorial(0)     → will return 1 * factorial(0)
#   factorial(0) → BASE CASE!          → returns 1
#
#   Stack at this point (each box is a frame / activation record):
#   ┌──────────────┐
#   │ factorial(0)  │  ← TOP (base case reached, returns 1)
#   │ factorial(1)  │  ← waiting for factorial(0)
#   │ factorial(2)  │  ← waiting for factorial(1)
#   │ factorial(3)  │  ← waiting for factorial(2)
#   │ factorial(4)  │  ← waiting for factorial(3)
#   └──────────────┘
#
# Step 2: POPPING frames and computing results (going BACK UP)
#
#   factorial(0) returns 1                          → pop
#   factorial(1) gets 1, returns 1 * 1 = 1          → pop
#   factorial(2) gets 1, returns 2 * 1 = 2          → pop
#   factorial(3) gets 2, returns 3 * 2 = 6          → pop
#   factorial(4) gets 6, returns 4 * 6 = 24         → pop  ← FINAL ANSWER
#
# Result: 24
#
# ----- Expansion view -----
# factorial(4) = 4 * factorial(3)
#              = 4 * (3 * factorial(2))
#              = 4 * (3 * (2 * factorial(1)))
#              = 4 * (3 * (2 * (1 * factorial(0))))
#              = 4 * (3 * (2 * (1 * 1)))
#              = 4 * (3 * (2 * 1))
#              = 4 * (3 * 2)
#              = 4 * 6
#              = 24

# ----- Iterative version for comparison -----

def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Both give the same answer. Which is better?
# Iterative: O(n) time, O(1) space (just one variable)
# Recursive: O(n) time, O(n) space (n frames on the call stack!)
# For factorial, iterative is more efficient. But recursion is more intuitive
# for some problems (trees, divide-and-conquer, backtracking).

# Time:  O(n) — n recursive calls, each doing O(1) work
# Space: O(n) — n frames on the call stack at the deepest point
#
# How to derive: Count the calls: factorial(n) → factorial(n-1) → ... → factorial(0)
# That's n+1 calls ≈ O(n). Each call adds one stack frame → O(n) space.


# =============================================================================
# SECTION 5: Recursive Multiplication
# =============================================================================

## Recursive code for multiplication of two numbers
# 6*4 = 24
# Is multiplication a repetitive problem statement? Yes.
# It's repetition of addition (6+6+6+6) → It's repetitive, so we can use Recursion.
#
# Mul(6,4) = 6 + mul(6,3) = 6+6+mul(6,2) ... = 6+6+6+6+mul(6,0) → anchor step = 24
#
# Generalized function:
#   Mul(a,b) = a + Mul(a, b-1)    when b > 0    → recursive step
#            = 0                   when b = 0    → anchor step
#
# ----- Trace: recursive_mul(6, 4) -----
# mul(6,4) = 6 + mul(6,3)
#          = 6 + (6 + mul(6,2))
#          = 6 + (6 + (6 + mul(6,1)))
#          = 6 + (6 + (6 + (6 + mul(6,0))))
#          = 6 + (6 + (6 + (6 + 0)))
#          = 6 + 6 + 6 + 6 = 24

def recursive_mul(a, b):
    if b == 0:              # anchor step (base case)
        return 0
    else:
        return a + recursive_mul(a, b - 1)   # recursive step

print(recursive_mul(6, 4))   # 24

# Time: O(b) — b recursive calls
# Space: O(b) — b frames on the stack


# =============================================================================
# SECTION 6: Sum of First N Natural Numbers
# =============================================================================

# sum(n) = 1 + 2 + 3 + ... + n
# sum(1) = 1                        (base case)
# sum(n) = n + sum(n - 1)           (recursive case)
#
# Think: "The sum of 1 to n is n plus the sum of 1 to n-1"

def recursive_sum(n):
    if n == 1:              # BASE CASE
        return 1
    return n + recursive_sum(n - 1)   # RECURSIVE CASE

print(recursive_sum(5))   # 15

# ----- Trace -----
# recursive_sum(5) = 5 + recursive_sum(4)
#                  = 5 + (4 + recursive_sum(3))
#                  = 5 + (4 + (3 + recursive_sum(2)))
#                  = 5 + (4 + (3 + (2 + recursive_sum(1))))
#                  = 5 + (4 + (3 + (2 + 1)))
#                  = 5 + 4 + 3 + 2 + 1 = 15

# Time: O(n), Space: O(n) — same reasoning as factorial
# Note: This can also be done in O(1) with the formula n*(n+1)/2


# =============================================================================
# SECTION 7: Power Function (a^n)
# =============================================================================

# a^n = a * a * a * ... * a   (n times)
# a^0 = 1                     (base case: anything to the power 0 is 1)
# a^n = a * a^(n-1)           (recursive case)

def power(a, n):
    if n == 0:              # BASE CASE
        return 1
    return a * power(a, n - 1)   # RECURSIVE CASE

print(power(2, 10))   # 1024

# ----- Trace: power(2, 4) -----
# power(2,4) = 2 * power(2,3)
#            = 2 * (2 * power(2,2))
#            = 2 * (2 * (2 * power(2,1)))
#            = 2 * (2 * (2 * (2 * power(2,0))))
#            = 2 * (2 * (2 * (2 * 1)))
#            = 2 * 2 * 2 * 2 = 16

# Time: O(n), Space: O(n)
#
# There's a FASTER version using "fast exponentiation":
#   a^n = (a^(n/2))^2       if n is even
#   a^n = a * (a^(n/2))^2   if n is odd
# This is O(log n) — halving n each step! (similar idea to binary search)


# =============================================================================
# SECTION 8: Sum of Digits
# =============================================================================

# Sum the digits of a number: 1234 → 1 + 2 + 3 + 4 = 10
#
# sum_digits(n) when n < 10: return n                          (base case)
# sum_digits(n):             return (n % 10) + sum_digits(n // 10)  (recursive case)
#
# n % 10  → extracts the LAST digit
# n // 10 → removes the LAST digit

def sum_digits(n):
    if n < 10:              # BASE CASE: single digit number
        return n
    return (n % 10) + sum_digits(n // 10)   # RECURSIVE CASE

print(sum_digits(1234))   # 10

# ----- Trace: sum_digits(1234) -----
# sum_digits(1234) = (1234 % 10) + sum_digits(1234 // 10)
#                  = 4 + sum_digits(123)
#                  = 4 + (3 + sum_digits(12))
#                  = 4 + (3 + (2 + sum_digits(1)))
#                  = 4 + (3 + (2 + 1))       ← base case: 1 < 10
#                  = 4 + 3 + 2 + 1 = 10

# Time: O(d) where d = number of digits = O(log n)
# Space: O(d) = O(log n) stack frames


# =============================================================================
# SECTION 9: String Reversal
# =============================================================================

# Reverse a string: "hello" → "olleh"
#
# reverse("") = ""                              (base case: empty string)
# reverse(s) = reverse(s[1:]) + s[0]            (recursive case)
#
# Idea: take the first character, put it at the END of the reversed rest.

def reverse_string(s):
    if len(s) <= 1:         # BASE CASE: empty or single character
        return s
    return reverse_string(s[1:]) + s[0]   # RECURSIVE CASE

print(reverse_string("hello"))   # "olleh"

# ----- Trace: reverse_string("hello") -----
# reverse_string("hello") = reverse_string("ello") + "h"
#                          = (reverse_string("llo") + "e") + "h"
#                          = ((reverse_string("lo") + "l") + "e") + "h"
#                          = (((reverse_string("o") + "l") + "l") + "e") + "h"
#                          = ((("o" + "l") + "l") + "e") + "h"     ← base case
#                          = "ol" + "l" + "e" + "h"
#                          = "olleh"

# Time: O(n^2) — n calls, but s[1:] creates a new string each time
# Space: O(n^2) — each call creates a new string slice + stack frame
# Note: the iterative version s[::-1] is O(n) — much better for strings!


# =============================================================================
# SECTION 10: Fibonacci (Why Naive Recursion Can Be SLOW)
# =============================================================================

# Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
# fib(0) = 0
# fib(1) = 1
# fib(n) = fib(n-1) + fib(n-2)     (TWO recursive calls!)

def fib(n):
    if n == 0:              # BASE CASE
        return 0
    if n == 1:              # BASE CASE
        return 1
    return fib(n - 1) + fib(n - 2)   # RECURSIVE CASE

print(fib(7))   # 13

# ----- The problem: REPEATED WORK -----
# Let's draw the recursion tree for fib(5):
#
#                          fib(5)
#                        /        \
#                   fib(4)        fib(3)
#                  /      \       /     \
#             fib(3)    fib(2)  fib(2)  fib(1)
#            /    \     /   \    /   \
#        fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
#        /   \
#    fib(1) fib(0)
#
# Notice: fib(3) is computed TWICE, fib(2) is computed THREE times!
# As n grows, the redundancy explodes.
#
# Total calls for fib(n) ≈ 2^n (each call branches into 2)
#
# Time:  O(2^n) — EXPONENTIAL! fib(50) would take billions of calls
# Space: O(n)   — max DEPTH of the tree is n (stack never has more than n frames)
#
# ----- Why is space O(n) when there are 2^n calls? -----
# Python doesn't run both branches at the same time.
# It finishes the ENTIRE left branch before starting the right branch.
# So the stack only holds one path from root to leaf at a time → depth = n.

# ----- How to fix it: Memoization -----
# Store results we've already computed so we don't recompute them.
#
# ----- Same tree, but with memoization -- repeated subtrees get PRUNED -----
#
#                          fib(5)
#                        /        \
#                   fib(4)        fib(3) <-- already in memo! O(1) lookup, no recursion
#                  /      \
#             fib(3)    fib(2)
#            /    \     /   \
#        fib(2) fib(1) [memo] [memo]
#        /   \
#    fib(1) fib(0)
#
# Once fib(3) and fib(2) are computed once (left side), every later request
# for them is a dictionary lookup instead of a re-expanded subtree.
# This is exactly why time drops from O(2^n) to O(n): each distinct fib(k)
# is expanded into the tree AT MOST ONCE.

def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

print(fib_memo(50))   # 12586269025  (instant! without memo this would take forever)

# With memoization:
# Time:  O(n) — each fib(k) is computed only ONCE, then looked up in O(1)
# Space: O(n) — the memo dict + the call stack

# ----- Iterative Fibonacci (best for this problem) -----

def fib_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Time: O(n), Space: O(1) — no call stack, no memo dict


# =============================================================================
# SECTION 11: Practice — Tracing a Tricky Recursive Function
# =============================================================================

# From the practice notebook: trace this function call.

def foo(n, r):
    if n == 0:
        return 1
    elif n % 2 == 0:
        return n + foo(n // 2, r)
    else:
        return n - foo(n // 3, r)

# ----- Trace: foo(20, 4) -----
# (Note: r is passed but never affects the logic — it's unused)
#
# foo(20, 4):  20 is even → return 20 + foo(10, 4)
#   foo(10, 4):  10 is even → return 10 + foo(5, 4)
#     foo(5, 4):   5 is odd  → return 5 - foo(1, 4)
#       foo(1, 4):   1 is odd  → return 1 - foo(0, 4)
#         foo(0, 4):   n == 0  → return 1           ← BASE CASE
#       foo(1, 4) = 1 - 1 = 0
#     foo(5, 4) = 5 - 0 = 5
#   foo(10, 4) = 10 + 5 = 15
# foo(20, 4) = 20 + 15 = 35

print(foo(20, 4))   # 35

# ----- How to trace ANY recursive function -----
# 1. Start with the outermost call
# 2. Check: does it hit a base case? If not, figure out which recursive call it makes
# 3. Indent and trace that call
# 4. Keep going deeper until you hit a base case
# 5. Then "unwind" — substitute return values back up level by level


# =============================================================================
# SECTION 12: How to THINK About Recursion (The "Leap of Faith")
# =============================================================================

# The hardest part of recursion is TRUSTING it. Here's the trick:
#
# ----- The Leap of Faith -----
# 1. ASSUME the recursive call works correctly for a smaller input.
#    (Don't trace it in your head — just trust it.)
# 2. Ask: "If I had the answer for the smaller problem, how would I
#    use it to solve the current problem?"
# 3. Make sure the base case is correct.
#
# ----- Example: Factorial -----
# I want factorial(5).
# LEAP OF FAITH: Assume factorial(4) gives me 24 (the correct answer).
# Then factorial(5) = 5 * factorial(4) = 5 * 24 = 120. Done!
# I didn't need to trace factorial(4) → factorial(3) → ... to believe this.
#
# ----- Example: Sum of digits -----
# I want sum_digits(1234).
# LEAP OF FAITH: Assume sum_digits(123) gives me 6 (correct: 1+2+3).
# Then sum_digits(1234) = (1234 % 10) + sum_digits(123) = 4 + 6 = 10. Done!
#
# ----- The Template for Writing Any Recursive Function -----
#
# Step 1: What is the SIMPLEST input? → That's your base case.
#         factorial(0) = 1,  fib(0) = 0,  empty string = ""
#
# Step 2: How does the CURRENT problem relate to a SMALLER version?
#         factorial(n) = n * factorial(n-1)
#         sum(list) = list[0] + sum(list[1:])
#
# Step 3: Trust that the recursive call works. Combine its result.
#
# That's it. Three steps. The rest is practice.


# =============================================================================
# SECTION 13: Recursion vs Iteration — When to Use Which
# =============================================================================

# ----- Side-by-side: Factorial -----
#
# Recursive:                        Iterative:
# def fact(n):                      def fact(n):
#     if n == 0: return 1               result = 1
#     return n * fact(n-1)              for i in range(1, n+1):
#                                           result *= i
#                                       return result
#
# ----- Side-by-side: Fibonacci -----
#
# Recursive (naive):                Iterative:
# def fib(n):                       def fib(n):
#     if n <= 1: return n                a, b = 0, 1
#     return fib(n-1)+fib(n-2)          for _ in range(n):
#                                            a, b = b, a+b
#                                        return a
#
# ----- When to use ITERATION -----
# - Simple counting, accumulation (sum, factorial, max/min)
# - When you need O(1) space
# - When performance matters and the recursive version has repeated work
#
# ----- When to use RECURSION -----
# - Tree/graph traversal (recursion is MUCH cleaner)
# - Divide and conquer (merge sort, quicksort, binary search)
# - Backtracking (sudoku solver, N-queens, maze solving)
# - When the problem is naturally defined recursively
# - Dynamic programming (recursion + memoization)
#
# ----- The Stack Overflow Risk -----
# Python has a default recursion limit of ~1000 calls.
# If your recursion goes deeper than that, Python raises:
#   RecursionError: maximum recursion depth exceeded
#
# You can increase it with:
#   import sys
#   sys.setrecursionlimit(10000)
#
# But if you need 10,000+ levels, use iteration instead.


# =============================================================================
# SECTION 14: Complexity of Recursive Functions — How to Derive It
# =============================================================================

# ----- Step 1: Draw the recursion tree -----
# Each node is a function call. Children are the recursive calls it makes.
#
# ----- Step 2: Count the total number of nodes -----
# That's the number of function calls = time complexity.
#
# ----- Step 3: Find the maximum depth -----
# That's the space complexity (max stack frames at any point).
#
# ----- Common patterns -----
#
# | Pattern                  | Calls per level | Depth | Time     | Space  |
# |--------------------------|-----------------|-------|----------|--------|
# | f(n) = f(n-1)            | 1               | n     | O(n)     | O(n)   |
# | f(n) = f(n-1) + f(n-2)   | 2               | n     | O(2^n)   | O(n)   |
# | f(n) = f(n/2)            | 1               | log n | O(log n) | O(log n)|
# | f(n) = 2*f(n/2)          | 2               | log n | O(n)     | O(log n)|
#
# ----- Why is recursive Fibonacci O(2^n) time but O(n) space? -----
# The TREE has ~2^n nodes (calls), but the STACK at any moment only holds
# the calls along ONE PATH from root to leaf — which is at most n deep.
# Python runs the left branch fully before starting the right branch.
#
# ----- Why does memoization fix Fibonacci? -----
# Without memo: fib(50) makes ~2^50 ≈ 10^15 calls
# With memo:    fib(50) makes ~99 calls
# Each fib(k) is computed once → O(1) lookup after that → O(n) total.


# =============================================================================
# SECTION 15: More Practice Problems
# =============================================================================

# ----- Check if a string is a palindrome -----

def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])

print(is_palindrome("racecar"))   # True
print(is_palindrome("hello"))     # False

# Trace: is_palindrome("racecar")
# s[0]='r', s[-1]='r' → match → is_palindrome("aceca")
# s[0]='a', s[-1]='a' → match → is_palindrome("cec")
# s[0]='c', s[-1]='c' → match → is_palindrome("e")
# len("e") <= 1 → True


# ----- Count occurrences of a character in a string -----

def count_char(s, ch):
    if len(s) == 0:
        return 0
    match = 1 if s[0] == ch else 0
    return match + count_char(s[1:], ch)

print(count_char("banana", "a"))   # 3


# ----- Print numbers from n down to 1, then back up to n -----
# This demonstrates: code BEFORE the recursive call runs on the way DOWN,
# code AFTER the recursive call runs on the way BACK UP.

def print_both(n):
    if n == 0:
        return
    print(n)                # runs on the way DOWN (before recursion)
    print_both(n - 1)
    print(n)                # runs on the way BACK UP (after recursion)

print_both(3)
# Output: 3 2 1 1 2 3
#
# Mental model -- the recursive call is the mirror line; code before it
# fires on the way DOWN, code after it fires on the way back UP:
#
#   print(3) -> print(2) -> print(1) -> print_both(0) -> return (base case)
#      |                                                       |
#      '---------------------- unwinding -----------------------'
#                          (back up: print(1) -> print(2) -> print(3))
#   Down pass prints: 3 2 1      Up pass prints: 1 2 3


# ----- Perimeter of a circle (from original lecture) -----

import math

def perimeter_of_circle(radius):
    return 2 * math.pi * radius

print(perimeter_of_circle(5))   # 31.4159...


# =============================================================================
# Summary: The 5 Things to Remember About Recursion
# =============================================================================

# 1. Every recursive function needs a BASE CASE (or it loops forever).
#
# 2. Each recursive call must move TOWARD the base case
#    (smaller n, shorter string, simpler problem).
#
# 3. The call stack stores each function call as a frame (activation record).
#    Going down = pushing frames. Returning = popping frames.
#
# 4. Use the LEAP OF FAITH: trust the recursive call works for
#    smaller input. Focus on how to combine its result.
#
# 5. Recursion uses O(depth) extra space for the call stack.
#    If you see repeated work (like Fibonacci), use memoization.
