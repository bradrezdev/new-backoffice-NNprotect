"""Nueva Backoffice NN Protect | Compras"""

import reflex as rx
from ..theme import Custom_theme
from rxconfig import config
from ..layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, header

def order_details() -> rx.Component:
    return rx.center(
        rx.desktop_only(
            rx.vstack(
                header(),
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
                                        rx.badge("Pendiente", color_scheme="orange", font_size="0.8em", border_radius="12px", padding="0.2em 1em"),
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
                                            bg="#6B7280" + "70",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("Programado", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("package-open", size=24, color="#FFFFFF"),
                                            bg="#6B7280" + "70",
                                            border_radius="50%",
                                            padding="10px",
                                        ),
                                        rx.text("En preparación", font_size="0.8em", color="#6B7280"),
                                        align="center",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("truck", size=24, color="#FFFFFF"),
                                            bg="#6B7280" + "70",
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

                            width="100%",
                        ),
                    )
                ),
                align="end",
                margin_top="8em",
                margin_bottom="0.2em",
                max_width="1920px",
            )
        ),

        rx.mobile_only(
            rx.vstack(
                # Header móvil
                mobile_header(),
                
                # Contenido principal móvil
                rx.vstack(
                    rx.text(
                        "Compras",
                        font_size="1.5rem",
                        font_weight="bold",
                        margin_bottom="1rem",
                        text_align="center"
                    ),
                    
                    # Lista de órdenes móvil
                    *[rx.box(
                        rx.vstack(
                            # Encabezado de orden
                            rx.hstack(
                                rx.text(f"Orden #{orden_id}", font_weight="bold", font_size="1rem"),
                                rx.text(total, font_weight="bold", font_size="1rem", color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["secondary"],
                                    dark=Custom_theme().light_colors()["secondary"]
                                )),
                                justify="between",
                                width="100%"
                            ),
                            
                            rx.divider(margin_y="0.5rem"),
                            
                            # Detalles de la orden
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("calendar", size=16, color="#6B7280"),
                                    rx.text(fecha, font_size="0.8rem", color="#6B7280"),
                                    spacing="1"
                                ),
                                rx.hstack(
                                    rx.icon("credit-card", size=16, color="#6B7280"),
                                    rx.text(metodo, font_size="0.8rem", color="#6B7280"),
                                    spacing="1"
                                ),
                                rx.hstack(
                                    rx.icon("truck", size=16, color="#6B7280"),
                                    rx.text(estado_envio, font_size="0.8rem", color="#6B7280"),
                                    spacing="1"
                                ),
                                spacing="2",
                                width="100%"
                            ),
                            
                            rx.divider(margin_y="0.5rem"),
                            
                            # Productos
                            rx.text("Productos:", font_weight="600", font_size="0.9rem"),
                            *[rx.hstack(
                                rx.text(f"• {producto}", font_size="0.85rem"),
                                rx.text(f"x{cantidad}", font_size="0.85rem", color="gray"),
                                rx.spacer(),
                                rx.text(precio, font_size="0.85rem", font_weight="600"),
                                width="100%"
                            ) for producto, cantidad, precio in productos],
                            
                            # Botón de detalles
                            rx.button(
                                "Ver detalles",
                                size="2",
                                width="100%",
                                variant="soft",
                                margin_top="0.5rem"
                            ),
                            
                            spacing="2",
                            width="100%"
                        ),
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["tertiary"],
                            dark=Custom_theme().dark_colors()["tertiary"]
                        ),
                        border_radius="12px",
                        padding="1rem",
                        width="100%",
                        margin_bottom="1rem"
                    ) for orden_id, total, fecha, metodo, estado_envio, productos in [
                        ("12345", "$1,746.50", "10 sept 2025 - 09:53", "Tarjeta de crédito", "En camino", 
                        [("Producto 1", "2", "$500.00"), ("Producto 2", "1", "$746.50"), ("Producto 3", "3", "$500.00")]),
                        ("12344", "$2,890.00", "8 sept 2025 - 14:20", "PayPal", "Entregado",
                        [("Producto 4", "1", "$1,890.00"), ("Producto 5", "2", "$1,000.00")]),
                    ]],
                    
                    spacing="4",
                    width="100%",
                    padding="1rem",
                    margin_top="80px",
                    margin_bottom="2rem"
                ),
            ),
            width="100%",
        ),

        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),
        width="100%",
        position="absolute",
    )