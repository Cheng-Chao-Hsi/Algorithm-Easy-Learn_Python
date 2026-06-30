import sqlite3
conn = sqlite3.connect("expense.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    type TEXE,
    category TEXT,
    item TEXT,
    money INTEGER,
    note TEXT
    )

""")
conn.commit()
conn.close()
print("資料庫建立成功!")