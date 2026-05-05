#!/usr/bin/env python3
"""
Verify and update GRAMMY wins from official GRAMMY.com for all artists with paths.
Fetches from https://www.grammy.com/artists/{path} and updates grammy_wins_official.json.
Artists without paths in grammy_artist_paths.json are left unchanged.
"""
import json
import re
import urllib.request
import ssl
import os

GRAMMY_BASE = "https://www.grammy.com/artists"
SSL_CTX = ssl.create_default_context()

# Fallback paths for artists whose primary path returns 404
PATH_FALLBACKS = {
    "Bad Bunny": ["bad-bunny/243129"],  # 251735 returns 404
}


def fetch_wins(path: str) -> int | None:
    url = f"{GRAMMY_BASE}/{path}"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (compatible; GrammyWinsBot/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception:
        return None
    m = re.search(
        r"WINS\*?\s*</[^>]+>\s*[^<]*(?:<[^>]+>)\s*(\d{1,2})", html, re.I | re.DOTALL
    )
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
    wins_path = os.path.join(project_root, "data", "grammy_wins_official.json")

    with open(paths_path, "r", encoding="utf-8") as f:
        paths = json.load(f)

    with open(wins_path, "r", encoding="utf-8") as f:
        current_wins = json.load(f)

    official_wins = {}
    failed = []
    corrections = []

    for name, path in paths.items():
        w = fetch_wins(path)
        if w is not None:
            official_wins[name] = w
            prev = current_wins.get(name)
            if prev is not None and prev != w:
                corrections.append((name, prev, w))
            print(f"  {name}: {w}")
        else:
            if name in PATH_FALLBACKS:
                for fallback in PATH_FALLBACKS[name]:
                    w2 = fetch_wins(fallback)
                    if w2 is not None:
                        official_wins[name] = w2
                        prev = current_wins.get(name)
                        if prev is not None and prev != w2:
                            corrections.append((name, prev, w2))
                        print(f"  {name}: {w2} (fallback path)")
                        break
                else:
                    failed.append(name)
                    print(f"  {name}: FAILED (all paths)")
            else:
                failed.append(name)
                print(f"  {name}: FAILED")

    # Merge: official values override, keep current for artists without paths
    merged = dict(current_wins)
    for name, wins in official_wins.items():
        merged[name] = wins

    with open(wins_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print()
    print(f"Fetched {len(official_wins)} artists from GRAMMY.com")
    print(f"Failed: {len(failed)}")
    if failed:
        print("  Failed artists (no path or 404):", ", ".join(failed))
    print(f"Artists without GRAMMY paths (kept existing): {len(merged) - len(paths)}")
    if corrections:
        print()
        print("Corrections applied (our value -> official):")
        for name, old, new in corrections:
            print(f"  {name}: {old} -> {new}")


if __name__ == "__main__":
    main()
