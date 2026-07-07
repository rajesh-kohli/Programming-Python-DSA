"""
Module 08: Modules and File Handling
======================================
Topics Covered:
  - Library / Package / Module hierarchy
  - Three import styles (import, from...import, import...as)
  - The OS module: interacting with the operating system
  - The webbrowser module (with BUG FIX demo)
  - All 12 file modes (text + binary)
  - Writing, reading, appending to files
  - Counting characters, words, and lines
  - Finding max / min length words
  - Counting alphabets, digits, special characters
  - Replacing characters (with String Immutability BUG FIX)
  - Copying files
  - The "with" statement (context manager)
  - File system mini-project with dictionary
  - The __name__ == "__main__" pattern
  - Cleanup with os.remove()

Source files: 10_modules_os.py, 12_file_handling.py, 13_file_system_project.py
"""

import os
import webbrowser

# =============================================================================
# SECTION 1: Library vs Package vs Module Hierarchy
# =============================================================================
#
# Python organizes code into a clear three-level hierarchy:
#
#   LIBRARY  (largest)   — e.g., NumPy, TensorFlow, scikit-learn
#   └── PACKAGE          — e.g., numpy.random  (a directory with __init__.py)
#       └── MODULE       — e.g., numpy.random.mtrand  (a single .py file)
#
# Analogy:
#   Library  = an entire bookshelf   (e.g., NumPy)
#   Package  = a single book         (e.g., numpy.random)
#   Module   = a chapter in a book   (e.g., numpy.random.mtrand)
#
# Types of modules:
#   1. Predefined  — already in Python (math, os, sys, time, webbrowser)
#   2. User-defined — any .py file you create; can be imported by others
#
# Predefined examples:
#   import math       → math.sqrt(16), math.pi
#   import os         → os.getcwd(), os.listdir()
#   import sys        → sys.argv, sys.path
#   import time       → time.sleep(1), time.time()
#   import webbrowser → webbrowser.open("https://www.google.com")

print("=" * 60)
print("SECTION 1: Library / Package / Module Hierarchy")
print("=" * 60)
print(f"  type(os)         : {type(os)}")           # Output: <class 'module'>
print(f"  type(webbrowser) : {type(webbrowser)}")   # Output: <class 'module'>
print()

# =============================================================================
# SECTION 2: Three Import Styles
# =============================================================================
#
# Style 1: import <module>
#   - Imports the entire module. Access via module.function()
#   - Keeps namespace clean — you always know where it came from
#   Example:
#     import os
#     os.getcwd()
#
# Style 2: from <module> import <name>
#   - Pulls a specific name into YOUR namespace — no prefix needed
#   - Convenient but can clash if two modules define the same name
#   - "from os import *"  ← NOT recommended (pollutes namespace)
#   Example:
#     from os import getcwd
#     getcwd()
#
# Style 3: import <module> as <alias>
#   - Renames the module with a shorter nickname
#   - Industry conventions: numpy → np, pandas → pd, matplotlib → plt
#   Example:
#     import os as operating_system
#     operating_system.getcwd()
#
# Mental model — a module is a NAMESPACE BOX full of names:
#
#   module "os"  (a box of names)           your namespace
#   +-------------------------+
#   | system   getcwd         |   import os  ──►  os.system(), os.getcwd()
#   | listdir  path  mkdir    |
#   +-------------------------+
#         |
#         | from os import getcwd  ──►  pulls just `getcwd` out of the box
#         v                             into YOUR namespace: getcwd()
#
#   "from os import *" dumps EVERY name out of the box into yours ─ risky!

# Style 1 demo
import os                        # entire module; use os.something
import webbrowser                # entire module; use webbrowser.something

# Style 2 demo
from os import getcwd, listdir   # specific names only
from os.path import join, exists # specific names from submodule

# Style 3 demo
import os as operating_system    # alias; use operating_system.something

print("=" * 60)
print("SECTION 2: Three Import Styles Demo")
print("=" * 60)
print(f"  Style 1 (import os):       {os.getcwd()[:40]}...")          # Output: current directory
print(f"  Style 2 (from os import):  {getcwd()[:40]}...")             # Output: same
print(f"  Style 3 (import os as):    {operating_system.getcwd()[:40]}...")  # Output: same
print()

# =============================================================================
# SECTION 3: The OS Module — Interacting with the Operating System
# =============================================================================
#
# The os module lets Python talk to the underlying OS.
# You can list files, create/remove directories, work with paths, and more.
#
# Common os functions:
#   os.getcwd()          — Get current working directory
#   os.listdir(path)     — List files/folders in a directory
#   os.mkdir(path)       — Create a new directory
#   os.remove(path)      — Delete a file
#   os.path.exists(path) — Check if a path exists (True/False)
#   os.path.join(a, b)   — Safely join path parts (handles / vs \ per OS)
#   os.system(command)   — Run a shell command
#
# Cross-platform note — os.system() commands are OS-specific:
#
#   Windows command             macOS equivalent
#   --------------------------  ----------------------------------
#   os.system("notepad")        os.system("open -a TextEdit")
#   os.system("chrome")         os.system("open -a 'Google Chrome'")
#   os.system("dir")            os.system("ls")
#   os.system("cls")            os.system("clear")
#
# os.path.join() is cross-platform — use it instead of hardcoding "/" or "\":
#   os.path.join("data", "input.txt")  → "data/input.txt"  (macOS/Linux)
#                                       → "data\input.txt"  (Windows)

print("=" * 60)
print("SECTION 3: The OS Module")
print("=" * 60)

cwd = os.getcwd()
print(f"  os.getcwd()         : {cwd}")                   # Output: .../08_Modules_and_File_Handling (or wherever)
print(f"  os.path.exists('.'): {os.path.exists('.')}")    # Output: True

# Build a safe cross-platform path
module_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
test_file_path = os.path.join(module_dir, "test_output.txt")
print(f"  test_output.txt path: {test_file_path}")        # Output: absolute path to test file
print()

# =============================================================================
# SECTION 4: The webbrowser Module
# =============================================================================
#
# The webbrowser module opens URLs in the default browser.
# Unlike os.system(), it works cross-platform with NO changes.
#
# Key functions:
#   webbrowser.open(url)         — Open URL in default browser
#   webbrowser.open_new(url)     — Open in a NEW browser window
#   webbrowser.open_new_tab(url) — Open in a new TAB
#
# *** BUG: Original source code had a typo in the URL:
#     webbrowser.open("https:www.google.com")   ← missing // after colon
#
# *** FIX: URL format requires :// (protocol, colon, double-slash):
#     webbrowser.open("https://www.google.com")  ← correct
#
# The // is part of the URL spec (RFC 3986). Without it, the browser
# tries to resolve it as a relative path, not a web address.
#
# The snippet below is commented out to avoid opening a browser window
# every time this file is run. Uncomment to test.

print("=" * 60)
print("SECTION 4: webbrowser Module (commented-out demo)")
print("=" * 60)
print("  # webbrowser.open('https://www.google.com')  ← correct")
print("  # *** BUG:  webbrowser.open('https:www.google.com')  ← missing //")
print("  # *** FIX:  Add // after the colon: https://")
print()

# =============================================================================
# SECTION 5: File Modes Reference
# =============================================================================
#
# Syntax:  file_object = open("filename", "mode")
#
# TEXT MODES:
# +-------+------------------------------------------------------------------+
# | "r"   | Read only (DEFAULT). File MUST exist.                            |
# | "w"   | Write only. Creates if missing. OVERWRITES existing content.     |
# | "a"   | Append only. Creates if missing. Adds to END if exists.          |
# | "r+"  | Read AND write. File must exist. Pointer at beginning.           |
# | "w+"  | Write AND read. Creates/overwrites. Can read after writing.      |
# | "a+"  | Append AND read. Creates if missing. Pointer at end.             |
# +-------+------------------------------------------------------------------+
# BINARY MODES (add 'b' suffix — same rules, no text encoding):
# | "rb"  | Read binary (images, PDFs, etc.)                                 |
# | "wb"  | Write binary                                                      |
# | "ab"  | Append binary                                                     |
# | "rb+" | Read/write binary                                                 |
# | "wb+" | Write/read binary                                                 |
# | "ab+" | Append/read binary                                                |
# +-------+------------------------------------------------------------------+
#
# KEY DIFFERENCES:
#   "w" vs "a" : "w" erases everything first; "a" adds to the end
#   "r" vs "r+": "r" is read-only; "r+" lets you also write
#   text vs binary: text handles encoding (newlines); binary is raw bytes
#
# Mental model:
#   open(f, "w")   → pointer at 0, OLD CONTENT GONE      → write here
#   open(f, "a")   → pointer at END, old content kept     → write appends
#   open(f, "r+")  → pointer at 0, content kept           → write OVERWRITES (no insert)

print("=" * 60)
print("SECTION 5: File Mode Reference (see comments above for full table)")
print("=" * 60)
print("  12 modes: r, w, a, r+, w+, a+, rb, wb, ab, rb+, wb+, ab+")
print()

# =============================================================================
# SECTION 6: Creating and Writing to a File (mode "w")
# =============================================================================
#
# "w" mode:
#   - Creates the file if it doesn't exist
#   - ERASES all content if the file already exists
#   - f.write(string) does NOT add a newline — include "\n" yourself
#
# WHY close files?
#   1. Data may be buffered in memory, not written to disk until close()
#   2. Open files consume system resources (file descriptors)
#   3. Other processes may not access the file while it's open
#
# Better: use the "with" statement — file closes automatically (Section 11).

print("=" * 60)
print("SECTION 6: Writing to a File (mode 'w')")
print("=" * 60)

# Create test_output.txt — this file is used throughout the module
f = open(test_file_path, "w")
f.write("Hello World")                       # no automatic newline
f.write("\nThis is a test file")             # \n adds line break
f.write("\nPython file handling is powerful")
f.write("\nLearning is the key to success")
f.close()

print(f"  Created: {test_file_path}")        # Output: file path
print()

# =============================================================================
# SECTION 7: Reading from a File — Three Methods
# =============================================================================
#
# f.read()      — Read the ENTIRE file as ONE string (loads all into memory)
# f.readline()  — Read ONE line at a time (returns empty string at EOF)
# f.readlines() — Read ALL lines into a LIST of strings (each line = list item)
# for line in f — Iterate line-by-line (most memory-efficient for large files)
#
# Mental model:
#   open() hands you a pointer into the file's byte stream:
#
#   file on disk: "Hello World\nThis is a test file"
#   f = open(...)  → pointer at position 0  →  |Hello World\nThis...
#   f.read()       → reads to end, pointer moves to end →  ...test file|
#   f.close()      → releases the OS file handle
#
# TIME COMPLEXITY: O(n) where n = total characters in the file
# SPACE COMPLEXITY: O(n) for f.read() (reads entire file into memory)
#                   O(k) for line-by-line (k = length of longest line)

print("=" * 60)
print("SECTION 7: Reading from a File (three methods)")
print("=" * 60)

# Method 1: f.read() — entire file as one string
f = open(test_file_path, "r")
content = f.read()
f.close()
print("  Method 1 — f.read():")
print(f"    {repr(content[:50])}...")   # Output: first 50 chars of file content

# Method 2: f.readline() — one line at a time
f = open(test_file_path, "r")
first_line  = f.readline()   # reads "Hello World\n"
second_line = f.readline()   # reads "This is a test file\n"
f.close()
print(f"  Method 2 — f.readline():")
print(f"    Line 1: {repr(first_line.strip())}")   # Output: 'Hello World'
print(f"    Line 2: {repr(second_line.strip())}")  # Output: 'This is a test file'

# Method 3: f.readlines() — all lines into a list
f = open(test_file_path, "r")
lines_list = f.readlines()
f.close()
print(f"  Method 3 — f.readlines():")
for i, line in enumerate(lines_list, start=1):
    print(f"    Line {i}: {repr(line.rstrip())}")  # Output: each line without trailing \n
print()

# =============================================================================
# SECTION 8: Appending to a File (mode "a")
# =============================================================================
#
# "a" mode: pointer starts at the END — all writes go to the end.
# Unlike "w", existing content is NOT erased.

print("=" * 60)
print("SECTION 8: Appending to a File (mode 'a')")
print("=" * 60)

f = open(test_file_path, "a")
f.write("\nAppended line: the 'a' mode never erases existing content")
f.close()

# Verify append worked
with open(test_file_path, "r") as f:
    lines = f.readlines()
print(f"  File now has {len(lines)} lines after append")  # Output: 5 lines
print(f"  Last line: {repr(lines[-1].rstrip())}")          # Output: the appended line
print()

# =============================================================================
# SECTION 9: Counting Characters, Words, and Lines
# =============================================================================
#
# TIME COMPLEXITY: O(n) for all three — must scan every character
# SPACE COMPLEXITY: O(n) for f.read() approach; O(k) for line-by-line
#
# str.split() splits on any whitespace by default (spaces, tabs, newlines).
# str.split("\n") splits on newlines specifically.
# len() counts ALL characters including "\n", spaces, tabs.

print("=" * 60)
print("SECTION 9: Counting Characters, Words, and Lines")
print("=" * 60)

# Count characters (Approach: read all, then len)
with open(test_file_path, "r") as f:
    data = f.read()

char_count = len(data)
word_count = len(data.split())
line_count = len(data.splitlines())

print(f"  Character count : {char_count}")   # Output: total chars including \n
print(f"  Word count      : {word_count}")   # Output: total words
print(f"  Line count      : {line_count}")   # Output: number of lines

# Per-line breakdown using enumerate (Pythonic — no manual counter)
print("\n  Per-line word count (using enumerate):")
with open(test_file_path, "r") as f:
    for line_num, line in enumerate(f, start=1):
        words_in_line = len(line.split())
        print(f"    Line {line_num}: {words_in_line} words")   # Output: word count per line
print()

# =============================================================================
# SECTION 10: Max and Min Length Words
# =============================================================================
#
# max(iterable, key=len) → item with the largest len() value
# min(iterable, key=len) → item with the smallest len() value
# key=len means "compare items BY their length"
#
# TIME COMPLEXITY:  O(n) each — single pass through words list
# SPACE COMPLEXITY: O(w) where w = number of words
#
# If multiple words share the same max/min length, max()/min() returns the FIRST one.

print("=" * 60)
print("SECTION 10: Max and Min Length Words")
print("=" * 60)

with open(test_file_path, "r") as f:
    words = f.read().split()

max_word = max(words, key=len)
min_word = min(words, key=len)

print(f"  Maximum length word: '{max_word}' ({len(max_word)} chars)")  # Output: longest word
print(f"  Minimum length word: '{min_word}' ({len(min_word)} chars)")  # Output: shortest word

# Manual approach (same result, shows the logic):
max_w = words[0]
min_w = words[0]
for word in words:
    if len(word) > len(max_w):
        max_w = word
    if len(word) < len(min_w):
        min_w = word
print(f"  (Manual) Max: '{max_w}' | Min: '{min_w}'")   # Output: same as above
print()

# =============================================================================
# SECTION 11: The "with" Statement — Context Manager (Preferred Pattern)
# =============================================================================
#
# The "with" statement automatically closes files when the block ends,
# even if an exception occurs. This is the RECOMMENDED approach.
#
# Manual approach (error-prone):
#   f = open("file.txt", "r")
#   data = f.read()
#   f.close()          ← easy to forget! exception skips this line!
#
# "with" approach (recommended):
#   with open("file.txt", "r") as f:
#       data = f.read()
#   # f is automatically closed here, even if an exception occurred
#
# How it works internally:
#   1. "with" calls f.__enter__()  → opens/acquires the resource
#   2. The block runs               → you use the resource
#   3. Block ends (normal OR error) → f.__exit__() is called
#   4. f.__exit__() calls f.close() → resource released (guaranteed!)
#
# You can open MULTIPLE files in one "with":
#   with open("in.txt", "r") as src, open("out.txt", "w") as dst:
#       dst.write(src.read())

print("=" * 60)
print("SECTION 11: The 'with' Statement (Context Manager)")
print("=" * 60)

with open(test_file_path, "r") as f:
    sample = f.read()

print(f"  Read {len(sample)} characters using 'with' (auto-closed)")   # Output: character count
print(f"  Is f closed after 'with' block? {f.closed}")                  # Output: True
print()

# =============================================================================
# SECTION 12: Counting Alphabets, Digits, and Special Characters
# =============================================================================
#
# Character classification methods:
#   char.isalpha()  — True if letter (a-z, A-Z)
#   char.isdigit()  — True if digit (0-9)
#   char.isalnum()  — True if letter OR digit
#   char.isspace()  — True if whitespace (space, tab, newline)
#
# TIME COMPLEXITY:  O(n) where n = total characters
# SPACE COMPLEXITY: O(n) for f.read(), O(1) for the counters

print("=" * 60)
print("SECTION 12: Counting Character Types")
print("=" * 60)

# Write a file with mixed content for demonstration
mixed_path = os.path.join(module_dir, "mixed_content.txt")
with open(mixed_path, "w") as f:
    f.write("Hello World 123!@#\n")
    f.write("Python3 is great!!!\n")
    f.write("abc123@#$\n")

# Approach 1: Manual loop
with open(mixed_path, "r") as f:
    data = f.read()

alphabets      = 0
digits         = 0
special_chars  = 0
spaces         = 0

for char in data:
    if char.isalpha():
        alphabets += 1
    elif char.isdigit():
        digits += 1
    elif char.isspace():
        spaces += 1
    else:
        special_chars += 1

print(f"  Alphabets       : {alphabets}")      # Output: count of letters
print(f"  Digits          : {digits}")         # Output: count of digits
print(f"  Special chars   : {special_chars}")  # Output: count of !@#$% etc.
print(f"  Spaces/newlines : {spaces}")         # Output: whitespace count

# Approach 2: Generator expressions with sum()
# sum(condition for c in data) works because True=1, False=0 in Python
with open(mixed_path, "r") as f:
    data2 = f.read()

alpha2   = sum(c.isalpha() for c in data2)
digit2   = sum(c.isdigit() for c in data2)
special2 = sum(not c.isalnum() and not c.isspace() for c in data2)
print(f"\n  (Generator approach) Alphabets: {alpha2} | Digits: {digit2} | Special: {special2}")  # Output: same counts
print()

# =============================================================================
# SECTION 13: String Immutability Bug — Replacing Characters
# =============================================================================
#
# IMPORTANT: Strings in Python are IMMUTABLE.
# You CANNOT modify a string in place. str.replace() returns a NEW string.
# The original string is never changed.
#
# Mental model:
#   data = "abc"
#   data.replace("a", "#")   creates id 2001: "#bc"  ← thrown away!
#         |
#         v (return value IGNORED)
#   data still → id 1001: "abc"   (UNCHANGED — this is the bug)
#
#   data = data.replace("a", "#")  ← MUST reassign to capture new string
#   data now   → id 2001: "#bc"   (data now points at the new string)
#
# *** BUG: The original source code had:
#       for i in data:
#           if i.isalpha():
#               data.replace(i, "#")   ← return value discarded! BUG!
#           elif i.isdigit():
#               data.replace(i, "*")   ← same BUG!
#           else:
#               data.replace(i, "0")   ← same BUG!
#       # Result: data is completely UNCHANGED because all replace() results were discarded
#
# *** FIX: Use "".join() with a generator expression to process each character once.
#       new_data = "".join(
#           "#" if c.isalpha() else "*" if c.isdigit() else "0"
#           for c in data
#       )
#       # Each character is processed EXACTLY ONCE — no double-replacement issue.

print("=" * 60)
print("SECTION 13: String Immutability — Replacing Characters")
print("=" * 60)

# Additional demonstration of string immutability with indexing
sample_string = "Hello"
print(f"  sample_string = {repr(sample_string)}")

# *** BUG: You CANNOT index-assign a string like a list
# sample_string[0] = "X"  ← TypeError: 'str' object does not support item assignment
print("  # *** BUG:  sample_string[0] = 'X'  → TypeError: str does not support item assignment")
print("  # *** FIX:  Convert to list, modify, join back:")

# *** FIX: List conversion
char_list = list(sample_string)   # ['H', 'e', 'l', 'l', 'o']
char_list[0] = "X"                # modify the list (lists are mutable)
fixed_string = "".join(char_list) # join back into a string
print(f"  Fixed: {repr(fixed_string)}")   # Output: 'Xello'
print()

# Now demo the correct replace approach using the mixed_content file
with open(mixed_path, "r") as f:
    data = f.read()

# *** BUG DEMO (no-op — replace result is discarded, data unchanged):
data_unchanged = data
for i in data_unchanged:
    if i.isalpha():
        data_unchanged.replace(i, "#")   # *** BUG: return value ignored!
    elif i.isdigit():
        data_unchanged.replace(i, "*")   # *** BUG: return value ignored!
    else:
        data_unchanged.replace(i, "0")   # *** BUG: return value ignored!

print(f"  After BUGGY code — data is unchanged:")
print(f"    First 30 chars: {repr(data_unchanged[:30])}")   # Output: original content

# *** FIX DEMO: generator expression — each character processed ONCE:
# TIME COMPLEXITY:  O(n) where n = number of characters
# SPACE COMPLEXITY: O(n) for the new string
new_data = "".join(
    "#" if c.isalpha() else "*" if c.isdigit() else "0"
    for c in data
)
# Explanation:
# - For each character c in data:
#     if c is a letter → replace with "#"
#     elif c is a digit → replace with "*"
#     else (space, newline, special) → replace with "0"
# - "".join() assembles all the transformed characters into one string

print(f"\n  After FIXED code — data is transformed:")
print(f"    Original:    {repr(data[:20])}")     # Output: original content
print(f"    Transformed: {repr(new_data[:20])}") # Output: all # * 0 characters
print()

# =============================================================================
# SECTION 14: Copying Files
# =============================================================================
#
# To copy a file: read from source, write to destination.
# For production code, use shutil.copy("src.txt", "dst.txt") — handles large files.
#
# TIME COMPLEXITY:  O(n) where n = file size in characters
# SPACE COMPLEXITY: O(n) because we read the entire file into memory
#
# Mental model:
#   source.txt → f.read() → data (in memory) → f.write() → destination.txt

print("=" * 60)
print("SECTION 14: Copying Files")
print("=" * 60)

copy_src = test_file_path
copy_dst = os.path.join(module_dir, "test_output_copy.txt")

# Manual copy
with open(copy_src, "r") as src:
    file_data = src.read()

with open(copy_dst, "w") as dst:
    dst.write(file_data)

# Verify
with open(copy_dst, "r") as f:
    copied_content = f.read()

print(f"  Copied {len(copied_content)} characters from test_output.txt → test_output_copy.txt")  # Output: char count
print(f"  Content matches: {file_data == copied_content}")   # Output: True

# Production approach (shutil) — shown as comment:
# import shutil
# shutil.copy("test_output.txt", "test_output_copy.txt")
print()

# =============================================================================
# SECTION 15: File System Mini-Project (Dict + Files)
# =============================================================================
#
# Combine dictionaries + file handling to build a mini "file system".
# - Dictionary keys   = file names (strings)
# - Dictionary values = file contents (strings)
# - Operations also write to REAL files on disk → data persists
#
# This mirrors how databases work: fast in-memory lookups + persistent storage.
#
# dict.get(key, default) is safer than dict[key]:
#   file_system.get("notes.txt", "")  → "" if file not in dict (no crash)
#   file_system["missing.txt"]        → KeyError! (crashes)
#
# TIME COMPLEXITY (dict operations):
#   Lookup:  O(1) average (hash table)
#   Insert:  O(1) average
#   Delete:  O(1) average
#   List all: O(n) where n = number of files
#
# __name__ == "__main__" pattern:
#   When you RUN a file directly → __name__ is "__main__"
#   When you IMPORT a file       → __name__ is the module name
#   Use "if __name__ == '__main__':" to prevent demo code from running on import.

print("=" * 60)
print("SECTION 15: File System Mini-Project")
print("=" * 60)

# Global in-memory index
file_system = {}


def create_file(file_name, contents=""):
    """
    Create a new file on disk and add it to the in-memory dictionary.
    If the file already exists, it is overwritten.

    TIME COMPLEXITY:  O(m) where m = length of contents
    SPACE COMPLEXITY: O(m) for storing in the dictionary
    """
    full_path = os.path.join(module_dir, file_name)
    with open(full_path, "w") as f:
        f.write(contents)
    file_system[file_name] = contents


def add_contents(file_name, contents):
    """
    Append contents to a file and update the dictionary.
    If the file doesn't exist, it is created first.

    TIME COMPLEXITY:  O(m) where m = length of new contents
    SPACE COMPLEXITY: O(1) additional
    """
    if file_name not in file_system:
        file_system[file_name] = ""
    full_path = os.path.join(module_dir, file_name)
    with open(full_path, "a") as f:
        f.write(contents)
    file_system[file_name] += contents   # update in-memory index


def read_file_fs(file_name):
    """
    Read from the in-memory dictionary (O(1) — no disk I/O).
    dict.get(key, default) returns default if key is missing (safe).

    TIME COMPLEXITY:  O(1)
    SPACE COMPLEXITY: O(1)
    """
    return file_system.get(file_name, "")  # safe: returns "" if not found


def list_files():
    """
    List all file names in the file system.

    TIME COMPLEXITY:  O(n) where n = number of files
    SPACE COMPLEXITY: O(n) for the returned list
    """
    return list(file_system.keys())


# Demo (runs only when executed directly, not when imported)
if __name__ == "__main__":
    create_file("notes.txt", "Hello")
    add_contents("notes.txt", " World")
    print(f"  read_file_fs('notes.txt') : {repr(read_file_fs('notes.txt'))}")   # Output: 'Hello World'
    print(f"  list_files()              : {list_files()}")                       # Output: ['notes.txt']
    create_file("todo.txt", "Buy groceries\n")
    add_contents("todo.txt", "Clean house\n")
    print(f"  list_files() with 2 files : {list_files()}")                       # Output: ['notes.txt', 'todo.txt']

print()

# =============================================================================
# SECTION 16: Binary File Modes (rb, wb, ab)
# =============================================================================
#
# Binary modes read/write raw bytes — no text encoding/decoding.
# Use for: images (.png, .jpg), PDFs, audio files, compiled code, etc.
#
# TEXT mode:   "Hello\n" → file contains H-e-l-l-o-newline (encodes \n per OS)
# BINARY mode: b"Hello\n" → file contains exactly H-e-l-l-o-\n (raw bytes)
#
# TIME COMPLEXITY:  O(n) where n = number of bytes
# SPACE COMPLEXITY: O(n) for reading the entire file into memory

print("=" * 60)
print("SECTION 16: Binary File Modes (rb / wb)")
print("=" * 60)

binary_path = os.path.join(module_dir, "binary_demo.bin")

# Write binary
with open(binary_path, "wb") as f:
    data_bytes = b"Binary data: \x00\x01\x02\x03\xFF"
    f.write(data_bytes)

# Read binary
with open(binary_path, "rb") as f:
    raw = f.read()

print(f"  Written bytes : {list(data_bytes)}")   # Output: list of byte values
print(f"  Read back     : {list(raw)}")           # Output: same list
print(f"  Match         : {raw == data_bytes}")   # Output: True
print()

# =============================================================================
# SECTION 17: r+ and a+ Modes (Read + Write Combined)
# =============================================================================
#
# "r+" mode:
#   - File MUST exist (no creation)
#   - Pointer starts at BEGINNING
#   - Can BOTH read and write
#   - write() OVERWRITES (doesn't insert) — replaces from pointer position
#
# "a+" mode:
#   - Creates file if missing
#   - All writes go to END (can't write to middle)
#   - Can read (seek to 0 first to read from beginning)

print("=" * 60)
print("SECTION 17: r+ and a+ Modes")
print("=" * 60)

rplus_path = os.path.join(module_dir, "rplus_demo.txt")

# Create file first
with open(rplus_path, "w") as f:
    f.write("ABCDEF")

# Open with r+ — overwrite from beginning
with open(rplus_path, "r+") as f:
    original = f.read()
    f.seek(0)           # move pointer back to start
    f.write("XY")       # overwrites first 2 chars: A→X, B→Y
    f.seek(0)
    updated = f.read()

print(f"  r+ mode: original='{original}', after write('XY')='{updated}'")   # Output: XYCDEF (first 2 chars changed)

# a+ mode demo
aplus_path = os.path.join(module_dir, "aplus_demo.txt")
with open(aplus_path, "a+") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.seek(0)            # seek to beginning to read
    content = f.read()

print(f"  a+ mode: content = {repr(content)}")   # Output: 'Line 1\nLine 2\n'
print()

# =============================================================================
# SECTION 18: Cleanup — Deleting Test Files with os.remove()
# =============================================================================
#
# os.remove(path) deletes a file from the filesystem.
# Always check os.path.exists(path) first to avoid FileNotFoundError.
#
# TIME COMPLEXITY:  O(1) — just an OS syscall
# SPACE COMPLEXITY: O(1)

print("=" * 60)
print("SECTION 18: Cleanup — os.remove()")
print("=" * 60)

files_to_clean = [
    os.path.join(module_dir, "test_output.txt"),
    os.path.join(module_dir, "test_output_copy.txt"),
    os.path.join(module_dir, "mixed_content.txt"),
    os.path.join(module_dir, "binary_demo.bin"),
    os.path.join(module_dir, "rplus_demo.txt"),
    os.path.join(module_dir, "aplus_demo.txt"),
    os.path.join(module_dir, "notes.txt"),
    os.path.join(module_dir, "todo.txt"),
]

for fpath in files_to_clean:
    if os.path.exists(fpath):
        os.remove(fpath)
        print(f"  Deleted: {os.path.basename(fpath)}")   # Output: filename of deleted file
    else:
        print(f"  Not found (skipped): {os.path.basename(fpath)}")

print()

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
# 1. Library > Package > Module — Python's code organization hierarchy.
# 2. Three import styles: import, from...import, import...as.
# 3. os module: getcwd(), listdir(), remove(), path.join(), path.exists().
# 4. webbrowser.open("https://...") — cross-platform URL opener.
#    BUG: missing // in URL ("https:..." instead of "https://...").
# 5. 12 file modes: r, w, a, r+, w+, a+  and their 'b' binary counterparts.
# 6. Always close files. Use "with" statement — it closes automatically.
# 7. f.read() reads all; f.readline() reads one line; f.readlines() returns list.
# 8. STRINGS ARE IMMUTABLE: str.replace() returns a NEW string — must reassign.
#    BUG: data.replace(i, "#") without assignment does NOTHING.
# 9. Use "".join(generator) for character-by-character transformation.
# 10. dict.get(key, default) is safer than dict[key] — returns default if missing.
# 11. if __name__ == "__main__" prevents demo code from running on import.
# 12. os.remove(path) deletes files; check os.path.exists() first.

# =============================================================================
# === PRACTICE ZONE ===
# =============================================================================
#
# Complete these exercises. Each is runnable with no input() calls needed.

# --- Exercise 1: File Statistics ---
# Create a file with at least 5 lines of text (any content you choose).
# Count and print: total chars, words, lines, longest word, shortest word.
# Expected output format:
#   Chars: 142  |  Words: 27  |  Lines: 5
#   Longest word: 'extraordinary' (13 chars)
#   Shortest word: 'a' (1 chars)

# YOUR CODE HERE:
# practice_path = os.path.join(module_dir, "practice_stats.txt")
# ...

# --- Exercise 2: Character Frequency ---
# Read a file and print the count of each UNIQUE character (case-insensitive).
# Ignore spaces and newlines.
# Hint: use a dictionary — char → count.

# YOUR CODE HERE:
# ...

# --- Exercise 3: Word Frequency ---
# Read a file and print the top 5 most frequent words (case-insensitive).
# Hint: str.lower(), dict, sorted(..., key=lambda x: x[1], reverse=True).

# YOUR CODE HERE:
# ...

# --- Exercise 4: File Merger ---
# Write a function merge_files(file_list, output_file) that reads all files
# in file_list and writes their combined content to output_file.
# Add a separator line "--- FILE: filename ---" between each file's content.

# YOUR CODE HERE:
# def merge_files(file_list, output_file):
#     pass

# --- Exercise 5: File System Mini-Project Extension ---
# Extend the file_system dict from Section 15 with:
#   delete_file(file_name) — removes from dict AND from disk
#   rename_file(old_name, new_name) — renames in dict AND on disk (os.rename)

# YOUR CODE HERE:
# def delete_file(file_name): ...
# def rename_file(old_name, new_name): ...
