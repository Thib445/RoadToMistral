from fastmcp import FastMCP
from spotify_infos import sp, me  # sp = Spotipy auth; me = current_user
from typing import Optional, Dict, Any
from build_custom_playlist import get_musics_from_query, create_playlist_description, create_playlist_name

mcp = FastMCP("spotify_connector")

# --- LOG au démarrage pour vérifier qu'on lance bien ce fichier ---
import time, sys



#@mcp.tool
def generateMoodBasedPlaylist(features: str, k: int = 15, public: bool = False):
    Songs = get_musics_from_query(features, k)
    title, description = create_playlist_name(features), create_playlist_description(features)
    print(f"[GenerateMoodBasedPlaylist] Creating playlist '{title}' with {len(Songs.morceaux)} songs...", file=sys.stderr)
    sp.user_playlist_create(user=me["id"], name=title, public=public, description=description)


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
    
    for song in Songs.morceaux:
        song_id = _find_song_id(song, market="US")
        print(f"Song ID: {song_id}", file=sys.stderr)
        if not song_id:
            return {"status": "not_found", "entity": "track", "query": song}

        playlist_id = _find_my_playlist_id(title)
        if not playlist_id:
            return {"status": "not_found", "entity": "playlist", "query": title}

        track_uri = f"spotify:track:{song_id}"

        sp.playlist_add_items(playlist_id, [track_uri])


        
generateMoodBasedPlaylist("Rap américain des années 90", k=10, public=False)

