s = "xinxinpythonc"  # 要被搜尋的字串
t = "ipt"  # 要包含的字元
need = {}  # 建立need
for c in t:  # 將遍歷的t的字串加入need
    need[c] = need.get(c,0)+1
    # need = {'i':1,'p':1,'t':1}
window = {}  # 建立window目前視窗
left = 0  # 初始化設left=0，視窗一開始[left......right]
for right in range(len(s)):  # 用for迴圈遍歷字串
    c = s[right]  # 取得右邊字元right，right=0時c='x'
    window[c] = window.get(c,0,)+1  
    # 把這個字存入視窗，找c如果沒有就給0，次數+1
    # 加入x>>>{'x':1}，加入i>>>{'x':1,'i':1}
    ok = True  # 先假設視窗符合目前條件
    for key in need:  # 檢查每個need
        if window.get(key,0) < need[key]:  # 目前視窗數量<需要的數量
            ok = False  # 判定為不符合
            break
    if ok:  # 如果所有需要字元已經夠了
        print("找到一段:",s[left:right+1])  # 輸出字串left到right
        break

    



    

