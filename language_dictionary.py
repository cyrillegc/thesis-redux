language_dict = {
    'spotify_followers': {'fre': 'Nbr followers Spotify', 'eng': 'Nbr Spotify followers'},
    'spotify_listeners': {'fre': 'Nbr auditeurs Spotify (mois)', 'eng': 'Nbr Spotify listeners (month)'},
    'nbr_venues': {'fre': 'Nbr salles', 'eng': 'Nbr venues'},
    'nbr_concerts': {'fre': 'Nbr concerts', 'eng': 'Nbr concerts'},
    'active_days': {'fre': 'Jours actifs', 'eng': 'Active days'},
    'active_days_weighted': {'fre': 'Jours actifs pondérés', 'eng': 'Active days weighted'},
    'concert_frequency': {'fre': 'Fréquence concerts', 'eng': 'Concert frequency'},
    'nbr_tours': {'fre': 'Nbr tournées', 'eng': 'Nbr tours'},
    'avg_tour_concerts': {'fre': 'Nbr concerts moy. par tournée', 'eng': 'Nbr concerts by tour avg.'},
    'avg_tour_days': {'fre': 'Durée moy. tournée', 'eng': 'Tour duration avg.'},
    'tour_concert_frequency': {'fre': 'Fréquence concerts par tournée', 'eng': 'Concert frequency by tour'},
    'artist_nbr_venues': {'fre': 'Nbr salles', 'eng': 'Nbr venues'},
    'artist_nbr_concerts': {'fre': 'Nbr concerts', 'eng': 'Nbr concerts'},
    'artist_active_days': {'fre': 'Jours actifs', 'eng': 'Active days'},
    'artist_active_days_weighted': {'fre': 'Jours actifs pondérés', 'eng': 'Active days weighted'},
    'artist_concert_frequency': {'fre': 'Fréquence concerts', 'eng': 'Concert frequency'},
    'artist_nbr_tours': {'fre': 'Nbr tournées', 'eng': 'Nbr tours'},
    'artist_avg_tour_concerts': {'fre': 'Nbr concerts moy. par tournée', 'eng': 'Nbr concerts by tour avg.'},
    'artist_avg_tour_days': {'fre': 'Durée moy. tournée', 'eng': 'Tour duration avg.'},
    'artist_tour_concert_frequency': {'fre': 'Fréquence concerts par tournée', 'eng': 'Concert frequency by tour'},
    'artist_centroid_lat': {'fre': 'Latitude centroïde', 'eng': 'Latitude centroid'},
    'artist_centroid_lon': {'fre': 'Longitude centroïde', 'eng': 'Longitude centroid'},
    'artist_dist_centroid_total': {'fre': 'Distance centroïde tot.', 'eng': 'Distance centroid tot.'},
    'artist_dist_centroid_mean': {'fre': 'Distance centroïde moy.', 'eng': 'Distance centroid avg.'},
    'artist_mobility': {'fre': 'Mobilité', 'eng': 'Mobility'},
    'artist_mobility_weighted': {'fre': 'Mobilité pondérée', 'eng': 'Mobility weighted'},
    'centroid_lat': {'fre': 'Latitude centroïde', 'eng': 'Latitude centroid'},
    'centroid_lon': {'fre': 'Longitude centroïde', 'eng': 'Longitude centroid'},
    'dist_centroid_total': {'fre': 'Distance centroïde tot.', 'eng': 'Distance centroid tot.'},
    'dist_centroid_mean': {'fre': 'Distance centroïde moy.', 'eng': 'Distance centroid avg.'},
    'dist_to_artists_centroid': {'fre': 'Distance salle-centroïde moy.', 'eng': 'Distance venue-centroid'},
    'mobility': {'fre': 'Mobilité', 'eng': 'Mobility'},
    'mobility_weighted': {'fre': 'Mobilité pondérée', 'eng': 'Mobility weighted'},
    'danceability': {'fre': 'Dansabilité', 'eng': 'Danceability'},
    'energy': {'fre': 'Energie', 'eng': 'Energy'},
    'loudness': {'fre': 'Force', 'eng': 'Loudness'},
    'speechiness': {'fre': 'Paroles', 'eng': 'Speechiness'},
    'acousticness': {'fre': 'Acoustique', 'eng': 'Acousticness'},
    'instrumentalness': {'fre': 'Instrumental', 'eng': 'Instrumentalness'},
    'liveness': {'fre': 'Live', 'eng': 'Liveness'},
    'valence': {'fre': 'Valence', 'eng': 'Valence'},
    'tempo': {'fre': 'Tempo', 'eng': 'Tempo'},
    'duration_ms': {'fre': 'Durée morceau (ms)', 'eng': 'Song duration (ms)'},
    'nbr_artists': {'fre': 'Nbr artistes', 'eng': 'Nbr artists'},
    'latitude': {'fre': 'Latitude', 'eng': 'Latitude'},
    'longitude': {'fre': 'Longitude', 'eng': 'Longitude'},
    'label_y_data_selection': {
        'fre': "Sélectionner une variable pour l'axe y",
        'eng': 'Select data for y-axis'},
    'label_artist_genre_selection': {
        'fre': 'Montrer artistes ou genres',
        'eng': 'Show artists or genres'},
    'label_concert_venue_selection': {
        'fre': 'Montrer salles ou concerts',
        'eng': 'Display venues or concerts'},
    'label_min_artists_selection': {
        'fre': 'Nbr min. artistes par salle',
        'eng': 'Min. nbr artists by venue'},
    'label_min_concerts_selection': {
        'fre': 'Nbr min. concerts par salle',
        'eng': 'Min. nbr concerts by venue'},
    'label_geographical_distribution': {
        'fre': 'Répartition géographique des salles',
        'eng': 'Geographical distribution of venues'},
    'description_geographical_distribution': {
        'fre': """
        Cet outil montre comment les salles de concert sont distribuées sur le territoire suisse, 
        de deux manières possibles:
        - Montrer les salles fréquentées par un ou plusieurs artistes
        - Montrer les salles où un ou plusieurs genres sont les plus fréquents (càd au moins 40% des artistes sont de ce genre)
        """,
        'eng': """
        This tool shows how concert venues are distributed on the Swiss territory, with two possibilities:
        - Show the venues visited by one or more artists
        - Show the venues where one or more genres are the most frequent (i.e. at least 40% of the artists are of this genre)
        """
    }
}