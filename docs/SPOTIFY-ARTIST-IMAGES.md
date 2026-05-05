# Spotify Artist Images – What Was Added

## Overview

Artist profile images from Spotify are shown in the info panel when you click a pin. The frontend fetches image URLs from a **backend proxy** (keeps your secret safe) and caches them.

---

## 1. Config: `config/spotify_credentials.json`

Stores your Spotify app credentials (not in the repo). Copy from the example file:

```bash
cp config/spotify_credentials.example.json config/spotify_credentials.json
```

Then edit `spotify_credentials.json` with your real `client_id` and `client_secret` from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

```json
{
  "client_id": "YOUR_SPOTIFY_CLIENT_ID",
  "client_secret": "YOUR_SPOTIFY_CLIENT_SECRET"
}
```

- The real file is listed in `.gitignore` so it is not committed.
- Read only by the local Node proxy (or by Netlify env vars in production).

---

## 2. Backend proxy: `scripts/spotify_image_proxy.js`

A Node.js server (no npm deps) that:

1. Serves the map, pin images, and other static files
2. Exposes `/api/artist/<spotify_id>` – calls Spotify’s API and returns `{ "imageUrl": "https://...", "name": "..." }`
3. Uses Client Credentials to get an access token, so the secret never goes to the browser

Flow: Browser → your proxy → Spotify → your proxy → browser.

---

## 3. Serve script: `serve-and-open.sh`

1. Finds a free port (8765, 8766, …)
2. Runs `node scripts/spotify_image_proxy.js <port>` (serves static files and the API)
3. If Node fails, falls back to `python3 -m http.server <port>` (no `/api/artist/` then)

If the fallback HTTP server is used, artist images in the panel will not load because there is no proxy.

---

## 4. Frontend: `index.html`

**UI:**

- `<img id="p-artist-img">` in the info panel (above stats)
- CSS: `.panel-artist-img` – 160×160px, rounded corners

**Logic:**

- `getSpotifyArtistId(spotify_url)` – pulls the artist ID from URLs like `https://open.spotify.com/artist/0hCNtLu0JehylgoiP8L4Gh`
- `loadArtistImage(a)` – called when the panel opens:
  - Checks `artistImageCache[id]`
  - If cached → sets `img.src` and shows the image
  - If not → `fetch('/api/artist/' + id)` → on success, caches and shows image
- `.catch(() => {})` – swallows errors, so failed fetches do not surface in the UI

---

## 5. Netlify

For deploys on Netlify, set **`SPOTIFY_CLIENT_ID`** and **`SPOTIFY_CLIENT_SECRET`** in the site environment variables. The function `netlify/functions/artist.js` implements the same `/api/artist/:id` behavior.

---

## Troubleshooting: Artist image not showing

### Most likely: proxy not running (local)

When you run `./serve-and-open.sh`, you should see output from the Node server, including a line with `Map: http://localhost:<port>/index.html`.

**Test the API** (use your port):

`http://localhost:<port>/api/artist/0hCNtLu0JehylgoiP8L4Gh`

- JSON with `imageUrl` → proxy is working.
- 404 on `/api/artist/` → you are on plain `python3 -m http.server` without the Node proxy.

**Fix:** Ensure Node is installed and `config/spotify_credentials.json` exists, then run `./serve-and-open.sh` again.

---

### Other possible issues

1. **Browser DevTools (Console)** – look for errors related to `fetch` or `/api/artist/`.
2. **Network tab** – check if `/api/artist/<id>` returns 200 or 404.
3. **Credentials** – if you rotated the client secret, update `config/spotify_credentials.json` (or Netlify env) with the new secret.
