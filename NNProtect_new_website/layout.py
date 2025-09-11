import reflex as rx
from .theme import Custom_theme

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
            sidebar_item("Dashboard", "layout-dashboard", "/"),
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
        border_radius="36px",
        box_shadow=rx.color_mode_cond(
            light=Custom_theme().light_colors()["box_shadow"],
            dark=Custom_theme().dark_colors()["box_shadow"],
        ),
        justify="start",
        padding="40px 20px 40px 20px",
        height="auto",
        width="16vw",
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
            sidebar_item("Dashboard", "layout-dashboard", "/"),
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
        box_shadow=rx.color_mode_cond(
            light=Custom_theme().light_colors()["box_shadow"],
            dark=Custom_theme().dark_colors()["box_shadow"],
        ),
        padding="20px 10px 20px 10px",
        height="100%",
        width="80vw",
        z_index="100",
    )

#######################################
# --- Contenedores principales ------- #
#######################################

def main_container_derecha(*children):
    return rx.box(
        rx.vstack(
            *children,
        ),
        #margin_left="px",
        width="80vw",  # Cambiado de 60vw a 100%
        flex="1",      # Para que ocupe el espacio restante
    )

def mobile_header():
    return rx.hstack(
        rx.drawer.root(
            rx.drawer.trigger(
                rx.button(
                    rx.icon("menu", size=20),
                    variant="ghost",
                    color=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["primary"],
                        dark=Custom_theme().dark_colors()["text"]
                    ),
                ),
            ),
            rx.drawer.overlay(z_index="500"),
            rx.drawer.portal(
                rx.drawer.content(
                    mobile_sidebar(),
                )
            ),
            direction="left",
        ),
        rx.spacer(),
        rx.heading("Dashboard", size="5"),
        rx.spacer(),
        rx.button(
            rx.icon("user", size=20),
            variant="ghost",
            color=rx.color_mode_cond(
                light=Custom_theme().light_colors()["primary"],
                dark=Custom_theme().dark_colors()["text"]
            )
        ),
        width="100%",
        padding="1rem",
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["traslucid-background"],
            dark=Custom_theme().dark_colors()["traslucid-background"]
        ),
        backdrop_filter="blur(30px)",
        position="fixed",
        top="0",
        z_index="1"
    )