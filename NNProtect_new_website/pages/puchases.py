"""Nueva Backoffice NN Protect | Compras"""

import reflex as rx
from ..theme import Custom_theme
from rxconfig import config
from ..layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, logged_in_user

def purchases() -> rx.Component:
    return rx.center(
        rx.desktop_only(
            rx.vstack(
                logged_in_user(),
                rx.hstack(
                    desktop_sidebar(),
                    main_container_derecha(
                        rx.vstack(
                            rx.text(
                                "Compras",
                                font_size="2rem",
                                font_weight="bold",
                            ),

                            # Contenedor de una orden
                            rx.box(
                                rx.hstack(
                                    rx.heading(
                                        "Orden #12345",
                                        size="6",
                                    ),
                                    rx.heading(
                                        "$1746.50 MXN",
                                        color=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["secondary"],
                                            dark=Custom_theme().light_colors()["secondary"],
                                        ),
                                        size="6",
                                    ),
                                    justify="between",
                                    margin_bottom="1em"
                                ),
                                rx.separator(
                                    orientation="horizontal",
                                    margin_bottom="1em"
                                ),

                                # Detalles de la compra
                                rx.flex(
                                    rx.flex(
                                        rx.hstack(
                                            rx.icon("calendar", size=20, color="#6B7280"),
                                            rx.text(
                                                "10 de septiembre de 2025 - 09:53",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        rx.hstack(
                                            rx.icon("map-pinned", size=20, color="#6B7280"),
                                            rx.text(
                                                "México",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        rx.hstack(
                                            rx.icon("credit-card", size=20, color="#6B7280"),
                                            rx.text(
                                                "Tarjeta de crédito",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        rx.hstack(
                                            rx.icon("container", size=20, color="#6B7280"),
                                            rx.text(
                                                "CEDIS: Oficina de Guadalajara",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        spacing="5",
                                        direction="row",
                                    ),
                                    rx.flex(
                                        rx.badge("Pagado", color_scheme="green", font_size="0.8em", border_radius="12px", padding="0.2em 1em"),
                                        rx.button(
                                            rx.icon("download", size=16),
                                            "PDF",
                                            variant="outline",
                                            color_scheme="blue",
                                            font_size="0.8em",
                                            border_radius="24px",
                                        ),
                                        spacing="3",
                                        direction="column",
                                    ),
                                    justify="between",
                                    direction="row",
                                    margin_bottom="3em"
                                ),

                                # Estado del pedido
                                rx.flex(
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("clipboard-clock", size=24, color="#FFFFFF"),
                                            bg="#E1E115",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Programado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("package-open", size=24, color="#FFFFFF"),
                                            bg="#B4D012",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("En preparación", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("truck", size=24, color="#FFFFFF"),
                                            bg="#64D012",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Enviado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("package-check", size=24, color="#FFFFFF"),
                                            #bg="#0BD43A",
                                            bg="#6B7280" + "70",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Entregado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    spacing="9",
                                    justify="center",
                                    width="100%",
                                    direction="row",
                                ),

                                rx.separator(
                                    margin="1em 0 1em 0"
                                ),

                                # Productos comprados
                                rx.text(
                                    "Productos",
                                    font_size="1rem",
                                    font_weight="bold",
                                    margin_bottom="1em",
                                ),

                                rx.vstack(

                                    # Detalle de un producto comprado
                                    rx.flex(
                                        rx.vstack(
                                            rx.text("Citrus Nanodispersión 30 ml", font_size="1em", font_weight="bold"),
                                            rx.flex(
                                                rx.text("Cantidad: 1", font_size="0.8em", color="#6B7280"),
                                                rx.text("Precio unitario: $349.30 MXN", font_size="0.8em", color="#6B7280"),
                                                rx.text("293 PV por producto", font_size="0.8em", color="#6B7280"),
                                                spacing="3",
                                            ),
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                "$349.30 MXN",
                                                font_size="1em",
                                                font_weight="bold"
                                            ),
                                            rx.badge(
                                                "293 PV",
                                                color_scheme="green",
                                                font_size="0.8em",
                                                border_radius="12px",
                                            ),
                                            align="end",
                                        ),
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["background"],
                                            dark=Custom_theme().dark_colors()["background"]
                                        ),
                                        border_radius="16px",
                                        padding="1em",
                                        width="100%",
                                        justify="between",
                                    ),

                                    # Detalle de otro producto comprado
                                    rx.flex(
                                        rx.vstack(
                                            rx.text("Chia Nanodispersión 30 ml", font_size="1em", font_weight="bold"),
                                            rx.flex(
                                                rx.text("Cantidad: 1", font_size="0.8em", color="#6B7280"),
                                                rx.text("Precio unitario: $349.30 MXN", font_size="0.8em", color="#6B7280"),
                                                rx.text("293 PV por producto", font_size="0.8em", color="#6B7280"),
                                                spacing="3",
                                            ),
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                "$349.30 MXN",
                                                font_size="1em",
                                                font_weight="bold"
                                            ),
                                            rx.badge(
                                                "293 PV",
                                                color_scheme="green",
                                                font_size="0.8em",
                                                border_radius="12px",
                                            ),
                                            align="end",
                                        ),
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["background"],
                                            dark=Custom_theme().dark_colors()["background"]
                                        ),
                                        border_radius="16px",
                                        padding="1em",
                                        width="100%",
                                        justify="between",
                                    ),

                                    # Detalle de un producto comprado
                                    rx.flex(
                                        rx.vstack(
                                            rx.text("Jengibre Nanodispersión 30 ml", font_size="1em", font_weight="bold"),
                                            rx.flex(
                                                rx.text("Cantidad: 2", font_size="0.8em", color="#6B7280"),
                                                rx.text("Precio unitario: $349.30 MXN", font_size="0.8em", color="#6B7280"),
                                                rx.text("293 PV por producto", font_size="0.8em", color="#6B7280"),
                                                spacing="3",
                                            ),
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                "$698.60 MXN",
                                                font_size="1em",
                                                font_weight="bold"
                                            ),
                                            rx.badge(
                                                "586 PV",
                                                color_scheme="green",
                                                font_size="0.8em",
                                                border_radius="12px",
                                            ),
                                            align="end",
                                        ),
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["background"],
                                            dark=Custom_theme().dark_colors()["background"]
                                        ),
                                        border_radius="16px",
                                        padding="1em",
                                        width="100%",
                                        justify="between",
                                    ),

                                    # Detalle de otro producto comprado
                                    rx.flex(
                                        rx.vstack(
                                            rx.text("Granada Nanodispersión 30 ml", font_size="1em", font_weight="bold"),
                                            rx.flex(
                                                rx.text("Cantidad: 1", font_size="0.8em", color="#6B7280"),
                                                rx.text("Precio unitario: $349.30 MXN", font_size="0.8em", color="#6B7280"),
                                                rx.text("293 PV por producto", font_size="0.8em", color="#6B7280"),
                                                spacing="3",
                                            ),
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                "$349.30 MXN",
                                                font_size="1em",
                                                font_weight="bold"
                                            ),
                                            rx.badge(
                                                "293 PV",
                                                color_scheme="green",
                                                font_size="0.8em",
                                                border_radius="12px",
                                            ),
                                            align="end",
                                        ),
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["background"],
                                            dark=Custom_theme().dark_colors()["background"]
                                        ),
                                        border_radius="16px",
                                        padding="1em",
                                        width="100%",
                                        justify="between",
                                    ),

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
                            
                            # Contenedor de otra orden
                            rx.box(
                                rx.hstack(
                                    rx.heading(
                                        "Orden #67890",
                                        size="6",
                                    ),
                                    rx.heading(
                                        "$1926.50 MXN",
                                        color=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["secondary"],
                                            dark=Custom_theme().light_colors()["secondary"],
                                        ),
                                        size="6",
                                    ),
                                    justify="between",
                                    margin_bottom="1em"
                                ),
                                rx.separator(
                                    orientation="horizontal",
                                    margin_bottom="1em"
                                ),

                                # Detalles de la compra
                                rx.flex(
                                    rx.flex(
                                        rx.hstack(
                                            rx.icon("calendar", size=20, color="#6B7280"),
                                            rx.text(
                                                "01 de agosto de 2025 - 19:32",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        rx.hstack(
                                            rx.icon("map-pinned", size=20, color="#6B7280"),
                                            rx.text(
                                                "República Dominicana",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        rx.hstack(
                                            rx.icon("credit-card", size=20, color="#6B7280"),
                                            rx.text(
                                                "Billetera digital",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        rx.hstack(
                                            rx.icon("container", size=20, color="#6B7280"),
                                            rx.text(
                                                "Domicilio del cliente",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        spacing="5",
                                        direction="row",
                                    ),
                                    rx.flex(
                                        rx.badge("Pagado", color_scheme="green", font_size="0.8em", border_radius="12px", padding="0.2em 1em"),
                                        rx.button(
                                            rx.icon("download", size=16),
                                            "PDF",
                                            variant="outline",
                                            color_scheme="blue",
                                            font_size="0.8em",
                                            border_radius="24px",
                                        ),
                                        spacing="3",
                                        direction="column",
                                    ),
                                    justify="between",
                                    direction="row",
                                    margin_bottom="3em"
                                ),

                                # Estado del pedido
                                rx.flex(
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("clipboard-clock", size=24, color="#FFFFFF"),
                                            bg="#E1E115",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Programado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("package-open", size=24, color="#FFFFFF"),
                                            bg="#B4D012",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("En preparación", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("truck", size=24, color="#FFFFFF"),
                                            bg="#64D012",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Enviado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("package-check", size=24, color="#FFFFFF"),
                                            bg="#0BD43A",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Entregado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    spacing="9",
                                    justify="center",
                                    width="100%",
                                    direction="row",
                                ),

                                rx.separator(
                                    margin="1em 0 1em 0"
                                ),

                                # Productos comprados
                                rx.text(
                                    "Productos",
                                    font_size="1rem",
                                    font_weight="bold",
                                    margin_bottom="1em",
                                ),

                                rx.vstack(
                                    rx.flex(
                                        rx.vstack(
                                            rx.text("Citrus Nanodispersión 30 ml", font_size="1em"),
                                            rx.flex(
                                                rx.text("Cantidad: 1", font_size="0.8em", color="#6B7280"),
                                                rx.text("Precio unitario: $349.30 MXN", font_size="0.8em", color="#6B7280"),
                                                rx.text("293 PV por producto", font_size="0.8em", color="#6B7280"),
                                                spacing="3",
                                            ),
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                "$349.30 MXN",
                                                font_size="1em",
                                                font_weight="bold"
                                            ),
                                            rx.badge(
                                                "293 PV",
                                                color_scheme="green",
                                                font_size="0.8em",
                                                border_radius="12px",
                                            ),
                                            align="end",
                                        ),
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["background"],
                                            dark=Custom_theme().dark_colors()["background"]
                                        ),
                                        border_radius="16px",
                                        padding="1em",
                                        width="100%",
                                        justify="between",
                                    ),
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

                            # Contenedor de otra orden
                            rx.box(
                                rx.hstack(
                                    rx.heading(
                                        "Orden #11121",
                                        size="6",
                                    ),
                                    rx.heading(
                                        "$1746.50 MXN",
                                        color=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["secondary"],
                                            dark=Custom_theme().light_colors()["secondary"],
                                        ),
                                        size="6",
                                    ),
                                    justify="between",
                                    margin_bottom="1em"
                                ),
                                rx.separator(
                                    orientation="horizontal",
                                    margin_bottom="1em"
                                ),

                                # Detalles de la compra
                                rx.flex(
                                    rx.flex(
                                        rx.hstack(
                                            rx.icon("calendar", size=20, color="#6B7280"),
                                            rx.text(
                                                "10 de septiembre de 2025 - 09:53",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        rx.hstack(
                                            rx.icon("map-pinned", size=20, color="#6B7280"),
                                            rx.text(
                                                "México",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        rx.hstack(
                                            rx.icon("credit-card", size=20, color="#6B7280"),
                                            rx.text(
                                                "Tarjeta de crédito",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        rx.hstack(
                                            rx.icon("container", size=20, color="#6B7280"),
                                            rx.text(
                                                "CEDIS: Oficina de Guadalajara",
                                                font_size="0.9em",
                                                color="#6B7280"
                                            ),
                                        ),
                                        spacing="5",
                                        direction="row",
                                    ),
                                    rx.flex(
                                        rx.badge("Pagado", color_scheme="green", font_size="0.8em", border_radius="12px", padding="0.2em 1em"),
                                        rx.button(
                                            rx.icon("download", size=16),
                                            "PDF",
                                            variant="outline",
                                            color_scheme="blue",
                                            font_size="0.8em",
                                            border_radius="24px",
                                        ),
                                        spacing="3",
                                        direction="column",
                                    ),
                                    justify="between",
                                    direction="row",
                                    margin_bottom="3em"
                                ),

                                # Estado del pedido
                                rx.flex(
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("clipboard-clock", size=24, color="#FFFFFF"),
                                            bg="#E1E115",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Programado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("package-open", size=24, color="#FFFFFF"),
                                            bg="#B4D012",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("En preparación", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("truck", size=24, color="#FFFFFF"),
                                            bg="#64D012",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Enviado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("package-check", size=24, color="#FFFFFF"),
                                            #bg="#0BD43A",
                                            bg="#6B7280" + "70",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Entregado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    spacing="9",
                                    justify="center",
                                    width="100%",
                                    direction="row",
                                ),

                                rx.separator(
                                    margin="1em 0 1em 0"
                                ),

                                # Productos comprados
                                rx.text(
                                    "Productos",
                                    font_size="1rem",
                                    font_weight="bold",
                                    margin_bottom="1em",
                                ),

                                rx.vstack(
                                    rx.flex(
                                        rx.vstack(
                                            rx.text("Citrus Nanodispersión 30 ml", font_size="1em"),
                                            rx.flex(
                                                rx.text("Cantidad: 1", font_size="0.8em", color="#6B7280"),
                                                rx.text("Precio unitario: $349.30 MXN", font_size="0.8em", color="#6B7280"),
                                                rx.text("293 PV por producto", font_size="0.8em", color="#6B7280"),
                                                spacing="3",
                                            ),
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                "$349.30 MXN",
                                                font_size="1em",
                                                font_weight="bold"
                                            ),
                                            rx.badge(
                                                "293 PV",
                                                color_scheme="green",
                                                font_size="0.8em",
                                                border_radius="12px",
                                            ),
                                            align="end",
                                        ),
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["background"],
                                            dark=Custom_theme().dark_colors()["background"]
                                        ),
                                        border_radius="16px",
                                        padding="1em",
                                        width="100%",
                                        justify="between",
                                    ),
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

                            width="100%",
                        ),
                    )
                ),
                align="end",
                margin_top="8em",
                margin_bottom="2em",
                max_width="1920px",
            )
        ),
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),
        width="100%",
        position="absolute",
    )