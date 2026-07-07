###############################################################################
#                 08 - Core Array & Hashing Problems                  #
###############################################################################

from typing import List
from collections import defaultdict

# =============================================================================
# SECTION 1: Reverse an Array
# =============================================================================

# ----- Approach 1: Brute Force (Create a new array) -----
def reverse_array_brute(arr: List[int]) -> List[int]:
    n = len(arr)
    ans = [0] * n
    for i in range(n):
        ans[n - 1 - i] = arr[i]
    return ans

# Time: O(n)
# Space: O(n) - creates a new array

# ----- Approach 2: Optimal (Two Pointers In-Place) -----
def reverse_array_optimal(arr: List[int]) -> None:
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        arr[lo], arr[hi] = arr[hi], arr[lo]
        lo += 1
        hi -= 1

# Time: O(n) - we do n/2 swaps
# Space: O(1) - modifies array in place

# --- Practice Skeleton ---
def practice_reverse_array(arr: List[int]) -> None:
    pass


# =============================================================================
# SECTION 2: Rotate Array by K steps
# =============================================================================

# ----- Approach 1: Brute Force (Rotate 1 by 1, K times) -----
def rotate_array_brute(arr: List[int], k: int) -> None:
    n = len(arr)
    if n == 0: return
    k = k % n
    for _ in range(k):
        # Shift all elements right by 1
        last = arr[-1]
        for i in range(n - 1, 0, -1):
            arr[i] = arr[i - 1]
        arr[0] = last

# Time: O(n * k) - TLE for large k
# Space: O(1)

# ----- Approach 2: Optimal (Reverse portions) -----
# Trick: Reverse whole array, then reverse first k elements, then reverse remaining n-k elements.
def rotate_array_optimal(arr: List[int], k: int) -> None:
    n = len(arr)
    if n == 0: return
    k = k % n
    
    def reverse(lo: int, hi: int):
        while lo < hi:
            arr[lo], arr[hi] = arr[hi], arr[lo]
            lo += 1
            hi -= 1
            
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)

# Time: O(n)
# Space: O(1)

# --- Practice Skeleton ---
def practice_rotate_array(arr: List[int], k: int) -> None:
    pass


# =============================================================================
# SECTION 3: Two Sum (Return Indices)
# =============================================================================

# ----- Approach 1: Brute Force -----
def two_sum_brute(arr: List[int], target: int) -> List[int]:
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return [i, j]
    return []

# Time: O(n^2)
# Space: O(1)

# ----- Approach 2: Optimal (Hash Map) -----
# Optimization Logic: Instead of checking every pair, we can iterate through the array once.
# For each number, we calculate the `complement` needed to reach the target (target - current).
# We check if this complement exists in our Hash Map. 
#   - If YES: We found our pair! Return the current index and the complement's index.
#   - If NO: We store the current number and its index in the Hash Map to be checked later.
def two_sum_optimal(arr: List[int], target: int) -> List[int]:
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Time: O(n) - Single pass, O(1) dict lookups
# Space: O(n) - To store up to n elements in dict

# --- Practice Skeleton ---
def practice_two_sum(arr: List[int], target: int) -> List[int]:
    pass


# =============================================================================
# SECTION 4: Contains Duplicate
# =============================================================================

# ----- Approach 1: Brute Force -----
def contains_duplicate_brute(nums: List[int]) -> bool:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True
    return False
# Time: O(n^2)

# ----- Approach 2: Sorting -----
def contains_duplicate_sorting(nums: List[int]) -> bool:
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return True
    return False
# Time: O(n log n), Space: O(1) or O(n) depending on sort

# ----- Approach 3: Optimal (Hash Set) -----
# Optimization Logic: A Hash Set provides O(1) average time complexity for lookups.
# As we iterate, we check if the current number is already in the set.
#   - If YES: We found a duplicate! Return True.
#   - If NO: Add the number to the set and continue.
def contains_duplicate_optimal(nums: List[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Time: O(n)
# Space: O(n)

# --- Practice Skeleton ---
def practice_contains_duplicate(nums: List[int]) -> bool:
    pass


# =============================================================================
# SECTION 5: Find the Duplicate Number (in array of 1 to n)
# =============================================================================
# Array of n+1 integers where each is in range [1, n]. There is exactly ONE duplicate.

# ----- Approach 1: Intermediate (Hash Set) -----
# Optimization Logic: Use a Hash Set to track seen numbers.
# If a number is already in the set, that is the duplicate.
def find_duplicate_hash_set(nums: List[int]) -> int:
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)

# Time: O(n)
# Space: O(n) - requires extra memory for the set.

# ----- Approach 2: Modifying array in-place (Index Mapping) -----
# Swap elements to their correct index (value i goes to index i).
# This gives O(1) space, but modifies the input array.
def find_duplicate_optimal(nums: List[int]) -> int:
    while True:
        x = nums[0]
        if nums[x] == x:
            return x
        # Swap x to its correct position
        nums[0], nums[x] = nums[x], nums[0]

# Time: O(n)
# Space: O(1) (but modifies the array)

# --- Practice Skeleton ---
def practice_find_duplicate(nums: List[int]) -> int:
    pass


# =============================================================================
# SECTION 6: Longest Consecutive Sequence
# =============================================================================

# ----- Approach 1: Sorting -----
def longest_consecutive_sorting(nums: List[int]) -> int:
    if not nums: return 0
    nums.sort()
    longest = 1
    current_streak = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            continue
        elif nums[i] == nums[i - 1] + 1:
            current_streak += 1
        else:
            longest = max(longest, current_streak)
            current_streak = 1
    return max(longest, current_streak)

# Time: O(n log n)

# ----- Approach 2: Optimal (Hash Set) -----
# Optimization Logic: Convert the list to a Hash Set for O(1) lookups.
# To avoid redundant work, we only start counting a sequence if the current `num` is the START.
# How do we know it's the start? If `num - 1` does NOT exist in the set!
def longest_consecutive_optimal(nums: List[int]) -> int:
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Check if it's the start of a sequence
        if (num - 1) not in num_set:
            length = 1
            while (num + length) in num_set:
                length += 1
            longest = max(longest, length)
            
    return longest

# Time: O(n) - We only run the while loop for sequence starters
# Space: O(n) - To store the set

# --- Practice Skeleton ---
def practice_longest_consecutive(nums: List[int]) -> int:
    pass


# =============================================================================
# SECTION 7: Longest Palindrome (from Characters)
# =============================================================================

# Given a string s, find the length of the longest palindrome that can be built.
def longest_palindrome_optimal(s: str) -> int:
    seen = set()
    ans = 0
    
    for ch in s:
        if ch in seen:
            ans += 2
            seen.remove(ch)
        else:
            seen.add(ch)
            
    if len(seen) > 0:
        ans += 1
        
    return ans

# Time: O(n)
# Space: O(1) - alphabet size is limited (max 52 for a-zA-Z)

# --- Practice Skeleton ---
def practice_longest_palindrome(s: str) -> int:
    pass


# =============================================================================
# SECTION 8: Product of Array Except Self
# =============================================================================

# ----- Approach 1: Division (Often disallowed) -----
def product_except_self_division(nums: List[int]) -> List[int]:
    prod = 1
    zero_count = 0
    for num in nums:
        if num == 0:
            zero_count += 1
        else:
            prod *= num
            
    ans = [0] * len(nums)
    if zero_count > 1:
        return ans
    
    for i in range(len(nums)):
        if zero_count == 1:
            ans[i] = prod if nums[i] == 0 else 0
        else:
            ans[i] = prod // nums[i]
    return ans
# Time: O(n), Space: O(1)

# ----- Approach 2: Optimal (Prefix & Suffix Products) -----
def product_except_self_optimal(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [1] * n
    
    # Pass 1: Build Prefix Products
    prefix = 1
    for i in range(n):
        ans[i] = prefix
        prefix *= nums[i]
        
    # Pass 2: Multiply by Suffix Products
    postfix = 1
    for i in range(n - 1, -1, -1):
        ans[i] *= postfix
        postfix *= nums[i]
        
    return ans

# Time: O(n)
# Space: O(1) - output array is generally not considered extra space

# --- Practice Skeleton ---
def practice_product_except_self(nums: List[int]) -> List[int]:
    pass

# =============================================================================
# DRIVER CODE FOR TESTING SKELETONS
# =============================================================================
if __name__ == "__main__":
    print("Testing 08_Core_Array_and_Hashing_Problems skeletons...")
    
    arr = [1, 2, 3]
    practice_reverse_array(arr)
    print("Reverse:", arr)
    
    arr = [1, 2, 3, 4, 5]
    practice_rotate_array(arr, 2)
    print("Rotate:", arr)
    
    print("Two Sum:", practice_two_sum([2, 7, 11, 15], 9))
    print("Contains Duplicate:", practice_contains_duplicate([1, 2, 3, 1]))
    print("Find Duplicate:", practice_find_duplicate([1, 3, 4, 2, 2]))
    print("Longest Consecutive:", practice_longest_consecutive([100, 4, 200, 1, 3, 2]))
    print("Longest Palindrome:", practice_longest_palindrome("abccccdd"))
    print("Product Except Self:", practice_product_except_self([1, 2, 3, 4]))
