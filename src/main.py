
import os
from spotify_browser import get_playlist_tracks
from downloader import find_best_match, download_track
import random
import time
import re


def parse_duration_to_ms(duration_str: str) -> int:
    minutes, seconds = map(int, duration_str.split(":"))
    return (minutes * 60 + seconds) * 1000


def main():
    print("🎵 Localify")
    print("-----------")

    url = input("Spotify playlist URL: ")
    tracks = get_playlist_tracks(url)

    print(f"\nFound {len(tracks)} tracks:\n")

    os.makedirs("downloads", exist_ok=True)

    for track in tracks:
        time.sleep(random.uniform(1.5, 3.5))
        artists = ", ".join(track["artists"])
        target_ms = parse_duration_to_ms(track["duration"])

        print(f'{track["position"]:03} | {track["title"]} | {artists}')

        try:
            match = find_best_match(track["title"], artists, target_ms)

            if match is None:
                print(f"  ⚠️  No good match found, skipping")
                continue

            safe_title = re.sub(r'[\\/*?:"<>|]', "", track["title"])
            safe_artist = re.sub(r'[\\/*?:"<>|]', "", artists)
            output_path = f'downloads/{track["position"]:03} - {safe_artist} - {safe_title}.%(ext)s'

            print(f"  ⬇️  Downloading...")
            download_track(match["id"], output_path)

        except Exception as e:
            print(f"  ❌ Failed: {e}")
            continue


if __name__ == "__main__":
    main()