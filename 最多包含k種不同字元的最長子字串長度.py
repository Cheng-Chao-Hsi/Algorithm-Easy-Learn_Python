s = "eceba"  # 建立字串
k = 2  # 最多允許k個不同字元
count = {}  # 建立視窗
left = 0  # 初始化視窗左邊界left=0
max_len = 0  # 記錄最長合法長度，初始化將最大設為0
for right in range(len(s)):  # for迴圈遍歷字串
    c = s[right]  # 將遍歷到的right存入c
    count[c] = count.get(c,0)+1  # 將c存入count視窗中，如果沒有就0+1，有就+1
    while len(count) > k:  # 當count字元種類數>k時，len(count)為字元種類數
        left_char = s[left]  # 找到字串最左存入left_char中
        count[left_char] -= 1  # 縮小視窗去掉left_char，次數-1

        if count[left_char] == 0:  # 當left_char == 0沒有這字元
            del count[left_char]  # 直接從count中刪除
        left += 1  # left字元索引+1
    max_len = max(max_len,right - left +1)  # 更新max_len
    # max_len為目前遇過最大合法長度，right-left+1為目前視窗長度
print(max_len)  # 輸出

