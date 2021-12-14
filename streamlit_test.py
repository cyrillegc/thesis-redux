import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
import statistics
from sklearn import preprocessing
from sklearn.cluster import KMeans
from language_dictionary import language_dict


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


@st.cache
def get_language_dict(lang_set):
    current_lang_dict = dict()
    for key, value in language_dict.items():
        current_lang_dict[key] = value[lang_set]

    return current_lang_dict


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

    with open('data/data_stats_venues_genres_v2.csv', encoding='utf-8') as file:
        stats_venues_genres_df = pd.read_csv(file, index_col=0)

    with open('data/data_stats_venues_artists_v2.csv', encoding='utf-8') as file:
        stats_venues_features_df = pd.read_csv(file, index_col=0)

    with open('data/data_stats_artists_features.csv', encoding='utf-8') as file:
        stats_artists_features_df = pd.read_csv(file, index_col=0)

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
        'stats_artists_features_df': stats_artists_features_df,
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
stats_artists_features_df = data_dict['stats_artists_features_df']
tracks_df = data_dict['tracks_df']

lang_set = 'fre'
current_lang = get_language_dict(lang_set)

# Scatter map
with st.container():
    st.subheader('Geographical distribution of concerts and venues')

    # scatter map options
    with st.container():
        col1, col2, col3= st.columns((1, 3, 1))
        with col1:
            artist_genre_selection = st.radio(
                label=current_lang['label_artist_genre_selection'],
                options=['Genres', 'Artists'],
            )

        if artist_genre_selection == 'Artists':
            with col2:
                artist_selection = st.multiselect(
                    'Select artist',
                    options=artists_df.index,
                    default=artists_df.iloc[0].name,
                    format_func=lambda x: artists_df.loc[x, 'artist_name'],
                )
        else:
            with col2:
                genres_selection = st.multiselect(
                    'Select genres',
                    options=sorted(full_data_df['top_genre'].dropna().unique()),
                    default=sorted(full_data_df['top_genre'].dropna().unique())[1]
                    # format_func=lambda x: venues_df.loc[x, 'locality'],
                )

            with col3:
                min_concerts_selection = st.number_input(
                    label=current_lang['label_min_artists_selection'],
                    min_value=1,
                    value=20,
                )

        #filtered_by_date_df = filter_by_date(date_selection[0], date_selection[1], concerts_df, full_data_df)

        if artist_genre_selection == 'Artists':
            results_df = full_data_df.loc[full_data_df['artist_id'].isin(artist_selection)]
            results_df = results_df.drop_duplicates(subset=['concert_id'], keep='first')
            results_df = results_df.merge(venues_df, left_on='venue_id', right_index=True)
            # get centroid coord for each artist
            centroid_columns = ['centroid_lat', 'centroid_lon', 'mobility_weighted_mean']
            centroid_df = stats_artists_features_df.loc[artist_selection][centroid_columns]
            centroid_df = centroid_df.merge(artists_df['spotify_name'], left_index=True, right_index=True)
            # add centroid coord to df
            results_df = results_df.merge(centroid_df, left_on='artist_id', right_index=True)
            results_df['color_id'] = results_df.groupby(['artist_id']).ngroup()
            results_df['size'] = 1
            hover_data = {'latitude': False, 'longitude': False, 'spotify_name': False, 'size': False}
            color = 'spotify_name'
            opacity = 0.8

        else:  # show venues with selected top genre
            venues_top_genre = stats_venues_genres_df.loc[
                (stats_venues_genres_df['nbr_concerts'] >= min_concerts_selection)
            ]

            venues_top_genre = venues_top_genre.drop(columns=['nbr_concerts', 'genre_diversity'])
            venues_top_genre = venues_top_genre.idxmax(axis=1)  # get top genre for each venue
            venues_top_genre.name = 'top_genre'  # rename Series
            venues_top_genre = venues_df.merge(venues_top_genre, left_on='venue_id', right_index=True)
            results_df = venues_top_genre.loc[venues_top_genre['top_genre'].isin(genres_selection)]
            results_df['size'] = 5

            color = 'top_genre'
            hover_data = {'latitude': False, 'longitude': False, 'size': False}
            opacity = 1

    if not results_df.empty:

        fig_scatter = px.scatter_mapbox(
            results_df,
            lat='latitude', lon='longitude',
            hover_name='venue',
            hover_data=hover_data,
            #color_discrete_sequence=px.colors.sequential.Bluered,
            opacity=opacity,
            zoom=6,
            center={'lat': 46.801111, 'lon': 8.226667},
            color=color,
            height=600,
            size='size',
            size_max=5,
        )

        if artist_genre_selection == 'Artists':

            for idx, row in results_df.iterrows():
                line_lat = [row['latitude'], row['centroid_lat']]
                line_lon = [row['longitude'], row['centroid_lon']]

                fig_scatter.add_trace(
                    go.Scattermapbox(
                        lat=line_lat,
                        lon=line_lon,
                        mode="lines",
                        line={'color': 'rgba(100,100,100, 0.2)'},
                        showlegend=False,
                        hoverinfo='skip',
                    )
                )

            centroid_lat = centroid_df['centroid_lat']
            centroid_lon = centroid_df['centroid_lon']
            #centroid_text = centroid_df['spotify_name']
            name_list = centroid_df['spotify_name']
            mobility_list = centroid_df['mobility_weighted_mean']
            centroid_text = list()
            for i in range(len(mobility_list)):
                centroid_text.append('Artist: ' + name_list[i] + '<br>Mobility: ' + str(mobility_list[i]))
            centroid_color = centroid_df['mobility_weighted_mean']

            fig_scatter.add_trace((go.Scattermapbox(
                lat=centroid_lat,
                lon=centroid_lon,
                mode='markers',
                marker={
                    'size': 11,
                    'color': centroid_color,
                    'colorscale': 'ylorrd',
                    'cmin': 0,
                    'cmax': 1,
                },
                hovertext=centroid_text,
                hoverinfo='text',
                showlegend=False,
            )))

        fig_scatter.update_layout(
            mapbox_style='light',
            mapbox_accesstoken=mapbox_token,
            hoverlabel={
                'bgcolor': 'white',
                'font_size': 12,
            },
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

# Genres in venue histogram
with st.container():
    st.subheader('Genres in venues')

    venue_selection = st.multiselect(
        'Select a venue',
        options=stats_venues_genres_df.index,
        format_func=lambda x: venues_df.loc[x, 'venue'] + ' (' + venues_df.loc[x, 'locality'] + ')',
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
            venue_stats = stats_venues_genres_df.loc[venue].drop(['nbr_concerts', 'genre_diversity'])
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
        min_followers = int(venues_stats_df['spotify_listeners'].min())
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
                current_lang['label_y_data_selection'],
                options=venues_stats_df.drop(['venue', 'locality'], axis=1).columns,
                format_func=lambda x: current_lang[x],
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

        @st.cache
        def filter_and_cluster(venues_stats_df, x_data, y_data, nbr_clusters):

            # filter DataFrame given the values selected in the options
            venues_stats_df = venues_stats_df.loc[
                (venues_stats_df['nbr_artists'] >= range_nbr_artists[0]) &
                (venues_stats_df['nbr_artists'] <= range_nbr_artists[1])
            ]
            venues_stats_df = venues_stats_df.loc[
                (venues_stats_df['spotify_listeners'] >= range_followers[0]) &
                (venues_stats_df['spotify_listeners'] <= range_followers[1])
            ]

            stats_df = venues_stats_df.copy()
            stats_df = stats_df[[x_data, y_data]]
            stats_df = (stats_df - stats_df.mean()) / stats_df.std()
            venue_names = list(stats_df.index)

            km = KMeans(n_clusters=nbr_clusters)
            km.fit(stats_df)
            clusters = km.labels_.tolist()
            clusters = [x + 1 for x in clusters]

            cluster_df = pd.DataFrame({'cluster': clusters}, index=venue_names)
            cluster_df = cluster_df.merge(venues_df['venue'], left_index=True, right_index=True)

            venues_stats_df = venues_stats_df.merge(cluster_df['cluster'], left_index=True, right_index=True)
            venues_stats_df = venues_stats_df.sort_values(by=['cluster'])
            venues_stats_df['cluster'] = venues_stats_df['cluster'].astype(str)

            return venues_stats_df

        venues_stats_df = filter_and_cluster(venues_stats_df, x_data_selection, y_data_selection, nbr_clusters_selection)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            venues_stats_df,
            x=x_data_selection,
            y=y_data_selection,
            color='cluster',
            trendline='ols',
            trendline_scope='overall',
            trendline_color_override='grey',
            color_discrete_sequence=px.colors.qualitative.Plotly,
            hover_data=['venue', 'locality', 'nbr_artists'],
        )

        fig.update_layout(
            dragmode='pan'
        )

        st.plotly_chart(fig, config=config)

    with col2:
        similar_venue_selection = st.selectbox(
            'Select a venue to see its similar venues',
            options=venues_stats_df.index,
            format_func=lambda x: venues_df.loc[x, 'venue'] + ' (' + venues_df.loc[x, 'locality'] + ')',
        )

        cluster_selection = venues_stats_df.loc[similar_venue_selection, 'cluster']
        st.write('Cluster ID:', cluster_selection)

        similar_venues_df = venues_stats_df.loc[venues_stats_df['cluster'] == str(cluster_selection)]
        similar_venues_df = similar_venues_df.sort_values(by=['venue'])
        similar_venues_df = similar_venues_df[['venue', 'locality']]
        similar_venues_df = similar_venues_df.set_index('venue')
        #similar_venues_df = similar_venues_df.style.set_properties(**{'background-color': 'black', 'color': 'green'})
        st.write(similar_venues_df)

# Concerts/artists in venue scatter plot
with st.container():
    st.subheader('Concerts stats')

    # scatter plot options
    with st.container():
        @st.cache
        def get_artists_and_concerts_stats():

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

            # drop rows where concert_id and artist_id are a duplicate
            # (ex: duplicated rows bc of multiple top genres for an artist)
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

            return artists_stats_df, concerts_stats_df

        artists_stats_df, concerts_stats_df = get_artists_and_concerts_stats()
        st.write(len(artists_stats_df['artist_id'].unique()))

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
            hover_data=['artist_name', 'concert_id'],
            hover_name='spotify_name',
            title='Show stats by artists in given venue',
        )

        fig.update_layout(
            dragmode='pan'
        )

        st.plotly_chart(fig, config=config)

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
