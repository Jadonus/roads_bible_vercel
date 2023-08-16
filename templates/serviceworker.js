importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');
workbox.routing.registerRoute(
  ({url}) => url.origin === 'https://example.com',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'roadscache1.0',
    plugins: [
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [200],
      }),
    ],
  })
);