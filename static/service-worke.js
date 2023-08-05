self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Clone the response to store in cache
        const clonedResponse = response.clone();
        caches.open('my-site-cache-v1')
          .then((cache) => cache.put(event.request, clonedResponse));
        return response;
      })
      .catch(() => {
        return caches.match(event.request);
      })
  );
});
