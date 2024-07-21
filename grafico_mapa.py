import pandas as pd
import plotly.express as px

def crear_grafico(df):
    # crear una nueva tabla agrupando por estado, y calculando la suma del valor_total para cada uno, asi como el promedio para latitud y longigud.  reset_index para que se convierta en dataframe. sort_values para ordenar por valor_total de manera descendente.
    df_mapa = df.groupby('geolocation_state').agg(
        {'valor_total' : 'sum', 
        'geolocation_lat' : 'mean',
        'geolocation_lng' : 'mean'
    }).reset_index().sort_values(by='valor_total', ascending=False)

    # Crear mapa
    graf_mapa = px.scatter_geo(df_mapa,
        lat = 'geolocation_lat',
        lon = 'geolocation_lng',
        scope = 'south america',
        template = 'seaborn',
        size = 'valor_total',
        hover_name =  'geolocation_state',
        hover_data = {'geolocation_lat' : False, 'geolocation_lng' : False},
        title = 'Ingresos por estado'
    )
    return graf_mapa
