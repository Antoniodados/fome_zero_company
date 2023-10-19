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

st.set_page_config( page_title = "Cities", page_icon= "🌃", layout= "wide" )

# ============================================================================================
# Funções
# ============================================================================================
def graph_bar_top_7 (df, title):
    """ Esta função tem a responsabilidade de Criar um gráfico de barra
        com as 7 cidades com => 4 e <= 2.5

        Input: 
            > DataFrame
            > op = >=4 ou <=2.5
            > Coluna para ordenar = str e list
            > ascending - str e list
            > Renomeia os nomes das colunas = str e list
            > Coloca o nome da variável Y e text
            > Título para o Gráfico
            > Título eixo X
            > Título eixo Y
        Output: gráfico de barras
    """
    df_aux02 = (df_aux01.loc[:, ['City', 'Restaurant ID','Name Country']]
                        .groupby(['City','Name Country'])
                        .nunique()
                        .sort_values('Restaurant ID', ascending=False)
                        .head(7)
                        .reset_index())
    df_aux02.columns = ['Cidade','País', 'Quantidade de Restaurante']
    fig= px.bar(df_aux02, x='Cidade', y='Quantidade de Restaurante', color = 'País', text = 'Quantidade de Restaurante')
    fig.update_layout(title = title,
                  title_x = 0.1,
                  xaxis_title = 'Cidades',
                  yaxis_title = 'Quantidade de Restaurantes')
    return fig

def graph_bar_top_cidades (df,columns, ordem,ascending, rename_col,var_y, title, xaxis, yaxis ):
    """ Esta função tem a responsabilidade de Criar um gráfico de barra
        Com as 10 principais cdade com mais restaurantes ou culunária distinta

        Input: 
            > DataFrame
            > Coluna para filtro = str e list
            > Coluna para ordenar = str e list
            > ascending - str e list
            > Renomeia os nomes das colunas = str e list
            > Coloca o nome da variável Y e text
            > Título para o Gráfico
            > Título eixo X
            > Título eixo Y
        Output: gráfico de barras
    """
    df_aux = (df.loc[:, columns]
                .groupby(['City','Name Country'])
                .nunique()
                .sort_values(ordem, ascending=ascending)
                .head(10)  
                .reset_index())
    df_aux.columns = rename_col
    fig= px.bar(df_aux, x='Cidade', y=var_y, color = 'País', text = var_y)
    fig.update_layout(title = title,
                      title_x = 0.3,
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
st.markdown('# 🌃 Visão Cidades')

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
    fig = graph_bar_top_cidades (df,['City', 'Restaurant ID', 'Name Country'], ['Restaurant ID', 'Restaurant ID'], 
                                     [False, True],['Cidade','País', 'Quantidade de Restaurante'],'Quantidade de Restaurante',
                                     'Top 10 Cidades com mais Restaurantes na Base de Dados', 'Cidades', 'Quantidade de Restaurantes' )
    st.plotly_chart( fig, use_container_width=True )

with st.container():
    col1, col2 = st.columns( 2 )
    
    with col1:
        df_aux01 = df.loc[df['Aggregate rating'] >= 4,:]
        fig = graph_bar_top_7 (df, 'Top 7 Cidades com Restaurantes com média de avaliação acima de 4')
        st.plotly_chart( fig, use_container_width=True )
    with col2:
        df_aux01 = df.loc[df['Aggregate rating'] <= 2.5,:]
        fig = graph_bar_top_7 (df, 'Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5')
        st.plotly_chart( fig, use_container_width=True )
        
with st.container():
    fig = graph_bar_top_cidades (df,['City', 'cozinha', 'Restaurant ID', 'Name Country'], ['cozinha', 'Restaurant ID'],[False, False], 
                             ['Cidade', 'País', 'Quantidade de Tipos de Culinárias Únicas','Quantidade Restaurante'],'Quantidade de Tipos de Culinárias Únicas',
                             'Top 10 Cidades com mais Restaurantes com tpos de culinárias distintas', 'Cidades', 'Quantidade de Tipos de Culinárias Únicas' )
    st.plotly_chart( fig, use_container_width=True )
