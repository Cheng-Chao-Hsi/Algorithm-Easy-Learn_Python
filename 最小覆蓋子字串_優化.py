s = "xinxinpythonc"  # 建立字串s
t = "ipt"  # 建立字串t
need = {}  # 建立need
for c in t:  # 遍歷t後存入need中
    need[c] = need.get(c,0)+1  # 將字串存入need
window = {}  # 建立window
left = 0  # 初始化left=0
min_len = float('inf')
start = 0  # 初始化start=0
for right in range(len(s)):  # for迴圈遍歷s
    c = s[right]  # 將遍歷到的right存入c
    window[c] = window.get(c,0)+1  # 加入window中
    ok = True
    for key in need:  # for迴圈遍歷need
        if window.get(key,0) < need[key]:  # 如果視窗中的字<need
            ok = False  # 條件未達成
            break
    while ok:  # 當條件達成時
        if right - left + 1 < min_len:  # 更新最短
            min_len = right - left +1
            start = left  # 更新start
        left_char = s[left]  # 將視窗中的left存入left_char
        window[left_char] -= 1  # 更新視窗中的left(-1)
        if left_char in need and window[left_char] < need[left_char]:  # 檢查是否縮到<need
            ok = False
        left += 1  # left往右移動
if min_len == float('inf'):
    print("沒有符合")
else:
    print("最短子字串:",s[start:start+min_len])

