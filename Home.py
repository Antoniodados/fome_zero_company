import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Home",
    page_icon = "♨️"
)

image_path='logo.png'
Image = Image.open(image_path)
st.sidebar.image(Image, width=120)

st.sidebar.markdown('# Fome Zero ')
st.sidebar.markdown('## Top Restaurants end Culinary Types')
st.sidebar.markdown("""---""")

st.write( "# Fome Zero Tops Dashboard" )

st.markdown(
    """
    Tops Dashboard foi construído para acmpanhar as métricas dos Top Restaurantes e Top tipos culinário.
    ### Como utilizar esse Tops Dashboard?
    - Main Page:
        - Métricas gerais de capacidade e crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Countres:
        - Acompanhamento dos indicadores capacidade e crescimento por país.
    - Cities:
        - Acompanhamento dos indicadores capacidade e crescimento por cidade.
    - Cuisines:
        - Acompanhamento dos indicadores dos melhores restaurantes por tipos de culinária.
    ### Ask for Help
    - Time de Data Sciense no email
        - antonio.ds@outlook.com.br
    
    """)
