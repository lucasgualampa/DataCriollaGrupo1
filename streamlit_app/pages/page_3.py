import mysql.connector
import streamlit as st
import pandas as pd

st.markdown("# Page 3 🎉")
st.sidebar.markdown("# Page 3 🎉")

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

st.write("""
Ploteo:
""")
