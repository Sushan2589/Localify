import yt_dlp
import re

def clean_query(track_name: str, artist: str) -> str:
    # strip noise like (Official Video), [Lyrics], feat. clutter
    name = re.sub(r"[\(\[].*?[\)\]]", "", track_name).strip()
    return f"{artist} {name}"

def find_best_match(track_name: str, artist: str, target_duration_ms: int, n=5):
    query = f"ytsearch{n}:{clean_query(track_name, artist)} audio"
    ydl_opts = {"quiet": True, "extract_flat": "in_playlist"}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(query, download=False)["entries"]

    target_sec = target_duration_ms / 1000
    best = None
    best_diff = float("inf")

    for r in results:
        if not r or not r.get("duration"):
            continue
        diff = abs(r["duration"] - target_sec)
        # small bonus for official/topic channels
        if diff < best_diff and diff <= 10:
            best, best_diff = r, diff

    return best  # None if nothing matched closely enough

def download_track(video_id: str, output_path: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://youtube.com/watch?v={video_id}"])