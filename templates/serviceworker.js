
importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.1.5/workbox-sw.js');
// Set up Workbox
workbox.setConfig({
  debug: true, // Enable logging
});

// Precache your assets (optional)
workbox.precaching.precacheAndRoute([]);
// Use StaleWhileRevalidate strategy for caching
workbox.routing.registerRoute(
  new RegExp('/static'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'my-cache-2', // Change this to a unique name
    plugins: [
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200], // Cache responses with these status codes
      }),
    ],
  })
);