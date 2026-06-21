# # Another example
# def fun1(a,b):
#     fun2(5,6)
#     x = fun3()
#     return a+b*b

# def fun2(p,q):
#     return p+q-2
        
# def fun3():
#     return 5

# print(fun1(6,7))

# x = 5
# def g():
#     global x
#     x = 7

# g()
# print(x)

# x = 2**3
# print(x)

# a = [1,2,3,4]
# print("Original ID:", id(a))
# a += [3,4,5]
# print("Result list:", a)
# print("After += ID:", id(a))

# a = 10//3
# print(a)

# a = 2**3**2
# b = 2*2*2*2*2*2
# c = 8*8*8
# print(a)
# print(b)
# print(c)

# n = 27
# is_prime = True
# if n < 2:
#     print("Number is not Prime")

# for i in range(2,n):
#     if n%i == 0:
#         is_prime = False
#         print (f"Number {n} is not Prime")
#         break
# else:
#     print(f"{n} is Prime")
    
#### Prime with While loop

# import math
# n = int(input("Enter a number: "))
# i = 2  
# if n < 2:
#     print (f"Number {n} is not Prime")
# else:
#     while i <= math.sqrt(n):
#         if n%i == 0:
#             print(f"{n} is not Prime")
#             break
#         i = i +1
#     else:
#         print(f"{n} is Prime")


number = int(input("Enter a number: "))

def check_prime(number):
    for i in range(2,number):
        if number % i == 0:
            return "Not Prime"
    else:
        return "Prime"

### Print all the prime numbers within a given range

lower_limit = int(input("Enter a number: "))
upper_limit = int(input("Enter a number: ")) 

for i in range (lower_limit,upper_limit,upper_limit+1):
    if   


### Loop variable scope

# i = 5
# for i in range(3):
#     print(i)
# print(i)

###
i = 1
while i < 5:
    print(i)
    i +=1
    if i == 3:
        pass 
else:
    print("While loop else block")