import mysql.connector
import streamlit as st
import pandas as pd

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

host = "localhost"
port = 3306
database = "olist_db"
user = "root"
password = "root1234"

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor= connection.cursor()

st.title('DataFrames:')

st.write("""
Ordenes:
""")
cursor.execute("SELECT * FROM olist_orders_dataset")
orders = cursor.fetchall()
orders_df = pd.DataFrame(orders, columns=cursor.column_names)
st.dataframe(orders_df)

st.write("""
Tratos Cerrados:
""")
cursor.execute("SELECT * FROM olist_closed_deals_dataset")
closedDeals = cursor.fetchall()
closedDeals_df = pd.DataFrame(closedDeals, columns=cursor.column_names)
st.dataframe(closedDeals_df)

st.write("""
Clientes:
""")
cursor.execute("SELECT * FROM olist_customers_dataset")
customers = cursor.fetchall()
customers_df = pd.DataFrame(customers, columns=cursor.column_names)
st.dataframe(customers_df)

st.write("""
Geolocalización:
""")
cursor.execute("SELECT * FROM olist_geolocation_dataset")
geolocation = cursor.fetchall()
geolocation_df = pd.DataFrame(geolocation, columns=cursor.column_names)
st.dataframe(geolocation_df)

st.write("""
Artículos encargados:
""")
cursor.execute("SELECT * FROM olist_order_items_dataset")
order_items = cursor.fetchall()
order_items_df = pd.DataFrame(order_items, columns=cursor.column_names)
st.dataframe(order_items_df)