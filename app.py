import sqlite3
import os
import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px


def get_connection():
    conn = sqlite3.connect("expenses.db")
    return conn

st.write("Current folder:", os.getcwd())

st.title("Expense Tracker")

menu = st.selectbox("Menu", ["Add Expense", "View Expense", "Category Summary", "Expense Chart", "Delete Expense", "Total Spendings"])

if menu == "Add Expense":
    category = st.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
)
    
    name = st.text_input("Expense Name")
    amount = st.number_input("Amount", min_value=0.0, step=1.0)

    if st.button("Add"):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (date, category, description, amount)
            VALUES (?, ?, ?, ?)
            """,
            (current_time, category, name, amount)
            )

        conn.commit()
        conn.close()

        st.success("Expense Added Successfully!")

 
elif menu == "View Expense":
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT date, category, description, amount FROM expenses")
    
    rows = cursor.fetchall()
    
    conn.close()
    
    if len(rows) == 0:
        st.warning("No expenses found")
    else:
        for row in rows:
            date_time, category, name, amount = row
            st.write(f"{date_time} | {category} | {name} | ₹{amount}")


elif menu == "Category Summary":
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY Category
    """)

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:
        st.warning("No expenses found")
    else:
        st.subheader("Category Wise Spending")

        for row in rows:
            category = row[0]
            total = row[1]

            st.metric(category, f"₹{total}")


elif menu == "Expense Chart":
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:
        st.warning("No expenses found")

    else:
        df = pd.DataFrame(
            rows,
            columns=["Category", "Amount"]
        )

        fig = px.pie(
            df,
            names="Category",
            values="Amount",
            title="Category Wise Expense Distribution"
        )

        st.plotly_chart(fig)

               

elif menu == "Delete Expense":
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("SELECT id, date, category, description, amount FROM expenses")

    rows = cursor.fetchall()

    expense_list = []
    
    for row in rows:
        expense_list.append(
            f"{row[0]} | {row[1]} | {row[2]} | {row[3]} - ₹{row[4]}"
            )

    if len(rows) == 0:
        st.warning("No expenses found")
    else:
        selected = st.selectbox("Select Expense", expense_list)

    if len(rows) > 0 and st.button("Delete"):
        expense_id = int(selected.split(" | ")[0])

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
            )
            
        conn.commit()
        conn.close()   
        st.success("Expense Deleted Successfully!")
    

elif menu == "Total Spendings":
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT date, category, description, amount FROM expenses")
    rows = cursor.fetchall()

    if len(rows) == 0:
        st.warning("No expenses found")
    else:
        for row in rows:
            date_time, category, name, amount = row
            st.write(f"{date_time} | {category} | {name} - ₹{amount}")

        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0]

        st.subheader(f"Total Spending: ₹{total}")

    conn.close()
