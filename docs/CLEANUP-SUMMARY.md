# Spotify-map folder: what each file is for

Use this to see what’s required for the site, what’s for future updates, and where everything lives after reorganization.

---

## Folder structure

```
spotify-map/
├── spotify_top100_map.html   ← the map (open this)
├── pin-images/               ← 1.png … 100.png (required for pins)
├── serve-and-open.sh          ← run to serve + open map
├── data/                      ← all JSON data
│   ├── spotify_top100_artists.json
│   ├── pin-artists.json
│   ├── grammy_wins_official.json
│   └── grammy_artist_paths.json
├── scripts/                   ← Python scripts (run from project root)
│   ├── fetch_grammy_wins.py
│   ├── fetch_plus_codes.py
│   ├── merge_grammy_into_html.py
│   └── merge_grammy_wins.py
├── tools/
│   └── pin-generator.html     ← open in browser to generate pin-images.zip
├── config/
│   └── google_api_key.txt
├── MARKETING-CONTEXT-AND-PLAN.md   ← marketing reminder (root, not in docs/)
└── docs/
    ├── PIN-IMAGES-SYSTEM.md
    ├── PLUS_CODES.md
    └── CLEANUP-SUMMARY.md     ← this file
```

---

## Required for the site to work

| Item | Purpose |
|------|--------|
| **spotify_top100_map.html** | The map page. Artists + GRAMMY data are embedded inside it. |
| **pin-images/** | Folder with 1.png … 100.png. The map loads these as pin icons. |

---

## Needed for future updates / regeneration

| Item | Purpose |
|------|--------|
| **tools/pin-generator.html** | Generate new pin images. Open in browser → “Generate pin-images.zip” → unzip into spotify-map so pin-images/ is next to the map. |
| **data/pin-artists.json** | Artist list (rank, name). Used when refreshing the generator’s list; generator also has a copy embedded. |
| **config/google_api_key.txt** | Your Maps API key. The map currently has the key in the HTML; keep this if you want to change the key in one place later. |
| **serve-and-open.sh** | Runs a local server and opens the map so pin images load (required when opening from disk). |
| **scripts/fetch_grammy_wins.py** | Fetches GRAMMY win counts from grammy.com. Writes data/grammy_wins_official.json. Run from spotify-map: `python3 scripts/fetch_grammy_wins.py` |
| **data/grammy_artist_paths.json** | Mapping artist name → GRAMMY.com path. Input for fetch_grammy_wins.py. |
| **data/grammy_wins_official.json** | GRAMMY wins by artist. Input for merge_grammy_into_html.py. |
| **scripts/merge_grammy_into_html.py** | Injects GRAMMY wins from data/grammy_wins_official.json into spotify_top100_map.html. Run from spotify-map: `python3 scripts/merge_grammy_into_html.py` |
| **scripts/merge_grammy_wins.py** | Merges grammy_wins_official.json into data/spotify_top100_artists.json. Run from spotify-map: `python3 scripts/merge_grammy_wins.py` |
| **data/spotify_top100_artists.json** | Full artist data (locations, etc.). Source for merge_grammy_wins. |
| **scripts/fetch_plus_codes.py** | Fetches plus codes for locations. Run from spotify-map: `python3 scripts/fetch_plus_codes.py` |
| **docs/PLUS_CODES.md** | How to get plus codes (manual + script). |

---

## Documentation

| Item | Purpose |
|------|--------|
| **MARKETING-CONTEXT-AND-PLAN.md** | Your marketing context and plan (in spotify-map root). |
| **docs/PIN-IMAGES-SYSTEM.md** | Explains how pin images are generated and displayed (for dev reference). |

---

## Removed during cleanup

| Item | Reason |
|------|--------|
| **spotify_artists_batches.md** | One-time research aid: batches of artist names for the Groq prompt to get birth locations. The map already has that data embedded. Only needed again if you add more artists and re-run that research. |
