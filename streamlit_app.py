import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache
def load_data():
    df = pd.read_csv('Global Superstore.csv')
    return df

df = load_data()

# Sidebar widgets
st.sidebar.title('Filters')
product_category = st.sidebar.selectbox('Select Product Category', df['Category'].unique())
profit_threshold = st.sidebar.slider('Select Profit Threshold', min_value=0, max_value=df['Profit'].max())

# KPIs
total_sales = df['Sales'].sum()
average_profit = df['Profit'].mean()
total_orders = df['Order ID'].nunique()

st.write(f'Total Sales: ${total_sales:.2f}')
st.write(f'Average Profit: ${average_profit:.2f}')
st.write(f'Total Orders: {total_orders}')

# Filter data based on sidebar selections
filtered_data = df[(df['Category'] == product_category) & (df['Profit'] >= profit_threshold)]

# Plot
st.header('Sales vs. Profit')
fig = px.scatter(filtered_data, x='Sales', y='Profit', color='Sub-Category', title='Sales vs. Profit')
st.plotly_chart(fig)
