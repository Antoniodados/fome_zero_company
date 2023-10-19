# ============================================================================================
#Librares(Bibliotecas necessárias)
# ============================================================================================
import pandas as pd
import folium
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title = "Main Page", page_icon= "📊", layout= "wide" )

# ============================================================================================
# Funções
# ============================================================================================
def criar_map (df):
    """ Esta função tem a responsabilidade de Criar um mapa com os restaurantes 
        E suas principais informações
                
        Input: DataFrame 
        Output: Mapa
    """
    df.columns = ['Restaurant ID', 'Restaurante:', 'Country Code', 'City', 'Address',
              'Locality', 'Locality Verbose', 'Longitude', 'Latitude', 'Cuisines',
              'Preço para 2:', 'Currency', 'Has Table booking',
              'Has Online delivery', 'Is delivering now', 'Price range',
              'Avaliação:', 'Rating color', 'Rating text', 'Votes', 'Tipo:',
              'Name Country']
    map = folium.Map(location = [df['Latitude'].mean(), df['Longitude'].mean()]) #efault_zoom_start )
    marcacao = MarkerCluster() .add_to(map)
    icon = folium.Icon(html='<i class="fa fa-home fa-2x"></i>')
    for index, location_info in df.iterrows():
        folium.Marker( [location_info['Latitude'],
                        location_info['Longitude']],
                        icon=folium.Icon(icon='cutlery'),
                        #popup=location_info[['Restaurante:','Preço para 2:', 'Tipo:', 'Avaliação:']]).add_to(marcacao)
                        popup=f"<b>{location_info['Restaurante:']}</b><br><br>"
                            f"Preço: ${round(location_info['Preço para 2:'], 2)}\n"
                            f"Avaliação:{location_info['Avaliação:']}/5.0\n"
                            f"Tipo:{location_info['Tipo:']}" ).add_to(marcacao)  

    map.fit_bounds([df.loc[:,['Latitude','Longitude']].min().values.tolist(), df.loc[:,['Latitude','Longitude']].max().values.tolist() ])
    
    return map

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
st.markdown('# Fome Zero!')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('## Temos as seguintes marcas dentro da nossa plataforma:')

image_path='logo.png'
Image = Image.open(image_path)
st.sidebar.image(Image, width=100)

st.sidebar.markdown('# Fome Zero ')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Filtros')
country_options = st.sidebar.multiselect(
    'Escolha os Paise que deseja vsualizar os Restaurantes',
    ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland", 
     "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka", 
     "Turkey", "United Arab Emirates", "England", "United States of America"],
    default =  ["Australia", "Brazil", "Canada",  "Qatar",  "South Africa", "England", ])

st.sidebar.markdown("""---""")

st.sidebar.markdown('## Dados Tratados')
st.sidebar.button('Download', df.to_excel('dados_tratados.xlsx'))


st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powerd by Comunidade DS')

#Filtro de Países
linhas_selecionadas = df['Name Country'].isin(country_options)
df = df.loc[linhas_selecionadas, :]

# ============================================================================================
# Layout no Streamlit
# ============================================================================================

with st.container():
                
    col1, col2, col3, col4, col5 = st.columns( 5 )

    with col1:
        restaurantes_unicos = (df['Restaurant ID'].nunique())  
        restaurantes_unicos = f'{restaurantes_unicos:,.0f}'
        restaurantes_unicos = restaurantes_unicos.replace(",",".")
        col1.metric('Restaurantes Cadastrados', restaurantes_unicos)

    with col2:
        paises_unicos = df['Country Code'].nunique()
        col2.metric('Países Cadastrados', paises_unicos)

    with col3:
        city_unicas = df['City'].nunique()
        col3.metric('Cidade Cadastradas', city_unicas)

    with col4:
        total_avaliacoes = df['Votes'].sum()
        total_avaliacoes = f'{total_avaliacoes:,.0f}'
        total_avaliacoes = total_avaliacoes.replace(",",".")
        col4.metric('Avaliações Feitas na Plataforma', total_avaliacoes)

    with col5:
        culinaria_unicas = df['cozinha'].nunique()
        col5.metric('Tipos de Culinárias Oferecidas',culinaria_unicas)

with st.container():
    map = criar_map (df)
    folium_static( map, width=1024, height=600 )
