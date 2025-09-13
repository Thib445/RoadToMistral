from fastmcp import FastMCP
from Playlistlib import *
import musique
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_infos import sp, me
from musique import Musique
from datetime import datetime, timedelta
import random
from client_mistral import llm_trouve_similaires




mcp = FastMCP("Spotify Manager")


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




@mcp.tool
def getplaylists(limit):
    """returns the first playlists of the user. Maximum number returned is equal to limit"""
    return [playlist.name for playlist in get_playlist_list(limit=limit)]

@mcp.tool
def tracklist_playlist(name: str):
    "gives the tracklist of the playlist that has the name <name>"
    lists = get_playlist_list()
    for playlist in lists:
        if playlist.name.lower().strip() == name.lower().strip():
            return playlist.get_tracklist_infos()
        

import time
@mcp.tool("blind_test")
def blind_test(track_id: str):
    """
    Lance un blind test Spotify : joue un extrait de 10s d'un morceau choisi au hasard dans la piste donnée.
    Args:
        track_id (str): L’ID Spotify du morceau à utiliser.
    """
    # Récupère la durée du morceau
    track = sp.track(track_id)
    duration_ms = track["duration_ms"]

    # Point de départ aléatoire (évite les 15 premières et 15 dernières secondes)
    start_ms = random.randint(15000, duration_ms - 15000)

    # Démarre la lecture au point choisi
    sp.start_playback(uris=[track["uri"]], position_ms=start_ms)

    # Attend 10 secondes
    time.sleep(10)

    # Met en pause
    sp.pause_playback()

    return f"⏸️ Extrait terminé ! Devinez le titre du morceau ?"


if __name__ == "__main__":
    mcp.run()