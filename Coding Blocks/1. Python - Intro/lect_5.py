
"""
sum of digits of a number
"""

num = int(input("Enter a number: "))
sum = 0
while num != 0:
    digit = num % 10
    sum += digit
    num //= 10
print("Sum of digits:", sum)

# OR
num = input("Enter a number: ") ## keep it string to iterate over it
sum = 0
for digit in num:
    sum += int(digit) # convert the digit to int before adding it to sum
print("Sum of digits:", sum)

# OR using map
num = input("Enter a number: ")
total = sum(map(int, num)) # map(int, num) will convert each character in the string num to an integer, and then sum() will add them up.
print("Sum of digits:", total)

"""
Reverse a number

eg. 123 -> 321
3*10
3*10 + 2 = 32
32*10
32*10 + 1 = 321
"""
num = int(input("Enter a number: "))
rev = 0
while num != 0:
    digit = num % 10
    rev = rev * 10 + digit
    num //= 10
print("Reversed number:", rev)


# OR - read a string and then reverse it using slicing
num = input("Enter a number: ")
rev = num[::-1] # slicing to reverse the string # also can use reversed() function and join() to reverse the string
# strings are immutable in python, so we cannot change the original string, but we can create a new string that is the reverse of the original string.
# num and rev don't have the same string object in memory, they are different objects. num is the original string, and rev is the new string that is the reverse of num.
print("Reversed number:", rev) # remember that rev is a string here, if you want it as an integer, you can convert it using int(rev)

# if you don't want to create a new object rev, and just copy num and print the reverse of num, you can do it like this:
num = input("Enter a number: ")
print("Reversed number:", num[::-1]) # slicing to reverse the string   

"""
Fibonacci series - Given a non-negative integer n, find the nth Fibonacci number. The Fibonacci numbers are the numbers in the following integer sequence.
0, 1, 1, 2, 3, 5, 8
The sequence starts with 0 and 1, and each subsequent number is the sum of the previous two numbers. 
That is, fib(0) = 0, fib(1) = 1, and fib(n) = fib(n - 1) + fib(n - 2
for n > 1.
This is an important problem in coding interviews, and is a good example of dynamic programming and also used in algorithm design, recursion.
So has a lot of applications in real life, like in nature, computer science, and mathematics.

Logic:
if n == 0, we know it's 0
if n == 1, we know it's 1
so for 0 and 1, we can return the value directly.
For n > 1, we can use a loop to calculate the Fibonacci number iteratively.
2nd fibonacci number is 1, 3rd is 2, 4th is 3, 5th is 5, 6th is 8, and so on.
we can use two variables a & b to keep track of the previous two Fibonacci numbers, and update them in each iteration of the loop.
The loop needs to run n-1 times, because we already know the first two Fibonacci numbers.

"""
n = int(input("Enter a number: "))
if n == 0 or n == 1:
    print(n)
else:
    a, b = 0, 1
    for i in range(2, n + 1):
        c = a + b
        a = b
        b = c
    print(b)
    
# OR
n = int(input("Enter a number: "))
a, b = 0, 1
for i in range(n):
    a, b = b, a + b
print(a) # a will be the nth Fibonacci number after the loop ends

# OR
n = int(input("Enter a number: "))
if n == 0:
    print(0)
elif n == 1:
    print(1)
else:
    a = 0
    b = 1
    i = 1
    while i <= n - 1:
        c = a + b
        a = b
        b = c
        i += 1
    print(c) # c will be the nth Fibonacci number after the loop ends

# Time complexity: O(n) - because the loop runs exactly n times
# Space complexity: O(1) - we are using constant space, only a few variables to keep track of the previous two Fibonacci numbers

"""
Largest of N numbers
We can assign a variable msf (max so far) = -infinity , we can use math module in python to assign infinity to a variable. import math
We can assign negative infinity in two ways: - math.inf or float('-inf')
Then we can use a loop to iterate over the numbers, and if the current number is greater than msf, we can update msf to the current number.
"""
import math
nums = list(map(int, input("Enter numbers separated by space: ").split()))
msf = float("-inf") # msf is the maximum so far, and we are using float to represent infinity
for num in nums:
    if num > msf:
        msf = num
print("Largest number:", msf)

# OR
import math
nums = list(map(int, input("Enter numbers separated by space: ").split()))
msf = float("-inf")
for num in nums:
    msf = max(msf, num)
print("Largest number:", msf)

"""
-2^31 (Int Min) to 2^31-1 (Int Max) are the range of integers in python
-2^63 (Long Min) to 2^63-1 (Long Max) are the range of long in python aka LLong-Min and LLong-Max
We can use Int min/max or Long min/max when we need to find integers or longs in a range, and the problem statement specifically asks for integers and longs, and not floats.
In python, we can use sys module to get the maximum integer and the minimum integer in the range.
sys.maxsize is the maximum long in the range, and sys.maxint is the maximum integer in the range
So we can use sys.maxsize and sys.maxint to find the largest number in the range
if the range is empty, it will return positive infinity
To get negative infinity, we can use -sys.maxsize -1 (calculates as -(2^63-1) - 1 = -2^63)
-2^31 to 2^31-1 are the range of int in python
-2^63 to 2^63-1 are the range of long in python aka LLong-Min and LLong-Max
We can use Int min/max or Long min/max when we need to find integers or longs in a range, and the problem statement sepcifically asks for integers and longs, and not floats.
Use the sys module when you need integers - otherwise use -math.inf and math.inf or float('-inf') and float('inf')
"""

n = int(input()) ## let's say n = 5 meaning we will get 5 integer values from the user
max_so_far = float("-inf")
for _ in range(n):
    num = int(input()) # Here we get 5 integer values from the user
    if num > max_so_far:
        max_so_far = num   
    #max_so_far = max(max_so_far, num)
print(max_so_far)



"""_Controlling Loops in Python_
    - Break statement: used to prematurely exit a loop
    - Continue statement: used to skip the rest of the current iteration and move to the next iteration
    - Pass statement: used to do nothing in a loop
"""

cnt = 0
while True:
    num = int(input("Enter a number: "))
    if num < 0:
        break
    cnt += 1
print("Total number of numbers entered:", cnt)

# OR
cnt = 0 
while True:
    num = int(input("Enter a number: "))
    if num == 0:
        break
    cnt += 1    
print("Total number of numbers entered:", cnt)

## When you encounter a break statement, the loop is immediately terminated, and the program continues with the next statement after the loop.
# You only break out of the innermost loop you're in.

"""
Check Fibonacci Number
Output should be True or False
Start generating the Fibonacci sequence until the nth Fibonacci number is greater than the number you entered.
As long as the Fibonacci number is less than the number you entered, keep generating the Fibonacci sequence.
And if the Fibonacci number is greater than the number you entered, stop generating the Fibonacci sequence.
"""
n = int(input("Enter a number: "))
if n == 0 or n == 1:
    print(True)
else:
    a = 0 # 0th Fibonacci number
    b = 1 # 1st Fibonacci number
    while True:
        c = a + b
        if c == n:
            print(True)
            break
        elif c > n:
            print(False)
            break
        else:
            a = b
            b = c


"""
Check Prime Number
"""
n = int(input())
i = 2
while i <= (n ** 0.5):
    if n % i == 0:
        print("not prime")
        break
    i += 1
else:
    print("prime")

"""
While can have an else clause which is executed when the loop is finished normally
In case you break, then else clause is not executed
This is helpful from the above example - to avoid printing both "not prime" and "prime" in case of composite numbers,
we can use else clause to only print "not prime" in case of composite numbers and "prime" in case of prime numbers
Eg. if the number is 13 - the while condition is False, so the else clause is executed
if the number is 10 - the while loop break statement is executed, so the else clause is not executed 
and you come out of the loop after printing "not prime" and the else clause is not executed
"""
# OR (instead of else clause)

# we can use boolean variable as flag to keep track of whether the number is prime or not
n = int(input())
i = 2
flag = True # assume the number is prime
while i <= (n ** 0.5):
    if n % i == 0:
        print("not prime")
        flag = False
        break
    i += 1
if flag:
    print("prime")
    
# OR if I don't want to use flag or else clause - another approach is:

n = int(input())
i = 2
while i <= (n ** 0.5):
    if n % i == 0:
        print("not prime")
        break
    i += 1
if i > (n ** 0.5):
    print("prime")
    
"""
In DSA, it's always preferable to avoid using floating point numbers. That is one issue with the above 3 approaches for prime number checking as we are calculating square root of a number.
As the universe of these floating point numbers is infinite, and it's not possible to represent all of them in a finite amount of space.
The memory space of a computer is finite, and it's not possible to represent all of the floating point numbers in a finite amount of space.
So, we can use integers to represent floating point numbers, and we can use the sys module to get the maximum integer and the minimum integer in the range.
What would happen if we try to fit all of the floating point numbers in a finite amount of space?
Maybe the floating point numbers that are close to each other will be stored in the same memory location. They will get the same binary
In discrete mathematics, there is a principle called Pigeonhole Principle, which states that if you have more than n items, then at least one of the items must be in more than one of the n boxes.
This principle is used in computer science to solve the problem of storing all of the floating point numbers in a finite amount of space.
We have this infinite universe of floating point numbers, and we want to map them to a finite set of binary representations.
So when we work with floating point numbers, we encounter "Precision Loss" and "Rounding Error" problems.
Precision loss is when we lose precision when we convert a floating point number to a binary representation.
Rounding error is when we round a floating point number to a binary representation, and the binary representation is not exactly the same as the original floating point number.
Eg. If we try to save 3.0 in memory, it's very likely that the binary representation of 3.0 will be different from the original floating point number.
If we try to save 3.141592653589793 in memory, it's very likely that the binary representation of 3.141592653589793 will be different from the original floating point number.
This is the reason we never compare floating point numbers for equality using == or !=
Eg. if I try to compare 3.0 with 3.0, it's likely one 3.0 is stored in binary form as 3.0000000001 and the other 3.0 is stored as 2.999999999, and they will never be equal.
"""
"""
So in the above prime number example, instead of using i<=(n**0.5), we can do i*i<=n

"""

n = int(input())
i = 2
while i*i <= n:
    if n % i == 0:
        print("not prime")
        break
    i += 1
else:
    print("prime")
    
# we can use boolean variable as flag to keep track of whether the number is prime or not
n = int(input())
i = 2
flag = True # assume the number is prime
while i*i <= n:
    if n % i == 0:
        print("not prime")
        flag = False
        break
    i += 1
if flag:
    print("prime")
    
# OR if I don't want to use flag or else clause - another approach is:

n = int(input())
i = 2
while i*i <= n:
    if n % i == 0:
        print("not prime")
        break
    i += 1
if i*i > n:
    print("prime")

""" Continue statement
Continue statement is used to skip the rest of the current iteration and move to the next iteration
It's similar to break statement, but it's not immediately terminated, and the program continues with the next iteration of the loop.
"""

for i in range(10):
    if i == 5:
        continue ## will print all numbers except for 5
    print(i)
    
"""
    IMPORTANT: If you are using continue in a while loop, make sure the update (i+=1) 
    doesn't get skipped, else you will be stuck in an infinite loop
    This problem doesn't happen in a for loop, because for loop does everything on its own 
    like initializing the loop variable, checking the condition, and updating the loop variable.
    See example below:
    
    i = 0
    while i < 10:
        if i == 5:
            continue
        print(i)
        i += 1 ## Here the i will now stay stuck at 5, because the update (i+=1) is skipped
"""
"""
Find SQUARE ROOT of a number
NOTE: Do this question without using the math module or any builtin functions or operators
eg. N = 64 Output: 8 #perfect square
N = 30 Output: 5.47 

This below strategy would work for perfect squares: 
Square root of any number is always going to be non-negative i.e >= 0
And the square of the square root of a number is always going to be <= the original number
So now, starting from zero, I will search for the largest number where the above condition is satisfied.
i.e keep going until i*i <= n
Once i*i > n, I will stop searching and return i-1

"""

n = int(input("Enter a number: "))
ans = 0

while ans*ans <= n:
    ans += 1
print(ans-1)

## Now for non-perfect squares: instead of adding/subtracting 1, we add/subtract 0.1 or 0.01 or 0.001 etc. depending on how many decimal places we want to round to.

n = int(input("Enter a number: "))
ans = 0

while ans*ans <= n:
    ans += 1

ans = ans - 1

while ans*ans <= n:
    ans += 0.1

ans = ans - 0.1

while ans*ans <= n:
    ans += 0.01
ans = ans-0.01


while ans*ans <= n:
    ans += 0.001
ans = ans-0.001

"""
Now let's generalize this to any number of decimal places.
We can see depending on the number of decimal places, p, we want in the output, we run the same while loop that many times.

"""

n = int(input("Enter a number: "))
p = int(input("Enter the number of decimal places: "))
ans = 0

while ans*ans <= n:
    ans = ans + 1

ans = ans - 1

for i in range(p):
    while ans*ans <= n:
        ans += 0.1 ** i
    ans = ans - 0.1 ** i
    
print(ans)

### More general way of doing it

n = int(input("Enter a number: "))
p = int(input("Enter the number of decimal places: "))
ans = 0

while ans*ans <= n:
    ans = ans + 1

ans = ans - 1
inc_fac = 0.1

for _ in range(p):
    while ans*ans <= n:
        ans = ans + inc_fac
    ans = ans - inc_fac
    inc_fac = inc_fac / 10
    
print(ans)
