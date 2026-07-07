###############################################################################
#               04 - Bitwise Operations and Logic Gates                       #
###############################################################################

from typing import List

# =============================================================================
# SECTION 1: Basic Bitwise Operators
# =============================================================================

def bitwise_basics():
    a = 5  # 101 in binary
    b = 3  # 011 in binary
    
    print(f"a = {a} (bin: {bin(a)})")
    print(f"b = {b} (bin: {bin(b)})")
    
    # AND
    print(f"a & b = {a & b} (bin: {bin(a & b)})")  # 101 & 011 = 001 (1)
    
    # OR
    print(f"a | b = {a | b} (bin: {bin(a | b)})")  # 101 | 011 = 111 (7)
    
    # XOR
    print(f"a ^ b = {a ^ b} (bin: {bin(a ^ b)})")  # 101 ^ 011 = 110 (6)
    
    # NOT
    print(f"~a = {~a} (bin: {bin(~a)})")        # ~101 = -110 (-6)
    
    # Shifts
    print(f"a << 1 = {a << 1} (Multiply by 2)") # 1010 (10)
    print(f"a >> 1 = {a >> 1} (Divide by 2)")   # 010 (2)

# =============================================================================
# SECTION 2: Bitwise Tricks and Patterns
# =============================================================================

def is_even_bitwise(n: int) -> bool:
    # If the least significant bit is 0, the number is even.
    # e.g., 4 is 100 (LSB is 0). 4 & 1 == 0
    return (n & 1) == 0

def find_single_number(nums: List[int]) -> int:
    """
    Given a non-empty array of integers where every element appears twice 
    except for one. Find that single one.
    """
    # XOR cancels out duplicates. 
    # A ^ A = 0
    # 0 ^ B = B
    res = 0
    for n in nums:
        res ^= n
    return res

def count_set_bits(n: int) -> int:
    """
    Count the number of '1's in the binary representation of n (Hamming Weight).
    """
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def count_set_bits_brian_kernighan(n: int) -> int:
    """
    Optimized: n & (n - 1) flips the lowest set bit to 0.
    Iterates only as many times as there are set bits.
    """
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count


# --- Practice Skeletons ---

def practice_is_power_of_two(n: int) -> bool:
    """ 
    Return True if n is a power of 2. 
    Hint: Think about what `n & (n - 1)` does. 
    """
    pass

def practice_missing_number(nums: List[int]) -> int:
    """
    Given an array containing n distinct numbers taken from 0, 1, 2, ..., n,
    find the one that is missing from the array using XOR.
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    print("--- Bitwise Basics ---")
    bitwise_basics()
    
    print("\n--- Bitwise Tricks ---")
    print("Is 10 even?", is_even_bitwise(10))
    print("Is 7 even?", is_even_bitwise(7))
    print("Single Number in [4, 1, 2, 1, 2]:", find_single_number([4, 1, 2, 1, 2]))
    
    print("\n--- Counting Set Bits ---")
    print("Set bits in 11 (1011):", count_set_bits(11))
    print("Set bits in 11 (Kernighan):", count_set_bits_brian_kernighan(11))
    
    print("\n--- Practice Skeletons ---")
    print("Is 16 power of two?", practice_is_power_of_two(16))
    print("Missing number in [3, 0, 1]:", practice_missing_number([3, 0, 1]))
