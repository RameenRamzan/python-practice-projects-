import streamlit as st
import plotly.express as px
from data import load_data

st.title("Personal Finance Dashboard")

uploaded_file = st.file_uploader("Upload your transactions CSV", type="csv")

if uploaded_file is not None:
    df = load_data(uploaded_file)

    st.subheader("Filter")
    selected_categories = st.multiselect(
        "Select categories to include",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )
    df = df[df['Category'].isin(selected_categories)]

    st.subheader("Spending by Category")
    category_spending = df[df['Amount'] < 0].groupby('Category')['Amount'].sum().sort_values()
    fig1 = px.pie(category_spending.abs().reset_index(), names='Category', values='Amount')
    st.plotly_chart(fig1)

    st.subheader("Spending Trend Over Time")
    monthly_spending = df.groupby('Month')['Amount'].sum()
    fig2 = px.line(
        monthly_spending.reset_index().astype({'Month': 'str'}),
        x='Month',
        y='Amount'
    )
    st.plotly_chart(fig2)

    st.subheader("Top 10 Biggest Expenses")
    top_expenses = df[df['Debit'] > 0].sort_values('Debit', ascending=False).head(10).copy()
    top_expenses['Label'] = top_expenses['Category'] + " (₨" + top_expenses['Debit'].astype(int).astype(str) + ")"
    fig3 = px.bar(
        top_expenses,
        x='Label',
        y='Debit',
        color='Category'
    )
    st.plotly_chart(fig3)

else:
    st.info("Upload a CSV to get started.")