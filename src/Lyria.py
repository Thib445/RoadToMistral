import sys
print(sys.executable)  # Check which Python interpreter is being used


import os
import google.generativeai as genai

# 1. Configure API key (put it in your .env for safety)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Pick the music model (Lyria)
model = genai.GenerativeModel("models/music-lm-1.0")

# 3. Generate music
prompt = "A calm lo-fi beat with piano and soft rain sounds"
response = model.generate_content(
    prompt,
    generation_config={
        "audio_format": "wav",    # wav or mp3
        "duration_seconds": 30    # length of generated track
    }
)

# 4. Save audio to file
with open("generated_song.wav", "wb") as f:
    f.write(response.candidates[0].content[0].binary.data)
print("✅ Song saved as generated_song.wav")
