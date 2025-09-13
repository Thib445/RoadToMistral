import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotify_infos

def search_id(query, type = 'track', sp=None):
    results = sp.search(q = query, limit=1, type = type)
    id = results[type + 's']['items'][0]['id']
    return id

if __name__ == "__main__":
    print(search_id("Justin Bieber", type='artist', sp=spotify_infos.sp))
    print(search_id("Afro Trap", type='track', sp=spotify_infos.sp))