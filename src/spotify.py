import subprocess
# Clean port 8000 before starting
subprocess.run(['lsof', '-ti', ':8000'], capture_output=True) and subprocess.run(['kill', '-9', subprocess.run(['lsof', '-ti', ':8001'], capture_output=True, text=True).stdout.strip().split('\n')[0]], check=False)

# spotify credentials
SPOTIPY_CLIENT_ID="12ae4c08efb74ce3a391b032514adae5"
SPOTIPY_CLIENT_SECRET="0cca7fdc50734671a395ba13080a7380"
SPOTIPY_REDIRECT_URI="https://127.0.0.1:8000/"

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scopes = (
    "user-library-read "
    "user-library-modify "
    "user-read-recently-played "
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-currently-playing "
    "playlist-read-private "
    "playlist-read-collaborative "
    "playlist-modify-public "
    "playlist-modify-private "
    "user-follow-read "
    "user-follow-modify "
    "user-top-read "
    "ugc-image-upload"
)

# Use the variables directly
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scopes
))


print(sp.current_user_playlists())