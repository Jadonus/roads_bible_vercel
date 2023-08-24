// Import Workbox from CDN
importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.1.5/workbox-sw.js');

// Set up Workbox
workbox.setConfig({
  debug: true, // Enable logging
});

// Precache your assets (optional)
workbox.precaching.precacheAndRoute([]);

// Cache routes starting with /roads and /static
workbox.routing.registerRoute(
  new RegExp('/static'),
  new workbox.strategies.CacheFirst({
    cacheName: 'my-cache2', // Change this to a unique name
    plugins: [
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200], // Cache responses with these status codes
      }),
    ],
  })
);