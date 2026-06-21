# Wrting code in either Function or Class is the right way to write a code
# Function is a block of code, with a set of instructions to perform a particular task
# Eg. Task - Calculator. Create different functions: add() sub() mul() div()

#Syntax:
    # def function_name(arguments):
    #    function body


# def --> Keyword
# function_name --> identifier
# arguments --> parameters (optional)
# function_body --> instruction within a function

# To execute a function, we need to call it
#function calling
    # function_name(arguments)
    # arguments --> function may or maynot have arguments

#Example - Function Definition
def my_function():
    print("Printing my function")

# Function calling to execute it
my_function()

# Why do we use functions:
# 1. Function: contains a block of code with a set of instructions
# 2. Modules: Whenever we have a larger program, we can divide the program into small blocks of code 
# called modules. Modularity concept. We achieve modularity in Python by writing a function
# 3. Reusability: Once we write a function, we can call the same function any number of times

#Example - addition of two numbers
def add(a,b):    ## Function definition
    sum = a+b
    print(sum)

add(112,123)   ## Function calling

# There is no priority attached to a function. Whichever function is called will be executed

# return: is a statement that returns a value to the function being called

def func1(a,b):
    ans = func2(3,4)
    # print(ans)
    return a+b

def func2(x,y):
    return x+y

print(func1(5,6))   

# Another example
def fun1(a,b):
    fun2(5,6)
    x = fun3()
    return a+b*b

def fun2(p,q):
    return p+q-2
        
def fun3():
    return 5

fun1(6,7)
    