import pandas as pd
import os
import requests
import time
from urllib.parse import quote

# ✅ Input file path
excel_path = r"C:\Users\hasin\Downloads\songs_list_english_300.xlsx"
df = pd.read_excel(excel_path)

# ✅ Create output folder
os.makedirs("data", exist_ok=True)

# ✅ Storage
lyrics_list = []
skipped_list = []

# ✅ Lyrics.ovh fetch function
def get_lyrics_ovh(artist, title):
    url = f"https://api.lyrics.ovh/v1/{quote(artist)}/{quote(title)}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("lyrics", None)
        return None
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None

# ✅ Loop 1: Try each song once
for i, row in df.iterrows():
    title = str(row["Title"]).strip()
    artist = str(row["Artist"]).strip()

    print(f"🔍 {i+1}/{len(df)}: Searching '{title}' by '{artist}'")
    lyrics = get_lyrics_ovh(artist, title)
    time.sleep(1)  # polite delay

    if lyrics:
        lyrics_list.append({"title": title, "artist": artist, "lyrics": lyrics})
    else:
        skipped_list.append({"title": title, "artist": artist})

# ✅ Loop 2: Retry skipped songs once
retry_success = []
still_skipped = []

if skipped_list:
    print(f"\n🔁 Retrying {len(skipped_list)} failed songs...\n")
    for i, row in enumerate(skipped_list):
        title = row["title"]
        artist = row["artist"]
        print(f"🔁 Retry {i+1}/{len(skipped_list)}: '{title}' by '{artist}'")
        lyrics = get_lyrics_ovh(artist, title)
        time.sleep(1)
        if lyrics:
            lyrics_list.append({"title": title, "artist": artist, "lyrics": lyrics})
            retry_success.append(row)
        else:
            still_skipped.append(row)

# ✅ Save collected lyrics
lyrics_df = pd.DataFrame(lyrics_list)
lyrics_df.to_excel("data/raw_lyrics_ovh.xlsx", index=False)
print(f"\n✅ Lyrics saved: {len(lyrics_list)} songs → data/raw_lyrics_ovh.xlsx")

# ✅ Save failed after retry
if still_skipped:
    skipped_df = pd.DataFrame(still_skipped)
    skipped_df.to_excel("data/skipped_songs_final.xlsx", index=False)
    print(f"⚠️ Still failed: {len(still_skipped)} songs → data/skipped_songs_final.xlsx")

print("\n🎉 DONE! Your lyrics are ready.")
