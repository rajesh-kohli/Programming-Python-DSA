#                  12 - Classical Sorting Algorithms                  #

from typing import List

# =============================================================================
# SECTION 1: Selection Sort
# =============================================================================
# Find the minimum element in the unsorted portion and swap it to the front.

def selection_sort(arr: List[int]) -> None:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

# Time: O(n^2) always
# Space: O(1)
# Stability: Unstable


# =============================================================================
# SECTION 2: Bubble Sort
# =============================================================================
# Repeatedly swap adjacent elements if they are in wrong order.
# Largest elements "bubble" to the end.

def bubble_sort(arr: List[int]) -> None:
    n = len(arr)
    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break # Optimization: array is already sorted

# Time: O(n^2) worst/average, O(n) best (if already sorted)
# Space: O(1)
# Stability: Stable


# =============================================================================
# SECTION 3: Insertion Sort
# =============================================================================
# Build sorted array one element at a time by shifting larger elements right.

def insertion_sort(arr: List[int]) -> None:
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Shift elements greater than key to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Time: O(n^2) worst/average, O(n) best
# Space: O(1)
# Stability: Stable


# =============================================================================
# SECTION 4: DNF Sort (Sort Colors / 0, 1, 2)
# =============================================================================
# Sort an array of exactly 3 distinct values in a single pass.

def dnf_sort(arr: List[int]) -> None:
    lo, mid, hi = 0, 0, len(arr) - 1
    
    while mid <= hi:
        if arr[mid] == 0:
            arr[lo], arr[mid] = arr[mid], arr[lo]
            lo += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else: # arr[mid] == 2
            arr[mid], arr[hi] = arr[hi], arr[mid]
            hi -= 1

# Time: O(n)
# Space: O(1)

# --- Practice Skeleton ---
def practice_dnf_sort(arr: List[int]) -> None:
    pass


# =============================================================================
# SECTION 5: Counting Sort
# =============================================================================
# Only works for positive integers in a small range.

def counting_sort(arr: List[int]) -> None:
    if not arr: return
    
    k = max(arr)
    freq = [0] * (k + 1)
    
    # Count frequencies
    for num in arr:
        freq[num] += 1
        
    # Reconstruct array
    idx = 0
    for num in range(k + 1):
        while freq[num] > 0:
            arr[idx] = num
            idx += 1
            freq[num] -= 1

# Time: O(n + k)
# Space: O(k)

# --- Practice Skeleton ---
def practice_counting_sort(arr: List[int]) -> None:
    pass


# =============================================================================
# SECTION 6: Generalized Counting Sort (Supports Negatives)
# =============================================================================
# Shift all elements by the minimum value so the range starts at 0.

def generalized_counting_sort(arr: List[int]) -> None:
    if not arr: return
    
    min_val = min(arr)
    max_val = max(arr)
    k = max_val - min_val
    
    freq = [0] * (k + 1)
    
    for num in arr:
        freq[num - min_val] += 1
        
    idx = 0
    for num in range(k + 1):
        while freq[num] > 0:
            arr[idx] = num + min_val
            idx += 1
            freq[num] -= 1

# Time: O(n + k)
# Space: O(k)


# =============================================================================
# DRIVER CODE FOR TESTING SKELETONS
# =============================================================================
if __name__ == "__main__":
    print("Testing 12_Classical_Sorting_Algorithms skeletons...")
    
    arr_dnf = [2, 0, 2, 1, 1, 0]
    practice_dnf_sort(arr_dnf)
    print("DNF Sort:", arr_dnf)
    
    arr_count = [4, 2, 2, 8, 3, 3, 1]
    practice_counting_sort(arr_count)
    print("Counting Sort:", arr_count)
