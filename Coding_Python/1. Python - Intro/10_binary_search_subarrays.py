###############################################################################
#                    Lecture 12 - Arrays: Binary Search & More                #
###############################################################################


# =============================================================================
# SECTION 1: Binary Search - O(log n)
# =============================================================================

## Binary Search - O(log n) - if the array is sorted

# where as Linear search is O(n)

# ----- Why Binary Search is faster than Linear Search -----
# Linear Search: checks every element one by one --> O(n)
# Binary Search: eliminates HALF the search space each step --> O(log n)
#
# Example: In an array of 1,000,000 elements:
#   - Linear Search: up to 1,000,000 comparisons
#   - Binary Search: at most ~20 comparisons (log2(1,000,000) ≈ 20)


# ----- Prerequisite: Monotonic Functions -----

# Monotonic functions:
# As value of x increase or decrease, they increase or decrease accordingly
# Monotonically non-increasing function --> increases first and then gets constant
# Monotonically non-decreasing function -->  decreases first and then gets constant
# the direction of monotonic functions will be only one

# if the array is sorted, we can say that is an example of monotonic function
# if sorted in increasing order, it would be monotonically increasing
# and vice versa

## Binary search works as long as the search space is monotonic


# ----- How does the algorithm work? (Step by step) -----

## How does this algorithm work?

# First define a bound space - meaning in case of an array of size n, the answer would lie within 0 to n-1
# lower bound (also notated with lo or s) is index 0
# higher bound (also notated with hi or e) is index n-1
# the bounds are included as well

# after the bounds are defined
# then find the mid point
# if target == mid, condition  = true, then stop, since t is found at index mid
# If condition is false, then target would be right or left of mid
# if target > arr[mid] --> go to right --> reduce your search space to [mid + 1, hi]
# if target < arr[mid] --> go to left --> reduce your search space to [lo, mid -1]
# now do a bineary search again in the new search space
# We keep repeating this process until lo <= hi and in the end there is only 1 element left when lo = hi

# ----- Visual Walkthrough -----
#
# arr = [10, 20, 30, 40, 50, 60, 70],  target = 50
#
# Step 1:  lo=0, hi=6  --> mid=3  --> arr[3]=40 < 50  --> go RIGHT  --> lo=4
# Step 2:  lo=4, hi=6  --> mid=5  --> arr[5]=60 > 50  --> go LEFT   --> hi=4
# Step 3:  lo=4, hi=4  --> mid=4  --> arr[4]=50 == 50 --> FOUND at index 4
#
# ----- The classic "narrowing range" picture -----
# Each step, lo and hi close in on each other, eliminating HALF the
# remaining elements (the side mid is NOT on):
#
#   idx:    0   1   2   3   4   5   6
#   arr:  [10, 20, 30, 40, 50, 60, 70]
#          lo              hi              mid=3 -> 40<50, eliminate [0..3]
#                          mid
#
#                       lo      hi          mid=5 -> 60>50, eliminate [5..6]
#                       mid
#
#                       lo,hi               mid=4 -> 50==50, FOUND!
#                       mid
#
#   Search space: 7 -> 3 -> 1 elements (roughly halved each step) -> O(log n)


def binary_search(arr: list[int], n: int, t: int) -> int:
    lo, hi = 0, n-1
    while lo <= hi:
        mid = (lo + hi) // 2  # remember integer division, not floating division because indices are integer values
        if arr[mid] == t:
            # t is found at index mid
            return mid
        elif t > arr[mid]:
            lo = mid + 1
        else:
            # t < arr[mid]
            hi = mid -1

    #t is not present in arr[]
    return -1


n, t = map(int, input().split()) # number of elements 7 , target value 100
arr = list(map (int, input().split())) # [10, 20, 30, 40, 50, 60, 70]
print(binary_search(arr, n, t))

## number of iterations are = k + 1
# time complexity of binary search  = O(logn) (Explanation in the video)
# Best case for this is constant and worse case is O(logn)

# ----- Why O(log n)? (Deriving it, not just memorizing it) -----
#
# Ask: "How many times can I halve n before I reach 1?"
#
# Each iteration cuts the search space in half:
#   n --> n/2 --> n/4 --> n/8 --> ... --> 1
# After k steps: n / 2^k = 1  -->  2^k = n  -->  k = log2(n)
#
# That's it. Whenever you see "cut in half each step", it's O(log n).
#
# ----- How to RECOGNIZE O(log n) in code -----
# Look for:  lo, hi pointers that move TOWARD each other by halving
#            or a variable that doubles/halves each iteration (i *= 2 or i //= 2)
# These are the hallmarks of logarithmic time.
#
# ----- Space: O(1) -----
# We only use a fixed number of variables (lo, hi, mid) regardless of array size.
# We don't create any new arrays or lists. The input array already exists —
# space complexity only counts EXTRA memory the algorithm uses.


# =============================================================================
# SECTION 2: First Occurrence in Sorted Array
# =============================================================================

## First Occurence in Sorted Array

# ----- Problem -----
# Given a sorted array with duplicates, find the FIRST (leftmost) index of target.
# Regular binary search stops at ANY match - we need the EARLIEST one.
#
# ----- Key Idea -----
# When we find arr[mid] == t, DON'T stop! Instead:
#   1. Save mid as a potential answer (ans = mid)
#   2. Keep searching LEFT (hi = mid - 1) to see if there's an earlier occurrence
#   3. Return ans after the loop ends (not mid immediately!)
#
# ----- Example -----
# arr = [10, 20, 30, 30, 30, 30, 30, 40, 50],  target = 30
#
# Step 1:  lo=0, hi=8  --> mid=4  --> arr[4]=30 == 30  --> ans=4, search LEFT --> hi=3
# Step 2:  lo=0, hi=3  --> mid=1  --> arr[1]=20 < 30   --> search RIGHT       --> lo=2
# Step 3:  lo=2, hi=3  --> mid=2  --> arr[2]=30 == 30  --> ans=2, search LEFT --> hi=1
# Step 4:  lo=2, hi=1  --> lo > hi, STOP
# Answer: ans = 2 (the first occurrence of 30)
#
# ----- Visual: even on a match, we keep shrinking hi to hunt LEFT -----
#   idx: 0   1   2   3   4   5   6   7   8
#   arr:[10, 20, 30, 30, 30, 30, 30, 40, 50]
#        lo                  hi              mid=4 -> match! ans=4, hi=3 (look left)
#        lo      hi                          mid=1 -> 20<30, lo=2 (look right)
#            lo  hi                          mid=2 -> match! ans=2, hi=1 (look left)
#            hi  lo                          lo>hi, STOP -> ans=2 is the LEFTMOST 30

def first_occ(arr: list[int], n: int, t: int) -> int:
    lo, hi = 0, n-1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == t:
            ans = mid
            hi = mid - 1       # keep searching LEFT for an earlier occurrence
        elif t > arr[mid]:
            lo = mid + 1
        else:
            hi = mid -1

    return ans


# ----- Why is this still O(log n) and not slower? -----
# You might think: "we don't stop when we find the target, so doesn't it take longer?"
# No! The loop still halves the search space every iteration (either hi = mid-1 or lo = mid+1).
# The number of iterations is still at most log2(n), same as regular binary search.
# The only difference is: instead of returning immediately on a match, we record it and keep going.
# But "keep going" still means halving — so the total number of steps doesn't change.
#
# Time:  O(log n) — same halving logic as binary search
# Space: O(1)     — just lo, hi, mid, ans

print(first_occ(arr, n, t))


# =============================================================================
# SECTION 3: Last Occurrence in Sorted Array
# =============================================================================

## Last Occurence in Sorted Array

# ----- Key Difference from first_occ -----
# When we find arr[mid] == t:
#   - first_occ searches LEFT  (hi = mid - 1)  --> finds earliest match
#   - last_occ  searches RIGHT (lo = mid + 1)  --> finds latest match
#
# Everything else stays the same!
#
# ----- Example -----
# arr = [10, 20, 30, 30, 30, 30, 30, 40, 50],  target = 30
#
# Step 1:  lo=0, hi=8  --> mid=4  --> arr[4]=30 == 30  --> ans=4, search RIGHT --> lo=5
# Step 2:  lo=5, hi=8  --> mid=6  --> arr[6]=30 == 30  --> ans=6, search RIGHT --> lo=7
# Step 3:  lo=7, hi=8  --> mid=7  --> arr[7]=40 > 30   --> search LEFT         --> hi=6
# Step 4:  lo=7, hi=6  --> lo > hi, STOP
# Answer: ans = 6 (the last occurrence of 30)

def last_occ(arr: list[int], n: int, t: int) -> int:
    lo, hi = 0, n-1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == t:
            ans = mid
            lo = mid + 1        # search right for later occurence
        elif t > arr[mid]:
            lo = mid + 1
        else:
            hi = mid -1

    return ans

print(last_occ(arr, n, t))

# always O(logn)

# ----- Summary: first_occ vs last_occ vs binary_search -----
#
# | Function      | When arr[mid] == t      | Returns             |
# |---------------|-------------------------|---------------------|
# | binary_search | return mid (stop)       | ANY matching index  |
# | first_occ     | ans=mid, hi = mid - 1   | FIRST matching idx  |
# | last_occ      | ans=mid, lo = mid + 1   | LAST matching idx   |


# =============================================================================
# SECTION 4: Count Occurrences in Sorted Array
# =============================================================================

## Count Occurences in Sorted Array

# ----- Key Idea -----
# Since the array is sorted, all occurrences of target are CONTIGUOUS (next to each other).
# So: count = last_index - first_index + 1
#
# ----- Example -----
# arr = [10, 20, 30, 30, 30, 30, 30, 40, 50],  target = 30
# first_occ = 2, last_occ = 6
# count = 6 - 2 + 1 = 5    (indices 2, 3, 4, 5, 6 --> five 30s)
#
# If target is not found, first_occ returns -1, so we return 0.

def count_occ(arr: list[int], n: int, t: int) -> int:
    first = first_occ(arr, n, t)
    if first == -1:
        return 0
    last = last_occ(arr, n, t)
    return last - first + 1

print(count_occ(arr, n, t))

# O(logn) - two binary searches, each O(logn)
# O(logn) + O(logn) = O(2 * logn) = O(logn)  (constants are dropped in Big-O)


# =============================================================================
# SECTION 5: Python's bisect Module (Built-in Binary Search)
# =============================================================================

## There is a module (collection of functions) in Python called - bisect

# Python provides a built-in module called 'bisect' that implements binary search
# so you don't have to write it yourself every time.

# ----- bisect_left -----

# there is an interesting function in bisect module called bisect_left

arr = [10, 20, 30, 30, 30, 30, 30, 40, 50]
t = 30

import bisect
print(bisect.bisect_left(arr, t)) ## does the same thing as what first_occ function did
# takes same time as O(logn)
# o/p = 2 (first index where 30 appears)

# whatif the element doesn't exist

crr = [100, 200, 300, 400, 500]
t = 250
print(bisect.bisect_left(crr, t))
# o/p = 2
## this will give the first index where the value is greater than equal to target
## or think of index position where if this value was present, what index position would this go

# bisect_left(arr, t) returns the 1st position where the value is >= t

drr = [1000, 2000, 3000]
t = 50
print(bisect.bisect_left(drr, t))
# o/p = 0

# if the target is smaller than all the elements in the array, you get 0
# if the target is greater than all the elements in the array, you get the length of the array

err = [100, 200, 300]
t = 500
print(bisect.bisect_left(err, t))
# o/p = 3

# ----- bisect_right -----

### bisect_right function - this tells you the first index where the value is > t

# ----- bisect_left vs bisect_right -----
#
# bisect_left(arr, t)  --> first index where value is >= t  (left side of duplicates)
# bisect_right(arr, t) --> first index where value is >  t  (right side of duplicates)
#
# For arr = [10, 20, 30, 30, 30, 30, 30, 40, 50], t = 30:
#                       ^                    ^
#              bisect_left = 2        bisect_right = 7
#
# Notice: bisect_right - bisect_left = count of target in array (7 - 2 = 5 thirties)

print(bisect.bisect_right(arr, t))
# o/p = 7
print(bisect.bisect_right(crr, t))
# o/p = 2
print(bisect.bisect_right(drr, t))
# o/p = 0
print(bisect.bisect_right(err, t))
# o/p = 3 # you just get the length again because the number doesn't exist

# ----- Importing bisect (different ways) -----

# simpler way so you don't have to write bisect every time

import bisect as bi

# bi.bisect_left

from bisect import * ## with this you just directly call bisect_left or any function inside the module, the way you write your own functions.
# chances of repeating your own functions with same name is higher, so this is not a good practice

# bisect_right(drr, t)


# =============================================================================
# SECTION 6: Generate Sub-Arrays
# =============================================================================

### Generate Sub-Arrays

# ----- What is a Sub-Array? -----
# A sub-array is a CONTIGUOUS (consecutive) portion of an array.
# It must maintain the original order and cannot skip elements.
#
# For arr = [1, 2, 3]:
#   Sub-arrays: [1], [1,2], [1,2,3], [2], [2,3], [3]
#   NOT a sub-array: [1, 3] (skips 2 - this would be a subsequence)
#   NOT a sub-array: [3, 1] (wrong order - this would be a permutation)

# think of sub-array as all slices of an array - starting from all index positions all the way to end

# ----- Approach -----
# Use two loops:
#   i = starting index (0 to n-1)
#   j = ending index   (i to n-1)  --> j starts from i because a sub-array can be a single element
#
# For arr = [1, 2, 3]:
#   i=0: j=0 -> [1],  j=1 -> [1,2],  j=2 -> [1,2,3]
#   i=1: j=1 -> [2],  j=2 -> [2,3]
#   i=2: j=2 -> [3]
#
# ----- Visual: i anchors the start, j sweeps right to grow the window -----
#   idx: 0  1  2
#   arr:[1, 2, 3]
#
#   i=0: [1]        i  j
#        [1,2]      i     j
#        [1,2,3]    i        j
#   i=1: [2]           i  j
#        [2,3]         i     j
#   i=2: [3]               i  j

def generate_subarrays(arr: list[int], n: int):
    for i in range(n):
        for j in range(i, n):
            print(arr[i:j+1])

generate_subarrays([1, 2, 3], 3)

n = int(input())
arr = list(map(int, input().split()))
generate_subarrays(arr,n)

# Total number of subarrays = n*(n+1)/2
# For n=3: 3*4/2 = 6 subarrays
# For n=5: 5*6/2 = 15 subarrays
#
# ----- Deriving the time complexity -----
#
# The two loops generate all (i, j) pairs where 0 <= i <= j <= n-1.
#
# Count the inner loop iterations:
#   i=0: j runs from 0 to n-1 --> n iterations
#   i=1: j runs from 1 to n-1 --> n-1 iterations
#   i=2: j runs from 2 to n-1 --> n-2 iterations
#   ...
#   i=n-1: j runs from n-1 to n-1 --> 1 iteration
#
# Total = n + (n-1) + (n-2) + ... + 1 = n*(n+1)/2 = O(n^2)
#
# BUT: inside the inner loop, arr[i:j+1] creates a SLICE, which copies (j-i+1) elements.
# That copy itself takes O(length of subarray) time. In the worst case, the subarray
# is length n, and on average it's about n/3. So the true total work is:
#
#   Sum over all (i,j) of (j - i + 1) = n*(n+1)*(n+2)/6 ≈ O(n^3)
#
# Takeaway: generating all subarrays is O(n^2), but printing/processing them is O(n^3)
# because each subarray has variable length.
#
# Space: O(n) — arr[i:j+1] creates a temporary list of up to n elements each time.
#   If we only printed individual elements (without slicing), it would be O(1) extra space.


# =============================================================================
# SECTION 7: Maximum Subarray Sum (Brute Force)
# =============================================================================

### Maximum Subarray Sum
# Given an array of N integers, design an algorithm to find the maximum subarray sum.

# ----- What is the problem? -----
# Given: an array of integers (can have NEGATIVES)
# Find:  the contiguous subarray whose elements add up to the LARGEST sum
#
# Example:
#   arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
#   Answer: subarray [4, -1, 2, 1] has sum = 6 (the maximum)
#
# ----- Why is this interesting? -----
# If all numbers were positive, the answer would be trivially the entire array.
# Negatives make it tricky: you have to decide where to start and where to stop.
#
# We'll solve this THREE ways, each faster than the last:
#   1. Brute Force:            O(n^3)
#   2. Optimized Brute Force:  O(n^2)
#   3. Prefix Sum approach:    O(n^2) but introduces a powerful concept
#   (Kadane's Algorithm is O(n) — covered in 11_two_pointers_and_kadane.py)


# ----- Approach 1: Brute Force — O(n^3) -----
#
# Try EVERY possible subarray. For each one, compute the sum. Track the maximum.
#
# Three nested loops:
#   i = start index     (picks where the subarray begins)
#   j = end index       (picks where the subarray ends)
#   k = sum loop        (adds up elements from i to j)
#
# ----- Walkthrough -----
# arr = [1, -2, 3, 4]
#
# i=0, j=0: sum([1])          = 1
# i=0, j=1: sum([1,-2])       = -1
# i=0, j=2: sum([1,-2,3])     = 2
# i=0, j=3: sum([1,-2,3,4])   = 6
# i=1, j=1: sum([-2])         = -2
# i=1, j=2: sum([-2,3])       = 1
# i=1, j=3: sum([-2,3,4])     = 5
# i=2, j=2: sum([3])          = 3
# i=2, j=3: sum([3,4])        = 7    <-- MAXIMUM!
# i=3, j=3: sum([4])          = 4
#
# Answer: 7

def max_subarray_sum_brute(arr: list[int], n: int) -> int:
    max_sum = float('-inf')

    for i in range(n):                  # start of subarray
        for j in range(i, n):           # end of subarray
            current_sum = 0
            for k in range(i, j + 1):   # compute sum of arr[i..j]
                current_sum += arr[k]
            max_sum = max(max_sum, current_sum)

    return max_sum

# ----- Deriving the Time Complexity: O(n^3) -----
#
# Let's count the work the INNERMOST loop (k) does across ALL iterations:
#
#   For i=0:
#     j=0: k runs 1 time       (sum of 1 element)
#     j=1: k runs 2 times      (sum of 2 elements)
#     j=2: k runs 3 times      ...
#     j=n-1: k runs n times
#     Total for i=0: 1 + 2 + 3 + ... + n = n*(n+1)/2
#
#   For i=1:
#     Total: 1 + 2 + ... + (n-1) = (n-1)*n/2
#
#   ...and so on until i=n-1 which does just 1 operation.
#
#   Grand total = n*(n+1)/2 + (n-1)*n/2 + ... + 1
#               = sum of k*(k+1)/2 for k = 1 to n
#               ≈ n^3 / 6
#               = O(n^3)
#
# ----- How to THINK about it more simply -----
# Three nested loops, each running up to n times --> O(n) * O(n) * O(n) = O(n^3).
# This is a loose upper bound but gives you the right Big-O.
#
# Space: O(1) — just a few variables (max_sum, current_sum, i, j, k).
#   We don't create any arrays. We compute sums on the fly.


# ----- Approach 2: Optimized Brute Force — O(n^2) -----
#
# Key insight: when we move from subarray [i..j] to [i..j+1],
# we're adding just ONE more element: arr[j+1].
# So: sum(i..j+1) = sum(i..j) + arr[j+1]
#
# We don't need the inner k-loop at all! Just extend the running sum.
#
# ----- How this eliminates the third loop -----
# Before:  for each (i,j), recompute sum from scratch with k-loop  --> O(n^3)
# After:   for each i, extend sum incrementally as j grows          --> O(n^2)
#
# ----- Walkthrough -----
# arr = [1, -2, 3, 4]
#
# i=0: current_sum starts at 0
#   j=0: current_sum += 1  = 1,  max_sum = 1
#   j=1: current_sum += -2 = -1, max_sum = 1
#   j=2: current_sum += 3  = 2,  max_sum = 2
#   j=3: current_sum += 4  = 6,  max_sum = 6
#
# i=1: current_sum resets to 0
#   j=1: current_sum += -2 = -2, max_sum = 6
#   j=2: current_sum += 3  = 1,  max_sum = 6
#   j=3: current_sum += 4  = 5,  max_sum = 6
#
# i=2: current_sum resets to 0
#   j=2: current_sum += 3  = 3,  max_sum = 6
#   j=3: current_sum += 4  = 7,  max_sum = 7   <-- new max!
#
# i=3: current_sum resets to 0
#   j=3: current_sum += 4  = 4,  max_sum = 7
#
# Answer: 7

def max_subarray_sum_optimized(arr: list[int], n: int) -> int:
    max_sum = float('-inf')

    for i in range(n):                  # start of subarray
        current_sum = 0                 # reset for each new starting point
        for j in range(i, n):           # end of subarray
            current_sum += arr[j]       # EXTEND the sum by one element
            max_sum = max(max_sum, current_sum)

    return max_sum

# ----- Deriving the Time Complexity: O(n^2) -----
#
# Two nested loops. Count the inner loop iterations:
#   i=0: j runs n times
#   i=1: j runs n-1 times
#   i=2: j runs n-2 times
#   ...
#   i=n-1: j runs 1 time
#
# Total = n + (n-1) + (n-2) + ... + 1 = n*(n+1)/2 = O(n^2)
#
# Each inner iteration does O(1) work (one addition, one comparison).
# So total work = O(n^2) * O(1) = O(n^2).
#
# ----- The key lesson: going from O(n^3) to O(n^2) -----
# We eliminated an entire loop by REUSING previous computation.
# Instead of recomputing the sum from scratch, we extended it.
# This is called "incremental computation" and is one of the most
# common ways to optimize algorithms. Always ask:
#   "Am I recomputing something I already know?"
#
# Space: O(1) — still just a few variables.


# =============================================================================
# SECTION 8: Prefix Sum
# =============================================================================

# ----- What is a Prefix Sum? -----
#
# A prefix sum array stores the CUMULATIVE SUM up to each index.
#
# Given: arr     = [3, 1, 4, 1, 5]
# Build: prefix  = [3, 4, 8, 9, 14]
#
# prefix[i] = arr[0] + arr[1] + ... + arr[i]
#            = "sum of all elements from the start up to index i"
#
# ----- How to build it -----
# prefix[0] = arr[0]                          (just the first element)
# prefix[i] = prefix[i-1] + arr[i]           (previous prefix + current element)
#
# ----- Walkthrough of building prefix sum -----
# arr = [3, 1, 4, 1, 5]
#
# prefix[0] = 3                               = 3
# prefix[1] = prefix[0] + arr[1] = 3 + 1      = 4
# prefix[2] = prefix[1] + arr[2] = 4 + 4      = 8
# prefix[3] = prefix[2] + arr[3] = 8 + 1      = 9
# prefix[4] = prefix[3] + arr[4] = 9 + 5      = 14
#
# prefix = [3, 4, 8, 9, 14]

def build_prefix_sum(arr: list[int], n: int) -> list[int]:
    prefix = [0] * n
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i - 1] + arr[i]
    return prefix

# Time:  O(n) — single loop through the array
# Space: O(n) — we create a new array of size n
#
# ----- Why is this useful? -----
#
# Once we have the prefix sum array, we can find the SUM OF ANY SUBARRAY
# in O(1) time — just ONE subtraction!
#
# sum(arr[i..j]) = prefix[j] - prefix[i-1]
#
# (If i == 0, then sum(arr[0..j]) = prefix[j])
#
# ----- Why does this formula work? -----
#
# prefix[j]   = arr[0] + arr[1] + ... + arr[i-1] + arr[i] + ... + arr[j]
# prefix[i-1] = arr[0] + arr[1] + ... + arr[i-1]
#
# Subtracting: prefix[j] - prefix[i-1] = arr[i] + arr[i+1] + ... + arr[j]
#
# The prefix[i-1] "cancels out" all the elements before index i, leaving
# exactly the sum of the subarray from i to j.
#
# ----- Walkthrough of using prefix sum -----
# arr    = [3, 1, 4, 1, 5]
# prefix = [3, 4, 8, 9, 14]
#
# Q: What is sum(arr[2..4])?   (sum of elements at indices 2, 3, 4)
# A: prefix[4] - prefix[1] = 14 - 4 = 10
# Check: arr[2]+arr[3]+arr[4] = 4 + 1 + 5 = 10 ✓
#
# Q: What is sum(arr[0..2])?   (sum of elements at indices 0, 1, 2)
# A: prefix[2] = 8             (i=0, so just use prefix[j] directly)
# Check: 3 + 1 + 4 = 8 ✓
#
# Q: What is sum(arr[1..3])?
# A: prefix[3] - prefix[0] = 9 - 3 = 6
# Check: 1 + 4 + 1 = 6 ✓

# ----- The Trade-off: Time vs Space -----
#
# Without prefix sum:
#   - Computing sum of any subarray takes O(n) time (loop through elements)
#   - No extra space needed
#
# With prefix sum:
#   - Building the prefix array: O(n) time, O(n) space (one-time cost)
#   - After that, ANY subarray sum is O(1)
#
# This is worth it when you need to answer MANY subarray sum queries.
# If you only need one sum, it's not worth building the prefix array.
# This is a classic "precomputation" trade-off: spend time and space upfront
# to make future queries faster.


# =============================================================================
# SECTION 9: Maximum Subarray Sum using Prefix Sum
# =============================================================================

# ----- Idea -----
# We already know:  sum(arr[i..j]) = prefix[j] - prefix[i-1]
#
# To maximize this, for each j, we want prefix[i-1] to be as SMALL as possible.
# (Because: bigger number minus smaller number = bigger result)
#
# Approach:
#   For every pair (i, j), compute prefix[j] - prefix[i-1] and track the maximum.
#
# This is still O(n^2) because we try all pairs, but it shows how prefix sums
# transform the problem from "summing subarrays" to "subtracting two values".

# ----- Method 1: Using prefix sum with two loops — O(n^2) -----

def max_subarray_sum_prefix(arr: list[int], n: int) -> int:
    prefix = build_prefix_sum(arr, n)

    max_sum = float('-inf')

    for i in range(n):                  # start of subarray
        for j in range(i, n):           # end of subarray
            if i == 0:
                current_sum = prefix[j]
            else:
                current_sum = prefix[j] - prefix[i - 1]
            max_sum = max(max_sum, current_sum)

    return max_sum

# ----- Walkthrough -----
# arr    = [1, -2, 3, 4]
# prefix = [1, -1, 2, 6]
#
# i=0, j=0: prefix[0]                  = 1,   max = 1
# i=0, j=1: prefix[1]                  = -1,  max = 1
# i=0, j=2: prefix[2]                  = 2,   max = 2
# i=0, j=3: prefix[3]                  = 6,   max = 6
# i=1, j=1: prefix[1] - prefix[0]      = -1-1 = -2,  max = 6
# i=1, j=2: prefix[2] - prefix[0]      = 2-1  = 1,   max = 6
# i=1, j=3: prefix[3] - prefix[0]      = 6-1  = 5,   max = 6
# i=2, j=2: prefix[2] - prefix[1]      = 2-(-1) = 3, max = 6
# i=2, j=3: prefix[3] - prefix[1]      = 6-(-1) = 7, max = 7  <-- new max!
# i=3, j=3: prefix[3] - prefix[2]      = 6-2 = 4,    max = 7
#
# Answer: 7 (subarray [3, 4])

# ----- Time: O(n^2) -----
# Building prefix sum: O(n)
# Two nested loops: O(n^2)
# Each inner iteration: O(1) (just a subtraction and comparison)
# Total: O(n) + O(n^2) = O(n^2)
#   (The O(n) for building prefix is absorbed by the larger O(n^2))
#
# ----- Space: O(n) -----
# The prefix array uses O(n) extra space.
# This is a trade-off vs the optimized brute force (O(1) space, same O(n^2) time).
# Here, the prefix sum doesn't give us a time advantage — but it introduces the
# CONCEPT which becomes powerful in other problems (range queries, 2D prefix sums, etc.)


# ----- Method 2: Smarter prefix sum approach — O(n) -----
#
# Key insight: sum(arr[i..j]) = prefix[j] - prefix[i-1]
# To MAXIMIZE this for a given j, we need the MINIMUM prefix[i-1] seen so far.
#
# So instead of trying all pairs (i,j), for each j we just need:
#   max_sum = max(max_sum, prefix[j] - min_prefix_so_far)
#
# We track min_prefix_so_far as we go — single pass!

def max_subarray_sum_prefix_optimized(arr: list[int], n: int) -> int:
    prefix = build_prefix_sum(arr, n)

    max_sum = float('-inf')
    min_prefix = 0          # represents prefix[-1] = 0 (empty prefix before index 0)

    for j in range(n):
        max_sum = max(max_sum, prefix[j] - min_prefix)
        min_prefix = min(min_prefix, prefix[j])

    return max_sum

# ----- Walkthrough -----
# arr    = [1, -2, 3, 4]
# prefix = [1, -1, 2, 6]
#
# Start: max_sum = -inf, min_prefix = 0
#
# j=0: max_sum = max(-inf, prefix[0] - 0) = max(-inf, 1) = 1
#      min_prefix = min(0, 1) = 0
#
# j=1: max_sum = max(1, prefix[1] - 0) = max(1, -1) = 1
#      min_prefix = min(0, -1) = -1
#
# j=2: max_sum = max(1, prefix[2] - (-1)) = max(1, 2+1) = max(1, 3) = 3
#      min_prefix = min(-1, 2) = -1
#
#      Wait — that gives 3, but the answer should be 7. Let me re-check...
#      Actually prefix[2] - min_prefix = 2 - (-1) = 3. That's sum(arr[1..2]) = -2+3 = 1.
#      Hmm, that doesn't match. Let me recalculate.
#
#      prefix[2] = arr[0]+arr[1]+arr[2] = 1+(-2)+3 = 2
#      min_prefix = -1 (which is prefix[1])
#      prefix[2] - prefix[1] = 2 - (-1) = 3
#      But sum(arr[2..2]) = 3, and sum(arr[1..2]) = -2+3 = 1
#      prefix[2] - prefix[1] = sum(arr[2..2]) = 3 ✓  (because prefix[j]-prefix[i-1] where i=2, i-1=1)
#
# j=3: max_sum = max(3, prefix[3] - (-1)) = max(3, 6+1) = max(3, 7) = 7
#      min_prefix = min(-1, 6) = -1
#
#      prefix[3] - prefix[1] = 6 - (-1) = 7
#      This is sum(arr[2..3]) = 3+4 = 7 ✓
#
# Answer: 7

# ----- Why does min_prefix start at 0? -----
# min_prefix represents the minimum of all prefix[-1], prefix[0], prefix[1], ..., prefix[j-1].
# prefix[-1] = 0 (the sum of zero elements before the array starts).
# This handles the case where the best subarray starts at index 0:
#   sum(arr[0..j]) = prefix[j] - prefix[-1] = prefix[j] - 0 = prefix[j]

# ----- Deriving the Time Complexity: O(n) -----
#
# Building prefix sum: O(n) — one pass
# Finding max subarray: O(n) — one pass
# Total: O(n) + O(n) = O(2n) = O(n)
#
# We went from O(n^3) --> O(n^2) --> O(n) by:
#   Step 1: Reusing partial sums (eliminated the k-loop)
#   Step 2: Precomputing all prefix sums (set up O(1) range queries)
#   Step 3: Realizing we only need the MINIMUM prefix, not all pairs
#
# ----- Space: O(n) -----
# The prefix array takes O(n). We could technically make this O(1) by computing
# the running prefix sum on the fly (like Kadane's algorithm does), but keeping
# the prefix array makes the logic clearer.


# =============================================================================
# SECTION 10: How to Think About Complexity (A Guide)
# =============================================================================

# ----- The Goal -----
# Don't memorize "binary search = O(log n)". Instead, learn to DERIVE it
# from the code structure. Here's how to think about it:
#
#
# === STEP 1: Count the loops ===
#
# Single loop over n elements:                    O(n)
# Two nested loops, each up to n:                 O(n^2)
# Three nested loops:                             O(n^3)
# Loop that halves/doubles each step:             O(log n)
# Loop of n with halving loop inside:             O(n log n)
#
#
# === STEP 2: Look at what happens INSIDE the innermost loop ===
#
# If the innermost operation is O(1) (addition, comparison, assignment):
#   Total = (number of iterations) * O(1) = number of iterations
#
# If the innermost operation itself takes O(k) time (e.g., slicing, copying):
#   Total = (number of iterations) * O(k)
#   This is why generate_subarrays is O(n^3) not O(n^2) — the slice is O(k)
#
#
# === STEP 3: Count the ACTUAL iterations, not just "up to n" ===
#
# For nested loops, the inner loop often runs a VARIABLE number of times:
#   for i in range(n):
#       for j in range(i, n):   # NOT range(n)!
#
# Inner iterations: n + (n-1) + (n-2) + ... + 1 = n*(n+1)/2
# This is O(n^2), not O(n^2) "times 2" — the 1/2 is a constant and drops.
#
#
# === STEP 4: For space, ask "what new data structures did I create?" ===
#
# No new arrays/lists → O(1) space
# One array of size n → O(n) space
# 2D array of size n x n → O(n^2) space
# Just a few variables → O(1) space
# Recursive calls (call stack) → O(depth) space
#
#
# === STEP 5: The "double the input" test ===
#
# If I double n, how does the runtime change?
#   O(1):      no change        (formula, array lookup)
#   O(log n):  adds ~1 step     (binary search)
#   O(n):      doubles          (single loop)
#   O(n log n): slightly > 2x   (merge sort)
#   O(n^2):    quadruples (4x)  (nested loops)
#   O(n^3):    8x               (triple nested loops)
#   O(2^n):    SQUARES           (exponential, unusable for large n)
#
#
# === COMMON PATTERNS IN THIS FILE ===
#
# | Code pattern                    | Complexity | Why                          |
# |---------------------------------|------------|------------------------------|
# | while lo <= hi: mid = ...       | O(log n)   | Search space halves each step|
# | for i in range(n):              | O(n)       | One pass through array       |
# | for i...for j in range(i,n):    | O(n^2)     | All pairs, triangular sum    |
# | for i...for j...for k(i,j+1):   | O(n^3)     | All pairs + sum each pair    |
# | prefix[j] - prefix[i-1]        | O(1)       | Precomputed, just subtraction|
# | track min/max "so far"          | O(n)       | One pass, constant work each |
#
#
# === THE OPTIMIZATION MINDSET ===
#
# When your solution is too slow, ask these questions in order:
#
# 1. "Am I recomputing something I already know?"
#    --> Use incremental computation (O(n^3) → O(n^2) in max subarray sum)
#
# 2. "Can I precompute answers to subproblems?"
#    --> Use prefix sums, lookup tables, memoization
#
# 3. "Do I need to check ALL possibilities, or can I eliminate some?"
#    --> Use binary search (O(n) → O(log n)), two pointers, sorting
#
# 4. "Can I track just what I need instead of storing everything?"
#    --> Use running min/max/sum instead of arrays (O(n) space → O(1))


# =============================================================================
# Test all approaches
# =============================================================================

arr = [1, -2, 3, 4]
n = 4
print("Brute force O(n^3):", max_subarray_sum_brute(arr, n))
print("Optimized O(n^2):  ", max_subarray_sum_optimized(arr, n))
print("Prefix sum O(n^2): ", max_subarray_sum_prefix(arr, n))
print("Prefix opt O(n):   ", max_subarray_sum_prefix_optimized(arr, n))

arr2 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
n2 = 9
print("\nClassic example [-2, 1, -3, 4, -1, 2, 1, -5, 4]:")
print("Brute force O(n^3):", max_subarray_sum_brute(arr2, n2))
print("Optimized O(n^2):  ", max_subarray_sum_optimized(arr2, n2))
print("Prefix sum O(n^2): ", max_subarray_sum_prefix(arr2, n2))
print("Prefix opt O(n):   ", max_subarray_sum_prefix_optimized(arr2, n2))

# Expected output: 7 for arr, 6 for arr2 (subarray [4, -1, 2, 1])

