"""
Componentes reutilizables para Admin App
"""

import reflex as rx
from .theme import Custom_theme


def admin_card(title: str, *children, **kwargs) -> rx.Component:
    """Card con título y contenido"""
    return rx.box(
        rx.heading(title),
        rx.divider(margin_y="1rem", border_color=rx.color_mode_cond(
            light=Custom_theme().light_colors()["text"],
            dark=Custom_theme().dark_colors()["text"]
        )),
        *children,
        **kwargs
    )


def admin_input(
    label: str,
    on_change = None,
    input_type: str = "text",
    **kwargs
) -> rx.Component:
    """Input con label - estilo mobile"""
    return rx.vstack(
        rx.text(
            label,
            font_weight="medium",
            font_size="1em",
        ),
        rx.input(
            on_change=on_change,
            type=input_type,
            border_radius="15px",
            height="48px",
            width="100%",
            font_size="1rem",
            background=rx.color_mode_cond(
                light=Custom_theme().light_colors()["tertiary"],
                dark=Custom_theme().dark_colors()["tertiary"]
            ),
            padding="0.875rem 1rem",
            **kwargs
        ),
        spacing="2",
        width="100%",
        align_items="start"
    )


def admin_select(
    label: str,
    options: list,
    on_change = None,
    **kwargs
) -> rx.Component:
    """Select con label - estilo mobile"""
    return rx.vstack(
        rx.text(
            label,
            font_weight="medium",
            font_size="1em",
        ),
        rx.select(
            options,
            on_change=on_change,
            radius="large",
            size="3",
            background=rx.color_mode_cond(
                light=Custom_theme().light_colors()["tertiary"],
                dark=Custom_theme().dark_colors()["tertiary"]
            ),
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
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["primary"],
            dark=Custom_theme().dark_colors()["primary"]
        ),
        color="white",
        border_radius="24px",
        font_size="1.1em",
        font_weight="bold",
        on_click=on_click,
        **kwargs
    )


def admin_badge(text: str, variant: str = "info") -> rx.Component:
    """Badge de estado"""
    return rx.box(
        text,
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
                    font_weight="500"
                ),
                rx.text(
                    value,
                    font_size="1.5rem",
                    font_weight="700",
                ),
                spacing="0",
                align_items="start"
            ),
            spacing="4",
            align_items="center"
        ),
        padding="1rem"
    )


def admin_alert(message: str, variant: str = "info") -> rx.Component:
    """Alerta de mensaje"""
    bg_colors = {
        "success": f"{rx.color_mode_cond(light=Custom_theme().light_colors()['success'], dark=Custom_theme().dark_colors()['success'])}10",
        "warning": f"{rx.color_mode_cond(light=Custom_theme().light_colors()['warning'], dark=Custom_theme().dark_colors()['warning'])}10",
        "error": f"{rx.color_mode_cond(light=Custom_theme().light_colors()['error'], dark=Custom_theme().dark_colors()['error'])}10",
        "info": f"{rx.color_mode_cond(light=Custom_theme().light_colors()['info'], dark=Custom_theme().dark_colors()['info'])}10",
    }

    border_colors = {
        "success": rx.color_mode_cond(light=Custom_theme().light_colors()['success'], dark=Custom_theme().dark_colors()['success']),
        "warning": rx.color_mode_cond(light=Custom_theme().light_colors()['warning'], dark=Custom_theme().dark_colors()['warning']),
        "error": rx.color_mode_cond(light=Custom_theme().light_colors()['error'], dark=Custom_theme().dark_colors()['error']),
        "info": rx.color_mode_cond(light=Custom_theme().light_colors()['info'], dark=Custom_theme().dark_colors()['info']),
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
        rx.heading(title),
        rx.cond(
            subtitle != "",
            rx.text(
                subtitle,
                color=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["text"],
                    dark=Custom_theme().dark_colors()["text"]
                ),
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
        border_color=rx.color_mode_cond(
            light=Custom_theme().light_colors()["border"],
            dark=Custom_theme().dark_colors()["border"]
        )
    )
