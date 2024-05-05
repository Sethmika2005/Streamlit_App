import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the dataset
df = pd.read_excel("Superstore.xlsx")

# Set Streamlit app title
st.title("Sales and Profit Dashboard")

# Create columns for layout
col1, col2, col3 = st.columns(3)

# Calculate KPIs and round to the nearest whole number as per the format
total_sales = "${:,.0f}".format(round(df["Sales"].sum()))
total_quantity = "{:,.0f} units".format(round(df["Quantity"].sum()))  # Appending 'units' to total quantity
total_profit = "${:,.0f}".format(round(df["Profit"].sum()))

# Display KPIs in separate columns
with col1:
    st.metric("Total Sales", total_sales)

with col2:
    st.metric("Total Quantity", total_quantity)

with col3:
    st.metric("Total Profit", total_profit)

# Create a sidebar with tiles
with st.sidebar:
    selected_option = st.radio("Select an option:", ["Sales Overview", "Profit Analysis", "Product Insights"])
    
    # Filter by date range
    st.sidebar.subheader("Date Range Filter")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime(df["Order Date"]).min())
    end_date = st.sidebar.date_input("End Date", pd.to_datetime(df["Order Date"]).max())

    # Filter by Region
    st.sidebar.subheader("Region Filter")
    all_regions = ["All"] + list(df["Region"].unique())
    selected_region = st.sidebar.selectbox("Select Region", all_regions)
    
    # Filter by Country
    st.sidebar.subheader("Country Filter")
    all_countries = ["All"] + list(df["Country"].unique())
    selected_country = st.sidebar.selectbox("Select Country", all_countries)
    
    # Filter by State
    st.sidebar.subheader("State Filter")
    all_states = ["All"] + list(df["State"].unique())
    selected_state = st.sidebar.selectbox("Select State", all_states)
    
    # Filter by Sub-Category
    st.sidebar.subheader("Sub-Category Filter")
    all_sub_categories = ["All"] + list(df["Sub-Category"].unique())
    selected_sub_category = st.sidebar.selectbox("Select Sub-Category", all_sub_categories)

# Filter options
if selected_option == "Sales Overview":
    filtered_df = df[
        (df["Order Date"] >= pd.Timestamp(start_date)) & 
        (df["Order Date"] <= pd.Timestamp(end_date)) &
        (df["Region"] if selected_region == "All" else df["Region"] == selected_region) &
        (df["Country"] if selected_country == "All" else df["Country"] == selected_country) &
        (df["State"] if selected_state == "All" else df["State"] == selected_state) &
        (df["Sub-Category"] if selected_sub_category == "All" else df["Sub-Category"] == selected_sub_category)
    ]


#Colour palete
colour_palete=['#357b72', '#6b9b8e', '#99bcb5', '#c8dedb']

# Filter options
if selected_option == "Sales Overview":
    st.subheader("Monthly Sales Trend")
    st.line_chart(filtered_df.set_index("Order Date")["Sales"], color='#357b72')

    # Sum of Sales by Segment and by Category
    # Create columns for layout
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sales by Segment")
        segment_sales = px.pie(filtered_df.groupby("Segment")["Sales"].sum(), values='Sales', names=filtered_df.groupby("Segment")["Sales"].sum().index, color_discrete_sequence=colour_palete)
        st.plotly_chart(segment_sales, use_container_width=True)
        
    with col2:
        st.subheader("Sales by Category")
        category_sales = px.pie(filtered_df.groupby("Category")["Sales"].sum(), values='Sales', names=filtered_df.groupby("Category")["Sales"].sum().index, color_discrete_sequence=colour_palete)
        st.plotly_chart(category_sales, use_container_width=True)
   
    # Sum of Sales by Market
    st.subheader("Sales by Market")
    market_sales = filtered_df.groupby("Market")["Sales"].sum()
    st.bar_chart(market_sales, color='#357b72')

    # Sum of Sales by Discount
    st.subheader("Sales by Discount")
    discount_sales = filtered_df.groupby("Discount")["Sales"].sum()
    st.bar_chart(discount_sales, color='#357b72')

elif selected_option == "Profit Analysis":
    filtered_df = df[
        (df["Order Date"] >= pd.Timestamp(start_date)) & 
        (df["Order Date"] <= pd.Timestamp(end_date)) &
        (df["Region"] if selected_region == "All" else df["Region"] == selected_region) &
        (df["Country"] if selected_country == "All" else df["Country"] == selected_country) &
        (df["State"] if selected_state == "All" else df["State"] == selected_state) &
        (df["Sub-Category"] if selected_sub_category == "All" else df["Sub-Category"] == selected_sub_category)
    ]

    st.subheader("Profit Trend over Time")
    st.line_chart(filtered_df.set_index("Order Date")["Profit"], color='#357b72')

    st.subheader("Profit vs. Discount")
    sns.scatterplot(data=filtered_df, x="Discount", y="Profit", color='#357b72')
    st.pyplot(plt)

    # Sum of Sales by Segment and by Category
    # Create columns for layout
    col1, col2 = st.columns(2)
    with col1:   
        # Sum of Profit by Segment
        st.subheader("Profit by Segment")
        segment_profit = px.pie(filtered_df.groupby("Segment")["Profit"].sum(), values='Profit', names=filtered_df.groupby("Segment")["Profit"].sum().index, color_discrete_sequence=colour_palete)
        st.plotly_chart(segment_profit, use_container_width=True)
    
    with col2:
        # Sum of Profit by Category
        st.subheader("Profit by Product Category")
        category_profit = px.pie(filtered_df.groupby("Category")["Profit"].sum(), values='Profit', names=filtered_df.groupby("Category")["Profit"].sum().index, color_discrete_sequence=colour_palete)
        st.plotly_chart(category_profit, use_container_width=True)

    # Sum of Profit by Market
    st.subheader("Profit by Market")
    market_profit = filtered_df.groupby("Market")["Profit"].sum()
    st.bar_chart(market_profit, color='#357b72')

    # Sum of Profit by Discount
    st.subheader("Profit by Discount")
    discount_profit = filtered_df.groupby("Discount")["Profit"].sum()
    st.bar_chart(discount_profit, color='#357b72')

elif selected_option == "Product Insights":
    selected_product = st.selectbox("Select a product:", filtered_df["Product Name"].unique())
    product_df = filtered_df[filtered_df["Product Name"] == selected_product]

    st.subheader(f"Sales and Profit for {selected_product}")
    st.bar_chart(product_df[["Sales", "Profit"]], color='#357b72')
