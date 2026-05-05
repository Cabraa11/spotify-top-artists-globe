/**
 * Netlify Function: /api/artist/:id
 * Fetches the artist image URL from Spotify API using server-side credentials.
 * Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in Netlify environment variables.
 */
const https = require('https');

let token = null;
let tokenExpiry = 0;

function httpsRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = https.request(
      {
        hostname: u.hostname,
        port: u.port || 443,
        path: u.pathname + u.search,
        method: options.method || 'GET',
        headers: options.headers || {},
      },
      (res) => {
        let data = '';
        res.on('data', (chunk) => (data += chunk));
        res.on('end', () => {
          try { resolve({ status: res.statusCode, data: JSON.parse(data) }); }
          catch { resolve({ status: res.statusCode, data }); }
        });
      }
    );
    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
}

async function getToken() {
  if (token && Date.now() < tokenExpiry - 60000) return token;
  const clientId = process.env.SPOTIFY_CLIENT_ID;
  const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;
  if (!clientId || !clientSecret) throw new Error('Missing Spotify credentials in environment variables.');
  const auth = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');
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
  if (status !== 200) throw new Error((data && data.error_description) || 'Failed to get token');
  token = data.access_token;
  tokenExpiry = Date.now() + (data.expires_in || 3600) * 1000;
  return token;
}

exports.handler = async (event) => {
  const cors = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
  };

  // Extract artist ID from path: /.netlify/functions/artist/<id>
  // or from query string: ?id=<id>
  const pathParts = (event.path || '').split('/');
  const artistId = pathParts[pathParts.length - 1] || (event.queryStringParameters || {}).id;

  if (!artistId || !/^[a-zA-Z0-9]+$/.test(artistId)) {
    return { statusCode: 400, headers: cors, body: JSON.stringify({ error: 'Invalid artist ID' }) };
  }

  try {
    const accessToken = await getToken();
    const { status, data } = await httpsRequest(`https://api.spotify.com/v1/artists/${artistId}`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (status !== 200) {
      return { statusCode: status, headers: cors, body: JSON.stringify({ imageUrl: null }) };
    }
    const images = data.images || [];
    const imageUrl = images.length > 0 ? images[0].url : null;
    return { statusCode: 200, headers: cors, body: JSON.stringify({ imageUrl }) };
  } catch (err) {
    return { statusCode: 500, headers: cors, body: JSON.stringify({ error: err.message, imageUrl: null }) };
  }
};
