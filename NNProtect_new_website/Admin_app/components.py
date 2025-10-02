"""
Componentes reutilizables para Admin App
"""

import reflex as rx
from .theme import COLORS, CARD_STYLE, INPUT_STYLE, SELECT_STYLE, BUTTON_STYLE, BADGE_STYLE, HEADING_STYLE


def admin_card(title: str, *children, **kwargs) -> rx.Component:
    """Card con título y contenido"""
    return rx.box(
        rx.heading(title, **HEADING_STYLE["h3"]),
        rx.divider(margin_y="1rem", border_color=COLORS["gray_200"]),
        *children,
        **CARD_STYLE,
        **kwargs
    )


def admin_input(
    label: str,
    placeholder: str = "",
    value = None,
    on_change = None,
    input_type: str = "text",
    **kwargs
) -> rx.Component:
    """Input con label - estilo mobile"""
    return rx.vstack(
        rx.text(
            label,
            font_weight="600",
            font_size="0.9375rem",
            color=COLORS["gray_700"],
        ),
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            type=input_type,
            border_radius="15px",
            height="48px",
            width="100%",
            font_size="1rem",
            background=COLORS["bg_input"],
            border=f"2px solid {COLORS['gray_200']}",
            padding="0.875rem 1rem",
            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            color=COLORS["gray_900"],
            _focus={
                "outline": "none",
                "border_color": COLORS["primary"],
                "box_shadow": f"0 0 0 4px {COLORS['primary_ultra_light']}",
            },
            _hover={
                "border_color": COLORS["gray_300"],
            },
            **kwargs
        ),
        spacing="2",
        width="100%",
        align_items="start"
    )


def admin_select(
    label: str,
    options: list,
    value = None,
    on_change = None,
    **kwargs
) -> rx.Component:
    """Select con label - estilo mobile"""
    return rx.vstack(
        rx.text(
            label,
            font_weight="600",
            font_size="0.9375rem",
            color=COLORS["gray_700"],
        ),
        rx.select(
            options,
            value=value,
            on_change=on_change,
            radius="large",
            size="3",
            background=COLORS["bg_input"],
            width="100%",
            **kwargs
        ),
        spacing="2",
        width="100%",
        align_items="start"
    )


def admin_button(
    text: str,
    on_click = None,
    variant: str = "primary",
    **kwargs
) -> rx.Component:
    """Botón con variantes"""
    return rx.button(
        text,
        on_click=on_click,
        **BUTTON_STYLE.get(variant, BUTTON_STYLE["primary"]),
        **kwargs
    )


def admin_badge(text: str, variant: str = "info") -> rx.Component:
    """Badge de estado"""
    return rx.box(
        text,
        **BADGE_STYLE.get(variant, BADGE_STYLE["info"])
    )


def admin_stat_card(label: str, value: str, icon: str = "📊") -> rx.Component:
    """Card de estadística"""
    return rx.box(
        rx.hstack(
            rx.text(icon, font_size="2rem"),
            rx.vstack(
                rx.text(
                    label,
                    font_size="0.875rem",
                    color=COLORS["gray_600"],
                    font_weight="500"
                ),
                rx.text(
                    value,
                    font_size="1.5rem",
                    font_weight="700",
                    color=COLORS["gray_900"]
                ),
                spacing="0",
                align_items="start"
            ),
            spacing="4",
            align_items="center"
        ),
        **CARD_STYLE,
        padding="1rem"
    )


def admin_alert(message: str, variant: str = "info") -> rx.Component:
    """Alerta de mensaje"""
    bg_colors = {
        "success": f"{COLORS['success']}10",
        "warning": f"{COLORS['warning']}10",
        "error": f"{COLORS['error']}10",
        "info": f"{COLORS['info']}10",
    }

    border_colors = {
        "success": COLORS['success'],
        "warning": COLORS['warning'],
        "error": COLORS['error'],
        "info": COLORS['info'],
    }

    icons = {
        "success": "✓",
        "warning": "⚠",
        "error": "✕",
        "info": "ℹ",
    }

    return rx.box(
        rx.hstack(
            rx.text(
                icons.get(variant, "ℹ"),
                font_size="1.25rem"
            ),
            rx.text(
                message,
                font_weight="500",
                font_size="0.875rem"
            ),
            spacing="3",
            align_items="center"
        ),
        background=bg_colors.get(variant, bg_colors["info"]),
        border_left=f"4px solid {border_colors.get(variant, border_colors['info'])}",
        padding="0.75rem 1rem",
        border_radius="0.5rem",
        width="100%"
    )


def admin_section_header(title: str, subtitle: str = "") -> rx.Component:
    """Header de sección"""
    return rx.vstack(
        rx.heading(title, **HEADING_STYLE["h2"]),
        rx.cond(
            subtitle != "",
            rx.text(
                subtitle,
                color=COLORS["gray_600"],
                font_size="0.875rem"
            )
        ),
        spacing="1",
        align_items="start",
        width="100%",
        margin_bottom="1.5rem"
    )


def admin_form_group(*children, columns: int = 1) -> rx.Component:
    """Grupo de inputs en grid"""
    return rx.box(
        *children,
        display="grid",
        grid_template_columns=f"repeat({columns}, 1fr)",
        gap="1rem",
        width="100%"
    )


def admin_divider() -> rx.Component:
    """Divider con estilo"""
    return rx.divider(
        margin_y="1.5rem",
        border_color=COLORS["gray_200"]
    )
