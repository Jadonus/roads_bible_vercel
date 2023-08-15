// Name of the cache
const CACHE_NAME = 'my-app-cache-v1';

// Files to cache
const urlsToCache = [
  // Add more files and routes as needed
];

// URLs to exclude from caching
const excludedUrls = [
  '/dashboard',
  '/accounts/login',
  '/accounts/logout',
  '/accounts/signup',
  '/'
];

self.addEventListener('install', function (event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function (event) {
  event.respondWith(
    isExcludedUrl(event.request.url) ?
      fetch(event.request) :
      caches.match(event.request)
        .then(function (response) {
          // Cache hit - return response
          if (response) {
            return response;
          }
          return fetch(event.request).then(
            function (response) {
              // Check if we received a valid response
              if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }

              // IMPORTANT: Clone the response. A response is a stream
              // and because we want the browser to consume the response
              // as well as the cache consuming the response, we need
              // to clone it so we have two streams.
              var responseToCache = response.clone();

              caches.open(CACHE_NAME)
                .then(function (cache) {
                  cache.put(event.request, responseToCache);
                });

              return response;
            }
          );
        })
  );
});

self.addEventListener('activate', function (event) {

  var cacheWhitelist = [CACHE_NAME];

  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames.map(function (cacheName) {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Utility function to check if a URL is in the excluded URLs list
function isExcludedUrl(url) {
  for (let i = 0; i < excludedUrls.length; i++) {
    if (url === excludedUrls[i] || url.startsWith(excludedUrls[i] + '/')) {
      return true;
    }
  }
  return false;
}
