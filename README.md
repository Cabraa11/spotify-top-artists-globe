# Spotify Map

An interactive **3D globe** showing the **top 100 artists on Spotify** as ranked pins: search, click a pin for an info panel (listeners, origin, optional GRAMMY wins, link to Spotify), and optional **artist profile images** loaded via a small server-side Spotify proxy so your client secret never ships to the browser.

## Why it exists

It turns “who is big on Spotify and where they are from” into a **browsable map** instead of a spreadsheet or list. Useful for artist geographical exploration.

## Features

- **3D map** with pre-generated **PNG pins** (`pin-images/1.png` … `100.png`) for consistent marker appearance on the 3D API.
- **Embedded artist dataset** (names, locations, Spotify URLs, optional GRAMMY counts) inside `index.html`.
- **Artist images** in the side panel when `GET /api/artist/<spotify_id>` is available (local Node proxy or Netlify function).

## Requirements

- A **Google Maps JavaScript API** key with the libraries used by the page (including **Maps 3D** / experimental APIs as required by Google for your project). Replace the placeholder in `index.html` (see below).
- **Node.js** (for `./serve-and-open.sh` and the image proxy). Python is only used as a fallback static server.
- Optional: **Spotify** app (Client ID + secret) for artist images—see [docs/SPOTIFY-ARTIST-IMAGES.md](docs/SPOTIFY-ARTIST-IMAGES.md).

## Quick start (local)

1. **Clone** the repo (do not commit secrets; see [Security](#security)).

2. **Google Maps key**  
   In `index.html`, find the script tag that loads `maps.googleapis.com` and replace  
   `YOUR_GOOGLE_MAPS_API_KEY`  
   with your key.  
   For Python helpers that call Google APIs (e.g. Plus Codes), copy `config/google_api_key.example.txt` to `config/google_api_key.txt` and put your key on one line (that file is gitignored).

3. **Pins**  
   Unzip generated `pin-images/` next to `index.html` (see `tools/pin-generator.html`).

4. **Spotify images (optional)**  
   ```bash
   cp config/spotify_credentials.example.json config/spotify_credentials.json
   ```  
   Fill in real values from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

5. **Run**  
   ```bash
   ./serve-and-open.sh
   ```  
   Opens `http://localhost:<port>/index.html`. The Node proxy serves the map and `/api/artist/...` when it starts successfully.

## Netlify

`netlify.toml` publishes the project root. Set **`SPOTIFY_CLIENT_ID`** and **`SPOTIFY_CLIENT_SECRET`** in Netlify environment variables for the artist image function. You still need to configure the Maps key in `index.html` (or add your own build step to inject it from env).

## Repo layout (high level)

| Path | Role |
|------|------|
| `index.html` | Main map page (data + UI + Maps bootstrap) |
| `data/` | JSON sources for artists, GRAMMY data, etc. |
| `scripts/` | Merge/update scripts, Spotify proxy, fetch helpers |
| `tools/pin-generator.html` | Generate `pin-images.zip` for markers |
| `netlify/functions/artist.js` | Serverless artist image proxy |