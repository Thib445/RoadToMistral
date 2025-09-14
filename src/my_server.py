from fastmcp import FastMCP

from Playlistlib import _find_my_playlist_id, get_playlist_list
from musique import _find_song_id, random_liked_track, lancer_musique
from typing import Optional, Dict, Any
from spotify_infos import sp, me 
import time, sys
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

BLIND_TEST_INSTRUCTION_TEMPLATE="""
You are organising a blind test for the user. You juste ran the music and you must ask the user to guess the title and artist of the music. 
The we answer is {answer} but you must not tell him unless he asks you to.
write a good question to the user to make him guess the title and artist of the music.
"""
@mcp.tool("blind_test")
def blind_test() :
    """
    Lance un blind test Spotify : joue un extrait de 10s d'un morceau choisi au hasard dans la piste donnée.
    Args:
        track_id (str): L’ID Spotify du morceau à utiliser.
    """
    # Récupère la durée du morceau
    query = random_liked_track()
    track_id = _find_song_id(query)
    track = sp.track(track_id)
    duration_ms = track["duration_ms"]

    #devices = sp.devices()["devices"]

    #device_id = devices[0]["id"]
    # Point de départ aléatoire (évite les 15 premières et 15 dernières secondes)
    start_ms = random.randint(15000, duration_ms - 15000)

    # Démarre la lecture au point choisi
    lancer_musique(track_id, position_ms=start_ms)
    # Attend 10 secondes
    time.sleep(10)

    # Met en pause
    sp.pause_playback()

    return BLIND_TEST_INSTRUCTION_TEMPLATE.format(answer=query)


@mcp.tool
def create_playlist(playlist_name: str, public: bool = False, description: str = "Playlist generated according to your mood!") -> Dict[str, Any]:
    """
    Create a new playlist in the connected user's account.
    Scopes: playlist-modify-private (and/or playlist-modify-public)
    """
    playlist = sp.user_playlist_create(user=me["id"], name=playlist_name, public=public, description=description)
    return {
        "status": "created",
        "playlist_id": playlist["id"],
        "playlist_url": playlist["external_urls"]["spotify"],
        "name": playlist_name,
        "public": public,
    }

@mcp.tool
def add2playlist(song_query: str, playlist_query: str, allow_duplicates: bool = True, market: Optional[str] = "from_token") -> Dict[str, Any]:
    """
    Find best match for 'song_query' and add it to YOUR playlist whose name contains 'playlist_query'.
    Scopes: playlist-read-private + playlist-modify-private (or public)
    """    

    song_id = _find_song_id(song_query, market=market)
    if not song_id:
        return {"status": "not_found", "entity": "track", "query": song_query}

    playlist_id = _find_my_playlist_id(playlist_query)
    if not playlist_id:
        return {"status": "not_found", "entity": "playlist", "query": playlist_query}

    track_uri = f"spotify:track:{song_id}"

    if not allow_duplicates:
        items = sp.playlist_items(playlist_id, limit=100).get("items", [])
        if any(track_uri == (it.get("track") or {}).get("uri") for it in items):
            return {"status": "skipped", "reason": "duplicate", "playlist_id": playlist_id, "track_uri": track_uri}

    sp.playlist_add_items(playlist_id, [track_uri])
    pl = sp.playlist(playlist_id, fields="name,external_urls.spotify")
    return {"status": "added", "playlist_id": playlist_id, "playlist_name": pl["name"], "playlist_url": pl["external_urls"]["spotify"], "track_uri": track_uri}

if __name__ == "__main__":
    mcp.run()