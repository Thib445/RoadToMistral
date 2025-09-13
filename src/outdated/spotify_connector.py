from fastmcp import FastMCP
from spotify_infos import sp, me  # sp = Spotipy auth; me = current_user
from typing import Optional, Dict, Any

mcp = FastMCP("spotify_connector")

# --- LOG au démarrage pour vérifier qu'on lance bien ce fichier ---
import time, sys
print(f"[MCP boot] spotify_connector starting at {time.strftime('%H:%M:%S')} | file={__file__}", file=sys.stderr)


# ---------------------------
# Tools
# ---------------------------

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
    def _find_song_id(query: str, market: Optional[str] = None) -> Optional[str]:
        res = sp.search(q=query, limit=1, type="track", market=market)
        items = res.get("tracks", {}).get("items", []) or []
        return items[0]["id"] if items else None


    def _find_my_playlist_id(query: str) -> Optional[str]:
        res = sp.current_user_playlists(limit=50)
        for pl in res.get("items", []):
            name = (pl.get("name") or "").lower()
            if query.lower() in name and pl.get("owner", {}).get("id") == me["id"]:
                return pl["id"]
        return None
    

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
    # Petit log de la liste des tools enregistrés
    """try:
        # FastMCP expose généralement mcp.tools (dict nom->callable). Ajuste si différent.
        tool_names = list(getattr(mcp, "tools", {}).keys())
        print(f"[MCP boot] registered tools: {tool_names}", file=sys.stderr)
    except Exception as e:
        print(f"[MCP boot] couldn't list tools: {e}", file=sys.stderr)

    print("[MCP] tools:", list(getattr(mcp, "tools", {}).keys()), flush=True)
    """
    mcp.run()


# from fastmcp import FastMCP
# from spotify_infos import sp, me
# from spotipy import Spotify
# import re
# from typing import Optional, Literal, Dict, Any, List

# mcp = FastMCP("spotify_connector")

# @mcp.tool
# # --- trouver un titre précis ---
# def create_playlist(playlist_name : str):
#     """
#     Crée une nouvelle playlist dans TON compte.
#     """
#     playlist = sp.user_playlist_create(
#         user=me["id"], 
#         name=playlist_name,
#         public=False,
#         description="Playlist generated qccording to your mood !"
#     )
#     return (f"I created the playlist {playlist_name} according to your mood !", "Here is the playlist link:", playlist["external_urls"]["spotify"])

# # --- ajouter un titre précis à une playlist ---
# def findsongID(query : str, type = 'track'):
#     results = sp.search(q = query, limit=1, type = type)
#     song_id = results[type + 's']['items'][0]['id']
#     return song_id

# def findplaylistID(query : str, type = 'playlist'):
#     results = sp.current_user_playlists(limit=50)
#     for pl in results["items"]:
#         if query.lower() in pl["name"].lower():
#             return pl["id"]

# @mcp.tool  
# def add2playlist(query_song : str, query_playlist : str, type = 'track'):
#     """
#     Ajoute le meilleur résultat de 'song_query' à la première de TES playlists qui contient 'playlist_query' dans son nom.
#     """
#     song_id, playlist_id = findsongID(query_song), findplaylistID(query_playlist)
#     sp.playlist_add_items(playlist_id, [f"spotify:track:{song_id}"])
#     return (f"I added {query_song} to your playlist {query_playlist} !")

# if __name__ == "__main__":
#     mcp.run()