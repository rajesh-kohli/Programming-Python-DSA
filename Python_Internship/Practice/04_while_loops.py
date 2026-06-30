# =============================================================================
# SECTION 1: Introduction -- Iterative vs Recursive Problem Solving
# =============================================================================
#
## Problem Solving:
#Task: Repetitive problem statement
## Two ways to solve it:
# 1. Iterative Approach 2. Recursive Approach
### Task:
# 5 houses and 5 gifts - Santa has to give one gift to each house
# Approach 1: Santa takes the gift and delivers it to each house individually one by one (Repeat 5 times)
#       --> Conventional --> Iterative --> performed with Loops
# Approach 2: Old Santa hires a manager who then hires 5 different people to deliver at each house
##  Here think of Manager as a function, and we then call the function 5 times with different parameters
### This is called Recursive approach - where we are calling the same function itself again and again
#
# WHEN TO USE WHICH:
#   Iterative: Simpler, uses less memory (no function call stack overhead).
#              Preferred when the problem is naturally sequential.
#   Recursive: Elegant for problems that break into smaller sub-problems
#              (trees, divide-and-conquer, backtracking).
#              Warning: can cause stack overflow for deep recursion.
# =============================================================================


# =============================================================================
# SECTION 2: While Loop Fundamentals
# =============================================================================
#
## Iterative approach: Loop
#### Three components of every loop:
#   1. INITIALIZATION --> from where we need to start (set the counter)
#   2. CONDITION      --> upto where we need to go (when to stop)
#   3. UPDATION       --> no of steps we need to take (how to move forward)
#
## Two kinds of loops in Python: For and While
#
# While loop:
# Syntax:
#     initialization
#     while condition:        # checked BEFORE each iteration
#         statements
#         updation            # MUST update, or you get an infinite loop!
#
# HOW IT WORKS:
#   1. Check condition --> if False, skip the loop entirely
#   2. Execute the body
#   3. Go back to step 1
#
# COMMON MISTAKES:
#   - Forgetting the updation step (infinite loop!)
#   - Off-by-one errors (using < instead of <=, or starting at 0 vs 1)
#   - In nested loops: forgetting to RESET the inner loop variable
#
# WHILE LOOP FLOW DIAGRAM:
#
#        +-------------------+
#        |  initialization   |   (runs once)
#        +-------------------+
#                  |
#                  v
#        +-------------------+
#   +--->|   check condition |
#   |    +-------------------+
#   |        |True      |False
#   |        v           v
#   |  +-----------+   (exit loop,
#   |  |   body    |    continue after)
#   |  +-----------+
#   |        |
#   |  +-----------+
#   |  | updation  |
#   |  +-----------+
#   |        |
#   +--------+
#
# TRACE TABLE for "i=1; while i<=10: print(i); i+=1" (first few iterations):
#
#   iteration | i (before body) | condition i<=10 | action
#   ----------|-----------------|------------------|----------------
#       1     |        1        |       True       | print 1, i->2
#       2     |        2        |       True       | print 2, i->3
#       3     |        3        |       True       | print 3, i->4
#      ...    |       ...       |        ...       | ...
#      11     |       11        |       False      | loop exits
# =============================================================================


# =============================================================================
# SECTION 3: Basic While Loop Examples
# =============================================================================

# ---- Example 1: Print numbers 1 to 10 ----
# Demonstrates the three components: initialization, condition, updation.
# TIME COMPLEXITY: O(n) where n = 10
print("Example 1")
# initialization
i = 1
# condition
while i <= 10:
    print(i)
    # updation
    i += 1
# Expected Output: 1 2 3 4 5 6 7 8 9 10 (each on a new line)


# ---- Example 2: Commented out -- would be an INFINITE LOOP ----
# If i starts at 10 and you decrement (i -= 1), the condition i <= 10
# is ALWAYS True (10, 9, 8, 7, ... goes on forever).
# This is a common beginner mistake!
print("Example 2")
# i = 10
# while i<=10:
#     print(i)
#     i-=1


# ---- Example 3: Conditional printing inside a loop ----
# For each i from 1 to 10:
#   If i is even: print i
#   If i is odd:  print i+1 (makes it even)
# So the output is always even numbers.
# TIME COMPLEXITY: O(n)
print("Example 3")
i = 1
while i <= 10:
    if i % 2 == 0:
        print(i)
    else:
        print(i + 1)
    i += 1
# Expected Output:
#   i=1 (odd):  print 2
#   i=2 (even): print 2
#   i=3 (odd):  print 4
#   i=4 (even): print 4
#   i=5 (odd):  print 6
#   i=6 (even): print 6
#   i=7 (odd):  print 8
#   i=8 (even): print 8
#   i=9 (odd):  print 10
#   i=10 (even): print 10


# ---- Example 4: Bitwise operators inside a loop ----
# i goes from 1 to 10 stepping by 2 (so i = 1, 3, 5, 7, 9).
# If i is NOT divisible by 3: print i << 2  (i * 4)
# If i IS divisible by 3:     print i >> 2  (i // 4, integer division)
# TIME COMPLEXITY: O(n)
print("Example 4")
i = 1
while i <= 10:
    if i % 3 != 0:
        print(i << 2)    # i * 4
    else:
        print(i >> 2)    # i // 4
    i += 2
# Expected Output:
#   i=1: 1%3!=0 -> 1<<2 = 4
#   i=3: 3%3==0 -> 3>>2 = 0  (binary 11 >> 2 = 0)
#   i=5: 5%3!=0 -> 5<<2 = 20
#   i=7: 7%3!=0 -> 7<<2 = 28
#   i=9: 9%3==0 -> 9>>2 = 2  (binary 1001 >> 2 = 10 = 2)


# ---- Example 5: Bitwise shifts with step size 3 ----
# i goes from 1 to 15, stepping by 3 (so i = 1, 4, 7, 10, 13).
# If i is even: print (i+1) << 2  -- NOTE: operator precedence!
#   i+1<<2 is parsed as i + (1<<2) = i + 4 due to precedence.
#   But the intent seems to be (i+1)<<2. The code as written does i + 4.
# If i is odd:  print (3*i) << 2  -- same precedence note.
#   3*i<<2 is parsed as (3*i) << 2 since * has higher precedence than <<.
# TIME COMPLEXITY: O(n)
print("Example 5")
i = 1
while i <= 15:
    if i % 2 == 0:
        print(i + 1 << 2)    # Precedence: i + (1 << 2) = i + 4
    else:
        print(3 * i << 2)    # Precedence: (3 * i) << 2 = 3*i * 4 = 12*i
    i += 3
# Expected Output:
#   i=1  (odd):  (3*1)<<2 = 3<<2 = 12
#   i=4  (even): 4 + (1<<2) = 4 + 4 = 8
#   i=7  (odd):  (3*7)<<2 = 21<<2 = 84
#   i=10 (even): 10 + (1<<2) = 10 + 4 = 14
#   i=13 (odd):  (3*13)<<2 = 39<<2 = 156


# ---- Example 6: Nested conditions with bitwise operators ----
# i goes from 1 to 15, stepping by 2 (so i = 1, 3, 5, 7, 9, 11, 13, 15).
# If i is divisible by 3:
#     If i > 3: print (i*2) >> 2   (i*2 divided by 4)
#     If i <= 3: do nothing (no else clause)
# If i is NOT divisible by 3:
#     print (i*2) << 1             (i*2 multiplied by 2 = i*4)
# TIME COMPLEXITY: O(n)
print("Example 6")
i = 1
while i <= 15:
    if i % 3 == 0:
        if i > 3:
            print(i * 2 >> 2)    # (i*2) >> 2 = i*2 // 4
    else:
        print(i * 2 << 1)        # (i*2) << 1 = i*2 * 2 = i*4
    i += 2
# Expected Output:
#   i=1:  1%3!=0  -> (1*2)<<1 = 2<<1 = 4
#   i=3:  3%3==0, but 3>3 is False -> nothing printed
#   i=5:  5%3!=0  -> (5*2)<<1 = 10<<1 = 20
#   i=7:  7%3!=0  -> (7*2)<<1 = 14<<1 = 28
#   i=9:  9%3==0, 9>3 -> (9*2)>>2 = 18>>2 = 4  (binary 10010 >> 2 = 100 = 4)
#   i=11: 11%3!=0 -> (11*2)<<1 = 22<<1 = 44
#   i=13: 13%3!=0 -> (13*2)<<1 = 26<<1 = 52
#   i=15: 15%3==0, 15>3 -> (15*2)>>2 = 30>>2 = 7  (binary 11110 >> 2 = 111 = 7)
# So output: 4, 20, 28, 4, 44, 52, 7


# =============================================================================
# SECTION 4: Nested While Loops
# =============================================================================
#
# A nested loop is a loop inside another loop.
# The INNER loop runs completely for each iteration of the OUTER loop.
#
# TIME COMPLEXITY: Generally O(n * m) where n = outer iterations, m = inner.
#
# CRITICAL CONCEPT -- Inner Loop Variable Reset:
# In a while loop, you MUST reset the inner loop variable at the START of
# each outer loop iteration. Otherwise, the inner loop only runs during the
# FIRST iteration of the outer loop, because the inner variable retains its
# final value from the previous iteration.
#
# This is different from a for loop, where the loop variable is automatically
# reset by the "for j in range(...):" statement.
#
# WHY THE BUG HAPPENS (visual trace, j initialized OUTSIDE the outer loop):
#
#   i=1: inner while j<=5  j:1->2->3->4->5->6  (condition fails, j stays 6)
#   i=2: inner while j<=5  j is already 6 --> condition False IMMEDIATELY
#   i=3: inner while j<=5  j is still 6   --> condition False IMMEDIATELY
#   ...  (inner loop body never runs again for the rest of i's lifetime)
#
#   Fix: put "j = 1" as the FIRST line inside the outer loop's body, so
#   every outer iteration gets a freshly reset inner counter.
# =============================================================================


# ---- Example 7: Nested loop -- CONTAINS A BUG ----
#
# *** BUG: j=1 is initialized BEFORE the outer loop. After the inner loop
# *** runs once (j goes from 1 to 5, ending at j=6), j is NEVER reset.
# *** On all subsequent iterations of i (i=2,3,...,10), the inner while j<=5
# *** is immediately False (since j=6), so the inner loop NEVER runs again.
# ***
# *** RESULT: Only prints i+j for i=1, j=1..5, then nothing for i=2..10.
# ***
# *** FIX: Move "j = 1" INSIDE the outer loop, right after "while i<=10:".
#
# Buggy version (original code):
#4,12,20
#Example
print("Example 7")
i = 1
j = 1               # BUG: j is only initialized once!
while i <= 10:
    while j <= 5:    # After first pass, j=6, so this never runs again
        print(i + j)
        j += 1
    i += 1
# ACTUAL Output (due to bug):
#   Only runs inner loop for i=1: prints 2, 3, 4, 5, 6
#   Then i goes from 2 to 10 with NO inner loop output.
#
# FIXED version would be:
#   i = 1
#   while i <= 10:
#       j = 1            # <-- RESET j here!
#       while j <= 5:
#           print(i + j)
#           j += 1
#       i += 1
# FIXED Expected Output (if bug were fixed):
#   i=1: 2,3,4,5,6  |  i=2: 3,4,5,6,7  |  ...  |  i=10: 11,12,13,14,15


# ---- Example 8: Nested loop with bitwise operators -- SAME BUG ----
#
# *** BUG: Same issue as Example 7. j=1 is initialized BEFORE the outer loop.
# *** After the inner loop runs once (j goes from 1 to 10, ending at j=11),
# *** j is NEVER reset. The inner loop only executes during the first
# *** iteration of i.
# ***
# *** FIX: Move "j = 1" INSIDE the outer loop, right after "while i<=20:".
#
print("Example 8")
i = 1
j = 1               # BUG: j is only initialized once!
while i <= 20:
    while j <= 10:   # After first pass, j=11, so this never runs again
        if (i + j) % 2 == 0:
            print((i + j) >> 2)    # (i+j) // 4
        else:
            print((i + j) << 2)    # (i+j) * 4
        j += 1
    i += 2
# ACTUAL Output (due to bug):
#   Only runs inner loop for i=1:
#   j=1: (1+1)=2, even -> 2>>2 = 0
#   j=2: (1+2)=3, odd  -> 3<<2 = 12
#   j=3: (1+3)=4, even -> 4>>2 = 1
#   j=4: (1+4)=5, odd  -> 5<<2 = 20
#   j=5: (1+5)=6, even -> 6>>2 = 1
#   j=6: (1+6)=7, odd  -> 7<<2 = 28
#   j=7: (1+7)=8, even -> 8>>2 = 2
#   j=8: (1+8)=9, odd  -> 9<<2 = 36
#   j=9: (1+9)=10, even -> 10>>2 = 2
#   j=10: (1+10)=11, odd -> 11<<2 = 44
#   Then i goes 3,5,7,...,19 but inner loop never runs (j=11).
#
# FIXED version would be:
#   i = 1
#   while i <= 20:
#       j = 1            # <-- RESET j here!
#       while j <= 10:
#           if (i + j) % 2 == 0:
#               print((i + j) >> 2)
#           else:
#               print((i + j) << 2)
#           j += 1
#       i += 2


# ---- Example 9: Nested loop -- DIFFERENT BUG ----
#
# *** BUG: j is initialized INSIDE the inner loop body (after the condition
# *** check), so on the first iteration j still holds its value from
# *** Example 8 (j=11). The inner while j<=10 is immediately False, so
# *** the j=1 reset line is NEVER reached. This is an unreachable code bug.
# ***
# *** Additionally, even if j were reset before the inner while, the "j = 1"
# *** inside the loop body would reset j to 1 on every iteration, causing
# *** an INFINITE LOOP (j would go 1 -> 1 -> 1 forever).
# ***
# *** FIX: Move "j = 1" to BEFORE the inner while loop (inside the outer
# *** loop), and remove it from inside the inner loop body:
# ***
# ***   while i <= 20:
# ***       j = 1              # <-- Initialize here
# ***       while j <= 10:
# ***           if (i+j) % 2 == 0:
# ***               print((i+j) >> 2)
# ***           else:
# ***               print((i+j) << 2)
# ***           j += 1
# ***       i += 2
# ***       print(i)
#
print("Example 9")
i = 1

while i <= 20:
    while j <= 10:    # j=11 from Example 8, so this never executes
        j = 1         # BUG: This line is unreachable AND would cause
                      #       an infinite loop if it were reached
        if (i + j) % 2 == 0:
            print((i + j) >> 2)
        else:
            print((i + j) << 2)
        j += 1
    i += 2
    print(i)
# ACTUAL Output (due to bug):
#   Inner loop never runs (j=11 from Example 8).
#   Only prints i after each outer iteration: 3, 5, 7, 9, 11, 13, 15, 17, 19, 21


# =============================================================================
# SECTION 5: Key Takeaways
# =============================================================================
#
# 1. ALWAYS RESET INNER LOOP VARIABLES:
#    In nested while loops, initialize the inner variable INSIDE the outer
#    loop, BEFORE the inner while statement. This is the #1 nested loop bug.
#
#    WRONG:                          RIGHT:
#    j = 1                           while i <= n:
#    while i <= n:                       j = 1           # <-- reset here!
#        while j <= m:                   while j <= m:
#            ...                             ...
#            j += 1                          j += 1
#        i += 1                          i += 1
#
# 2. THREE COMPONENTS: Every loop needs initialization, condition, updation.
#    Missing any one leads to bugs (infinite loops, off-by-one errors, etc.)
#
# 3. BITWISE IN LOOPS:
#    << and >> are fast alternatives to multiplication/division by powers of 2.
#    Be careful with OPERATOR PRECEDENCE:
#      i + 1 << 2  is  i + (1 << 2)  = i + 4     (NOT (i+1) << 2)
#      3 * i << 2  is  (3 * i) << 2  = 12 * i    (* has higher precedence)
#
# 4. FOR vs WHILE:
#    - for loops auto-manage the loop variable (no reset bug possible)
#    - while loops give more control but require manual management
#    - Use for when you know the number of iterations
#    - Use while when the termination depends on a condition
# =============================================================================
