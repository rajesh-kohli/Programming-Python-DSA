"""

"""
# %% [markdown]
# OS Module
#
### Library
# - A collection of packages and modules
# - eg. Numpy, sklearn, tensorflow, pytorch
### Package
# - Collection of modules, but is organized in the form of directory
# - pandas, matplotlib
### Modules
# - a single python file with .py extension
# - eg. math, os, time, etc.

#### There are two types of modules in Python:
# - Predefined module - already defined in the language
# - User defined module

##### OS module
# - with this module, python can interact with the operating system
# - let's say through Python, if user wants to interact with the OS, we use this module
# - we can control some functionality of Operating system through OS module
# %%

import os
# %%
os.system("notepad") ## opens the notepad application - similar to what works on terminal / cmd prompt
os.system("chrome")
os.system("WhatsApp")
# %%
inp = int(input("enter an input"))
if inp == 1:
    os.system("OneNote")
if inp == 2:
    os.system("chrome")

"""
Now let's say if I give a prompt instead like:
 - Can you please open notepad for me?
 - open chrome
"""

inp = input("enter the input")
if "notepad" in inp:
    os.system("notepad")
if "chrome" in inp:
    os.system("chrome")


os.system("chrome")
# %%
import os
os.system("Notes")
# %%

import webbrowser
webbrowser.open("https:www.google.com")
# %%
f = open("abc.txt","r")
print(f.read())
f.close()
# %%
