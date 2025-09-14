import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_infos import sp, me  # sp = Spotipy auth; me = current_user

class Musique:

    def __init__(self, id, sp=None):
        self.id = id
        self.sp = sp or spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self.info = self.sp.track(self.id)
        self.titre = self.info['name']
        self.artiste = self.info['artists'][0]['name']
        self.album = self.info['album']['name']
        self.duree_ms = self.info['duration_ms']
        self.popularity = self.info['popularity']
        self.type = self.info['type']
    def get_info(self):
        return {
            'titre': self.titre,
            'artiste': self.artiste,
            'album': self.album,
            'duration_ms':self.duree_ms,
            'popularity':self.popularity
        }
    
    def get_popularity(self):
        return self.popularity
    
    def get_duree(self):
        return self.duree_ms // 1000  # Convertir en secondes
    
    def get_type(self):
        return self.type   
    
    def get_id(self):
        return self.id
    
    def get_titre(self):
        return self.titre
    
    def get_artiste(self):
        return self.artiste
    
def _find_song_id(query, market = None):
        res = sp.search(q=query, limit=1, type="track", market=market)
        items = res.get("tracks", {}).get("items", []) or []
        return items[0]["id"] if items else None