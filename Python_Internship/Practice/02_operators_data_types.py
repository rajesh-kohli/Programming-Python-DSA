# =============================================================================
# SECTION 1: Arithmetic and Assignment Operators
# =============================================================================
#
# Python supports standard arithmetic operators:
#   +   Addition          5 + 3  = 8
#   -   Subtraction       5 - 3  = 2
#   *   Multiplication    5 * 3  = 15
#   /   Division (float)  5 / 3  = 1.6667
#   //  Floor Division    5 // 3 = 1
#   %   Modulus           5 % 3  = 2
#   **  Exponentiation    5 ** 3 = 125
#
# COMPOUND ASSIGNMENT OPERATORS combine an operation with assignment:
#   +=   Add and assign        a += 5  is the same as  a = a + 5
#   -=   Subtract and assign   a -= 5  is the same as  a = a - 5
#   *=   Multiply and assign   a *= 5  is the same as  a = a * 5
#   &=   Bitwise AND and assign (explained below)
#
# All operations below are O(1) time and O(1) space.
# =============================================================================

a = 4
print(a)         # Output: 4

a += 5
print(a)         # Output: 9  (4 + 5 = 9)

# &= is the BITWISE AND assignment operator.
# It performs a bitwise AND between 'a' and the right operand, then assigns
# the result back to 'a'.
#
# HOW IT WORKS (step by step):
#   a = 9      -->  binary: 1001
#   a &= 4    means a = a & 4
#   a = 9 & 4 -->  1001 & 0100 = 0000 --> result is 0
#
# Bitwise AND: each bit is 1 only if BOTH corresponding bits are 1.
#   1 0 0 1   (9)
# & 0 1 0 0   (4)
# ---------
#   0 0 0 0   (0)
a &= 4
print(a)         # Output: 0


# =============================================================================
# SECTION 2: Membership Operators (in / not in)
# =============================================================================
#
# 'in'     --> Returns True if the value is found in the sequence
# 'not in' --> Returns True if the value is NOT found in the sequence
#
# Works with: lists, tuples, strings, sets, dicts (checks keys)
#
# TIME COMPLEXITY:
#   - Lists/Tuples: O(n) -- must scan elements one by one
#   - Sets/Dicts:   O(1) average -- uses hash table lookup
# =============================================================================

container = [3, 4, 5, 6, 7, 8, 10]
print(container)          # Output: [3, 4, 5, 6, 7, 8, 10]

# NOTE: These expressions evaluate to True/False but the results are not
# printed. To see them, wrap in print().
print(10 in container)    # Output: True  (10 is in the list)
print(9 in container)     # Output: False (9 is NOT in the list)
print(15 not in container)  # Output: True (15 is NOT in the list)


# =============================================================================
# SECTION 3: Identity Operator (is) vs Equality Operator (==)
# =============================================================================
#
# == (EQUALITY):  Checks if two variables have the SAME VALUE.
# is (IDENTITY):  Checks if two variables point to the SAME OBJECT in memory
#                 (i.e., same id()).
#
# CRITICAL CONCEPT -- Python Integer Caching:
# Python pre-creates and caches integer objects from -5 to 256.
# This is an optimization because these small integers are used so frequently.
# When you assign a = 5, Python doesn't create a new object -- it reuses the
# cached one. So any variable set to 5 will point to the SAME memory location.
#
# For integers OUTSIDE -5 to 256, Python MAY or MAY NOT create separate
# objects. The behavior can vary between interactive mode and script mode.
#
# RULE OF THUMB:
#   - Use == to compare VALUES  (almost always what you want)
#   - Use 'is' to compare with None:  if x is None
#   - Avoid using 'is' to compare integers or strings in general
# =============================================================================

a = b = 5
# Both a and b are assigned to 5. Since 5 is in the cached range (-5 to 256),
# they point to the EXACT SAME object in memory.
print(id(b))       # Memory address of b
print(id(a))       # Same memory address as b!
print(a is b)      # Output: True (same object)

a = b = 256
# 256 is the upper boundary of Python's integer cache.
# Still the same object.
print(a is b)      # Output: True

a = b = 257
# 257 is OUTSIDE the cache range. But because a and b are assigned in the
# SAME statement (a = b = 257), Python is smart enough to reuse the object.
print(a is b)      # Output: True (same statement optimization)
print(id(a))
print(id(b))       # Same id as a

a = 256
b = 257
# Different values, so obviously different objects.
print(a is b)      # Output: False
print(id(a))
print(id(b))

a = 260
b = 260
# Both are 260 (outside cache range), assigned in SEPARATE statements.
# In script mode, Python's compiler may still optimize and reuse the object.
# In interactive mode (REPL), these would likely be different objects.
print(a is b)      # Output: may be True in script, False in REPL
print(id(a))
print(id(b))


# =============================================================================
# SECTION 4: Data Types in Python
# =============================================================================
#
# Python has several built-in data types:
#
# NUMERIC TYPES:
#   int      - Whole numbers:     123, -45, 0
#   float    - Decimal numbers:   3.14, -0.5, 2.0
#   complex  - Complex numbers:   3+4j  (j is the imaginary unit, not i)
#
# TEXT TYPE:
#   str      - Strings:           "Hello", 'World'
#
# BOOLEAN TYPE:
#   bool     - True or False      (subclass of int: True==1, False==0)
#
# SEQUENCE TYPES:
#   list     - Ordered, MUTABLE:    [1, 2, 3]
#   tuple    - Ordered, IMMUTABLE:  (1, 2, 3)
#
# MAPPING TYPE:
#   dict     - Key-value pairs:     {"name": "Alice", "age": 25}
#
# SET TYPE:
#   set      - Unordered, unique:   {1, 2, 3}
#
# MUTABLE vs IMMUTABLE:
#   MUTABLE:   Can be changed after creation  --> list, dict, set
#   IMMUTABLE: Cannot be changed after creation --> int, float, str, tuple, bool
#
#   Why does this matter?
#   - If you pass a mutable object to a function, the function CAN modify it
#   - If you pass an immutable object, the function CANNOT modify the original
#   - Immutable objects are hashable and can be used as dictionary keys
# =============================================================================

a = 123
print(type(a))     # Output: <class 'int'>

a = 123.456
print(type(a))     # Output: <class 'float'>

a = "Hello"
print(type(a))     # Output: <class 'str'>

# NOTE: In Python, the imaginary unit is 'j', not 'i' (unlike math notation).
a = 3 + 4j
print(type(a))     # Output: <class 'complex'>

a = True
print(a)           # Output: True
print(type(a))     # Output: <class 'bool'>


# =============================================================================
# SECTION 5: Lists (Mutable, Ordered Sequences)
# =============================================================================
#
# Lists are ordered collections that can hold items of any type.
# They are MUTABLE -- you can add, remove, and change elements.
#
# Creating:   lst = [1, 2, 3]  or  lst = list()
# Indexing:   lst[0] = first element, lst[-1] = last element
# Slicing:    lst[1:3] = elements at index 1 and 2
#
# TIME COMPLEXITY:
#   Access by index:  O(1)
#   Search by value:  O(n)
#   Append:           O(1) amortized
#   Insert at index:  O(n)
#   Delete by index:  O(n)
# =============================================================================

lst1 = []
print(lst1)            # Output: []

lst2 = [3, 4, 5, 6]
print(lst2)            # Output: [3, 4, 5, 6]
print(type(lst2))      # Output: <class 'list'>

# Commented out because 'i' is not valid for imaginary numbers in Python
# (use 'j' instead). Example: [3+5j, 6+9j] would work.
#lst4 = [3+5j, 6+9i]
#print(lst4)
#print(type(lst4))

# Positive indexing starts at 0 from the left.
# Negative indexing starts at -1 from the right.
#   lst2 = [3, 4, 5, 6]
#   Index:  0  1  2  3
#   Neg:   -4 -3 -2 -1
print(lst2[3])         # Output: 6  (4th element, index 3)
print(lst2[-3])        # Output: 4  (3rd from the end)

lst1 = [1, 2, 3]
lst2 = [5, 6, 7]

print(lst1 + lst2)     # Output: [1, 2, 3, 5, 6, 7]  ##concatenate

# However these below operations are not possible
# lst1 - lst2     # TypeError: unsupported operand
# lst1 * lst2     # TypeError: unsupported operand
# lst1 / lst2     # TypeError: unsupported operand
# NOTE: lst1 * 3 IS valid -- it repeats the list: [1,2,3,1,2,3,1,2,3]

print(lst2)            # Output: [5, 6, 7]

# DEMONSTRATING MUTABILITY:
# Lists are mutable, so we can change individual elements.
lst2[1] = 1000
print(lst2)  # Output: [5, 1000, 7]
# list is mutable - you can change the elements of a list but can't do with Tuple


# =============================================================================
# SECTION 6: Tuples (Immutable, Ordered Sequences)
# =============================================================================
#
# Tuples are like lists, but IMMUTABLE -- once created, you cannot change them.
#
# Creating:  t = (1, 2, 3)  or  t = tuple([1, 2, 3])
# Indexing:  Same as lists -- t[0], t[-1], t[1:3]
#
# WHY USE TUPLES INSTEAD OF LISTS?
#   1. They're faster (slight performance gain)
#   2. They're safe from accidental modification
#   3. They can be used as dictionary keys (because they're hashable)
#   4. They signal "this data should not change"
#
# TIME COMPLEXITY: Same as lists for access/search.
# =============================================================================

t1 = ()
print(t1)              # Output: ()
print(type(t1))        # Output: <class 'tuple'>

t2 = (2, 3, 4, 5)
print(t2)              # Output: (2, 3, 4, 5)
print(type(t2))        # Output: <class 'tuple'>

t3 = (2.5, 3.7, 4.8, 5.9)
print(t3)              # Output: (2.5, 3.7, 4.8, 5.9)
print(type(t3))        # Output: <class 'tuple'>

# Commented out: 'i' is not valid in Python for imaginary numbers (use 'j')
# t4 = (3+4j,4+2i)
# t2 = (2,3,4,5)
# print(t4)
# print(type(t4))

# Tuples can hold MIXED data types:
t5 = (1, 2, 4.5, "Hello", 6)
print(t5)              # Output: (1, 2, 4.5, 'Hello', 6)
print(type(t5))        # Output: <class 'tuple'>

# IMPORTANT: Trying to modify a tuple will raise a TypeError:
#   t5[0] = 100   -->  TypeError: 'tuple' object does not support item assignment


# =============================================================================
# SECTION 7: Sets and Dictionaries
# =============================================================================
#
# SETS:
#   - Unordered collection of UNIQUE elements
#   - Cannot contain duplicates
#   - Very fast membership testing: O(1) average for 'in'
#   - Creating: s = {1, 2, 3}  or  s = set([1, 2, 3])
#
# DICTIONARIES:
#   - Collection of key-value pairs
#   - Keys must be unique and immutable (str, int, tuple)
#   - Values can be anything
#   - Creating: d = {"key": "value"}  or  d = dict()
#   - Access: d["key"] or d.get("key")
#
# GOTCHA: {} creates an empty DICT, not an empty set!
#   - Empty set: set()
#   - Empty dict: {} or dict()
# =============================================================================

# CAUTION: This creates an empty DICTIONARY, not a set!
s1 = {}
print(s1)              # Output: {}
print(type(s1))        # Output: <class 'dict'>  <-- NOT set!

# To create an empty set, use: s1 = set()

# BUG FIX: The original code had:
#   print(dict_1 = {1:"Add", 2:"subtract"})
# This is a SyntaxError because you cannot put an assignment (=) inside print().
# Python thinks dict_1 is a keyword argument to print(), but print() has no
# such parameter. The fix is to separate the assignment and the print:
dict_1 = {1: "Add", 2: "subtract"}
print(dict_1)          # Output: {1: 'Add', 2: 'subtract'}

# =============================================================================
# SUMMARY TABLE: Mutable vs Immutable Types
# =============================================================================
#
#   Type      | Mutable? | Ordered? | Duplicates? | Example
#   ----------|----------|----------|-------------|--------------------
#   int       | No       | N/A      | N/A         | 42
#   float     | No       | N/A      | N/A         | 3.14
#   str       | No       | Yes      | Yes         | "hello"
#   bool      | No       | N/A      | N/A         | True
#   complex   | No       | N/A      | N/A         | 3+4j
#   list      | YES      | Yes      | Yes         | [1, 2, 3]
#   tuple     | No       | Yes      | Yes         | (1, 2, 3)
#   set       | YES      | No       | No          | {1, 2, 3}
#   dict      | YES      | Yes*     | Keys: No    | {"a": 1}
#
#   * Dicts are insertion-ordered since Python 3.7+
# =============================================================================
