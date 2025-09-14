# minimal Genius test — requires python-dotenv and requests; put GENIUS_ACCESS_TOKEN in your .env
from dotenv import load_dotenv
import os, requests

load_dotenv()
token = os.environ["GENIUS_ACCESS_TOKEN"]


def genius_song_info(title: str):
    # Step 1: search for the title
    search = requests.get(
        "https://api.genius.com/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": title},
        timeout=10,
    )
    search.raise_for_status()
    hits = search.json().get("response", {}).get("hits", [])
    if not hits:
        return None

    # Step 2: take the first hit and fetch /songs/{id}
    song_id = hits[0]["result"]["id"]
    song = requests.get(
        f"https://api.genius.com/songs/{song_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    song.raise_for_status()
    return song.json().get("response", {}).get("song", {})


# Example usage:
""" info = genius_song_info("Bohemian Rhapsody")
print("Title:", info.get("full_title"))
print("Artist:", info.get("primary_artist", {}).get("name"))
print("Release date:", info.get("release_date"))
print("Pageviews:", info.get("stats", {}).get("pageviews"))
print("URL:", info.get("url")) """

headers = {"Authorization": f"Bearer {token}"}


def genius_full_info(title: str, artist: str):
    # 1) Search for song
    q = f"{title} {artist}"
    search = requests.get(
        "https://api.genius.com/search", headers=headers, params={"q": q}, timeout=10
    )
    search.raise_for_status()
    hits = search.json().get("response", {}).get("hits", [])
    if not hits:
        return None

    # 2) Take first hit → get full song info
    song_id = hits[0].get("result", {}).get("id")
    if not song_id:
        return None
    song_resp = requests.get(
        f"https://api.genius.com/songs/{song_id}", headers=headers, timeout=10
    )
    song_resp.raise_for_status()
    song = song_resp.json().get("response", {}).get("song", {})

    # 3) Extract artist info
    artist_id = song.get("primary_artist", {}).get("id")
    artist_info = {}
    if artist_id:
        artist_resp = requests.get(
            f"https://api.genius.com/artists/{artist_id}", headers=headers, timeout=10
        )
        if artist_resp.status_code == 200:
            artist_info = artist_resp.json().get("response", {}).get("artist", {})

    # 4) Extract album info if available
    album_info = None
    album_id = song.get("album", {}).get("id")
    if album_id:
        album_resp = requests.get(
            f"https://api.genius.com/albums/{album_id}", headers=headers, timeout=10
        )
        if album_resp.status_code == 200:
            album_info = album_resp.json().get("response", {}).get("album", {})

    return {
        "song": {
            "title": song.get("full_title") or "",
            "url": song.get("url") or "",
            "description": (song.get("description", {}) or {}).get("plain") or "",
            "pageviews": (song.get("stats", {}) or {}).get("pageviews"),
            "annotation_count": song.get("annotation_count"),
            "album": song.get("album", {}).get("name") if song.get("album") else None,
        },
        "artist": {
            "name": artist_info.get("name") or "",
            "bio": (artist_info.get("description", {}) or {}).get("plain") or "",
            "url": artist_info.get("url") or "",
            "image": artist_info.get("image_url") or "",
        },
        "album": {
            "name": album_info.get("name") if album_info else None,
            "url": album_info.get("url") if album_info else None,
            "release_date": album_info.get("release_date") if album_info else None,
            "cover_art_url": album_info.get("cover_art_url") if album_info else None,
        }
        if album_info
        else None,
    }


def genius_formatted_info(song_title: str, artist_name: str) -> str:
    """Get formatted Genius information for a song"""
    info = genius_full_info(song_title, artist_name)
    if not info:
        return "❌ No Genius information found for this song.\n"

    song = info.get("song", {})
    artist = info.get("artist", {})
    album = info.get("album")

    result = ""

    # Song information
    result += "🎤 **Song Details:**\n"
    result += f"   • Title: {song.get('title', 'N/A')}\n"
    result += (
        f"   • Pageviews: {song.get('pageviews', 'N/A'):,}\n"
        if song.get("pageviews")
        else "   • Pageviews: N/A\n"
    )
    result += f"   • Annotations: {song.get('annotation_count', 'N/A')}\n"
    if song.get("album"):
        result += f"   • Album: {song.get('album')}\n"
    if song.get("url"):
        result += f"   • Genius URL: {song.get('url')}\n"
    if song.get("description"):
        result += f"   • Description: {song.get('description')[:300]}...\n"
    result += "\n"

    # Artist information
    if artist.get("name"):
        result += "👩‍🎤 **Artist Information:**\n"
        result += f"   • Name: {artist.get('name')}\n"
        if artist.get("bio"):
            result += f"   • Bio: {artist.get('bio')[:300]}...\n"
        if artist.get("url"):
            result += f"   • Genius URL: {artist.get('url')}\n"
        result += "\n"

    # Album information
    if album:
        result += "💿 **Album Information:**\n"
        result += f"   • Name: {album.get('name', 'N/A')}\n"
        if album.get("release_date"):
            result += f"   • Release Date: {album.get('release_date')}\n"
        if album.get("url"):
            result += f"   • Album URL: {album.get('url')}\n"
        result += "\n"

    return result


# Example usage:
info = genius_full_info("Djaja", "Aya Nakamura")

print("🎵 Song:", info["song"]["title"])
print("   URL:", info["song"]["url"])
print("   Pageviews:", info["song"]["pageviews"])
print("   Annotations:", info["song"]["annotation_count"])
print()
print("👩 Artist:", info["artist"]["name"])
print("   URL:", info["artist"]["url"])
print("   Bio:", info["artist"]["bio"][:500], "...")
print()
if info["album"]:
    print("💿 Album:", info["album"]["name"])
    print("   Released:", info["album"]["release_date"])
    print("   URL:", info["album"]["url"])
