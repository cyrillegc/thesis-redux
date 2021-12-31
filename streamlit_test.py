import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
from sklearn.cluster import KMeans
from language_dictionary import language_dict
from PIL import ImageColor

in_dev = False
st.set_page_config(layout="wide")
bg_color = "white"
mapbox_token = 'pk.eyJ1Ijoic29sbGlyeWMiLCJhIjoiY2t1bGl1aml1MW5lZDJxbXl2d2RvbWNwdiJ9.ugect2o_eFp-XGOgxaRpBg'
min_date = datetime.date(2010, 1, 1)
max_date = datetime.date(2019, 12, 31)
genres_id = [
    'acoustic music',
    'art music',
    'blues',
    "children's music",
    'country music',
    'dance music',
    'electronic music',
    'experimental music',
    'folk music',
    'functional music',
    'funk',
    'hip hop music',
    'independent music',
    'instrumental music',
    'jazz',
    'lo-fi music',
    'pop music',
    'rhythm and blues',
    'rock music',
    'soul music',
    'underground music',
    'vocal music',
    'world music',
]
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

@st.cache
def spiralize_coord(data_df):
    # initialize
    coord_cols = ['longitude', 'latitude']
    coord_id = 0
    sign = 1
    lim = 1
    curr = 0

    while True:
        # algorithm to jitter point around original point (square spiral)
        if curr == lim:
            curr = 0
            if coord_id == 0:
                sign = -1 * sign
                coord_id = 1
            else:
                lim += 1
                coord_id = 0

        coord = coord_cols[coord_id]
        curr += 1

        duplicate_coord_df = data_df.loc[data_df.duplicated(subset=coord_cols)]
        duplicate_coord_df = duplicate_coord_df.dropna(subset=coord_cols)
        duplicate_coord_df[coord] = duplicate_coord_df[coord] + (0.00001 * sign)
        data_df.loc[data_df.index.isin(duplicate_coord_df.index), coord] = duplicate_coord_df[coord]

        if duplicate_coord_df.empty:
            break

    return data_df


@st.cache
def convert_df(df):
    return df.to_csv(encoding='utf-8')


def get_language_dict(lang_set):
    current_lang_dict = dict()
    for key, value in language_dict.items():
        current_lang_dict[key] = value[lang_set]

    return current_lang_dict


@st.cache(show_spinner=False)
def open_data():
    with open('data/songkick/data_songkick_venues_light_coord.csv', encoding='utf-8') as file:
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

venues_df = data_dict['venues_df'].copy()
concerts_df = data_dict['concerts_df'].copy()
artists_df = data_dict['artists_df'].copy()
genres_df = data_dict['genres_df'].copy()
full_data_df = data_dict['full_data_df'].copy()
stats_venues_genres_df = data_dict['stats_venues_genres_df'].copy()
stats_venues_features_df = data_dict['stats_venues_features_df'].copy()
stats_artists_features_df = data_dict['stats_artists_features_df'].copy()
tracks_df = data_dict['tracks_df'].copy()

# header
col1, col2 = st.columns((5, 1))
with col2:
    lang_id = {'fre': 'Français', 'eng': 'English'}
    lang_set = st.selectbox(
        'Choisir une langue',
        options=['fre', 'eng'],
        format_func=lambda x: lang_id[x],
    )
    current_lang = get_language_dict(lang_set)
with col1:
    st.title(current_lang['label_title'])
    st.markdown(current_lang['description_overall'])


# sidebar
page_selection = st.sidebar.selectbox(
    label=current_lang['label_selection_page'],
    options=['label_page_homepage', 'label_page_map_distribution', 'label_page_genre_frequency',
             'label_page_venues_characteristics', 'label_page_concerts_in_venue', 'label_page_artists_characteristics'],
    format_func=lambda x: current_lang[x],
)

# genres language dict
genres_lang_dict = dict()
for i in range(len(genres_id)):
    genres_name = current_lang['list_labels_genres']
    genres_lang_dict[genres_id[i]] = genres_name[i]

# change genres name according to selected language
full_data_df['top_genre'] = full_data_df['top_genre'].replace(to_replace=genres_lang_dict)
stats_venues_genres_df = stats_venues_genres_df.rename(columns=genres_lang_dict)

# Scatter map
# TODO: choisir une salle et voir tous les centroides des artistes et centroïde moyen
# TODO: afficher toutes les salles sur une carte (avec filtres nbr concerts)

if page_selection == 'label_page_map_distribution' or in_dev:
    st.markdown('---')
    st.subheader(current_lang['label_header_map_distribution'])
    col1, col2 = st.columns((6, 2))
    with col1:
        with st.expander(current_lang['label_expander']):
            st.markdown(current_lang['description_map_distribution'])

    # scatter map options
    with st.container():
        col1, col2, col3, col4, col5 = st.columns((1, 1, 4, 1, 1))
        with col1:
            # select between artists, genres, names
            map_item_selection = st.radio(
                label=current_lang['label_selection_map_item'],
                options=current_lang['options_map_item'],
            )

        with col2:
            if map_item_selection not in ['Venues', 'Salles']:
                st.markdown(current_lang['label_selection_display'], unsafe_allow_html=True)
                show_centroid_selection = st.checkbox(label=current_lang['option_centroids'])
                if show_centroid_selection:
                    show_links_selection = st.checkbox(label=current_lang['option_links'])
            else:
                show_centroid_selection = None

        if map_item_selection in ['Artists', 'Artistes']:
            with col3:
                artist_selection = st.multiselect(
                    label=current_lang['label_selection_artists'],
                    options=sorted(full_data_df['artist_id'].unique()),
                    default='/artists/8181873-duck-duck-grey-duck',  # artists_df.iloc[0].name,
                    format_func=lambda x: artists_df.loc[x, 'spotify_name'],
                )
        elif map_item_selection == 'Genres':
            with col3:
                genres_selection = st.multiselect(
                    label=current_lang['label_selection_genres'],
                    options=sorted(full_data_df['top_genre'].dropna().unique()),
                    default=sorted(full_data_df['top_genre'].dropna().unique())[1]
                    # format_func=lambda x: venues_df.loc[x, 'locality'],
                )

            with col4:
                min_concerts_selection = st.number_input(
                    label=current_lang['label_selection_min_concerts'],
                    min_value=1,
                    value=20,
                )

            with col5:
                genre_frequency_selection = st.slider(
                    label=current_lang['label_selection_genre_frequency'],
                    min_value=0,
                    max_value=100,
                    value=30,
                    step=5,
                )
        else:
            with col3:
                venues_selection = st.multiselect(
                    label=current_lang['label_selection_venues'],
                    options=sorted(full_data_df['venue_id'].unique()),
                    default='/venues/35054',  # venues_df.iloc[0].name,
                    format_func=lambda x: venues_df.loc[x, 'venue'],
                )

        if map_item_selection in ['Artists', 'Artistes']:
            def get_artists_coord(data_df, artist_id_list):
                artists_coord_df = data_df.loc[full_data_df['artist_id'].isin(artist_id_list)]
                artists_coord_df = artists_coord_df.drop_duplicates(subset=['concert_id'], keep='first')
                artists_coord_df = artists_coord_df.merge(venues_df, left_on='venue_id', right_index=True)

                # get centroid coord for each artist
                centroid_columns = ['centroid_lat', 'centroid_lon', 'mobility_weighted']
                centroid_df = stats_artists_features_df.loc[artist_selection][centroid_columns]
                centroid_df = centroid_df.merge(artists_df['spotify_name'], left_index=True, right_index=True)

                # add centroid coord to df
                artists_coord_df = artists_coord_df.merge(centroid_df, left_on='artist_id', right_index=True)
                artists_coord_df['color_id'] = artists_coord_df.groupby(['artist_id']).ngroup()
                artists_coord_df['size'] = 1

                # spiralize duplicate coordinates
                artists_coord_df = spiralize_coord(artists_coord_df)

                venues_distrib = artists_coord_df['spotify_name'].value_counts().reset_index()
                venues_distrib = venues_distrib.rename(columns={
                    'spotify_name': 'nbr_concerts',
                    'index': 'spotify_name',
                    'top_genre': 'genre',
                })

                return artists_coord_df, centroid_df, venues_distrib

            def map_color(data_df):
                # assign artist to a fixed color
                # artists sorted by most count to avoid having two popular genres with same color
                artists_list = data_df['spotify_name'].value_counts().index
                color_list = px.colors.qualitative.Plotly
                nbr_colors = len(color_list)

                color_map_dict = dict()
                for i in range(len(artists_list)):
                    color_id = i % nbr_colors
                    color_map_dict[artists_list[i]] = color_list[color_id]

                return color_map_dict

            results_df, centroid_df, venues_count_df = get_artists_coord(full_data_df, artist_selection)

            color_map = map_color(results_df)
            show_scale = True
            hover_data = {'latitude': False, 'longitude': False, 'spotify_name': True, 'size': False}
            color = 'spotify_name'
            opacity = 1

        # show venues with selected top genre
        elif map_item_selection == 'Genres':
            def get_genres_coord(genres_id_list, min_concerts):
                # filter venues by min number of concerts
                genres_coord_df = stats_venues_genres_df.loc[
                    (stats_venues_genres_df['nbr_concerts'] >= min_concerts)
                ]
                genres_coord_df = genres_coord_df.drop(columns=['nbr_concerts', 'genre_diversity'])

                # get venues with genre freq of at least specified ratio
                genre_ratio = genre_frequency_selection / 100
                genres_coord_df = genres_coord_df[genres_coord_df >= genre_ratio].stack().reset_index()
                genres_coord_df = genres_coord_df.loc[genres_coord_df['level_1'].isin(genres_id_list)]
                genres_coord_df = genres_coord_df.rename(columns={'level_1': 'genre', 0: 'genre_frequency'})
                genres_coord_df = venues_df.merge(genres_coord_df, on='venue_id')

                # get centroid of venues
                centroid_df = genres_coord_df.groupby('genre')[['latitude', 'longitude']].mean()
                centroid_df = centroid_df.rename(columns={'latitude': 'centroid_lat', 'longitude': 'centroid_lon'})

                # add centroid coord to df
                genres_coord_df = genres_coord_df.merge(centroid_df, left_on='genre', right_index=True)
                genres_coord_df['size'] = 1

                venues_distrib = genres_coord_df['genre'].value_counts().reset_index()
                venues_distrib = venues_distrib.rename(columns={'genre': 'nbr_venues', 'index': 'genre'})

                # spiralize duplicate coordinates
                genres_coord_df = spiralize_coord(genres_coord_df)

                return genres_coord_df, centroid_df, venues_distrib

            def map_color(data_df):
                # assign genre to a fixed color
                # genres sorted by most count to avoid having two popular genres with same color
                genres_list = data_df['top_genre'].dropna().value_counts().index
                color_list = px.colors.qualitative.Plotly
                nbr_colors = len(color_list)

                color_map_dict = dict()
                for i in range(len(genres_list)):
                    color_id = i % nbr_colors
                    color_map_dict[genres_list[i]] = color_list[color_id]

                return color_map_dict

            results_df, centroid_df, venues_count_df = get_genres_coord(genres_selection, min_concerts_selection)

            color_map = map_color(full_data_df)
            show_scale = False
            color = 'genre'
            hover_data = {'latitude': False, 'longitude': False, 'size': False, 'genre_frequency': True}
            opacity = 1

        else:
            results_df = full_data_df.merge(venues_df, on='venue_id')
            results_df = results_df.loc[results_df['venue_id'].isin(venues_selection)]
            results_df = results_df.drop_duplicates(subset=['venue_id'], keep='first')
            results_df['size'] = 1

            color_map = dict()
            show_scale = False
            color = 'venue'
            hover_data = {'latitude': False, 'longitude': False, 'size': False}
            opacity = 1

    if not results_df.empty:
        #results_df['genre'] = results_df['genre'].replace(to_replace=genres_lang_dict)

        col1, col2 = st.columns((2, 6))

        with col2:
            if map_item_selection in ['Artistes', 'Artists']:
                st.caption(current_lang['label_plot_map_concerts_artist'])
            else:
                st.caption(current_lang['label_plot_map_venues_genre'])

            def plot_scatter_map():
                fig_scatter = px.scatter_mapbox(
                    results_df,
                    lat='latitude', lon='longitude',
                    hover_name='venue',
                    hover_data=hover_data,
                    color_discrete_map=color_map,
                    opacity=opacity,
                    zoom=6,
                    center={'lat': 46.801111, 'lon': 8.226667},
                    color=color,
                    height=500,
                    size='size',
                    size_max=6,
                    category_orders={color: sorted(results_df[color])},
                    labels=current_lang['label_variables'],
                )

                if map_item_selection not in ['Names', 'Noms'] and show_centroid_selection:
                    if show_links_selection:
                        # add centroid lines

                        for idx, row in results_df.iterrows():
                            line_lat = [row['latitude'], row['centroid_lat']]
                            line_lon = [row['longitude'], row['centroid_lon']]
                            color_id = row[color]
                            hex = color_map[color_id]
                            rgb = ImageColor.getrgb(hex)
                            color_line = 'rgba(' + str(rgb[0]) + ',' + str(rgb[1]) + ',' + str(rgb[2]) + ', 0.1)'

                            fig_scatter.add_trace(
                                go.Scattermapbox(
                                    lat=line_lat,
                                    lon=line_lon,
                                    mode="lines",
                                    #line={'color': 'rgba(100,100,100, 0.2)'},
                                    line=go.scattermapbox.Line(
                                        color=color_line,
                                    ),
                                    showlegend=False,
                                    hoverinfo='skip',
                                )
                            )

                    centroid_lat = centroid_df['centroid_lat']
                    centroid_lon = centroid_df['centroid_lon']

                    # add centroid
                    if map_item_selection in ['Artists', 'Artistes']:
                        artist_name_list = centroid_df['spotify_name']
                        mobility_list = centroid_df['mobility_weighted']
                        centroid_text = list()
                        for i in range(len(mobility_list)):
                            hover_string = '<b>Centroid</b><br>Artist: ' + artist_name_list[i] + \
                                           '<br>Mobility: ' + str(round(mobility_list[i], 2))
                            centroid_text.append(hover_string)
                        inner_centroid_color = centroid_df['mobility_weighted']
                        centroid_color = list()
                        for artist in centroid_df['spotify_name']:
                            centroid_color.append(color_map[artist])
                        outer_size = 15
                        inner_size = 11
                    elif map_item_selection == 'Genres':
                        centroid_text = ['<b>Centroid</b><br>' + s for s in centroid_df.index]
                        centroid_color = list()
                        for genre in centroid_df.index:
                            centroid_color.append(color_map[genre])
                        inner_centroid_color = ['black' for i in range(len(centroid_df))]
                        outer_size = 15
                        inner_size = 8

                    fig_scatter.add_trace(go.Scattermapbox(
                        lat=centroid_lat,
                        lon=centroid_lon,
                        mode='markers',
                        marker=go.scattermapbox.Marker(
                            size=outer_size,
                            color=centroid_color,
                        ),
                        hovertext=centroid_text,
                        hoverinfo='text',
                        showlegend=False,
                    ))

                    # add color for inner centroid
                    fig_scatter.add_trace(go.Scattermapbox(
                        lat=centroid_lat,
                        lon=centroid_lon,
                        mode='markers',
                        marker=go.scattermapbox.Marker(
                            size=inner_size,
                            color=inner_centroid_color,
                            colorscale='ylorrd',
                            cmin=0,
                            cmax=1,
                            showscale=show_scale,
                            colorbar=dict(
                                title='Mobility',
                                len=0.5,
                                y=0.25,
                            ),
                        ),
                        hoverinfo='skip',
                        showlegend=False,
                    ))

                fig_scatter.update_layout(
                    mapbox_style='light',
                    mapbox_accesstoken=mapbox_token,
                    hoverlabel={
                        'bgcolor': 'white',
                        'font_size': 12,
                    },
                    paper_bgcolor=bg_color,
                    margin=dict(l=0, r=0, t=0, b=0),
                )

                return fig_scatter

            fig_scatter = plot_scatter_map()
            st.plotly_chart(fig_scatter, use_container_width=True)

        if map_item_selection not in ['Names', 'Noms']:
            # bar plot for venue counts by artist/genre
            with col1:
                if map_item_selection in ['Artistes', 'Artists']:
                    st.caption(current_lang['label_plot_concerts_count_artist'])
                else:
                    st.caption(current_lang['label_plot_venues_count_genre'])

                nbr_items = venues_count_df.iloc[:, 0].nunique()
                if nbr_items == 1:
                    bar_width = 0.5
                else:
                    bar_width = 0.8

                if map_item_selection in ['Artists', 'Artistes']:
                    x_label = 'spotify_name'
                    y_label = 'nbr_concerts'
                elif map_item_selection == 'Genres':
                    x_label = 'genre'
                    y_label = 'nbr_venues'

                fig = px.bar(
                    venues_count_df,
                    x=x_label,
                    y=y_label,
                    height=500,
                    color_discrete_map=color_map,
                    color=color,
                    labels=current_lang['label_variables'],
                )
                fig.update_traces(
                    width=bar_width,
                )
                fig.update_layout(
                    paper_bgcolor=bg_color,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

# Genres in venue histogram
if page_selection == 'label_page_genre_frequency' or in_dev:
    st.markdown('---')
    st.subheader(current_lang['label_header_genre_frequency'])
    col1, col2 = st.columns((6, 2))
    with col1:
        with st.expander(current_lang['label_expander']):
            st.markdown(current_lang['description_genre_frequency'])

    col1, col2 = st.columns((6, 2))
    with col1:
        venue_selection = st.multiselect(
            label=current_lang['label_selection_venues'],
            options=stats_venues_genres_df.index,
            format_func=lambda x: venues_df.loc[x, 'venue'] + ' (' + venues_df.loc[x, 'locality'] + ')',
            default='/venues/35054',  # default choice: les docks
        )

    with col2:
        venue_dict = {current_lang['alpha']: 'alpha'}
        venue_names = list()
        for venue_id in venue_selection:
            venue_name = venues_df.loc[venue_id, 'venue'] + ' (' + venues_df.loc[venue_id, 'locality'] + ')'
            venue_names.append(venue_name)
            venue_dict[venue_name] = venue_id

        genres_sorting_selection = st.selectbox(
            label=current_lang['label_selection_genres_sorting'],
            options=[current_lang['alpha']] + venue_names,
        )

        genres_sorting_selection = venue_dict[genres_sorting_selection]

    col1, col2, = st.columns((3, 2))

    nbr_selected_venues = len(venue_selection)

    if 0 < nbr_selected_venues < 5:
        idx = 0
        fig_bar = go.Figure()
        colors = ['#f06868', '#80d6ff', '#fab57a', '#edf798']

        # get a list of the genres alphabetically sorted
        sorted_genres = sorted(stats_venues_genres_df.drop(columns=['nbr_concerts', 'genre_diversity']).columns)
        for venue in venue_selection:
            venue_stats = stats_venues_genres_df.loc[venue].drop(['nbr_concerts', 'genre_diversity'])

            # sort the genres by a venue, if selected
            if genres_sorting_selection == venue:
                sorted_genres = list(venue_stats.sort_values(ascending=False).index)

            venue_name = venues_df.loc[venue]['venue']
            fig_bar.add_trace(go.Bar(
                x=venue_stats.index,
                y=venue_stats.values*100,
                name=venue_name,
                marker_color=colors[idx],
            ))
            idx += 1

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig_bar.update_layout(
            barmode='group',
            xaxis_tickangle=-45,
            yaxis_title=current_lang['label_axis_y_genre_frequency'],
            autosize=False,
            height=500,
            paper_bgcolor=bg_color,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis={
                'categoryorder': 'array',
                'categoryarray': sorted_genres,
            },
        )

        with col1:
            st.caption(current_lang['label_plot_genre_frequency'])
            st.plotly_chart(fig_bar, use_container_width=True)

        # show common artists between venues
        with col2:
            if nbr_selected_venues > 1:
                st.caption(current_lang['label_plot_common_artists'])
                artists_list = list()
                for venue in venue_selection:
                    artists_in_venue = sorted(full_data_df.loc[full_data_df['venue_id'] == venue]['artist_id'].unique())
                    artists_list.append(artists_in_venue)

                nbr_venues = len(artists_list)
                if nbr_venues > 1:
                    common_artists = set(artists_list[0])
                    for i in range(1, nbr_venues):
                        common_artists = common_artists.intersection(artists_list[i])

                    concerts_in_venues = full_data_df.loc[full_data_df['venue_id'].isin(venue_selection)]
                    concerts_by_artists = concerts_in_venues.loc[concerts_in_venues['artist_id'].isin(common_artists)]
                    concerts_by_artists = concerts_by_artists.drop_duplicates(subset=['artist_id', 'concert_id'], keep='first')
                    # add concert data
                    concerts_by_artists = concerts_by_artists.merge(concerts_df[['concert_id', 'date']], on='concert_id')
                    # add venues data
                    concerts_by_artists = concerts_by_artists.merge(
                        venues_df[['venue', 'locality']], left_on='venue_id', right_index=True)
                    # add artist data
                    concerts_by_artists = concerts_by_artists.merge(
                        artists_df[['artist_name']], left_on='artist_id', right_index=True)
                    # reorder and rename columns
                    col_order = ['artist_name', 'date', 'venue', 'locality']
                    concerts_by_artists = concerts_by_artists[col_order].sort_values(by=['artist_name', 'date', 'venue'])
                    concerts_by_artists.rename(columns=current_lang['label_variables'], inplace=True)
                    concerts_by_artists.set_index('artist_name', inplace=True)

                    # show dataframe
                    if not concerts_by_artists.empty:
                        st.write(concerts_by_artists)
                    else:
                        st.markdown(current_lang['warning_common_artists'])
    else:
        st.markdown(current_lang['warning_genre_frequency'])

# Venues data scatter plot
if page_selection == 'label_page_venues_characteristics' or in_dev:
    st.markdown('---')
    st.subheader(current_lang['label_header_venues_characteristics'])
    col1, col2 = st.columns((6, 2))
    with col1:
        with st.expander(current_lang['label_expander']):
            st.markdown(current_lang['description_venues_characteristics'])

    # scatter plot options
    with st.container():
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
                label=current_lang['label_selection_x_data'],
                options=venues_stats_df.drop(['venue', 'locality'], axis=1).columns,
                format_func=lambda x: current_lang[x],
                index=0,
                key='x_select_venues'
            )

            locality_selection = st.multiselect(
                label=current_lang['label_selection_locality'],
                options=venues_stats_df['locality'].unique(),
            )

        with col2:
            y_data_selection = st.selectbox(
                label=current_lang['label_selection_y_data'],
                options=venues_stats_df.drop(['venue', 'locality'], axis=1).columns,
                format_func=lambda x: current_lang[x],
                index=1,
                key='y_select_venues'
            )

            max_artists = int(venues_stats_df['nbr_artists'].max())
            range_nbr_artists = st.slider(
                label=current_lang['label_selection_nbr_artists'],
                min_value=1,
                max_value=max_artists,
                value=(100, max_artists),
            )

        with col3:
            nbr_clusters_selection = st.selectbox(
                label=current_lang['label_selection_cluster'],
                options=range(1, 11),
                index=5,
            )

            #max_followers = 10000000
            #range_followers = st.slider(
            #    label=current_lang['label_selection_nbr_followers'],
            #    'Select min and max nbr of followers median',
            #    min_followers, max_followers,
            #    (min_followers, max_followers),
            #    step=10000,
            #)

        if locality_selection:
            venues_stats_df = venues_stats_df.loc[venues_stats_df['locality'].isin(locality_selection)]

        def filter_and_cluster(venues_stats_df, x_data, y_data, nbr_clusters):

            # filter DataFrame given the values selected in the options
            venues_stats_df = venues_stats_df.loc[
                (venues_stats_df['nbr_artists'] >= range_nbr_artists[0]) &
                (venues_stats_df['nbr_artists'] <= range_nbr_artists[1])
            ]
            #venues_stats_df = venues_stats_df.loc[
            #    (venues_stats_df['spotify_listeners'] >= range_followers[0]) &
            #    (venues_stats_df['spotify_listeners'] <= range_followers[1])
            #]

            stats_df = venues_stats_df.copy()
            stats_df = stats_df[[x_data, y_data]]
            stats_df = (stats_df - stats_df.mean()) / stats_df.std()
            venue_names = list(stats_df.index)

            # there can't be more clusters than venues, so if nbr of clusters is too high set it to nbr of venues
            if len(stats_df) < nbr_clusters:
                nbr_clusters = len(stats_df)

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

    col1, col2 = st.columns((5, 3))

    with col1:
        fig = px.scatter(
            venues_stats_df,
            x=x_data_selection,
            y=y_data_selection,
            color='cluster',
            trendline=None,
            trendline_scope='overall',
            trendline_color_override='grey',
            color_discrete_sequence=px.colors.qualitative.Plotly,
            hover_data=['venue', 'locality', 'nbr_artists'],
            #marginal_x='histogram',
            #marginal_y='histogram',
        )

        fig.update_layout(
            dragmode='pan',
            paper_bgcolor=bg_color,
            margin=dict(l=0, r=0, t=0, b=0),
        )

        st.plotly_chart(fig, config=config)

    with col2:
        similar_venue_selection = st.selectbox(
            label=current_lang['label_selection_similar_venues'],
            options=venues_stats_df.index,
            format_func=lambda x: venues_df.loc[x, 'venue'] + ' (' + venues_df.loc[x, 'locality'] + ')',
        )

        cluster_selection = venues_stats_df.loc[similar_venue_selection, 'cluster']
        st.write('Cluster ID:', cluster_selection)

        similar_venues_df = venues_stats_df.loc[venues_stats_df['cluster'] == str(cluster_selection)]
        similar_venues_df = similar_venues_df.sort_values(by=['venue'])
        similar_venues_df = similar_venues_df[['venue', 'locality']]
        similar_venues_df = similar_venues_df.set_index('venue')
        similar_venues_df.rename(columns=current_lang['label_variables'], inplace=True)
        #similar_venues_df = similar_venues_df.style.set_properties(**{'background-color': 'black', 'color': 'green'})

        st.write(similar_venues_df)

# Concerts/artists in venue scatter plot
if page_selection == 'label_page_concerts_in_venue' or in_dev:
    st.markdown('---')
    st.subheader(current_lang['label_header_concerts_in_venue'])
    col1, col2 = st.columns((6, 2))
    with col1:
        with st.expander(current_lang['label_expander']):
            st.markdown(current_lang['description_concerts_in_venue'])

    # scatter plot options
    with st.container():
        @st.cache
        def get_concerts_in_venue_stats():
            # drop rows where concert_id and artist_id are a duplicate
            concerts_in_venues = full_data_df.drop_duplicates(subset=['concert_id', 'artist_id']).sort_values(
                by=['concert_id'])
            # get stats for each artist in each concert
            concerts_in_venues = concerts_in_venues.merge(stats_artists_features_df, how='left', left_on='artist_id', right_index=True)
            # get number of artists in each concert
            concerts_size = concerts_in_venues.groupby('concert_id').size().reset_index()
            concerts_size = concerts_size.rename(columns={0: 'nbr_artists'})
            # mean of artists stats by concert (pas besoin de median rarement plus de 2 artistes par concert)
            concerts_in_venues = concerts_in_venues.groupby('concert_id').mean().reset_index()
            # add number of artists in each concert
            concerts_in_venues = concerts_in_venues.merge(concerts_size, on='concert_id')
            # add date and venue of concert
            concerts_in_venues = concerts_in_venues.merge(
                concerts_df[['date', 'concert_id', 'venue_id']], on='concert_id')
            concerts_in_venues = concerts_in_venues.merge(
                venues_df[['linked_venue_id', 'venue']], left_on='venue_id', right_index=True)
            # sort by venue
            concerts_in_venues = concerts_in_venues.sort_values(by=['venue'])

            return concerts_in_venues

        @st.cache
        def get_artists_in_venue_stats():
            # drop rows where venue_id and artist_id are a duplicate
            # (ex: duplicated rows bc of multiple top genres for an artist)
            artists_in_venues = full_data_df.drop_duplicates(subset=['concert_id', 'artist_id']).sort_values(
                by=['venue_id'])
            # get number concerts in venue by an artist
            artists_size = artists_in_venues.groupby(['venue_id', 'artist_id']).size().reset_index()
            artists_size = artists_size.rename(columns={0: 'nbr_concerts'})
            artists_in_venues = artists_in_venues.drop(columns=['spotify_genre', 'top_genre'])
            # add linked venue id and venue name
            artists_in_venues = artists_in_venues.merge(
                venues_df[['linked_venue_id', 'venue']], left_on='venue_id', right_index=True)
            # get artist name
            artists_in_venues = artists_in_venues.merge(
                artists_df[['artist_name', 'spotify_name']], left_on='artist_id', right_index=True)
            # add artist audio features stats
            artists_in_venues = artists_in_venues.merge(
                stats_artists_features_df.drop(columns=['nbr_concerts']), how='left', left_on='artist_id', right_index=True)
            # add nbr concerts in venue by artist
            artists_in_venues = artists_in_venues.merge(
                artists_size, on=['artist_id', 'venue_id'])
            # add date and venue of concert
            artists_in_venues = artists_in_venues.merge(
                concerts_df[['date', 'concert_id']], on='concert_id')
            # sort by venue name
            artists_in_venues = artists_in_venues.sort_values(by=['venue'])

            return artists_in_venues

        audio_features = [
            'danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
            'valence', 'loudness', 'tempo', 'duration_ms',
        ]
        popularity_features = ['spotify_followers', 'spotify_listeners']
        spatial_features = [
            'centroid_lat', 'centroid_lon', 'dist_centroid_total',
            'dist_centroid_mean', 'mobility', 'mobility_weighted'
        ]
        temporal_features = [
            'active_days', 'active_days_weighted', 'concert_frequency',
            'nbr_tours', 'avg_tour_concerts', 'avg_tour_days', 'tour_concert_frequency',
        ]

        artists_stats_df = get_artists_in_venue_stats()
        concerts_stats_df = get_concerts_in_venue_stats()

        col1, col2, col3, col4 = st.columns((2, 1, 1, 1))

        with col1:
            venue_selection_scatter = st.selectbox(
                label=current_lang['label_selection_venue'],
                options=artists_stats_df['linked_venue_id'].unique(),
                format_func=lambda x: venues_df.loc[x, 'venue'] + ' (' + venues_df.loc[x, 'locality'] + ')',
            )

        with col3:
            x_data_selection = st.selectbox(
                label=current_lang['label_selection_x_data'],
                options=popularity_features+audio_features+['date'],
                format_func=lambda x: x.replace('_median', ''),  # remove _median from displayed results
                index=0,
            )

        with col4:
            y_data_selection = st.selectbox(
                label=current_lang['label_selection_y_data'],
                options=popularity_features+audio_features+['date'],
                format_func=lambda x: x.replace('_median', ''),  # remove _median from displayed results
                index=1,
            )

        # get only concerts in given venue
        filtered_concerts_df = concerts_stats_df.loc[concerts_stats_df['linked_venue_id'] == venue_selection_scatter]

        # get only artists in given venue
        filtered_artists_df = artists_stats_df[artists_stats_df['linked_venue_id'] == venue_selection_scatter]

        if x_data_selection == y_data_selection:
            trendline = None
        elif x_data_selection == 'date':
            trendline = None
        else:
            trendline = 'ols'

    col1, col2 = st.columns(2)

    with col1:
        st.caption(current_lang['label_plot_venue_concerts'])
        fig = px.scatter(
            filtered_concerts_df,
            x=x_data_selection,
            y=y_data_selection,
            trendline=trendline,
            color='nbr_artists',
            hover_data=['venue', 'nbr_artists', filtered_concerts_df.index],
        )

        fig.update_layout(
            dragmode='pan',
            paper_bgcolor=bg_color,
            margin=dict(t=0, b=0),
        )

        st.plotly_chart(fig, config=config)

        venue_concerts_csv = convert_df(filtered_concerts_df)
        venue_name = venues_df.loc[venue_selection_scatter, 'venue'].lower().replace(' ', '_')
        st.download_button(
            label="Download venue data as CSV",
            data=venue_concerts_csv,
            file_name='data_' + venue_name + '_concerts.csv',
            mime='text/csv',
        )

    with col2:
        st.caption(current_lang['label_plot_venue_artists'])
        fig = px.scatter(
            filtered_artists_df,
            x=x_data_selection,
            y=y_data_selection,
            trendline=trendline,
            color='nbr_concerts',
            hover_data=['artist_name', 'concert_id'],
            hover_name='spotify_name',
        )

        fig.update_layout(
            dragmode='pan',
            paper_bgcolor=bg_color,
            margin=dict(t=0, b=0),
        )

        st.plotly_chart(fig, config=config)

        venue_artists_csv = convert_df(filtered_artists_df)
        venue_name = venues_df.loc[venue_selection_scatter, 'venue'].lower().replace(' ', '_')
        st.download_button(
            label="Download venue data as CSV",
            data=venue_artists_csv,
            file_name='data_' + venue_name + '_artists.csv',
            mime='text/csv',
        )

# Individual artists stats
if page_selection == 'label_page_artists_characteristics' or in_dev:
    st.markdown('---')
    st.subheader(current_lang['label_header_artists_characteristics'])
    col1, col2 = st.columns((6, 2))
    with col1:
        with st.expander(current_lang['label_expander']):
            st.markdown(current_lang['description_artists_characteristics'])

    artist_stats_selection = st.selectbox(
        'Select an artist',
        options=full_data_df['artist_id'].unique(),
        format_func=lambda x: artists_df.loc[x, 'artist_name'],
    )

    artist_data = full_data_df.loc[full_data_df['artist_id'] == artist_stats_selection]

    col1, col2 = st.columns(2)
    with col1:
        # get concerts by artist
        artist_concerts = artist_data.drop_duplicates(subset=['artist_id', 'concert_id'], keep='first')
        # add concert data
        artist_concerts = artist_concerts.merge(concerts_df[['concert_id', 'date']], on='concert_id')
        # add venues data
        artist_concerts = artist_concerts.merge(
            venues_df[['venue', 'locality', 'latitude', 'longitude']], left_on='venue_id', right_index=True)
        # add artist data
        artist_concerts = artist_concerts.merge(artists_df[['artist_name']], left_on='artist_id', right_index=True)
        # reorder and rename columns
        col_order = ['artist_name', 'date', 'venue', 'locality', 'latitude', 'longitude']
        artist_concerts = artist_concerts[col_order].sort_values(by=['date'])
        artist_concerts = artist_concerts.rename(columns={'date': 'concert date'})
        artist_concerts = artist_concerts.reset_index(drop=True)

        st.write(artist_concerts)

        artist_csv = convert_df(artist_concerts)
        artist_name = artists_df.loc[artist_stats_selection, 'artist_name'].lower().replace(' ', '_')
        st.download_button(
            label="Download artist concerts data as CSV",
            data=artist_csv,
            file_name='data_' + artist_name + '_concerts.csv',
            mime='text/csv',
        )

    with col2:
        artist_genres = artist_data.drop_duplicates(subset=['spotify_genre', 'top_genre'])
        artist_genres = artist_genres[['spotify_genre', 'top_genre']].reset_index(drop=True)

        st.write(artist_genres)

    # Artists stats
    with st.container():
        st.subheader('Artists stats')
        artist_stats_df = stats_artists_features_df.copy()
        categorical_columns = ['spotify_genres', 'top_genres', 'first_concert_date', 'last_concert_date']
        artist_stats_df = artist_stats_df.drop(columns=categorical_columns)

        col1, col2, col3 = st.columns(3)

        with col1:
            x_data_selection = st.selectbox(
                label=current_lang['label_selection_x_data'],
                options=artist_stats_df.columns,
                format_func=lambda x: x.replace('_median', ''),  # remove _median from displayed results
                index=1,
                key='x_select_artist'
            )

        with col2:
            y_data_selection = st.selectbox(
                label=current_lang['label_selection_y_data'],
                options=artist_stats_df.columns,
                #format_func=lambda x: current_lang[x],
                index=2,
                key='y_select_artist'
            )

        with col3:
            max_concerts = int(artist_stats_df['nbr_concerts'].max())
            range_nbr_concerts = st.slider(
                'Min number of concerts',
                1, max_concerts,
                (5, max_concerts),
            )

        artist_stats_df = artist_stats_df.loc[
            (artist_stats_df['nbr_concerts'] >= range_nbr_concerts[0]) &
            (artist_stats_df['nbr_concerts'] <= range_nbr_concerts[1])
            ]

        artist_stats_df = artist_stats_df.merge(artists_df['spotify_name'], left_index=True, right_index=True)
        artist_stats_df = artist_stats_df.rename(columns={'spotify_name': 'artist'})

        fig = px.scatter(
            artist_stats_df,
            x=x_data_selection,
            y=y_data_selection,
            #color='cluster',
            #trendline='ols',
            #trendline_scope='overall',
            trendline_color_override='grey',
            color_discrete_sequence=px.colors.qualitative.Plotly,
            hover_data=['artist'],
        )

        fig.update_layout(
            dragmode='pan',
            paper_bgcolor=bg_color,
            margin=dict(l=0, r=0, t=0, b=0),
        )

        st.plotly_chart(fig, config=config)

# sources
st.markdown('---')
st.subheader(current_lang['label_header_sources'])
st.markdown(current_lang['description_sources'])
