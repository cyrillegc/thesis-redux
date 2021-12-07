import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
import statistics
from sklearn import preprocessing
#from streamlit_agraph import agraph, Node, Edge, Config
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")
mapbox_token = 'pk.eyJ1Ijoic29sbGlyeWMiLCJhIjoiY2t1bGl1aml1MW5lZDJxbXl2d2RvbWNwdiJ9.ugect2o_eFp-XGOgxaRpBg'
min_date = datetime.date(2010, 1, 1)
max_date = datetime.date(2020, 1, 1)
config = {
    'scrollZoom': True,
    'toImageButtonOptions': {
        'format': 'png',  # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': 720,
        'width': 1280,
    },
    'toImage': {
        'title': None,  # change snapshot icon label to "Download plot"
    }
}


def filter_by_date(start_date, end_date, concerts_df, venues_top_genres_df):
    date_filter = concerts_df[
        (concerts_df['date'] > str(start_date)) & (concerts_df['date'] < str(end_date))]['concert_id']
    data_filtered_df = venues_top_genres_df.loc[venues_top_genres_df['concert_id'].isin(date_filter)]

    return data_filtered_df


def show_network_genres():
    if len(venue_selection) == 1:
        concerts_idx_in_venue = concerts_df.loc[concerts_df['venue_id'] == venue_selection[0]].index
        artists_in_concerts = full_data_df[full_data_df['concert_id'].isin(concerts_idx_in_venue)]
        artists_in_concerts = artists_in_concerts.drop_duplicates(subset=['artist_id', 'spotify_genre', 'top_genre'])

        nodes = []
        edges = []

        top_genres = artists_in_concerts['top_genre'].unique()
        sub_genres = artists_in_concerts['spotify_genre'].unique()
        artists = artists_in_concerts['artist_id'].unique()

        for top_genre in top_genres:
            nodes.append(Node(id=top_genre, label=top_genre, size=400, color='orange'))

        for artist in artists:
            nodes.append(Node(id=artist, size=50, renderLabel=False))

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
    else:
        st.write('Select only one venue to see its genres network')


@st.cache
def open_data():
    with open('data/songkick/data_songkick_venues_light.csv', encoding='utf-8') as file:
        venues_df = pd.read_csv(file, index_col=1).drop(columns=['Unnamed: 0'])
        venues_df = venues_df.sort_values(by=['venue'])

    with open('data/spotify/data_spotify_artists_light.csv', encoding='utf-8') as file:
        artists_df = pd.read_csv(file, index_col=1).drop(columns=['Unnamed: 0'])

    with open('data/songkick/data_songkick_concerts_light.csv', encoding='utf-8') as file:
        concerts_df = pd.read_csv(file, index_col=0)

    with open('data/spotify/data_spotify_top_genres_final.csv', encoding='utf-8') as file:
        genres_df = pd.read_csv(file, index_col=0)

    with open('data/full_data.csv', encoding='utf-8') as file:
        full_data_df = pd.read_csv(file, index_col=0)

    with open('data/data_stats_venues_genres.csv', encoding='utf-8') as file:
        stats_venues_genres_df = pd.read_csv(file, index_col=0)

    with open('data/data_stats_venues_features.csv', encoding='utf-8') as file:
        stats_venues_features_df = pd.read_csv(file, index_col=0)

    with open('data/spotify/data_spotify_tracks.csv', encoding='utf-8') as file:
        tracks_df = pd.read_csv(file, index_col=0)

    stats_venues_genres_df = stats_venues_genres_df.merge(venues_df[['venue']], left_index=True, right_index=True).sort_values(by=['venue'])
    stats_venues_genres_df = stats_venues_genres_df.drop(columns=['venue'])

    data_dict = {
        'venues_df': venues_df,
        'artists_df': artists_df,
        'concerts_df': concerts_df,
        'full_data_df': full_data_df,
        'stats_venues_genres_df': stats_venues_genres_df,
        'stats_venues_features_df': stats_venues_features_df,
        'genres_df': genres_df,
        'tracks_df': tracks_df,
    }

    return data_dict


data_dict = open_data()

venues_df = data_dict['venues_df']
concerts_df = data_dict['concerts_df']
artists_df = data_dict['artists_df']
genres_df = data_dict['genres_df']
full_data_df = data_dict['full_data_df']
stats_venues_genres_df = data_dict['stats_venues_genres_df']
stats_venues_features_df = data_dict['stats_venues_features_df']
tracks_df = data_dict['tracks_df']

# Scatter map
with st.container():
    st.subheader('Geographical distribution of concerts and venues')

    # scatter map options
    with st.container():
        date_selection = st.slider(
            'Select start and end date',
            min_date, max_date,
            (min_date, max_date),
            format='DD-MM-YYYY',
        )

        col1, col2 = st.columns(2)
        with col1:
            artist_genre_selection = st.radio(
                'Show artists or genres',
                options=['Genres', 'Artists'],
            )

        with col2:
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
                options=sorted(full_data_df['top_genre'].dropna().unique()),
                default=sorted(full_data_df['top_genre'].dropna().unique())[0]
                # format_func=lambda x: venues_df.loc[x, 'locality'],
            )

        filtered_by_date_df = filter_by_date(date_selection[0], date_selection[1], concerts_df, full_data_df)
        hover_data = {'latitude': False, 'longitude': False}

        if artist_genre_selection == 'Artists':
            data_selection = artist_selection
            column_name = 'artist_id'
        else:
            data_selection = genres_selection
            column_name = 'top_genre'

        if concert_venue_selection == 'Venues':
            results_df = filtered_by_date_df.loc[filtered_by_date_df[column_name].isin(data_selection)]['venue_id'].unique()
            results_df = venues_df.loc[venues_df.index.isin(results_df)]
            results_df = results_df
            marker_size = None
        else:
            results_df = filtered_by_date_df.loc[filtered_by_date_df[column_name].isin(data_selection)]['concert_id'].unique()
            results_df = concerts_df.loc[concerts_df['concert_id'].isin(results_df)]['venue_id']
            results_df = venues_df.loc[venues_df['venue_id'].isin(results_df)]
            results_df

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
            height=500,
        )

        fig_scatter.update_layout(
            mapbox_style='basic',
            mapbox_accesstoken=mapbox_token,
            hoverlabel={
                'bgcolor': 'white',
                'font_size': 12,
            }
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

# Genres in venue histogram
with st.container():
    st.subheader('Genres in venues')

    venue_selection = st.multiselect(
        'Select a venue',
        options=full_data_df['venue_id'].unique(),
        format_func=lambda x: venues_df.loc[venues_df.index == x]['venue'][0],
        #default=stats_df.index.get_loc(stats_df.loc['/venues/418386'].name),  # set default selection to Caves du Manoir
        help='Select at most 4 venues to compare',
    )

    col1, col2, = st.columns(2)

    nbr_selected_venues = len(venue_selection)

    if 0 < nbr_selected_venues < 5:
        idx = 0
        fig_bar = go.Figure()
        colors = ['#f06868', '#80d6ff', '#fab57a', '#edf798']

        for venue in venue_selection:
            venue_stats = stats_venues_genres_df.loc[venue].drop(['nbr_concerts', 'nbr_artists'])
            venue_name = venues_df.loc[venue]['venue']

            fig_bar.add_trace(go.Bar(
                x=venue_stats.index,
                y=venue_stats.values,
                name=venue_name,
                marker_color=colors[idx],
            ))
            idx += 1

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig_bar.update_layout(barmode='group', xaxis_tickangle=-45, autosize=False, height=500, )
        st.plotly_chart(fig_bar, use_container_width=True)

# Artists stats
with st.container():
    st.subheader('Artist stats')

    artist_stats_selection = st.selectbox(
        'Select an artist',
        options=full_data_df['artist_id'].unique(),
        format_func=lambda x: artists_df.loc[x, 'artist_name'],
    )



# Venues data scatter plot
with st.container():
    st.subheader('Venues stats')

    # scatter plot options
    with st.container():
        def useless():
            # get number of artists in each venue
            venues_stats_df = pd.DataFrame(artists_stats_df.groupby('linked_venue_id').size())
            venues_stats_df = venues_stats_df.rename(columns={0: 'nbr_artists'})
            # get median values of listeners and followers for each venue
            venues_stats_df = venues_stats_df.join(pd.DataFrame(artists_stats_df.groupby('linked_venue_id').median()))
            # rename columns with median value
            venues_stats_df = venues_stats_df.rename(columns={
                'listeners': 'listeners_median',
                'followers': 'followers_median'})
            st.write(len(venues_stats_df))

        venues_stats_df = stats_venues_features_df.copy()
        # add venue name and locality to DataFrame
        venues_stats_df = venues_stats_df.merge(
            venues_df[['venue', 'locality', 'latitude', 'longitude']], left_index=True, right_index=True)
        venues_stats_df = venues_stats_df.sort_values(by=['locality'])

        # get min and max nbr of followers (used for slider selection)
        min_followers = int(venues_stats_df['listeners_median'].min())
        #max_followers = int(venues_stats_df['listeners_median'].max())

        col1, col2, col3 = st.columns(3)

        with col1:
            x_data_selection = st.selectbox(
                'Select data for x-axis',
                options=venues_stats_df.drop(['venue', 'locality'], axis=1).columns,
                format_func=lambda x: x.replace('_median', ''),  # remove _median from displayed results
                index=1,
                key='x_select_venues'
            )

            locality_selection = st.multiselect(
                'Select one or multiple localities',
                options=venues_stats_df['locality'].unique(),
            )

        with col2:
            y_data_selection = st.selectbox(
                'Select data for x-axis',
                options=venues_stats_df.drop(['venue', 'locality'], axis=1).columns,
                format_func=lambda x: x.replace('_median', ''),  # remove _median from displayed results
                index=2,
                key='y_select_venues'
            )

            max_artists = int(venues_stats_df['nbr_artists'].max())
            range_nbr_artists = st.slider(
                'Min number of artists',
                1, max_artists,
                (100, max_artists),
            )

        with col3:
            nbr_clusters_selection = st.selectbox(
                'Select number of clusters to show',
                options=range(1, 11),
                index=9,
            )

            max_followers = 10000000
            range_followers = st.slider(
                'Select min and max nbr of followers median',
                min_followers, max_followers,
                (min_followers, max_followers),
                step=10000,
            )

        if locality_selection:
            venues_stats_df = venues_stats_df.loc[venues_stats_df['locality'].isin(locality_selection)]

        # filter DataFrame given the values selected in the options
        venues_stats_df = venues_stats_df.loc[
            (venues_stats_df['nbr_artists'] >= range_nbr_artists[0]) &
            (venues_stats_df['nbr_artists'] <= range_nbr_artists[1])
        ]
        venues_stats_df = venues_stats_df.loc[
            (venues_stats_df['listeners_median'] >= range_followers[0]) &
            (venues_stats_df['listeners_median'] <= range_followers[1])
        ]

        stats_df = venues_stats_df.copy()
        stats_df = stats_df[[x_data_selection, y_data_selection]]
        stats_df = (stats_df - stats_df.mean()) / stats_df.std()
        venue_names = list(stats_df.index)

        km = KMeans(n_clusters=nbr_clusters_selection)
        km.fit(stats_df)
        clusters = km.labels_.tolist()

        cluster_df = pd.DataFrame({'cluster': clusters}, index=venue_names).merge(venues_df['venue'], left_index=True,
                                                                                  right_index=True)
        venues_stats_df = venues_stats_df.merge(cluster_df['cluster'], left_index=True, right_index=True)
        venues_stats_df['cluster'] = venues_stats_df['cluster'].astype(str)

    col1, col2 = st.columns(2)

    with col1:
        # Create distplot with curve_type set to 'normal'
        fig = px.scatter(
            venues_stats_df,
            x=x_data_selection,
            y=y_data_selection,
            color='cluster',
            trendline='ols',
            trendline_scope='overall',
            trendline_color_override='grey',
            color_discrete_sequence=px.colors.qualitative.G10,
            hover_data=['venue', 'locality', 'nbr_artists'],
        )

        fig.update_layout(
            dragmode='pan'
        )

        st.plotly_chart(fig, config=config)

# Concerts in venue scatter plot
with st.container():
    st.subheader('Concerts stats')

    # scatter plot options
    with st.container():
        # features left out: track_popularity, key, mode, type, time_signature
        features_columns = [
            'artist_id', 'danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness',
            'liveness', 'valence', 'loudness', 'tempo', 'duration_ms',
        ]

        # get median of audio features for each artist
        tracks_median_df = tracks_df[features_columns].groupby('artist_id').median()
        # add suffix median to column names
        tracks_median_df = tracks_median_df.add_suffix('_median')
        # sort columns alphabetically
        tracks_median_df = tracks_median_df.reindex(sorted(tracks_median_df.columns), axis=1)

        # drop rows where concert_id and artist_id are a duplicate (ex: duplicated rows bc of multiple top genres for an artist)
        artists_in_concerts = full_data_df.drop_duplicates(subset=['concert_id', 'artist_id']).sort_values(
            by=['venue_id'])
        # add artist listeners and followers stats, rename columns (remove spotify prefix)
        artists_stats_df = artists_in_concerts.merge(
            artists_df[['spotify_listeners', 'spotify_followers']],
            left_on='artist_id', right_index=True)
        artists_stats_df = artists_stats_df.rename(
            columns={'spotify_listeners': 'listeners', 'spotify_followers': 'followers'})
        # add linked venue id
        artists_stats_df = artists_stats_df.merge(venues_df[['linked_venue_id']], left_on='venue_id', right_index=True)
        # add artist audio features stats
        artists_stats_df = artists_stats_df.merge(tracks_median_df, how='left', left_on='artist_id', right_index=True)

        # get number of artists in each concert
        concerts_stats_df = pd.DataFrame(artists_stats_df.groupby('concert_id').size())
        concerts_stats_df = concerts_stats_df.rename(columns={0: 'nbr_artists'})
        # get median values of listeners and followers for each concert
        concerts_stats_df = concerts_stats_df.join(pd.DataFrame(artists_stats_df.groupby('concert_id').median()))
        concerts_stats_df = concerts_stats_df.rename(columns={
            'listeners': 'listeners_median',
            'followers': 'followers_median'})
        # add date of concert
        concerts_stats_df = concerts_stats_df.merge(concerts_df[['date', 'concert_id']], left_index=True, right_on='concert_id')
        concerts_stats_df['date'] = pd.to_datetime(concerts_stats_df['date'])
        # add venue and venue_id columns (to get the name and to filter results by venue)
        concerts_stats_df = concerts_stats_df.merge(concerts_df['venue_id'], left_index=True, right_index=True)
        concerts_stats_df = concerts_stats_df.merge(venues_df['linked_venue_id'], left_on='venue_id', right_index=True)
        concerts_stats_df = concerts_stats_df.merge(venues_df['venue'], left_on='venue_id', right_index=True)
        # sort df by venue name
        concerts_stats_df = concerts_stats_df.sort_values(by=['venue'])
        # keep concerts in venue whose nbr of artists is in range of artist_nbr slider
        concerts_stats_df = concerts_stats_df.loc[concerts_stats_df['linked_venue_id'].isin(venues_stats_df.index)]

        col1, col2, col3 = st.columns(3)

        with col1:
            venue_selection_scatter = st.selectbox(
                'Select a venue',
                options=concerts_stats_df['linked_venue_id'].unique(),
                format_func=lambda x: venues_df.loc[x, 'venue'] + ' (' + venues_df.loc[x, 'locality'] + ')',
            )

        with col2:
            x_data_selection = st.selectbox(
                'Select data for x-axis',
                options=concerts_stats_df.drop(['venue_id', 'venue', 'linked_venue_id'], axis=1).columns,
                format_func=lambda x: x.replace('_median', ''),  # remove _median from displayed results
                index=1,
            )

        with col3:
            y_data_selection = st.selectbox(
                'Select data for y-axis',
                options=concerts_stats_df.drop(['venue_id', 'venue', 'linked_venue_id'], axis=1).columns,
                format_func=lambda x: x.replace('_median', ''),  # remove _median from displayed results
                index=2,
            )

        # get only concerts in given venue
        filtered_concerts_df = concerts_stats_df.loc[concerts_stats_df['linked_venue_id'] == venue_selection_scatter]

        # get only artists in given venue
        filtered_artists_df = artists_stats_df[artists_stats_df['linked_venue_id'] == venue_selection_scatter]
        # drop useless columns
        filtered_artists_df = filtered_artists_df.drop(columns=['spotify_genre', 'top_genre'])
        # get artist name
        filtered_artists_df = filtered_artists_df.merge(artists_df[['artist_name', 'spotify_name']], left_on='artist_id', right_index=True)
        # rename columns
        filtered_artists_df = filtered_artists_df.rename(columns={
            'listeners': 'listeners_median',
            'followers': 'followers_median'})
        # add date of concert
        filtered_artists_df = filtered_artists_df.merge(concerts_df[['concert_id', 'date']], on='concert_id')
        filtered_artists_df['date'] = pd.to_datetime(filtered_artists_df['date'])

        col1, col2 = st.columns(2)

        if x_data_selection == y_data_selection:
            trendline = None
        elif x_data_selection == 'date':
            trendline = None
        else:
            trendline = 'ols'

    filtered_artists_df
    with col1:
        fig = px.scatter(
            filtered_concerts_df,
            x=x_data_selection,
            y=y_data_selection,
            trendline=trendline,
            color='nbr_artists',
            hover_data=['venue', 'nbr_artists', filtered_concerts_df.index],
            title='Show stats by concert in given venue',
        )

        fig.update_layout(
            dragmode='pan'
        )

        st.plotly_chart(fig, config=config)

    with col2:
        fig = px.scatter(
            filtered_artists_df,
            x=x_data_selection,
            y=y_data_selection,
            trendline=trendline,
            #color='nbr_artists',
            hover_data=['artist_name', 'spotify_name', 'concert_id'],
            title='Show stats by artists in given venue',
        )

        fig.update_layout(
            dragmode='pan'
        )

        st.plotly_chart(fig, config=config)

# Venues clusters
with st.container():
    def filter_data(df, nbr_artists):
        filtered_df = df.loc[df['nbr_artists'] > nbr_artists]
        return filtered_df

    filtered_genres_df = filter_data(stats_venues_genres_df, 100)
    filtered_genres_df = filtered_genres_df.drop(columns=['nbr_artists', 'nbr_concerts'])
    filtered_features_df = filter_data(stats_venues_features_df, 100)
    filtered_features_df = filtered_features_df.drop(columns=['nbr_artists'])

    stats_df = filtered_features_df.merge(filtered_genres_df, left_index=True, right_index=True)
    stats_df = stats_df[['listeners_median', 'dance music']]
    stats_df = (stats_df - stats_df.mean()) / stats_df.std()
    venue_names = list(stats_df.index)

    num_clusters = 10
    km = KMeans(n_clusters=num_clusters)
    km.fit(filtered_genres_df)
    clusters = km.labels_.tolist()

    cluster_df = pd.DataFrame({'cluster': clusters}, index=venue_names).merge(venues_df['venue'], left_index=True,
                                                                              right_index=True)

    for x in range(num_clusters):
        st.write(cluster_df.loc[cluster_df['cluster'] == x]['venue'])

# Artists popularity distribution
with st.container():
    st.subheader('Artists stats')

    col1, col2 = st.columns(2)

    with col2:
        preprocess_selection = st.radio('Preprocess data', ['Standardize', 'Normalize', 'None'])

        artists_matched_df = artists_df.loc[pd.notna(artists_df['spotify_id'])]
        artists_matched_df = artists_matched_df[['spotify_followers', 'spotify_listeners']]
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

    with col1:
        # Create distplot with curve_type set to 'normal'
        fig = ff.create_distplot(
            dist_data,
            dist_labels,
            curve_type='normal',  # override default 'kde'
            show_hist=False,
            show_rug=False,
        )

        st.plotly_chart(fig, use_container_width=True)
