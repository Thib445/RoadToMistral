# RoadToMistral 🎵

A powerful **Spotify Music Management System** built with **FastMCP** that integrates Spotify, Mistral AI, Genius, and Wikipedia APIs to provide intelligent music discovery, playlist management, and comprehensive music information.

## 🌟 Features

### 🎧 Music Management
- **Playlist Operations**: Create, manage, and explore your Spotify playlists
- **Track Discovery**: Find and add songs to playlists with intelligent search
- **Music Playback**: Control Spotify playback directly from the application
- **Blind Test Game**: Interactive music guessing game with random track snippets

### 🤖 AI-Powered Features
- **Smart Recommendations**: Uses Mistral AI to find similar music based on your listening history
- **Custom Playlist Generation**: AI-generated playlists based on mood, activity, or specific queries
- **Intelligent Search**: Enhanced music discovery using AI-powered similarity matching

### 📚 Rich Music Information
- **Comprehensive Song Data**: Combines information from multiple sources
- **Genius Integration**: Access lyrics, song meanings, and artist insights
- **Wikipedia Integration**: Get detailed artist biographies and song background information
- **Spotify Metadata**: Track popularity, duration, album information, and more

### 🔧 Technical Features
- **MCP Server**: Model Context Protocol server for seamless AI integration
- **Robust Authentication**: Secure Spotify OAuth2 integration with comprehensive scopes
- **Error Handling**: Built-in retry mechanisms and graceful error handling
- **Structured Data**: Pydantic models for type-safe data handling

## 🏗️ Architecture

The project is organized into several key modules:

```
src/
├── my_server.py          # Main MCP server with all tools
├── musique.py            # Music track management and playback
├── Playlistlib.py        # Playlist operations and management
├── spotify_infos.py      # Spotify authentication and configuration
├── client_mistral.py     # Mistral AI integration
├── build_custom_playlist.py # AI-powered playlist generation
├── Genius.py             # Genius API integration for lyrics/artists
├── Wikipedia.py          # Wikipedia API integration
└── outdated/             # Legacy code (deprecated)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Spotify Developer Account
- Mistral AI API Key
- Genius API Token (optional, for enhanced features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RoadToMistral
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   # or using uv (recommended)
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   # Spotify Configuration
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIPY_REDIRECT_URI=http://localhost:8080/callback
   
   # Mistral AI Configuration
   MISTRAL_API_KEY=your_mistral_api_key
   
   # Genius Configuration (optional)
   GENIUS_ACCESS_TOKEN=your_genius_token
   ```

4. **Run the MCP server**
   ```bash
   python src/my_server.py
   ```

## 🎯 Available Tools

### Music Discovery & Management
- `musiques_derniere_semaine(username)` - Get recently played tracks and AI-generated similar recommendations
- `getplaylists(limit)` - List your Spotify playlists
- `tracklist_playlist(name)` - Get detailed track information for a specific playlist
- `add2playlist(song_query, playlist_query)` - Add songs to playlists with intelligent matching

### Playlist Creation
- `create_playlist(playlist_name, public, description)` - Create new Spotify playlists
- `build_custom_playlist.py` - AI-powered playlist generation based on queries

### Music Information
- `info_song_or_artist(song_title, artist_name)` - Comprehensive song and artist information from multiple sources

### Entertainment
- `blind_test()` - Interactive music guessing game with random track snippets

## 🔧 Configuration

### Spotify Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Set redirect URI to `http://localhost:8080/callback`
4. Copy Client ID and Client Secret to your `.env` file

### Mistral AI Setup
1. Get your API key from [Mistral AI Console](https://console.mistral.ai/)
2. Add it to your `.env` file

### Genius Setup (Optional)
1. Get your access token from [Genius API](https://genius.com/api-clients)
2. Add it to your `.env` file

## 📖 Usage Examples

### Basic Playlist Management
```python
# Get your playlists
playlists = getplaylists(10)

# Get tracks from a specific playlist
tracks = tracklist_playlist("My Favorites")

# Add a song to a playlist
result = add2playlist("Bohemian Rhapsody", "Rock Classics")
```

### AI-Powered Music Discovery
```python
# Get recent music with AI recommendations
recent_music = musiques_derniere_semaine("your_username")

# Generate custom playlist
from build_custom_playlist import get_musics_from_query
songs = get_musics_from_query("relaxing jazz for studying", 10)
```

### Music Information
```python
# Get comprehensive song information
info = info_song_or_artist("Bohemian Rhapsody", "Queen")
print(info)  # Includes Genius lyrics, Wikipedia info, etc.
```

### Blind Test Game
```python
# Start a blind test game
question = blind_test()
print(question)  # Play 10 seconds of a random liked track
```

## 🛠️ Development

### Code Quality
The project uses several tools for code quality:
- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Pre-commit**: Git hooks for code quality

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
ruff format .
ruff check .
```

## 🔒 Security & Privacy

- All API keys are stored securely in environment variables
- Spotify OAuth2 provides secure authentication
- No sensitive data is logged or stored permanently
- All API calls use HTTPS with proper timeout handling

## 📝 API Scopes

The application requires the following Spotify scopes:
- `user-read-playback-state`
- `user-modify-playback-state`
- `user-read-currently-playing`
- `streaming`
- `playlist-read-private`
- `playlist-modify-private`
- `playlist-modify-public`
- `user-library-read`
- `user-read-recently-played`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Spotify** for the comprehensive music API
- **Mistral AI** for powerful language model capabilities
- **Genius** for rich music metadata and lyrics
- **Wikipedia** for comprehensive artist and song information
- **FastMCP** for the Model Context Protocol framework

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainer.

---

**Made with ❤️ for music lovers and AI enthusiasts**
