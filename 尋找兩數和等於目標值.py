nums = [2,7,11,5]  # 原始陣列
target = 9  # 目標總和
seen = {}  # 用來存數字和它的index，例如{2:0,7:1}
for i in range(len(nums)):  # 遍歷nums中的數字
    num = nums[i]  # 將遍歷到的數存入num
    need = target - num  # 用target-num存入need
    if need in seen:  # 如果need數字在seen中
        print(seen[need],i)  # 輸出
        break
    seen[num] = i  # 將i存入seen
# i=0，num = 2，need = 7，seen = {}
# if need in seen:  7不再seen中>>>跳過
# seen[num] = i 將i存入seen中，seen = {2:0}
# i=1，num = 7，need = 2，seen = {2:0}
# if need in seen:  2在seen中
# print(seen[need],i)  輸出(0,1)

