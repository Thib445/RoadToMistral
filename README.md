# RoadToMistral Music Tooling 🎵

**An AI-powered Spotify assistant** that helps you discover music, manage playlists, and learn about songs using Mistral AI, Genius, and Wikipedia.

## What This Does

This tool connects to your Spotify account and uses AI to:

- **Find similar music** to what you've been listening to
- **Create smart playlists** based on your mood or requests
- **Play music games** like blind tests
- **Get detailed song info** including lyrics, artist stories, and background
- **Manage your playlists** - add songs, create new ones, explore tracks

## Key Features

### 🎧 Music Control

- Play any song from your Spotify account
- Create and manage playlists
- Add songs to playlists by name
- Get your recent listening history

### 🤖 AI Magic

- **Smart recommendations**: "Find songs like what I listened to this week"
- **Custom playlists**: "Make a playlist for studying" or "Songs for a workout"
- **Music discovery**: AI finds similar tracks you might like

### 📚 Song Information

- **Lyrics and meanings** from Genius
- **Artist biographies** from Wikipedia
- **Song background** and release information
- **Track details** like popularity and duration

### 🎮 Fun Features

- **Blind test game**: Play 10 seconds of a random song and guess what it is
- **Music trivia**: Learn interesting facts about songs and artists

## How It Works

The app is built as an **MCP (Model Context Protocol) server** that connects different services:

- **Spotify API**: Controls your music and playlists
- **Mistral AI**: Finds similar songs and creates smart recommendations
- **Genius API**: Gets lyrics and song meanings
- **Wikipedia API**: Provides artist biographies and song background

When you ask for something like "find songs like what I listened to this week", the AI analyzes your recent music and suggests similar tracks.

## Setup (5 minutes)

### What You Need

- Python 3.12+
- Spotify account
- Mistral AI API key
- Genius API token (optional)

### Step 1: Get API Keys

**Spotify:**

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create new app → Copy Client ID & Secret
3. Set redirect URI to: `http://localhost:8080/callback`

**Mistral AI:**

1. Get API key from [Mistral Console](https://console.mistral.ai/)

**Genius (optional):**

1. Get token from [Genius API](https://genius.com/api-clients)

### Step 2: Install & Configure

```bash
# Clone and install
git clone <repository-url>
cd RoadToMistral
pip install -e .

# Create .env file with your keys
echo "SPOTIPY_CLIENT_ID=your_spotify_client_id" > .env
echo "SPOTIPY_CLIENT_SECRET=your_spotify_client_secret" >> .env
echo "SPOTIPY_REDIRECT_URI=http://localhost:8080/callback" >> .env
echo "MISTRAL_API_KEY=your_mistral_api_key" >> .env
echo "GENIUS_ACCESS_TOKEN=your_genius_token" >> .env

# Run the server
python src/my_server.py
```

## What You Can Do

Once running, you can use these commands:

### 🎵 Music Discovery

- **Get similar songs**: "Find music like what I listened to this week"
- **Create playlists**: "Make a workout playlist" or "Songs for studying"
- **Add songs**: "Add Bohemian Rhapsody to my Rock playlist"

### 📋 Playlist Management

- **List playlists**: See all your Spotify playlists
- **View tracks**: Get all songs in a specific playlist
- **Create new**: Make new playlists with custom names

### 🎮 Fun & Games

- **Blind test**: Play 10 seconds of a random song and guess what it is
- **Song info**: Get lyrics, artist biography, and song background

### 📊 Music Data

- **Recent tracks**: See what you've been listening to
- **Song details**: Popularity, duration, album info
- **Artist info**: Biographies and background from Wikipedia

## Example Usage

### Get AI Music Recommendations

```python
# Find songs similar to what you listened to this week
recent_music = musiques_derniere_semaine("your_username")
# Returns: ["Bohemian Rhapsody - Queen", "Hotel California - Eagles", ...]
```

### Create Smart Playlists

```python
# Generate playlist based on mood/activity
from build_custom_playlist import get_musics_from_query
songs = get_musics_from_query("relaxing jazz for studying", 10)
# AI finds 10 jazz songs perfect for studying
```

### Get Song Information

```python
# Get comprehensive info about a song
info = info_song_or_artist("Bohemian Rhapsody", "Queen")
# Returns: Lyrics from Genius + Artist bio from Wikipedia + Spotify data
```

### Play Music Games

```python
# Start a blind test
question = blind_test()
# Plays 10 seconds of a random song, asks you to guess
```

## Troubleshooting

**"Authentication failed"**: Check your Spotify API keys in `.env`
**"No playlists found"**: Make sure you have playlists in your Spotify account
**"AI not working"**: Verify your Mistral API key is correct

## Privacy & Security

- API keys stored in `.env` file (never committed)
- Spotify OAuth2 for secure authentication
- No personal data stored permanently
- All API calls use HTTP
