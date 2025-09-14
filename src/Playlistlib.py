import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from musiqueLib import Musique
from spotify_infos import sp, me  # sp = Spotipy auth; me = current_user


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

def _find_my_playlist_id(query):    
    res = sp.current_user_playlists(limit=50)
    for pl in res.get("items", []):
        name = (pl.get("name") or "").lower()
        if query.lower() in name and pl.get("owner", {}).get("id") == me["id"]:
            return pl["id"]
    return None
