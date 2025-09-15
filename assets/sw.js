
// Service Worker para NN Protect PWA
const CACHE_NAME = 'nn-protect-v1';
const urlsToCache = [
	'/',
	'/manifest.json',
	'/logotipo.png',
	'/banner_dashboard.png'
];

// Instalar service worker
self.addEventListener('install', function(event) {
	event.waitUntil(
		caches.open(CACHE_NAME)
			.then(function(cache) {
				console.log('Cache abierto');
				return cache.addAll(urlsToCache);
			})
	);
	self.skipWaiting();
});

// Interceptar requests de red
self.addEventListener('fetch', function(event) {
	event.respondWith(
		caches.match(event.request)
			.then(function(response) {
				// Devolver desde cache si existe, sino fetch de red
				return response || fetch(event.request);
			})
	);
});

// Activar service worker
self.addEventListener('activate', function(event) {
	event.waitUntil(
		caches.keys().then(function(cacheNames) {
			return Promise.all(
				cacheNames.map(function(cacheName) {
					if (cacheName !== CACHE_NAME) {
						return caches.delete(cacheName);
					}
				})
			);
		})
	);
	self.clients.claim();
});
