"""Nueva Backoffice NN Protect | Método de pago"""

import reflex as rx
from ..shared_ui.theme import Custom_theme
from rxconfig import config
from ..shared_ui.layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, header

from ..product_service.store_products_state import CountProducts  # Importar estado del carrito

def payment() -> rx.Component:
    # 📦 EJEMPLO DE REUTILIZACIÓN DE DATOS DEL CARRITO
    # Usando CountProducts podemos acceder a toda la información
    # del carrito desde cualquier página de forma dinámica

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
                        "Método de pago",
                        size="8",
                        font_weight="bold",
                        text_align="center",
                    ),

                    rx.text(
                        "Selecciona cómo quieres pagar tu pedido",
                        size="2",
                        color="gray",
                        margin_bottom="2em",
                        text_align="center"
                    ),

                    # Opciones de pago disponibles
                    rx.vstack(
                        # Opción 1: Saldo en billetera
                        rx.box(
                            rx.hstack(
                                # Icono de billetera
                                rx.box(
                                    rx.icon("wallet", size=24, color="#059669"),
                                    width="48px",
                                    height="48px",
                                    bg="rgba(5, 150, 105, 0.1)",
                                    border_radius="12px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    margin_right="1em"
                                ),

                                # Información de la billetera
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Saldo en billetera", font_weight="semibold", size="3"),
                                        align="center",
                                        width="100%"
                                    ),

                                    rx.vstack(
                                        rx.text(
                                            "Saldo actual: $2,450.00 MXN",
                                            size="3",
                                            font_weight="medium",
                                            color="#059669"
                                        ),
                                        rx.text(
                                            "Pago instantáneo",
                                            size="1",
                                            color="gray"
                                        ),
                                        align="start",
                                        spacing="1"
                                    ),

                                    align="start",
                                    spacing="1",
                                    flex="1"
                                ),

                                align="start",
                                width="100%",
                                spacing="0"
                            ),

                            # Estilos de la tarjeta
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="29px",
                            padding="1em",
                            border="2px solid transparent",
                            _hover={"border": "2px solid #059669"},
                            transition="all 0.2s ease",
                            margin_bottom="16px",
                            width="100%",
                            cursor="pointer"
                        ),

                        # Opción 2: Tarjeta de Débito/Crédito
                        rx.box(
                            rx.hstack(
                                # Icono de tarjeta
                                rx.box(
                                    rx.icon("credit-card", size=24, color=Custom_theme().light_colors()["primary"]),
                                    width="48px",
                                    height="48px",
                                    bg=rx.color_mode_cond(
                                        light="rgba(0, 57, 242, 0.1)",
                                        dark="rgba(0, 57, 242, 0.2)"
                                    ),
                                    border_radius="12px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    margin_right="1em"
                                ),

                                # Información de tarjeta
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Tarjeta de Débito/Crédito", font_weight="semibold", size="3"),
                                        align="center",
                                        width="100%"
                                    ),

                                    rx.vstack(
                                        rx.text(
                                            "Visa, Mastercard, American Express",
                                            size="1",
                                            color="gray"
                                        ),
                                        align="start",
                                        spacing="1"
                                    ),

                                    align="start",
                                    spacing="1",
                                    flex="1"
                                ),

                                # Botón de selección (deshabilitado por ahora)
                                rx.box(
                                    rx.box(
                                        width="20px",
                                        height="20px",
                                        border_radius="50%",
                                        border="2px solid #d1d5db",
                                        bg="transparent",
                                        opacity="0.5",
                                        transition="all 0.2s ease"
                                    ),
                                    width="32px",
                                    height="32px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center"
                                ),

                                align="start",
                                width="100%",
                                spacing="0"
                            ),

                            # Estilos de la tarjeta
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="29px",
                            padding="1em",
                            border="2px solid transparent",
                            _hover={"border": "2px solid #d1d5db"},
                            transition="all 0.2s ease",
                            margin_bottom="16px",
                            width="100%",
                            cursor="not-allowed",
                            opacity="0.7"
                        ),

                        # Opción 3: Pago en OXXO
                        rx.box(
                            rx.hstack(
                                # Icono de OXXO
                                rx.box(
                                    rx.box(
                                        rx.text("OXXO", font_size="0.7rem", font_weight="bold", color="#d32f2f"),
                                        width="100%",
                                        height="100%",
                                        display="flex",
                                        align_items="center",
                                        justify_content="center"
                                    ),
                                    width="48px",
                                    height="48px",
                                    bg="rgba(211, 47, 47, 0.1)",
                                    border_radius="12px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    margin_right="1em"
                                ),

                                # Información de OXXO
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Pago en OXXO", font_weight="semibold", size="3"),
                                        align="center",
                                        width="100%"
                                    ),

                                    rx.vstack(
                                        rx.text(
                                            "Paga en cualquier tienda OXXO",
                                            size="1",
                                            color="gray"
                                        ),
                                        align="start",
                                        spacing="1"
                                    ),

                                    align="start",
                                    spacing="1",
                                    flex="1"
                                ),

                                align="start",
                                width="100%",
                                spacing="0"
                            ),

                            # Estilos de la tarjeta
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="29px",
                            padding="1em",
                            border="2px solid transparent",
                            _hover={"border": "2px solid #d32f2f"},
                            transition="all 0.2s ease",
                            margin_bottom="16px",
                            width="100%",
                            cursor="pointer"
                        ),

                        spacing="0",
                        width="100%",
                        margin_bottom="2em"
                    ),

                    # Métodos de pago alternativos
                    rx.vstack(
                        rx.text(
                            "Otros métodos",
                            size="4",
                            font_weight="semibold",
                            margin_bottom="1em",
                            text_align="center"
                        ),

                        # Pago en efectivo
                        rx.box(
                            rx.hstack(
                                rx.box(
                                    rx.icon("dollar-sign", size=24, color="#059669"),
                                    width="48px",
                                    height="48px",
                                    bg="rgba(5, 150, 105, 0.1)",
                                    border_radius="12px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    margin_right="1em"
                                ),

                                rx.vstack(
                                    rx.text("Pago en efectivo", font_weight="semibold", font_size="1rem"),
                                    rx.text(
                                        "Paga al recibir tu pedido",
                                        font_size="0.85rem",
                                        color="gray"
                                    ),
                                    align="start",
                                    spacing="1",
                                    flex="1"
                                ),

                                rx.box(
                                    rx.box(
                                        width="20px",
                                        height="20px",
                                        border_radius="50%",
                                        border="2px solid #059669",
                                        bg="transparent",
                                        _hover={"bg": "#059669"},
                                        transition="all 0.2s ease"
                                    ),
                                    width="32px",
                                    height="32px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center"
                                ),

                                align="start",
                                width="100%",
                                spacing="0"
                            ),

                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="16px",
                            padding="1em",
                            border="2px solid transparent",
                            _hover={"border": "2px solid #059669"},
                            transition="all 0.2s ease",
                            margin_bottom="12px",
                            width="100%",
                            cursor="pointer"
                        ),

                        # Pago con criptomonedas
                        rx.box(
                            rx.hstack(
                                rx.box(
                                    rx.icon("bitcoin", size=24, color="#f59e0b"),
                                    width="48px",
                                    height="48px",
                                    bg="rgba(245, 158, 11, 0.1)",
                                    border_radius="12px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    margin_right="1em"
                                ),

                                rx.vstack(
                                    rx.text("Criptomonedas", font_weight="semibold", font_size="1rem"),
                                    rx.text(
                                        "Bitcoin, Ethereum y más",
                                        font_size="0.85rem",
                                        color="gray"
                                    ),
                                    align="start",
                                    spacing="1",
                                    flex="1"
                                ),

                                rx.box(
                                    rx.box(
                                        width="20px",
                                        height="20px",
                                        border_radius="50%",
                                        border="2px solid #f59e0b",
                                        bg="transparent",
                                        _hover={"bg": "#f59e0b"},
                                        transition="all 0.2s ease"
                                    ),
                                    width="32px",
                                    height="32px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center"
                                ),

                                align="start",
                                width="100%",
                                spacing="0"
                            ),

                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="16px",
                            padding="1em",
                            border="2px solid transparent",
                            _hover={"border": "2px solid #f59e0b"},
                            transition="all 0.2s ease",
                            margin_bottom="12px",
                            width="100%",
                            cursor="pointer"
                        ),

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

                # Box flotante con resumen de pago - copiado de shopping_cart.py
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
                                rx.text(f"Productos ({CountProducts.cart_total})", font_size="0.9rem", color="gray"),
                                rx.spacer(),
                                rx.text(f"${CountProducts.cart_subtotal:.2f}", font_size="0.9rem", font_weight="medium"),
                                width="100%",
                                align="center"
                            ),

                            # Puntos de volumen
                            rx.hstack(
                                rx.text("Puntos de volumen", font_size="0.9rem", color="gray"),
                                rx.spacer(),
                                rx.text(f"{CountProducts.cart_volume_points} pts", font_size="0.9rem", font_weight="medium", color="#f59e0b"),
                                width="100%",
                                align="center"
                            ),

                            # Costo de envío
                            rx.hstack(
                                rx.text("Costo de envío", font_size="0.9rem", color="gray"),
                                rx.spacer(),
                                rx.cond(
                                    CountProducts.cart_shipping_cost == 0,
                                    rx.text("GRATIS", font_size="0.9rem", font_weight="medium", color="#059669"),
                                    rx.text(f"${CountProducts.cart_shipping_cost:.2f}", font_size="0.9rem", font_weight="medium")
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
                                rx.text(f"${CountProducts.cart_final_total:.2f}", font_size="1rem", font_weight="bold", color=Custom_theme().light_colors()["primary"]),
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
                                    "Confirmar pago",
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
                                href="/order_confirmation",  # Página de confirmación (por crear)
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
