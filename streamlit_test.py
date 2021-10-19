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

    with open('data/data_stats_venues_genres.csv', encoding='utf-8') as file_stats:
        stats_df = pd.read_csv(file_stats, index_col=0)

    return venues_df, artists_df, concerts_df, venues_top_genres_df, stats_df


venues_df, artists_df, concerts_df, venues_top_genres_df, stats_df = open_data()

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

    artist_genre_selection = st.radio(
        'Show artists or genres',
        options=['Genres', 'Artists'],
    )

with col2:
    end_date = st.date_input(
        'End date range',
        value=max_date,
        min_value=min_date,
        max_value=max_date,
    )

    concert_venue_selection = st.radio(
        'Display venues or concerts',
        options=['Venues', 'Concerts'],
    )

if artist_genre_selection == 'Artists':
    artist_selection = st.multiselect(
        'Select artist',
        options=artists_df.index,
        default=artists_df.iloc[0].name,
        format_func=lambda x: artists_df.loc[x, 'artist_name'],
    )
else:
    genres_selection = st.multiselect(
        'Select genres',
        options=sorted(venues_top_genres_df['top_genre'].unique()),
        default=sorted(venues_top_genres_df['top_genre'].unique())[0]
        # format_func=lambda x: venues_df.loc[x, 'locality'],
    )

date_filter = concerts_df[(concerts_df['startDate'] > str(start_date)) & (concerts_df['startDate'] < str(end_date))].index
filtered_by_date_df = venues_top_genres_df.loc[venues_top_genres_df['concert_id'].isin(date_filter)]

if artist_genre_selection == 'Artists':
    data_selection = artist_selection
    column_name = 'artist_id'
else:
    data_selection = genres_selection
    column_name = 'top_genre'

if concert_venue_selection == 'Venues':
    results_df = venues_df.loc[
        filtered_by_date_df.loc[
            filtered_by_date_df[column_name].isin(data_selection)
        ]['venue_id'].unique()
    ]
    marker_size = None
else:
    results_df = venues_df.loc[
        concerts_df.loc[
            filtered_by_date_df.loc[
                filtered_by_date_df[column_name].isin(data_selection)
            ]['concert_id'].unique()
        ]['venue_id']
    ]

    results_df['venue_ratio'] = 0
    venue_count = results_df.groupby('venue')['venue_ratio'].transform("count")
    sum_venue_count = venue_count.sum()
    results_df['venue_ratio'] = venue_count / sum_venue_count
    marker_size = results_df['venue_ratio']

if not results_df.empty:
    fig_scatter = px.scatter_mapbox(
        results_df,
        lat='latitude', lon='longitude',
        hover_name='venue', hover_data=hover_data,
        color_discrete_sequence=['red'],
        opacity=1,
        zoom=6,
        center={'lat': 46.801111, 'lon': 8.226667},
        size=marker_size,
        color=None,
        size_max=15,
    )

    fig_scatter.update_layout(
        mapbox_style='basic',
        mapbox_accesstoken=mapbox_token,
        hoverlabel={
            'bgcolor': 'white',
            'font_size': 12,
        }
    )

    st.plotly_chart(fig_scatter)

venue_selection = st.selectbox(
    'Show genres stats about a venue',
    options=stats_df.index,
    format_func=lambda x: venues_df.loc[x, 'venue']
)

sort_bar_chart = st.checkbox(
    'Sort bar chart'
)

if venue_selection:
    venue_stats = stats_df.loc[venue_selection].drop('nbr_concerts')
    if sort_bar_chart:
        venue_stats = venue_stats.sort_values(ascending=False)

    fig_histo = px.bar(
        venue_stats
    )
    st.plotly_chart(fig_histo)
