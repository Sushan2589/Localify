import os
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="playlist-read-private playlist-read-collaborative",
        cache_path=".spotify_cache",
    )
)


def get_playlist_tracks(playlist_url: str):

    playlist_id = playlist_url.split("playlist/")[1].split("?")[0]

    tracks = []

    results = spotify.playlist_items(
        playlist_id,
        additional_types=["track"],
    )

    while results:

        for item in results["items"]:

            track = item.get("track")

            if not track:
                continue

            tracks.append({
                "title": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "track_number": track["track_number"],
                "spotify_url": track["external_urls"]["spotify"],
            })

        if results["next"]:
            results = spotify.next(results)
        else:
            break

    return tracks