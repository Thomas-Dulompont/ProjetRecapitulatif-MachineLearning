import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def ApiSpotify(music_name, artist_name):

    # Authentification avec les informations d'identification de l'API Spotify
    client_id = os.getenv("client_id") 
    client_secret = os.getenv("client_secret") 

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Recherche du track id
    results = sp.search(q=f"track:{music_name} artist:{artist_name}", type="track", limit=1)
    track_id = results['tracks']['items'][0]['id']

    # Récupération des caractéristiques audio du track
    audio_features = sp.audio_features(track_id)[0]
    preview_url = results['tracks']['items'][0]['preview_url']
    album_image_url = results['tracks']['items'][0]['album']['images'][0]['url']

    return audio_features, album_image_url, preview_url