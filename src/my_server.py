from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")




@mcp.tool
def get_artist_info(artist_name: str) -> dict:
    from artist import artist
    from get_id import search_id
    artist_id = search_id(artist_name, type='artist')
    if artist_id:
        info = artist(artist_id).get_info()
        return info

    
if __name__ == "__main__":
    mcp.run()