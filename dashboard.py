"""
Global Superstore Dashboard

This Streamlit app visualizes sales and profit data
from the Global Superstore dataset.

 Problem Statement:
Managers and analysts need a dynamic tool to understand
sales and profitability across different regions, categories,
and product segments.

 Goal:
To develop an interactive dashboard that enables filtering
by Region, Category, and Sub-Category, while visualizing
key metrics like Total Sales, Profit, and Customer Insights.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(layout="wide")

# Title
st.title("Global Superstore Dashboard")

# Load dataset
df = pd.read_csv('superstore.csv', encoding='ISO-8859-1')
df.dropna(inplace=True)
df['Order.Date'] = pd.to_datetime(df['Order.Date'])

# Sidebar filters
region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())
sub_category = st.sidebar.multiselect("Select Sub-Category", options=df['Sub.Category'].unique(), default=df['Sub.Category'].unique())

# Filter data
filtered_df = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category)) &
    (df['Sub.Category'].isin(sub_category))
]

# KPIs
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
top_customers = filtered_df.groupby('Customer.Name')['Sales'].sum().nlargest(5).reset_index()

col1, col2 = st.columns(2)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")

# Sales by Category
st.subheader(" Sales by Category")
fig1 = px.bar(filtered_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', color='Category')
st.plotly_chart(fig1, use_container_width=True)

# Top 5 Customers
st.subheader("Top 5 Customers by Sales")
fig2 = px.bar(top_customers, x='Customer.Name', y='Sales', color='Customer.Name')
st.plotly_chart(fig2, use_container_width=True)

"""
✅ Conclusion:
You now have a clean, filtered dataset ready for visual analysis.
Next steps include adding KPIs, customer charts, and trend plots.
"""