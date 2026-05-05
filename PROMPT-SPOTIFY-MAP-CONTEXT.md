# Context prompt: Spotify Top 100 Artists Map

**Paste this into a new Cursor chat when you open the Spotify map project so the AI has full context.**

---

## What this project is
- **Spotify Top 100 Map**: An interactive 3D globe showing where the Spotify Top 100 artists were **born** (or formed). Built out of curiosity (“where are the most talented artists from?”). Also used to practice marketing/branding.
- **Stack**: Single-page HTML (`spotify_top100_map.html`) using **Google Maps JavaScript API** with **Map3DElement** and **Marker3DInteractiveElement** (3D globe). Artist data and GRAMMY wins are **embedded** in the HTML. Pins are **pre-generated PNG images** (not HTML/CSS on the map, because the 3D API doesn’t render custom HTML for markers).

---

## How the pin images work (important)
- **Generation**: Open `tools/pin-generator.html` in a browser. It uses **html2canvas** (scale 6) to rasterize a green pill label (e.g. “#1 Taylor Swift”) and downloads **pin-images.zip**. Unzip into the **project root** so the folder **pin-images/** (with 1.png … 100.png) sits **next to** `spotify_top100_map.html`.
- **Display**: The 3D map sizes markers by the **intrinsic pixel dimensions** of the image (CSS width/height on the `<img>` are ignored). So:
  - We keep **high-res source PNGs** from the generator.
  - At **display time** we **downscale**: load each PNG, draw it into a **small canvas** with **fixed height** (e.g. `pinHeight = 48` px) and **width = aspect ratio**, then use that canvas image as the marker’s `img` src. Result: all pins same height, variable width, no stretching, small on the globe.
- **No “pin tail”**: The pill design has **no** triangle/arrow at the bottom (the `.custom-pin::after` that drew it was removed from both the generator and the map’s fallback CSS).
- **Serving**: The map must be loaded over **HTTP** (e.g. `http://localhost:8765/spotify_top100_map.html`). Opening the HTML via **file://** blocks loading local images and breaks the map. Use **serve-and-open.sh** or run `python3 -m http.server 8765` from the project root, then open that URL.

---

## Project layout (after reorganization)
- **Root**: `spotify_top100_map.html`, `pin-images/`, `serve-and-open.sh`, `MARKETING-CONTEXT-AND-PLAN.md`
- **data/**: `spotify_top100_artists.json`, `pin-artists.json`, `grammy_wins_official.json`, `grammy_artist_paths.json`
- **scripts/**: `fetch_grammy_wins.py`, `fetch_plus_codes.py`, `merge_grammy_into_html.py`, `merge_grammy_wins.py` — all run from **project root** (e.g. `python3 scripts/merge_grammy_into_html.py`). They use paths like `../data/...` and `../spotify_top100_map.html`.
- **tools/**: `pin-generator.html` (open in browser to regenerate pin PNGs)
- **config/**: `google_api_key.txt` (Maps API key; the HTML may also have the key inline)
- **docs/**: `PIN-IMAGES-SYSTEM.md`, `CLEANUP-SUMMARY.md`, `PLUS_CODES.md` (how pin images work, folder summary, plus codes for locations)

---

## Marketing / future TODOs (in MARKETING-CONTEXT-AND-PLAN.md)
- **Improve the site**: Current design was 100% AI-coded; refine to your taste and aim above “average map project” look.
- **Cheaper map provider**: Before publishing, look for an alternative to Google Maps API that is as close as possible in quality but **much cheaper**, so traffic doesn’t blow the budget.
- **Distribution**: Plan to market on X (Twitter), TikTok, Instagram Reels, and YouTube Shorts; adapt the hook per platform.

---

## Common tasks
- **Regenerate pin images**: Open `tools/pin-generator.html` → “Generate pin-images.zip” → unzip into project root so `pin-images/` is next to the map HTML.
- **Run the map locally**: From project root, run `./serve-and-open.sh` or `python3 -m http.server 8765` then open `http://localhost:8765/spotify_top100_map.html`.
- **Update GRAMMY data**: Run `python3 scripts/fetch_grammy_wins.py` (writes `data/grammy_wins_official.json`), then `python3 scripts/merge_grammy_into_html.py` to inject wins into the map HTML.
- **Adjust pin size on globe**: In `spotify_top100_map.html`, change `pinHeight` (e.g. 48) in the `loadAndDownscale` / marker-creation section; fixed height keeps all pins the same height, width follows source aspect ratio.

---

Use this context to answer questions, change the map, fix bugs, or add features without losing the above decisions and structure.
