"""
str - introduction to strings in Python
A string is a built-in data structure that is used to store a sequence of characters.
s[i] - access the character at index i
s[i:j] - access the substring from index i to j-1
s[i:j:k] - access the substring from index i to j-1 with step k
s[::-1] - reverse the string
s[i] = 'a' - strings are immutable, so this will raise an error
s[-1] - access the last character of the string
len(s) - get the length of the string
String objects won't support item assignment - strings are immutable, so you cannot change a character in a string.
You can create a new string by concatenating or slicing.
String supports many built-in methods like upper(), lower(), strip(), split(), join(), find(), replace(), etc.
Just like lists, strings can be iterated over using a for loop.
Also like lists and tuples, strings support membership testing using the in and not in operators, as well as comparison operators.
"""
s = "coding"
print(len(s))  # 6
print(s[0])    # c
print(s[-1])   # g
print(s[1:4])  # odi
print(s[::-1]) # gnidoc
# Remember whenever you are creating a slice, you are creating a copy / new string, not modifying the original string.
print(type(s))  # <class 'str'>
# We use the built-in str ( ) to obtain the string representation of an object. 

y = str(123)
print(type(y))  # <class 'str'>

z = str([1, 2, 3])
print(type(z))  # <class 'str'>

w = str({'a': 1, 'b': 2})
print(type(w))  # <class 'str'>


"""
Looping over Python strings:
You can loop over a string using a for loop, just like you would with a list or tuple.
Each iteration of the loop will give you one character from the string.

eg.
for char in s:
    print(char) 

"""
for char in s:
    print(char) 

i = 0
while i < len(s):
    print(s[i])
    i += 1

"""
Basic Operations on a String Object :
Length of a string: len(s)
Changing Case of a string: s.upper(), s.lower()
String Concatenation: s1 + s2
String Comparision: s1 == s2, s1 != s2, s1 < s2, s1 > s2
String Copy: s1 = s2
String Reverse: s[::-1]
Check for existence of a substring in a string: 'substring' in s
Searching for a substring in a string: s.find('substring')
Replacing a substring in a string: s.replace('old', 'new')
Removing Whitespaces from a string: s.strip()
"""

s = "  Hello, World!  "
# find the length of the string
print(len(s))          # 17
# remove leading and trailing whitespaces
print(s.strip())       # "Hello, World!"
# convert the string to uppercase and lowercase
print(s.upper())       # "  HELLO, WORLD!  "
print(s.lower())       # "  hello, world!  "
# check if the string starts with a substring
print(s.startswith("  Hello"))  # True
# check if the string ends with a substring
print(s.endswith("World!  "))    # True 
# check if a substring exists in the string
print("World" in s)    # True
# find the index of a substring in the string
print(s.find("World"))  # 9
# replace a substring in the string
print(s.replace("World", "Python"))  # "  Hello, Python!  "
# if you want to replace all occurrences of a substring in the string, you can use the replace() method with the count parameter set to -1 (default value).
s = "Hello, World! Hello, Python!"
print(s.replace("Hello", "Hi"))  # "Hi, World! Hi, Python!"
print(s.replace("Hello", "Hi", 1))  # "Hi, World! Hello, Python!" # only the first occurrence of "Hello" is replaced with "Hi"
# and to delete a substring from a string, you can use the replace() method with the substring to be deleted and an empty string as the replacement.
s = "Hello, World! Hello, Python!"
print(s.replace("Hello", ""))  # ", World! , Python!" # all occurrences of "Hello" are deleted from the string
print(s.replace("Hello", "", 1))  # ", World! Hello, Python!" # only the first occurrence of "Hello" is deleted 
# strip the string of leading and trailing whitespaces
print(s.strip())       # "Hello, World! Hello, Python!"
# lstrip the string of leading whitespaces
print(s.lstrip())      # "Hello, World! Hello, Python!"
# rstrip the string of trailing whitespaces
print(s.rstrip())      # "Hello, World! Hello, Python!"
# split the string into a list of substrings
print(s.split(","))    # ['  Hello', ' World!  ']
# concatenate two strings
s1 = "Hello"
s2 = "World"
print(s1 + " " + s2)   # "Hello World"
# compare two strings -
# lexicographically which means based on the alphabetical order of the characters in the strings
# and then ASCII values of the characters in the strings to determine the order of the strings. 
# if all characters match, then the shorter string is considered smaller which means it comes first in the order.
# And then you look at the length of the strings. If they are equal, then the strings are considered equal.
# Example: "Hello" < "World" because 'H' < 'W' in ASCII values. More examples:
# "abc" < "abd" because 'c' < 'd' in ASCII values. 
# "abc" < "abcd" because the first three characters match, but the first string is shorter.
# You won't use length to compare strings, but it is used to determine if two strings are equal or not.
# "abcd" < "x" because 'a' < 'x' in ASCII values.
# it's linear time complexity O(n) where n is the length of the strings being compared.
print(s1 == s2)        # False
print(s1 != s2)        # True
print(s1 < s2)         # True
print(s1 > s2)         # False
# copy a string
s3 = s1
print(s3)              # "Hello"
s1 = "abc"
s2 = "abd"

if s1 == s2:
    print(s1, " == ", s2)
elif s1 < s2:
    print(s1, " < ", s2)
else:
    print(s1, " > ", s2)
# there is also a copy module in Python that provides a way to create shallow and deep copies of objects, including strings.
# reverse a string
print(s[::-1])         # "  !dlroW ,olleH  "
# there is also reversed() function in Python that returns an iterator that accesses the given sequence in the reverse order.
# eg. list(reversed(s)) will give you a list of characters in reverse order. and then you can use ''.join(list(reversed(s))) to get the reversed string.
# and .reverse method that reverses the elements of a list in place. eg. s_list = list(s); s_list.reverse(); reversed_s = ''.join(s_list)

# capitalize the first letter of each word in a string
s = "hello world"
print(s.title())  # "Hello World"
# capitalize the first letter of the string
print(s.capitalize())  # "Hello world"

# in, not in, isalpha(), isdigit(), isspace(), islower(), isupper(), istitle() are some other useful string methods.
s = "hi today is 8th July"
print(s.isalpha())  # False # isalpha() returns True if all the characters in the string are alphabetic and there is at least one character, otherwise it returns False. In this case, the string has spaces and digits, so it returns False.
print(s.isdigit())  # False # isdigit() returns True if all the characters in the string are digits and there is at least one character, otherwise it returns False. In this case, the string has alphabetic characters and spaces, so it returns False.
print(s.isspace())  # False # isspace() returns True if all the characters in the string are whitespace and there is at least one character, otherwise it returns False. In this case, the string has alphabetic characters and digits, so it returns False.
print(s.islower())  # True # islower() returns True if all the characters in the string are lowercase and there is at least one character, otherwise it returns False. In this case, the string has lowercase letters, so it returns True.
print(s.isupper())  # False # isupper() returns True if all the characters in the string are uppercase and there is at least one character, otherwise it returns False. In this case, the string has lowercase letters, so it returns False.
print(s.istitle())  # False  # istitle() returns True if the string is a titlecased string, which means the first character of each word is uppercase and the rest are lowercase. In this case, the string is not titlecased, so it returns False.

print(s.isalnum())  # False # isalnum() returns True if all the characters in the string are alphanumeric (either alphabetic or digits) and there is at least one character, otherwise it returns False. In this case, the string has spaces, so it returns False.
print(s.isprintable())  # True # isprintable() returns True if all the characters in the string are printable or the string is empty, otherwise it returns False. In this case, the string has printable characters, so it returns True.

print(s.isidentifier())  # False # isidentifier() returns True if the string is a valid identifier according to the Python language definition, otherwise it returns False. In this case, the string has spaces and digits, so it returns False.
print(s.isascii())  # True # isascii() returns True if all the characters in the string are ASCII characters (i.e., have a Unicode code point less than 128), otherwise it returns False. In this case, the string has ASCII characters, so it returns True.
print(s.isnumeric())  # False # isnumeric() returns True if all the characters in the string are numeric characters and there is at least one character, otherwise it returns False. In this case, the string has alphabetic characters and spaces, so it returns False.
print(s.isdecimal())  # False # isdecimal() returns True if all the characters in the string are decimal characters and there is at least one character, otherwise it returns False. In this case, the string has alphabetic characters and spaces, so it returns False.

# in
print("today" in s)  # True
# not in
print("tomorrow" not in s)  # True

print(s.find("today"))  # 3 # find() returns the index of the first occurrence of the substring in the string, otherwise it returns -1. In this case, the substring "today" is found at index 3.
print(s.index("today"))  # 3 # index() returns the index of the first occurrence of the substring in the string, otherwise it raises a ValueError. In this case, the substring "today" is found at index 3.
print(s.rfind("is"))  # 11 # rfind() returns the index of the last occurrence of the substring in the string, otherwise it returns -1. In this case, the substring "is" is found at index 11.

# use find and rfind over index and rindex, as index throws a value error if the value is not present, and then you would have to do exception handling

"""
Splitting a string into a list of substrings using the split() method.
The split() method takes a delimiter as an argument and splits the string into a list of substrings based on that delimiter. 
If no delimiter is provided, it splits the string based on whitespace.
"""

sports = "soccer, basketball, baseball, football"
# split the string into a list of substrings using the default delimiter (whitespace)
print(sports.split())  # ['soccer,', 'basketball,', 'baseball,', 'football']
# split the string into a list of substrings using a comma as the delimiter
print(sports.split(","))  # ['soccer', ' basketball', ' baseball', ' football']
# split the string into a list of substrings using a comma and space as the delimiter
print(sports.split(", "))  # ['soccer', 'basketball', 'baseball', 'football']
# split the string into a list of substrings using a comma and space as the delimiter and limit the number of splits to 2
print(sports.split(", ", 2))  # ['soccer', 'basketball', 'baseball, football']

Sun = "the sun is shining bright"
# split the string into a list of substrings using the default delimiter (whitespace)
print(Sun.split())  # ['the', 'sun', 'is', 'shining', 'bright']
# split the string into a list of substrings using a space as the delimiter
print(Sun.split(" "))  # ['the', 'sun', 'is', 'shining', 'bright']
# split the string into a list of substrings using a space as the delimiter and limit the number of splits to 2
print(Sun.split(" ", 2))  # ['the', 'sun', 'is shining bright']

"""
Joining a String - if I have a list of strings and I want to join them into a single string, I can use the join() method.
The join() method takes a list of strings as an argument and joins them into a single string using the string as a delimiter.
"""
fruits = ["apple", "banana", "cherry"]
# join the list of strings into a single string using a comma and space as the delimiter
print(", ".join(fruits))  # "apple, banana, cherry"
x = " ".join(fruits)  # "apple banana cherry"
print(x) # "apple banana cherry"
print(type(x))  # <class 'str'>

"""
String Interpolation :
It is the process of inserting values (variables or expressions) into a string.

f-strings (formatted string literals) are a way to do string interpolation in Python.
f-strings are prefixed with the letter 'f' or 'F' and use curly braces {} to evaluate expressions inside the string.
f-strings are available in Python 3.6 and later versions.
f-strings are faster than the older methods of string formatting (%, str.format(), and concatenation) because they are evaluated at runtime and do not require any additional function calls.
"""
country = "India"
year = 1947
# using f-strings # new way of doing string interpolation, much more readable, simple and concise
print(f"{country} gained independence in {year}.")  # "India gained independence in 1947."
# using str.format() # old way of doing string interpolation
print("{} gained independence in {}.".format(country, year))  # "India gained independence in 1947."
# using concatenation # old way of doing string interpolation
print(country + " gained independence in " + str(year) + ".")  # "India gained independence in 1947."

"""
Check Palindrome:
Given a string represented as a character arrays, check it is a palindrome or not.
Example:
Input : "racecar"
Output : true
Input : "rotator"
Output : true
"""
s == s[::-1]  # True if s is a palindrome, False otherwise
# this approach takes O(n) linear time and O(n) space due to copy, where n is the length of the string.
# If I don't want to use extra space by creating a copy, I can use two pointers approach to check if the string is a palindrome or not.
# i = 0, j = len(s) - 1
# while i < j:
#     if s[i] != s[j]:
#         return False
#     i += 1
#     j -= 1
# return True
# In this approach, we are doing n/2 comparisons, so the time complexity is O(n) and the space complexity is O(1) constant space.
# n/2 comparisons is still O(n) linear time complexity, because we drop the constant factor when analyzing time complexity.
# even though both approaches have the same time complexity, the second approach is more space efficient because it doesn't create a copy of the string. And also, n/2 is better than 2*n

def isPalindrome(s:str)->bool:
    i, j = 0, len(s)-1
    while i < j:
        if s[i] == s[j]:
            i += 1
            j -= 1
        else:
            # s is not a palindrome
            return False
    # s is a palindrome
    return True

s = input()
if isPalindrome(s):
    print("palindrome")
else:
    print("not a palindrome")

# can also do the above if else this way
print("palindrome") if isPalindrome(s) else print("not a palindrome")

"""
Valid Palindrome: Leetcode
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters 
and removing all non-alphanumeric characters, it reads the same forward and backward. 
Alphanumeric characters include letters and numbers.
Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

"""
def isPalindrome(s:str)->bool:
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():
            # skip the ith character
            i += 1
        elif not s[j].isalnum():
            # skip the jth character
            j -= 1
        else:
            if s[i].lower() == s[j].lower():
                i += 1
                j -= 1
            else:
                # s is not a palindrome
                return False
        # s is a palindrome
        return True

# currently my input string is constant, that's why the .isalnum and .lower operations are constant. They depend on the length of the string

"""
Check Anagrams:
Given a two strings represented as a character arrays, check if they are anagrams.
note : assume characters the input strings are lowercase letters ( a - z ).
Example:

Input : "state" and "taste"
Output : true

Input : "abacbac" and "aabbbcc"
Output : false
"""
# one solution is to build a frequency map for both the strings and compare them
# another solution is we can also sort both the strings and then compare
# how do you sort a string because string class doesn't offer any .sort() function like list
# In sorted function you can pass any object - string, tuple or list and would return a list with sorted elements



def is_anagram(s1:str, s2:str)->bool:
    sorted_s1 = "".join(sorted(s1))
    print(sorted_s1)
    sorted_s2 = "".join(sorted(s2))
    print(sorted_s2)
    return sorted_s1 == sorted_s2

s1 = input()
s2 = input()

print ("anagram") if is_anagram(s1, s2) else print("not an anagram")

# we assume both the strings length is n - that's only when they would be considered an anagram
# sorting is nlogn
# time = nlogn (for sorting s1) + nlogn (for sorting s2) + n (for comparing) ~ O(nlogn) = total time
# space: sorting function returns a copy, so that's linear. So total space is n + n ~ O(n)

## The other solution was frequency map - for which we can use dictionary

def is_anagram(s1:str, s2:str)->bool:
    f1 = {}
    for ch in s1:
        # if ch in f1:
        #     f1[ch] += 1
        # else:
        #     f1[ch] = 1
        f1[ch] = f1.get(ch,0) + 1 # does the same thing as if else above
        
# there is another way to do this - using default dictionary

from collections import defaultdict
def is_anagram(s1:str, s2:str)->bool:
    f1 = defaultdict(int)
    for ch in s1:
        f1[ch] += 1
    
    f2 = defaultdict(int)
    for ch in s2:
        f2[ch] += 1
        
    return f1 == f2

# time: n (to build f1) + n (to build f2) + 26 (to compare) ~ O(n)
# space: 26 (for dict1) + 26 (for dict2) = constant

# this is a better option because here space is constant and time is linear which is better than nlogn
 
# remember - dictionary preserves the order of elements, and we can still compare two dictionaries using == because it compares based on content / elements, not the order


## we can also do this with just one frequency map instead of two - do this yourself

# another option: all(x == 0 for x in f1.values())


## how we wrote code above to build frequency map
# similar to how there is a special class - defaultdict
# there is another special class - counter whose only purpose is to build frequency map only

from collections import Counter
def is_anagram(s1:str, s2:str)->bool:
    # f1 = Counter(s1)
    # print(f1)
    # f2 = Counter(s2)
    # print(f2)
    # return f1 == f2
    return Counter(s1) == Counter(s2) # can be done in a single line

"""
https://www.w3schools.com/python/ref_module_collections.asp
"""
# most_common() function - gives all key-value pairs sorted by values in decreasing order
# what if - To build a frequency map without using dict, defaultdict, or any built-in containers (like list, set, or tuple)

# we can build a frequency array with size 26
# we can build an array of size 26 - where index 0 tracks frequency of a and so on with index 25 tracks frequency of z
# one challenge here is how do we do mapping of a to 0, b to 1, c to 2 and so on
# for this we can use ASCII values where we subtract any character ASCII value from a
# subtract a's ascii value from the ascii values of other alphabets
# or we can also do ordinal values subtraction - ord(ch) - ord('a')

def is_anagram(s1:str, s2:str)->bool:
    f1 = [0] * 26
    for ch in s1:
        idx = ord(ch) - ord('a')
        f1[idx] += 1
    print(f1)
    
    f2 = [0] * 26
    for ch in s2:
        f2[ord(ch) - ord("a")] += 1 #in the s1 for loop we have defined idx variable, we can also do directly but the above code is more readable

    print(f2)
    
    return f1 == f2

# now this is also linear time and constant space compexity
# so which one do we use
# Always prefer array as a map because all operations are much faster here, compared to dictionaries, etc
# freq array will be faster as we know size is fixed i.e.  26
# you will notice in Dynamic programming where we will mostly use array as a map
# there will be some situations where you can't use array as a map and there we will use dictionaries and built in containers where we can't use default indexing

"""
Count Palindromic Substrings
Given a string s, design an algorithm to count the no. of palindromic substrings in it.
"""

