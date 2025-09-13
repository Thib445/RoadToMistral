import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load your .env file
load_dotenv()
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

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=scopes
))

class Playlist():
    def __init__(self,dico):
        self.eternal_url = dico["external_urls"]["spotify"]
        self.id = dico["id"]
        self.name = dico["name"]

    def get_tracks(self):
        return 0
    
    def pr(self):
        print(self.eternal_url)
        print(self.name)

def get_last_playlist(limit_plays: int = 50):
    """
    Returns (playlist_name, playlist_url, playlist_id) for the most recent playlist
    found in your recently played items. Returns None if none found.
    """
    history = sp.current_user_recently_played(limit=min(50, max(1, limit_plays)))
    for item in history.get("items", []):
        ctx = item.get("context")
        if not ctx:
            continue
        if ctx.get("type") == "playlist" and ctx.get("uri"):
            # context URI looks like "spotify:playlist:<id>"
            pl_id = ctx["uri"].split(":")[-1]
            pl = sp.playlist(pl_id, fields="name,external_urls.spotify,id")
            return pl["name"], pl["external_urls"]["spotify"], pl["id"]
    return None

import json

def get_playlist_list():
    currentUserPlaylists = []
    current_user_playlst = sp.current_user_playlists(limit=50,offset=0).get("items",[])
    if current_user_playlst != []:
        for playlist in current_user_playlst:
            currentUserPlaylists.append(Playlist(playlist))
    return currentUserPlaylists

get_playlist_list()[0].pr()



