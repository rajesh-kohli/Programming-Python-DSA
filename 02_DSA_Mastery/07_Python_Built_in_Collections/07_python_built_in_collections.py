###############################################################################
#                  07 - Python Built-in Collections                           #
###############################################################################

from typing import List, Tuple, Dict, Set

# =============================================================================
# SECTION 1: Lists & Slicing
# =============================================================================

def list_operations():
    arr = [10, 20, 30]
    
    # O(1) Operations
    arr.append(40)      # Add to end
    last = arr.pop()    # Remove from end
    val = arr[1]        # Lookup
    
    # O(N) Operations
    arr.insert(0, 5)    # Insert at beginning
    first = arr.pop(0)  # Remove from beginning
    arr.remove(20)      # Remove by value
    
    print(f"Final list: {arr}")

def list_slicing():
    arr = [0, 1, 2, 3, 4, 5, 6, 7]
    
    print("arr[2:5]   ->", arr[2:5])   # [2, 3, 4]
    print("arr[:3]    ->", arr[:3])    # [0, 1, 2]
    print("arr[5:]    ->", arr[5:])    # [5, 6, 7]
    print("arr[::-1]  ->", arr[::-1])  # Reverse
    print("arr[::2]   ->", arr[::2])   # Every 2nd element


# =============================================================================
# SECTION 2: Tuples
# =============================================================================

def tuple_operations():
    # Tuples are immutable
    tup = (1, 2, 3)
    
    # Packing and Unpacking
    a, b, c = tup
    print(f"Unpacked: a={a}, b={b}, c={c}")
    
    # Swapping variables uses tuple packing/unpacking under the hood
    a, b = b, a
    
    # Returning multiple values from a function
    def min_max(arr) -> Tuple[int, int]:
        return min(arr), max(arr)
        
    mini, maxi = min_max([10, 5, 20])
    print(f"Min: {mini}, Max: {maxi}")


# =============================================================================
# SECTION 3: Dictionaries (Hash Maps)
# =============================================================================

def dictionary_operations():
    # O(1) insertions and lookups
    hash_map = {"apple": 1, "banana": 2}
    
    # Insert / Update
    hash_map["orange"] = 3
    hash_map["apple"] = 5
    
    # Safe Lookup (avoid KeyError)
    count = hash_map.get("grape", 0) # Returns 0 if "grape" not found
    
    # Iterating
    print("Dictionary Iteration:")
    for key, val in hash_map.items():
        print(f"  {key}: {val}")


# =============================================================================
# SECTION 4: Sets (Hash Sets)
# =============================================================================

def set_operations():
    my_set = {1, 2, 3}
    
    # O(1) operations
    my_set.add(4)
    my_set.add(2) # Duplicate, ignored
    
    my_set.remove(4) # Throws KeyError if not found
    my_set.discard(10) # Safe remove, no error if not found
    
    # O(1) Lookup
    print("Is 3 in set?", 3 in my_set)
    
    # De-duplicating a list
    arr = [1, 1, 2, 2, 3, 3, 3]
    unique_arr = list(set(arr))
    print("Deduplicated array:", unique_arr)


# --- Practice Skeletons ---

def practice_frequency_counter(arr: List[int]) -> Dict[int, int]:
    """ 
    Return a dictionary where the keys are the elements of `arr`
    and the values are the number of times they appear.
    """
    pass

def practice_find_unique(arr: List[int]) -> List[int]:
    """
    Return a new list containing only the unique elements of `arr`.
    Order doesn't matter. Try doing it in O(N) time.
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    print("--- Lists ---")
    list_operations()
    list_slicing()
    
    print("\n--- Tuples ---")
    tuple_operations()
    
    print("\n--- Dictionaries ---")
    dictionary_operations()
    
    print("\n--- Sets ---")
    set_operations()
    
    print("\n--- Practice Skeletons ---")
    print("Frequencies:", practice_frequency_counter([1, 2, 2, 3, 3, 3]))
    print("Unique items:", practice_find_unique([1, 1, 2, 3, 3]))
