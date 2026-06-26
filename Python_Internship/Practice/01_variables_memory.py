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
# WHY DOES THIS MATTER?
#   Understanding memory helps you avoid bugs with mutable objects (like lists)
#   and understand why "is" and "==" behave differently (covered in file 02).
#
# TIME COMPLEXITY: All operations here are O(1) - constant time.
# SPACE COMPLEXITY: O(1) - we store a single integer.
# =============================================================================

import time  # Built-in module for time-related functions

pid = 1001
print("Product_id is:", pid)
print()

# id() returns the memory address where the object `pid` points to is stored.
# This address is an integer and is unique for each object currently in memory.
# NOTE: The exact address changes every time you run the program because the
# operating system assigns memory dynamically.
print("Memory_Address is:", id(pid))
print()

# time.sleep(seconds) pauses (blocks) the program for the given number of
# seconds. The program literally does nothing during this time.
# USE CASES:
#   - Adding delays between API calls to avoid rate limiting
#   - Creating countdowns or timed events
#   - Simulating processing time in demos
# Here we pause for 2 seconds before printing the final message.
time.sleep(2)
print("End of an application")

# =============================================================================
# QUICK EXPERIMENTS TO TRY:
# =============================================================================
# 1. Try: print(id(1001)) and compare with id(pid). Are they the same?
#    (They might not be -- Python may create a new object for the literal 1001)
#
# 2. Try assigning two variables to the same value:
#       a = 100
#       b = 100
#       print(id(a), id(b))   # Same address! Python caches small integers.
#
# 3. Try with a larger number:
#       a = 1000
#       b = 1000
#       print(id(a), id(b))   # May be different addresses!
#    (Python only caches integers from -5 to 256 -- more on this in file 02)
# =============================================================================
