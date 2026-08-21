/* Service Worker — PWA Cité de la Miséricorde (§25)
 * Stratégies :
 *  - Pré-cache des pages clés (Accueil, À propos, Contact)
 *  - Cache First, Network Fallback pour les assets statiques
 *  - Page hors-ligne (offline fallback)
 */
const CACHE_NAME = "cite-misericorde-v1";
const PRECACHE_URLS = [
  "/",
  "/a-propos/",
  "/notre-mission/",
  "/contact/",
  "/static/css/main.css",
  "/static/js/app.js",
  "/static/manifest.json",
  "/static/img/icon-192.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // Assets statiques : Cache First, Network Fallback
  if (url.pathname.startsWith("/static/")) {
    event.respondWith(
      caches.match(request).then(
        (cached) =>
          cached ||
          fetch(request).then((response) => {
            const copy = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
            return response;
          })
      )
    );
    return;
  }

  // Pages : Network First, cache fallback, sinon page hors-ligne
  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          return response;
        })
        .catch(() =>
          caches.match(request).then((cached) => cached || caches.match("/offline/"))
        )
    );
    return;
  }

  // Autres : cache d'abord puis réseau
  event.respondWith(
    caches.match(request).then(
      (cached) =>
        cached ||
        fetch(request).then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          return response;
        })
    )
  );
});
