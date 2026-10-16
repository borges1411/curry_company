import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np

from haversine import haversine
from PIL import Image
from datetime import datetime
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = APP_DIR / "dataset" / "train.csv"

st.set_page_config(page_title="Visão Restaurantes", page_icon="🍽️", layout="wide")

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


def get_avg_distance( df ):
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
    df['distance'] = df.loc[:, cols].apply( lambda x: haversine(  
                                         (x['Restaurant_latitude'], x['Restaurant_longitude'] ),
                                         (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1 )

    avg_distance = np.round( df['distance'].mean(), 2 )
    return avg_distance


def get_avg_time_by_city( df ):
    df_aux = df.loc[:, ['City', 'Time_taken(min)']].groupby( 'City' ).agg( {'Time_taken(min)': ['mean', 'std']} )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure() 
    fig.add_trace( go.Bar( name='Control',
                           x=df_aux['City'],
                           y=df_aux['avg_time'],
                           error_y=dict( type='data', array=df_aux['std_time'] ) ) ) 

    fig.update_layout(barmode='group') 
    fig.update_layout( margin=dict(l=40, r=40, t=40, b=40) )
    st.plotly_chart( fig, width="stretch" )



def get_distribution_distance( df ):
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
    df['distance'] = df.loc[:, cols].apply( lambda x:
                                haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                           (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1 )

    df_aux = df.loc[:, ['City', 'distance']].groupby( 'City' ).mean().reset_index()

    # pull is given as a fraction of the pie radius
    fig = go.Figure( data=[ go.Pie( labels=df_aux['City'], values=df_aux['distance'], pull=[0, 0.1, 0])])
    fig.update_layout( margin=dict(l=40, r=40, t=40, b=40) )
    st.plotly_chart( fig, width="stretch" )


def get_avg_time_by_order( df ):
    df_aux = ( df.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                 .groupby( ['City', 'Type_of_order'] )
                 .agg( {'Time_taken(min)': ['mean', 'std']} ) )

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    st.dataframe( df_aux )


def get_delivery_time_festival( df, festival=True ):
    df_aux = ( df.loc[:, ['Time_taken(min)', 'Festival']]
                 .groupby( 'Festival' )
                 .agg( {'Time_taken(min)': ['mean', 'std']} ) )

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    festival_value = 'Yes' if festival else 'No'
    result = df_aux.loc[df_aux['Festival'] == festival_value, ['avg_time', 'std_time']]

    if result.empty:
        return 0.0, 0.0

    avg_time = np.round(result['avg_time'].iloc[0], 2)
    std_time = np.round(result['std_time'].iloc[0], 2)

    return avg_time, std_time


def get_delivery_time_by_city( df ):
    df_aux = ( df.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                 .groupby( ['City', 'Road_traffic_density'] )
                 .agg( {'Time_taken(min)': ['mean', 'std']} ) )

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                      color='std_time', color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df_aux['std_time'] ) )

    fig.update_layout( margin=dict(l=40, r=40, t=40, b=40) )

    st.plotly_chart( fig, width="stretch" )

# ===========================
# Título
# ===========================
st.header("Marketplace - Visão Restaurantes")  ## Main Title

# ===========================
# Filtros - Side bar
# ===========================
image = Image.open(APP_DIR / "logo.png")
st.sidebar.image( image, width=120 )

st.sidebar.markdown( "# Curry Company" )
st.sidebar.markdown( "## Entrega rápida, decisões melhores" )

st.sidebar.markdown( """---""" )
st.sidebar.markdown( "## Selecione um data limite" )
date_slider = st.sidebar.slider(
        "Até qual valor?",
        value = datetime( 2022, 4, 6 ),
        min_value=datetime( 2022, 2, 11),
        max_value=datetime( 2022, 4, 6 ),
        format="DD-MM-YYYY"
    )


st.sidebar.markdown( """---""" )
st.sidebar.markdown( "## Selecione uma condição de trânsito" )
traffic_options = st.sidebar.multiselect(
        'Quais a condições do trânsito?', ['Low', 'Medium', 'High', 'Jam'], 
        default=['Low', 'Medium', 'High', 'Jam'] )


st.sidebar.markdown( """---""" )
st.sidebar.markdown( "## Selecione uma cidade" )
city_options = st.sidebar.multiselect(
        'Quais a cidade?', ['Metropolitian', 'Semi-Urban', 'Urban'], 
        default=['Urban', 'Semi-Urban', 'Metropolitian'] )
# ===========================
# ETL
# ===========================
# Extracao
df = pd.read_csv(DATA_FILE)

# Limpeza
df = clean_code( df )

# Tranformação
df = df.loc[df['Order_Date'] <= date_slider, :]
df = df.loc[df['Road_traffic_density'].isin( traffic_options ), :]
df = df.loc[df['City'].isin( city_options ), :]

# ===========================
# Layout
# ===========================
# Tabs
tab1 = st.tabs(['Visão Gerencial'])[0]


# Quantidade de entregadores únicos
delivery_unique = len( df.loc[:, 'Delivery_person_ID'].unique() )

with tab1:
    with st.container():
        st.title("Indicadores gerais")
        col1, col2, col3, col4, col5, col6 = st.columns( 6 )

        # Display Number - 
        col1.metric( "Entregadores únicos", delivery_unique )
        col2.metric( "Distância média (km)", get_avg_distance( df ) )

        avg_time, std_time = get_delivery_time_festival( df, festival=True )
        col3.metric( "Tempo médio com festival", avg_time  )
        col4.metric( "Desvio padrão com festival", std_time  )

        avg_time, std_time = get_delivery_time_festival( df, festival=False )
        col5.metric( "Tempo médio sem festival", avg_time  )
        col6.metric( "Desvio padrão sem festival", std_time  )


    with st.container():
        st.markdown("""---""")
        st.title( "Tempo médio de entrega por cidade" )
        get_avg_time_by_city( df )

    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns( 2 )

        with col1:
            st.subheader( "Distribuição da distância média por cidade" )
            get_distribution_distance( df )

        with col2:
            st.subheader( "Tempo médio por tipo de pedido" )
            get_avg_time_by_order( df )

    with st.container():
        st.markdown("""---""")
        st.subheader( "Tempo médio por cidade e trânsito" )
        get_delivery_time_by_city( df )
