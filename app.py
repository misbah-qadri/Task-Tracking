# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Load or create the CSV file
CSV_FILE = 'expenses.csv'
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['Date','Category','Amount', 'Type', 'Description'])
    df.to_csv(CSV_FILE, index=False)

st.set_page_config(page_title="💸 Personal Expense Tracker", layout="wide")
# Load data
df = pd.read_csv(CSV_FILE)

st.title("💸 Personal Expense Tracker - By Misbah")

# --- Input Form ---
st.header("➕ Add New Transaction")
with st.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ['Food', 'Transport', 'Utilities', 'Shopping', 'Salary', 'Other', 'Entertainment', 'Health', 'Education', 'Travel', 'Investment', 'Gifts', 'Savings', 'Loan', 'Rent',])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    trans_type = st.radio("Type", ["Expense", "Income"])
    desc = st.text_input("Description (optional)")
    submitted = st.form_submit_button("Add Transaction")

if submitted and amount > 0:
    new_data = pd.DataFrame([[date, category, amount, trans_type, desc]], 
                            columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.success("Transaction added successfully!....")

# --- View & Summary ---
st.header("📊 Expense Summary")

if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])

    # Filters
    with st.expander("🔍 Filter"):
        month = st.selectbox("Select Month", ['All'] + sorted(df['Date'].dt.strftime('%B').unique().tolist()))
        if month != 'All':
            df = df[df['Date'].dt.strftime('%B') == month]

    # Total Summary
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expense", f"₹{total_expense:,.2f}")
    col3.metric("Balance", f"₹{balance:,.2f}")

    # Category-wise Pie Chart
    expense_by_cat = df[df['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
    fig, ax = plt.subplots()
    expense_by_cat.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

    # Show data
    with st.expander("📄 View All Transactions"):
        st.dataframe(df.sort_values(by="Date", ascending=False))
else:
    st.info("No transactions added yet.")


