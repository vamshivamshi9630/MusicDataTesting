# -*- coding: utf-8 -*-
import os
import json

try:
    from urllib import quote  # Python 2
except ImportError:
    from urllib.parse import quote  # Python 3

BASE_URL = "https://github.com/vamshivamshi9630/MusicData/raw/refs/heads/main/"
OUTPUT_FILE = "songs.json"

# Load existing data if available
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r") as f:
        try:
            existing_songs = json.load(f)
        except json.JSONDecodeError:
            existing_songs = []
else:
    existing_songs = []

def is_duplicate(song_name, album_name):
    for song in existing_songs:
        if song["name"] == song_name and song["album"] == album_name:
            return True
    return False

new_songs = []

# Go through each album folder
for album_folder in sorted(os.listdir("."), reverse=True):  # Latest folders first
    if os.path.isdir(album_folder):
        album_image_url = None

        # Search for a .png file to use as album image
        for file in os.listdir(album_folder):
            if file.lower().endswith(".png"):
                album_image_url = BASE_URL + quote(album_folder) + "/" + quote(file)
                break

        # Go through .mp3 files in album
        for file in os.listdir(album_folder):
            if file.lower().endswith(".mp3"):
                song_name = os.path.splitext(file)[0]

                if not is_duplicate(song_name, album_folder):
                    song_url = BASE_URL + quote(album_folder) + "/" + quote(file)

                    new_songs.append({
                        "name": song_name,
                        "album": album_folder,
                        "url": song_url,
                        "albumImageUrl": album_image_url
                    })

# Prepend new songs to existing list
final_songs = new_songs + existing_songs

# Save updated JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_songs, f, indent=2, ensure_ascii=False)

print(f"✅ songs.json updated: {len(new_songs)} new songs added, {len(final_songs)} total.")
