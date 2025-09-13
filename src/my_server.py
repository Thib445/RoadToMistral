from fastmcp import FastMCP
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_infos import sp, me
import musique.py



mcp = FastMCP("Spotify Manager")

@mcp.tool
def derniere_musique(username: str) -> str:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    # Récupère les 1 dernières musiques du user (nécessite l'API utilisateur, pas juste ClientCredentials)
    recent = sp.current_user_recently_played(limit=1)
    if recent == None:
        return "Aucune musique récemment écoutée."
    
    last_music = musique(recent,sp)
    titre = last_music.get_titre()
    artiste = last_music.get_artiste()
    return f"{titre} - {artiste}"




if __name__ == "__main__":
    mcp.run()