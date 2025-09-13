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
    def __init__(self,id):
        playlist = sp.playlist(id)
        self.eternal_url = playlist["external_urls"]["spotify"]
        self.id = playlist["id"]
        self.name = playlist["name"]

    def get_tracks(self):
        return 0
    
    def pr(self):
        print(self.eternal_url)
        print(self.name)

    def getPlaylistDuration(self):
        total_ms = 0
        results = sp.playlist_items(self.id, fields="items.track.duration_ms,next", additional_types=["track"])
        
        while results:
            for item in results["items"]:
                track = item.get("track")
                if track and track.get("duration_ms"):
                    total_ms += track["duration_ms"]
            
            if results.get("next"):
                results = sp.next(results)
            else:
                results = None
                
        self.duration = total_ms
        
def get_playlist_list():
    currentUserPlaylists = []
    current_user_playlst = sp.current_user_playlists(limit=50,offset=0).get("items",[])
    if current_user_playlst != []:
        for playlist in current_user_playlst:
            currentUserPlaylists.append(Playlist(playlist["id"]))
    return currentUserPlaylists

def get_last_listened_playlist(limit_plays = 100):
    history = sp.current_user_recently_played(limit=min(50, max(1, limit_plays)))
    for item in history.get("items", []):
        ctx = item.get("context")
        if not ctx:
            continue
        if ctx.get("type") == "playlist" and ctx.get("uri"):
            
            return Playlist(ctx["external_urls"]["spotify"])
    return None

get_last_listened_playlist().pr()



