from fastmcp import FastMCP
from Playlistlib import *
import musique
 
mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def tracklist_playlist(name: str):
    "gives the tracklist of the playlist that has the name <name>"
    lists = get_playlist_list()
    print(name)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    for playlist in lists:
        print(playlist.name)
        if playlist.name.lower().strip() == name.lower().strip():
            return [song.get_titre() for song in playlist.get_tracks()]
    
if __name__ == "__main__":
    mcp.run()