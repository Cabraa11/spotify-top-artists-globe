#!/usr/bin/env python3
"""
Fetch Plus Codes for the 13 hospitals using Google Geocoding API.
Copy config/google_api_key.example.txt to config/google_api_key.txt and put your key on one line,
or set GOOGLE_MAPS_API_KEY in the environment. (google_api_key.txt is gitignored.)

Requires Geocoding API enabled in your Google Cloud project.
"""
import os
import json
import time
import urllib.request
import urllib.parse

# Delay between requests (seconds) to avoid rate limits / REQUEST_DENIED
REQUEST_DELAY = 2

# Artist name -> address query for Geocoding (hospital name + city/country)
HOSPITAL_QUERIES = [
    ("Taylor Swift", "Reading Hospital, 420 South 5th Avenue, West Reading, Pennsylvania, USA"),
    ("Justin Bieber", "St. Joseph's Hospital, 268 Grosvenor Street, London, Ontario, Canada"),
    ("Lady Gaga", "Lenox Hill Hospital, 100 East 77th Street, New York, NY, USA"),
    ("Ariana Grande", "Mount Sinai West, 1000 10th Avenue, New York, NY, USA"),
    ("Kanye West", "Grady Memorial Hospital, 80 Jesse Hill Jr Dr SE, Atlanta, Georgia, USA"),
    ("Lana Del Rey", "Lenox Hill Hospital, 100 East 77th Street, New York, NY, USA"),  # same as Lady Gaga
    ("Zara Larsson", "Karolinska University Hospital, Solna, Stockholm, Sweden"),
    ("Sabrina Carpenter", "St Luke's Quakertown Hospital, 1021 Park Avenue, Quakertown, Pennsylvania, USA"),
    ("Harry Styles", "Alexandra Hospital, Redditch, Worcestershire, England"),
    ("Katy Perry", "Goleta Valley Cottage Hospital, 351 South Patterson Avenue, Santa Barbara, California, USA"),
    ("Michael Jackson", "St. Mary's Mercy Hospital, 549 Tyler Street, Gary, Indiana, USA"),
    ("Khalid", "Winn Army Community Hospital, 1061 Harmon Avenue, Fort Stewart, Georgia, USA"),
    ("Madonna", "Mercy Hospital Bay City, 15th and Water Streets, Bay City, Michigan, USA"),
]

def geocode(address: str, api_key: str) -> dict:
    url = "https://maps.googleapis.com/maps/api/geocode/json?" + urllib.parse.urlencode({
        "address": address,
        "key": api_key,
    })
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read().decode())


def main():
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()
    if not api_key:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, ".."))
        key_file = os.path.join(project_root, "config", "google_api_key.txt")
        if os.path.isfile(key_file):
            with open(key_file, "r") as f:
                api_key = f.read().strip()
    if not api_key:
        print("Add your API key to config/google_api_key.txt (copy from google_api_key.example.txt).")
        print("Or set GOOGLE_MAPS_API_KEY. Enable Geocoding API in Cloud Console.")
        return

    print("Fetching Plus Codes via Geocoding API...\n")
    for artist, query in HOSPITAL_QUERIES:
        try:
            data = geocode(query, api_key)
            if data.get("status") != "OK":
                print(f"{artist}: API status {data.get('status')} – {query}")
                continue
            results = data.get("results", [])
            if not results:
                print(f"{artist}: No results – {query}")
                continue
            first = results[0]
            plus = first.get("plus_code")
            global_code = (plus or {}).get("global_code")
            compound = (plus or {}).get("compound_code", "")
            if global_code:
                print(f"{artist}")
                print(f"  plus_code: \"{global_code}\"")
                print(f"  (compound: {compound})")
            else:
                print(f"{artist}: No Plus Code in response – {query}")
            print()
        except Exception as e:
            print(f"{artist}: Error – {e}\n")

        time.sleep(REQUEST_DELAY)

    print("Copy each plus_code into the artist object in data/spotify_top100_artists.json and spotify_top100_map.html.")


if __name__ == "__main__":
    main()
