s = "AABABBA"  # 字串
k = 1  # 可修改次數
count = {}  # 每個字元出現幾次
left = 0  # 視窗左邊界
max_count = 0  # 目前最多字元出現次數
max_len = 0  # 記錄答案(最長長度)
for right in range(len(s)):  # for迴圈遍歷右指標擴張
    c = s[right]  # 取遍歷到的右邊字元存入c
    count[c] = count.get(c,0)+1  # 加入視窗，沒有就從0開始+1
    max_count = max(max_count,count[c])  # 將最大頻率更新到max_count
    while (right-left+1) - max_count > k:  
        # 當視窗長度-最多字元數>k，需修改>k不合法需縮小
        left_char = s[left]  # 找到最左邊字元
        count[left_char] -= 1  # 把它從視窗中移除
        left += 1  # 左邊索引+1
    max_len = max(max_len,right-left+1)  # 更新最大長度
print(max_len)  # 輸出

