import reflex as rx
from .theme import Custom_theme
from rxconfig import config

class State(rx.State):
    """The app state."""

def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )

def sidebar_items() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.image(src="/nnprotect_logo.png", height="5vh", position="top", margin="auto"),
            rx.spacer(),
            rx.spacer(),
            rx.spacer(),
            rx.spacer(),
            rx.spacer(),
            sidebar_item("Dashboard", "layout-dashboard", "/",),
            sidebar_item("Nuevo registro", "circle-plus", "/new_register"),
            sidebar_item("Red de usuarios", "network", "/network"),
            sidebar_item("Compras", "scroll-text", "/purchases"),
            sidebar_item("NN Travels", "plane", "/travels"),
            sidebar_item("Billetera", "wallet", "/wallet"),
            sidebar_item("Tickets/Soporte", "messages-square", "/tickets"),
            sidebar_item("Tienda", "store", "/store"),
            sidebar_item("Herramientas", "folder-cog", "/tools"),
            rx.button(
                "Cerrar sesión",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["secondary"],
                    dark=Custom_theme().light_colors()["secondary"],
                ),
                border_radius="16px",
                height="48px",
                margin_top="32px",
                width="100%",
            ),
            spacing="2",
            width="100%",
        ),
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"],
        ),
        #position="absolute",
        border_radius="36px",
        box_shadow=rx.color_mode_cond(
            light=Custom_theme().light_colors()["box_shadow"],
            dark=Custom_theme().dark_colors()["box_shadow"],
        ),
        justify="start",
        padding="40px 20px 40px 20px", # <- top, right, bottom, left
        height="auto",
        width="14vw",
        #z_index="100",
    )