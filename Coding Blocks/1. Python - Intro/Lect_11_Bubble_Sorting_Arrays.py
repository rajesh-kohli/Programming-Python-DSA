"""
## Sorting Algorithms:
- Bubble Sort
- Selection Sort
- Insertion Sort
The sorted function - offered by Python
The Lambda keyword - to create annonymous functions
"""
"""
Given an array of N integers, sort the array using the `bubble sort` algorithm
Bubble sort as an algorithm works in passes, so we will have to do multiple passes
We start by assuming the entire array is unsorted
In the first pass, our goal is to bring the largest number to it's correct position
We start by swapping the first two numbers at index 0 and 1, if the value at index 1 is smaller tham index 0
And then we keep repeating the swap operation untile we reach the last two elements
eg. arr = [50, 20, 30, 10, 40]
so we only swap when the value at index i+1 is smaller than index i, but the number of comparisons is still n
Now for the second pass, we do the same things for the unsorted part of the array
And so on, untill we reach the last pass, where we swap/compare the last two elements at index 0 and 1

Keep in mind, you only do n-1 passes for the array of size n
Because the smallest would automatically be in the correct position in the end

Bubble Sort would have n-1 passes for an array of size n

"""
n = int(input("Enter the size of the array: "))
arr = list(map(int, input("Enter the elements of the array: ").split()))
# arr = [50, 20, 30, 10, 40]

def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-1-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

bubble_sort(arr)
print(arr)

n = int(input())
arr = [int(input()) for _ in range(n)]
def bubble_sort2(arr: list[int])->None:
    for i in range(1,n):
        # in the ith pass, put the largest value in the 
        # unsorted part of the array to its correct position
        for j in range(n-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
                
                


print(arr) # [50, 40, 30, 20, 10]
bubble_sort2(arr,n)
print(arr) # [10, 20, 30, 40, 50]

"""
How much time will bubble sort take if the array is already sorted?
 - It will do all comparisons in all the passes, although there won't be any swaps
 - Number of comparisons in the current implementation is still O(n^2)
 
if the array is already sorted or partially sorted, can we do better than O(n^2) what is happening in the above implementation?
"""

"""
We can do something like - if there is no swap in a given pass, we can stop doing the next set of passes
We can apply this minor optimization to the above implementation
We can maintain a flag and set it to False, where we assume no swaps will be done in the ith pass
"""

def bubble_sort3(arr: list[int], n: int)->None:
    cnt = 0
    for i in range(1, n): #[1,n)
        # in the ith pass, put the largest value in the 
        # unsorted part of the array to its correct position
        flag = False # assume no swaps will be done in the ith pass
        for j in range(n-i): # [0, n-i)
            cnt += 1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                flag = True
        if flag == False:   ### can also write if not flag:
            break
    print(cnt)
    return arr



