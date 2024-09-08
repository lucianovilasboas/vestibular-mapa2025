import streamlit as st 
import pandas as pd 
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
from functions import ler_coordenadas, ler_dados

st.set_page_config(layout="wide")

df_ = ler_dados()
df_mun_geo = ler_coordenadas()

st.title('📊 Análise Geográfica de Inscrições - IFMG 2025')


st.header(f'🗺️ Mapa 1...', divider='rainbow')
col = st.container()
campus_lista = df_["Campus_UF"].sort_values().unique() 


with col:
    campus = st.multiselect (
    "📶 Campus...",
        campus_lista, campus_lista,  
        placeholder="Selecione o campus...",
        key='options_col'
    )

    df_filtered = df_[ df_['Campus_UF'].isin(campus)]
    # df_filtered =  df_filtered[["CPF","Nome","Cidade","Campus","Curso","Cidade_UF","Campus_UF"]]


    by = ['Cidade_UF']

    df_filtered_g =  df_filtered.groupby(by).count()[['Inscricao']].sort_values('Inscricao', ascending=False).reset_index()
    df_filtered_g["Cidade_Lat"] = df_filtered_g["Cidade_UF"].apply(lambda c: df_mun_geo.loc[c]["latitude"] )
    df_filtered_g["Cidade_Lon"] = df_filtered_g["Cidade_UF"].apply(lambda c: df_mun_geo.loc[c]["longitude"] )
    df_filtered_g.rename(columns={"Inscricao":"Total"}, inplace=True)

    # Gerar mapa de dispersão
    fig = px.scatter_mapbox(df_filtered_g, 
                            lat="Cidade_Lat", 
                            lon="Cidade_Lon", 
                            hover_name=by[0], 
                            hover_data=["Total"], 
                            color="Total",
                            size="Total", 
                            color_continuous_scale=px.colors.cyclical.HSV, 
                            size_max=50, zoom=6, title="Distribuição de Inscrições por Cidade")

    # Configuração do mapa
    # fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(mapbox_style="carto-positron") 
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500, 
                      mapbox_center={"lat": -19.91018, "lon": -43.92657})
    
    fig.update_layout(showlegend=False)
    # Exibir gráfico
    col.plotly_chart(fig, use_container_width=True)



st.header(f'🌐 Mapa 2..', divider='rainbow')
col3, col4 = st.columns(2)
campus_lista_default = campus_lista[:5]
with col3:
   campus2 = st.multiselect (
    "📶 Campus...",
        campus_lista, campus_lista_default,  
        placeholder="Selecione o campus...",
        key='options_col2'
   )

with col4 :
   filter = st.slider("📶 Filtro...", 1, 10, 5, 1)

col2 = st.container()
with col2:

   df_filtered = df_[ df_['Campus_UF'].isin(campus2)]
#    df_filtered =  df_filtered[["CPF","Nome","Cidade","Campus","Curso","Cidade_UF","Campus_UF"]]
   df_filtered_g =  df_filtered.groupby(['Cidade_UF','Campus_UF']).count()[['Inscricao']].sort_values('Inscricao', ascending=False).reset_index()
   df_filtered_g["Cidade_Lat"] = df_filtered_g["Cidade_UF"].apply(lambda c: df_mun_geo.loc[c]["latitude"] )
   df_filtered_g["Cidade_Lon"] = df_filtered_g["Cidade_UF"].apply(lambda c: df_mun_geo.loc[c]["longitude"] )
   df_filtered_g["Campus_Lat"] = df_filtered_g["Campus_UF"].apply(lambda c: df_mun_geo.loc[c]["latitude"] )
   df_filtered_g["Campus_Lon"] = df_filtered_g["Campus_UF"].apply(lambda c: df_mun_geo.loc[c]["longitude"] )
   df_filtered_g.rename(columns={"Inscricao":"Total"}, inplace=True)

   # Função para gerar pontos intermediários para curvar as linhas (Bezier curve simplificada)
   def generate_curve_points(lat1, lon1, lat2, lon2, curvature=0.1, num_points=2):
       lats = np.linspace(lat1, lat2, num_points)
       lons = np.linspace(lon1, lon2, num_points)
       # Adicionando uma leve curvatura, alterando a longitude e latitude no meio
       middle_idx = num_points // 2
       lons[middle_idx] += curvature * (lon2 - lon1)
       lats[middle_idx] += curvature * (lat2 - lat1)
       return lats, lons
   # Criando o mapa de dispersão com os totais de candidatos por cidade de origem
   fig = px.scatter_mapbox(df_filtered_g, lat="Cidade_Lat", lon="Cidade_Lon", hover_name="Cidade_UF", 
                           hover_data=["Total"], color="Total", size="Total", 
                           color_continuous_scale=px.colors.cyclical.HSV,
                           size_max=40, zoom=6, title="Distribuição de Inscrições por Cidade")
   # Adicionando setas que indicam a conexão entre a cidade de origem e o campus com curvas
   for i, row in df_filtered_g.iterrows():
       if row["Total"] >= filter:  # Verificação: só traçar as setas se Total for >= 4
           # Gerando pontos curvados entre a cidade e o campus
           curve_lat, curve_lon = generate_curve_points(row["Cidade_Lat"],
                                                       row["Cidade_Lon"], 
                                                       row["Campus_Lat"], 
                                                       row["Campus_Lon"], 
                                                       num_points=50)
           fig.add_trace(go.Scattermapbox(
               lon=curve_lon,
               lat=curve_lat,
               mode='lines',
               line=dict(width=row["Total"] * 0.05, color='blue'),  # Espessura proporcional ao valor de 'Total'
               # line=dict(width=.2, color='blue'),
               hoverinfo='text',
               hovertext=f'{row["Cidade_UF"]} → {row["Campus_UF"]} ({row["Total"]})',  # Informações no hover
               showlegend=False
           ))
   # Configuração do estilo do mapa
   # fig.update_layout(mapbox_style="open-street-map")
   fig.update_layout(mapbox_style="carto-positron") 
   fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, 
                     height=500, mapbox_center={"lat": -19.91018, "lon": -43.92657})

   fig.update_layout(showlegend=False)
       # Exibir gráfico
   col2.plotly_chart(fig, use_container_width=True)