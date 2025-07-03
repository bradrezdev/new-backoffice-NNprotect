import reflex as rx

def main_container_derecha(*children):
    return rx.box(
        rx.vstack(
            *children,
        ),
        margin_left="32px",
        width="60vw",
    )