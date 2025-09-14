from fastmcp import FastMCP

from Playlistlib import _find_my_playlist_id, get_playlist_list
from musiqueLib import _find_song_id, random_liked_track, lancer_musique
from typing import Optional, Dict, Any
from spotify_infos import sp, me
import time, sys
from datetime import datetime, timedelta
import random
from client_mistral import llm_trouve_similaires

from Wikipedia import wikipedia_artist_info, wikipedia_song_info
from Genius import genius_formatted_info

mcp = FastMCP("My MCP Server")
print(
    f"[MCP boot] spotify_connector starting at {time.strftime('%H:%M:%S')} | file={__file__}",
    file=sys.stderr,
)

mcp = FastMCP("Spotify Manager")


@mcp.tool
def musiques_derniere_semaine(username: str) -> list:
    # Authentification utilisateur avec le scope nécessaire
    une_semaine = datetime.now() - timedelta(days=7)
    recent = sp.current_user_recently_played(limit=50)
    musiques = []
    for item in recent["items"]:
        played_at = datetime.strptime(item["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if played_at >= une_semaine:
            titre = item["track"]["name"]
            artiste = item["track"]["artists"][0]["name"]
            musiques.append(f"{titre} - {artiste}")
    musiques_similaires = llm_trouve_similaires(
        musiques,
        f"Trouve des musiques similaires à celles-ci : {', '.join(musiques)}. Donne-moi seulement les titres et artistes, séparés par des virgules.",
    )
    liste_musiques_similaires = [m.strip() for m in musiques_similaires.split(",")]
    toutes = musiques + liste_musiques_similaires
    random.shuffle(toutes)
    return toutes


@mcp.tool
def getplaylists(limit: int) -> list:
    """Get a list of the user's Spotify playlists. Returns the first N playlists where N is the limit parameter.
    Each item in the returned list is a playlist name string."""
    return [playlist.name for playlist in get_playlist_list(limit=limit)]


@mcp.tool
def tracklist_playlist(name: str) -> list:
    """Get the tracklist (list of songs) for a specific Spotify playlist by name.
    Searches through the user's playlists to find one matching the provided name (case-insensitive).
    Returns detailed information about each track in the playlist including song title, artist, and other metadata."""
    lists = get_playlist_list()
    for playlist in lists:
        if playlist.name.lower().strip() == name.lower().strip():
            return playlist.get_tracklist_infos()


import time

BLIND_TEST_INSTRUCTION_TEMPLATE = """
You are organising a blind test for the user. You juste ran the music and you must ask the user to guess the title and artist of the music. 
The we answer is {answer} but you must not tell him unless he asks you to.
write a good question to the user to make him guess the title and artist of the music.
"""


@mcp.tool("blind_test")
def blind_test():
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

    # devices = sp.devices()["devices"]

    # device_id = devices[0]["id"]
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
def create_playlist(
    playlist_name: str,
    public: bool = False,
    description: str = "Playlist generated according to your mood!",
) -> Dict[str, Any]:
    """
    Create a new playlist in the connected user's account.
    Scopes: playlist-modify-private (and/or playlist-modify-public)
    """
    playlist = sp.user_playlist_create(
        user=me["id"], name=playlist_name, public=public, description=description
    )
    return {
        "status": "created",
        "playlist_id": playlist["id"],
        "playlist_url": playlist["external_urls"]["spotify"],
        "name": playlist_name,
        "public": public,
    }


@mcp.tool
def add2playlist(
    song_query: str,
    playlist_query: str,
    allow_duplicates: bool = True,
    market: Optional[str] = "from_token",
) -> Dict[str, Any]:
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
            return {
                "status": "skipped",
                "reason": "duplicate",
                "playlist_id": playlist_id,
                "track_uri": track_uri,
            }

    sp.playlist_add_items(playlist_id, [track_uri])
    pl = sp.playlist(playlist_id, fields="name,external_urls.spotify")
    return {
        "status": "added",
        "playlist_id": playlist_id,
        "playlist_name": pl["name"],
        "playlist_url": pl["external_urls"]["spotify"],
        "track_uri": track_uri,
    }


@mcp.tool
def info_song_or_artist(song_title: str, artist_name: str) -> str:
    """Get comprehensive information about a song by combining data from Wikipedia and Genius.
    Provides detailed song information including lyrics context, artist biography, album details, and general background.
    Returns formatted information from both sources for a complete overview of the song and artist."""

    result = f"🎵 **{song_title}** by **{artist_name}**\n\n"

    # Get Genius information
    result += genius_formatted_info(song_title, artist_name)

    # Get Wikipedia information
    result += wikipedia_artist_info(artist_name) + "\n"
    result += wikipedia_song_info(song_title, artist_name)

    return result


@mcp.tool
def info_song_or_artist(song_title: str, artist_name: str) -> str:
    """Get comprehensive information about a song by combining data from Wikipedia and Genius.
    Provides detailed song information including lyrics context, artist biography, album details, and general background.
    Returns formatted information from both sources for a complete overview of the song and artist."""

    result = f"🎵 **{song_title}** by **{artist_name}**\n\n"

    # Get Genius information
    result += genius_formatted_info(song_title, artist_name)

    # Get Wikipedia information
    result += wikipedia_artist_info(artist_name) + "\n"
    result += wikipedia_song_info(song_title, artist_name)

    return result


if __name__ == "__main__":
    mcp.run()
