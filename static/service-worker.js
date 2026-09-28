const CACHE_NAME = 'ens-daily-v2';
const APP_SHELL = [
  '/',
  '/static/app.js',
  '/static/style.css',
  '/static/icons/icon-192.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('fetch', event => {
  const requestUrl = new URL(event.request.url);

  if (
    event.request.method !== 'GET' ||
    requestUrl.origin !== self.location.origin ||
    requestUrl.pathname.startsWith('/api/') ||
    !APP_SHELL.includes(requestUrl.pathname)
  ) {
    return;
  }

  event.respondWith(
    fetch(event.request).then(response => {
      if (response.ok) {
        const clonedResponse = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clonedResponse));
      }
      return response;
    }).catch(async () => {
      const cachedResponse = await caches.match(event.request);
      if (cachedResponse) {
        return cachedResponse;
      }

      if (event.request.mode === 'navigate') {
        return caches.match('/');
      }

      return new Response('Offline - Página não disponível', {
        status: 503,
        statusText: 'Service Unavailable'
      })
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName.startsWith('ens-daily-') && cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});
