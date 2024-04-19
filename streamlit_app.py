
import streamlit as st
import pandas as pd
import plotly.express as px
 
# Reading the entire workbook
data = pd.ExcelFile("Global Superstore lite.xlsx")

# Reading each sheet into a DataFrame
superSales = data.parse('Orders')
returns_df = data.parse('Returns')
people_df = data.parse('People')

# Setting page config
st.set_page_config(page_title="Super Store Dashboard", 
                   page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Map-circle-blue.svg/1024px-Map-circle-blue.svg.png",
                   initial_sidebar_state="expanded",
                   )

# the layout Variables
hero = st.container()
topRow = st.container()
midRow = st.container()
chartRow = st.container()
footer = st.container()

# Sidebar
with st.sidebar:
    st.markdown(f'''
        <style>
        section[data-testid="stSidebar"] {{
                width: 500px;
                background-color: #000b1a;
                }}
        section[data-testid="stSidebar"] h1 {{
                color: #e3eefc;
                }}
        section[data-testid="stSidebar"] p {{
                color: #ddd;
                text-align: left;
                }}
        section[data-testid="stSidebar"] svg {{
                fill: #ddd;
                }}
        </style>
    ''',unsafe_allow_html=True)
    st.title(":anchor: About the dataset")
    st.markdown("The growth of supermarkets in most populated cities are increasing and market competitions are also high. In this dashboard we'll give it a try and turn everything into a readable visualizations.")

    # The Selectbox
    Product_lines = superSales['Product_line'].unique()
    line = st.selectbox('',['Choose the Product Line'] + list(Product_lines))
    if line == 'Choose the Product Line':
        chosen_line = superSales
    else:
        chosen_line = superSales[superSales['Product_line'] == line]

    # Customizing the select box
    st.markdown(f'''
    <style>
        .stSelectbox div div {{
                background-color: #fafafa;
                color: #333;
        }}
        .stSelectbox div div:hover {{
                cursor: pointer
        }}
        .stSelectbox div div .option {{
                background-color: red;
                color: #111;
        }}
        .stSelectbox div div svg {{
                fill: black;
        }}
    </style>
    ''', unsafe_allow_html=True)

    with chartRow:
    # Filter for the month
        superSales['Order_date'] = pd.to_datetime(superSales['Order_date'])
    mar_data = (superSales['Order_date'].dt.month == 3)
    lineQuantity = chosen_line[(mar_data)]

    # Quantity for each day
    quantity_per_day = lineQuantity.groupby('Order_date')['Quantity'].sum().reset_index()

    # some space
    st.markdown('<div></div>', unsafe_allow_html=True)
    
    # Create a line chart for Quantity over the last month using Plotly
    fig_quantity = px.line(
        quantity_per_day, 
        x='Order_date', 
        y='Quantity', 
        title='Quantity Sold over the Last Month'
    )
    fig_quantity.update_layout(
        margin_r=100,
    )
    st.plotly_chart(fig_quantity)