"""
File handling in Python:
used to perform operations on files like opening, reading, writing, appending, closing, etc.

syntax:
file_object = open("filename", "mode") # mode: r, w, a, r+, w+, a+, rb, wb, ab, rb+, wb+, ab+

(read, write, append, read/write, binary read, binary write, binary append, binary read/write)
eg. 
f = open("test.txt", "r") # open file in read mode
f = open("test.txt", "w") # open file in write mode
f = open("test.txt", "a") # open file in append mode
f = open("test.txt", "r+") # open file in read/write mode
f = open("test.txt", "w+") # open file in write/read mode
f = open("test.txt", "a+") # open file in append/read mode
f = open("test.txt", "rb") # open file in binary read mode
f = open("test.txt", "wb") # open file in binary write mode
f = open("test.txt", "ab") # open file in binary append mode
f = open("test.txt", "rb+") # open file in binary read/write mode
f = open("test.txt", "wb+") # open file in binary write/read mode
f = open("test.txt", "ab+") # open file in binary append/read mode
"""
f = open("test.txt", "w") # open file in write mode
f.write("Hello World") # write to file
f.write("\nThis is a test file") # write to file
f.write("\nThis is a test file") # write to file
f.close() # close file

f1 = open("test.txt", "r") # open file in read mode
print(f1.read()) # read file
f1.close() # close file

# write a program to count the number of characters in a file
f = open("test.txt", "r")
count = 0
for line in f:
    count += len(line)
print("Number of characters in file:", count)
f.close()

# OR
f = open("test.txt", "r")
count = len(f.read())
print("Number of characters in file:", count)
f.close()

# OR
f = open("test.txt", "r")
data = f.read()
print("Number of characters in file:", len(data))
f.close()

# write a program to count the number of words in a file
f = open("test.txt", "r")
count = 0
for line in f:
    words = line.split()
    count += len(words)
print("Number of words in file:", count)
f.close()

# OR

f = open("test.txt", "r")
count = len(f.read().split())
print("Number of words in file:", count)
f.close()

#OR

f = open("test.txt", "r")
data = f.read()
words = data.split()
print("Number of words in file:", len(words))
f.close()

## Write a program to find the maximum length word and minimum length word in a file
f = open("test.txt", "r")
words = f.read().split()
max_word = max(words, key=len)
min_word = min(words, key=len)
print("Maximum length word:", max_word)
print("Minimum length word:", min_word)
f.close()

# OR
f = open("test.txt", "r")
max_word = ""
min_word = ""
for line in f:
    words = line.split()
    for word in words:
        if len(word) > len(max_word):
            max_word = word
        if len(word) < len(min_word) or min_word == "":
            min_word = word
print("Maximum length word:", max_word)
print("Minimum length word:", min_word)
f.close()

# OR

f = open("test.txt", "r")
data = f.read()
words = data.split()
max_word = max(words, key=len)
min_word = min(words, key=len)
print("Maximum length word:", max_word)
print("Minimum length word:", min_word)
f.close()

# OR

f = open("test.txt", "r")
data = f.read()
lst = data.split()
max_word = lst[0]
min_word = lst[0]
for word in lst:
    if len(word) > len(max_word):
        max_word = word
    if len(word) < len(min_word):
        min_word = word
print("Maximum length word:", max_word)
print("Minimum length word:", min_word)
f.close()

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

## Write a program to count the number of alphabets, digits and special characters in a file
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
print("Number of alphabets:", alphabets)
print("Number of digits:", digits)
print("Number of special characters:", special_characters)
f.close()

# OR

f = open("tp.txt", "r")
data = f.read()
alphabets = sum(c.isalpha() for c in data)
digits = sum(c.isdigit() for c in data)
special_characters = sum(not c.isalnum() and not c.isspace() for c in data)
print("Number of alphabets:", alphabets)
print("Number of digits:", digits)
print("Number of special characters:", special_characters)
f.close()

## Write a program to calculate the characters in each line of a file and print the line number along with the character count
f = open("tp.txt", "r")
line_number = 1
for line in f:
    char_count = len(line)
    print(f"Line {line_number}: {char_count} characters")
    line_number += 1
f.close()

# OR

f = open("tp.txt", "r")
data = f.read()
lst = data.split()
print(lst)
for i in range(0, len(lst)):
    char_count = 0
    for j in lst[i]:
        char_count += 1
    print(f"Line {i + 1}: {char_count} characters") 
f.close()

# Write a program to count the number of words in each line of a file and print the line number along with the word count
f = open("tp.txt", "r")
line_number = 1
for line in f:
    word_count = len(line.split())
    print(f"Line {line_number}: {word_count} words")
    line_number += 1
f.close()  

# OR

f = open("tp.txt", "r")
data = f.read()
lst = data.split("\n")
for i in range(0, len(lst)):
    word_count = len(lst[i].split())
    print(f"Line {i + 1}: {word_count} words")  
f.close()

#OR

f = open("tp.txt", "r")
line_number = 1
for line in f:
    word_count = 0
    for word in line.split():
        word_count += 1
    print(f"Line {line_number}: {word_count} words")
    line_number += 1
f.close()

