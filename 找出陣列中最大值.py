arr = [3,2,7,9,5]  # 建立列表
max_number = arr[0]  # 先將最大設為index0
for i in range(1,len(arr)):  # for迴圈遍歷index1~4
    if arr[i] > max_number:  # 如果遍歷到比max_number大
        max_number = arr[i]  # 更新max_number
print("最大值為:",max_number)  # 輸出


