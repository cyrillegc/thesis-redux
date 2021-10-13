import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px
import pandas as pd
import datetime


mapbox_token = 'pk.eyJ1Ijoic29sbGlyeWMiLCJhIjoiY2t1bGl1aml1MW5lZDJxbXl2d2RvbWNwdiJ9.ugect2o_eFp-XGOgxaRpBg'


@st.cache
def open_data():
    with open('data/data_songkick_venues.csv', encoding='utf-8') as file_venues:
        venues_df = pd.read_csv(file_venues, index_col=0)
        #venues_df = venues_df.dropna(subset=['latitude'])
        venues_df = venues_df.sort_values(by=['venue'])

    with open('data/data_spotify_artists_light.csv', encoding='utf-8') as file_artists:
        artists_df = pd.read_csv(file_artists, index_col=0)

    with open('data/data_songkick_concerts_light.csv', encoding='utf-8') as file_concerts:
        concerts_df = pd.read_csv(file_concerts, index_col=0)

    with open('data/data_singled_venues_top_genres.csv', encoding='utf-8') as file_concat:
        venues_top_genres_df = pd.read_csv(file_concat, index_col=0)

    return venues_df, artists_df, concerts_df, venues_top_genres_df


venues_df, artists_df, concerts_df, venues_top_genres_df = open_data()

hover_data = {'latitude': False, 'longitude': False}

min_date = datetime.date(2010, 1, 1)
max_date = datetime.date(2020, 1, 1)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        'Start date range',
        value=min_date,
        min_value=min_date,
        max_value=max_date,
    )

    artist_selection = st.multiselect(
        'Select artist',
        options=artists_df.index,
        default=artists_df.iloc[0].name,
        format_func=lambda x: artists_df.loc[x, 'artist_name'],
    )

with col2:
    end_date = st.date_input(
        'End date range',
        value=max_date,
        min_value=min_date,
        max_value=max_date,
    )

    genres_selection = st.multiselect(
        'Select genres',
        options=sorted(venues_top_genres_df['top_genre'].unique()),
        default=sorted(venues_top_genres_df['top_genre'].unique())[0]
        #format_func=lambda x: venues_df.loc[x, 'locality'],
    )

type_selection = st.radio(
    'Display venues by artists or genres',
    options=['Genres', 'Artists'],
)

date_filter = concerts_df[(concerts_df['startDate'] > str(start_date)) & (concerts_df['startDate'] < str(end_date))].index
filtered_by_date_df = venues_top_genres_df.loc[venues_top_genres_df['concert_id'].isin(date_filter)]

if type_selection == 'Artists':
    results_df = venues_df.loc[
        filtered_by_date_df.loc[
            filtered_by_date_df['artist_id'].isin(artist_selection)
        ]['venue_id'].unique()
    ]
else:
    results_df = venues_df.loc[
        filtered_by_date_df.loc[
            filtered_by_date_df['top_genre'].isin(genres_selection)
        ]['venue_id'].unique()
    ]

fig_scatter = px.scatter_mapbox(
    results_df,
    lat='latitude', lon='longitude',
    hover_name='venue', hover_data=hover_data,
    color_discrete_sequence=['red'],
    opacity=1,
)

fig_scatter.update_layout(
    mapbox_style='streets',
    mapbox_accesstoken=mapbox_token,
    hoverlabel={
        'bgcolor': 'white',
        'font_size': 12,
    }
)

fig_density = px.density_mapbox(
    venues_df,
    lat='latitude', lon='longitude',
    hover_name='venue',
    radius=10,
)

fig_density.update_layout(
    mapbox_style='streets',
    mapbox_accesstoken=mapbox_token,
    hoverlabel={
        'bgcolor': 'white',
        'font_size': 12,
    }
)

st.plotly_chart(fig_scatter)

st.write('Show info about artist')
st.write(artists_df.loc[artist_selection])
st.write('Show concerts by artist')
st.write(
    concerts_df.loc[
        venues_top_genres_df.loc[
            venues_top_genres_df['artist_id'].isin(artist_selection)
        ]['concert_id'].unique()
    ].sort_values(by=['startDate'])
)
