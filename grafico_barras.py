import pandas as pd
import plotly.express as px

def crear_grafico(df):
    # Generar tabla para graficar.  Se van a mostrar los ingresos por producto.  Se van a agrupar los productos por el nombre del producto product_category_name.  Una vez agrupada se suma la columna valor total para tener los ingresos por producto.  Se ordenan ascendentemente por el nomnbre de la columna valor total.  Para que sea un dataframe se aplica reset_index.  Los productos de mayores ingresos quedarán al final de la tabla.
    revenue_productos = df.groupby('product_category_name')[['valor_total']].sum().sort_values('valor_total', ascending = True).reset_index()

    # crear figura
    fig = px.bar(revenue_productos.tail(10),
        x = 'valor_total',
        y = 'product_category_name',
        text = 'valor_total',
        title = 'Top ingresos por producto ($)'
    )

    fig.update_layout(yaxis_title =  'Productos', xaxis_title = 'Ingresos ($)', showlegend = False)
    # formatear número que se muestra encima de las barras, maximo con tres caracteres
    fig.update_traces(texttemplate = '%{text:.3s}')

    return fig