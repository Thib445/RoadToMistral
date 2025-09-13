import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Identifiants 
SPOTIPY_CLIENT_ID = 'ton_client_id'
SPOTIPY_CLIENT_SECRET = 'ton_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'  # URI de redirection



# Initialise le client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-library-read playlist-modify-public"  # Définis les permissions nécessaires
))
