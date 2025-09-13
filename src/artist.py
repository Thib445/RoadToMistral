import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Artist:

    def __init__(self, id, sp=None):
        self.id = id
        self.sp = sp or spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self.info = self.sp.artist(self.id)
        self.name = self.info['name']
        self.followers = self.info["followers"]["total"]
        self.genres = self.info['genres']
        self.popularity = self.info['popularity']
        self.type = self.info['type']



    def get_info(self):
        return {
            'name': self.name,
            'genres': self.genres,
            'followers': self.followers,
            'popularity': self.popularity,
        }
    
    def get_name(self):
        return self.name
    
    def get_genres(self):
        return self.genres
    
    def get_followers(self):   
        return self.followers
    
    def get_popularity(self):
        return self.popularity
    
    def get_id(self):
        return self.id
    
    def is_artiste(self):
        return self.artiste == 'artist'
    
    def get_similar_artists(self):
        results = self.sp.artist_related_artists(self.id)
        similar_artists = []
        for artist in results['artists']:
            similar_artists.append(artist['name'])
        return similar_artists
    
