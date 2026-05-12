arr = [1,2,3,2,3,1,3]
count = {}

for num in arr:
    if num in count:
        count[num] += 1
    else:
        count[num] = 1
for num in count:
    if count[num] % 2 == 1:
        print("出現次數為奇數:",count[num])



