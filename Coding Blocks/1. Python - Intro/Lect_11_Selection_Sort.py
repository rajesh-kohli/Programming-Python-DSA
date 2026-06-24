"""
The selection sort algorithm works in passes such that in its each pass, 
we place the smallest element in the unsorted part of the array to its correct position
"""

n = int(input())
arr = [int(input()) for _ in range(n)]

def selection_sort(arr: list[int], n: int)->None:
    for i in range(1, n): #[1,n)
        # in the ith pass, put the smallest value in the 
        # unsorted part of the array to its correct position
        min_idx = i-1
        for j in range(i, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i-1], arr[min_idx] = arr[min_idx], arr[i-1]
    return arr


print(arr) # [50, 20, 30, 10, 40]
selection_sort(arr, n)
print(arr) # [10, 20, 30, 40, 50]

