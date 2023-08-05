const cacheName = 'visited-pages';

self.addEventListener('install', async (event) => {
  event.waitUntil(
    caches.open(cacheName).then((cache) => {
      // Cache all of the pages that the user has visited so far.
      const visitedPages = await fetch('/api/visited_pages');
      const visitedPagesData = await visitedPages.json();
      for (const page of visitedPagesData) {
        cache.add(page);
      }
    })
  );
});

self.addEventListener('fetch', async (event) => {
  const request = event.request;

  // If the request is for a page that has already been visited, serve it from the cache.
  if (request.url.startsWith('/')) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      event.respondWith(cachedResponse);
      return;
    }
  }

  // Otherwise, fetch the resource from the network and cache it.
  event.respondWith(
    fetch(request).then((response) => {
      caches.open(cacheName).then((cache) => {
        cache.put(request, response);
      });
      return response;
    })
  );
});
