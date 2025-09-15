# === Archivo: status_bar.py ===
# Módulo para manejo del status bar con degradado negro a transparente

import reflex as rx

def pwa_meta_tags():
	"""
	Genera todos los meta tags necesarios para PWA con status bar personalizado.
	Retorna una lista de elementos meta para agregar al head de cada página.
	"""
	return [
		# === Meta tags básicos PWA ===
		rx.el.meta(
			name="viewport", 
			content="width=device-width, initial-scale=1.0, viewport-fit=cover"
		),
		
		# === Theme colors para Android ===
		rx.el.meta(name="theme-color", content="#000000"),
		rx.el.meta(
			name="theme-color", 
			content="#000000", 
			media="(prefers-color-scheme: light)"
		),
		rx.el.meta(
			name="theme-color", 
			content="#1a1a1a", 
			media="(prefers-color-scheme: dark)"
		),
		
		# === iOS Safari específico ===
		rx.el.meta(name="apple-mobile-web-app-capable", content="yes"),
		rx.el.meta(
			name="apple-mobile-web-app-status-bar-style", 
			content="black-translucent"
		),
		rx.el.meta(name="apple-mobile-web-app-title", content="NN Protect"),
		
		# === PWA manifest y iconos ===
		rx.el.link(rel="manifest", href="/manifest.json"),
		rx.el.link(rel="apple-touch-icon", href="/icons/icon-192x192.png"),
		rx.el.link(rel="icon", type="image/png", sizes="32x32", href="/icons/icon-192x192.png"),
		
		# === Service Worker ===
		rx.script("""
			// Registrar Service Worker para PWA
			if ('serviceWorker' in navigator) {
				window.addEventListener('load', function() {
					navigator.serviceWorker.register('/sw.js')
						.then(function(registration) {
							console.log('✅ Service Worker registrado:', registration.scope);
						})
						.catch(function(error) {
							console.log('❌ Error registrando Service Worker:', error);
						});
				});
			}
		""")
	]

def status_bar_css():
	"""
	CSS personalizado para crear el degradado de negro a transparente en el status bar.
	"""
	return rx.el.style("""
		/* === Variables CSS para el status bar === */
		:root {
			--status-bar-height: env(safe-area-inset-top, 44px);
			--gradient-start: rgba(0, 0, 0, 0.8);
			--gradient-end: rgba(0, 0, 0, 0);
		}
		
		/* === Ajustes globales para PWA === */
		html, body {
			margin: 0;
			padding: 0;
			height: 100%;
			overflow-x: hidden;
		}
		
		/* === Fondo del status bar con degradado === */
		.status-bar-gradient {
			position: fixed;
			top: 0;
			left: 0;
			right: 0;
			height: calc(var(--status-bar-height) + 60px);
			background: linear-gradient(
				to bottom,
				var(--gradient-start) 0%,
				rgba(0, 0, 0, 0.4) 50%,
				var(--gradient-end) 100%
			);
			z-index: -1;  /* ← CAMBIO PRINCIPAL: Detrás del contenido */
			pointer-events: none;
			backdrop-filter: blur(8px);
			-webkit-backdrop-filter: blur(8px);
		}
		
		/* === Contenedor principal que respeta el status bar === */
		.main-app-container {
			padding-top: var(--status-bar-height);
			min-height: 100vh;
			position: relative;
			z-index: 1;  /* ← NUEVO: Asegurar que esté encima del degradado */
		}
		
		/* === Soporte para notch en dispositivos modernos === */
		@supports (padding: max(0px)) {
			:root {
				--status-bar-height: max(env(safe-area-inset-top), 44px);
			}
		}
		
		/* === Fallback para iOS 11 === */
		@supports (padding: constant(safe-area-inset-top)) {
			:root {
				--status-bar-height: max(constant(safe-area-inset-top), 44px);
			}
		}
		
		/* === Ajustes para header móvil existente === */
		.mobile-header-with-statusbar {
			margin-top: var(--status-bar-height);
			position: relative;
			z-index: 2;  /* ← NUEVO: Header encima de todo */
		}
		
		/* === Prevenir contenido detrás del status bar === */
		.content-with-statusbar {
			padding-top: calc(var(--status-bar-height) + 20px);
			position: relative;
			z-index: 1;  /* ← NUEVO: Contenido encima del degradado */
		}
		
		/* === Animación suave para cambios de orientación === */
		.status-bar-gradient {
			transition: height 0.3s ease;
		}
		
		/* === Responsive para orientación landscape === */
		@media (orientation: landscape) and (max-width: 896px) {
			:root {
				--status-bar-height: env(safe-area-inset-top, 20px);
			}
		}
	""")

def status_bar_overlay():
	"""
	Componente que crea el overlay visual del degradado en el status bar.
	Este componente debe agregarse al inicio de cada página.
	"""
	return rx.el.div(class_name="status-bar-gradient")

def status_bar_script():
	"""
	JavaScript para manejar cambios dinámicos del status bar.
	"""
	return rx.script("""
		// === Manejo dinámico del status bar ===
		class StatusBarManager {
			constructor() {
				this.init();
			}
			
			init() {
				this.handleOrientationChange();
				this.handleResize();
			}
			
			// Manejar cambios de orientación
			handleOrientationChange() {
				window.addEventListener('orientationchange', () => {
					setTimeout(() => {
						this.adjustStatusBarHeight();
					}, 500);
				});
			}
			
			// Manejar cambios de tamaño de ventana
			handleResize() {
				window.addEventListener('resize', () => {
					this.adjustStatusBarHeight();
				});
			}
			
			// Ajustar altura del status bar dinámicamente
			adjustStatusBarHeight() {
				const statusBarElement = document.querySelector('.status-bar-gradient');
				if (statusBarElement) {
					// Forzar recálculo de CSS variables
					statusBarElement.style.display = 'none';
					statusBarElement.offsetHeight; // Trigger reflow
					statusBarElement.style.display = 'block';
				}
			}
			
			// Método público para cambiar la intensidad del degradado
			setGradientIntensity(intensity) {
				const root = document.documentElement;
				root.style.setProperty('--gradient-start', `rgba(0, 0, 0, ${intensity})`);
			}
		}
		
		// Inicializar cuando el DOM esté listo
		document.addEventListener('DOMContentLoaded', function() {
			window.statusBarManager = new StatusBarManager();
			console.log('✅ Status Bar Manager inicializado');
		});
	""")

def wrap_page_with_statusbar(page_content):
	"""
	Envuelve el contenido de una página con el status bar.
	
	Args:
		page_content: El contenido de la página (componente Reflex)
	
	Returns:
		Página envuelta con status bar y estilos necesarios
	"""
	return rx.fragment(
		# CSS del status bar
		status_bar_css(),
		
		# Overlay del degradado
		status_bar_overlay(),
		
		# Contenido de la página en contenedor que respeta el status bar
		rx.el.div(
			page_content,
			class_name="main-app-container"
		),
		
		# JavaScript del status bar
		status_bar_script()
	)

# === Funciones auxiliares ===

def get_safe_area_padding():
	"""Retorna el padding necesario para evitar el notch"""
	return {
		"padding_top": "var(--status-bar-height)",
		"box_sizing": "border-box"
	}

def mobile_header_with_statusbar():
	"""
	Versión del mobile header que considera el status bar.
	Úsala en lugar del mobile_header() original para páginas con status bar.
	"""
	return rx.el.div(
		# Aquí va tu mobile_header() existente
		class_name="mobile-header-with-statusbar"
	)