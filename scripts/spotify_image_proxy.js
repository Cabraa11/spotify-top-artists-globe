#!/usr/bin/env node
/**
 * Spotify artist image proxy. Fetches artist images from Spotify API and serves them
 * so the frontend can load images without exposing the client secret.
 * Run: node scripts/spotify_image_proxy.js [port]
 */
const path = require('path');
const fs = require('fs');
const http = require('http');
const https = require('https');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const CREDS_PATH = path.join(PROJECT_ROOT, 'config', 'spotify_credentials.json');

let token = null;
let tokenExpiry = 0;

function loadCredentials() {
  if (!fs.existsSync(CREDS_PATH)) {
    console.error(`Missing ${CREDS_PATH}. Create it with client_id and client_secret.`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CREDS_PATH, 'utf8'));
}

function httpsRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const reqOpts = {
      hostname: u.hostname,
      port: u.port || 443,
      path: u.pathname + u.search,
      method: options.method || 'GET',
      headers: options.headers || {},
    };
    const req = https.request(reqOpts, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, data });
        }
      });
    });
    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
}

async function getToken() {
  if (token && Date.now() < tokenExpiry - 60000) return token;
  const creds = loadCredentials();
  const auth = Buffer.from(`${creds.client_id}:${creds.client_secret}`).toString('base64');
  const body = 'grant_type=client_credentials';
  const { status, data } = await httpsRequest('https://accounts.spotify.com/api/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(body),
      Authorization: `Basic ${auth}`,
    },
    body,
  });
  if (status !== 200) {
    throw new Error((data && data.error_description) || 'Failed to get token');
  }
  token = data.access_token;
  tokenExpiry = Date.now() + (data.expires_in || 3600) * 1000;
  return token;
}

async function fetchArtistImage(artistId) {
  const accessToken = await getToken();
  const { status, data } = await httpsRequest(`https://api.spotify.com/v1/artists/${artistId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (status !== 200) return null;
  const images = data.images || [];
  return images.length > 0 ? images[0].url : null;
}

function findFreePort(start) {
  return new Promise((resolve) => {
    const server = require('http').createServer();
    server.listen(start, () => {
      const port = server.address().port;
      server.close(() => resolve(port));
    });
    server.on('error', () => findFreePort(start + 1).then(resolve));
  });
}

function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const map = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.ico': 'image/x-icon',
  };
  return map[ext] || 'application/octet-stream';
}

async function main() {
  const portArg = parseInt(process.argv[2], 10);
  const port = Number.isFinite(portArg) && portArg > 0 ? portArg : 8765;
  const resolvedPort = await findFreePort(port);

  const server = http.createServer(async (req, res) => {
    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET',
    };

    const apiMatch = req.url.match(/^\/api\/artist\/([a-zA-Z0-9]+)$/);
    if (apiMatch) {
      const artistId = apiMatch[1];
      try {
        const imageUrl = await fetchArtistImage(artistId);
        res.writeHead(200, { 'Content-Type': 'application/json', ...cors });
        res.end(JSON.stringify({ imageUrl, name: null }));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json', ...cors });
        res.end(JSON.stringify({ error: err.message, imageUrl: null }));
      }
      return;
    }

    const urlPath = (req.url === '/' ? 'index.html' : req.url.split('?')[0].replace(/^\//, '')) || 'index.html';
    let filePath = path.join(PROJECT_ROOT, urlPath);
    const resolved = path.resolve(filePath);
    if (resolved.startsWith(PROJECT_ROOT) && fs.existsSync(resolved) && fs.statSync(resolved).isFile()) {
      res.writeHead(200, { 'Content-Type': getMimeType(filePath), ...cors });
      res.end(fs.readFileSync(filePath));
      return;
    }

    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not found');
  });

  server.listen(resolvedPort, '0.0.0.0', () => {
    console.log(`Serving at http://localhost:${resolvedPort}/`);
    console.log(`Map: http://localhost:${resolvedPort}/index.html`);
    console.log('Press Ctrl+C to stop.');
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
