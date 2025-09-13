from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os


load_dotenv()

SPOTIPY_CLIENT_ID= os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET=os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI=os.getenv("SPOTIPY_REDIRECT_URI")

print("ID: ", SPOTIPY_CLIENT_ID)

SCOPES = "playlist-modify-private playlist-modify-public user-read-email"

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPES,
    open_browser=True
))

me = sp.current_user()


