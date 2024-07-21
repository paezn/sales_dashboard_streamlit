import pandas as pd
import plotly.express as px

def crear_grafico(df):
    # Crear una tabla agrupada por mes, año y nombre del mes, mostrando las ventas de ese mes

    # set_index crea el indice del nuevo dataframe. el indice es la propia columna order_purchase_timestamp.  Agrupar por mes usando el metodo Grouper, que genera frecuencias a través de algún valor dentro del datetime.  Se suma la columna valor_total.  reset_index para convertir en un dataframe con dos columnas: valor_total y order_purchase_timestamp
    revenues_monthly = df.set_index('order_purchase_timestamp').groupby(pd.Grouper(freq = 'ME'))['valor_total'].sum().reset_index()
    # Crear columna para el año
    revenues_monthly['Year'] = revenues_monthly['order_purchase_timestamp'].dt.year
    # crear columna para el mes
    revenues_monthly['Month'] = revenues_monthly['order_purchase_timestamp'].dt.month_name()
    # quitar el 2016, para mejorar gráfico
    revenues_monthly = revenues_monthly[revenues_monthly['Year'] > 2016]

    # crear figura
    fig = px.line(revenues_monthly,
        x = 'Month',
        y = 'valor_total',
        markers = True,
        range_y = (0,revenues_monthly.max()),
        color = 'Year',
        line_dash = 'Year',
        title = 'Ingresos mensuales'
        )
    # actualizar el layout.  Poniendo titulo al eje y
    fig.update_layout(yaxis_title = 'Ingresos ($)')

    return fig


