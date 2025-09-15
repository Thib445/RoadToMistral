import spotipy
from fastmcp import FastMCP
from Playlistlib import *
from Playlistlib import _find_my_playlist_id
from musique import *
from musique import _find_song_id
from typing import Optional, Dict, Any
from spotify_infos import sp, me  # sp = Spotipy auth; me = current_user
import time, sys
from datetime import datetime, timedelta
import random
from client_mistral import llm_trouve_similaires
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import soundfile as sf
import torch
import io, base64
from google.cloud import storage
from datetime import timedelta


mcp = FastMCP("Spotify Manager")

# -------- Cache modèle (Génération de musique)-----------
MODEL_ID = "facebook/musicgen-small"
_processor = None
_model = None

def _load_model_once():
    global _processor, _model
    if _processor is None or _model is None:
        _processor = AutoProcessor.from_pretrained(MODEL_ID)
        _model = MusicgenForConditionalGeneration.from_pretrained(MODEL_ID)
        _model.eval().to("cpu")

# -------- Cache modèle (Génération de musique)-----------


@mcp.tool
def musiques_derniere_semaine(username: str) -> list:
    # Authentification utilisateur avec le scope nécessaire
    une_semaine = datetime.now() - timedelta(days=7)
    recent = sp.current_user_recently_played(limit=50)
    musiques = []
    for item in recent['items']:
        played_at = datetime.strptime(item['played_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if played_at >= une_semaine:
            titre = item['track']['name']
            artiste = item['track']['artists'][0]['name']
            musiques.append(f"{titre} - {artiste}")
    musiques_similaires = llm_trouve_similaires(musiques,  f"Trouve des musiques similaires à celles-ci : {', '.join(musiques)}. Donne-moi seulement les titres et artistes, séparés par des virgules.")
    liste_musiques_similaires = [m.strip() for m in musiques_similaires.split(',')]
    toutes = musiques + liste_musiques_similaires
    random.shuffle(toutes)
    return toutes

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


def upload_base64_to_gcs(b64_data: str, dest_name: str, content_type: str = "application/octet-stream", expires_sec: int = 3600) -> str:
    """
    Décode un base64 et l'upload dans GCS.
    Retourne une URL signée pour télécharger le fichier.
    """
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(dest_name)

    # décoder le base64 en bytes
    file_bytes = base64.b64decode(b64_data)

    # upload depuis mémoire
    blob.upload_from_string(file_bytes, content_type=content_type)

    # générer une URL signée (download direct)
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(seconds=expires_sec),
        method="GET"
    )
    return url

@mcp.tool
def generate_music(user_prompt: str, seconds: int = 10, guidance_scale: float = 3.0):
    """
    Génère un extrait musical avec MusicGen et renvoie un WAV encodé en base64.
    - user_prompt: description du style (ex: "lofi chill with warm piano")
    - seconds: durée approx (5-12s recommandé en CPU)
    - guidance_scale: 2.0–4.0 = contrainte du prompt
    """
    try:
        _load_model_once()

        # approx: ~256 tokens ≈ 5s
        max_new_tokens = max(128, min(1024, int(51.2 * seconds)))

        inputs = _processor(text=[user_prompt], padding=True, return_tensors="pt")
        with torch.inference_mode():
            audio_values = _model.generate(
                **inputs,
                do_sample=True,
                guidance_scale=guidance_scale,
                max_new_tokens=max_new_tokens
            )

        wav = audio_values[0, 0].cpu().numpy()
        sr = _model.config.audio_encoder.sampling_rate

        # Écrire dans un buffer mémoire
        buffer = io.BytesIO()
        sf.write(buffer, wav, sr, format="WAV")
        buffer.seek(0)

        # Encoder en base64
        b64_audio = base64.b64encode(buffer.read()).decode("utf-8")

        url = upload_base64_to_gcs(b64_audio, "test")
        print(url)
        return {
            "status": "ok",
            "prompt": user_prompt,
            "approx_seconds": round(len(wav) / sr, 2),
            "sampling_rate": sr,
            "filename": "musicgen_demo.wav",
            "mimetype": "audio/wav",
            "data_base64": b64_audio
        }
    
    

    except Exception as e:
        return {"status": "error", "message": str(e)}


BUCKET_NAME = "mood2music-uploads"






if __name__ == "__main__":
    mcp.run()