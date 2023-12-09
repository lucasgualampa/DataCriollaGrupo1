import streamlit as st 
import mysql.connector as connector

host = "localhost"
port = 3306
database = "olist_db"
user = "root"
password = "root1234"


connection = connector.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)


from sqlalchemy.exc import SQLAlchemyError

try:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM olist_sales_by_date_hour_city_category")

    results = cursor.fetchall()

    st.dataframe(results)
except SQLAlchemyError as e:
    st.error(f"Error retrieving data: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()