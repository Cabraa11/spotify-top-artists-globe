# How to Get Plus Codes for Hospital Locations

Plus Codes are what Google Maps uses to pinpoint a place. Using them ensures our map pins match the exact location Google shows.

---

## Option 1: Manual (Google Maps)

1. Open **Google Maps** (maps.google.com).
2. Search for the hospital, e.g. **Reading Hospital, West Reading PA** or **Lenox Hill Hospital New York**.
3. Click the **place** so the info panel opens (left or bottom).
4. In the info panel, click the **coordinates** (e.g. `40.330315, -75.950553`).  
   The **Plus Code** appears (e.g. `87F8Q2G2+2F`).
5. Copy the code and paste it into the data (see “Where to put them” below).

**On mobile:** Touch and hold to drop a pin → tap the bottom panel → tap the Plus Code to copy.

**Tip:** Use the full “global” code (e.g. `87F8Q2G2+2F`) so it works everywhere without a city name.

---

## Option 2: Programmatic (Geocoding API)

The script **`scripts/fetch_plus_codes.py`**:

- Takes the 13 hospital names/addresses from your data.
- Calls Google’s **Geocoding API** with each.
- Reads the **Plus Code** from the API response and prints (or writes) it.

**Requirements:**

- **Geocoding API** enabled in [Google Cloud Console](https://console.cloud.google.com/) for the same project as your Maps key.
- Your API key allowed to call Geocoding (if the key is restricted to “Maps JavaScript API” only, add “Geocoding API” or use an unrestricted key for this script).

**Run:** (from the spotify-map folder)

```bash
cd spotify-map
export GOOGLE_MAPS_API_KEY="your_key_here"   # or use config/google_api_key.txt
python3 scripts/fetch_plus_codes.py
```

If you see `REQUEST_DENIED`, enable “Geocoding API” under APIs & Services and ensure the key can call it. **Option 1 (manual)** always works and needs no API changes.

---

## Where to Put the Plus Codes

- In **`data/spotify_top100_artists.json`**: add a field `"plus_code": "87F8Q2G2+2F"` (no spaces) for each artist that has a named hospital.
- In **`spotify_top100_map.html`**: same — add `"plus_code": "..."` to each of those artist objects. The map can then resolve Plus Code → lat/lng when drawing pins (e.g. with a small client-side decoder or a single Geocoding call per code).

---

## Links

- [Find & share a location using Plus Codes (Google Help)](https://support.google.com/maps/answer/7047426)
- [Plus Codes on the web](https://plus.codes/)
- [Geocoding API – Plus Code in response](https://developers.google.com/maps/documentation/geocoding/overview#PlusCodes)
