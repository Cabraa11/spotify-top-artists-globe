#!/usr/bin/env python3
"""
Merge official GRAMMY wins (from grammy_wins_official.json) into artist data.
Preserves the 5-array structure of spotify_top100_artists.json.
Source: https://www.grammy.com/artists/
"""
import json
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    wins_path = os.path.join(project_root, "data", "grammy_wins_official.json")
    json_path = os.path.join(project_root, "data", "spotify_top100_artists.json")

    with open(wins_path, "r", encoding="utf-8") as f:
        wins_by_name = json.load(f)

    with open(json_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Parse multiple concatenated arrays
    artists = []
    decoder = json.JSONDecoder()
    pos = 0
    raw_stripped = raw.strip()
    while pos < len(raw_stripped):
        obj, idx = decoder.raw_decode(raw_stripped, pos)
        artists.extend(obj)
        pos += idx
        next_start = raw_stripped.find("[", pos)
        if next_start < 0:
            break
        pos = next_start

    # Add grammy_wins to each artist
    for a in artists:
        name = a.get("name")
        if name in wins_by_name:
            a["grammy_wins"] = wins_by_name[name]
        else:
            a["grammy_wins"] = None

    # Write back as 5 arrays of 20 (preserve original structure)
    n = len(artists)
    chunk_size = 20
    chunks = [artists[i:i + chunk_size] for i in range(0, n, chunk_size)]
    with open(json_path, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            if i > 0:
                f.write("\n")
            json.dump(chunk, f, indent=2, ensure_ascii=False)

    count = sum(1 for a in artists if a.get("grammy_wins") is not None)
    print(f"Updated {json_path} with grammy_wins for {count} artists (source: GRAMMY.com).")

if __name__ == "__main__":
    main()
