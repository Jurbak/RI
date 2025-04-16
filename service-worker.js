const CACHE_NAME = "scrap-cache-v1";

const chapterUrls = Array.from({ length: 2334 }, (_, i) => `chapter/${i + 1}.html`);

const urlsToCache = [
  "index.html",
  "style.css",
  "output.html",
  "offline.html",
  ...chapterUrls
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
      .catch(() => {
        // fallback untuk halaman HTML
        if (event.request.destination === 'document') {
          return caches.match("offline.html");
        }
      })
  );
});
