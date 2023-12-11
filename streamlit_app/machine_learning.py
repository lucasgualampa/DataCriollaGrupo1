# Primero realizamos importaciones necesarios
import pandas as pd
import numpy as np
import os
import sys
import subprocess
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import performance_metrics
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import seaborn as sns

#Descomentar en caso de necesitar instalar alguna dependencia
""" python_executable = sys.executable

# El nombre del paquete que deseas instalar
nombre_del_paquete = "prophet"

# Utiliza subprocess para ejecutar el comando de instalación
comando = [python_executable, "-m", "pip", "install", nombre_del_paquete]

# Ejecuta el comando
try:
    subprocess.check_call(comando)
    print(f"El paquete {nombre_del_paquete} se instaló correctamente.")
except subprocess.CalledProcessError as e:
    print(f"Error al instalar el paquete {nombre_del_paquete}.")
    print(f"Error: {e}") """



# Analisamos los datasets limpios con el ETL realizado que vamos a utilizar
df_orders = pd.read_csv("C:/Users/Lucas/Desktop/consultorBI/DataCriollaGrupo1/streamlit_app/datasets/olist_orders_dataset.csv")
#print(df_orders.info())

""" 
 0   order_id                       96475 non-null  object
 1   customer_id                    96475 non-null  object
 2   order_status                   96475 non-null  object
 3   order_purchase_timestamp       96475 non-null  object 
"""

df_orders_items = pd.read_csv("C:/Users/Lucas/Desktop/consultorBI/DataCriollaGrupo1/streamlit_app/datasets/olist_order_items_dataset.csv")
#print(df_orders_items.info())

"""  
5   price                112650 non-null  float64
"""

df_customers = pd.read_csv("C:/Users/Lucas/Desktop/consultorBI/DataCriollaGrupo1/streamlit_app/datasets/olist_customers_dataset.csv")
#print(df_customers.info())

""" 
 0   customer_id               99441 non-null  object
 3   customer_city             99441 non-null  object
 4   customer_state            99441 non-null  object
"""

# Unimos tablas segun la PK
df_merged = pd.merge(df_customers, df_orders, on="customer_id")
#print(df_merged.info())

df_final = pd.merge(df_merged, df_orders_items, on="order_id")
#print(df_final.info())

# Sacamos columnas que no vamos a utilizar
df_final_clean = df_final.drop(columns=["customer_zip_code_prefix", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "shipping_limit_date"])
#print(df_final_clean.info())
#print(df_final["order_approved_at"].value_counts())
df_final_clean.order_purchase_timestamp = pd.to_datetime(df_final_clean.order_purchase_timestamp)
#print(df_final_clean.columns)
#df_final_clean = df_final_clean.set_index("order_purchase_timestamp")
#print(df_final_clean.columns)
#df_final_clean.index = df_final_clean.index.to_period('D')
#print(df_final_clean.head())


# Realizamos un df en base a 2 columnas, limpiamos nulos y ordenamos
df_ts = df_final_clean[['order_purchase_timestamp', 'price']]
df_ts.dropna(inplace=True)
df_ts.reset_index(inplace=True)
df_ts.sort_values(by=['order_purchase_timestamp'], inplace=True, ignore_index=True)
# CSV con index para streamlit 
#df_ts.to_csv("df_ts_index.csv")

# Eliminamos la columna index, ya que no lo vamos a utilizar
df_ts2 = df_ts.drop(columns=["index"])
df_ts2.set_index('order_purchase_timestamp', inplace = True) 
df_d = df_ts2.resample('D').sum() # convertimos la frecuencia a Diaria
df_d['y_mean'] = df_ts2.resample('D').mean() # promedio
df_d['y_operations'] = df_ts2.resample('D').count() # contamos los valores no nulos
df_d.isna().sum()
# Se arma un dataset df_d_na para mostrar los lugares donde hay nulos
df_d_na = df_d.copy()
df_d_na['y_na'] = np.nan
df_d_na['y_na'] = df_d_na['price'].where(df_d_na['price'].notna(),other=0)
df_d_na['y_na'] = df_d_na['y_na'].where(df_d_na['y_na']==0,other=np.nan)
# Tendencias sobre el total de observaciones de la serie
trace1 = go.Scatter(x=df_d_na.index, y=df_d_na['price'],mode='markers', name='Ventas diarias', marker=dict(color='green'))
trace2 = go.Scatter(x=df_d_na.index, y=df_d_na['y_na'],mode='markers', name='Nulos')
# Create the figure with both scatter plots
fig = go.Figure(data=[trace1,trace2])
fig.update_layout( 
                  title=dict(text="Venta diaria", font=dict(size=24)), 
                  xaxis_title='Fecha', 
                  yaxis_title='Ventas')
# Show the figure
#fig.show()

df_d.notna().sum() # el nro de valor no nulos
df_ts.index.nunique() # el nrop de valores unicos en el index

df_d.shape # el nro de filas y el nro de columnas
df_d.isna().sum() # devuelve el nro de valores nulos
##############################################################################
#reestructuracion del dataset
df_d = df_d.loc['2017-01-01':'2018-08-31'].interpolate() # eliminamos el periodo donde hubieron valores nulos
# creo un csv para poder usarlo en streamlit
#df_d.to_csv("df_d_reestructure.csv")

# Grafico la tendencia sobre el total de observaciones de la serie en base al precio
trace1 = go.Scatter(x=df_d.index, y=df_d['price'],mode='lines', name='Valor de venta diaria')#, marker=dict(color='green'))
# Create the figure with both scatter plots
fig = go.Figure(data=[trace1])
fig.update_layout( 
                  title=dict(text="Venta diaria por fecha", font=dict(size=24)), 
                  xaxis_title='Fecha', 
                  yaxis_title='Ventas')
# Show the figure
#fig.show()

##############################################################################
# Tendencias sobre el total de observaciones de la serie en base al promedio
trace1 = go.Scatter(x=df_d.index, y=df_d['y_mean'],mode='lines', name='Valor de venta diaria',line=dict(color='green'))#, marker=dict(color='green'))
# Create the figure with both scatter plots
fig = go.Figure(data=[trace1])
fig.update_layout( 
                  title=dict(text="Valor promedio de venta", font=dict(size=24)), 
                  xaxis_title='Fecha', 
                  yaxis_title='Venta')
# Show the figure
#fig.show()

##############################################################################
# Tendencias sobre el total de observaciones de la serie en base a las operaciones
trace1 = go.Scatter(x=df_d.index, y=df_d['y_operations'],mode='lines', name='Cantidad de operaciones',line=dict(color='red'))#, marker=dict(color='green'))
# Create the figure with both scatter plots
fig = go.Figure(data=[trace1])
fig.update_layout( 
                  title=dict(text="Operaciones diarias", font=dict(size=24)), 
                  xaxis_title='Fecha', 
                  yaxis_title='Venta')
# Show the figure
#fig.show()

##############################################################################
# graficamos la estacionalidad 
fig = go.Figure(data=go.Box(x=df_d.index.day_name(),y=df_d.price))
fig.update_layout(title='Estacionalidad semanal', xaxis_title='Día de la semana', yaxis_title='Ventas')
#fig.show()


##############################################################################
#Tendencia
# Graficamos las tendencias en base la frecuencia diaria, semanal y mensual.
df_w = df_d.resample('W',convention='start').sum() # la frecuencia semanal
df_m = df_d.resample('M',convention='start').sum() # la frecuencia mensual

# Tendencias sobre el total de observaciones de la serie
trace1 = go.Scatter(x=df_d.index, y=df_d['price'], mode='lines', name='Diaria', fillcolor='blue')
trace2 = go.Scatter(x=df_w.index, y=df_w['price'], mode='lines', name='Semanal', fillcolor='red')
trace3 = go.Scatter(x=df_m.index, y=df_m['price'], mode='lines', name='Mensual', fillcolor='green')
# Create the figure with both scatter plots
fig = go.Figure(data=[trace1, trace2,trace3])
fig.update_layout(title='Tendencia de ventas', xaxis_title='Fecha', yaxis_title='Ventas')
# Show the figure
#fig.show()


##############################################################################
# Forecasting frecuencia diaria

# Instanciamos y entrenamos el modelo
df_ts3 = df_ts.drop(columns=["index"])
df_ts3.rename(columns={'order_purchase_timestamp':'ds','price':'y'}, inplace=True)
md = Prophet()
#md.add_seasonality(name='monthly', period=30.5, fourier_order=5)
md.fit(df_ts3)

# Prediccion
future_d = md.make_future_dataframe(periods=180)
forecast_d = md.predict(future_d)
#print(forecast_d[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

#fig = md.plot(forecast_d)
#a = add_changepoints_to_plot(fig.gca(), md, forecast_d)
#fig.show()

#fig = md.plot_components(forecast_d)
#fig.show()

