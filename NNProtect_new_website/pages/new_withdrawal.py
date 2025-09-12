"""Nueva Backoffice NN Protect | Solicitud de retiro"""

import reflex as rx
from ..theme import Custom_theme
from rxconfig import config
from ..layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar

def new_withdrawal() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    desktop_sidebar(),
                    # Container de la derecha. Contiene el formulario de registro.
                    main_container_derecha(
                        rx.vstack(
                            # Encabezado de la página
                            rx.text(
                                "Solicitud de retiro",
                                font_size="2rem",
                                font_weight="bold",
                                margin_bottom="0.5em"
                            ),
                            # Contenedor del formulario
                            rx.box(
                                rx.vstack(
                                    # Monto a retirar
                                    rx.vstack(
                                        rx.text("Monto a retirar", font_size="1rem", font_weight="semibold"),
                                        rx.input(
                                            placeholder="Ingrese el monto a retirar",
                                            type="number",
                                            padding="12px",
                                            border_radius="8px",
                                            border=f"1px solid {Custom_theme().light_colors()['border']}",
                                            _focus={
                                                "border": f"2px solid {Custom_theme().light_colors()['primary']}"
                                            },
                                        ),
                                        width="100%",
                                        margin_bottom="1em"
                                    ),
                                    # Método de retiro
                                    rx.vstack(
                                        rx.text("Método de retiro", font_size="1rem", font_weight="semibold"),
                                        rx.select(
                                            ["Cuenta bancaria 1", "Cuenta bancaria 2", "Cuenta bancaria 3"],
                                            placeholder="Seleccione un método de retiro",
                                            padding="12px",
                                            border_radius="8px",
                                            border=f"1px solid {Custom_theme().light_colors()['border']}",
                                            _focus={
                                                "border": f"2px solid {Custom_theme().light_colors()['primary']}"
                                            },
                                        ),
                                        width="100%",
                                        margin_bottom="1em"
                                    ),
                                    # Botón de enviar solicitud
                                    rx.button(
                                        "Enviar solicitud",
                                        bg=Custom_theme().light_colors()["primary"],
                                        color="white",
                                        padding="12px",
                                        border_radius="8px",
                                        _hover={"opacity": 0.9},
                                        width="100%",
                                    )
                                ),
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                                border_radius="24px",
                                padding="32px",
                                width="100%",
                            ),
                            # Propiedades del contenedor del formulario
                            width="100%",
                        ),
                    )
                ),
                # Propiedades vstack que contiene el contenido de la página.
                justify="center",
                margin_top="120px",
                margin_bottom="0.2em",
                max_width="1440px",
            )
        ),

        # Versión móvil
        rx.mobile_only(
            rx.vstack(
                # Header móvil
                mobile_header(),

                # Contenido principal móvil
                rx.vstack(
                    rx.text(
                        "Retiros",
                        font_size="1.5rem",
                        font_weight="bold",
                        margin_bottom="0.5em",
                        margin_top="1em",
                    ),
                    rx.box(
                        rx.html(
                            '<iframe src="/withdrawals.html" width="100%" height="552px" style="border:none;"></iframe>'
                        ),
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["tertiary"],
                            dark=Custom_theme().dark_colors()["tertiary"]
                        ),
                        border_radius="24px",
                        margin_bottom="32px",
                        padding="16px",
                        min_width="240px",
                        width="100%",
                    ),
                    # Propiedades del vstack principal móvil
                    width="100%",
                    padding="16px",
                )
            )
        ),
        width="100vw",
        height="100%",
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"],
        ),
    )