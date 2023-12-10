import streamlit as st 

host = "localhost"
port = 3306
database = "olist_db"
user = "root"
password = "root1234"

# Initialize connection.
conn = st.connection('mysql', type='sql', persist="disk")

# Perform query.
df = conn.query('SELECT * FROM olist_orders_dataset', ttl=600)

# Print results.
st.dataframe(df)