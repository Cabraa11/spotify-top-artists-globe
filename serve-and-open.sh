#!/bin/bash
# Serve spotify-map over HTTP (with Spotify image proxy). Then open the map.
cd "$(dirname "$0")"

PORT=8765
while ! python3 -c "import socket; s=socket.socket(); s.bind(('', $PORT)); s.close()" 2>/dev/null; do
  PORT=$((PORT + 1))
done

echo "Serving at http://localhost:$PORT/"
echo "Open: http://localhost:$PORT/index.html"
echo "Press Ctrl+C to stop the server."
# Open browser after 2s so the server is ready
( sleep 2; open "http://localhost:$PORT/index.html" ) &
node scripts/spotify_image_proxy.js "$PORT" || python3 -m http.server "$PORT"
