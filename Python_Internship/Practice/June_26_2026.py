## Exception Handling

try:
    f = open("magic.txt","r") ## this file doesn't exist, so except would run
    print(f.read())
    f.close()
except:
    print("File not present in directory")
    
    
# write an exception handling code which handle list index error

lst = [10,20,30]
try:
    # print(lst[5])
    index = int(input("Enter the index of element"))
    print(lst[index])
except:
    print("The list index is not present, out of range")
    
## dictionary:
employee_info = {
    "mayur":10000,
    "abc":20000,
    "pqr":3000
}

try:
    name = input("Enter the name of the employee".lower)
    print(employee_info[name])
except:
    print("The employee is not present")
finally:
    print("Execution done")