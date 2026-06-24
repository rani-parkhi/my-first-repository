import os
import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import csv

if not os.path.exists("expenses.csv"):
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            ["DateTime", "Category", "Expense Name", "Amount"]
        )

st.write("Current folder:", os.getcwd())

st.title("Expense Tracker")

menu = st.selectbox("Menu", ["Add Expense", "View Expense", "Category Summary", "Expense Chart", "Delete Expense", "Total Spendings"])

file_name = "expenses.txt"

if menu == "Add Expense":
    category = st.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
)
    
    name = st.text_input("Expense Name")
    amount = st.number_input("Amount", min_value=0)

    if st.button("Add"):
        with open("expenses.csv", "a", newline="") as file:

            writer = csv.writer(file)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([current_time, category, name, amount])
            

        st.success("Expense Added!")

 
elif menu == "View Expense":
    
    try:
        with open("expenses.csv", "r") as file:

            reader = csv.reader(file)

            next(reader)

            found = False

            for row in reader:

                found = True

                date_time = row[0]
                category = row[1]
                name = row[2]
                amount = row[3]

                st.write(
                    f"{date_time} | {category} | {name} | ₹{amount}"
                )

            if not found:
                st.warning("No expenses found")

    except FileNotFoundError:
        st.warning("No expenses found")


elif menu == "Category Summary":
    
    try:
        summary = {}

        with open("expenses.csv", "r") as file:

            reader = csv.reader(file)

            next(reader)  # Skip header

            for row in reader:

                category = row[1]
                amount = int(float(row[3]))

                if category in summary:
                    summary[category] += amount
                else:
                    summary[category] = amount

        st.subheader("Category Wise Spending")

        for category, total in summary.items():
            st.metric(category, f"₹{total}")

    except FileNotFoundError:
        st.warning("No expenses found")


elif menu == "Expense Chart":
    
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            
            summary = {}
            
            for row in reader:
                
                category = row[1]
                amount = int(float(row[3]))

                if category in summary:
                    summary[category] += (amount)
                else:
                    summary[category] = (amount)
                    
                df = pd.DataFrame({ 
                "Category": summary.keys(),
                "Amount": summary.values()}
                )

        fig = px.pie(
            df,
            names="Category",
            values="Amount",
            title="Category Wise Expense Distribution"
        )

        st.plotly_chart(fig)

    except FileNotFoundError:
        st.warning("No expenses found")

elif menu == "Delete Expense":
    
    try:
        with open("expenses.csv", "r") as file:
            lines = file.readlines()

        if len(lines) == 0:
            st.warning("No expenses to delete")

        else:
            expense_list = []

            for i, line in enumerate(lines):
                date_time, category, name, amount = line.strip().split(",")
                expense_list.append(f"{i+1}. {date_time} | {category} | {name} - ₹{amount}")

            selected = st.selectbox("Select expense to delete", expense_list)

            if st.button("Delete"):

                index = expense_list.index(selected)

                lines.pop(index)

                with open("expenses.csv", "w") as file:
                    file.writelines(lines)

                st.success("Expense deleted successfully!")
    except FileNotFoundError:
        st.warning("No expenses found")



elif menu == "Total Spendings":
    
    try:

        total = 0

        with open("expenses.csv", "r") as file:

            reader = csv.reader(file)

            next(reader)

            found = False

            for row in reader:

                found = True

                date_time, category, name, amount = row

                st.write(
                    f"{date_time} | {category} | {name} - ₹{amount}"
                )

                total += int(float(amount))

        if not found:
            st.warning("No expenses found")
        else:
            st.subheader(f"Total Spending: ₹{total}")

    except FileNotFoundError:
        st.warning("No expenses found")