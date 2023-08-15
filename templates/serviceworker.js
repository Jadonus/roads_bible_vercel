importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.2.0/workbox-sw.js');

const CACHE_NAME = 'my-app-cache-v2';

// URLs to exclude from caching
const excludedUrls = [
  '{% url "/" %}',
  '/dashboard/',
  '/accounts/login/',
  '/accounts/logout/',
  '/accounts/signup/',
];

// Configure Workbox to use the cache name
workbox.core.setCacheNameDetails({ prefix: CACHE_NAME });

// Exclude specific URLs from caching
workbox.routing.registerRoute(
  ({ url }) => isExcludedUrl(url.pathname),
  new workbox.strategies.NetworkOnly()
);

// Cache other requests using the Stale-While-Revalidate strategy
workbox.routing.registerRoute(
  ({ url }) => !isExcludedUrl(url.pathname),
  new workbox.strategies.StaleWhileRevalidate()
);

function isExcludedUrl(url) {
  return excludedUrls.some(function (excludedUrl) {
    return url === excludedUrl;
  });
}