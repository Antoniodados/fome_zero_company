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

st.set_page_config( page_title = "Cuisines", page_icon= "🍽️", layout= "wide" )

# ============================================================================================
# Funções
# ============================================================================================
def top_restaurantes (df):
    """ Esta função tem a responsabilidade de Criar um DataFrame
        com os melhores restaurantes com base nas avaliações

        Input: 
                > DataFrame
                > Tipo de culinária
        Output: DataFrame
    """
    df_aux = (df.loc[:, ['Restaurant ID', 'Restaurant Name', 'Name Country', 'City', 'cozinha', 'Average Cost for two', 'Aggregate rating', 'Votes']]
                .sort_values(['Aggregate rating', 'Restaurant ID'], ascending=[False, True])
                .head(quantidade_slider)
                .reset_index( drop=True))
    
    return df_aux
    
def melhor_cozinha (df, cozinha):
    """ Esta função tem a responsabilidade de Criar a métricas
        indica os melhores restaurantes com base nas avaliações

        Input: 
                > DataFrame
                > Tipo de culinária
        Output: DataFrame
    """
    df_aux= df.loc[df['cozinha'] == cozinha, :]
    df_aux01 = (df_aux.loc[:,['City','Name Country', 'Restaurant Name','Aggregate rating', 'Restaurant ID','Average Cost for two']]
                  .groupby(['City','Name Country', 'Restaurant ID', 'Restaurant Name'])
                  .mean() 
                  .sort_values(['Aggregate rating', 'Restaurant ID'], ascending=[False, True])
                  .reset_index())
      
    return df_aux01

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
st.markdown('# 🍽️ Visão Tipos de Cozinhas')
st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')

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

quantidade_slider = st.sidebar.slider(
    'Selecione a quantidade de Restaurantes que deseja visualizar',
    value=20,
    min_value=1,
    max_value=20)

st.sidebar.markdown("""---""")
cuisines_options = st.sidebar.multiselect(
    'Escolha os Tipos de Culinária',
   ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
       'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'],
    default =  ["Home-made", "BBQ", "Japanese",  "Brazilian",  "Arabian", "American", "Italian" ])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powerd by Comunidade DS')

#Filtro de Países
linhas_selecionadas = df['Name Country'].isin(country_options)
df = df.loc[linhas_selecionadas, :]

#Filtro de tipos culinário
linhas_selecionadas = df['cozinha'].isin(cuisines_options)
df = df.loc[linhas_selecionadas, :]


# ============================================================================================
# Layout no Streamlit
# ============================================================================================
with st.container():
                
    col1, col2, col3, col4, col5 = st.columns( 5 )

    with col1:
        df_aux01 = melhor_cozinha (df, 'Italian')
        avaliacao_italiana = df_aux01.iloc[0,4]
        avaliacao_cities = df_aux01.iloc[0,3]
        col1.metric(f'Italiana: {avaliacao_cities}', f'{avaliacao_italiana}/5.0', 
                    help = f"Pais: {df_aux01.iloc[0,1]} \n\n" 
                           f"Cidade: {df_aux01.iloc[0,0]}\n\n"
                           f"Média Prato para dois: $ {df_aux01.iloc[0,5]}")
                
    with col2:
        df_aux01 = melhor_cozinha (df, 'American')
        avaliacao_americana = df_aux01.iloc[0,4]
        avaliacao_cities = df_aux01.iloc[0,3]
        col2.metric(f'Americana: {avaliacao_cities}', f'{avaliacao_americana}/5.0',
                    help = f"Pais: {df_aux01.iloc[0,1]} \n\n" 
                           f"Cidade: {df_aux01.iloc[0,0]}\n\n"
                           f"Média Prato para dois: $ {df_aux01.iloc[0,5]}")

    with col3:
        df_aux01 = melhor_cozinha (df, 'Arabian')
        avaliacao_arabian = df_aux01.iloc[0,4]
        avaliacao_cities = df_aux01.iloc[0,3]
        col3.metric(f'Arábica: {avaliacao_cities}', f'{avaliacao_arabian}/5.0',
                    help = f"Pais: {df_aux01.iloc[0,1]} \n\n" 
                           f"Cidade: {df_aux01.iloc[0,0]}\n\n"
                           f"Média Prato para dois: $ {df_aux01.iloc[0,5]}")

    with col4:
        df_aux01 = melhor_cozinha (df, 'Japanese')
        avaliacao_japanese = df_aux01.iloc[0,4]
        avaliacao_cities = df_aux01.iloc[0,3]
        col4.metric(f'Japonesa: {avaliacao_cities}', f'{avaliacao_japanese}/5.0',
                    help = f"Pais: {df_aux01.iloc[0,1]}\n\n" 
                           f"Cidade: {df_aux01.iloc[0,0]}\n\n"
                           f"Média Prato para dois: $ {df_aux01.iloc[0,5]}")
        
    with col5:
        df_aux01 = melhor_cozinha (df, 'Brazilian')
        avaliacao_brasileira = df_aux01.iloc[0,4]
        avaliacao_cities = df_aux01.iloc[0,3]
        col5.metric(f'Brasileira: {avaliacao_cities}', f'{avaliacao_brasileira}/5.0',
                    help = f"Pais: {df_aux01.iloc[0,1]}\n\n" 
                           f"Cidade: {df_aux01.iloc[0,0]}\n\n"
                           f"Média Prato para dois: $ {df_aux01.iloc[0,5]}")

with st.container():
    st.markdown(f'# Top {quantidade_slider} Restaurantes')
    df_aux = top_restaurantes (df)
    st.dataframe(df_aux)