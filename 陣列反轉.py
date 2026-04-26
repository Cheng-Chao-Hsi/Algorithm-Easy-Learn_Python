arr = [3,2,7,9,5,8,10]

def rever_number(arr):
    left = 0
    right = len(arr)-1

    while left < right:
        arr[left],arr[right] = arr[right],arr[left]
        left += 1
        right -= 1
    
(rever_number(arr))
print(arr)



