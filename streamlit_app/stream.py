import streamlit as st
from sqlalchemy.pool import SingletonPool

host = "localhost"
port = 3306
database = "olist_db"
user = "root"
password = "root1234"

# Initialize connection with SingletonPool.
conn = st.connection('mysql', type='sql', connect_args={'poolclass': SingletonPool})

# Perform query.
df = conn.query('SELECT * FROM olist_orders_dataset')

# Print results.
st.dataframe(df)