s = "XINXINPYTHONC"  # 建立字串
t = "IPT"  # 建立字串:包含字元
need = {}  # 建立need字典儲存包含字元
for c in t :  # for迴圈遍歷t字串
    need[c] = need.get(c,0)+1  # 將遍歷到的字存入need字典並記錄出現次數
window = {}  # 建立window字典
left = 0  # 初始化設left(最左索引)為0
valid = 0  # 初始化符合need條件的字元種類
min_len = float('inf')  # 初始化設最大長度為0
start = 0  # 初始化設start為0
for right in range(len(s)):  # for迴圈遍歷s字串
    c = s[right]  # 將遍歷到的字串存入c中
    window[c] = window.get(c,0)+1  # 將遍歷到的字存入window字典
    if c in need and window[c] == need[c]:  # 如果遍歷到的c在need字典中==window字典的字
        valid += 1  # 有效字+1
    while valid == len(need):  # 當有效字長度==need長度時
        if right - left +1 < min_len:  # 字串長度<min_len
            min_len = right - left + 1  # 更新最小長度
            start = left  # left放入start中
        left_char = s[left]  # s[left]存入left_char
        window[left_char] -= 1  # window中出現次數-1
        if left_char in need and window[left_char] < need[left_char]:
            # 當window中的left_char出現次數<need
            valid -= 1  # 有效字元-1
        left += 1  # left索引往右+1
if min_len == float('inf'):
    print("no")
else:
    print(s[start:start+min_len])

