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

# ----- Why O(log n)? -----
# Each iteration cuts the search space in half:
#   n --> n/2 --> n/4 --> n/8 --> ... --> 1
# After k steps: n / 2^k = 1  -->  k = log2(n)


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


# this is always O(logn)

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
# Time complexity: O(n^2) for generating, O(n^3) if you count printing each subarray


### Maximum Subarray Sum
def maximum_subarray_sum



