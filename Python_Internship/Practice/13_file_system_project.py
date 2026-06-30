"""
Lecture 13: Mini-Project -- Building a File System with Dictionaries
=====================================================================
Topics Covered:
  - Combining functions + dictionaries + file handling
  - Dictionary .get() method with default values
  - The __name__ == "__main__" pattern
  - Creating, reading, and listing files

PROJECT OVERVIEW:
  We build a simple "file system" using a Python dictionary.
  - The dictionary keys are file names (strings)
  - The dictionary values are file contents (strings)
  - Each operation also writes to actual files on disk, so the data persists

  This project demonstrates how functions, dictionaries, and file handling
  work together to build something useful.

  file_system = {
      "notes.txt": "Hello World",
      "todo.txt": "Buy groceries",
      ...
  }

MENTAL MODEL -- dict as a tiny "file system":
  Think of the dictionary as a flat directory listing: each key is a
  filename, each value is that file's full contents. There are no folders
  here, just a single flat namespace -- exactly like one folder on disk
  with no subfolders.

      file_system (dict)              disk (mirrored by every call)
      +----------------+----------+   +-----------------------+
      | KEY (filename) | VALUE    |   | notes.txt             |
      +----------------+----------+   |   Hello World         |
      | "notes.txt"    | "Hello.."|   +-----------------------+
      | "todo.txt"     | "Buy..." |   | todo.txt              |
      +----------------+----------+   |   Buy groceries       |
                                       +-----------------------+

  Every function below keeps these two views in sync: it writes/reads the
  real file on disk AND updates the in-memory dict so lookups stay O(1)
  without re-reading from disk each time.
"""

# =============================================================================
# SECTION 1: The File System Dictionary (Global State)
# =============================================================================
#
# This dictionary acts as an in-memory "index" of all files.
# It mirrors what's on disk, giving us fast O(1) lookups by filename
# without having to read from disk every time.
#
# Time Complexity for dictionary operations:
#   - Lookup (file_system[key]):      O(1) average
#   - Insert (file_system[key] = v):  O(1) average
#   - Delete (del file_system[key]):  O(1) average
#   - List all (file_system.keys()):  O(n) where n = number of files
#
# Space Complexity: O(n * m) where n = number of files, m = average content size

# We do it through dictionaries where the file_name is the key and the
# contents of the file is the value.
#
# I need to write a function that creates new files in the file system.
# And also a function that add contents to a particular file name in the file system.

file_system = {}


# =============================================================================
# SECTION 2: create_file() -- Create a New File
# =============================================================================

def create_file(file_name, contents=""):
    """
    Create a new file on disk and add it to the file system dictionary.
    If the file already exists, it is overwritten with the new contents.

    :param file_name: The name of the file to be created.
    :param contents: The contents of the file to be created.
                     Defaults to "" (empty string) -- this is a default parameter.
    :return: None

    Time Complexity: O(m) where m = length of contents (for writing)
    Space Complexity: O(m) for storing contents in the dictionary

    NOTE: Using "w" mode means if the file already exists, its contents are
    completely replaced. If you want to prevent accidental overwrites, you
    could check "if file_name in file_system:" first and raise an error.
    """
    # "with" automatically closes the file when the block ends
    with open(file_name, "w") as f:
        f.write(contents)
    # Also store in our in-memory dictionary for quick access
    file_system[file_name] = contents


# =============================================================================
# SECTION 3: add_contents() -- Append to an Existing File
# =============================================================================

def add_contents(file_name, contents):
    """
    Append contents to a file on disk and update the file system dictionary.
    If the file does not exist, it is created first.

    :param file_name: The name of the file to be added to.
    :param contents: The contents to be added to the file.
    :return: None

    Time Complexity: O(m) where m = length of new contents
    Space Complexity: O(1) additional (string concatenation creates a new string
                      but replaces the old one)

    WHAT HAPPENS IF THE FILE DOESN'T EXIST YET?
    - If you call add_contents("new_file.txt", "data") and "new_file.txt"
      is NOT in the file_system dictionary, this function handles it:
      1. It adds the key to file_system with an empty string value
      2. Then opens the file in "a" (append) mode -- which also creates the
         file on disk if it doesn't exist
      3. Appends the new contents both to disk and to the dictionary
    - This is a defensive programming pattern -- handle edge cases gracefully
      instead of crashing with a KeyError.

    FLOW DIAGRAM (create -> add -> read):

        create_file("notes.txt", "Hello")
            file_system = {"notes.txt": "Hello"}

        add_contents("notes.txt", " World")
            file_system = {"notes.txt": "Hello World"}   <- appended, not replaced

        read_file("notes.txt")
            returns "Hello World"   <- read straight from the dict (no disk I/O)
    """
    if file_name not in file_system:
        file_system[file_name] = ""

    with open(file_name, "a") as f:
        f.write(contents)
    # String concatenation: adds new contents to existing contents in the dict
    # NOTE: += on strings creates a new string (strings are immutable), but
    # the dict reference is updated to point to the new string.
    file_system[file_name] += contents


# =============================================================================
# SECTION 4: read_file() -- Read File Contents
# =============================================================================

def read_file(file_name):
    """
    Read the contents of a file in the file system.

    :param file_name: The name of the file to read.
    :return: The contents of the file as a string.

    Time Complexity: O(1) -- dictionary lookup (reads from memory, not disk!)
    Space Complexity: O(1) -- returns a reference to the existing string

    ABOUT .get(key, default):
    - dict.get(key, default) returns the value for key if it exists,
      otherwise returns the default value.
    - This is safer than dict[key] which raises a KeyError if the key is missing.

    Example:
      file_system = {"notes.txt": "Hello"}
      file_system.get("notes.txt", "")    --> "Hello"     (key exists)
      file_system.get("missing.txt", "")  --> ""          (key missing, returns default)
      file_system["missing.txt"]          --> KeyError!   (crashes)
    """
    return file_system.get(file_name, "")


# =============================================================================
# SECTION 5: list_files() -- List All Files
# =============================================================================

def list_files():
    """
    List all files currently stored in the file system.

    :return: A list of file names.

    Time Complexity: O(n) where n = number of files (to create the list)
    Space Complexity: O(n) for the returned list

    NOTE: dict.keys() returns a "view" object, not a list. We wrap it in
    list() to get a proper list. The view object would also work for
    iteration, but a list is easier to work with (indexing, slicing, etc.)
    """
    return list(file_system.keys())


# =============================================================================
# SECTION 6: The __name__ == "__main__" Pattern
# =============================================================================
#
# WHAT IS __name__?
#   Every Python file has a special built-in variable called __name__.
#   - When you RUN a file directly (python 13_file_system_project.py),
#     __name__ is set to "__main__"
#   - When you IMPORT a file (import file_system_project),
#     __name__ is set to the module name ("file_system_project")
#
# WHY USE if __name__ == "__main__"?
#   It lets you write code that only runs when the file is executed directly,
#   NOT when it's imported as a module by another file.
#
#   Without this guard, if someone does "import file_system_project" in
#   another file, all the create_file() and print() calls below would
#   execute immediately -- which is usually not what you want.
#
# EXAMPLE:
#   # In another_file.py:
#   import file_system_project  # Only imports functions, doesn't run the demo
#
#   file_system_project.create_file("my_file.txt", "my contents")
#
# This is a standard Python pattern that you'll see in almost every
# well-structured Python project.

if __name__ == "__main__":
    # This block only runs when you execute this file directly.
    # It serves as a demo / test of the functions defined above.

    create_file("notes.txt", "Hello")     # Create a file with initial content
    add_contents("notes.txt", " World")   # Append " World" to it
    print(read_file("notes.txt"))         # Output: "Hello World"
    print(list_files())                   # Output: ["notes.txt"]

    # You can try more operations:
    # create_file("todo.txt", "Buy groceries\n")
    # add_contents("todo.txt", "Clean house\n")
    # print(read_file("todo.txt"))
    # print(list_files())  # Output: ["notes.txt", "todo.txt"]

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
# 1. Dictionaries provide O(1) average lookup -- perfect for mapping filenames
#    to contents (like a simple database or index).
# 2. dict.get(key, default) is safer than dict[key] -- it returns a default
#    value instead of crashing with a KeyError.
# 3. The "with" statement ensures files are always properly closed.
# 4. if __name__ == "__main__": prevents demo/test code from running when
#    the file is imported as a module.
# 5. Default parameter values (contents="") let callers skip optional arguments.
# 6. This project pattern (in-memory dict + on-disk files) is a simplified
#    version of how databases work: fast reads from memory, persistent
#    storage on disk.
# 7. Functions make code reusable and testable -- each operation (create, read,
#    add, list) is a separate, focused function with a clear responsibility.
