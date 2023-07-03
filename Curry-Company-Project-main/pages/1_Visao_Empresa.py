import streamlit as st
import plotly.express as px

import pandas as pd
import numpy as np
import folium

import matplotlib.pyplot as plt

from PIL import Image
from streamlit_folium import folium_static
from datetime import datetime

st.set_page_config( page_title="Visao Empresa", page_icon="📈", layout='wide' )

# ===========================
# Function
# ===========================
def clean_code( df ):
    # removing NA
    df = df.loc[(df['Delivery_person_Age'] != 'NaN '), :]
    df = df.loc[(df['City'] != 'NaN '), :]
    df = df.loc[(df['Road_traffic_density'] != 'NaN '), :]
    df = df.loc[(df['Festival'] != 'NaN '), :]
    df = df.loc[(df['multiple_deliveries'] != 'NaN '), :].copy()

    # converting data type
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype( float )
    df['Delivery_person_Age']     = df['Delivery_person_Age'].astype( int )
    df['Order_Date']              = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )
    df['multiple_deliveries']     = df['multiple_deliveries'].astype( int )

    # removing espacos
    df.loc[:, 'ID'] = df.loc[:, 'ID'].str.strip()
    df.loc[:, 'Road_traffic_density'] = df.loc[:, 'Road_traffic_density'].str.strip()
    df.loc[:, 'Type_of_order'] = df.loc[:, 'Type_of_order'].str.strip()
    df.loc[:, 'Type_of_vehicle'] = df.loc[:, 'Type_of_vehicle'].str.strip()
    df.loc[:, 'City'] = df.loc[:, 'City'].str.strip()
    df.loc[:, 'Festival'] = df.loc[:, 'Festival'].str.strip()

    # cleaning coluna time taken
    df['Time_taken(min)'] = df['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
    df['Time_taken(min)'] = df['Time_taken(min)'].astype( int )

    df['week_of_year'] = df['Order_Date'].dt.strftime( "%U" )

    return df


def order_metric( df, period='day' ):
    if period == 'day':
        st.header( 'Orders by Day' )
        df_aux = df.loc[:, ['ID', 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()
        df_aux.columns = ['order_date', 'qtde_entregas']

        # gráfico
        fig = px.bar( df_aux, x='order_date', y='qtde_entregas',
                     labels={'order_date': 'data do pedido', 'qtde_entregas': 'quantidade de entregas'}
                     )
        st.plotly_chart( fig, use_container_width=True )

    else:
        st.header( 'Orders by Week' )
        df_aux = df.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()

        # gráfico
        fig = px.bar( df_aux, x='week_of_year', y='ID',
                     labels={'week_of_year': 'Semana do Ano', 'ID': 'Quantidade de Entregas'} )
        st.plotly_chart( fig, use_container_width=True )


def order_by_deliver( df ):
    st.header( 'Week order share' )
    df_aux1 = df.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df_aux2 = df.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' )

    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    # gráfico
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
    st.plotly_chart( fig, use_container_width=True )


def order_share_by_traffic( df ):
    st.header( 'Traffic Order Share' )
    df_aux = df.loc[:, ['ID', 'Road_traffic_density']].groupby( 'Road_traffic_density' ).count().reset_index()
    df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )

    # gráfico
    fig = px.pie( df_aux, values='perc_ID', names='Road_traffic_density' )
    st.plotly_chart( fig, user_container_width=True )


def order_by_city_vehicle( df ):
    st.header( 'Type of Vehicle by City' )
    df_aux = df[['ID', 'Type_of_vehicle', 'City', ]].groupby( ['City', 'Type_of_vehicle'] ).count().reset_index()

    # grafico
    fig = px.scatter( df_aux, x='City', y='Type_of_vehicle', size='ID', color='City' )
    st.plotly_chart( fig, user_container_width=True )


def density_traffic_map( df ):
    df_aux = df.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby( ['City', 'Road_traffic_density'] ).median().reset_index()

    # Desenhar o mapa
    map_ = folium.Map( zoom_start=11 )

    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                       location_info['Delivery_location_longitude']],
                       popup=location_info[['City', 'Road_traffic_density']] ).add_to( map_ )

    folium_static( map_, width=1024 , height=600 )


# ===========================
# Título
# ===========================
st.header("Marketplace - Visão Empresa")   ## Main Title

# ===========================
# Filtros - Side bar
# ===========================
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( "# Curry Company" )
st.sidebar.markdown( "## Fastest Delivery in Town" )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( "## Selecione um data limite" )
date_slider = st.sidebar.slider(
        "Até qual valor?",
        value=pd.datetime( 2022, 4, 13 ),
        min_value=pd.datetime( 2022, 2, 11),
        max_value=pd.datetime( 2022, 5, 6 ), 
        format="DD-MM-YYYY"
    )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( "## Selecione uma condição de trânsito" )
traffic_options = st.sidebar.multiselect(
        'Quais a condições do trânsito?',
        ['Low', 'Medium', 'High', 'Jam'], default='Medium' )

# ===========================
# ETL
# ===========================
# Extracao
file_path = 'dataset/'
df = pd.read_csv( file_path + 'train.csv' )

# Limpeza
df = clean_code( df )

# Tranformação
df = df.loc[df['Order_Date'] <= date_slider, :]
df = df.loc[df['Road_traffic_density'].isin( traffic_options ), :]

# ===========================
# Layout
# ===========================
# Tabs
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

with tab1:
    with st.container():
        order_metric( df, period='day' )

    with st.container():
        col3, col4 = st.columns(2)

        with col3:
            order_share_by_traffic( df )
        with col4:
            order_by_city_vehicle( df )

with tab2:
    with st.container():
        order_metric( df, period='week' )

    with st.container():
        order_by_deliver( df )

with tab3:
    with st.container():
        density_traffic_map( df )
