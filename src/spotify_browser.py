from playwright.sync_api import sync_playwright


def get_playlist_tracks(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1280,
                "height": 900
            }
        )

        print("🌐 Opening Spotify playlist...")

        page.goto(
            url,
            wait_until="domcontentloaded"
        )

        print("⏳ Waiting for playlist...")
        page.wait_for_timeout(5000)

        tracks = {}

        print("🔄 Collecting tracks...")

        previous_count = 0
        stable_rounds = 0

        while stable_rounds < 5:

            rows = page.locator(
                '[data-testid="tracklist-row"]'
            )

            for i in range(rows.count()):

                row = rows.nth(i)

                try:
                    # Track position
                    position_text = row.locator(
                        '[aria-colindex="1"] span'
                    ).first.inner_text()

                    if not position_text.isdigit():
                        continue

                    position = int(position_text)

                    # Title
                    title = row.locator(
                        '[data-testid="internal-track-link"]'
                    ).inner_text()

                    # Artist(s)
                    artist_links = row.locator(
                        'a[href^="/artist/"]'
                    )

                    artists = []

                    for j in range(artist_links.count()):
                        artists.append(
                            artist_links.nth(j).inner_text()
                        )

                    # Album
                    album = row.locator(
                        '[aria-colindex="3"] a[href^="/album/"]'
                    ).inner_text()

                    # Date added
                    date_added = row.locator(
                        '[aria-colindex="4"]'
                    ).inner_text()

                    # Duration
                    duration = row.locator(
                        '[aria-colindex="5"]'
                    ).locator(
                        'div'
                    ).first.inner_text()

                    # Spotify track ID
                    track_link = row.locator(
                        '[data-testid="internal-track-link"]'
                    )

                    href = track_link.get_attribute("href")

                    track_id = None

                    if href:
                        track_id = href.split("/track/")[-1]

                    tracks[position] = {
                        "position": position,
                        "title": title,
                        "artists": artists,
                        "album": album,
                        "date_added": date_added,
                        "duration": duration,
                        "spotify_id": track_id,
                    }

                except Exception:
                    continue

            current_count = len(tracks)

            print(
                f"\r🎵 Collected {current_count} tracks...",
                end="",
                flush=True
            )

            if current_count == previous_count:
                stable_rounds += 1
            else:
                stable_rounds = 0

            previous_count = current_count

            # Scroll Spotify's actual playlist container
            page.evaluate("""
                () => {
                    const el = [...document.querySelectorAll('div')]
                        .find(el =>
                            el.scrollHeight > 5000 &&
                            el.clientHeight > 500
                        );

                    if (el) {
                        el.scrollTop += 700;
                    }
                }
            """)

            page.wait_for_timeout(700)

        print()

        browser.close()

        return [
            tracks[position]
            for position in sorted(tracks)
        ]