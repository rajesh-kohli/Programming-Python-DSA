"""
Building a File System
We do it through dictionaries where the file_name is the key and the contents of the file is the value.

I need to write a function that creates new files in the file system.
And also a function that add contents to the a particular file name in the file system.

"""

file_system = {}


def create_file(file_name, contents=""):
    """
    Create a new file on disk and add it to the file system dictionary.
    If the file already exists, it is overwritten with the new contents.
    :param file_name: The name of the file to be created.
    :param contents: The contents of the file to be created.
    :return: None
    """
    with open(file_name, "w") as f:
        f.write(contents)
    file_system[file_name] = contents


def add_contents(file_name, contents):
    """
    Append contents to a file on disk and update the file system dictionary.
    If the file does not exist, it is created first.
    :param file_name: The name of the file to be added to.
    :param contents: The contents to be added to the file.
    :return: None
    """
    if file_name not in file_system:
        file_system[file_name] = ""

    with open(file_name, "a") as f:
        f.write(contents)
    file_system[file_name] += contents


def read_file(file_name):
    """
    Read the contents of a file in the file system.
    :param file_name: The name of the file to read.
    :return: The contents of the file as a string.
    """
    return file_system.get(file_name, "")


def list_files():
    """
    List all files currently stored in the file system.
    :return: A list of file names.
    """
    return list(file_system.keys())


if __name__ == "__main__":
    create_file("notes.txt", "Hello")
    add_contents("notes.txt", " World")
    print(read_file("notes.txt"))
    print(list_files())
