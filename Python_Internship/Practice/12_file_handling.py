"""
Lecture 12: File Handling in Python
====================================
Topics Covered:
  - File modes (read, write, append, binary, combined)
  - Writing to files
  - Reading from files
  - Counting characters, words, and lines
  - Finding max/min length words
  - Counting alphabets, digits, and special characters
  - Replacing characters in file content
  - Copying file contents
  - The "with" statement (context manager)
  - Common bug: string immutability

File handling is used to perform operations on files like opening, reading,
writing, appending, and closing. Files let your program persist data beyond
the current execution -- if you store data in a variable, it's lost when the
program ends. Files keep data permanently on disk.
"""

# =============================================================================
# SECTION 1: File Modes Reference Table
# =============================================================================
#
# syntax:
# file_object = open("filename", "mode")
#
# +------+------------------------------------------------------------------+
# | Mode | Description                                                      |
# +------+------------------------------------------------------------------+
# | "r"  | Read only (DEFAULT). File must exist.                            |
# | "w"  | Write only. Creates file if missing. OVERWRITES if exists.       |
# | "a"  | Append only. Creates file if missing. Adds to end if exists.     |
# | "r+" | Read AND write. File must exist. Pointer starts at beginning.    |
# | "w+" | Write AND read. Creates/overwrites. Can read after writing.      |
# | "a+" | Append AND read. Creates if missing. Pointer starts at end.      |
# +------+------------------------------------------------------------------+
# | "rb" | Read binary. For non-text files (images, PDFs, etc.)             |
# | "wb" | Write binary.                                                    |
# | "ab" | Append binary.                                                   |
# | "rb+"| Read/write binary.                                              |
# | "wb+"| Write/read binary.                                              |
# | "ab+"| Append/read binary.                                             |
# +------+------------------------------------------------------------------+
#
# KEY DIFFERENCES:
#   "w" vs "a" : "w" erases everything first; "a" adds to the end
#   "r" vs "r+": "r" is read-only; "r+" lets you also write
#   text vs binary: text mode handles encoding (newlines, etc.);
#                   binary mode reads/writes raw bytes

# (read, write, append, read/write, binary read, binary write, binary append, binary read/write)
# eg.
# f = open("test.txt", "r") # open file in read mode
# f = open("test.txt", "w") # open file in write mode
# f = open("test.txt", "a") # open file in append mode
# f = open("test.txt", "r+") # open file in read/write mode
# f = open("test.txt", "w+") # open file in write/read mode
# f = open("test.txt", "a+") # open file in append/read mode
# f = open("test.txt", "rb") # open file in binary read mode
# f = open("test.txt", "wb") # open file in binary write mode
# f = open("test.txt", "ab") # open file in binary append mode
# f = open("test.txt", "rb+") # open file in binary read/write mode
# f = open("test.txt", "wb+") # open file in binary write/read mode
# f = open("test.txt", "ab+") # open file in binary append/read mode

# =============================================================================
# SECTION 2: Writing to Files
# =============================================================================
#
# When you open a file in "w" mode, it creates the file if it doesn't exist.
# WARNING: If the file already exists, "w" mode ERASES all existing content!
# Use "a" (append) mode if you want to add to existing content.
#
# f.write(string) writes the string to the file. It does NOT add a newline
# automatically -- you must include "\n" yourself if you want line breaks.

f = open("test.txt", "w")  # open file in write mode
f.write("Hello World")  # write to file
f.write("\nThis is a test file")  # write to file (note the \n for newline)
f.write("\nThis is a test file")  # write to file
f.close()  # close file

# WHY close files?
# 1. Data may be buffered (sitting in memory, not written to disk yet).
#    close() flushes the buffer and ensures data is saved.
# 2. Open files use system resources (file descriptors). Your OS limits
#    how many files you can have open simultaneously.
# 3. Other programs may not be able to access the file while it's open.

# =============================================================================
# SECTION 3: Reading from Files
# =============================================================================
#
# f.read()       -- Read the ENTIRE file as one string
# f.readline()   -- Read one line at a time
# f.readlines()  -- Read all lines into a list of strings
# for line in f  -- Iterate over lines (memory efficient for large files)

f1 = open("test.txt", "r")  # open file in read mode
print(f1.read())  # read file
f1.close()  # close file

# =============================================================================
# SECTION 4: Counting Characters in a File
# =============================================================================
#
# Time Complexity: O(n) where n is the total number of characters in the file
# Space Complexity: O(n) for f.read() (reads entire file into memory)
#                   O(k) for the line-by-line approach (k = length of longest line)

# write a program to count the number of characters in a file

# Approach 1: Line-by-line counting
# Space efficient for very large files -- only one line in memory at a time
f = open("test.txt", "r")
count = 0
for line in f:
    count += len(line)
print("Number of characters in file:", count)
f.close()

# OR

# Approach 2: Read entire file, then get length
f = open("test.txt", "r")
count = len(f.read())
print("Number of characters in file:", count)
f.close()

# OR

# Approach 3: Same as Approach 2, but store in a variable first
# (useful if you need 'data' for other operations later)
f = open("test.txt", "r")
data = f.read()
print("Number of characters in file:", len(data))
f.close()

# NOTE: len() counts ALL characters including \n (newline), spaces, tabs, etc.
# If you want only visible characters, you'd need to filter them out.

# =============================================================================
# SECTION 5: Counting Words in a File
# =============================================================================
#
# str.split() splits a string by whitespace (spaces, tabs, newlines) and
# returns a list of words. Multiple consecutive spaces are treated as one.
#
# Time Complexity: O(n) where n is total characters (split scans every char)
# Space Complexity: O(w) where w is the number of words

# write a program to count the number of words in a file

# Approach 1: Line-by-line word counting
f = open("test.txt", "r")
count = 0
for line in f:
    words = line.split()  # split() with no args splits on ANY whitespace
    count += len(words)
print("Number of words in file:", count)
f.close()

# OR

# Approach 2: One-liner -- read everything, split, count
f = open("test.txt", "r")
count = len(f.read().split())
print("Number of words in file:", count)
f.close()

# OR

# Approach 3: Store intermediate results in variables
f = open("test.txt", "r")
data = f.read()
words = data.split()
print("Number of words in file:", len(words))
f.close()

# =============================================================================
# SECTION 6: Finding Max and Min Length Words
# =============================================================================
#
# max(iterable, key=func) returns the item with the largest key value.
# min(iterable, key=func) returns the item with the smallest key value.
# key=len means "compare items by their length."
#
# Time Complexity:
#   - Using max()/min() with key=len: O(n) each, so O(n) total for both
#   - Using manual loop: O(n) single pass for both max and min
# Space Complexity: O(w) where w is number of words (for the words list)

## Write a program to find the maximum length word and minimum length word in a file

# Approach 1: Using built-in max() and min() with key=len
# This is the most Pythonic (idiomatic) approach
f = open("test.txt", "r")
words = f.read().split()
max_word = max(words, key=len)
min_word = min(words, key=len)
print("Maximum length word:", max_word)
print("Minimum length word:", min_word)
f.close()

# OR

# Approach 2: Manual comparison, line by line
f = open("test.txt", "r")
max_word = ""
min_word = ""
for line in f:
    words = line.split()
    for word in words:
        if len(word) > len(max_word):
            max_word = word
        if len(word) < len(min_word) or min_word == "":
            # The "or min_word == ''" handles the initial case where min_word
            # is empty -- any word is shorter than "no word at all"
            min_word = word
print("Maximum length word:", max_word)
print("Minimum length word:", min_word)
f.close()

# OR

# Approach 3: Same as Approach 1 but with intermediate variable
f = open("test.txt", "r")
data = f.read()
words = data.split()
max_word = max(words, key=len)
min_word = min(words, key=len)
print("Maximum length word:", max_word)
print("Minimum length word:", min_word)
f.close()

# OR

# Approach 4: Manual loop over the words list
f = open("test.txt", "r")
data = f.read()
lst = data.split()
max_word = lst[0]  # Initialize with the first word (better than empty string)
min_word = lst[0]
for word in lst:
    if len(word) > len(max_word):
        max_word = word
    if len(word) < len(min_word):
        min_word = word
print("Maximum length word:", max_word)
print("Minimum length word:", min_word)
f.close()

# NOTE: If there are multiple words with the same max/min length,
# max() and min() return the FIRST one found.

# =============================================================================
# SECTION 7: Working with a Messier File (tp.txt)
# =============================================================================
#
# Let's create a file with mixed content (letters, digits, special chars)
# to practice more complex file analysis.

###
f = open("tp.txt", "w")
f.write("sdkjashuewvbnjbsdjlilusdjlsbdlvsduleiv\n")
f.write("sjfdsfkvsljkhsuiiub xz siluciucjhczxjzbjx zjl\n")
f.write("asbjchuyefeiouhjacbhzxjbn ziulcewiu zxlJ\n")
f.write("sdkjash@198P9E19E8YD88E8uewvbnjbsdjlilusdjlsbdlvsduleiv\n")
f.write("sdkjashuewv!@#^%&((&!&@&bnjbsdjlilusdjlsbdlvsduleiv\n")
f.close()

f = open("tp.txt", "r")
print(f.read())
f.close()

# =============================================================================
# SECTION 8: Counting Alphabets, Digits, and Special Characters
# =============================================================================
#
# Character classification methods:
#   char.isalpha()  -- True if char is a letter (a-z, A-Z)
#   char.isdigit()  -- True if char is a digit (0-9)
#   char.isalnum()  -- True if char is a letter OR digit
#   char.isspace()  -- True if char is whitespace (space, tab, newline)
#
# Time Complexity: O(n) where n is total characters in the file
# Space Complexity: O(n) for f.read(), O(1) for the counters

## Write a program to count the number of alphabets, digits and special characters in a file

# Approach 1: Loop through each character, line by line
f = open("tp.txt", "r")
alphabets = 0
digits = 0
special_characters = 0
for line in f:
    for char in line:
        if char.isalpha():
            alphabets += 1
        elif char.isdigit():
            digits += 1
        else:
            special_characters += 1
            # NOTE: This "else" catches spaces, newlines, tabs, AND special
            # characters. If you want to separate spaces from special chars,
            # add an elif for char.isspace()
print("Number of alphabets:", alphabets)
print("Number of digits:", digits)
print("Number of special characters:", special_characters)
f.close()

# OR

# Approach 2: Using generator expressions with sum()
# sum(True/False for ...) works because True=1 and False=0 in Python
f = open("tp.txt", "r")
data = f.read()
alphabets = sum(c.isalpha() for c in data)
digits = sum(c.isdigit() for c in data)
special_characters = sum(not c.isalnum() and not c.isspace() for c in data)
# NOTE: This approach is more precise -- it excludes spaces and newlines
# from the "special characters" count by checking "not c.isspace()"
print("Number of alphabets:", alphabets)
print("Number of digits:", digits)
print("Number of special characters:", special_characters)
f.close()

# =============================================================================
# SECTION 9: Character Count Per Line
# =============================================================================
#
# Time Complexity: O(n) where n is total characters
# Space Complexity: O(k) where k is the longest line length

## Write a program to calculate the characters in each line of a file
## and print the line number along with the character count

# Approach 1: Using a manual line counter
f = open("tp.txt", "r")
line_number = 1
for line in f:
    char_count = len(line)
    # NOTE: len(line) includes the \n newline character at the end of each line.
    # To exclude it, use len(line.strip()) or len(line.rstrip('\n'))
    print(f"Line {line_number}: {char_count} characters")
    line_number += 1
f.close()

# TIP: You can use enumerate() instead of a manual counter:
# for line_number, line in enumerate(f, start=1):
#     print(f"Line {line_number}: {len(line)} characters")

# OR

# Approach 2: Read all at once, split into words (NOT lines!)
# WARNING: This approach has a flaw -- data.split() splits by whitespace (words),
# NOT by lines. So each "Line" here is actually a WORD, not a line.
# To split by lines, use data.split("\n") or data.splitlines()
f = open("tp.txt", "r")
data = f.read()
lst = data.split()  # This splits into WORDS, not lines!
print(lst)
for i in range(0, len(lst)):
    char_count = 0
    for j in lst[i]:
        char_count += 1
    print(f"Line {i + 1}: {char_count} characters")
f.close()

# =============================================================================
# SECTION 10: Word Count Per Line
# =============================================================================
#
# Time Complexity: O(n) where n is total characters (splitting scans all chars)
# Space Complexity: O(k) per line where k is the number of words in that line

# Write a program to count the number of words in each line of a file
# and print the line number along with the word count

# Approach 1: Using a manual line counter
f = open("tp.txt", "r")
line_number = 1
for line in f:
    word_count = len(line.split())
    print(f"Line {line_number}: {word_count} words")
    line_number += 1
f.close()

# OR

# Approach 2: Read all, split by newline, then count words per line
f = open("tp.txt", "r")
data = f.read()
lst = data.split("\n")  # Split by newline to get individual lines
for i in range(0, len(lst)):
    word_count = len(lst[i].split())
    print(f"Line {i + 1}: {word_count} words")
f.close()

# OR

# Approach 3: Manual word counting within each line
f = open("tp.txt", "r")
line_number = 1
for line in f:
    word_count = 0
    for word in line.split():
        word_count += 1
    print(f"Line {line_number}: {word_count} words")
    line_number += 1
f.close()

# =============================================================================
# SECTION 11: Replacing Characters in a File
# =============================================================================
#
# IMPORTANT CONCEPT: Strings in Python are IMMUTABLE.
# This means you CANNOT change a string in place. Any operation that
# "modifies" a string actually creates a NEW string.

f2 = open("tp.txt", "r")
print(f2.read())
f2.close()

# Write a program where alphabets are replaced with # and digits are
# replaced with * and special characters are replaced with 0

# -------------------------------------------------------------------------
# BUG (original code):
#   f = open("tp.txt", "r")
#   data = f.read()
#   for i in data:
#       if i.isalpha():
#           data.replace(i, "#")      <-- BUG! Return value is IGNORED
#       elif i.isdigit():
#           data.replace(i, "*")      <-- BUG! Return value is IGNORED
#       else:
#           data.replace(i, "0")      <-- BUG! Return value is IGNORED
#   f.close()
#
# WHY THIS DOESN'T WORK:
#   str.replace() does NOT modify the string in place -- it RETURNS a new
#   string with the replacements. Since strings are IMMUTABLE in Python,
#   you MUST capture the return value:
#       data = data.replace(i, "#")   <-- This saves the new string back
#
#   Without "data = ", the new string is created and immediately discarded.
#   The variable "data" still holds the original unchanged string.
#
#   This is one of the most common Python mistakes for beginners!
#
# ADDITIONAL ISSUE with the loop approach:
#   Even with "data = data.replace(i, '#')", this approach has a subtle bug:
#   In the first iteration, all alphabets get replaced with "#". But then
#   in subsequent iterations, those "#" characters aren't alpha or digit,
#   so they get replaced with "0" in the else branch. The loop modifies
#   characters that were already replaced!
# -------------------------------------------------------------------------

# --- Original BUGGY code (kept for reference -- DO NOT USE) ---
f = open("tp.txt", "r")
data = f.read()
for i in data:
    if i.isalpha():
        data.replace(i, "#")       # BUG: return value not captured!
    elif i.isdigit():
        data.replace(i, "*")       # BUG: return value not captured!
    else:
        data.replace(i, "0")       # BUG: return value not captured!
f.close()
f = open("tp.txt", "r")
print(f.read())  # File is unchanged because data.replace() results were discarded
f.close()


# --- CORRECT version using "with" and a generator expression ---
# This is the proper way to do character-by-character replacement.
# It processes each character ONCE, deciding what to replace it with.
#
# How it works:
# 1. Read the file content
# 2. Use a generator expression to transform each character:
#    - alphabet -> "#"
#    - digit    -> "*"
#    - other    -> "0"
# 3. "".join() combines all transformed characters into one string
# 4. Write the new string back to the file
#
# Time Complexity: O(n) where n is the number of characters
# Space Complexity: O(n) for the new string

with open("tp.txt", "r") as f:
    data = f.read()

new_data = "".join(
    "#" if c.isalpha() else "*" if c.isdigit() else "0"
    for c in data
)
# This is a generator expression inside "".join()
# It's like a for loop compressed into one line:
#   result = []
#   for c in data:
#       if c.isalpha():
#           result.append("#")
#       elif c.isdigit():
#           result.append("*")
#       else:
#           result.append("0")
#   new_data = "".join(result)

with open("tp.txt", "w") as f:
    f.write(new_data)

# WHY the "with" version is better:
# 1. File is automatically closed (even if an error occurs)
# 2. Each character is processed exactly once (no double-replacement bug)
# 3. Uses a generator expression (memory efficient -- doesn't build a list)
# 4. Cleaner, more readable code

# =============================================================================
# SECTION 12: File Copying
# =============================================================================
#
# To copy a file's contents, read from the source and write to the destination.
# This is a basic approach -- for production code, use the shutil module:
#   import shutil
#   shutil.copy("source.txt", "destination.txt")
#
# Time Complexity: O(n) where n is the file size
# Space Complexity: O(n) because we read the entire file into memory

###########################################################################################################################################################################################################################################################################################################################################################################################################################################
f5 = open("abc.txt", "w")
f5.write("Hello World")
f5.write("\nThis is a test file")
f5.write("jsfuiwefncshuiuewifw88q392e[0wchkncx9uqw90rfq39u89qw89r87r2ihuchasd89qwy98h ]")
f5.write("2392809480ue!!@&*&@&*#%^%^!&*!*(!())_#&*&^%%^$$@#$%^&*()(&*^%$%#FYTUJHGFGHVBN")
f5.close()

f6 = open("abc.txt", "r")
print(f6.read())
f6.close()

# Copy contents of abc.txt into abc1.txt
f6 = open("abc.txt", "r")
data = f6.read()
f7 = open("abc1.txt", "w")
f7.write(data)
f7.close()
f6.close()

# BETTER version using "with" (automatically closes both files):
# with open("abc.txt", "r") as source, open("abc1.txt", "w") as dest:
#     dest.write(source.read())

###########################################################################################################################################################################################################################################################################################################################################################################################################################################

# =============================================================================
# SECTION 13: The "with" Statement (Context Manager) -- Summary
# =============================================================================
#
# Throughout this file, we've used open()/close() manually. The BETTER way
# is the "with" statement, which automatically closes the file.
#
# Manual approach (error-prone):
#   f = open("file.txt", "r")
#   data = f.read()
#   f.close()        # Easy to forget! And if an error occurs above,
#                    # f.close() never runs and the file stays open.
#
# "with" approach (recommended):
#   with open("file.txt", "r") as f:
#       data = f.read()
#   # f is automatically closed here, even if an exception occurred
#
# The "with" statement works with any "context manager" object -- files,
# database connections, network sockets, locks, etc. The key idea is:
#   - __enter__() runs at the start (opens the resource)
#   - __exit__() runs at the end (closes the resource, guaranteed)

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
# 1. "w" mode overwrites; "a" mode appends; "r" mode reads (file must exist).
# 2. Always close files with f.close(), or better, use "with open(...) as f:".
# 3. f.read() reads the whole file; iterate with "for line in f:" for large files.
# 4. str.split() splits on whitespace by default; split("\n") splits on newlines.
# 5. STRINGS ARE IMMUTABLE: str.replace() returns a NEW string -- you must
#    capture it: data = data.replace(old, new)
# 6. For character-by-character transformation, use "".join(generator_expression).
# 7. For copying files in production, use shutil.copy() instead of manual read/write.
# 8. Use enumerate(f, start=1) instead of manual line counters.
