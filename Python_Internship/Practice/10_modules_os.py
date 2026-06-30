"""
Lecture 10: Modules and the OS Module
=====================================
Topics Covered:
  - What are Libraries, Packages, and Modules?
  - Importing modules (import, from...import, import...as)
  - The OS module: interacting with the operating system
  - The webbrowser module: opening URLs
  - Basic file reading with open()
"""

# =============================================================================
# SECTION 1: Library vs Package vs Module
# =============================================================================
#
# Python organizes code into a clear hierarchy:
#
#   LIBRARY (largest)
#   +-- contains multiple PACKAGES
#       +-- each package contains multiple MODULES
#           +-- each module is a single .py file
#
### Library
# - A collection of packages and modules
# - eg. Numpy, sklearn, tensorflow, pytorch
#
### Package
# - Collection of modules, but is organized in the form of directory
# - A package is a directory that contains an __init__.py file (can be empty)
# - pandas, matplotlib
#
### Modules
# - a single python file with .py extension
# - eg. math, os, time, etc.
#
# Think of it like this:
#   Library  = a whole bookshelf    (e.g., NumPy)
#   Package  = a single book        (e.g., numpy.random)
#   Module   = a chapter in a book  (e.g., numpy.random.mtrand)
#
#### There are two types of modules in Python:
# - Predefined module - already defined in the language (e.g., math, os, sys)
# - User defined module - any .py file you create can be imported as a module

# =============================================================================
# SECTION 2: Ways to Import Modules
# =============================================================================
#
# There are three main ways to import modules in Python:
#
# 1. import <module>
#    - Imports the entire module. You access its functions with module.function()
#    - Example: import os  -->  os.system("ls")
#
# 2. from <module> import <function>
#    - Imports specific functions directly into your namespace.
#    - You can use the function name directly without the module prefix.
#    - Example: from os import system  -->  system("ls")
#    - You can also import everything: from os import *  (NOT recommended --
#      it pollutes your namespace and makes it hard to tell where a function
#      came from)
#
# 3. import <module> as <alias>
#    - Imports the module with a shorter nickname (alias).
#    - Common conventions: import numpy as np, import pandas as pd
#    - Example: import os as operating_system  -->  operating_system.system("ls")
#
# WHY does this matter?
# - "import os" keeps your namespace clean -- you always know os.path came from os.
# - "from os import path" is convenient when you use path() many times.
# - "import numpy as np" saves typing for modules you use constantly.
#
# Mental model -- a module is a NAMESPACE BOX full of names you pull from:
#
#   module "os"  (a box of names)              your code's namespace
#   +-----------------------+
#   | system   getcwd       |   import os  -->  os.system(), os.getcwd()
#   | listdir  path  ...    |
#   +-----------------------+
#         |
#         | from os import system  -->  pulls just `system` out of the box
#         v                              into your own namespace: system()
#
#   "from os import *" dumps EVERY name out of the box into yours --
#   convenient but risky: if two modules export the same name, the
#   second import silently overwrites the first.

# =============================================================================
# SECTION 3: The OS Module -- Interacting with the Operating System
# =============================================================================
#
# The os module lets Python interact with the operating system.
# You can: open applications, list directory contents, create/remove folders,
# get environment variables, work with file paths, and much more.
#
# Common os functions:
#   os.system(command)   -- Run a shell command (like typing in terminal/cmd)
#   os.getcwd()          -- Get current working directory
#   os.listdir(path)     -- List files in a directory
#   os.mkdir(path)       -- Create a new directory
#   os.remove(path)      -- Delete a file
#   os.path.exists(path) -- Check if a file/path exists
#   os.path.join(a, b)   -- Safely join path components (handles / vs \ for you)
#
# Mental model -- os.path treats the filesystem as a tree you walk/inspect:
#
#   /Users/you/project/            os.getcwd()       -> ".../project"
#   +-- data/                      os.listdir(".")   -> ["data", "main.py"]
#   |   +-- input.txt              os.path.exists("data/input.txt") -> True
#   +-- main.py
#
#   os.path.join("data", "input.txt") -> "data/input.txt" (or "data\input.txt"
#   on Windows) -- it picks the right separator for you so the same code
#   works cross-platform instead of hardcoding "/" or "\".

import os

# %%

##### OS module
# - with this module, python can interact with the operating system
# - let's say through Python, if user wants to interact with the OS, we use this module
# - we can control some functionality of Operating system through OS module

# -------------------------------------------------------------------------
# NOTE FOR macOS USERS:
# The os.system() calls below were written for Windows. On macOS (and Linux),
# the command names and syntax are different.
#
# Windows command          macOS equivalent
# --------------------     ----------------------------------------
# os.system("notepad")     os.system("open -a TextEdit")
# os.system("chrome")      os.system("open -a 'Google Chrome'")
# os.system("WhatsApp")    os.system("open -a WhatsApp")
# os.system("OneNote")     os.system("open -a 'Microsoft OneNote'")
# os.system("Notes")       os.system("open -a Notes")
#
# The "open -a" command on macOS tells the system to open an application by name.
# If the app name has spaces, wrap it in quotes: open -a 'Google Chrome'
#
# On Linux, you would use the application's binary name directly:
#   os.system("google-chrome")
#   os.system("gedit")      # text editor
# -------------------------------------------------------------------------

# %%
# --- Original Windows examples (will not work on macOS as-is) ---
# os.system("notepad")    ## opens the notepad application - similar to what works on terminal / cmd prompt
# os.system("chrome")
# os.system("WhatsApp")

# --- macOS equivalents ---
# os.system("open -a TextEdit")         # macOS equivalent of notepad
# os.system("open -a 'Google Chrome'")  # macOS equivalent of chrome
# os.system("open -a WhatsApp")         # macOS equivalent of WhatsApp

# %%

# Example: Open an app based on user input (number-based)
# inp = int(input("enter an input: "))
# if inp == 1:
#     os.system("open -a 'Microsoft OneNote'")  # macOS; Windows: os.system("OneNote")
# if inp == 2:
#     os.system("open -a 'Google Chrome'")      # macOS; Windows: os.system("chrome")

"""
Now let's say if I give a prompt instead like:
 - Can you please open notepad for me?
 - open chrome

This is a basic form of Natural Language Processing (NLP)!
We check if a keyword appears anywhere in the user's input string.
The "in" operator does a substring search -- it checks if the left string
exists anywhere inside the right string.
"""

# Example: Open an app based on natural language input (keyword matching)
# inp = input("enter the input: ")
# if "notepad" in inp:
#     os.system("open -a TextEdit")         # macOS; Windows: os.system("notepad")
# if "chrome" in inp:
#     os.system("open -a 'Google Chrome'")  # macOS; Windows: os.system("chrome")

# =============================================================================
# SECTION 4: The webbrowser Module -- Opening URLs
# =============================================================================
#
# The webbrowser module provides a high-level interface for opening URLs
# in the user's default web browser. Unlike os.system(), it works
# cross-platform (Windows, macOS, Linux) without any changes.
#
# Key functions:
#   webbrowser.open(url)          -- Open URL in default browser
#   webbrowser.open_new(url)      -- Open URL in a new browser window
#   webbrowser.open_new_tab(url)  -- Open URL in a new tab

import webbrowser

# BUG FIX: Original code had "https:www.google.com" (missing //)
# The correct URL format requires :// after the protocol.
# Original (broken):  webbrowser.open("https:www.google.com")
# Fixed:
# webbrowser.open("https://www.google.com")

# =============================================================================
# SECTION 5: Basic File Reading with open()
# =============================================================================
#
# The open() function opens a file and returns a file object.
# "r" mode means read-only (the file must already exist).
#
# Always close files after you're done with f.close(), or better yet,
# use the "with" statement (covered in detail in Lecture 12).
#
# Pattern:
#   f = open("filename.txt", "r")   # Open the file
#   content = f.read()               # Read all contents into a string
#   print(content)                   # Do something with the contents
#   f.close()                        # ALWAYS close when done
#
# Better pattern (using "with" -- the file closes automatically):
#   with open("filename.txt", "r") as f:
#       content = f.read()
#       print(content)
#   # File is automatically closed here, even if an error occurs
#
# Mental model -- open() hands you a pointer into the file's byte stream:
#
#   filename.txt on disk: "Hello, world!"
#   f = open(...)  ->  pointer starts at position 0 -->|Hello, world!
#   f.read()       ->  reads to the end, pointer moves to the end ------->|
#   f.close()      ->  releases the OS file handle (forgetting this leaks
#                       handles and can leave writes un-flushed to disk)
#
#   See Lecture 12 (file_handling) for read/write modes in full detail.

# %%
# f = open("abc.txt", "r")
# print(f.read())
# f.close()

# The same thing using the "with" statement (preferred):
# with open("abc.txt", "r") as f:
#     print(f.read())
# %%

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
# 1. Library > Package > Module is the hierarchy of Python code organization.
# 2. Use "import" for full modules, "from...import" for specific items,
#    and "import...as" for aliases.
# 3. os.system() runs shell commands but is platform-specific. Use the
#    subprocess module for more robust cross-platform process management.
# 4. The webbrowser module is cross-platform and simpler for opening URLs.
# 5. Always close files after opening them, or use the "with" statement.
# 6. URL format matters: "https://..." not "https:..." (need the //).
