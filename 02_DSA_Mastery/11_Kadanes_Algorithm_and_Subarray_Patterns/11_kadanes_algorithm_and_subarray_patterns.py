#             11 - Kadane's Algorithm and Subarray Patterns           #

from typing import List, Tuple

# =============================================================================
# SECTION 1: Generate All Subarrays
# =============================================================================

# ----- Approach: Brute Force -----
def generate_subarrays(arr: List[int]) -> None:
    n = len(arr)
    for i in range(n):
        for j in range(i, n):
            # arr[i:j+1] creates a new list (slice), which takes O(k) time
            print(arr[i:j+1])

# Time: O(n^3) - n^2 pairs, and O(n) average slice length
# Space: O(n) - temp array for the slice

# --- Practice Skeleton ---
def practice_generate_subarrays(arr: List[int]) -> None:
    pass


# =============================================================================
# SECTION 2: Prefix Sum
# =============================================================================

# ----- Approach: Optimal -----
def build_prefix_sum(arr: List[int]) -> List[int]:
    n = len(arr)
    if n == 0: return []
    
    prefix = [0] * n
    prefix[0] = arr[0]
    
    for i in range(1, n):
        prefix[i] = prefix[i - 1] + arr[i]
        
    return prefix

# Time: O(n)
# Space: O(n) - new prefix array

def range_query(prefix: List[int], i: int, j: int) -> int:
    if i == 0:
        return prefix[j]
    return prefix[j] - prefix[i - 1]

# Time: O(1) per query

# --- Practice Skeleton ---
def practice_build_prefix_sum(arr: List[int]) -> List[int]:
    pass


# =============================================================================
# SECTION 3: Maximum Subarray Sum
# =============================================================================

# ----- Approach 1: Brute Force -----
def max_subarray_sum_brute(arr: List[int]) -> int:
    n = len(arr)
    max_sum = float('-inf')
    
    for i in range(n):
        for j in range(i, n):
            current_sum = 0
            for k in range(i, j + 1):
                current_sum += arr[k]
            max_sum = max(max_sum, current_sum)
            
    return int(max_sum)
# Time: O(n^3)

# ----- Approach 2: Optimized Brute Force -----
def max_subarray_sum_opt_brute(arr: List[int]) -> int:
    n = len(arr)
    max_sum = float('-inf')
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j] # Extend previous sum
            max_sum = max(max_sum, current_sum)
            
    return int(max_sum)
# Time: O(n^2)

# ----- Approach 3: Prefix Sum -----
# sum(i, j) = prefix[j] - prefix[i-1]
# To maximize sum for a fixed j, we need the MINIMUM prefix[i-1] seen so far.
def max_subarray_sum_prefix(arr: List[int]) -> int:
    prefix = build_prefix_sum(arr)
    max_sum = float('-inf')
    min_prefix = 0 # sum of empty prefix
    
    for j in range(len(arr)):
        max_sum = max(max_sum, prefix[j] - min_prefix)
        min_prefix = min(min_prefix, prefix[j])
        
    return int(max_sum)
# Time: O(n), Space: O(n)

# ----- Approach 4: Kadane's Algorithm (Optimal) -----
# At each step, either extend the existing subarray sum, or start fresh.
def kadanes_algorithm(arr: List[int]) -> int:
    max_so_far = arr[0]
    x = arr[0] # Running sum ending at current index
    
    for i in range(1, len(arr)):
        x = max(x + arr[i], arr[i])
        max_so_far = max(max_so_far, x)
        
    return max_so_far
# Time: O(n), Space: O(1)

# --- Practice Skeleton ---
def practice_kadanes(arr: List[int]) -> int:
    pass


# =============================================================================
# SECTION 4: Kadane's returning the Subarray itself
# =============================================================================

def kadanes_with_subarray(arr: List[int]) -> Tuple[int, List[int]]:
    if not arr: return 0, []
    
    max_so_far = arr[0]
    x = arr[0]
    
    start = end = temp_start = 0
    
    for i in range(1, len(arr)):
        if arr[i] > x + arr[i]:
            x = arr[i]
            temp_start = i # Reset potential start
        else:
            x += arr[i]
            
        if x > max_so_far:
            max_so_far = x
            start = temp_start
            end = i
            
    return max_so_far, arr[start:end+1]


# =============================================================================
# SECTION 5: Maximum Circular Subarray Sum
# =============================================================================
# Elements can wrap around the end back to the start.

# Trick: 
# Case 1: Max subarray is NOT circular (standard Kadane's).
# Case 2: Max subarray IS circular. This means it wraps around.
#         If we find the MINIMUM contiguous subarray and subtract it from the
#         Total Sum of the array, we get the max circular subarray.
# Final Answer: max(Case 1, Total Sum - Min Subarray)
# Edge case: If all elements are negative, Total Sum == Min Subarray. 
#            Return Case 1.

def max_circular_subarray(arr: List[int]) -> int:
    def get_max_kadane(nums: List[int]) -> int:
        cur_max, global_max = nums[0], nums[0]
        for i in range(1, len(nums)):
            cur_max = max(cur_max + nums[i], nums[i])
            global_max = max(global_max, cur_max)
        return global_max

    def get_min_kadane(nums: List[int]) -> int:
        cur_min, global_min = nums[0], nums[0]
        for i in range(1, len(nums)):
            cur_min = min(cur_min + nums[i], nums[i])
            global_min = min(global_min, cur_min)
        return global_min

    total_sum = sum(arr)
    max_normal = get_max_kadane(arr)
    min_normal = get_min_kadane(arr)
    
    if max_normal < 0:
        return max_normal # All elements are negative
        
    return max(max_normal, total_sum - min_normal)

# Time: O(n)
# Space: O(1)

# --- Practice Skeleton ---
def practice_max_circular_subarray(arr: List[int]) -> int:
    pass


# =============================================================================
# DRIVER CODE FOR TESTING SKELETONS
# =============================================================================
if __name__ == "__main__":
    print("Testing 11_Kadanes_Algorithm_and_Subarray_Patterns skeletons...")
    
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print("Kadane's:", practice_kadanes(arr))
    
    circ_arr = [5, -3, 5]
    print("Max Circular Subarray:", practice_max_circular_subarray(circ_arr))
