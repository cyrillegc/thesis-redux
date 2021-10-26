import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px
import pandas as pd
import datetime
import statistics
from sklearn import preprocessing
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(layout="wide")
mapbox_token = 'pk.eyJ1Ijoic29sbGlyeWMiLCJhIjoiY2t1bGl1aml1MW5lZDJxbXl2d2RvbWNwdiJ9.ugect2o_eFp-XGOgxaRpBg'
min_date = datetime.date(2010, 1, 1)
max_date = datetime.date(2020, 1, 1)
config = dict({'scrollZoom': True})


def filter_by_date(start_date, end_date, concerts_df, venues_top_genres_df):
    date_filter = concerts_df[
        (concerts_df['startDate'] > str(start_date)) & (concerts_df['startDate'] < str(end_date))].index
    data_filtered_df = venues_top_genres_df.loc[venues_top_genres_df['concert_id'].isin(date_filter)]

    return data_filtered_df


def show_scatter_map():
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
            options=sorted(data_full_df['top_genre'].unique()),
            default=sorted(data_full_df['top_genre'].unique())[0]
            # format_func=lambda x: venues_df.loc[x, 'locality'],
        )

    filtered_by_date_df = filter_by_date(start_date, end_date, concerts_df, data_full_df)
    hover_data = {'latitude': False, 'longitude': False}

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


def show_network_genres():
    if venue_selection:
        concerts_idx_in_venue = concerts_df.loc[concerts_df['venue_id'] == venue_selection].index
        artists_in_concerts = data_full_df[data_full_df['concert_id'].isin(concerts_idx_in_venue)]
        artists_in_concerts = artists_in_concerts.drop_duplicates(subset=['artist_id', 'spotify_genre', 'top_genre'])

        nodes = []
        edges = []

        top_genres = artists_in_concerts['top_genre'].unique()
        sub_genres = artists_in_concerts['spotify_genre'].unique()
        artists = artists_in_concerts['artist_id'].unique()

        for top_genre in top_genres:
            nodes.append(Node(id=top_genre, label=top_genre, size=400, color='orange'))

        for artist in artists:
            nodes.append(Node(id=artist, size=100, renderLabel=False))

        for idx, row in artists_in_concerts.iterrows():
            top_genre = row['top_genre']
            artist = row['artist_id']
            edges.append(Edge(source=artist, target=top_genre, color='lightblue'))

        config = Config(
            width=500,
            height=500,
            directed=True,
            nodeHighlightBehavior=True,
            highlightColor="blue",  # or "blue"
            collapsible=True,
            node={'labelProperty': 'label'},
            link={'labelProperty': 'label', 'renderLabel': True},
            # **kwargs e.g. node_size=1000 or node_color="blue"
        )

        agraph(
            nodes=nodes,
            edges=edges,
            config=config,
        )


def show_bar_chart_genres():
    sort_bar_chart = st.checkbox(
        'Sort bar chart'
    )

    if venue_selection:
        venue_stats = stats_df.loc[venue_selection].drop(['nbr_concerts'])
        if sort_bar_chart:
            venue_stats = venue_stats.sort_values(ascending=False)

        fig_histo = px.bar(
            venue_stats
        )
        st.plotly_chart(fig_histo)


def show_distribution_artists():
    preprocess_selection = st.radio('Preprocess data', ['Standardize', 'Normalize', 'None'])

    artists_matched_df = artists_df.loc[pd.notna(artists_df['spotify_id'])]
    artists_matched_df = artists_matched_df[['spotify_popularity', 'spotify_followers', 'spotify_listeners']]
    stats_array = artists_matched_df.values

    if preprocess_selection == 'Standardize':
        standardizer = preprocessing.StandardScaler()
        preprocessed_data = standardizer.fit_transform(stats_array.T)
    elif preprocess_selection == 'Normalize':
        normalizer = preprocessing.Normalizer()
        preprocessed_data = normalizer.fit_transform(stats_array.T)
    else:
        preprocessed_data = stats_array.T

    dist_data = [x for x in preprocessed_data]
    dist_labels = [label for label in artists_matched_df.columns]

    # Create distplot with curve_type set to 'normal'
    fig = ff.create_distplot(
        dist_data,
        dist_labels,
        curve_type='normal',  # override default 'kde'
        show_hist=False,
        show_rug=False,
    )

    st.plotly_chart(fig)


@st.cache
def open_data():
    with open('data/songkick/data_songkick_venues.csv', encoding='utf-8') as file_venues:
        venues_df = pd.read_csv(file_venues, index_col=0)
        #venues_df = venues_df.dropna(subset=['latitude'])
        venues_df = venues_df.sort_values(by=['venue'])

    with open('data/spotify/data_spotify_artists_light.csv', encoding='utf-8') as file_artists:
        artists_df = pd.read_csv(file_artists, index_col=0)

    with open('data/songkick/data_songkick_concerts_light.csv', encoding='utf-8') as file_concerts:
        concerts_df = pd.read_csv(file_concerts, index_col=0)

    with open('data/spotify/data_spotify_top_genres_v3.csv', encoding='utf-8') as file_genres:
        genres_df = pd.read_csv(file_genres, index_col=0)

    with open('data/data_singled_venues_top_genres.csv', encoding='utf-8') as file_concat:
        data_full_df = pd.read_csv(file_concat, index_col=0)

    with open('data/data_stats_venues_genres.csv', encoding='utf-8') as file_stats:
        stats_df = pd.read_csv(file_stats, index_col=0)

    data_full_df = filter_by_date(min_date, max_date, concerts_df, data_full_df)

    stats_df = stats_df.merge(venues_df['venue'], left_index=True, right_index=True).sort_values(by=['venue'])
    stats_df = stats_df.drop(columns=['venue'])

    data_dict = {
        'venues_df': venues_df,
        'artists_df': artists_df,
        'concerts_df': concerts_df,
        'data_full_df': data_full_df,
        'stats_df': stats_df,
        'genres_df': genres_df,
    }

    return data_dict


data_dict = open_data()
venues_df = data_dict['venues_df']
concerts_df = data_dict['concerts_df']
artists_df = data_dict['artists_df']
genres_df = data_dict['genres_df']
data_full_df = data_dict['data_full_df']
stats_df = data_dict['stats_df']

st.subheader('Date range')
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

show_scatter_map()

st.subheader('Genres in venues')

venue_selection = st.selectbox(
    'Select a venue',
    options=stats_df.index,
    format_func=lambda x: venues_df.loc[x, 'venue'],
    index=stats_df.index.get_loc(stats_df.loc['/venues/418386'].name),  # set default selection to Caves du Manoir
)

col1, col2, = st.columns(2)

with col1:
    st.write('Genres of artists who have played in the venue:')
    show_network_genres()

with col2:
    st.write('Genres frequency in the venue:')
    show_bar_chart_genres()

st.subheader('Artists popularity')
show_distribution_artists()

st.subheader('Venues popularity')

artists_in_concerts = data_full_df.drop_duplicates(subset=['concert_id', 'artist_id']).sort_values(by=['venue_id'])
concerts_stats = artists_in_concerts.merge(artists_df[['spotify_listeners', 'spotify_followers']], left_on='artist_id', right_index=True)

venues_mean_median_df = pd.DataFrame(concerts_stats.groupby('venue_id').size())
venues_mean_median_df = venues_mean_median_df.rename(columns={0: 'nbr_artists'})
venues_mean_median_df = venues_mean_median_df.join(pd.DataFrame(concerts_stats.groupby('venue_id').mean()))
venues_mean_median_df = venues_mean_median_df.rename(columns={'spotify_listeners': 'listeners_mean', 'spotify_followers': 'followers_mean'})
venues_mean_median_df = venues_mean_median_df.join(pd.DataFrame(concerts_stats.groupby('venue_id').median()))
venues_mean_median_df = venues_mean_median_df.rename(columns={'spotify_listeners': 'listeners_median', 'spotify_followers': 'followers_median'})
venues_mean_median_df = venues_mean_median_df.merge(venues_df['venue'], left_index=True, right_index=True)

col1, col2 = st.columns(2)

with col1:
    max_artists = int(venues_mean_median_df['nbr_artists'].max())
    min_nbr_artists = st.slider(
        'Min number of artists',
        1, max_artists,
        (1, max_artists),
    )

with col2:
    min_followers = int(venues_mean_median_df['followers_median'].min())
    max_followers = int(venues_mean_median_df['followers_median'].max())

    range_followers = st.slider(
        'Select min and max nbr of followers median',
        min_followers, max_followers,
        (min_followers, max_followers),
        step=10000,
    )

    venues_mean_median_df = venues_mean_median_df.loc[
        (venues_mean_median_df['nbr_artists'] > min_nbr_artists[0]) &
        (venues_mean_median_df['nbr_artists'] < min_nbr_artists[1])
    ]
    venues_mean_median_df = venues_mean_median_df.loc[
        (venues_mean_median_df['followers_median'] > range_followers[0]) &
        (venues_mean_median_df['followers_median'] < range_followers[1])
    ]

with col1:
    # Create distplot with curve_type set to 'normal'
    fig = px.scatter(
        venues_mean_median_df,
        x='listeners_median',
        y='followers_median',
        trendline='ols',
        hover_data=['venue'],
    )

    fig.update_layout(
        dragmode='pan'
    )

    st.plotly_chart(fig, config=config)

with col2:
    # Create distplot with curve_type set to 'normal'
    fig = px.scatter(
        venues_mean_median_df,
        x='nbr_artists',
        y='followers_median',
        trendline='ols',
        hover_data=['venue'],
    )

    fig.update_layout(
        dragmode='pan'
    )

    st.plotly_chart(fig, config=config)
