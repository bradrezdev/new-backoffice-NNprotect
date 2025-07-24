import reflex as rx
from .theme import Custom_theme
from rxconfig import config

class State(rx.State):
    """The app state."""

#######################################
# --- Componentes para el sidebar --- #
#######################################

def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, font_size="1rem"),
            width="100%",
            padding_x="1rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5rem",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )

def sidebar_subitem(text: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.text(text, font_size="1rem"),
            width="100%",
            padding_x="1rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5rem",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )

def desktop_sidebar() -> rx.Component:
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
            rx.accordion.root(
                rx.accordion.item(
                    header=rx.hstack(rx.icon("network"), rx.text("Negocio")),
                    content=rx.vstack(
                        sidebar_subitem("Red de negocio", "/network"),
                        sidebar_subitem("Reportes de red", "/network_reports"),
                        sidebar_subitem("Detalles de comisiones", "/income_reports")
                    ),
                ),
                variant="ghost",
                collapsible=True,
                type="multiple",
                width="100%",
            ),
            # sidebar_item("Detalles de red", "network", "/network"),
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
        width="16vw",
        #z_index="100",
    )

def mobile_sidebar() -> rx.Component:
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
            rx.accordion.root(
                rx.accordion.item(
                    header=rx.hstack(rx.icon("network"), rx.text("Negocio")),
                    content=rx.vstack(
                        sidebar_subitem("Red de negocio", "/network"),
                        sidebar_subitem("Reportes de red", "/network_reports"),
                        sidebar_subitem("Detalles de comisiones", "/income_reports")
                    ),
                ),
                variant="ghost",
                collapsible=True,
                type="multiple",
                width="100%",
            ),
            # sidebar_item("Detalles de red", "network", "/network"),
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
        #top="auto",
        #right="auto",
        box_shadow=rx.color_mode_cond(
            light=Custom_theme().light_colors()["box_shadow"],
            dark=Custom_theme().dark_colors()["box_shadow"],
        ),
        #justify="start",
        padding="20px 10px 20px 10px", # <- top, right, bottom, left
        height="100%",
        width="80vw",
        z_index="100",
    )