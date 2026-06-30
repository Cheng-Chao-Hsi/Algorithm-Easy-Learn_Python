from flask import Flask, render_template, request, redirect, session,Response
from datetime import date
import sqlite3
today = date.today()

app = Flask(__name__)
app.secret_key = "123456"

edit_id = None

@app.route("/", methods=["GET", "POST"])
def home():

    if "user" not in session:
        return redirect("/login")

    keyword = request.args.get("keyword","")

    keyword = request.args.get("keyword","")
    sort = request.args.get("sort","")
    start_date = request.args.get("start_date","")
    end_date = request.args.get("end_date","")

    budget_status = []

    category_budget = {
        "飲食":7000,
        "交通":3000,
        "娛樂":3000,
        "購物":5000
    }

    

    conn = sqlite3.connect("expense.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
    id,
    date,
    type,
    category,
    item,
    money,
    note
    FROM records
    """)
    filtered_records = cursor.fetchall()
    conn.close()

    if start_date or end_date:
        temp = []

        for record in filtered_records:
            id,date,type,category,item,money,note = record
            if start_date and date < start_date:
                continue
            if end_date and date > end_date:
                continue
            temp.append(record)
        filtered_records = temp
    if keyword:
        temp = []
        for record in filtered_records:
            id,date,type,category,item,money,note = record
            if (
                keyword in item or
                keyword in category or
                keyword in note
            ):
                temp.append(record)
        filtered_records = temp
    if sort == "date":
        filtered_records.sort(
            key=lambda x:x[0]
        )
    elif sort == "money_asc":
        filtered_records.sort(
            key=lambda x:x[4]
        )
    elif sort == "money_desc":
        filtered_records.sort(
            key=lambda x:x[4],
            reverse=True
        )

    global edit_id
    
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        item = request.form["item"]
        money = int(request.form["money"])
        type = request.form["type"]
        note = request.form["note"]

        if edit_id is None:
            conn = sqlite3.connect("expense.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO records
            (date,type,category,item,money,note)
            VALUES(?,?,?,?,?,?)
            """,
            (date,type,category,item,money,note)
            )

            conn.commit()
            conn.close()

        else:
            conn = sqlite3.connect("expense.db")
            cursor = conn.cursor()

            cursor.execute("""
            UPDATE records
            SET date=?,
                type=?,
                category=?,
                item=?,
                money=?,
                note=?
            WHERE id=?
            """,
            (
                date,
                type,
                category,
                item,
                money,
                note,
                edit_id
            ))
            conn.commit()
            conn.close()

            edit_id = None

        return redirect("/")

    category_data = {}
    for id,date,type,category,item,money,note in filtered_records:
        if type == "支出":
            if category not in category_data :
                category_data[category] = 0
            category_data[category] += money

    daily_expense = {}
    for id,date,type,category,item,money,note in filtered_records:
        if type == "支出":
            if date not in daily_expense:
                daily_expense[date] = 0
            daily_expense[date] += money

    total = sum(
        money for id,date,type,category,item,money,note in filtered_records
        if type == "支出"
        )

    total_balance = 0
    for id,date,type,category,item,money,note in filtered_records:
        if type == "收入":
            total_balance += money
        else:
            total_balance -= money

    edit_record = None

    budget = 10000
    remaining = budget - total
    percent = (total/budget) * 100
    if percent > 100:
        percent = 100
    warning = None
    if total > budget:
        warning = "本月預算以超支!"
    elif total > budget * 0.8:
        warning = "已使用超過80%預算"

    
    print("keyword =", keyword)

    print("filtered_records =", len(filtered_records))

    category_expense = {}

    for id,date,type,category,item,money,note in filtered_records:
        if type == "支出":
            if category not in category_expense:
                category_expense[category] = 0
            category_expense[category] += money

    ranking = sorted(
        category_expense.items(),
        key = lambda x:x[1],
        reverse = True
    )

    for category,budget in category_budget.items():
        used = category_expense.get(category,0)
        remain = budget - used

        if budget > 0:
            category_percent = (used / budget) * 100
        else:
            category_percent = 0

        if category_percent > 100:
            category_percent = 100
        budget_status.append({
            "category":category,
            "budget":budget,
            "used":used,
            "remain":remain,
            "percent":category_percent
        })
    income_total = sum(
        money
        for id,date,type,category,item,money,note in filtered_records
        if type == "收入"
    )
    expense_total = sum(
        money
        for id,date,type,category,item,money,note in filtered_records
        if type == "支出"
    )

    monthly_data = {}
    for id,date,type,category,item,money,note in filtered_records:
        month = date[:7]
        if month not in monthly_data:
            monthly_data[month] = {
                "income":0,
                "expense":0
            }
        if type == "收入":
            monthly_data[month]["income"] += money
        else:
            monthly_data[month]["expense"] += money

    recent_records = filtered_records[-5:]
    recent_records.reverse()

    return render_template(
        "index.html",
        records=filtered_records,
        total=total,
        edit_record=edit_record,
        edit_id=edit_id,
        total_balance=total_balance,
        category_data=category_data,
        daily_expense=daily_expense,
        remaining=remaining,
        budget=budget,
        percent=percent,
        keyword=keyword,
        budget_status=budget_status,
        today=today,
        warning=warning,
        ranking=ranking,
        income_total=income_total,
        expense_total=expense_total,
        monthly_data=monthly_data,
        recent_records=recent_records
        
    )
@app.route("/export")
def export_csv():
    print("CSV export!")
    conn = sqlite3.connect("expense.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
    date,
    type,
    category,
    item,
    money,
    note
    FROM records

    """)
    records = cursor.fetchall()
    conn.close()
    csv_data = "日期,類型,分類,項目,金額,備註\n"
    
    for row in records:
        csv_data += ",".join(map(str,row))
        csv_data += "\n"
    return Response(
        csv_data.encode("utf-8-sig"),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment;filename=expense.csv"
        }
    )


@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("expense.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM records WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    global edit_id
    edit_record = None

    if edit_id is not None:
        conn = sqlite3.connect("expense.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
        id,date,type,category,item,money,note
        FROM records
        WHERE id=?
        """,(edit_id,))

        edit_record = cursor.fetchone()
        conn.commit()
        conn.close()

        return redirect("/")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)