import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the dataset
df = pd.read_excel("Superstore.xlsx")

# Convert "Order Date" column to datetime64[ns]
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Calculate KPIs
total_sales = df["Sales"].sum()
total_quantity = df["Quantity"].sum()
total_profit = df["Profit"].sum()

# Set Streamlit app title
st.title("Sales and Profit Dashboard")

# Custom KPI styling
st.markdown(
    """
    <style>
        .kpi-container {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
        }
        .kpi-value {
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """
)

# Create custom KPI layout
st.markdown("## Key Performance Indicators")
st.markdown(
    """
    <div class="kpi-container">
        <div class="kpi-value">{:.0f}</div>
        <div>Total Sales</div>
    </div>
    """.format(total_sales)
)
st.markdown(
    """
    <div class="kpi-container">
        <div class="kpi-value">{:.0f}</div>
        <div>Total Quantity</div>
    </div>
    """.format(total_quantity)
)
st.markdown(
    """
    <div class="kpi-container">
        <div class="kpi-value">{:.0f}</div>
        <div>Total Profit</div>
    </div>
    """.format(total_profit)
)

# Create a sidebar with tiles
with st.sidebar:
    selected_option = st.radio("Select an option:", ["Sales Overview", "Profit Analysis", "Product Insights"])

# Filter by Date section
st.sidebar.subheader("Filter by Date")
start_date = st.sidebar.date_input("Start Date", min(df["Order Date"]))
end_date = st.sidebar.date_input("End Date", max(df["Order Date"]))

# Convert start_date and end_date to datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter by Region
regions = df["Region"].unique()
selected_region = st.sidebar.selectbox("Select Region", regions)

# Filter by Country
countries = df[df["Region"] == selected_region]["Country"].unique()
selected_country = st.sidebar.selectbox("Select Country", countries)

# Filter by State
states = df[df["Country"] == selected_country]["State"].unique()
selected_state = st.sidebar.selectbox("Select State", states)

# Filter by Sub-Category
sub_categories = df["Sub-Category"].unique()
selected_sub_category = st.sidebar.selectbox("Select Sub-Category", sub_categories)


# Filter options
if selected_option == "Sales Overview":
    st.subheader("Monthly Sales Trend")
    filtered_sales = df[(df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)]
    st.line_chart(filtered_sales.set_index("Order Date")["Sales"], color='#357b72')

    st.subheader("Sales by Product Category")
    category_sales = filtered_sales.groupby("Category")["Sales"].sum()
    st.bar_chart(category_sales, color='#357b72')

elif selected_option == "Profit Analysis":
    st.subheader("Profit Trend over Time")
    filtered_profit = df[(df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)]
    st.line_chart(filtered_profit.set_index("Order Date")["Profit"], color='#357b72')

    st.subheader("Profit vs. Discount")
    sns.scatterplot(data=filtered_profit, x="Discount", y="Profit", color='#357b72')
    st.pyplot(plt)

elif selected_option == "Product Insights":
    selected_product = st.selectbox("Select a product:", df["Product Name"].unique())
    product_df = df[df["Product Name"] == selected_product]

    st.subheader(f"Sales and Profit for {selected_product}")
    st.bar_chart(product_df[["Sales", "Profit"]], color='#357b72')


