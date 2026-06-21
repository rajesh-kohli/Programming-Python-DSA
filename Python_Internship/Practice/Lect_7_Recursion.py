#Write a function to find the perimeter of a circle
# Perimeter of a circle: Circumference  = 2*pi*r

# def PerimeterOfCircle(radius):
#     return 2*3.142*radius


# import math
# def PerimeterOfCircle(radius):
#     return 2*math.pi*radius


# radius = 5
# print(PerimeterOfCircle(radius))

## Recursion: A function calling itself again and again until some condition is satisfied
# Whenever we have a repetitive problem statement: two solutions exists:
# 1. Iterative approach (loops) 2. Loops
# Dynamic Programming concept uses Recursion

# To write any code in Recursion, we need to find two steps:
# 1. Anchor / Stop Step : Where exactly we have to stop
# 2. Inductive / Recursive step: repetitive code we will write in this step

# Whenever we are performing recursion, stack data structure is getting created in stack segment of memory implicitly

# From OS point of view: memory is a collection of frames
# From Computer Architecture point of view: memeory is a collection of blocks
# From Progammmers point of view: Memory is a collection of segments --> Our focus
# Here Memory means - RAM (Primary memory of a computer)
# Memory is divided into 4 segments:
# 1. Code segment 2. Data Segment 3. Stack segment 4. Heap Segment
    # Entire code will be stored in code segment. Read only. No modifications allowed in this segment
    # All the global variables, global functions, static variables, static functions, static methods, constants are stored in Data Segment
    # Stack segment contains recursive function, local variable, local functions, recursive stack, etc.
    # Heap Segment contains dynamic data structures, objects and classes
## These concepts will come up in detail in OOP
## Stack segment wll grow --> top to down
## Heap segment will grow --> down to top

## Stack:
    # linear data structure (storing data one after the other)
    # organize data in a way that it gets structure and becomes meaningful
    # Goal: We need to organize data in Optimal way (meaning takes less space to store and less time to execute)
## Structure of Stack:
    # One side open and one side closed
    # We can insert and delete the elements from the stack from one side only
    # Stack follows LIFO or FILO (Last In First Out or First In Last Out)
    # Two standard routines in a stack:
        # Push (Inserting elements onto the stack)
        # Pop (Removing/Deleting elements from the stack) - TOS top of stack element gets deleted first
    # Backend Usecase: Browsing history
# In recursive code, stack is getting created - what will you push and pop
    # push --> recursive function call is pushed onto the stack
    # pop --> After execution, the function returns a value that we need to pop

## Recursive code for multiplication of two numbers
# 6*4 = 24
# Is multiplication a repetitive problem statement? Yes. It's repetition of addition (6+6+6+6) --> It's repetitive, so we can use Recursion here
# Mul(6,4) = 6 + mul(6, (4-1)) = 6+mul(6,3) = 6+6+mul(6,2) ... = 6+6+6+6+mul(6,0) --> anchor step = 6+6+6+6+0 = 24
# Generalized function
    # Mul(a,b) = a + Mul(a,(b-1)) when b>0 --> recursive step
    #          = 0 when b = 0 --> anchor step
    
#snippet:
    # Structure:
        #def fun():
            # anchor step
            # recursive step

# def recursive_mul(a,b):
#     if b == 0:  #anchor step
#         return 0
#     else:
#         return a + recursive_mul(a,(b-1))   #recursive step

# The elements stored in stack during Recursion are called Activation Records
# In the context of stack-based recursion, DAG - Directed Acyclic Graph - 
# represents the hidden "call graph" or history of recursive calls
# Recursion Tree - Another method to trace the code and output

def factorial(n):
    if n==0:
        return 1
    else:
        return n*factorial(n-1)

print(factorial(5))




