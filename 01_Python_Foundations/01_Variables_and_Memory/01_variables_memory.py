# =============================================================================
# SECTION 1: Variables and Memory in Python
# =============================================================================
#
# WHAT IS A VARIABLE?
# -------------------
# A variable is a name (label) that refers to a value stored in memory.
# Think of it like a sticky note on a box: the sticky note is the variable
# name, and the box holds the actual data.
#
# In Python, variables do NOT store values directly. Instead, they store
# a REFERENCE (pointer) to an object in memory. When you write:
#     pid = 1001
# Python creates an integer object 1001 somewhere in memory, and the name
# "pid" points to that memory location.
#
# KEY CONCEPTS:
#   - id(variable)   --> Returns the memory address (identity) of the object
#                        the variable points to. Each object in memory has a
#                        unique id during its lifetime.
#   - type(variable) --> Returns the data type of the object.
#   - Every variable in Python is actually a reference to an object.
#
# MENTAL MODEL: name --> reference --> object in memory
# -------------------------------------------------------
#   pid = 1001
#
#       pid ----------> +--------+
#       (name)           | 1001   |  <- object in memory (has its own id())
#                         +--------+
#
# TIME COMPLEXITY: All operations here are O(1) - constant time.
# SPACE COMPLEXITY: O(1) - we store a single integer.
# =============================================================================

import time

if __name__ == "__main__":
    pid = 1001
    print(f"Product_id is: {pid}")
    # Output: Product_id is: 1001
    print()

    # id() returns the memory address where the object `pid` points to is stored.
    # This address is an integer and is unique for each object currently in memory.
    print(f"Memory_Address is: {id(pid)}")
    # Output: Memory_Address is: <some_integer>
    
    print(f"Type is: {type(pid)}")
    # Output: Type is: <class 'int'>
    print()

    # NOTE ON time.sleep():
    # time.sleep(seconds) pauses (blocks) the program for the given number of seconds.
    # USE CASES:
    #   - Adding delays between API calls to avoid rate limiting
    #   - Creating countdowns or timed events
    #   - Simulating processing time in demos
    # (Commented out to prevent blocking automated testing)
    # time.sleep(2)
    print("End of an application")

    # =============================================================================
    # QUICK EXPERIMENTS
    # =============================================================================
    print("\n--- CACHE EXPERIMENTS ---")

    # 1. Try assigning two variables to the same small value:
    a = 100
    b = 100
    print(f"a = 100, id(a): {id(a)}")
    print(f"b = 100, id(b): {id(b)}")
    print(f"Are they the same object? {a is b}")
    # Output: Are they the same object? True
    
    # VISUALIZING THE CACHE DIFFERENCE:
    #   Small ints (-5 to 256) are pre-built and SHARED:
    #       a = 100  ----\
    #                      >---> +-----+
    #       b = 100  ----/        | 100 |   <- ONE shared object, two arrows
    #                              +-----+

    print()

    # 2. Try with a larger number:
    x = 1000
    y = 1000
    print(f"x = 1000, id(x): {id(x)}")
    print(f"y = 1000, id(y): {id(y)}")
    # Note: Python's compiler might optimize `x=1000; y=1000` in the same block 
    # to share the same object, but theoretically they are separate objects outside the cache.
    
    #   Larger ints (outside the cache) get a fresh object EACH time:
    #       x = 1000 --------> +------+
    #                            | 1000 |   <- separate object
    #                            +------+
    #       y = 1000 --------> +------+
    #                            | 1000 |   <- another separate object
    #                            +------+

    # === PRACTICE ZONE ===
    # Experiment by creating lists and checking their ids!
    # list1 = [1, 2, 3]
    # list2 = [1, 2, 3]
    # print(id(list1) == id(list2)) # False! Lists are mutable and never cached.
