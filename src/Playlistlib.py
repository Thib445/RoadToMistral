import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from musique import Musique

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
        self.track_list = []
        
    def get_tracks(self):
        track_list = [
            Musique(i["track"]["id"],sp=sp) 
            for i in sp.playlist_items(self.id).get("items",[])
        ]
        self.track_list = track_list
        return self.track_list
    
    def get_tracklist_infos(self):
        if self.track_list:
            return [music.get_info() for music in self.track_list]
        else:
            self.track_list = self.get_tracks()
            return [music.get_info() for music in self.track_list]
        
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
        
def get_playlist_list(limit = 50)-> list[Playlist]:
    currentUserPlaylists = []
    current_user_playlst = sp.current_user_playlists(limit=limit,offset=0).get("items",[])
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

"""or i in get_playlist_list():
    if i.name == "Rap lyrique ":
        print(" jn")
        i.get_tracks()"""




