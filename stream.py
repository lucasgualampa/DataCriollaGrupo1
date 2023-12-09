import subprocess
import sys
import os
#import pandas as pd

#import matplotlib.pyplot as plt
#import seaborn as sns
#import plotly.express as px
#import mysql.connector as connector
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
    password=password,
    driver = "pymysql"
)

if connection.is_connected():
    print("Conectado a la base de datos")
else:
    print("Error al conectar a la base de datos")

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Reemplaza 'sqlite:///mi_basededatos.db' con tu cadena de conexión y tipo de base de datos
engine = create_engine('mysql+mysqlconnector://root:root1234@localhost/olist_db')

# Consultar los datos
cursor = connection.cursor()
cursor.execute("SELECT * FROM olist_sales_by_date_hour_city_category")

# Obtener los resultados
results = cursor.fetchall()

st.dataframe(results)
# Cerrar la conexión
#connection.close()