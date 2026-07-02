/**
 * PyMD Editor — Service Worker
 * Caches the app shell so it loads offline.
 * API calls (/api/*) always go to the network.
 */

const CACHE_NAME = 'pymd-shell-v2';
const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/style.css',
  '/app.js',
  '/manifest.json',
  '/icon.svg',
  '/pyodide_worker.js',
];

// ── Install: pre-cache shell ──────────────────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(SHELL_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// ── Activate: clean old caches ────────────────────────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(k => k !== CACHE_NAME)
          .map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch: cache-first for shell, network-only for API ────────────────────────
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Never cache API requests — always go to network
  if (url.pathname.startsWith('/api/')) return;

  // Cache-first for shell assets
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        // Cache successful GET responses for shell paths
        if (
          response.ok &&
          event.request.method === 'GET' &&
          SHELL_ASSETS.some(a => url.pathname === a || url.pathname === '/')
        ) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      });
    })
  );
});
