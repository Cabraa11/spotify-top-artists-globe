#!/usr/bin/env python3
"""
Fetch GRAMMY wins from official GRAMMY.com artist pages and add to artist data.
Uses grammy_artist_paths.json for artist name -> path (slug/id) mapping.
Source: https://www.grammy.com/artists/{path}
"""
import json
import re
import urllib.request
import ssl
import os

GRAMMY_BASE = "https://www.grammy.com/artists"
SSL_CTX = ssl.create_default_context()

def fetch_wins(path: str) -> int | None:
    url = f"{GRAMMY_BASE}/{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; GrammyWinsBot/1.0)"})
        with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception:
        return None
    # Page shows "WINS*" then a number; avoid matching script/style (e.g. 666). Wins are 0-99.
    m = re.search(r"WINS\*?\s*</[^>]+>\s*[^<]*(?:<[^>]+>)\s*(\d{1,2})", html, re.I | re.DOTALL)
    if m:
        return int(m.group(1))
    m = re.search(r"WINS\*?\s*[^0-9]{0,80}?\b(\d{1,2})\b", html, re.I | re.DOTALL)
    if m:
        val = int(m.group(1))
        if val <= 99:
            return val
    return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    paths_path = os.path.join(project_root, "data", "grammy_artist_paths.json")
    json_path = os.path.join(project_root, "data", "spotify_top100_artists.json")

    with open(paths_path, "r", encoding="utf-8") as f:
        paths = json.load(f)

    wins_by_name = {}
    for name, path in paths.items():
        print(f"Fetching {name} ... ", end="", flush=True)
        w = fetch_wins(path)
        if w is not None:
            wins_by_name[name] = w
            print(w)
        else:
            print("skip")

    with open(json_path, "r", encoding="utf-8") as f:
        raw = f.read()
    # File may be multiple concatenated JSON arrays
    artists = []
    decoder = json.JSONDecoder()
    pos = 0
    raw = raw.strip()
    while pos < len(raw):
        obj, idx = decoder.raw_decode(raw, pos)
        artists.extend(obj)
        pos += idx
        pos = raw.find("[", pos)
        if pos < 0:
            break

    for a in artists:
        name = a.get("name")
        a["grammy_wins"] = wins_by_name.get(name)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(artists, f, indent=2, ensure_ascii=False)

    print(f"\nUpdated {json_path} with grammy_wins for {len(wins_by_name)} artists.")

if __name__ == "__main__":
    main()
