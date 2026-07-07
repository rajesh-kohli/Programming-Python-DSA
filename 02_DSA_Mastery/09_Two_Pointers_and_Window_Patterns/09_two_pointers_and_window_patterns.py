#               09 - Two Pointers and Window Patterns                 #

from typing import List

# =============================================================================
# SECTION 1: Target Sum Pair (Sorted Array)
# =============================================================================

# ----- Approach 1: Brute Force -----
def target_sum_pair_brute(arr: List[int], target: int) -> int:
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                count += 1
    return count
# Time: O(n^2), Space: O(1)

# ----- Approach 2: Optimal (Two Pointers - Opposite Ends) -----
# ONLY works if the array is sorted.
def target_sum_pair_optimal(arr: List[int], target: int) -> int:
    # arr must be sorted!
    i, j = 0, len(arr) - 1
    count = 0
    
    while i < j:
        current_sum = arr[i] + arr[j]
        if current_sum == target:
            count += 1
            i += 1
            j -= 1
        elif current_sum < target:
            i += 1 # We need a larger sum, move left pointer right
        else:
            j -= 1 # We need a smaller sum, move right pointer left
            
    return count
# Time: O(n), Space: O(1)

# --- Practice Skeleton ---
def practice_target_sum_pair(arr: List[int], target: int) -> int:
    pass


# =============================================================================
# SECTION 2: Container With Most Water
# =============================================================================
# Find two lines that together with the x-axis form a container holding the most water.
# Area = width * min(height_left, height_right)

# ----- Approach 1: Brute Force -----
def max_area_brute(height: List[int]) -> int:
    n = len(height)
    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            w = j - i
            h = min(height[i], height[j])
            max_area = max(max_area, w * h)
    return max_area
# Time: O(n^2)

# ----- Approach 2: Optimal (Two Pointers) -----
# Start wide. The height is capped by the SHORTER line.
# To potentially increase area, we MUST move the shorter line inward.
def max_area_optimal(height: List[int]) -> int:
    i, j = 0, len(height) - 1
    max_area = 0
    
    while i < j:
        w = j - i
        h = min(height[i], height[j])
        max_area = max(max_area, w * h)
        
        # Move the limiting (shorter) side
        if height[i] < height[j]:
            i += 1
        else:
            j -= 1
            
    return max_area
# Time: O(n), Space: O(1)

# --- Practice Skeleton ---
def practice_max_area(height: List[int]) -> int:
    pass


# =============================================================================
# SECTION 3: Merge Two Sorted Arrays
# =============================================================================

# ----- Approach: Optimal (Two Pointers - Same Direction) -----
def merge_sorted_arrays(a: List[int], b: List[int]) -> List[int]:
    n, m = len(a), len(b)
    c = [0] * (n + m)
    i, j, k = 0, 0, 0
    
    while i < n and j < m:
        if a[i] <= b[j]:
            c[k] = a[i]
            i += 1
        else:
            c[k] = b[j]
            j += 1
        k += 1
        
    # Copy remaining elements (only one of these while loops will run)
    while i < n:
        c[k] = a[i]
        i += 1
        k += 1
        
    while j < m:
        c[k] = b[j]
        j += 1
        k += 1
        
    return c
# Time: O(n + m), Space: O(n + m)

# --- Practice Skeleton ---
def practice_merge_sorted_arrays(a: List[int], b: List[int]) -> List[int]:
    pass


# =============================================================================
# SECTION 4: Remove Duplicates from Sorted Array (In-Place)
# =============================================================================

# ----- Approach: Optimal (Fast/Slow Pointers) -----
# 'slow' tracks the boundary of the unique elements.
# 'fast' scouts ahead to find new unique elements.
def remove_duplicates_optimal(arr: List[int]) -> int:
    if not arr: return 0
    slow = 0
    
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
            
    # return the new length of unique elements
    return slow + 1
# Time: O(n), Space: O(1)

# --- Practice Skeleton ---
def practice_remove_duplicates(arr: List[int]) -> int:
    pass


# =============================================================================
# SECTION 5: Rainwater Trapping
# =============================================================================
# Calculate total trapped water after raining.
# Water at index i = min(max_left, max_right) - height[i]

# ----- Approach 1: Prefix / Suffix arrays -----
def trap_water_arrays(height: List[int]) -> int:
    n = len(height)
    if n <= 2: return 0
    
    left_max = [0] * n
    right_max = [0] * n
    
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])
        
    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])
        
    total_water = 0
    for i in range(n):
        total_water += min(left_max[i], right_max[i]) - height[i]
        
    return total_water
# Time: O(n), Space: O(n)

# ----- Approach 2: Optimal (Two Pointers) -----
def trap_water_optimal(height: List[int]) -> int:
    n = len(height)
    if n <= 2: return 0
    
    left, right = 0, n - 1
    left_max, right_max = height[left], height[right]
    total_water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            total_water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            total_water += right_max - height[right]
            
    return total_water
# Time: O(n), Space: O(1)

# --- Practice Skeleton ---
def practice_trap_water(height: List[int]) -> int:
    pass

# =============================================================================
# DRIVER CODE FOR TESTING SKELETONS
# =============================================================================
if __name__ == "__main__":
    print("Testing 09_Two_Pointers_and_Window_Patterns skeletons...")
    
    print("Target Sum Pair:", practice_target_sum_pair([1, 2, 3, 4, 5, 6], 7))
    print("Max Area:", practice_max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))
    print("Merge Sorted:", practice_merge_sorted_arrays([1, 3, 5], [2, 4, 6]))
    
    nums = [1, 1, 2, 2, 3]
    length = practice_remove_duplicates(nums)
    print("Remove Duplicates:", length, "->", nums[:length] if length is not None else None)
    
    print("Trap Water:", practice_trap_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
