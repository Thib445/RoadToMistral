from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

SPOTIPY_CLIENT_ID= os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET=os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI=os.getenv("SPOTIPY_REDIRECT_URI")

SCOPES = (
    "ugc-image-upload "
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-currently-playing "
    "app-remote-control "
    "streaming "
    "playlist-read-private "
    "playlist-read-collaborative "
    "playlist-modify-private "
    "playlist-modify-public "
    "user-follow-modify "
    "user-follow-read "
    "user-library-modify "
    "user-library-read "
    "user-read-email "
    "user-read-private "
    "user-top-read "
    "user-read-recently-played "
    "user-read-playback-position"
)


# Session requests avec retries
session = Session()
retry = Retry(
    total=5,               # nb max de tentatives
    connect=5, read=5,
    backoff_factor=0.5,    # 0.5s, 1s, 2s, ...
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET","POST","PUT","DELETE","HEAD","OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)
session.mount("http://", adapter)

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPES,
    open_browser=True,
    requests_session=session,
    requests_timeout=20     # ⬅️ passe de 5 à 20s
))

me = sp.current_user()
print("Logged in as:", me["display_name"], f"({me['id']})")


