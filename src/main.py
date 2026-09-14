import os
import random
import time
import re

from spotify_browser import get_playlist_tracks
from downloader import find_best_match, download_track


def parse_duration_to_ms(duration_str: str) -> int:
    minutes, seconds = map(int, duration_str.split(":"))
    return (minutes * 60 + seconds) * 1000


def main():
    print("🎵 Localify")
    print("-----------")

    url = input("Spotify playlist URL: ")
    tracks = get_playlist_tracks(url)

    print(f"\nFound {len(tracks)} tracks:\n")

    downloads_dir = "downloads"
    os.makedirs(downloads_dir, exist_ok=True)

    for track in tracks:
        artists = ", ".join(track["artists"])

        safe_title = re.sub(
            r'[\\/*?:"<>|]',
            "",
            track["title"]
        )

        safe_artist = re.sub(
            r'[\\/*?:"<>|]',
            "",
            artists
        )

        # No .mp3 here.
        # yt-dlp + FFmpeg will add .mp3 automatically.
        filename = f"{safe_artist} - {safe_title}"
        output_path = os.path.join(downloads_dir, filename)

        # This is the actual file we expect to exist.
        expected_file = output_path + ".mp3"

        print(
            f'{track["position"]:03} | '
            f'{track["title"]} | {artists}'
        )

        # Check downloads folder BEFORE doing anything else.
        if os.path.exists(expected_file):
            print("  ⏭️  Already downloaded, skipping\n")
            continue

        time.sleep(random.uniform(1.5, 3.5))

        target_ms = parse_duration_to_ms(track["duration"])

        try:
            match = find_best_match(
                track["title"],
                artists,
                target_ms
            )

            if match is None:
                print("  ⚠️  No good match found, skipping\n")
                continue

            print("  ⬇️  Downloading...")

            download_track(
                match["id"],
                output_path
            )

            print()

        except Exception as e:
            print(f"  ❌ Failed: {e}\n")
            continue


if __name__ == "__main__":
    main()