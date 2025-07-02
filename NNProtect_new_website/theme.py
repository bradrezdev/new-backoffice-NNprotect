'''Archivo que contiene los colores oficiales del tema personalizado de la página'''

import reflex as rx

class Custom_theme():
    def light_colors(self):
        return {
            "primary": "#0026C0",
            "secondary": "#5E79FF",
            "tertiary": "#FFFFFF",
            "background": "#F2F3F8",
            "text": "#000000",
            "border": "#0026C0"
        }
    
    def dark_colors(self):
        return {
            "primary": "#7C3AED",
            "secondary": "#F3E8FF",
            "tertiary": "#1C1C1E",
            "background": "#000000",
            "text": "#FFFFFF",
            "border": "#D8B4FE",
        }