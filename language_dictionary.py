language_dict = {
    '': {
        'fre': '',
        'eng': ''},

    # others
    'alpha': {'fre': 'Ordre alphabétique', 'eng': 'Alphabetical order'},
    'artist': {'fre': "Artiste", 'eng': 'Artist'},
    'cluster': {'fre': 'Partition', 'eng': 'Cluster'},
    'locality': {'fre': 'Localité', 'eng': 'Locality'},
    'venue': {'fre': 'Salle', 'eng': 'Venue'},


    # variables
    'spotify_followers': {'fre': 'Nbr followers Spotify', 'eng': 'Nbr Spotify followers'},
    'spotify_listeners': {'fre': 'Nbr auditeurs Spotify', 'eng': 'Nbr Spotify listeners'},
    'nbr_venues': {'fre': 'Nbr salles', 'eng': 'Nbr venues'},
    'nbr_concerts': {'fre': 'Nbr concerts', 'eng': 'Nbr concerts'},
    'active_days': {'fre': 'Jours actifs', 'eng': 'Active days'},
    'active_days_weighted': {'fre': 'Jours actifs pondérés', 'eng': 'Active days weighted'},
    'concert_frequency': {'fre': 'Fréquence concerts', 'eng': 'Concert frequency'},
    'nbr_tours': {'fre': 'Nbr tournées', 'eng': 'Nbr tours'},
    'avg_tour_concerts': {'fre': 'Nbr concerts moy. par tournée', 'eng': 'Nbr concerts by tour avg.'},
    'avg_tour_days': {'fre': 'Durée moy. tournée', 'eng': 'Tour duration avg.'},
    'tour_concert_frequency': {'fre': 'Fréquence concerts par tournée', 'eng': 'Concert frequency by tour'},
    'date': {'fre': 'Date concert', 'eng': 'Concert date'},

    'artist_spotify_followers': {'fre': 'Nbr followers Spotify (moy. des artistes)', 'eng': 'Nbr Spotify followers'},
    'artist_spotify_listeners': {'fre': 'Nbr auditeurs Spotify (moy. des artistes)', 'eng': 'Nbr Spotify listeners'},
    'artist_nbr_venues': {'fre': 'Nbr salles (moy. des artistes)', 'eng': 'Nbr venues'},
    'artist_nbr_concerts': {'fre': 'Nbr concerts (moy. des artistes)', 'eng': 'Nbr concerts'},
    'artist_active_days': {'fre': 'Jours actifs (moy. des artistes)', 'eng': 'Active days by artists'},
    'artist_active_days_weighted': {'fre': 'Jours actifs pondérés (moy. des artistes)', 'eng': 'Active days weighted'},
    'artist_concert_frequency': {'fre': 'Fréquence concerts (moy. des artistes)', 'eng': 'Concert frequency'},
    'artist_nbr_tours': {'fre': 'Nbr tournées (moy. des artistes)', 'eng': 'Nbr tours'},
    'artist_avg_tour_concerts': {'fre': 'Nbr concerts moy. par tournée (moy. des artistes)', 'eng': 'Nbr concerts by tour avg.'},
    'artist_average_tour_concerts': {'fre': 'Nbr concerts moy. par tournée (moy. des artistes)', 'eng': 'Nbr concerts by tour avg.'},
    'artist_avg_tour_days': {'fre': 'Durée moy. tournée (moy. des artistes)', 'eng': 'Tour duration avg.'},
    'artist_tour_concert_frequency': {'fre': 'Fréquence concerts par tournée (moy. des artistes)', 'eng': 'Concert frequency by tour'},
    'artist_centroid_lat': {'fre': 'Latitude centroïde (moy. des artistes)', 'eng': 'Latitude centroid'},
    'artist_centroid_lon': {'fre': 'Longitude centroïde (moy. des artistes)', 'eng': 'Longitude centroid'},
    'artist_dist_centroid_total': {'fre': 'Distance centroïde tot. (moy. des artistes)', 'eng': 'Distance centroid tot.'},
    'artist_dist_centroid_mean': {'fre': 'Distance centroïde moy. (moy. des artistes)', 'eng': 'Distance centroid avg.'},
    'artist_mobility': {'fre': 'Mobilité (moy. des artistes)', 'eng': 'Mobility'},
    'artist_mobility_weighted': {'fre': 'Mobilité pondérée (moy. des artistes)', 'eng': 'Mobility weighted'},

    'centroid': {'fre': 'Centroïde', 'eng': 'Centroid'},
    'centroid_lat': {'fre': 'Latitude centroïde', 'eng': 'Latitude centroid'},
    'centroid_lon': {'fre': 'Longitude centroïde', 'eng': 'Longitude centroid'},
    'dist_centroid_total': {'fre': 'Distance centroïde tot.', 'eng': 'Distance centroid tot.'},
    'dist_centroid_mean': {'fre': 'Distance centroïde moy.', 'eng': 'Distance centroid avg.'},
    'dist_to_artists_centroid': {'fre': 'Distance salle-centroïde moy.', 'eng': 'Distance venue-centroid'},
    'mobility': {'fre': 'Mobilité', 'eng': 'Mobility'},
    'mobility_weighted': {'fre': 'Mobilité pondérée', 'eng': 'Mobility weighted'},
    'danceability': {'fre': 'Musique dansante', 'eng': 'Dancy music'},
    'energy': {'fre': 'Musique énergique', 'eng': 'Energic music'},
    'loudness': {'fre': 'Musique forte', 'eng': 'Loud music'},
    'speechiness': {'fre': 'Musique avec des paroles', 'eng': 'Speechy music'},
    'acousticness': {'fre': 'Musique acoustique', 'eng': 'Acoustic music'},
    'instrumentalness': {'fre': 'Musique instrumentale', 'eng': 'Instrumental music'},
    'liveness': {'fre': 'Musique live', 'eng': 'Live music'},
    'valence': {'fre': 'Valence de la musique', 'eng': 'Valence of music'},
    'tempo': {'fre': 'Tempo de la musique', 'eng': 'Music tempo'},
    'duration_ms': {'fre': "Durée moy. d'un morceau (en ms)", 'eng': 'Average song duration (in ms)'},
    'nbr_artists': {'fre': 'Nbr artistes', 'eng': 'Nbr artists'},
    'latitude': {'fre': 'Latitude', 'eng': 'Latitude'},
    'longitude': {'fre': 'Longitude', 'eng': 'Longitude'},

    'label_title': {
        'fre': "T'as où les salles?",
        'eng': 'Where are your venues?'},
    'label_expander': {
        'fre': "Explications",
        'eng': 'Details'},

    # label header
    'label_header_map_distribution': {
        'fre': 'Comment sont répartis les salles et les concerts en Suisse?',
        'eng': 'How are venues and concerts distributed in Switzerland?'},
    'label_header_genre_frequency': {
        'fre': 'Quels sont les genres les plus fréquents dans les salles?',
        'eng': 'What are the most frequent genres in venues?'},
    'label_header_venues_characteristics': {
        'fre': 'Quelles sont les caractéristiques des salles?',
        'eng': "What are the venues' characteristics?"},
    'label_header_concerts_in_venue': {
        'fre': "Quelles sont les caractéristiques des concerts d'une salle?",
        'eng': "What are the concerts' characteristics of a venue?"},
    'label_header_artists_characteristics': {
        'fre': "Quelles sont les caractéristiques des artistes?",
        'eng': "What are the artists' characteristics?"},
    'label_header_artist_stats': {
        'fre': "Quels sont les genres et les concerts d'un artiste précis?",
        'eng': "What are the genres and concerts of a specific artist?"},
    'label_header_sources': {
        'fre': 'Sources',
        'eng': "Sources"},

    # label page
    'label_page_homepage': {
        'fre': "Page d'accueil",
        'eng': 'Homepage'},
    'label_page_map_distribution': {
        'fre': 'Cartographie des salles et concerts',
        'eng': 'Venues and concerts mapping'},
    'label_page_genre_frequency': {
        'fre': 'Genres les plus fréquents dans les salles',
        'eng': 'Most frequent genres in venues'},
    'label_page_venues_characteristics': {
        'fre': 'Caractéristiques des salles',
        'eng': "Venues' characteristics"},
    'label_page_concerts_in_venue': {
        'fre': "Caractéristiques des concerts d'une salle",
        'eng': "Concerts' characteristics of a venue"},
    'label_page_artists_characteristics': {
        'fre': "Caractéristiques des artistes",
        'eng': "Artists' characteristics"},
    'label_page_artist_stats': {
        'fre': "Genres et concerts d'un artiste",
        'eng': "Artist's genres and concerts"},

    # label plot caption
    'label_plot_concerts_count_artist': {
        'fre': 'Nombre de concerts par artiste',
        'eng': 'Concerts count by artist'},
    'label_plot_venues_count_genre': {
        'fre': 'Nombre de salles par genre',
        'eng': 'Venues count by genre'},
    'label_plot_map_concerts_artist': {
        'fre': 'Distribution géographique des concerts par artiste',
        'eng': 'Geographical distribution of concerts by artist'},
    'label_plot_map_venues_genre': {
        'fre': 'Distribution géographique des salles par genre',
        'eng': 'Geographical distribution of concerts by genre'},
    'label_plot_genre_frequency': {
        'fre': 'Fréquence des genres dans les salles sélectionnées',
        'eng': 'Genres frequency in selected venues'},
    'label_plot_common_artists': {
        'fre': 'Artistes communs dans les salles sélectionnées',
        'eng': 'Common artists between selected venues'},
    'label_plot_venue_artists': {
        'fre': 'Caractéristiques des artistes dans la salle sélectionnée',
        'eng': 'Artists charateristics in selected venue'},
    'label_plot_venue_concerts': {
        'fre': 'Caractéristiques des concerts dans la salle sélectionnée',
        'eng': 'Concerts charateristics in selected venue'},

    # label selections
    'label_selection_page': {
        'fre': 'Choisir une page',
        'eng': 'Select a page'},
    'label_selection_artists': {
        'fre': 'Choisir un ou plusieurs artistes',
        'eng': 'Select one or multiple artists'},
    'label_selection_all_artists': {
        'fre': 'Tous les artistes?',
        'eng': 'All artists?'},
    'label_selection_artist_stats': {
        'fre': 'Choisir un artiste',
        'eng': 'Select one artist'},
    'label_selection_concerts_artists': {
        'fre': 'Caractéristiques',
        'eng': 'Characteristics'},
    'label_selection_genre_frequency': {
        'fre': 'Fréquence genre (en %)',
        'eng': 'Genre frequency (in %)'},
    'label_selection_genres': {
        'fre': 'Choisir un ou plusieurs genres',
        'eng': 'Select one or multiple genres'},
    'label_selection_genres_sorting': {
        'fre': 'Trier les genres par',
        'eng': 'Sort genres by'},
    'label_selection_map_item': {
        'fre': 'Filtrer les salles par:',
        'eng': 'Filter venues by:'},
    'label_selection_min_artists': {
        'fre': 'Nbr min. artistes par salle',
        'eng': 'Min. nbr artists by venue'},
    'label_selection_min_concerts': {
        'fre': 'Nbr min. concerts par salle',
        'eng': 'Min. nbr concerts by venue'},
    'label_selection_display': {
        'fre': "<span style='font-size:14px'>Options d'affichage</span>",
        'eng': '<span style="font-size:14px">Display options</span>'},
    'label_selection_venues': {
        'fre': 'Choisir une ou plusieurs salles de concert',
        'eng': 'Select one or multiple venues'},
    'label_selection_venue': {
        'fre': 'Choisir une salle de concert',
        'eng': 'Select one venue'},
    'label_selection_cluster': {
        'fre': 'Choisir le nombre de partitions',
        'eng': 'Select number of clusters'},
    'label_selection_locality': {
        'fre': 'Choisir une ou plusieurs localités',
        'eng': 'Select one or multiple localities'},
    'label_selection_nbr_artists': {
        'fre': "Choisir les salles avec un certain nombre d'artistes",
        'eng': 'Select venues with given number of artists'},
    'label_selection_nbr_concerts': {
        'fre': "Choisir les artistes avec un certain nombre de concerts",
        'eng': 'Select artists with given number of concerts'},
    'label_selection_nbr_followers': {
        'fre': "TBD",
        'eng': 'TBD'},
    'label_selection_similar_venues': {
        'fre': "Choisir une salle pour voir les salles similaires",
        'eng': 'Select a venue to see its similar venues'},
    'label_selection_x_data': {
        'fre': "Sélectionner une variable pour l'axe x",
        'eng': 'Select data for x-axis'},
    'label_selection_y_data': {
        'fre': "Sélectionner une variable pour l'axe y",
        'eng': 'Select data for y-axis'},

    # label axis
    'label_axis_y_genre_frequency': {
        'fre': "Fréquence (en %)",
        'eng': 'Frequency (in %)'},

    # label table
    'label_table_artist_concerts': {
        'fre': "Historique des concerts de l'artiste sélectionné",
        'eng': 'Concert history of the selected artist'},
    'label_table_artist_genres': {
        'fre': "**Genres associés à l'artiste sélectionné**",
        'eng': '**Genres of the selected artist**'},

    # label download
    'label_download_data': {
        'fre': "Télécharger les données en CSV",
        'eng': 'Download data as CSV'},
    'label_download_artist_concerts': {
        'fre': "Télécharger les données sur les concerts de l'artiste en CSV",
        'eng': 'Download artist concerts data as CSV'},

    # warnings
    'warning_genre_frequency': {
        'fre': "⚠️ *Choisir entre 1 et 4 salles.*",
        'eng': '⚠️ *Please select between 1 and 4 venues.*'},
    'warning_common_artists': {
        'fre': "*Aucun artiste commun entre les salles choisies.*",
        'eng': '*No common artist between selected venues.*'},
    'warning_artist_genre': {
        'fre': "*Aucun genre associé à cet artiste.*",
        'eng': '*No genre associated with this artist.*'},

    # details
    'details_common_artists': {
        'fre': "Nombre d'artistes en commun: ",
        'eng': 'Number of common artists: '},
    'details_venues_cluster': {
        'fre': "Ces salles font partie de la ",
        'eng': 'Theses venues belong to '},

    # label variables
    'label_variables': {
        'fre': {
            'nbr_concerts': 'Nombre de concerts',
            'spotify_name': "Nom de l'artiste",
            'date': 'Date concert',
            'venue': 'Salle',
            'locality': 'Localité',
            'cluster': 'Partition'
        },
        'eng': {
            'nbr_concerts': 'Number of concerts',
            'spotify_name': "Artist name",
            'date': 'Concert date',
            'venue': 'Venue',
            'locality': 'Locality',
            'cluster': 'Cluster',
        },
    },

    # list of labels
    'list_labels_genres': {
        'fre': ['Acoustique', 'Classique', 'Blues', "Enfants", 'Country', 'Dance', 'Electronique', 'Expérimentale',
                'Folk', 'Fonctionnelle', 'Funk', 'Hip hop', 'Indé', 'Instrumentale', 'Jazz', 'Lo-fi', 'Pop',
                'Rhythm & blues', 'Rock', 'Soul', 'Underground', 'Vocale', 'Musiques du monde'],
        'eng': ['Acoustic', 'Classical', 'Blues', "Children", 'Country', 'Dance', 'Electronic', 'Experimental',
                'Folk', 'Functional', 'Funk', 'Hip hop', 'Indie', 'Instrumental', 'Jazz', 'Lo-fi', 'Pop',
                'Rhythm and blues', 'Rock', 'Soul', 'Underground', 'Vocal', 'World music']},

    'options_map_item': {
        'fre': ['Artistes', 'Genres', 'Noms'],
        'eng': ['Artists', 'Genres', 'Names']},
    'options_concerts_artists': {
        'fre': ['Concerts', 'Artistes'],
        'eng': ['Concerts', 'Artists']},
    'options_yes_no': {
        'fre': ['Oui', 'Non'],
        'eng': ['Yes', 'No']},
    'option_centroids': {
        'fre': 'Centroïdes',
        'eng': 'Centroids'},
    'option_links': {
        'fre': 'Liens',
        'eng': 'Links'},
    'option_clusters': {
        'fre': 'Partitions',
        'eng': 'Clusters'},
    'option_trendline': {
        'fre': 'Ligne de tendance',
        'eng': 'Trendline'},

    'description_overall': {
        'fre': """
            Outils de visualisation de la scène musicale suisse pour mieux comprendre comment les salles de concert et 
            les artistes évoluent dans ce milieu.
        """,
        'eng': """
            Visualization tools of the Swiss music scene to better understand how concert venues and artists evolve in this environment.
        """
    },
    'description_map_distribution': {
        'fre': """
            #####
            Cet outil de cartographie montre comment les salles de concert et les concerts sont géographiquement distribués sur le territoire suisse, en fonction des artistes, des genres musicaux ou des noms des salles.
            
            ### Graphiques
            ##### Carte
            Cette carte montre où les concerts et les salles sont situés en Suisse. Chaque point sur la carte montre l'emplacement d'un salle de concert. Si plusieurs concerts ont lieu dans la même salle, les différents événements sont affichés légèrement en décalage. Chaque artiste ou chaque genre a une couleur différente (jusqu'à 10 individus). Des informations pour chaque point sont affichées en survolant un point avec la souris.
            
            ##### Nombre d'individus
            Ce diagramme en barre comptabilise le nombre d'individus affichés sur la carte. Si les concerts d'un ou plusieurs artistes sont affichés sur la carte, le diagramme montre le nombre de concerts joués par chaque artiste. Si les salles d'un ou plusieurs genres sont affichées sur la carte, le diagramme montre le nombre de salles pour chaque genre.
            
            ### Paramètres
            
            ##### Filtrer
            
            - **Artistes:**
            Voir toutes les salles où ont joué un ou plusieurs artistes.
            - **Genres:**
            Voir toutes les salles où un ou plusieurs genres sont fréquents.
            - **Noms:**
            Voir où se situe une ou plusieurs salles précises.
            
            #####
            ##### Options d'affichage
            - **Centroïdes:** La carte peut afficher le centroïde (le point moyen) des salles ou concerts affichés. Cela permet de voir la zone moyenne d'un artiste ou d'un genre.
              - Le centroïde d'un artiste correspond à l'emplacement moyen de tous ses concerts. La couleur du centroïde d'un artiste est définie par sa mobilité. La mobilité d'un artiste est définie par la distance parcourue entre ses différents concerts et la variété des lieux de concert. Plus un artiste est mobile, plus son centroïde tendra vers le rouge. A l'inverse, moins un artiste est mobile, plus son centroïde tendra vers le jaune.
              - Le centroïde d'un genre correspond à l'emplacement moyen des salles de concert où ce genre est fréquent. La couleur du centroïde est noire, avec un cercle de la couleur du genre autour.
            - **Liens:**
            Si l'option *Centroïdes* est sélectionnée, les liens entre un centroïde et ses points peuvent être affichés. Cela permet de voir vers quelles zones un artiste ou un genre convergent. L'affichage des liens nécessite une capacité de calcul plus importante et peut péjorer les performances de l'application.
            
            #####
            ##### Choix des artistes, genres ou salles
            En fonction du paramètre *Filtrer* sélectionné, il est possible de choisir un ou plusieurs artistes, genres ou salles. Pour des questions de lisibilité de la carte, il est conseillé de sélectionner au maximum 5 éléments.
            
            ##### Nombre de concerts par salle (avec option *Genres* uniquement)
            Cette option permet de choisir les salles dans lesquelles un nombre minimum de concerts ont été organisés. Par exemple si le nombre minimum choisi est 20, seules les salles où au moins 20 concerts ont eu lieu seront affichées. Cela permet de désengorger la carte des lieux qui ont organisé peu de concerts et qui sont moins représentatifs de la scène musicale suisse.
            
            ##### Fréquence des genres (avec option *Genres* uniquement)
            Cette option permet de choisir les salles dont la fréquence minimum des genres sélectionnés se situe au-delà d'un certain seuil. Par exemple, si le seuil de fréquence choisi est de 30% et que le genre *Rock* est choisi, seules les salles où au moins 30% des artistes sont apparentés au rock sont affichées. Cela permet de mettre en évidence les salles où un genre est commun ou dominant.

        """,
        'eng': """
            #####
            This mapping tool shows how concert venues and concerts are geographically distributed on the Swiss territory, depending on artists, musical genres or venue names.
            
            ### Charts
            ##### Map
            This map shows where concerts and venues are located in Switzerland. Each point on the map shows the location of a concert venue. If several concerts take place in the same venue, the different events are displayed slightly offset. Each artist or genre has a different color (up to 10 individuals). Information for each point is displayed by hovering over it with the mouse.
            
            ##### Number of individuals
            This bar chart counts the number of individuals displayed on the map. If the concerts of one or more artists are displayed on the map, the chart shows the number of concerts played by each artist. If the venues of one or more genres are displayed on the map, the chart shows the number of venues for each genre.
            
            ### Settings
            
            ##### Filter
            
            - Artists:**
            See all the venues where one or more artists have played.
            - Genres:**
            See all venues where one or more genres are frequent.
            - Names:**
            See where one or more specific venues are located.
            
            #####
            ##### Display options
            - Centroids:** The map can display the centroid (the average point) of the venues or concerts displayed. This allows you to see the average area of an artist or genre.
              - The centroid of an artist is the average location of all his concerts. The color of the centroid of an artist is defined by its mobility. The mobility of an artist is defined by the distance traveled between his concerts and the variety of venues. The more mobile an artist is, the more his centroid will tend towards red. On the contrary, the less mobile an artist is, the more his centroid will tend towards yellow.
              - The centroid of a genre corresponds to the average location of concert halls where this genre is frequent. The color of the centroid is black, with a circle of the genre color around it.
            - Links:**
            If the *Centroids* option is selected, the links between a centroid and its points can be displayed. This allows you to see which areas an artist or genre converges on. Displaying links requires more computing power and may affect the performance of the application.
            
            #####
            ##### Choice of artists, genres or venues
            Depending on the *Filter* parameter selected, it is possible to choose one or more artists, genres or venues.For the sake of readability of the map, it is recommended to select a maximum of 5 individuals.
            
            
            ##### Number of concerts per venue (with *Genres* option only)
            This option allows you to select the venues in which a minimum number of concerts have been organized. For example, if the minimum number chosen is 20, only the venues where at least 20 concerts have taken place will be displayed. This allows to clear the map of venues that have organized few concerts and are less representative of the Swiss music scene.
            
            ##### Genre frequency (with *Genres* option only)
            This option allows you to select the venues whose minimum frequency of the selected genres is above a certain threshold. For example, if the frequency threshold is 30% and the genre *Rock* is selected, only venues where at least 30% of the artists are rock related are displayed. This allows to highlight the venues where a genre is common or dominant.            
        """
    },
    'description_genre_frequency': {
        'fre': """
            #####
            Cet outil montre comment les genres musicaux sont distribués dans les salles de concert.
            
            ### Graphique et tableau
            ##### Fréquence des genres
            Ce diagramme en barre montre le pourcentage d'artistes apparentés à un genre musical dans une ou plusieurs salles. Si aucun artiste apparenté à un certain genre n'a joué dans une salle, la fréquence de ce genre est de 0%. Si tous les artistes ayant joué dans une salle sont apparentés à un même genre, ce genre a une fréquence de 100%. Un artiste peut-être apparenté à plusieurs genres, c'est pourquoi la somme des fréquences de tous les genres peut dépasser 100.
            
            ##### Artistes communs
            Lorsque plusieurs salles sont sélectionnées et que ces salles ont des artistes en commun, un tableau s'affiche et montre les concerts donnés par ces artistes dans ces salles. Il est possible de trier le tableau par nom d'artiste, date du concert, salle ou localité.
            
            ### Paramètres
            ##### Choix des salles
            Cette option permet de choisir une ou plusieurs salles pour voir la fréquence des genres dans ces lieux. Pour des questions de lisibilité du graphique, 4 salles maximum peuvent être comparées.
            
            ##### Tri
            Cette option permet de choisir comment les genres sont classés sur le graphique. Il est possible de trier alphabétiquement les genres ou bien en fonction d'une des salles sélectionnées. Si une salle est sélectionnée pour le tri, les genres sont triés en fonction de la fréquence des genres dans cette salle, de manière descendante (du plus fréquent au moins fréquent).
        """,
        'eng': """
            #####
            This tool shows how musical genres are distributed in concert venues.
            
            ### Graph and table
            ##### Genre frequency
            This bar chart shows the percentage of artists related to a musical genre in one or more venues. If no artists related to a certain genre played at a venue, the frequency of that genre is 0%. If all artists who played in a venue are related to a certain genre, this genre has a frequency of 100%. An artist can be related to several genres, that's why the sum of the frequencies of all the genres can exceed 100.
            
            ##### Common artists
            When several venues are selected and these venues have artists in common, a table is displayed showing the concerts given by these artists in these venues. It is possible to sort the table by artist name, concert date, venue or location.
            
            ### Settings
            ##### Choice of venues
            This option allows you to choose one or more venues to see the frequency of genres in these places. For the sake of readability of the chart, a maximum of 4 venues can be compared.
            
            ##### Sorting
            This option allows you to choose how the genres are sorted on the graph. It is possible to sort the genres alphabetically or according to one of the selected venues. If a room is selected for sorting, the genres are sorted according to the frequency of the genres in this room, in a descending order (from most frequent to least frequent).
        """
    },
    'description_venues_characteristics': {
        'fre': """
            #####
            Cet outil met en évidence les caractéristiques des salles de concert, qui sont définies par la moyenne des caractéristiques des artistes ayant joué dans cette salle. La popularité, les attributs musicaux, l'activité et la mobilité des artistes peuvent être comparés. 
            
            ### Graphique et tableau
            ##### Caractéristiques des salles
            Ce diagramme en nuage de points montre les caractéristiques des salles de concert. Chaque point représente une salle et l'emplacement de ce point est défini par deux variables qui sont deux caractéristiques de la salle. Des informations pour chaque point sont affichées en survolant un point avec la souris.
            
            ##### Salles similaires
            Lorsque l'option *Partitions* est sélectionnée, il est possible d'afficher un tableau des salles similaires à une salle donnée, selon les deux caractéristiques choisies. La similarité des salles est définie par l'algorithme du *K-means*.
            
            ### Paramètres
            ##### Variables pour les axes x et y
            Cette option permet de choisir les deux caractéristiques pour comparer les salles. Si une même variable est choisie pour les deux axes, tous les points seront alignés. Les variables possibles sont les suivantes:
            - Popularité:
              - **Nombre d'artistes**: nombre d'artistes ayant joué dans la salle
              - **Nombre de followers**: nombre de followers sur Spotify
              - **Nombre d'auditeurs**: nombre d'auditeurs mensuels sur Spotify
            - Attributs musicaux
              - **Musique acoustique**: de 0 (peu acoustique) à 1 (très acoustique)
              - **Musique dansante**: de 0 (peu dansant) à 1 (très dansant)
              - **Musique énergique**: de 0 (peu énergique) à 1 (très énergique)
              - **Musique instrumentale**: de 0 (peu instrumentale) à 1 (très instrumentale)
              - **Musique forte**: de 0 (musique douce) à 1 (musique forte)
              - **Musique avec des paroles**: de 0 (musique sans parole) à 1 (musique avec que des paroles)
              - **Tempo de la musique**: de 0 à 100
              - **Valence de la musique**: de 0 (négatif) à 1 (positif)
            - Activité des artistes
              - **Fréquence des concerts**: de 0 (aucun concert) à 1 (concert quotidien)
              - **Nombre moyen de concerts par tournée**: une tournée est définie comme une période durant laquelle au moins deux concerts ont lieu, sans qu’il ne se passe plus de 90 jours entre deux concerts successifs
              - **Intensité moyenne d'une tournée**: de 0 (1 concert chaque 90 jours dans une tournée) à 1 (1 concert par jour dans une tournée)
            - Mobilité des artistes
              - **Mobilité**: de 0 (un artiste ne change pas de salle) à 1 (un artiste n'a jamais joué 2 fois au même endroit)
              - **Mobilité pondérée**: de 0 (1 seule salle fréquentée et aucune distance parcourue) à 1 (jamais 2 fois la même salle et une distance maximum parcourue entre chaque salle)
            #####
            ##### Choix de localités
            Cette option permet de choisir d'afficher uniquement les salles situées dans une ou plusieurs localités. Cela permet de faire des comparaisons plus ciblées sur des salles qui se trouvent dans des même localités.
            
            ##### Nombre d'artistes par salle
            Cette option permet de choisir les salles dans lesquelles un certain nombre d'artistes ont joué. Par exemple si le nombre minimum choisi est 100, seules les salles où au moins 100 artistes ont se sont produits seront affichées. Cela permet de désengorger le graphique des lieux qui ont organisé peu de concerts et qui sont moins représentatifs de la scène musicale suisse.
            
            ##### Options d'affichage
            - **Partitions**: cette option permet de grouper les points en un certain nombre de partitions, définies par l'algorithme du *K-means*. Si cette option est sélectionnée, il est possible de choisir le **Nombre de partitions**, entre 1 et 10. Cela permet de montrer quelles salles sont similaires selon les caractéristiques choisies. Dans la plupart des combinaisons de variables, il est recommandé d'avoir un nombre de partitions entre 4 et 8. Au-delà de 8, les partitions obtenues ne reflètent pas nécessairement une réelle différence entre chaque groupe.
            - **Ligne de tendance**: cette option permet d'afficher sur le graphique une ligne de tendance.
        """,
        'eng': """
            #####
            This tool highlights the characteristics of concert venues, which are defined by the average of the characteristics of the artists who have performed in that venue. Artists' popularity, musical attributes, activity and mobility can be compared. 
            
            ### Graph and table
            ##### Venue characteristics
            This scatter plot shows the characteristics of concert venues. Each point represents a venue and the location of that point is defined by two variables that are two characteristics of the venue. Information for each point is displayed by hovering over a point with the mouse.
            
            ##### Similar venues
            When the *Partitions* option is selected, it is possible to display a table of venues similar to a given venue, according to the two selected characteristics. The similarity of the venues is defined by the *K-means* algorithm.
            
            ### Parameters
            ##### Variables for x and y axis
            This option allows to choose the two characteristics to compare the venues. If the same variable is chosen for both axes, all points will be aligned. The possible variables are as follows:
            - Popularity:
              - **Number of artists**: number of artists who have played in the venue
              - **Number of followers**: number of followers on Spotify
              - **Number of listeners**: number of monthly listeners on Spotify
            - Musical attributes
              - **Acoustic music**: from 0 (not very acoustic) to 1 (very acoustic)
              - **Dance music**: from 0 (not very danceable) to 1 (very danceable)
              - **Energetic music**: from 0 (not very energetic) to 1 (very energetic)
              - **Instrumental music**: from 0 (not very instrumental) to 1 (very instrumental)
              - **Loud music**: from 0 (soft music) to 1 (loud music)
              - **Music with lyrics**: from 0 (music without lyrics) to 1 (music with lyrics only)
              - **Music tempo**: from 0 to 100
              - **Music valence**: from 0 (negative) to 1 (positive)
            - Activity of artists
              - **Frequency of concerts**: from 0 (no concert) to 1 (daily concert)
              - **Average number of concerts per tour**: a tour is defined as a period during which at least two concerts take place, with no more than 90 days between two successive concerts
              - **Average density of a tour**: from 0 (1 concert every 90 days on a tour) to 1 (1 concert per day on a tour)
            - Mobility of artists
              - **Mobility**: from 0 (an artist does not change venue) to 1 (an artist has never played twice in the same place)
              - **Weighted mobility**: from 0 (only 1 venue attended and no distance traveled) to 1 (never the same venue twice and maximum distance traveled between each venue)
            #####
            ##### Choice of localities
            This option allows you to choose to display only the rooms located in one or more localities. This allows you to make more targeted comparisons between venues in the same locality.
            
            ##### Number of artists per venue
            This option allows you to select the venues in which a certain number of artists have played. For example, if the minimum number chosen is 100, only the venues where at least 100 artists have performed will be displayed. This allows you to clear the graph of venues that have organized few concerts and that are less representative of the Swiss music scene.
            
            ##### Display options
            - Partitions**: this option allows to group the points into a number of partitions, defined by the *K-means* algorithm. If this option is selected, it is possible to choose the **Number of partitions**, between 1 and 10. This allows to show which rooms are similar according to the chosen characteristics. In most combinations of variables, it is recommended to have a number of partitions between 4 and 8. Beyond 8, the scores obtained do not necessarily reflect a real difference between each group.
            - Trend line**: this option allows you to display a trend line on the graph.
            
        """
    },
    'description_concerts_in_venue': {
        'fre': """
            Cet outil met en évidence, pour une salle de concert précise, les caractéristiques des concerts qui y ont eu lieu et des artistes qui y ont joué. Les caractéristiques d'un concert sont définies par la moyenne des caractéristiques des artistes participant à ce concert. La popularité, les attributs musicaux, l'activité et la mobilité des artistes peuvent être comparés. 
            
            ### Graphique
            ##### Caractéristiques des concerts d'une salle
            Ce diagramme en nuage de points montre les caractéristiques de tous les concerts ayant eu lieu dans une salle. Chaque point représente un concert et l'emplacement de ce point est défini par deux variables qui sont deux caractéristiques de ce concert. Des informations pour chaque point sont affichées en survolant un point avec la souris.
            
            ### Paramètres
            ##### Choix d'une salle de concert
            Cette option permet de choisir une salle de concert pour voir les caractéristiques de ses concerts ou artistes.
            
            ##### Variables pour les axes x et y
            Cette option permet de choisir les deux caractéristiques pour comparer les concerts ou les artistes liés à la salle sélectionnée. Si une même variable est choisie pour les deux axes, tous les points seront alignés. Les variables possibles sont les suivantes:
            - Popularité:
              - **Nombre d'artistes**: nombre d'artistes ayant pris part au concert (uniquement avec l'option *Caractéristiques: Concerts* sélectionnée)
               - **Nombre de concerts**: nombre de concerts auxquels l'artiste a pris part dans la salle sélectionnée (uniquement avec l'option *Caractéristiques: Artistes* sélectionnée)
              - **Nombre de followers**: nombre de followers sur Spotify
              - **Nombre d'auditeurs**: nombre d'auditeurs mensuels sur Spotify
            - Attributs musicaux
              - **Musique acoustique**: de 0 (peu acoustique) à 1 (très acoustique)
              - **Musique dansante**: de 0 (peu dansant) à 1 (très dansant)
              - **Musique énergique**: de 0 (peu énergique) à 1 (très énergique)
              - **Musique instrumentale**: de 0 (peu instrumentale) à 1 (très instrumentale)
              - **Musique forte**: de 0 (musique douce) à 1 (musique forte)
              - **Musique avec des paroles**: de 0 (musique sans parole) à 1 (musique avec que des paroles)
              - **Tempo de la musique**: de 0 à 100
              - **Valence de la musique**: de 0 (négatif) à 1 (positif)
            - Intensité des tournées
              - **Fréquence des concerts**: de 0 (aucun concert) à 1 (concert quotidien)
              - **Nombre moyen de concerts par tournée**: une tournée est définie comme une période durant laquelle au moins deux concerts ont lieu, sans qu’il ne se passe plus de 90 jours entre deux concerts successifs
              - **Intensité moyenne d'une tournée**: de 0 (1 concert chaque 90 jours dans une tournée) à 1 (1 concert par jour dans une tournée)
            - Mobilité des artistes
              - **Mobilité**: de 0 (un artiste ne change pas de salle) à 1 (un artiste n'a jamais joué 2 fois au même endroit)
              - **Mobilité pondérée**: de 0 (1 seule salle fréquentée et aucune distance parcourue) à 1 (jamais 2 fois la même salle et une distance maximum parcourue entre chaque salle)
            - Autre
              - **Date du concert**
            #####
            ##### Caractéristiques
            Cette option permet de choisir de montrer les caractéristiques des concerts ou des artistes. Les caractéristiques d'un concert sont définies par la moyenne des caractéristiques des artistes ayant pris part à ce concert. Des artistes hétéroclites peuvent participer au même concert, c'est pourquoi il peut être intéressant de voir individuellement les caractéristiques de chaque artiste.
            
            ##### Options d'affichage
            L'option de *Ligne de tendance* permet d'afficher sur le graphique une ligne de tendance.            
        """,
        'eng': """
            This tool highlights, for a specific concert venue, the characteristics of the concerts that took place there and of the artists that played there. The characteristics of a concert are defined by the average of the characteristics of the artists participating in that concert. The popularity, musical attributes, activity and mobility of the artists can be compared. 
            
            ### Chart
            ##### Characteristics of concerts in a venue
            This scatter plot shows the characteristics of all concerts that took place in a venue. Each point represents a concert and the location of this point is defined by two variables that are two characteristics of this concert. Information for each point is displayed by hovering over a point with the mouse.
            
            ### Parameters
            ##### Choice of a concert venue
            This option allows you to choose a concert venue to see the characteristics of its concerts or artists.
            
            ##### Variables for the x and y axes
            This option allows you to choose the two characteristics to compare the concerts or artists related to the selected venue. If the same variable is chosen for both axes, all points will be aligned. The possible variables are as follows:
            - Popularity:
              - **Number of artists**: number of artists who took part in the concert (only with the *Characteristics: Concerts* option selected)
              - **Number of concerts**: number of concerts in which the artist has taken part in the selected venue (only with the option *Characteristics: Artists* selected)
              - **Number of followers**: number of followers on Spotify
              - **Number of listeners**: number of monthly listeners on Spotify
            - Music attributes
              - **Acoustic music**: from 0 (not very acoustic) to 1 (very acoustic)
              - **Dance music**: from 0 (not very danceable) to 1 (very danceable)
              - **Energetic music**: from 0 (not very energetic) to 1 (very energetic)
              - **Instrumental music**: from 0 (not very instrumental) to 1 (very instrumental)
              - **Loud music**: from 0 (soft music) to 1 (loud music)
              - **Music with lyrics**: from 0 (music without lyrics) to 1 (music with lyrics only)
              - **Music tempo**: from 0 to 100
              - **Music valence**: from 0 (negative) to 1 (positive)
            - Intensity of the tours
              - **Frequency of concerts**: from 0 (no concert) to 1 (daily concert)
              - **Average number of concerts per tour**: a tour is defined as a period during which at least two concerts take place, with no more than 90 days between two successive concerts
              - **Average density of a tour**: from 0 (1 concert every 90 days on a tour) to 1 (1 concert per day on a tour)
            - Mobility of artists
              - **Mobility**: from 0 (an artist does not change venue) to 1 (an artist has never played twice in the same place)
              - **Weighted mobility**: from 0 (only 1 venue attended and no distance traveled) to 1 (never the same venue twice and a maximum distance traveled between each venue)
            - Other
              - **Date of the concert**
            #####
            ##### Characteristics
            This option allows you to choose to show the characteristics of concerts or artists. The characteristics of a concert are defined by the average of the characteristics of the artists who took part in this concert. Different artists may participate in the same concert, so it may be interesting to see the characteristics of each artist individually.
            
            ##### Display options
            The *Trend line* option allows you to display a trend line on the graph.
        """
    },
    'description_artists_characteristics': {
        'fre': """
            Cet outil met en évidence les caractéristiques des artistes ayant joué en Suisse ou de certains artistes. La popularité, les attributs musicaux, l'activité et la mobilité des artistes peuvent être comparés.
            
            ### Graphique
            ##### Caractéristiques des artistes
            Ce diagramme en nuage de points montre les caractéristiques des artistes ayant joué en Suisse ou de certains artistes. Chaque point représente un artiste et l'emplacement de ce point est défini par deux variables qui sont deux caractéristiques de cet artiste. Des informations pour chaque point sont affichées en survolant un point avec la souris. Un bouton permet de télécharger les données du graphique en format CSV.
            
            ### Paramètres  
            ##### Variables pour les axes x et y  
            Cette option permet de choisir les deux caractéristiques pour comparer les artistes. Si une même variable est choisie pour les deux axes, tous les points seront alignés. Les variables possibles sont les suivantes:  
            - Popularité:  
              - **Nombre d'artistes**: nombre d'artistes ayant joué dans la salle
              - **Nombre de followers**: nombre de followers sur Spotify
              - **Nombre d'auditeurs**: nombre d'auditeurs mensuels sur Spotify
            - Attributs musicaux  
              - **Musique acoustique**: de 0 (peu acoustique) à 1 (très acoustique)
              - **Musique dansante**: de 0 (peu dansant) à 1 (très dansant)
              - **Musique énergique**: de 0 (peu énergique) à 1 (très énergique)
              - **Musique instrumentale**: de 0 (peu instrumentale) à 1 (très instrumentale) 
              - **Musique forte**: de 0 (musique douce) à 1 (musique forte)
              - **Musique avec des paroles**: de 0 (musique sans parole) à 1 (musique avec que des paroles)
              - **Tempo de la musique**: de 0 à 100
              - **Valence de la musique**: de 0 (négatif) à 1 (positif)
            - Activité des artistes
              - **Fréquence des concerts**: de 0 (aucun concert) à 1 (concert quotidien)
              - **Nombre moyen de concerts par tournée**: une tournée est définie comme une période durant laquelle au moins deux concerts ont lieu, sans qu’il ne se passe plus de 90 jours entre deux concerts successifs
              - **Intensité moyenne d'une tournée**: de 0 (1 concert chaque 90 jours dans une tournée) à 1 (1 concert par jour dans une tournée)
            - Mobilité des artistes
              - **Mobilité**: de 0 (un artiste ne change pas de salle) à 1 (un artiste n'a jamais joué 2 fois au même endroit)
              - **Mobilité pondérée**: de 0 (1 seule salle fréquentée et aucune distance parcourue) à 1 (jamais 2 fois la même salle et une distance maximum parcourue entre chaque salle)
            #####
            ##### Tous les artistes?
            Cette option binaire permet d'afficher soit l'ensemble des artistes soit une sélection d'artistes.
            
            ##### Nombre de concerts (avec l'option *Tous les artistes* uniquement)
            Cette option permet de choisir les artistes qui ont joué un certain nombre de concerts en Suisse. Par exemple, si le nombre de concerts minimum choisi est 5, seuls les artistes qui se sont produits au moins 5 fois en Suisse seront affichés. Cela permet de désengorger le graphique des artistes qui ont peu joué en Suisse et qui peuvent être moins représentatifs de la scène musicale suisse.
            
            ##### Choix d'un artiste (sans l'option *Tous les artistes* uniquement)
            Cette option permet de choisir les artistes à afficher sur le graphique.
        """,
        'eng': """
            This tool highlights the characteristics of artists who have performed in Switzerland or of certain artists. The popularity, musical attributes, activity and mobility of the artists can be compared.
            
            ### Graphic
            ##### Characteristics of the artists
            This scatter plot shows the characteristics of artists who have performed in Switzerland or of selected artists. Each point represents an artist and the location of this point is defined by two variables that are two characteristics of this artist. Information for each point is displayed by hovering the mouse over a point. A button allows you to download the graph data in CSV format.
            
            ### Parameters  
            ##### Variables for x and y axis  
            This option allows you to choose the two characteristics to compare the artists. If the same variable is chosen for both axes, all points will be aligned. The possible variables are as follows:  
            - Popularity:
              - **Number of artists**: number of artists who took part in the concert (only with the *Characteristics: Concerts* option selected)
              - **Number of concerts**: number of concerts in which the artist has taken part in the selected venue (only with the option *Characteristics: Artists* selected)
              - **Number of followers**: number of followers on Spotify
              - **Number of listeners**: number of monthly listeners on Spotify
            - Music attributes
              - **Acoustic music**: from 0 (not very acoustic) to 1 (very acoustic)
              - **Dance music**: from 0 (not very danceable) to 1 (very danceable)
              - **Energetic music**: from 0 (not very energetic) to 1 (very energetic)
              - **Instrumental music**: from 0 (not very instrumental) to 1 (very instrumental)
              - **Loud music**: from 0 (soft music) to 1 (loud music)
              - **Music with lyrics**: from 0 (music without lyrics) to 1 (music with lyrics only)
              - **Music tempo**: from 0 to 100
              - **Music valence**: from 0 (negative) to 1 (positive)
            - Intensity of the tours
              - **Frequency of concerts**: from 0 (no concert) to 1 (daily concert)
              - **Average number of concerts per tour**: a tour is defined as a period during which at least two concerts take place, with no more than 90 days between two successive concerts
              - **Average density of a tour**: from 0 (1 concert every 90 days on a tour) to 1 (1 concert per day on a tour)
            - Mobility of artists
              - **Mobility**: from 0 (an artist does not change venue) to 1 (an artist has never played twice in the same place)
              - **Weighted mobility**: from 0 (only 1 venue attended and no distance traveled) to 1 (never the same venue twice and a maximum distance traveled between each venue)
            #####
            ##### All artists?
            This binary option allows you to display either all the artists or a selection of artists.
            
            ##### Number of concerts (with the *All artists* option only)
            This option allows you to select the artists who have played a certain number of concerts in Switzerland. For example, if the minimum number of concerts chosen is 5, only the artists who have performed at least 5 times in Switzerland will be displayed. This allows to clear the chart of artists who have not played many concerts in Switzerland and who may be less representative of the Swiss music scene.
            
            ##### Choose an artist (without the *All artists* option only)
            This option allows you to choose the artists to be displayed on the graph.
        """
    },

    'description_artist_stats': {
        'fre': """
            Cet outil permet de voir quels genres sont associés à un artiste précis et d'obtenir une liste détaillée des concerts auxquels il a pris part en Suisse.
            
            ### Graphique et tableau
            ##### Genres associés à un artiste
            Ce diagramme de Sankey montre les genres musicaux associés à un certain artiste, en mettant en évidence ses genres globaux et les genres spécifiques. Par exemple, si un artiste a comme genre spécifique le *dance rock*, les genres globaux de *dance* et *rock* seront associés aussi à cet artiste. Un genre global peut être lié à plusieurs genres spécifiques et vice versa. Le diagramme montre donc à la fois l'ensemble des genres associés à un artiste, mais aussi les liens entre les genres globaux et les genres spécifiques. 
            
            ##### Historique des concerts d'un artiste
            Ce tableau liste l'ensemble des concerts joués par un artiste précis. Pour chaque  concert est renseigné sa date, sa salle, sa localité et ses coordonnées géographiques. Un bouton permet de télécharger les données du tableau en format CSV.
            
            ### Paramètre
            ##### Choix d'un artiste
            Cette option permet de choisir un artiste pour voir les genres qui lui sont associés et son historique de concerts en Suisse.
        """,
        'eng': """
            This tool allows you to see which genres are associated with a specific artist and to obtain a detailed list of concerts in which he or she took part in Switzerland.
            
            ### Graphic and table
            ##### Genres associated with an artist
            This Sankey diagram shows the musical genres associated with a certain artist, highlighting their global genres and specific genres. For example, if an artist has *dance rock* as a specific genre, the global genres of *dance* and *rock* will also be associated with that artist. A global genre can be linked to several specific genres and vice versa. The diagram therefore shows both the set of genres associated with an artist, but also the links between the global genres and the specific genres. 
            
            ##### Concert history of an artist
            This table lists all the concerts played by a specific artist. For each concert, the date, the venue, the location and the geographical coordinates are indicated. A button allows you to download the data from the table in CSV format.
            
            ### Parameter
            ##### Choice of an artist
            This option allows you to choose an artist to see the genres associated with him/her and his/her concert history in Switzerland.
        """
    },

    'description_sources_data': {
        'fre': """
            #### Données
            - Salles et concerts: [Songkick](https://www.songkick.com/)
            - Artistes: [Spotify](https://developer.spotify.com/documentation/web-api/)
            - Genres musicaux: [Wikidata](https://www.wikidata.org/)
            
            Le projet complet est disponible sur [Github](https://github.com/cyrillegc/thesis-redux).
        """,
        'eng': """
            #### Data
            - Venues and concerts: [Songkick](https://www.songkick.com/)
            - Artists: [Spotify](https://developer.spotify.com/documentation/web-api/)
            - Music genres: [Wikidata](https://www.wikidata.org/)
            
            The full project is available on [Github](https://github.com/cyrillegc/thesis-redux).            
        """
    },
    'description_sources_packages': {
        'fre': """
            #### Librairies
            - Mise en page: [Streamlit](https://streamlit.io/)
            - Graphiques: [Plotly](https://plotly.com/)
            - Cartographie: [Mapbox](https://www.mapbox.com/)
        """,
        'eng': """
            #### Packages
            - Layout: [Streamlit](https://streamlit.io/)
            - Graphs: [Plotly](https://plotly.com/)
            - Map: [Mapbox](https://www.mapbox.com/)
        """
    },
}
