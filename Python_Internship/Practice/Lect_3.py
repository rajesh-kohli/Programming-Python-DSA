
x = 6

if x&1==0 and x%2!=0:
    print(x>>1)
    
if ((x-1)>>1)<3:
    print(x<<2>>1)
    
if((x-1)>>1) or ((x>>1)<3) and (x!=3):
    print(x>>1<<2)

x = input("enter any value:")
y = input("enter any value:")
print(x+y)
print(type(x+y))

## need to do type casting
x = int(input("enter any value:")) ##type casting
y = int(input("enter any value:"))
print(x+y)
print(type(x+y))

### check a number is even or odd using bitwise operator
number = int(input("enter any number:"))
if (number & 1) ==0:
    print("even")
if (number & 1) !=0:
    print("odd")

### the same problem we can solve using else - it will reduce unnecessary condtions

if (number & 1) ==0:
    print("even")
else:
    print("odd")
    
## point (x,y) and radius "r" is given. 
## write a program to Check whether the point lies inside, on or outside the circle

## compute the distance from the center to the point. If the distance is equal to r, then on the circle

radius = int(input("enter the radius of a circle:"))
x_cor = int(input("enter x_coordinates of a point"))
y_cor = int(input("enter y_coordinates of a point"))
c_x = 0
c_y = 0
distance = (((y_cor-c_y)**2) + ((x_cor-c_x)**2))**0.5
if radius==distance:
    print("point is on the circle")
elif radius > distance:
    print("point is inside the circle")
else:
    print("point is outside the circle")
    
#### TASK 1 #### WAP to check whether the two vectors are collinear

### TASK 2 - perform swapping by bitwise operators. ##
# input: a= 5, b = 6 after swapping a = 6, b = 5 --> perform using bitwise operator (hint XOR)
## hack: if you perform 3 XOR operations of bitwise operators, you get numbers swapped

a= int(input("enter first number:"))
b = int(input("enter second number:"))
a = a^b
b = a^b
a = a^b
print(a,b)

