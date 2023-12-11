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


""" # CARGA DEL MODELO #
model_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "C:/Users/Lucas/Desktop/consultorBI/DataCriollaGrupo1/streamlit_app/pages/forecast_olis.json")
model = model_from_json(open(model_path, 'r').read()) """


# PREFICCION #


def predicción(df_fechas):
    df_pred = model.predict(df_fechas)
    return df_pred


def df_rango_fechas(start, end):
    lista_fechas = [start + timedelta(days=d)
                    for d in range((end - start).days+1)]
    ds = pd.DataFrame({'ds': lista_fechas})
    return ds

# PLOTEO #


def plot(df_predicted, df_real, ds):
    """plotea serie de tiempo

    Args:
        df_predicted (datetime): dataframe con predicciones
        df_real (datetime): dataframe con valores reales
        ds (datetime): rango de fechas
    """
    #df_real = df_real[df_real.loc[ds['ds']]]
    trace1 = go.Scatter(
        x=df_real.index, y=df_real['y'], mode='markers', name='Real', marker=dict(color='mediumpurple'))
    trace2 = go.Scatter(x=df_predicted['ds'], y=df_predicted['yhat'],
                        mode='lines', name='Predicción', line=dict(color='red'))
    fig = go.Figure(data=[trace1, trace2])
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Ventas')
    # Show the figure
    return fig

# LAYOUT PRINCIPAL #
def main():
    # TITULOS
    st.title('Forcasting de ventas :chart_with_upwards_trend:')
    st.markdown('---')

    # CARGA DEL DATAFRAME
    with st.spinner('Extrayendo datos...'):
        df_d = get_df_transformed()
        connection.close()
    st.success('Datos cargados exitosamente!')
    st.markdown(""" Es importante analizar y entender la evolución y el comportamiento de 
                los datos reales de venta a lo largo del tiempo. Por eso se presentan los componentes
                de la serie a partir de la predicción correspondiente.""")

    # SIDEBAR
    with st.sidebar:
        st.subheader('For our client:')
        st.subheader('Made with :heart: by:')

    st.header('Predicción con rango de fechas')

    # Slicer
    start_date = st.date_input(label="Fecha de inicio",
                               value=datetime.strptime("2017-06-13", "%Y-%m-%d"))
    end_date = st.date_input(label="Fecha de fin",
                             value=datetime.strptime("2018-12-18", "%Y-%m-%d"))  # , format="Y-%m-%d"

    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date:`%s`' %
                   (start_date, end_date))
        slider = st.slider(
            'Selecciona el rango de fechas de predicción', min_value=start_date, value=(start_date, end_date))
        st.write("Tu rango de predicción es:", slider)
        # Dataframe de fechas

        if st.button(label='Aplicar'):
            ds = df_rango_fechas(slider[0], slider[1])
            df_predict = model.predict(ds)
            st.subheader("Predicción de venta diaria")
            figura = plot(df_predict, df_d, ds)
            st.plotly_chart(figura, sharing="streamlit", theme="streamlit")
        else:
            st.write('Click en el boton')

    else:
        st.error('Error: End date must fall after start date.')


""" if __name__ == "__main__":
    main() """

cursor.execute("SELECT * FROM olist_orders_count_by_date")
orders_by_date = cursor.fetchall()
orders_by_date_df = pd.DataFrame(orders_by_date, columns=cursor.column_names)

cursor.execute("SELECT * FROM olist_order_payments_dataset")
payments_order = cursor.fetchall()
payments_order_df = pd.DataFrame(payments_order, columns=cursor.column_names)

items_agrupado = order_items_df.groupby(by=['order_id']).sum()
items_agrupado['price'].sum()
items_agrupado.shape
items_agrupado.reset_index(inplace=True)
items_agrupado.head()
items_agrupado.duplicated(subset=['order_id'],keep=False).sum()

payments_agrupado = payments_order_df.groupby(by='order_id').sum()
payments_agrupado.reset_index(inplace=True)
payments_agrupado.head()

df_merge = orders_by_date_df.merge(payments_agrupado[['order_id','payment_value']], how = 'left', on='order_id').merge(items_agrupado[['order_id','price']], how = 'left', on='order_id')
df_merge



df_d = df_ts.resample('D').sum()
# Instanciamos y entrenamos el modelo
md = Prophet()
#md.add_seasonality(name='monthly', period=30.5, fourier_order=5)
md.fit(df_d.reset_index())

fig = md.plot(forecast_d)
