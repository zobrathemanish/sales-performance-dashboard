import streamlit as st
import pandas as pd
import plotly.express as px

# Load data with specified encoding
data = pd.read_csv("Ecommerce_data.csv", encoding="ISO-8859-1")  # Adjust path if necessary
data['order_date'] = pd.to_datetime(data['order_date'], dayfirst=True) # Convert order_date to datetime

# Streamlit app setup
st.set_page_config(page_title="E-commerce Sales Dashboard", layout="wide")
st.title("E-commerce Sales Insights Dashboard 🛒")

# Sidebar for filters
st.sidebar.header("Filters")
selected_category = st.sidebar.selectbox("Select Category", options=data['category_name'].unique(), index=0)
selected_segment = st.sidebar.selectbox("Select Customer Segment", options=data['customer_segment'].unique(), index=0)

# Filter data based on sidebar selections
filtered_data = data[(data['category_name'] == selected_category) & (data['customer_segment'] == selected_segment)]

# KPIs
st.header("📊 Key Metrics")
total_sales = filtered_data['sales_per_order'].sum()
total_profit = filtered_data['profit_per_order'].sum()
total_orders = filtered_data['order_id'].nunique()
average_order_value = total_sales / total_orders if total_orders else 0
average_profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Average Order Value", f"${average_order_value:,.2f}")
col4.metric("Profit Margin (%)", f"{average_profit_margin:.2f}%")

# Sales by Product
st.header("🛍️ Sales by Product")
fig_product_sales = px.bar(filtered_data, x='product_name', y='sales_per_order',
                           title='Sales by Product', color='sales_per_order', 
                           color_continuous_scale='Blues')
st.plotly_chart(fig_product_sales, use_container_width=True)

# Profit by Category
st.header("💰 Profit by Category")
profit_by_category = filtered_data.groupby('category_name')['profit_per_order'].sum().reset_index()
fig_profit_category = px.pie(profit_by_category, values='profit_per_order', names='category_name',
                             title='Profit Distribution by Category', hole=0.4, 
                             color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig_profit_category, use_container_width=True)

# Sales Over Time
st.header("📈 Sales and Profit Over Time")
monthly_sales = filtered_data.resample('M', on='order_date').sum()
fig_sales_time = px.line(monthly_sales, x=monthly_sales.index, y='sales_per_order', title='Monthly Sales Over Time')
fig_sales_time.add_scatter(x=monthly_sales.index, y=monthly_sales['profit_per_order'], mode='lines', name='Profit')
st.plotly_chart(fig_sales_time, use_container_width=True)

# Top 10 Products by Sales
st.header("🏆 Top 10 Products by Sales")
top_products = filtered_data.groupby('product_name')['sales_per_order'].sum().nlargest(10).reset_index()
fig_top_products = px.bar(top_products, x='sales_per_order', y='product_name', 
                          title='Top 10 Products by Sales', orientation='h', color='sales_per_order',
                          color_continuous_scale='viridis')
st.plotly_chart(fig_top_products, use_container_width=True)

# Average Shipping Time
st.header("🚚 Average Shipping Time by Delivery Status")
shipping_time = filtered_data.groupby('delivery_status')['days_for_shipment_real'].mean().reset_index()
fig_shipping_time = px.bar(shipping_time, x='delivery_status', y='days_for_shipment_real',
                           title='Average Shipping Time by Delivery Status', color='days_for_shipment_real',
                           color_continuous_scale='reds')
st.plotly_chart(fig_shipping_time, use_container_width=True)

# Region-wise Sales Analysis (Map)
st.header("🌍 Region-wise Sales Analysis")
fig_region_sales = px.scatter_geo(filtered_data, locationmode='country names', locations='customer_country', 
                                  size='sales_per_order', color='customer_region', title='Sales by Region',
                                  hover_name='customer_city', projection="natural earth")
st.plotly_chart(fig_region_sales, use_container_width=True)

# Footer
st.markdown("### Insights")
st.write("This dashboard provides key insights into the sales and profitability of different products, categories, and regions, helping stakeholders make data-driven decisions.")

st.markdown("---")
st.caption("Created with ❤️ by Manish | E-commerce Sales Insights Dashboard")

# Run the app with `streamlit run app.py`
