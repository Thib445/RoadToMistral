from fastmcp import FastMCP
from Playlistlib import *
import musique
 
mcp = FastMCP("My MCP Server")

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

if __name__ == "__main__":
    mcp.run()