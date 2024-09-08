import pandas as pd
import streamlit as st
import os
from datetime import datetime
import pytz


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


def get_last_modified_file(): 

    # Obtém o tempo de modificação em segundos desde a época
    timestamp = os.path.getmtime("./dados/processado.xlsx")

    # Converte o timestamp para uma data legível
    data_modificacao = datetime.fromtimestamp(timestamp) 

    # Define o fuso horário para "America/Sao_Paulo"
    fuso_horario = pytz.timezone("America/Sao_Paulo")

    data_modificacao = data_modificacao.astimezone(fuso_horario)

    return data_modificacao.strftime("%d/%m/%Y %H:%M:%S")