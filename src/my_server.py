from fastmcp import FastMCP
import spotify_infos

mcp = FastMCP("My MCP Server")




@mcp.tool
def get_artist_info(artist_name: str) -> dict:
    from artist import artist
    from get_id import search_id
    sp = spotify_infos.sp
    artist_id = search_id(artist_name, type='artist', sp=sp)
    if artist_id:
        info = artist(artist_id).get_info()
        return info

    
if __name__ == "__main__":
    mcp.run()