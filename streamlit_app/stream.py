import streamlit as st 
import mysql.connector as connector

host = "localhost"
port = 3306
database = "olist_db"
user = "root"
password = "root1234"

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * FROM olist_sales_by_date_hour_city_category;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")