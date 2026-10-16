import streamlit as st
from PIL import Image
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Curry Company | Dashboard",
    page_icon="📊",
    layout="wide",
)

image = Image.open(APP_DIR / "logo.png")
st.sidebar.image( image, width=120 )


st.sidebar.markdown( "# Curry Company" )
st.sidebar.markdown( "## Fastest Delivery in Town" )
st.sidebar.markdown( """---""" )

st.write("# Curry Company — Growth Dashboard")

st.markdown(
    """
    Painel analítico desenvolvido para acompanhar indicadores operacionais de um
    marketplace de entregas. A navegação está organizada em três perspectivas:

    - **Visão Empresa:** volume de pedidos, evolução semanal, perfil de trânsito e distribuição geográfica.
    - **Visão Entregadores:** idade, avaliações, condições dos veículos e desempenho por cidade.
    - **Visão Restaurantes:** distâncias, tempos de entrega e impactos de trânsito, cidade e festivais.

    Use o menu lateral para escolher a visão e ajustar os filtros disponíveis.

    > Projeto demonstrativo de portfólio. Os dados são utilizados exclusivamente
    > para fins educacionais e não representam uma operação real.
""" )
