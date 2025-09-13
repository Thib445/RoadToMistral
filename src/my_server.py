from fastmcp import FastMCP
from Playlistlib import *
from Playlistlib import _find_my_playlist_id
from musique import *
from musique import _find_song_id
from typing import Optional, Dict, Any
from spotify_infos import sp, me  # sp = Spotipy auth; me = current_user
import time, sys

mcp = FastMCP("My MCP Server")
print(f"[MCP boot] spotify_connector starting at {time.strftime('%H:%M:%S')} | file={__file__}", file=sys.stderr)

@mcp.tool
def dezjio(name: str) -> str:
    return f"Hello, {name}!"

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