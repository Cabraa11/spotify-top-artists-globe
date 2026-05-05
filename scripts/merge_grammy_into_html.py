#!/usr/bin/env python3
"""Inject GRAMMY wins (from grammy_wins_official.json) into index.html artists array."""
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
HTML_PATH = os.path.join(PROJECT_ROOT, "index.html")
WINS_PATH = os.path.join(PROJECT_ROOT, "data", "grammy_wins_official.json")

def main():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    start_marker = "const artists = "
    end_marker = "\n\nlet map"
    idx = html.find(start_marker)
    idx_end = html.find(end_marker)
    if idx == -1 or idx_end == -1:
        raise SystemExit("Could not find artists array in HTML")
    chunk = html[idx + len(start_marker) : idx_end].strip()
    if chunk.endswith(";"):
        chunk = chunk[:-1]
    artists = json.loads(chunk)

    with open(WINS_PATH, "r", encoding="utf-8") as f:
        wins_by_name = json.load(f)

    for a in artists:
        a["grammy_wins"] = wins_by_name.get(a["name"])

    new_json = json.dumps(artists, indent=2, ensure_ascii=False)
    new_html = (
        html[:idx]
        + "const artists = "
        + new_json
        + ";\n\nlet map"
        + html[idx_end + len(end_marker) :]
    )
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)
    count = sum(1 for a in artists if a.get("grammy_wins") is not None)
    print(f"Injected grammy_wins into HTML for {count} artists (source: GRAMMY.com).")

if __name__ == "__main__":
    main()
