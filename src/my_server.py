from fastmcp import FastMCP
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_infos import sp, me
from musique import Musique
from datetime import datetime, timedelta
import random
from client_mistral import llm_trouve_similaires




mcp = FastMCP("Spotify Manager")
"""
@mcp.tool
def derniere_musique(username: str) -> str:
    # Récupère les 1 dernières musiques du user (nécessite l'API utilisateur, pas juste ClientCredentials)
    recent = sp.current_user_recently_played(limit=1)
    if recent == None:
        return "Aucune musique récemment écoutée."
    
    last_music = musique(recent,sp)
    titre = last_music.get_titre()
    artiste = last_music.get_artiste()
    return f"{titre} - {artiste}"""

@mcp.tool
def musiques_derniere_semaine(username: str) -> list:
    # Authentification utilisateur avec le scope nécessaire
    une_semaine = datetime.now() - timedelta(days=7)
    recent = sp.current_user_recently_played(limit=50)
    musiques = []
    for item in recent['items']:
        played_at = datetime.strptime(item['played_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if played_at >= une_semaine:
            titre = item['track']['name']
            artiste = item['track']['artists'][0]['name']
            musiques.append(f"{titre} - {artiste}")
    musiques_similaires = llm_trouve_similaires(musiques,  f"Trouve des musiques similaires à celles-ci : {', '.join(musiques)}. Donne-moi seulement les titres et artistes, séparés par des virgules.")
    liste_musiques_similaires = [m.strip() for m in musiques_similaires.split(',')]
    toutes = musiques + liste_musiques_similaires
    random.shuffle(toutes)
    return toutes





if __name__ == "__main__":
    mcp.run()