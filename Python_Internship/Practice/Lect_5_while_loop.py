# # WAP to find the sum of all even numbers from given n numbers

# n = int(input("Enter the number: "))
# i = 1
# sum = 0
# while i <=n:
#     if i%2 == 0:
#         sum = sum + i
#     i += 1
# print(sum)


# ## WAP to print a sum of difference of even and odd numbers from 1 to n
# n = int(input("Enter the number: "))
# i = 1
# sum = 0
# while i <= n:
#     if i%2 == 0:
#         sum = sum + i
#     else:
#         sum = sum - i
#     i += 1
# print(abs(sum))

# ##WAP to find the sum of digits of a given number. eg. 123 = 1+2+3 = 6
# n = int(input("Enter the number: "))
# sum = 0
# while n > 0:
#     rem = n%10
#     sum = sum + rem
#     n = n//10
# print(sum)

# # Approach 2
# n = int(input("Enter the number: "))
# n_str = str(n)
# sum = 0
# i = 0
# while i < len(n_str):
#     sum = sum + int(n_str[i])
#     i += 1
# print(sum)

# ## WAP to find the sum of even digits of a given number. eg. 123 = 2
# n = int(input("Enter the number: "))
# sum_even = 0
# while n > 0:
#     rem = n % 10
#     if rem % 2 == 0:
#         sum_even += rem
#     n = n // 10
# print(sum_even) 

# ## WAP to find the factorial of a number
# n = int(input("Enter the number: "))
# factorial = 1
# i = 1
# while i <= n:
#     factorial = factorial * i
#     i += 1
# print(factorial)  


print("Pyramid of Stars")
n = int(input("Enter the value of n:"))
i = 1
while i<=n:
    j = 1
    while j <= n-i:
        print(" ",end=" ")
        j = j + 1
    k = 1
    while k <= 2*i -1:
        print("*",end=" ")
        k = k+1
    l = 1
    while l <= n-i:
        
        print (" ",end=" ")
        l = l+1
    i = i + 1
    print()