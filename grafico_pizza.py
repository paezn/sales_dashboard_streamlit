import pandas as pd
import plotly.express as px

def crear_grafico(df):
    # crear tabla agrupada por reviwe_score.  Mostrar la cantidad de ventas por cada una de las 5 calificaciones. Se suma la cantidad de itens vendidos de cada producto
    df_review = df.groupby('review_score').agg(
        total_ventas = ('cantidad_itens', 'sum')
    ).reset_index()

    colors = ['#0077b6', '#1A4D83', '#063970', '#2f567D', '#4B6A92']

    fig = px.pie(df_review,
        values = 'total_ventas',        
        names = 'review_score',
        title = 'Calificación de las ventas',
        color_discrete_sequence = colors
    )

    fig.update_layout(yaxis_title = 'Calificación', xaxis_title = 'Ventas', showlegend = False)

    # actualizar textos que se muestran dentro del grafico
    fig.update_traces(textposition = 'inside', textinfo = 'percent+label', insidetextfont = dict(size=16))

    return fig