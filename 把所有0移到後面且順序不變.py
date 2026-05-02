arr = [0,1,0,3,12]
new_arr = []
for num in arr:
    if num != 0:
        new_arr.append(num)
for num in arr:
    if num == 0:
        new_arr.append(0)
print(new_arr)


