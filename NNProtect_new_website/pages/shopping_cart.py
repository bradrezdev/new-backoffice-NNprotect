"""Nueva Backoffice NN Protect | Carrito de compras"""

import reflex as rx
from ..theme import Custom_theme
from rxconfig import config
from ..layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, header

def shopping_cart() -> rx.Component:
    # Datos de ejemplo para productos en el carrito
    cart_items = [
        {
            "id": 1,
            "name": "NN Protect Basic",
            "price": 250.00,
            "quantity": 2,
            "volume_points": 50,
            "image": "/product_1.png",
            "subtotal": 500.00,
            "volume_subtotal": 100
        },
        {
            "id": 2,
            "name": "NN Protect Premium",
            "price": 450.00,
            "quantity": 1,
            "volume_points": 90,
            "image": "/product_2.png",
            "subtotal": 450.00,
            "volume_subtotal": 90
        },
        {
            "id": 3,
            "name": "NN Protect Pro",
            "price": 350.00,
            "quantity": 3,
            "volume_points": 70,
            "image": "/product_3.png",
            "subtotal": 1050.00,
            "volume_subtotal": 210
        }
    ]

    # Cálculos del carrito
    total_products = sum(item["quantity"] for item in cart_items)
    subtotal_products = sum(item["subtotal"] for item in cart_items)
    total_volume_points = sum(item["volume_subtotal"] for item in cart_items)
    shipping_cost = 99.00 if subtotal_products < 1000 else 0.00
    final_total = subtotal_products + shipping_cost

    return rx.center(
        # Versión desktop - dejada en blanco según requerimiento
        rx.desktop_only(),

        # Versión móvil - implementación completa
        rx.mobile_only(
            rx.vstack(
                # Header móvil
                mobile_header(),

                # Contenido principal móvil
                rx.vstack(

                    # Título principal
                    rx.text(
                        "Carrito de compras",
                        size="8",
                        font_weight="bold",
                    ),

                    rx.text(
                        f"{total_products} producto{'s' if total_products != 1 else ''} en tu carrito",
                        font_size="0.9rem",
                        color="gray",
                        margin_bottom="1.5em",
                        text_align="center"
                    ),

                    # Lista de productos en el carrito
                    rx.vstack(
                        *[rx.box(
                            rx.hstack(
                                # Imagen del producto
                                rx.box(
                                    rx.image(
                                        src=item["image"],
                                        height="60px",
                                        width="60px",
                                        object_fit="contain",
                                        border_radius="13px",
                                        bg="rgba(0,0,0,0.05)"
                                    ),
                                    border_radius="8px",
                                    overflow="hidden"
                                ),

                                # Información del producto
                                rx.vstack(
                                    rx.text(
                                        item["name"],
                                        font_weight="semibold",
                                        font_size="0.9rem",
                                        line_height="1.2"
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            f"${item['price']:.2f}",
                                            font_size="0.8rem",
                                            color=Custom_theme().light_colors()["primary"],
                                            font_weight="medium"
                                        ),
                                        rx.text(
                                            f"• {item['volume_points']} pts",
                                            font_size="0.8rem",
                                            color="gray"
                                        ),
                                        spacing="1",
                                        align="center"
                                    ),
                                    rx.text(
                                        f"Subtotal: ${item['subtotal']:.2f}",
                                        font_size="0.8rem",
                                        font_weight="medium",
                                        color="#059669"
                                    ),
                                    spacing="1",
                                    align="start",
                                    flex="1"
                                ),

                                # Controles de cantidad y eliminar
                                rx.vstack(
                                    # Controles de cantidad
                                    rx.hstack(
                                        rx.button(
                                            rx.icon("minus", size=12),
                                            size="1",
                                            variant="soft",
                                            border_radius="6px",
                                            min_width="28px",
                                            height="28px",
                                            _hover={"bg": "rgba(239, 68, 68, 0.1)"}
                                        ),
                                        rx.box(
                                            rx.text(
                                                str(item["quantity"]),
                                                font_size="0.8rem",
                                                font_weight="medium",
                                                text_align="center"
                                            ),
                                            min_width="32px",
                                            height="28px",
                                            border_radius="6px",
                                            bg=rx.color_mode_cond(
                                                light="rgba(0,0,0,0.05)",
                                                dark="rgba(255,255,255,0.1)"
                                            ),
                                            display="flex",
                                            align_items="center",
                                            justify_content="center"
                                        ),
                                        rx.button(
                                            rx.icon("plus", size=12),
                                            size="1",
                                            variant="soft",
                                            border_radius="6px",
                                            min_width="28px",
                                            height="28px",
                                            _hover={"bg": "rgba(34, 197, 94, 0.1)"}
                                        ),
                                        spacing="1",
                                        align="center"
                                    ),

                                    # Botón eliminar
                                    rx.button(
                                        rx.icon("trash-2", size=14),
                                        variant="ghost",
                                        size="1",
                                        border_radius="6px",
                                        padding="6px",
                                        _hover={"bg": "rgba(239, 68, 68, 0.1)"},
                                        margin_top="0.5em"
                                    ),

                                    spacing="1",
                                    align="center"
                                ),

                                spacing="3",
                                align="start",
                                width="100%"
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="29px",
                            padding="16px",
                            border="1px solid rgba(0,0,0,0.05)",
                            margin_bottom="12px",
                            width="100%"
                        ) for item in cart_items],

                        spacing="0",
                        width="100%",
                        margin_bottom="2em"
                    ),

                    # Espacio para el box flotante
                    rx.box(height="200px"),

                    # Propiedades del vstack principal móvil
                    margin="80px 0 20px 0",
                    width="100%",
                    padding="0 1em",
                ),

                # Box flotante con resumen - posicionado fixed
                rx.box(
                    rx.vstack(
                        # Línea divisoria superior
                        rx.box(
                            width="60px",
                            height="4px",
                            bg="rgba(0,0,0,0.2)",
                            border_radius="2px",
                            margin="0 auto 1em auto"
                        ),

                        # Resumen del pedido
                        rx.vstack(
                            # Productos
                            rx.hstack(
                                rx.text(f"Productos ({total_products})", font_size="0.9rem", color="gray"),
                                rx.spacer(),
                                rx.text(f"${subtotal_products:.2f}", font_size="0.9rem", font_weight="medium"),
                                width="100%",
                                align="center"
                            ),

                            # Puntos de volumen
                            rx.hstack(
                                rx.text("Puntos de volumen", font_size="0.9rem", color="gray"),
                                rx.spacer(),
                                rx.text(f"{total_volume_points} pts", font_size="0.9rem", font_weight="medium", color="#f59e0b"),
                                width="100%",
                                align="center"
                            ),

                            # Costo de envío
                            rx.hstack(
                                rx.text("Costo de envío", font_size="0.9rem", color="gray"),
                                rx.spacer(),
                                rx.cond(
                                    shipping_cost == 0,
                                    rx.text("GRATIS", font_size="0.9rem", font_weight="medium", color="#059669"),
                                    rx.text(f"${shipping_cost:.2f}", font_size="0.9rem", font_weight="medium")
                                ),
                                width="100%",
                                align="center"
                            ),

                            # Línea divisoria
                            rx.box(
                                height="1px",
                                bg="rgba(0,0,0,0.1)",
                                width="100%",
                                margin="0.5em 0"
                            ),

                            # Total
                            rx.hstack(
                                rx.text("Total", font_size="1rem", font_weight="bold"),
                                rx.spacer(),
                                rx.text(f"${final_total:.2f}", font_size="1rem", font_weight="bold", color=Custom_theme().light_colors()["primary"]),
                                width="100%",
                                align="center"
                            ),

                            spacing="1",
                            width="100%"
                        ),

                        # Botones de acción
                        rx.vstack(
                            rx.link(
                                rx.button(
                                    "Proceder al envío",
                                    align="center",
                                    bg=Custom_theme().light_colors()["primary"],
                                    color="white",
                                    size="4",
                                    border_radius="15px",
                                    padding="16px",
                                    width="100%",
                                    _hover={"opacity": 0.9, "transform": "translateY(-1px)"},
                                    transition="all 0.2s ease",
                                ),
                                width="100%",
                                href="/shipment_method",
                            ),

                            spacing="2",
                            width="100%",
                            margin_top="1em"
                        ),
                        spacing="0",
                        width="100%"
                    ),

                    # Estilos del box flotante
                    bg=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["tertiary"],
                        dark=Custom_theme().dark_colors()["tertiary"]
                    ),
                    border_radius="29px 29px 0 0",
                    padding="20px",
                    box_shadow="0 -4px 12px rgba(0, 0, 0, 0.1)",
                    border_top="1px solid rgba(0,0,0,0.05)",
                    position="fixed",
                    bottom="0",
                    left="0",
                    right="0",
                    z_index="100",
                    width="100%",
                    max_width="100vw"
                ),
                width="100%",
            ),
            width="100%",
        ),

        # Propiedades del contenedor principal
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),
        position="absolute",
        width="100%",
    )