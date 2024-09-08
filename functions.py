import pandas as pd
import streamlit as st

@st.cache_data
def ler_coordenadas():
    dfmun_geo = pd.read_csv("./dados/latitude-longitude-cidades.csv", sep=";")#.groupby("NOME_MUNICIPIO").count().sort_values("NOME_MUNICIPIO", ascending=False).reset_index()
    dfmun_geo['Mun_UF'] = dfmun_geo['municipio'] +' - '+ dfmun_geo['uf']
    dfmun_geo = dfmun_geo.set_index('Mun_UF')
    
    return dfmun_geo


@st.cache_data
def ler_dados():
    df = pd.read_excel('./dados/processado.xlsx')   
    return df
