import reflex as rx

class SlideToAnyWhere(rx.State):
    """State para deslizar pantalla a cualquier parte de la página."""

    def scroll_to_suplements(self):
        """Deslizar a la sección de suplementos."""
        return rx.call_script("document.getElementById('suplementos').scrollIntoView({behavior: 'smooth'})")
    
    def scroll_to_skin_care(self):
        """Deslizar a la sección de cuidado de la piel."""
        return rx.call_script("document.getElementById('cuidado_piel').scrollIntoView({behavior: 'smooth'})")

    def scroll_to_disinfectants(self):
        """Deslizar a la sección de desinfectantes."""
        return rx.call_script("document.getElementById('desinfectantes').scrollIntoView({behavior: 'smooth'})")