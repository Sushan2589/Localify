# 🎵 Localify

Download your Spotify playlists locally — no Spotify Premium, no Spotify API key required.

Localify scrapes a public Spotify playlist page with a headless browser to get track metadata, then finds and downloads the best-matching audio for each track from YouTube via `yt-dlp`.

## How it works

1. **Scrape** — `spotify_browser.py` opens the given Spotify playlist URL in a headless browser (Playwright), scrolls through the lazy-loaded track list, and extracts title, artists, album, and duration for every track.
2. **Match** — `downloader.py` searches YouTube for each track and picks the closest match by comparing durations (Spotify duration vs. YouTube result duration).
3. **Download** — the matched video's audio is extracted and saved as an MP3 into the `downloads/` folder.

No Spotify Developer account, API key, or Premium subscription is needed at any point — everything is read from Spotify's public playlist page.

## Requirements

- **Python 3.13+**
- **[Playwright](https://playwright.dev/python/)** — headless browser for scraping
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — YouTube search & download
- **FFmpeg** — required by yt-dlp to extract/convert audio to MP3
- **[Deno](https://deno.com/)** *(recommended)* — JS runtime yt-dlp uses to solve YouTube's signature challenges; without it you may see missing formats or a runtime warning

## Setup

**1. Clone the repo and enter the project folder**
```bash
git clone <your-repo-url> localify
cd localify
```

**2. Create a virtual environment and install dependencies**
```bash
Do:
python -m venv .venv


# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate


```

```bash
pip install playwright yt-dlp python-dotenv
playwright install chromium
```

**3. Install FFmpeg**
- Windows: `winget install ffmpeg` [in powershell] (or download from [ffmpeg.org](https://ffmpeg.org/))
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

**4. Install Deno** (recommended, avoids yt-dlp JS runtime warnings)
```bash
# Windows
winget install deno
# macOS/Linux
curl -fsSL https://deno.land/install.sh | sh
```
Restart your terminal afterwards so `deno` is on your PATH.

**5. Set up environment variables**
```bash
cp .env.example .env
```
Fill in any values `.env.example` calls for, then save.

## Usage

Run the app from the project root:
```bash
python src/main.py
```

You'll be prompted for a playlist URL:
```
🎵 Localify
-----------
Spotify playlist URL: https://open.spotify.com/playlist/<playlist_id>
```

Localify will:
1. Open the playlist and collect all tracks
2. Print each track as it's found
3. Search YouTube and download the best match for each one into `downloads/`

Example output:
```
001 | Jo Tum Mere Ho | Anuv Jain
  ⬇️  Downloading...
002 | Husn | Anuv Jain
  ⬇️  Downloading...
```

Downloaded files are named:
```
downloads/{position} - {artist} - {title}.mp3
```

If a track has no close-enough YouTube match (duration mismatch beyond the tolerance), it's skipped with a warning rather than downloading the wrong audio. If a download fails (rate limit, network issue, etc.), it's logged and Localify moves on to the next track instead of stopping the whole run.

## Notes & limitations

- Relies on scraping Spotify's public playlist page — if Spotify changes their page structure, the scraper may need updates.
- Matching is duration-based; occasional wrong matches (remixes, covers, live versions) can slip through.
- Downloads are throttled with randomized delays between tracks to avoid YouTube rate limiting — expect the run to take a while for large playlists.
- Intended for personal, offline use only.

## Project structure

```
localify/
├── src/
│   ├── main.py            # Entry point — runs the full scrape → match → download flow
│   ├── spotify_browser.py # Headless browser scraping of the Spotify playlist page
│   ├── spotify.py         # Spotify-related helpers
│   ├── downloader.py      # YouTube search, matching, and download logic (yt-dlp)
│   ├── metadata.py        # Track metadata handling
│   ├── config.py          # Configuration
│   └── downloads/         # Downloaded MP3s land here
├── .env.example
└── .gitignore
```
