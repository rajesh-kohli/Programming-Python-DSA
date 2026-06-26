###############################################################################
#              Lecture 11 - Arrays: Sorting Algorithms & Built-in Sort        #
###############################################################################

# This lecture covers three fundamental sorting algorithms:
#   1. Selection Sort
#   2. Bubble Sort
#   3. Insertion Sort
# And then Python's built-in sorting tools (sorted() and .sort())

# ----- Key Terminology -----
#
# "In-place":  The algorithm sorts the array without creating a new array.
#              It modifies the original array directly. All three algorithms below are in-place.
#
# "Stable":    A sorting algorithm is stable if it preserves the relative order
#              of elements that have EQUAL values.
#              Example: [(A, 3), (B, 1), (C, 3)] sorted by number:
#                Stable:   [(B, 1), (A, 3), (C, 3)]   --> A still comes before C (original order kept)
#                Unstable: [(B, 1), (C, 3), (A, 3)]   --> C came before A (original order NOT kept)
#              This matters when sorting by multiple criteria (e.g., sort by grade, then by name).


# =============================================================================
# SECTION 1: Selection Sort - O(n^2)
# =============================================================================

# ----- Core Idea -----
# In each pass, FIND the smallest element in the unsorted portion
# and SWAP it into its correct position at the front.
#
# Think of it like: picking the smallest card from a pile and placing it in order.
#
# ----- How it works (step by step) -----
# The array is divided into two parts:
#   [  sorted part  |  unsorted part  ]
#   Left side is sorted, right side is unsorted.
#   In each pass, we grow the sorted part by 1 element.
#
# ----- Visual Walkthrough -----
# arr = [50, 20, 30, 10, 40]
#
# Pass 1 (i=1): Find smallest in [50, 20, 30, 10, 40] --> 10 at index 3
#               Swap arr[0] and arr[3]
#               [10, 20, 30, 50, 40]
#                ^sorted|  unsorted
#
# Pass 2 (i=2): Find smallest in [20, 30, 50, 40] --> 20 at index 1
#               Swap arr[1] and arr[1] (already in place!)
#               [10, 20, 30, 50, 40]
#                ^sorted^|  unsorted
#
# Pass 3 (i=3): Find smallest in [30, 50, 40] --> 30 at index 2
#               Swap arr[2] and arr[2] (already in place!)
#               [10, 20, 30, 50, 40]
#                ^sorted   ^| unsorted
#
# Pass 4 (i=4): Find smallest in [50, 40] --> 40 at index 4
#               Swap arr[3] and arr[4]
#               [10, 20, 30, 40, 50]
#                ^sorted         ^  DONE!

# time : O(n^2) always (even if already sorted - it still scans for min each time)
# selection sort is NOT a stable sorting algorithm
# (swapping can change the relative order of equal elements)

def selection_sort(arr: list[int], n: int) -> None:
    """
    The selection sort algorithm works in passes such that in its each pass,
    we place the smallest element in the unsorted part of the array to its correct position
    """
    for i in range(1, n):  # [1, n) --> n-1 passes
        # in the ith pass, put the smallest
        # element in the unsorted part of the
        # array to its correct position

        min_idx = i - 1     # assume the first unsorted element is the smallest

        for j in range(i, n):           # scan through the rest of unsorted part
            if arr[j] < arr[min_idx]:
                min_idx = j             # found something smaller, update min_idx

        arr[i - 1], arr[min_idx] = arr[min_idx], arr[i - 1]    # swap smallest to front

# ----- Why O(n^2)? -----
# Pass 1: compare n-1 elements
# Pass 2: compare n-2 elements
# Pass 3: compare n-3 elements
# ...
# Total comparisons = (n-1) + (n-2) + ... + 1 = n*(n-1)/2 = O(n^2)
#
# ----- Why NOT stable? -----
# Example: arr = [4a, 4b, 1]  (4a and 4b are both value 4)
# Pass 1: smallest = 1, swap arr[0] and arr[2] --> [1, 4b, 4a]
# Now 4b comes before 4a - original order of equal elements is broken!


n = int(input())
arr = [int(input()) for _ in range(n)]

print(arr)  # [50, 40, 30, 20, 10]
selection_sort(arr, n)
print(arr)  # [10, 20, 30, 40, 50]


# =============================================================================
# SECTION 2: Bubble Sort - O(n^2) worst, O(n) best
# =============================================================================

# ----- Core Idea -----
# Repeatedly walk through the array, comparing ADJACENT elements,
# and SWAP them if they are in the wrong order.
# The largest unsorted element "bubbles up" to the end in each pass.
#
# Think of it like: the biggest bubble always floats to the top.
#
# ----- How it works (step by step) -----
# In each pass, compare arr[j] with arr[j+1]:
#   - If arr[j] > arr[j+1], swap them (bigger element moves right)
#   - After pass i, the i-th largest element is in its final position
#
# ----- Visual Walkthrough -----
# arr = [50, 40, 30, 20, 10]
#
# Pass 1 (i=1): Compare adjacent pairs in [50, 40, 30, 20, 10]
#   j=0: 50 > 40? YES, swap --> [40, 50, 30, 20, 10]
#   j=1: 50 > 30? YES, swap --> [40, 30, 50, 20, 10]
#   j=2: 50 > 20? YES, swap --> [40, 30, 20, 50, 10]
#   j=3: 50 > 10? YES, swap --> [40, 30, 20, 10, 50]
#                                                 ^^ 50 bubbled to the end!
#
# Pass 2 (i=2): Compare adjacent pairs in [40, 30, 20, 10 | 50]
#   j=0: 40 > 30? YES, swap --> [30, 40, 20, 10, 50]
#   j=1: 40 > 20? YES, swap --> [30, 20, 40, 10, 50]
#   j=2: 40 > 10? YES, swap --> [30, 20, 10, 40, 50]
#                                             ^^ 40 in place!
#
# Pass 3 (i=3): Compare adjacent pairs in [30, 20, 10 | 40, 50]
#   j=0: 30 > 20? YES, swap --> [20, 30, 10, 40, 50]
#   j=1: 30 > 10? YES, swap --> [20, 10, 30, 40, 50]
#                                         ^^ 30 in place!
#
# Pass 4 (i=4): Compare adjacent pairs in [20, 10 | 30, 40, 50]
#   j=0: 20 > 10? YES, swap --> [10, 20, 30, 40, 50]  DONE!
#
# ----- The "flag" Optimization (Early Termination) -----
# If during a pass, NO swaps happen, the array is already sorted!
# We can stop early. This is what makes best case O(n).
#
# Example: arr = [10, 20, 30, 40, 50] (already sorted)
# Pass 1: compare all adjacent pairs, no swaps needed --> flag stays False --> STOP
# Only 1 pass with n-1 comparisons = O(n)

# time : O(n^2) worst case (e.g. reverse sorted: [50, 40, 30, 20, 10])
# time : O(n) best case (e.g. already sorted: [10, 20, 30, 40, 50])
# bubble sort is a stable sorting algorithm
# (only swaps adjacent elements, so equal elements never cross each other)

def bubble_sort(arr: list[int], n: int) -> None:
    cnt = 0     # counts total comparisons (for learning purposes)

    for i in range(1, n):  # [1, n) --> at most n-1 passes
        # in the ith pass, put the largest
        # value in the unsorted part of the
        # array to its correct position

        flag = False  # assume no swaps will be done in the ith pass

        for j in range(n - i):  # [0, n-i) --> each pass has fewer comparisons
            cnt += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]    # swap adjacent elements
                flag = True     # a swap happened

        if not flag:  # flag == False --> no swaps in this pass --> already sorted!
            break

    print(cnt)

# ----- Why O(n^2)? -----
# Without the flag optimization:
# Pass 1: n-1 comparisons
# Pass 2: n-2 comparisons
# ...
# Total = (n-1) + (n-2) + ... + 1 = n*(n-1)/2 = O(n^2)
#
# With flag optimization (best case - already sorted):
# Pass 1: n-1 comparisons, no swaps --> break
# Total = n-1 = O(n)
#
# ----- Why is it Stable? -----
# We only swap arr[j] and arr[j+1] when arr[j] > arr[j+1] (strictly greater).
# If arr[j] == arr[j+1], NO swap happens, so equal elements stay in original order.


n = int(input())
arr = [int(input()) for _ in range(n)]

print(arr)  # [50, 40, 30, 20, 10]
bubble_sort(arr, n)
print(arr)  # [10, 20, 30, 40, 50]


# =============================================================================
# SECTION 3: Insertion Sort - O(n^2) worst, O(n) best
# =============================================================================

# ----- Core Idea -----
# Pick each element (the "key") and INSERT it into its correct position
# in the already-sorted portion to its left.
#
# Think of it like: sorting playing cards in your hand.
# You pick up one card at a time and slide it into the right spot among
# the cards you're already holding.
#
# ----- How it works (step by step) -----
# 1. Start from index 1 (index 0 is a "sorted array" of 1 element)
# 2. Save arr[i] as the "key"
# 3. Compare key with elements to its left (j = i-1, i-2, ...)
# 4. Shift elements RIGHT that are greater than key (arr[j+1] = arr[j])
# 5. Place key in the gap that's left (arr[j+1] = key)
#
# ----- Visual Walkthrough -----
# arr = [50, 40, 30, 20, 10]
#
# Pass 1 (i=1): key = 40
#   Sorted part: [50]  |  key = 40
#   j=0: arr[0]=50 > 40? YES, shift 50 right --> [50, 50, 30, 20, 10]
#   j=-1: stop (out of bounds)
#   Place key at j+1=0 --> [40, 50, 30, 20, 10]
#                           ^^sorted|  unsorted
#
# Pass 2 (i=2): key = 30
#   Sorted part: [40, 50]  |  key = 30
#   j=1: arr[1]=50 > 30? YES, shift right --> [40, 50, 50, 20, 10]
#   j=0: arr[0]=40 > 30? YES, shift right --> [40, 40, 50, 20, 10]
#   j=-1: stop
#   Place key at j+1=0 --> [30, 40, 50, 20, 10]
#                           ^^ sorted ^| unsorted
#
# Pass 3 (i=3): key = 20
#   Sorted part: [30, 40, 50]  |  key = 20
#   j=2: 50 > 20? YES, shift --> [30, 40, 50, 50, 10]
#   j=1: 40 > 20? YES, shift --> [30, 40, 40, 50, 10]
#   j=0: 30 > 20? YES, shift --> [30, 30, 40, 50, 10]
#   j=-1: stop
#   Place key at 0 --> [20, 30, 40, 50, 10]
#
# Pass 4 (i=4): key = 10
#   Sorted part: [20, 30, 40, 50]  |  key = 10
#   Shift all right (all > 10)
#   Place key at 0 --> [10, 20, 30, 40, 50]  DONE!
#
# ----- Best Case: Already Sorted -----
# arr = [10, 20, 30, 40, 50]
# Pass 1: key=20, compare with 10 --> 10 < 20 --> no shift --> O(1) work
# Pass 2: key=30, compare with 20 --> 20 < 30 --> no shift --> O(1) work
# ...each pass does only 1 comparison --> total = n-1 = O(n)

# stable sorting algorithm
# (we only shift elements that are strictly greater than key, so equal elements keep order)
# time : O(n^2) worst case e.g. 50 40 30 20 10 (reverse sorted - maximum shifts)
# time : O(n) best e.g. 10, 20, 30, 40, 50 (already sorted - no shifts needed)

def insertion_sort(arr: list[int], n: int) -> None:
    for i in range(1, n):  # [1, n) --> start from 2nd element
        key = arr[i]            # element to be inserted
        # in the ith pass, insert the key to
        # its correct position in the sorted
        # part of the arr
        j = i - 1
        while j >= 0 and key < arr[j]:      # move left while elements are larger than key
            arr[j + 1] = arr[j]              # shift element one position to the right
            j -= 1

        arr[j + 1] = key       # place key in the correct gap

# ----- Why j+1? -----
# The while loop stops when EITHER:
#   - j < 0  (key is smaller than everything, goes to index 0)
#   - key >= arr[j]  (found the right spot: key goes right AFTER arr[j])
# In both cases, the correct position is j + 1.
#
# ----- Why O(n^2)? -----
# Worst case (reverse sorted): each element shifts ALL the way to the front
# Pass 1: 1 shift
# Pass 2: 2 shifts
# ...
# Pass n-1: n-1 shifts
# Total = 1 + 2 + ... + (n-1) = n*(n-1)/2 = O(n^2)


n = int(input())
arr = [int(input()) for _ in range(n)]

print(arr)  # [50, 40, 30, 20, 10]
insertion_sort(arr, n)
print(arr)  # [10, 20, 30, 40, 50]


# =============================================================================
# SECTION 4: Comparison of All Three Algorithms
# =============================================================================

# | Algorithm      | Best Case | Worst Case | Stable? | Key Operation         |
# |----------------|-----------|------------|---------|-----------------------|
# | Selection Sort | O(n^2)    | O(n^2)     | NO      | Find min, swap        |
# | Bubble Sort    | O(n)      | O(n^2)     | YES     | Compare adjacent, swap|
# | Insertion Sort | O(n)      | O(n^2)     | YES     | Shift and insert      |
#
# When to use which?
# - Selection Sort: fewest SWAPS (only n-1 swaps total) - good when swapping is expensive
# - Bubble Sort:    simple to understand, detects already-sorted arrays quickly
# - Insertion Sort: best for NEARLY sorted arrays and small arrays, used in practice
#                   (Python's built-in sort uses insertion sort for small subarrays!)
#
# All three are O(n^2) in worst case, so they are NOT efficient for large datasets.
# For large arrays, use O(n log n) algorithms like Merge Sort or Quick Sort.


# =============================================================================
# SECTION 5: Python's Built-in Sorting
# =============================================================================

# Python provides two ways to sort:
#   sorted(list)  --> returns a NEW sorted list (original unchanged)
#   list.sort()   --> sorts the list IN-PLACE (modifies original, returns None)

# ----- sorted() function: creates a new sorted list -----

nums = [30, 10, 20, 50, 40]
sorted_nums = sorted(nums)  # creates a sorted list in inc. order
# sorted_nums = sorted(nums, reverse=True) # creates a sorted list in dec. order

print(nums)         # [30, 10, 20, 50, 40]  --> original unchanged!
print(sorted_nums)  # [10, 20, 30, 40, 50]

# ----- .sort() method: sorts in-place -----

temp = [87, 90, 95, 76, 98]
# temp.sort() # sorts the list in-place
temp.sort(reverse=True)     # sort in descending order
print(temp)  # [98, 95, 90, 87, 76]

# ----- Sorting strings (alphabetical / lexicographic order) -----

animals = ["ch", "ze", "al", "be", "ti"]
sorted_animals = sorted(animals)
# sorted_animals = sorted(animals, reverse=True)
print(sorted_animals)   # ['al', 'be', 'ch', 'ti', 'ze']

# ----- Custom sorting with key= parameter -----
# key= takes a function that extracts a comparison value from each element
# The list is then sorted by those extracted values

names = ["ifrah", "aryan", "avi", "aditya", "yash"]
sorted_names = sorted(names, key=len)       # sort by LENGTH of each name
# sorted_names = sorted(names, key=len, reverse=True)
print(sorted_names)     # ['avi', 'yash', 'ifrah', 'aryan', 'aditya']
# 'avi'(3) < 'yash'(4) < 'ifrah'(5) = 'aryan'(5) < 'aditya'(6)

# ----- Sorting tuples with lambda -----
# lambda is an anonymous (unnamed) function
# lambda p: p[1]  means: "given a tuple p, return its element at index 1"

pairs = [(3, 1), (2, 0), (1, 3), (4, 2)]
# sorted_pairs = sorted(pairs)     # default: sorts by first element, then second
sorted_pairs = sorted(pairs, key=lambda p: p[1], reverse=True)
print(sorted_pairs)     # [(1, 3), (4, 2), (3, 1), (2, 0)]
# Sorted by second element (p[1]) in descending order:
# p[1] values: 3, 2, 1, 0 --> pairs: (1,3), (4,2), (3,1), (2,0)

# ----- Python's sort is Timsort: O(n log n) -----
# Under the hood, Python uses Timsort (a hybrid of Merge Sort + Insertion Sort).
# It is stable and runs in O(n log n) worst case, much faster than the O(n^2) algorithms above.
