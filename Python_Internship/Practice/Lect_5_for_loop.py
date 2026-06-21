# for loop
# 1. Initialization
# 2. condition
# 3. Updation

# range function: range(start, end, step_size)
# start--> initialization
# end --> where we want to stop --> condition
# stepsize

print("Example 1")
for i in range (0,10,2):
    print(i)

print("Example 2")
for i in range (10):  #in this case we didn't specify start and step_size. Default is 0 and 1 respectively
    print(i)
    
print("Example 3")

for i in range(10):
    if i%2==0:
        print(i>>2+1)

print("Example 4")

for i in range(5):
    for j in range(1,5,1):
        print(i%j)
    

print("Example 5")

for i in range(10):
    for j in range(1,5,1):
        if i%j == 0:
            print(i>>2)
        else:
            print(i<<1)

print("Example 6")

for i in range(10):
    for j in range(5):
        for k in range (3):
            print(i+j-k)