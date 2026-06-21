a = 4
print(a)
a += 5
print(a)
a &= 4
print(a)

container = [3,4,5,6,7,8,10]

print(container)
10 in container

9 in container
15 not in  container

a = b = 5

print(id(b))
print(id (a))

print(a is b)

a = b = 256

print(a is b)

a = b = 257
print(a is b)
print(id(a))
print(id(b))

a = 256
b = 257

print(a is b)
print(id(a))
print(id(b))

a = 260
b = 260

print(a is b)
print(id(a))
print(id(b))

a = 123
print(type(a))

a = 123.456
print(type(a))

a = "Hello"
print(type(a))

a = 3 + 4j
print(type(a))

a = True
print(a)
print(type(a))

lst1 = []
print(lst1)

lst2 = [3,4,5,6]
print(lst2)
print(type(lst2))

#lst4 = [3+5j, 6+9i]
#print(lst4)
#print(type(lst4))

print(lst2[3])
print(lst2[-3])

lst1 = [1,2,3]
lst2 = [5,6,7]

print(lst1 + lst2) ##concatenate

# However these below operatins are not possible
# lst1 - lst2
# lst1 * lst2
# lst1 / lst2

print(lst2)

lst2[1] = 1000
print(lst2) #list is mutable - you can change the elements of a list but can't do with Tuple

t1 = ()
print(t1)
print(type(t1))

t2 = (2,3,4,5)
print(t2)
print(type(t2))

t3 = (2.5,3.7,4.8,5.9)
print(t3)
print(type(t3))

# t4 = (3+4j,4+2i)
# t2 = (2,3,4,5)
# print(t4)
# print(type(t4))

t5 = (1,2,4.5,"Hello",6)
print(t5)
print(type(t5))

s1 = {}
print(s1)
print(type(s1))

print(dict_1 = {1:"Add", 2:"subtract"})



