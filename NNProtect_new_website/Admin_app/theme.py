"""
Tema y colores para Admin App - Diseño minimalista morado y gris
"""

import reflex as rx

class Custom_theme():
    def light_colors(self):
        return {
            "primary": "#0039F2",
            "secondary": "#5E79FF",
            "tertiary": "#FFFFFF",
            "background": "#F2F3F8",
            "traslucid-background": "rgba(255, 255, 255, 0.5)",
            "traslucid-background-blue": "rgba(0, 57, 242, 0.8)",
            "text": "#000000",
            "border": "#0039F2",
            "box_shadow": "0px 0px 16px 3px #5E79FF10",
            "success": "#10B981",
            "success_light": "#D1FAE5",
            "warning": "#F59E0B",
            "warning_light": "#FEF3C7",
            "error": "#EF4444",
            "error_light": "#FEE2E2",
            "info": "#3B82F6",
            "info_light": "#DBEAFE",
        }
    
    def dark_colors(self):
        return {
            "primary": "#0039F2",
            "secondary": "#5E79FF",
            "tertiary": "#1C1C1E",
            "background": "#000000",
            "traslucid-background": "rgba(0, 0, 0, 0.6)",
            "text": "#FFFFFF",
            "border": "#D8B4FE",
            "box_shadow": "0px 0px 16px 2px #1A155C90",
            "success": "#10B981",
            "success_light": "#D1FAE5",
            "warning": "#F59E0B",
            "warning_light": "#FEF3C7",
            "error": "#EF4444",
            "error_light": "#FEE2E2",
            "info": "#3B82F6",
            "info_light": "#DBEAFE",
        }

# Estilos comunes - Refinados con sombras y transiciones suaves
BUTTON_STYLE = {
    "primary": {
        "background": rx.color_mode_cond(
            light=Custom_theme().light_colors()["primary"],
            dark=Custom_theme().dark_colors()["primary"]
        ),
        "color": "white",
        "padding": "0.75rem 1.75rem",
        "border_radius": "0.625rem",
        "font_weight": "600",
        "font_size": "0.9375rem",
        "cursor": "pointer",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "box_shadow": "0 4px 6px -1px rgba(124, 58, 237, 0.2), 0 2px 4px -1px rgba(124, 58, 237, 0.1)",
        "_hover": {
            "background": rx.color_mode_cond(
                light=Custom_theme().light_colors()["secondary"],
                dark=Custom_theme().dark_colors()["secondary"]
            ),
            "transform": "translateY(-2px)",
            "box_shadow": "0 10px 15px -3px rgba(124, 58, 237, 0.3), 0 4px 6px -2px rgba(124, 58, 237, 0.15)",
        },
        "_active": {
            "transform": "translateY(0)",
        },
        "border": "none",
    },
    "secondary": {
        "background": rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"]
        ),
        "color": "white",
        "padding": "0.75rem 1.75rem",
        "border_radius": "0.625rem",
        "font_weight": "600",
        "font_size": "0.9375rem",
        "cursor": "pointer",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "box_shadow": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "_hover": {
            "background": rx.color_mode_cond(
                light=Custom_theme().light_colors()["secondary"],
                dark=Custom_theme().dark_colors()["secondary"]
            ),
            "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        },
        "border": "none",
    },
    "outline": {
        "background": "white",
        "color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["primary"],
            dark=Custom_theme().dark_colors()["primary"]
        ),
        "padding": "0.75rem 1.75rem",
        "border_radius": "0.625rem",
        "font_weight": "600",
        "font_size": "0.9375rem",
        "cursor": "pointer",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "border": f"2px solid {rx.color_mode_cond(
            light=Custom_theme().light_colors()["primary"],
            dark=Custom_theme().dark_colors()["primary"]
        )}",
        "box_shadow": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "_hover": {
            "background": rx.color_mode_cond(
                light=Custom_theme().light_colors()["secondary"],
                dark=Custom_theme().dark_colors()["secondary"]
            ),
            "box_shadow": "0 4px 6px -1px rgba(124, 58, 237, 0.1), 0 2px 4px -1px rgba(124, 58, 237, 0.06)",
        },
    },
}

CARD_STYLE = {
    "background": rx.color_mode_cond(
        light=Custom_theme().light_colors()["tertiary"],
        dark=Custom_theme().dark_colors()["tertiary"]
    ),
    "padding": "2rem",
    "border_radius": "1rem",
    "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)",
    "border": f"1px solid {rx.color_mode_cond(
        light=Custom_theme().light_colors()["border"],
        dark=Custom_theme().dark_colors()["border"]
    )}",
    "transition": "box-shadow 0.3s ease",
    "_hover": {
        "box_shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04)",
    },
}

INPUT_STYLE = {


    "border_radius": "16px",
    "padding": "0.875rem 1rem",
    "width": "100%",
    "font_size": "0.9375rem",
    "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
    "color": rx.color_mode_cond(
        light=Custom_theme().light_colors()["text"],
        dark=Custom_theme().dark_colors()["text"]
    ),
    "_placeholder": {
        "color": rx.color_mode_cond(
            light="#9CA3AF",
            dark="#4B5563"
        ),
    },
    "_focus": {
        "outline": "none",
        "border_color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["border"],
            dark=Custom_theme().dark_colors()["border"]
        ),
        "box_shadow": f"0 0 0 4px {rx.color_mode_cond(
            light=Custom_theme().light_colors()["box_shadow"],
            dark=Custom_theme().dark_colors()["box_shadow"]
        )}, 0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "background": rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"]
        ),
    },
    "_hover": {
        "border_color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["border"],
            dark=Custom_theme().dark_colors()["border"]
        ),
    },
}

SELECT_STYLE = {
    "background": rx.color_mode_cond(
        light=Custom_theme().light_colors()["tertiary"],
        dark=Custom_theme().dark_colors()["tertiary"]
    ),
    "border": f"2px solid {rx.color_mode_cond(
        light=Custom_theme().light_colors()["border"],
        dark=Custom_theme().dark_colors()["border"]
    )}",
    "border_radius": "0.625rem",
    "padding": "0.875rem 1rem",
    "width": "100%",
    "font_size": "0.9375rem",
    "cursor": "pointer",
    "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
    "color": rx.color_mode_cond(
        light=Custom_theme().light_colors()["text"],
        dark=Custom_theme().dark_colors()["text"]
    ),
    "_focus": {
        "outline": "none",
        "border_color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["border"],
            dark=Custom_theme().dark_colors()["border"]
        ),
        "box_shadow": f"0 0 0 4px {rx.color_mode_cond(
            light=Custom_theme().light_colors()["box_shadow"],
            dark=Custom_theme().dark_colors()["box_shadow"]
        )}, 0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    },
    "_hover": {
        "border_color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["border"],
            dark=Custom_theme().dark_colors()["border"]
        ),
    },
}

HEADING_STYLE = {
    "h1": {
        "font_size": "2.25rem",
        "font_weight": "800",
        "color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["text"],
            dark=Custom_theme().dark_colors()["text"]
        ),
        "margin_bottom": "0.5rem",
        "letter_spacing": "-0.025em",
    },
    "h2": {
        "font_size": "1.75rem",
        "font_weight": "700",
        "color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["text"],
            dark=Custom_theme().dark_colors()["text"]
        ),
        "margin_bottom": "0.5rem",
        "letter_spacing": "-0.015em",
    },
    "h3": {
        "font_size": "1.375rem",
        "font_weight": "600",
        "color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["text"],
            dark=Custom_theme().dark_colors()["text"]
        ),
        "margin_bottom": "0.5rem",
    },
}

BADGE_STYLE = {
    "success": {
        "background": rx.color_mode_cond(
            light=Custom_theme().light_colors()["success_light"],
            dark=Custom_theme().dark_colors()["success_light"]
        ),
        "color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["success"],
            dark=Custom_theme().dark_colors()["success"]
        ),
        "padding": "0.375rem 0.875rem",
        "border_radius": "9999px",
        "font_size": "0.8125rem",
        "font_weight": "600",
        "border": f"1px solid {rx.color_mode_cond(
            light=Custom_theme().light_colors()["success"],
            dark=Custom_theme().dark_colors()["success"]
        )}40",
    },
    "warning": {
        "background": rx.color_mode_cond(
            light=Custom_theme().light_colors()["warning_light"],
            dark=Custom_theme().dark_colors()["warning_light"]
        ),
        "color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["warning"],
            dark=Custom_theme().dark_colors()["warning"]
        ),
        "padding": "0.375rem 0.875rem",
        "border_radius": "9999px",
        "font_size": "0.8125rem",
        "font_weight": "600",
        "border": f"1px solid {rx.color_mode_cond(
            light=Custom_theme().light_colors()["warning"],
            dark=Custom_theme().dark_colors()["warning"]
        )}40",
    },
    "error": {
        "background": rx.color_mode_cond(
            light=Custom_theme().light_colors()["error_light"],
            dark=Custom_theme().dark_colors()["error_light"]
        ),
        "color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["error"],
            dark=Custom_theme().dark_colors()["error"]
        ),
        "padding": "0.375rem 0.875rem",
        "border_radius": "9999px",
        "font_size": "0.8125rem",
        "font_weight": "600",
        "border": f"1px solid {rx.color_mode_cond(
            light=Custom_theme().light_colors()["error"],
            dark=Custom_theme().dark_colors()["error"]
        )}40",
    },
    "info": {
        "background": rx.color_mode_cond(
            light=Custom_theme().light_colors()["info_light"],
            dark=Custom_theme().dark_colors()["info_light"]
        ),
        "color": rx.color_mode_cond(
            light=Custom_theme().light_colors()["info"],
            dark=Custom_theme().dark_colors()["info"]
        ),
        "padding": "0.375rem 0.875rem",
        "border_radius": "9999px",
        "font_size": "0.8125rem",
        "font_weight": "600",
        "border": f"1px solid {rx.color_mode_cond(
            light=Custom_theme().light_colors()["info"],
            dark=Custom_theme().dark_colors()["info"]
        )}40",
    },
}
