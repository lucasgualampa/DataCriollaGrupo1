import streamlit as st 

host = "localhost"
port = 3306
database = "olist_db"
user = "root"
password = "root1234"

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * FROM olist_orders_dataset')

# Print results.
st.dataframe(df)