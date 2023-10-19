# ============================================================================================
#Librares(Bibliotecas necessárias)
# ============================================================================================
import pandas as pd
import folium
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title = "Countries", page_icon= "🌍", layout= "wide" )

# ============================================================================================
# Funções
# ============================================================================================
def graph_bar_replace (df):
    """ Esta função tem a responsabilidade de Criar um gráfico de barra
    Agrupa pela métrica mean e troca ponto por vírgula

    Input: 
            > DataFrame
    Output: gráfico de barras
    """
    df_aux = (df.loc[:, ['Name Country', 'Average Cost for two']]
                .groupby(['Name Country'])
                .mean()
                .sort_values('Average Cost for two', ascending=False)
                .reset_index())
    df_aux = round(df_aux,2)
    df_aux['Average Cost for two'] = df_aux['Average Cost for two'].replace(",",".")
    df_aux.columns = ['País', 'Preço do prato para 2 pessoas']
    fig= px.bar(df_aux, x='País', y='Preço do prato para 2 pessoas', text = 'Preço do prato para 2 pessoas')
    fig.update_layout(title = 'Méda de Preço de um prato para duas pessoa por País',
                          title_x = 0.3,
                          xaxis_title = 'Países',
                          yaxis_title = 'Preço de ´rato para duas Pessoas')
    return fig

def graph_bar_mean (df, columns, title, xaxis, yaxis):
    """ Esta função tem a responsabilidade de Criar um gráfico de barra
        Agrupa pela métrica mean

        Input: 
            > DataFrame
            > Coluna para Eixo Y
            > Título para o Gráfico
            > Título eixo X
            > Título eixo Y
        Output: gráfico de barras
    """
    df_aux = (df.loc[:, ['Name Country', columns]]
                .groupby(['Name Country'])
                .mean()
                .sort_values(columns, ascending=False)
                .reset_index())
    df_aux = round(df_aux,2)
    df_aux.columns = ['País', 'Quantidade de Restaurantes']
    fig= px.bar(df_aux, x='País', y='Quantidade de Restaurantes', text = 'Quantidade de Restaurantes')
    fig.update_layout(title = title,
                      title_x = 0.5,
                      xaxis_title = xaxis,
                      yaxis_title = yaxis)
    return fig

def graph_bar_nunique (df, columns, title, xaxis, yaxis):
    """ Esta função tem a responsabilidade de Criar um gráfico de barra
        Agrupa pela métrica nunique

        Input: 
            > DataFrame
            > Coluna para Eixo Y
            > Título para o Gráfico
            > Título eixo X
            > Título eixo Y
        Output: gráfico de barras
    """
    df_aux = (df.loc[:, ['Name Country', columns]]
                .groupby(['Name Country'])
                .nunique()
                .sort_values(columns, ascending=False)
                .reset_index())
    df_aux.columns = ['País', 'Quantidade de Restaurantes']
    fig= px.bar(df_aux, x='País', y='Quantidade de Restaurantes', text = 'Quantidade de Restaurantes')
    fig.update_layout(title = title,
                      title_x = 0.5,
                      xaxis_title = xaxis,
                      yaxis_title = yaxis)
    return fig

def country_name (df):
    """ Esta função tem a responsabilidade de Criar a Coluna com nome dos países
        
        Aloca para cada código um nome de país
        
        Input: DataFrame 
        Output: DataFrame
    """
    paises = {'Country Code': [1, 14, 30, 37, 94, 148, 162, 166, 184, 189, 191, 208, 214, 215, 216],
          'Name Country': ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland", 
                           "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka", 
                           "Turkey", "United Arab Emirates", "England", "United States of America"]}

    paises = pd.DataFrame(paises)
    df = df.merge(paises, on='Country Code', how='inner')
    return df


def clean_code( df ):
    """ Esta função tem a responsabilidade de limpar o dataframe
        
        Tipos de limpeza:
        1. Dexar apenas um tipo de culinária na coluna Cuisines
        2. Excluir as colunas sem informações
        3. Excluir as linhas com células vazas
        4. Excluir linhas duplicadas
                
        Input: DataFrame
        Output: DataFrame
    """
    df[['cozinha','1', '2', '3', '4', '5', '6', '7']] = df['Cuisines'].str.split(',', expand=True)
    df = df.drop(['Switch to order menu', '1', '2', '3', '4', '5', '6', '7'], axis='columns')
    df = df.dropna(how="any", axis=0)
    df = df.drop_duplicates( ignore_index=True)
    return df
    
#--------------------------------------- Inicio da Estrutura lógica do código ------------------------------------------------------------

# ============================================================================================
#Import Dataset
# ============================================================================================
dataframe = pd.read_csv('zomato.csv')

# ============================================================================================
# Limpando os dados
# ============================================================================================
df = clean_code( dataframe )

# ============================================================================================
# Incluir Colunas (Name Country)
# ============================================================================================
df = country_name (df)

# ============================================================================================
# Barra lateral
# ============================================================================================
st.markdown('# 🌍 Visão Países')

image_path='logo.png'
Image = Image.open(image_path)
st.sidebar.image(Image, width=100)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Filtros')
country_options = st.sidebar.multiselect(
    'Escolha os Paise que deseja vsualizar os Restaurantes',
    ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland", 
     "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka", 
     "Turkey", "United Arab Emirates", "England", "United States of America"],
    default =  ["Australia", "Brazil", "Canada",  "Qatar",  "South Africa", "England", ])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powerd by Comunidade DS')

#Filtro de Países
linhas_selecionadas = df['Name Country'].isin(country_options)
df = df.loc[linhas_selecionadas, :]

# ============================================================================================
# Layout no Streamlit
# ============================================================================================

with st.container():
    fig = graph_bar_nunique (df, 'Restaurant ID', 'Quantidade de Restaurantes Registradas por País', 'Países', 'Quantidade de Restaurantes')
    st.plotly_chart( fig, use_container_width=True )
        
with st.container():
    fig = graph_bar_nunique (df, 'City', 'Quantidade de Cidades Registradas por País', 'Países', 'Quantidade de Cidades')
    st.plotly_chart( fig, use_container_width=True )
    
with st.container():
    
    col1, col2 = st.columns( 2 )
    
    with col1:
        fig = graph_bar_mean (df, 'Votes', 'Média de Avaliações por País', 'Países', 'Quantidade de Avaliações' )
        st.plotly_chart( fig, use_container_width=True )
        
    with col2:
        fig = graph_bar_replace (df)
        st.plotly_chart( fig, use_container_width=True )
