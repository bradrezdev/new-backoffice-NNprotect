"""
Componentes de productos para la tienda NN Protect.
Genera tarjetas de productos con datos reales de la base de datos.
"""
import reflex as rx
from typing import Dict
from ..shared_ui.theme import Custom_theme

from .store_products_state import CountProducts

def plusminus_buttons(product_id: int):
    """
    Botones con contador reactivo directo.
    Principio KISS: acceso directo a variables de estado.
    """
    return rx.hstack(
        rx.button(
            "-",
            size="1",
            variant="soft",
            border_radius="8px",
            min_width="36px",
            height="36px",
            on_click=lambda: CountProducts.decrement(product_id)
        ),
        rx.text(
            rx.match(
                product_id,
                (1, CountProducts.count_1),
                (2, CountProducts.count_2),
                (3, CountProducts.count_3),
                (4, CountProducts.count_4),
                (5, CountProducts.count_5),
                (6, CountProducts.count_6),
                (7, CountProducts.count_7),
                (8, CountProducts.count_8),
                (9, CountProducts.count_9),
                (10, CountProducts.count_10),
                (11, CountProducts.count_11),
                (12, CountProducts.count_12),
                (13, CountProducts.count_13),
                (14, CountProducts.count_14),
                (15, CountProducts.count_15),
                (16, CountProducts.count_16),
                (17, CountProducts.count_17),
                (18, CountProducts.count_18),
                (19, CountProducts.count_19),
                (20, CountProducts.count_20),
                (21, CountProducts.count_21),
                (22, CountProducts.count_22),
                (23, CountProducts.count_23),
                (24, CountProducts.count_24),
                0  # default
            ),
            font_size="0.9rem",
            font_weight="bold",
            min_width="40px",
            text_align="center"
        ),
        rx.button(
            "+",
            size="1", 
            variant="soft",
            border_radius="8px",
            min_width="36px",
            height="36px",
            on_click=lambda: CountProducts.increment(product_id)
        ),
        justify="center",
        spacing="2",
        align="center",
        margin_bottom="0.5em"
    )


def product_card(product_data: Dict, is_popular: bool = False) -> rx.Component:
    """
    Crea una tarjeta de producto con datos reales.
    Principio KISS: diseño simple y funcional.
    
    Args:
        product_data: Diccionario con datos del producto
        is_popular: Si mostrar badge de popular
        
    Returns:
        rx.Component: Tarjeta del producto
    """
    return rx.box(
        rx.vstack(
            # Badge de popular si aplica
            rx.cond(
                is_popular,
                rx.badge(
                    "⭐ Popular",
                    color_scheme="orange",
                    size="1",
                    position="absolute",
                    top="8px",
                    right="8px",
                    z_index="10"
                )
            ),

            # Imagen del producto (usar ID para consistencia)
            rx.image(
                src=f"/product_{product_data.get('id', 1)}.jpg",
                height="100%",
                width="100%",
                object_fit="cover",
                border_radius="19px",
                bg="rgba(0,0,0,0.05)",
                margin_bottom="0.5em",
                loading="lazy"  # Optimización de carga
            ),

            # Información del producto
            rx.vstack(
                rx.text(
                    product_data.get("name", "Producto"),
                    font_weight="bold",
                    font_size="0.9rem",
                    text_align="center",
                    no_of_lines=2
                ),
                rx.text(
                    product_data.get("formatted_price", "$0.00"),
                    font_weight="600",
                    font_size="0.9rem",
                    color=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["primary"],
                        dark=Custom_theme().dark_colors()["primary"]
                    ),
                    text_align="center"
                ),
                # Mostrar PV si está disponible
                rx.cond(
                    product_data.get("pv", 0) > 0,
                    rx.text(
                        f"PV: {product_data.get('pv', 0)}",
                        font_size="0.8rem",
                        color="gray",
                        text_align="center"
                    )
                ),
                spacing="1",
                align="center",
                width="100%"
            ),

            # Controles de cantidad
            plusminus_buttons(product_data.get("id", 1)),  # ✅ CORREGIDO: agregar paréntesis y product_id

            # Botón agregar
            rx.button(
                "Agregar",
                size="3",
                width="100%",
                variant="solid",
                border_radius="19px",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"]
                ),
                color="white",
                _hover={"opacity": 0.9},
                on_click=CountProducts.add_to_cart(product_data.get("id", 1))
            ),

            spacing="3",
            align="center",
            width="100%"
        ),
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"]
        ),
        border_radius="29px",
        padding="10px",
        width="45vw",  # Ancho consistente con diseño existente
        position="relative"
    )


def product_card_horizontal(product_data: Dict) -> rx.Component:
    """
    Tarjeta de producto para scroll horizontal (últimas novedades).
    Principio DRY: reutiliza estilos de product_card.
    """
    return rx.box(
        rx.vstack(
            # Imagen del producto
            rx.image(
                src=f"/product_{product_data.get('id', 4)}.jpg",
                height="100%",
                width="100%",
                object_fit="cover",
                border_radius="19px",
                bg="rgba(0,0,0,0.05)",
                margin_bottom="0.5em"
            ),

            # Información del producto
            rx.vstack(
                rx.text(
                    product_data.get("name"),
                    font_weight="bold",
                    font_size="1em",
                    text_align="center",
                    no_of_lines=2,
                ),
                rx.text(
                    product_data.get("formatted_price"),
                    font_weight="600",
                    font_size="0.9em",
                    color=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["primary"],
                        dark=Custom_theme().dark_colors()["secondary"]
                    ),
                    text_align="center"
                ),
                z_index=1,
                spacing="1",
                align="center",
                width="100%"
            ),

            # Controles de cantidad
            plusminus_buttons(product_data.get("id", 1)),  # ✅ CORREGIDO: agregar paréntesis y product_id

            # Botón agregar más pequeño
            rx.button(
                "Agregar",
                size="3",
                width="100%",
                variant="solid",
                border_radius="19px",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"]
                ),
                color="white",
                _hover={"opacity": 0.9},
                on_click=CountProducts.add_to_cart(product_data.get("id", 1))
            ),
            spacing="3",
            align="center",
            width="100%"
        ),
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"]
        ),
        border_radius="19px",
        padding="8px",
        min_height="360px",
        width="65vw",
        flex_shrink="0"  # Importante para scroll horizontal
    )


def new_products_card(product_data: Dict) -> rx.Component:
    """
    Tarjeta de producto para la sección "Últimas novedades".
    Principio DRY: hereda propiedades de product_card_horizontal.
    """
    return rx.box(
        rx.vstack(
            # Badge de nuevo
            rx.badge(
                "Nuevo producto",
                color_scheme="green",
                size="2",
                border_radius="12px",
                position="absolute",
                top="12px",
                right="12px",
                z_index="10"
            ),

            # Imagen del producto
            rx.image(
                src=f"/product_{product_data.get('id', 4)}.jpg",
                height="100%",
                width="100%",
                object_fit="cover",
                border_radius="15px",
                bg="rgba(0,0,0,0.05)",
                margin_bottom="0.5em"
            ),

            # Información del producto
            rx.vstack(
                rx.text(
                    product_data.get("name"),
                    font_weight="bold",
                    font_size="1em",
                    text_align="center",
                    no_of_lines=2,
                ),
                rx.text(
                    product_data.get("formatted_price"),
                    font_weight="600",
                    font_size="0.9em",
                    color=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["primary"],
                        dark=Custom_theme().dark_colors()["secondary"]
                    ),
                    text_align="center"
                ),
                rx.text(
                    f"{product_data.get('pv')} PV",
                    font_size="0.9em",
                    color="gray",
                    text_align="center",
                ),
                spacing="1",
                align="center",
                width="100%"
            ),

            # Controles de cantidad
            plusminus_buttons(product_data.get("id", 1)),

            # Botón agregar
            rx.button(
                rx.icon("shopping-cart", size=18),
                "Agregar",
                size="3",
                width="100%",
                variant="solid",
                border_radius="19px",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"]
                ),
                color="white",
                _hover={"opacity": 0.9},
                on_click=CountProducts.add_to_cart(product_data.get("id", 1))
            ),
            spacing="3",
            align="center",
            width="100%"
        ),
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"]
        ),
        border_radius="19px",
        padding="6px",
        min_height="360px",
        width="60vw",
        flex_shrink="0",
        position="relative"
    )


def most_requested_products_card(product_data: Dict) -> rx.Component:
    """
    Tarjeta de producto para la sección "Productos más pedidos".
    Principio DRY: hereda propiedades de product_card_horizontal.
    """
    return rx.box(
        rx.vstack(
            # Badge de más pedido
            rx.badge(
                "🔥 Popular",
                color_scheme="red",
                size="2",
                border_radius="12px",
                position="absolute",
                top="12px",
                right="12px",
                z_index="10"
            ),

            # Imagen del producto
            rx.image(
                src=f"/product_{product_data.get('id', 4)}.jpg",
                height="100%",
                width="100%",
                object_fit="cover",
                border_radius="15px",
                bg="rgba(0,0,0,0.05)",
                margin_bottom="0.5em"
            ),

            # Información del producto
            rx.vstack(
                rx.text(
                    product_data.get("name"),
                    font_weight="bold",
                    font_size="1em",
                    text_align="center",
                    no_of_lines=2,
                ),
                rx.text(
                    product_data.get("formatted_price"),
                    font_weight="600",
                    font_size="0.9em",
                    color=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["primary"],
                        dark=Custom_theme().dark_colors()["secondary"]
                    ),
                    text_align="center"
                ),
                rx.text(
                    f"{product_data.get('pv')} PV",
                    font_size="0.9em",
                    color="gray",
                    text_align="center",
                ),
                spacing="1",
                align="center",
                width="100%"
            ),

            # Controles de cantidad
            plusminus_buttons(product_data.get("id", 1)),

            # Botón agregar
            rx.button(
                rx.icon("shopping-cart", size=18),
                "Agregar",
                size="3",
                width="100%",
                variant="solid",
                border_radius="19px",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"]
                ),
                color="white",
                _hover={"opacity": 0.9},
                on_click=CountProducts.add_to_cart(product_data.get("id", 1))
            ),
            spacing="3",
            align="center",
            width="100%"
        ),
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"]
        ),
        border_radius="19px",
        padding="6px",
        min_height="360px",
        width="60vw",
        flex_shrink="0",
        position="relative"
    )


def supplement_products_card(product_data: Dict) -> rx.Component:
    """
    Tarjeta de producto para la sección "Suplementos".
    Principio DRY: hereda propiedades de product_card_horizontal.
    """
    return rx.box(
        rx.vstack(
            # Badge de suplemento
            rx.badge(
                "Suplemento",
                color_scheme="blue",
                size="2",
                border_radius="12px",
                position="absolute",
                top="12px",
                right="12px",
                z_index="10"
            ),

            # Imagen del producto
            rx.image(
                src=f"/product_{product_data.get('id', 4)}.jpg",
                height="100%",
                width="100%",
                object_fit="cover",
                border_radius="15px",
                bg="rgba(0,0,0,0.05)",
                margin_bottom="0.5em"
            ),

            # Información del producto con PV destacado
            rx.vstack(
                rx.text(
                    product_data.get("name"),
                    font_weight="bold",
                    font_size="1em",
                    text_align="center",
                    no_of_lines="2",
                ),
                rx.text(
                    product_data.get("formatted_price"),
                    font_weight="600",
                    font_size="1em",
                    color=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["primary"],
                        dark=Custom_theme().dark_colors()["secondary"]
                    ),
                    text_align="center"
                ),
                rx.text(
                    f"{product_data.get('pv')} PV",
                    font_size="0.9em",
                    color="gray",
                    text_align="center"
                ),
                spacing="1",
                align="center",
                width="100%"
            ),

            # Controles de cantidad
            plusminus_buttons(product_data.get("id", 1)),

            # Botón agregar
            rx.button(
                rx.icon("shopping-cart", size=18),
                "Agregar",
                size="3",
                width="100%",
                variant="solid",
                border_radius="19px",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"]
                ),
                color="white",
                _hover={"opacity": 0.9},
                on_click=CountProducts.add_to_cart(product_data.get("id", 1))
            ),
            spacing="3",
            align="center",
            width="100%"
        ),
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"]
        ),
        border_radius="19px",
        padding="6px",
        min_height="360px",
        width="45vw",
        flex_shrink="0",
        position="relative"
    )


def skincare_products_card(product_data: Dict) -> rx.Component:
    """
    Tarjeta de producto para la sección "Cuidado de la piel".
    Principio DRY: hereda propiedades de product_card_horizontal.
    """
    return rx.box(
        rx.vstack(
            # Badge de cuidado de la piel
            rx.badge(
                "Cuidado de la piel",
                color_scheme="violet",
                size="2",
                border_radius="12px",
                position="absolute",
                top="12px",
                right="12px",
                z_index="10"
            ),

            # Imagen del producto
            rx.image(
                src=f"/product_{product_data.get('id', 4)}.jpg",
                height="100%",
                width="100%",
                object_fit="cover",
                border_radius="15px",
                bg="rgba(0,0,0,0.05)",
                margin_bottom="0.5em"
            ),

            # Información del producto con PV destacado
            rx.vstack(
                rx.text(
                    product_data.get("name"),
                    font_weight="bold",
                    font_size="1em",
                    text_align="center",
                    no_of_lines="2",
                ),
                rx.text(
                    product_data.get("formatted_price"),
                    font_weight="600",
                    font_size="1em",
                    color=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["primary"],
                        dark=Custom_theme().dark_colors()["secondary"]
                    ),
                    text_align="center"
                ),
                rx.text(
                    f"{product_data.get('pv')} PV",
                    font_size="0.9em",
                    color="gray",
                    text_align="center"
                ),
                spacing="1",
                align="center",
                width="100%"
            ),

            # Controles de cantidad
            plusminus_buttons(product_data.get("id", 1)),

            # Botón agregar
            rx.button(
                rx.icon("shopping-cart", size=18),
                "Agregar",
                size="3",
                width="100%",
                variant="solid",
                border_radius="19px",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"]
                ),
                color="white",
                _hover={"opacity": 0.9},
                on_click=CountProducts.add_to_cart(product_data.get("id", 1))
            ),
            spacing="3",
            align="center",
            width="100%"
        ),
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"]
        ),
        border_radius="19px",
        padding="6px",
        min_height="360px",
        width="45vw",
        flex_shrink="0",
        position="relative"
    )

def sanitized_products_card(product_data: Dict) -> rx.Component:
    """
    Tarjeta de producto para la sección "Cuidado de la piel".
    Principio DRY: hereda propiedades de product_card_horizontal.
    """
    return rx.box(
        rx.vstack(
            # Badge de cuidado de la piel
            rx.badge(
                "Cuidado de la piel",
                color_scheme="violet",
                size="2",
                border_radius="12px",
                position="absolute",
                top="12px",
                right="12px",
                z_index="10"
            ),

            # Imagen del producto
            rx.image(
                src=f"/product_{product_data.get('id', 4)}.jpg",
                height="100%",
                width="100%",
                object_fit="cover",
                border_radius="15px",
                bg="rgba(0,0,0,0.05)",
                margin_bottom="0.5em"
            ),

            # Información del producto con PV destacado
            rx.vstack(
                rx.text(
                    product_data.get("name"),
                    font_weight="bold",
                    font_size="1em",
                    text_align="center",
                    no_of_lines="2",
                ),
                rx.text(
                    product_data.get("formatted_price"),
                    font_weight="600",
                    font_size="1em",
                    color=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["primary"],
                        dark=Custom_theme().dark_colors()["secondary"]
                    ),
                    text_align="center"
                ),
                rx.text(
                    f"{product_data.get('pv')} PV",
                    font_size="0.9em",
                    color="gray",
                    text_align="center"
                ),
                spacing="1",
                align="center",
                width="100%"
            ),

            # Controles de cantidad
            plusminus_buttons(product_data.get("id", 1)),

            # Botón agregar
            rx.button(
                rx.icon("shopping-cart", size=18),
                "Agregar",
                size="3",
                width="100%",
                variant="solid",
                border_radius="19px",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"]
                ),
                color="white",
                _hover={"opacity": 0.9},
                on_click=CountProducts.add_to_cart(product_data.get("id", 1)),
            ),
            spacing="3",
            align="center",
            width="100%"
        ),
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["tertiary"],
            dark=Custom_theme().dark_colors()["tertiary"]
        ),
        border_radius="19px",
        padding="6px",
        min_height="360px",
        width="45vw",
        flex_shrink="0",
        position="relative"
    )