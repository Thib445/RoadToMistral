import requests
import urllib.parse

def wikipedia_summary(query: str, lang: str = "en"):
    """Get Wikipedia summary for a query"""
    headers = {'User-Agent': 'EloanMCP/1.0'}
    
    # Search for the page
    search_url = f"https://{lang}.wikipedia.org/w/api.php"
    search_params = {
        "action": "query", "format": "json", "list": "search",
        "srsearch": query, "srlimit": 1
    }
    
    try:
        # Find page
        search_resp = requests.get(search_url, params=search_params, headers=headers, timeout=10)
        search_data = search_resp.json()
        
        if not search_data.get("query", {}).get("search"):
            return {"title": "", "url": "", "summary": "No results found"}
        
        page_title = search_data["query"]["search"][0]["title"]
        
        # Get summary
        summary_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(page_title)}"
        summary_resp = requests.get(summary_url, headers=headers, timeout=10)
        
        if summary_resp.status_code == 200:
            data = summary_resp.json()
            return {
                "title": data.get("title", ""),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                "summary": data.get("extract", ""),
            }
        else:
            return {"title": "", "url": "", "summary": f"Error: {summary_resp.status_code}"}
            
    except Exception as e:
        return {"title": "", "url": "", "summary": f"Error: {str(e)}"}

def wikipedia_artist_info(artist_name: str) -> str:
    """Get formatted Wikipedia information for an artist"""
    info = wikipedia_summary(artist_name)
    if not info.get("title"):
        return "❌ No Wikipedia information found for this artist."
    
    result = "📖 **Artist Wikipedia Information:**\n"
    result += f"   • Title: {info.get('title')}\n"
    result += f"   • Summary: {info.get('summary', '')[:400]}...\n"
    if info.get('url'):
        result += f"   • Wikipedia URL: {info.get('url')}\n"
    return result

def wikipedia_song_info(song_title: str, artist_name: str) -> str:
    """Get formatted Wikipedia information for a song"""
    info = wikipedia_summary(f"{song_title} {artist_name}")
    if not info.get("title"):
        return "❌ No Wikipedia information found for this song."
    
    result = "🎵 **Song Wikipedia Information:**\n"
    result += f"   • Title: {info.get('title')}\n"
    result += f"   • Summary: {info.get('summary', '')[:400]}...\n"
    if info.get('url'):
        result += f"   • Wikipedia URL: {info.get('url')}\n"
    return result

# Example usage
if __name__ == "__main__":
    info = wikipedia_summary("Aya Nakamura")
    print("📖", info["title"] or "No title")
    print("📄", (info["summary"][:1000] or "No summary") + "...")