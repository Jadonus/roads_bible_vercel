self.importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js'); workbox.routing.registerRoute(({ url }) => url.origin === 'https://www.roadsbible.com/roads/', new workbox.strategies.StaleWhileRevalidate({ cacheName: 'roadscache1.0', plugins: [new workbox.cacheableResponse.CacheableResponsePlugin({ statuses: [200], }),], })); workbox.routing.registerRoute(({ url }) => url.origin === self.location.origin && url.pathname.startsWith('/static/'), new workbox.strategies.StaleWhileRevalidate({ cacheName: 'staticcache1.0', plugins: [new workbox.cacheableResponse.CacheableResponsePlugin({ statuses: [200], }),], }));