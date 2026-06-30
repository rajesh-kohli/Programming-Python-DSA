"""
Lecture 11: Exception Handling
===============================
Topics Covered:
  - What are exceptions and why we handle them
  - try / except / else / finally flow
  - Handling file errors, list index errors, dictionary key errors
  - Specific vs bare (generic) except clauses
  - The "with" statement for safe file handling
"""

# =============================================================================
# SECTION 1: What Are Exceptions?
# =============================================================================
#
# An EXCEPTION is an error that occurs during program execution (at runtime).
# Without handling, an exception crashes your program immediately.
#
# Common exception types:
#   FileNotFoundError  -- Trying to open a file that doesn't exist
#   IndexError         -- Accessing a list index that is out of range
#   KeyError           -- Accessing a dictionary key that doesn't exist
#   ValueError         -- Passing the wrong type of value (e.g., int("abc"))
#   TypeError          -- Performing an operation on incompatible types
#   ZeroDivisionError  -- Dividing by zero
#   NameError          -- Using a variable that hasn't been defined
#
# WHY handle exceptions?
# - Prevent your program from crashing unexpectedly
# - Give the user a helpful error message instead of a scary traceback
# - Allow the program to recover and continue running
# - Handle predictable problems gracefully (file missing, bad input, etc.)
#
# Mental model -- exceptions form a TREE (a small slice of it shown here):
#
#                     BaseException
#                           |
#                       Exception
#              /            |             \
#       ArithmeticError  LookupError    ValueError   TypeError
#             |             /    \
#    ZeroDivisionError  IndexError  KeyError
#
#   `except Exception` catches ValueError, TypeError, LookupError and all
#   their children (IndexError, KeyError, ...) -- but NOT KeyboardInterrupt
#   or SystemExit, which live directly under BaseException, outside Exception.
#   This is exactly why a bare "except:" (which catches BaseException) is
#   more dangerous than "except Exception:" -- see Section 6 below.

# =============================================================================
# SECTION 2: The try / except / else / finally Flow
# =============================================================================
#
# The full structure looks like this:
#
#   try:
#       # Code that MIGHT raise an exception
#       # If an exception occurs here, Python jumps to the matching except block
#   except SpecificError:
#       # Runs ONLY if SpecificError was raised in the try block
#   except AnotherError:
#       # Runs ONLY if AnotherError was raised
#   else:
#       # Runs ONLY if NO exception was raised in the try block
#       # This is a good place for code that should only run on success
#   finally:
#       # ALWAYS runs, whether an exception occurred or not
#       # Perfect for cleanup: closing files, database connections, etc.
#
# Execution flow:
#   1. Python tries to execute the code in the "try" block
#   2. If NO error  -->  skip "except", run "else", then run "finally"
#   3. If an error  -->  run matching "except", skip "else", then run "finally"
#
# Mental model -- two possible paths through the block, "finally" is the
# only stop both paths always pass through:
#
#   SUCCESS PATH:   try (no error) -----> else -----> finally
#                          |
#   EXCEPTION PATH: try (error!) --> matching except --------> finally
#                                          |
#                          (else is SKIPPED on this path)
#
#   No matter which path is taken, "finally" runs at the end -- that's
#   what makes it the right place for cleanup (closing files, releasing
#   locks/connections) that must happen whether or not things went wrong.

# =============================================================================
# SECTION 3: Handling File Errors
# =============================================================================

## Exception Handling

# Example 1: Catching a FileNotFoundError
# We try to open "magic.txt" which doesn't exist. Instead of crashing,
# we catch the error and print a friendly message.

try:
    f = open("magic.txt", "r")  ## this file doesn't exist, so except would run
    print(f.read())
    f.close()
except FileNotFoundError:
    # BEST PRACTICE: Catch the specific exception type you expect.
    # FileNotFoundError is raised when the file doesn't exist.
    print("File not present in directory")

# NOTE: The above uses a specific exception type (FileNotFoundError).
# The original code used a bare "except:" which is bad practice (see Section 6).

# BETTER APPROACH: Use the "with" statement so you don't need to manually close:
#
# try:
#     with open("magic.txt", "r") as f:
#         print(f.read())
# except FileNotFoundError:
#     print("File not present in directory")
#
# With the "with" statement, f.close() is called automatically, even if
# an error occurs inside the block. This is called a "context manager."

# =============================================================================
# SECTION 4: Handling List Index Errors
# =============================================================================

# write an exception handling code which handle list index error

lst = [10, 20, 30]

# The list has indices 0, 1, 2 (and -1, -2, -3 for reverse).
# Accessing lst[5] would raise an IndexError because index 5 doesn't exist.
# Time complexity of list indexing: O(1) -- direct access by position

try:
    # print(lst[5])
    index = int(input("Enter the index of element: "))
    print(lst[index])
except IndexError:
    # IndexError is raised when you try to access an index beyond the list length
    print("The list index is not present, out of range")
except ValueError:
    # ValueError is raised if the user types something that isn't a number
    # e.g., typing "abc" when we expect an integer
    print("Please enter a valid integer")

# =============================================================================
# SECTION 5: Handling Dictionary Key Errors
# =============================================================================

## dictionary:
employee_info = {
    "mayur": 10000,
    "abc": 20000,
    "pqr": 3000
}

# Time complexity of dictionary lookup: O(1) average case (hash table)
# KeyError is raised when you try to access a key that doesn't exist in the dict.

# -------------------------------------------------------------------------
# BUG FIX (original line 29):
#   Original:  name = input("Enter the name of the employee".lower)
#
#   TWO bugs here:
#   1. ".lower" is missing parentheses -- it should be ".lower()" to CALL the method.
#      Without (), you're just referencing the method object, not calling it.
#      input() would receive something like "<built-in method lower of str object>"
#   2. ".lower" / ".lower()" is being called on the STRING LITERAL
#      "Enter the name of the employee", not on the user's INPUT.
#      We want to lowercase what the user types, not the prompt text.
#
#   Fix: Move .lower() AFTER input() so it applies to the user's response.
#         input("Enter the name of the employee: ").lower()
# -------------------------------------------------------------------------

try:
    name = input("Enter the name of the employee: ").lower()  # BUG FIXED
    print(employee_info[name])
except KeyError:
    # KeyError is raised when the key doesn't exist in the dictionary
    print("The employee is not present")
finally:
    # The "finally" block ALWAYS executes, no matter what.
    # Common uses: closing files, releasing resources, logging
    print("Execution done")

# =============================================================================
# SECTION 6: Why Bare "except:" Is Bad Practice
# =============================================================================
#
# A bare "except:" (with no exception type) catches EVERYTHING, including:
#   - KeyboardInterrupt (Ctrl+C) -- user trying to stop the program
#   - SystemExit -- program trying to exit normally
#   - MemoryError -- system running out of memory
#
# This makes debugging very hard because you can't tell what went wrong.
#
# BAD:
#   try:
#       do_something()
#   except:                    # Catches EVERYTHING -- even Ctrl+C!
#       print("error")
#
# GOOD:
#   try:
#       do_something()
#   except (ValueError, KeyError) as e:   # Catch only what you expect
#       print(f"Error: {e}")
#
# If you truly need to catch all "normal" exceptions, use Exception:
#   except Exception as e:    # Catches all exceptions EXCEPT KeyboardInterrupt
#       print(f"Unexpected error: {e}")
#
# The "as e" part stores the exception object in variable e, so you can
# print or log the actual error message for debugging.
#
# Mental model -- how wide a net each except clause casts (narrow to wide):
#
#   except FileNotFoundError:   [.]              narrowest -- one error type
#   except (ValueError, KeyError):  [. .]         two specific types
#   except Exception:            [. . . . . .]    almost everything (no Ctrl+C)
#   except:  (bare)        [. . . . . . . . . .]  EVERYTHING, incl. Ctrl+C/exit
#
#   Prefer the narrowest net that still covers what you actually expect --
#   it's the difference between a helpful error message and silently
#   swallowing a bug (or worse, eating the user's Ctrl+C).

# =============================================================================
# SECTION 7: The "with" Statement (Context Manager)
# =============================================================================
#
# The "with" statement is the PREFERRED way to work with files in Python.
# It automatically handles closing the file, even if an exception occurs.
#
# Without "with" (manual close -- easy to forget, especially if errors occur):
#   f = open("data.txt", "r")
#   try:
#       data = f.read()
#   finally:
#       f.close()
#
# With "with" (automatic close -- cleaner, safer):
#   with open("data.txt", "r") as f:
#       data = f.read()
#   # f is automatically closed here
#
# How it works:
#   1. "with" calls __enter__() on the file object when the block starts
#   2. The file object is assigned to the variable after "as"
#   3. When the block ends (normally or via exception), __exit__() is called
#   4. __exit__() closes the file for you
#
# You can even open multiple files at once:
#   with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
#       outfile.write(infile.read())
#
# Mental model -- "with" guarantees cleanup runs no matter what happens:
#
#   with open(...) as f:        __enter__() runs --> f is ready to use
#       data = f.read()         block runs (may raise an exception)
#   # block ends (normally OR via exception)
#                                __exit__() runs  --> f.close() guaranteed
#
#   This is the same safety "finally" gives you, but scoped automatically
#   to the resource -- no need to remember to write the finally yourself.

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
# 1. Use try/except to handle predictable runtime errors gracefully.
# 2. Always catch SPECIFIC exception types (FileNotFoundError, IndexError, etc.)
#    rather than using a bare "except:".
# 3. Use "else" for code that should only run when no exception occurred.
# 4. Use "finally" for cleanup code that must always run (close files, etc.).
# 5. Use the "with" statement for file operations -- it auto-closes files.
# 6. The "as e" syntax lets you capture the exception object for debugging.
# 7. .lower() needs parentheses to CALL the method -- .lower is just a reference.
