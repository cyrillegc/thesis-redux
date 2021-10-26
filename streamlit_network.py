import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px
import pandas as pd
import datetime
import statistics
from sklearn import preprocessing
from streamlit_agraph import agraph, Node, Edge, Config

with open('data/spotify/data_spotify_top_genres_v3.csv', encoding='utf-8') as file_genres:
    genres_df = pd.read_csv(file_genres, index_col=0)

nodes = []
edges = []

genres_df = genres_df.iloc[:100]
top_genres = genres_df['top_genre'].unique()
sub_genres = genres_df['spotify_genre'].unique()

for top_genre in top_genres:
    nodes.append(Node(id=top_genre, label=top_genre, size=400, color='orange'))

for sub_genre in sub_genres:
    nodes.append(Node(id=sub_genre, label=sub_genre, size=100))

for idx, row in genres_df.iterrows():
    top_genre = row['top_genre']
    sub_genre = row['spotify_genre']
    edges.append(Edge(source=sub_genre, target=top_genre, color='lightblue'))

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