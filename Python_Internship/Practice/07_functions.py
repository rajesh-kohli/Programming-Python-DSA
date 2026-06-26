# =============================================================================
# FUNCTIONS IN PYTHON
# =============================================================================
# Writing code in either Functions or Classes is the right way to write code.
# A Function is a block of code with a set of instructions to perform a
# particular task.
#
# Example: Task - Calculator
#   Create different functions: add(), sub(), mul(), div()
#   Each function handles one specific operation.


# =============================================================================
# SECTION 1: Why Functions Matter
# =============================================================================
# 1. MODULARITY: Break a big program into small, manageable pieces.
#    Instead of one giant script, you have small, focused functions.
#    This makes code easier to understand, debug, and maintain.
#
# 2. REUSABILITY: Write once, call many times. Instead of copy-pasting
#    the same 10 lines of code in 5 places, put them in a function
#    and call it 5 times. If you need to fix a bug, fix it in one place.
#
# 3. READABILITY: Good function names act as documentation.
#    calculate_tax(income) is clearer than 20 lines of math.
#
# 4. TESTING: Small functions are easier to test individually.
#    You can verify each piece works before combining them.
#
# 5. ABSTRACTION: Hide the complex details inside a function.
#    The caller doesn't need to know HOW it works, just WHAT it does.


# =============================================================================
# SECTION 2: Function Syntax
# =============================================================================
# Syntax:
#     def function_name(parameters):
#         function body
#         return value        # optional
#
# Components:
#   def            --> keyword that tells Python "I'm defining a function"
#   function_name  --> identifier (follows same naming rules as variables)
#   parameters     --> inputs the function needs (optional -- can be empty)
#   function_body  --> the instructions inside the function (indented)
#   return         --> sends a value back to the caller (optional)
#
# To execute a function, you must CALL it:
#     function_name(arguments)
#
# IMPORTANT: Parameters vs Arguments
#   - PARAMETERS are the variable names in the function DEFINITION
#     (they're placeholders)
#   - ARGUMENTS are the actual values you pass when CALLING the function
#
#   def greet(name):      # 'name' is a PARAMETER
#       print(f"Hi {name}")
#
#   greet("Alice")        # "Alice" is an ARGUMENT


# =============================================================================
# SECTION 3: Basic Function -- No Parameters, No Return
# =============================================================================

# Function Definition -- this only DEFINES the function, it does NOT run it
def my_function():
    print("Printing my function")

# Function Calling -- this actually EXECUTES the function
my_function()
# Output: Printing my function

# You can call a function as many times as you want (reusability!)
# my_function()  # Would print again
# my_function()  # And again


# =============================================================================
# SECTION 4: Function with Parameters
# =============================================================================
# Parameters let you pass data INTO a function so it can work with
# different inputs each time.

# Example - addition of two numbers
def add(a, b):         # a and b are PARAMETERS (part of the definition)
    sum = a + b
    print(sum)

add(112, 123)          # 112 and 123 are ARGUMENTS (actual values)
# Output: 235

# There is no priority attached to a function. Whichever function is
# called will be executed. Functions are just defined -- they sit idle
# until you call them.


# =============================================================================
# SECTION 5: The return Statement
# =============================================================================
# `return` sends a value BACK to the place where the function was called.
#
# KEY DIFFERENCE: print() vs return
# ---------------------------------
# print() displays text on the screen -- it's for HUMANS to read.
# return sends a value back to the PROGRAM -- it's for CODE to use.
#
# Example to illustrate the difference:
#
#   def add_print(a, b):
#       print(a + b)       # Shows "7" on screen, but returns None
#
#   def add_return(a, b):
#       return a + b        # Sends 7 back to the caller
#
#   result1 = add_print(3, 4)   # Prints "7", but result1 is None!
#   result2 = add_return(3, 4)  # result2 is 7 -- you can use it later
#
#   # This fails with print version:
#   # total = add_print(3, 4) + add_print(5, 6)  # None + None = ERROR!
#
#   # This works with return version:
#   # total = add_return(3, 4) + add_return(5, 6)  # 7 + 11 = 18
#
# RULE OF THUMB: Use return for computation, use print for display.
# A function that computes something should almost always return it.

# What happens when a function has no return statement?
# It returns None automatically.
#
#   def say_hello():
#       print("Hello!")
#
#   result = say_hello()   # Prints "Hello!", result is None
#   print(result)          # Output: None
#   print(type(result))    # Output: <class 'NoneType'>


# =============================================================================
# SECTION 6: Functions Calling Other Functions (Call Stack)
# =============================================================================
# Functions can call other functions! When this happens, Python uses a
# "call stack" to keep track of where it is.
#
# Think of it like a stack of plates:
#   - When you call a function, you put a plate on top
#   - When a function returns, you remove the plate from the top
#   - You always work with the top plate (most recent function call)

def func1(a, b):
    ans = func2(3, 4)       # func1 pauses here, calls func2
    # print(ans)             # ans would be 7 (return value of func2)
    return a + b

def func2(x, y):
    return x + y

print(func1(5, 6))
# Output: 11

# CALL STACK TRACE for func1(5, 6):
# -------------------------------------------------------
# Step 1: main calls func1(5, 6)
#         Stack: [main, func1(a=5, b=6)]
#
# Step 2: func1 calls func2(3, 4)
#         Stack: [main, func1(a=5, b=6), func2(x=3, y=4)]
#         func1 is PAUSED waiting for func2 to finish
#
# Step 3: func2 returns 3 + 4 = 7
#         Stack: [main, func1(a=5, b=6)]
#         ans = 7 in func1
#
# Step 4: func1 returns 5 + 6 = 11
#         Stack: [main]
#         (note: ans=7 is computed but never used in the return)
#
# Step 5: print(11) displays "11"
# -------------------------------------------------------


# =============================================================================
# SECTION 7: More Complex Function Composition
# =============================================================================

def fun1(a, b):
    fun2(5, 6)          # Calls fun2, but DISCARDS the return value!
    x = fun3()          # Calls fun3, stores return value in x (x = 5)
    return a + b * b    # Note: b*b is computed first (multiplication before addition)
                        # So this is a + (b*b), NOT (a+b) * b

def fun2(p, q):
    return p + q - 2    # Returns 5 + 6 - 2 = 9, but nobody uses it!

def fun3():
    return 5

result = fun1(6, 7)
# Output: fun1 returns 6 + 7*7 = 6 + 49 = 55
# But result is not printed! (see note below)

# CALL STACK TRACE for fun1(6, 7):
# -------------------------------------------------------
# Step 1: main calls fun1(6, 7)
#         Stack: [main, fun1(a=6, b=7)]
#
# Step 2: fun1 calls fun2(5, 6)
#         Stack: [main, fun1(a=6, b=7), fun2(p=5, q=6)]
#
# Step 3: fun2 returns 5 + 6 - 2 = 9
#         Stack: [main, fun1(a=6, b=7)]
#         Return value 9 is DISCARDED (not stored in any variable)
#
# Step 4: fun1 calls fun3()
#         Stack: [main, fun1(a=6, b=7), fun3()]
#
# Step 5: fun3 returns 5
#         Stack: [main, fun1(a=6, b=7)]
#         x = 5 in fun1 (but x is never used in the return!)
#
# Step 6: fun1 returns 6 + 7*7 = 6 + 49 = 55
#         Stack: [main]
#         result = 55
# -------------------------------------------------------
#
# OBSERVATION: fun2's return value is thrown away, and x from fun3 is
# never used in the final computation. This is likely unintentional --
# in real code, if you call a function but ignore its return value,
# ask yourself: "Why am I calling this?"

# Let's print the result so we can see it:
print(f"fun1(6, 7) = {result}")
# Output: fun1(6, 7) = 55


# =============================================================================
# SECTION 8: Key Takeaways
# =============================================================================
# 1. Define a function with `def`, call it by name with parentheses.
#
# 2. Parameters (in definition) vs Arguments (in call):
#       def add(a, b):    <-- a, b are parameters
#       add(3, 5)         <-- 3, 5 are arguments
#
# 3. return vs print:
#       return --> gives a value back to the code (for computation)
#       print  --> shows text on screen (for humans)
#       A function without return implicitly returns None.
#
# 4. Call stack: Python tracks function calls in a stack (LIFO).
#    When function A calls function B, A pauses until B returns.
#
# 5. Common beginner mistake: forgetting to use the return value.
#       def double(x):
#           return x * 2
#       double(5)          # This computes 10 but throws it away!
#       result = double(5) # This stores 10 in result -- correct!
#       print(double(5))   # This prints 10 -- also correct!
