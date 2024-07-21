import streamlit as st
import pandas as pd
import grafico_mapa as graf1
import grafico_lineas as graf2
import grafico_barras as graf3
import grafico_pizza as graf4

# Para mantener en modo ancho la visualizacion en ventana del navegador, por defecto
st.set_page_config(layout='wide')

# Poner un titulo a la pagina
st.title('Dashboard de ventas :shopping_trolley:')

# Funcion para dar formato a numeros
def formata_numero(valor, prefijo=''):
    for unidad in ['', 'k']:
        if valor<1000:
            return f'{prefijo} {valor:.2f} {unidad}'
        valor /= 1000
    return f'{prefijo} {valor:.2f} M'

# Abrimos la base de datos
df_ventas = pd.read_csv('https://raw.githubusercontent.com/paezn/sales_dashboard_streamlit/main/base_ventas.csv') 
# Crear nueva columna en dataframe
df_ventas['valor_total'] = (df_ventas.price * df_ventas.cantidad_itens) + (df_ventas.freight_value * df_ventas.cantidad_itens)
# Asegurarnos que este en datetime la columna de la fecha, para poder extraer año, dia, mes
df_ventas['order_purchase_timestamp'] = pd.to_datetime(df_ventas['order_purchase_timestamp'])
# Separar los nombres del los productos.  Se crea una columna unicamente con la primera palabra del producto
df_ventas['tipo_producto'] = df_ventas['product_category_name'].str.split('_').str[0]

# ########################
# Configuramos los filtros
# ########################
st.sidebar.image('escudoGuanenta.png')
st.sidebar.title('Filtros')

# Filtro para estados o ciudades
estados = sorted(list(df_ventas['geolocation_state'].unique()))
ciudades = st.sidebar.multiselect('Estados', estados)

# filtro para productos.  dropna quita valores nulos
productos = sorted(list((df_ventas['tipo_producto'].dropna().unique())))
# Agregar elemento 'Todos' al inicio de la lista
productos.insert(0,'Todos')
producto = st.sidebar.selectbox('Productos', productos)

# filtro para año
años = st.sidebar.checkbox('Todo el periodo', value = True)
if not años:
    año = st.sidebar.slider('Año', df_ventas['order_purchase_timestamp'].dt.year.min(), df_ventas['order_purchase_timestamp'].dt.year.max())

# #################################################
# Dar interactiviad a los datos - Filtrar los datos
# #################################################

# por ciudad
if ciudades:
    df_ventas = df_ventas[df_ventas['geolocation_state'].isin(ciudades)]

# por producto
if producto != 'Todos':
    df_ventas = df_ventas[df_ventas['tipo_producto'] == producto]

# por año
if not años: # años es el checkbox
    df_ventas = df_ventas[df_ventas['order_purchase_timestamp'].dt.year == año] # año es el slider

# #####################
# Llamar a los gráficos
# #####################
graf_mapa = graf1.crear_grafico(df_ventas)
graf_lineas = graf2.crear_grafico(df_ventas)
graf_barras = graf3.crear_grafico(df_ventas)
graf_pizza = graf4.crear_grafico(df_ventas)

# Metricas
# Mostrar en dos columnas
col1, col2 = st.columns(2)
with col1:
    st.metric('**Total de Revenues**', formata_numero(df_ventas['valor_total'].sum(), '$'))
    # Mostrar mapa
    st.plotly_chart(graf_mapa, use_container_width=True)# respetar ancho de columna
    # mostrar grafico de barras
    st.plotly_chart(graf_barras, use_container_width=True)
with col2:
    st.metric('**Total de ventas**', formata_numero(df_ventas['cantidad_itens'].sum()))
    # mostrar grafico de lineas
    st.plotly_chart(graf_lineas, use_container_width=True)
    # mostrar grafico pizza
    st.plotly_chart(graf_pizza, use_container_width=True)


# Mostrar dataframe
# st.dataframe(df_ventas)