"""
Tema y colores para Admin App - Diseño minimalista morado y gris
"""

# Paleta de colores morado y gris - Refinada
COLORS = {
    # Morados - Gradiente refinado
    "primary": "#7C3AED",          # Morado principal
    "primary_hover": "#6D28D9",    # Morado hover
    "primary_light": "#A78BFA",    # Morado claro
    "primary_dark": "#5B21B6",     # Morado oscuro
    "primary_ultra_light": "#EDE9FE", # Morado ultra claro para backgrounds

    # Grises - Escala refinada
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",
    "gray_900": "#111827",

    # Estados - Tonos refinados
    "success": "#10B981",
    "success_light": "#D1FAE5",
    "warning": "#F59E0B",
    "warning_light": "#FEF3C7",
    "error": "#EF4444",
    "error_light": "#FEE2E2",
    "info": "#3B82F6",
    "info_light": "#DBEAFE",

    # Fondos - Sutiles
    "bg_main": "#F8F9FA",
    "bg_card": "#FFFFFF",
    "bg_input": "#FFFFFF",
    "bg_hover": "#F9FAFB",
}

# Estilos comunes - Refinados con sombras y transiciones suaves
BUTTON_STYLE = {
    "primary": {
        "background": COLORS["primary"],
        "color": "white",
        "padding": "0.75rem 1.75rem",
        "border_radius": "0.625rem",
        "font_weight": "600",
        "font_size": "0.9375rem",
        "cursor": "pointer",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "box_shadow": "0 4px 6px -1px rgba(124, 58, 237, 0.2), 0 2px 4px -1px rgba(124, 58, 237, 0.1)",
        "_hover": {
            "background": COLORS["primary_hover"],
            "transform": "translateY(-2px)",
            "box_shadow": "0 10px 15px -3px rgba(124, 58, 237, 0.3), 0 4px 6px -2px rgba(124, 58, 237, 0.15)",
        },
        "_active": {
            "transform": "translateY(0)",
        },
        "border": "none",
    },
    "secondary": {
        "background": COLORS["gray_100"],
        "color": COLORS["gray_700"],
        "padding": "0.75rem 1.75rem",
        "border_radius": "0.625rem",
        "font_weight": "600",
        "font_size": "0.9375rem",
        "cursor": "pointer",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "box_shadow": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "_hover": {
            "background": COLORS["gray_200"],
            "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        },
        "border": "none",
    },
    "outline": {
        "background": "white",
        "color": COLORS["primary"],
        "padding": "0.75rem 1.75rem",
        "border_radius": "0.625rem",
        "font_weight": "600",
        "font_size": "0.9375rem",
        "cursor": "pointer",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "border": f"2px solid {COLORS['primary']}",
        "box_shadow": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "_hover": {
            "background": COLORS["primary_ultra_light"],
            "box_shadow": "0 4px 6px -1px rgba(124, 58, 237, 0.1), 0 2px 4px -1px rgba(124, 58, 237, 0.06)",
        },
    },
}

CARD_STYLE = {
    "background": COLORS["bg_card"],
    "padding": "2rem",
    "border_radius": "1rem",
    "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)",
    "border": f"1px solid {COLORS['gray_100']}",
    "transition": "box-shadow 0.3s ease",
    "_hover": {
        "box_shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04)",
    },
}

INPUT_STYLE = {
    "background": COLORS["bg_input"],
    "border": f"2px solid {COLORS['gray_200']}",
    "border_radius": "0.625rem",
    "padding": "0.875rem 1rem",
    "width": "100%",
    "font_size": "0.9375rem",
    "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
    "color": COLORS["gray_900"],
    "_placeholder": {
        "color": COLORS["gray_400"],
    },
    "_focus": {
        "outline": "none",
        "border_color": COLORS["primary"],
        "box_shadow": f"0 0 0 4px {COLORS['primary_ultra_light']}, 0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "background": COLORS["bg_card"],
    },
    "_hover": {
        "border_color": COLORS["gray_300"],
    },
}

SELECT_STYLE = {
    "background": COLORS["bg_input"],
    "border": f"2px solid {COLORS['gray_200']}",
    "border_radius": "0.625rem",
    "padding": "0.875rem 1rem",
    "width": "100%",
    "font_size": "0.9375rem",
    "cursor": "pointer",
    "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
    "color": COLORS["gray_900"],
    "_focus": {
        "outline": "none",
        "border_color": COLORS["primary"],
        "box_shadow": f"0 0 0 4px {COLORS['primary_ultra_light']}, 0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    },
    "_hover": {
        "border_color": COLORS["gray_300"],
    },
}

HEADING_STYLE = {
    "h1": {
        "font_size": "2.25rem",
        "font_weight": "800",
        "color": COLORS["gray_900"],
        "margin_bottom": "0.5rem",
        "letter_spacing": "-0.025em",
    },
    "h2": {
        "font_size": "1.75rem",
        "font_weight": "700",
        "color": COLORS["gray_800"],
        "margin_bottom": "0.5rem",
        "letter_spacing": "-0.015em",
    },
    "h3": {
        "font_size": "1.375rem",
        "font_weight": "600",
        "color": COLORS["gray_700"],
        "margin_bottom": "0.5rem",
    },
}

BADGE_STYLE = {
    "success": {
        "background": COLORS["success_light"],
        "color": COLORS["success"],
        "padding": "0.375rem 0.875rem",
        "border_radius": "9999px",
        "font_size": "0.8125rem",
        "font_weight": "600",
        "border": f"1px solid {COLORS['success']}40",
    },
    "warning": {
        "background": COLORS["warning_light"],
        "color": COLORS["warning"],
        "padding": "0.375rem 0.875rem",
        "border_radius": "9999px",
        "font_size": "0.8125rem",
        "font_weight": "600",
        "border": f"1px solid {COLORS['warning']}40",
    },
    "error": {
        "background": COLORS["error_light"],
        "color": COLORS["error"],
        "padding": "0.375rem 0.875rem",
        "border_radius": "9999px",
        "font_size": "0.8125rem",
        "font_weight": "600",
        "border": f"1px solid {COLORS['error']}40",
    },
    "info": {
        "background": COLORS["info_light"],
        "color": COLORS["info"],
        "padding": "0.375rem 0.875rem",
        "border_radius": "9999px",
        "font_size": "0.8125rem",
        "font_weight": "600",
        "border": f"1px solid {COLORS['info']}40",
    },
}
