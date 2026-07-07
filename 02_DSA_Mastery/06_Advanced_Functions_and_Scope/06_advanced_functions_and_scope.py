###############################################################################
#                    06 - Advanced Functions and Scope                        #
###############################################################################

from typing import List

# =============================================================================
# SECTION 1: Arguments (*args and **kwargs)
# =============================================================================

def greet(greeting: str, name: str = "Guest"):
    """ Uses a default argument. """
    print(f"{greeting}, {name}!")

def sum_all(*args) -> int:
    """ *args collects arbitrary positional arguments into a tuple. """
    total = 0
    for num in args:
        total += num
    return total

def print_info(**kwargs):
    """ **kwargs collects arbitrary keyword arguments into a dictionary. """
    for key, value in kwargs.items():
        print(f"{key}: {value}")


# =============================================================================
# SECTION 2: Global vs Local Scope
# =============================================================================

global_counter = 0

def increment_global():
    """ 
    To modify a global variable, you MUST declare it global.
    Otherwise, Python creates a new local variable.
    """
    global global_counter
    global_counter += 1
    return global_counter

def read_global():
    """ To just read a global, no declaration is needed. """
    return global_counter


# =============================================================================
# SECTION 3: Nonlocal Scope (Crucial for Nested Functions/DFS)
# =============================================================================

def counter_factory():
    """ Demonstrates nonlocal keyword used in nested functions. """
    count = 0
    
    def increment():
        nonlocal count
        count += 1
        return count
        
    return increment


# =============================================================================
# SECTION 4: Lambda Functions & Sorting
# =============================================================================

def sort_by_length_and_alphabet():
    words = ["banana", "apple", "pear", "kiwi", "grape"]
    
    # Sort primarily by length (len(x)), secondarily alphabetically (x)
    words.sort(key=lambda x: (len(x), x))
    return words


# --- Practice Skeletons ---

def practice_filter_even_numbers(nums: List[int]) -> List[int]:
    """ 
    Use the built-in `filter()` function and a `lambda` to return only the 
    even numbers from the list.
    """
    pass

def practice_nested_dfs_simulation():
    """
    Create an outer function that initializes `total_sum = 0`.
    Create an inner function `add(n)` that adds `n` to `total_sum` using `nonlocal`.
    Call `add(5)` and `add(10)`, then return `total_sum`.
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    print("--- Arguments ---")
    greet("Hello")
    greet("Hi", "Alice")
    print("Sum all:", sum_all(1, 2, 3, 4, 5))
    print_info(role="Admin", level=99)
    
    print("\n--- Scope ---")
    print("Initial global:", read_global())
    increment_global()
    print("After increment:", read_global())
    
    print("\n--- Nonlocal ---")
    my_counter = counter_factory()
    print("Counter call 1:", my_counter())
    print("Counter call 2:", my_counter())
    
    print("\n--- Lambdas ---")
    print("Sorted words:", sort_by_length_and_alphabet())
    
    print("\n--- Practice Skeletons ---")
    print("Filter evens:", practice_filter_even_numbers([1, 2, 3, 4, 5, 6]))
    print("Nested DFS Sim:", practice_nested_dfs_simulation())
