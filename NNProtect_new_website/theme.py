'''Archivo que contiene los colores oficiales del tema personalizado de la página'''

import reflex as rx

class Custom_theme():
    def light_colors(self):
        return {
            "primary": "#0039F2",
            "secondary": "#5E79FF",
            "tertiary": "#FFFFFF",
            "background": "#F2F3F8",
            "text": "#000000",
            "border": "#0039F2",
            "box_shadow": "0px 0px 16px 3px #5E79FF10"
        }
    
    def dark_colors(self):
        return {
            "primary": "#0039F2",
            "secondary": "#5E79FF",
            "tertiary": "#1C1C1E",
            "background": "#000000",
            "text": "#FFFFFF",
            "border": "#D8B4FE",
            "box_shadow": "0px 0px 16px 2px #1A155C90"
        }