nums = [1,2,3,1]  # 原始陣列
seen = set()  # 建立set()不重複且查詢快(O(1))
for num in nums:  # 遍歷陣列，會依序拿到1,2,3,1
    if num in seen:  # 如果這個數有在seen中
        print(True)  # 回傳True
        break  # 結束程式
    seen.add(num)  # 如果沒看過會把這個數存入seen中
else:  # 這個else要for迴圈結束後沒有遇到break執行，不是if的else
    print(False)  # 輸出False

