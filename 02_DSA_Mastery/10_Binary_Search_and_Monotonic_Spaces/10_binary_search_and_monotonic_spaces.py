#               10 - Binary Search and Monotonic Spaces               #

from typing import List
import bisect

# =============================================================================
# SECTION 1: Standard Binary Search
# =============================================================================

# ----- Approach: Optimal O(log n) -----
def binary_search(arr: List[int], target: int) -> int:
    lo, hi = 0, len(arr) - 1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1 # Target is to the right
        else:
            hi = mid - 1 # Target is to the left
            
    return -1

# Time: O(log n)
# Space: O(1)

# --- Practice Skeleton ---
def practice_binary_search(arr: List[int], target: int) -> int:
    pass


# =============================================================================
# SECTION 2: First Occurrence in Sorted Array
# =============================================================================
# Regular binary search stops at ANY match. To find the first occurrence,
# DO NOT stop when you find a match. Save it, and keep searching LEFT.

# ----- Approach: Optimal O(log n) -----
def first_occurrence(arr: List[int], target: int) -> int:
    lo, hi = 0, len(arr) - 1
    ans = -1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        
        if arr[mid] == target:
            ans = mid
            # Found a match, but there might be an earlier one. Keep searching left.
            hi = mid - 1
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
            
    return ans

# Time: O(log n)
# Space: O(1)

# --- Practice Skeleton ---
def practice_first_occurrence(arr: List[int], target: int) -> int:
    pass


# =============================================================================
# SECTION 3: Last Occurrence in Sorted Array
# =============================================================================
# To find the last occurrence, DO NOT stop when you find a match.
# Save it, and keep searching RIGHT.

# ----- Approach: Optimal O(log n) -----
def last_occurrence(arr: List[int], target: int) -> int:
    lo, hi = 0, len(arr) - 1
    ans = -1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        
        if arr[mid] == target:
            ans = mid
            # Found a match, but there might be a later one. Keep searching right.
            lo = mid + 1
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
            
    return ans

# Time: O(log n)
# Space: O(1)

# --- Practice Skeleton ---
def practice_last_occurrence(arr: List[int], target: int) -> int:
    pass


# =============================================================================
# SECTION 4: Count Occurrences in Sorted Array
# =============================================================================
# Since the array is sorted, all occurrences of `target` are contiguous.
# Count = last_index - first_index + 1

# ----- Approach: Optimal O(log n) -----
def count_occurrences(arr: List[int], target: int) -> int:
    first = first_occurrence(arr, target)
    if first == -1:
        return 0
    last = last_occurrence(arr, target)
    return last - first + 1

# Time: O(log n) + O(log n) = O(log n)
# Space: O(1)

# --- Practice Skeleton ---
def practice_count_occurrences(arr: List[int], target: int) -> int:
    pass


# =============================================================================
# SECTION 5: Python's Built-in 'bisect' Module
# =============================================================================
# In interviews, if you don't need to write binary search from scratch, use bisect.

def bisect_examples():
    arr = [10, 20, 30, 30, 30, 40, 50]
    target = 30
    
    # bisect_left gives the FIRST occurrence (or where it should be inserted to maintain order)
    left_idx = bisect.bisect_left(arr, target)
    print(f"bisect_left({target}):", left_idx) # Output: 2
    
    # bisect_right gives the index AFTER the last occurrence
    right_idx = bisect.bisect_right(arr, target)
    print(f"bisect_right({target}):", right_idx) # Output: 5
    
    # Count occurrences using bisect
    count = right_idx - left_idx
    print(f"Count of {target}:", count) # Output: 3


# =============================================================================
# DRIVER CODE FOR TESTING SKELETONS
# =============================================================================
if __name__ == "__main__":
    print("Testing 10_Binary_Search_and_Monotonic_Spaces skeletons...")
    
    arr = [10, 20, 30, 30, 30, 40, 50]
    print("Binary Search (30):", practice_binary_search(arr, 30))
    print("First Occurrence (30):", practice_first_occurrence(arr, 30))
    print("Last Occurrence (30):", practice_last_occurrence(arr, 30))
    print("Count Occurrences (30):", practice_count_occurrences(arr, 30))
    
    print("\n--- Built-in Bisect Examples ---")
    bisect_examples()
