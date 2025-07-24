import reflex as rx
from .theme import Custom_theme
from .state import desktop_sidebar, mobile_sidebar

def main_container_derecha(*children):
    return rx.box(
        rx.vstack(
            *children,
        ),
        margin_left="32px",
        width="60vw",
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
    ),