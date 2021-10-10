import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px
import pandas as pd


mapbox_token = 'pk.eyJ1Ijoic29sbGlyeWMiLCJhIjoiY2t1bGl1aml1MW5lZDJxbXl2d2RvbWNwdiJ9.ugect2o_eFp-XGOgxaRpBg'

with open('data/data_songkick_venues.csv', encoding='utf-8') as file_venues:
    venues_df = pd.read_csv(file_venues, index_col=0)

hover_data = {'latitude': False, 'longitude': False}

if st.button('Say hello'):
    color = ['green']
else:
    color = ['red']

venues_selection = st.multiselect(
    'venues',
    options=venues_df.index,
    format_func=lambda x: venues_df.loc[x, 'venue'] + ', ' + venues_df.loc[x, 'locality'],
)
print(venues_selection)

fig = px.scatter_mapbox(
    venues_df.loc[venues_selection],
    lat='latitude', lon='longitude',
    height=500,
    hover_name='venue', hover_data=hover_data,
    color_discrete_sequence=color
)

fig.update_layout(mapbox_style='streets', mapbox_accesstoken=mapbox_token)

fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
    )
)

st.plotly_chart(fig)