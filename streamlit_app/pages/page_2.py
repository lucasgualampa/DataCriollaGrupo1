import mysql
import mysql.connector
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
from prophet.serialize import model_from_json
from prophet import Prophet


st.markdown("# Analisis de datos 📊")
st.sidebar.markdown("# Page 2 📊")

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
    Acercamiento a los datos
""")

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



st.write("""
Ordenes por fecha:
""")
cursor.execute("SELECT * FROM olist_orders_count_by_date")
orders_by_date = cursor.fetchall()
orders_by_date_df = pd.DataFrame(orders_by_date, columns=cursor.column_names)
st.dataframe(orders_by_date_df)

st.write("""
Ordenes de pago:
""")
cursor.execute("SELECT * FROM olist_order_payments_dataset")
payments_order = cursor.fetchall()
payments_order_df = pd.DataFrame(payments_order, columns=cursor.column_names)
st.dataframe(payments_order_df)


st.title("Graficos: ")
st.write("""
Tendencia sobre el total de observaciones de la serie:
""")
st.image('newplot.jpg', caption='tendencia con nulos')

st.write("""
Grafico la tendencia sobre el total de observaciones de la serie en base al precio:
""")
st.image('newplotwithoutnulls.jpg', caption='tendencia sin nulos')

st.write("""
Tendencias sobre el total de observaciones de la serie en base al promedio:
""")
st.image('sellpromvalues.jpg', caption='Valor promedio de ventas')

st.write("""
Tendencias sobre el total de observaciones de la serie en base a las operaciones:
""")
st.image('operationspromvalues.jpg', caption='Valor promedio de operaciones')

st.write("""
Estacionalidad:
""")
st.image('estacionalidadsemanal.jpg', caption='estacionalidad semanal')

st.write("""
Graficamos las tendencias en base la frecuencia diaria, semanal y mensual:
""")
st.image('tendenciasporfrecuencias.jpg', caption='tendencias por frecuencias')