"""Nueva implementación de tarjetas para versión mobile"""

import reflex as rx
from ..theme import Custom_theme
from rxconfig import config
from ..layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, header

def store() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        
        # Versión móvil
        rx.mobile_only(
            rx.vstack(
                # Header móvil
                mobile_header(),
                
                # Contenido principal móvil
                rx.vstack(
                    # Título y carrito
                    rx.hstack(
                        rx.text("Tienda", size="8", font_weight="bold"),
                        rx.button(
                            rx.hstack(
                                rx.icon("shopping-cart", size=20),
                                rx.text("(0)", font_size="0.9rem"),
                                spacing="1"
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["secondary"],
                                dark=Custom_theme().dark_colors()["secondary"]
                            ),
                            color="white",
                            border_radius="15px",
                            variant="soft",
                            size="2"
                        ),
                        align="center",
                        justify="between",
                        width="100%",
                        margin_bottom="0.5em"
                    ),
                    
                    # Categorías móvil
                    rx.hstack(
                        *[rx.button(
                            categoria,
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["secondary"] if i == 0 else "transparent",
                                dark=Custom_theme().dark_colors()["secondary"] if i == 0 else "transparent"
                            ),
                            color=rx.color_mode_cond(
                                light="white" if i == 0 else Custom_theme().light_colors()["primary"],
                                dark="white" if i == 0 else Custom_theme().dark_colors()["primary"]
                            ),
                            variant="soft" if i == 0 else "outline",
                            size="2",
                            border_radius="15px",
                        ) for i, categoria in enumerate(["Todo", "Populares", "Suplementos", "Belleza"])],
                        spacing="2",
                        width="100%",
                        margin_bottom="1.5em"
                    ),
                    
                    # Populares del mes móvil - Card Slides Horizontales
                    rx.text("Populares del mes", size="5", font_weight="bold", margin_bottom="1em"),

                    # Contenedor del scroll horizontal
                    rx.box(
                        rx.scroll_area(
                            # Contenedor horizontal de las tarjetas
                            rx.hstack(
                                *[rx.box(
                                    rx.vstack(
                                        # Imagen del producto
                                        rx.image(
                                            src=f"/product_{i}.jpg",
                                            height="100%",
                                            width="100%",
                                            object_fit="cover",
                                            border_radius="23px",
                                            z_index=0,
                                            top=0,
                                            left=0,
                                            bg="rgba(0,0,0,0.05)",
                                        ),

                                        # Información del producto
                                        rx.flex(
                                            rx.text(
                                                f"Producto {i}",
                                                font_weight="bold",
                                                font_size="0.9rem",
                                                text_align="center",
                                                no_of_lines=2,
                                                color="white",
                                            ),
                                            rx.text(
                                                "$999.00",
                                                font_weight="600",
                                                font_size="0.9rem",
                                                color="white",
                                                text_align="center"
                                            ),

                                            # Controles de cantidad
                                            rx.hstack(
                                                rx.button(
                                                    "-",
                                                    size="1",
                                                    bg="white",
                                                    color=rx.color_mode_cond(
                                                        light=Custom_theme().light_colors()["primary"],
                                                        dark=Custom_theme().dark_colors()["primary"]
                                                    ),
                                                    variant="soft",
                                                    border_radius="8px",
                                                    min_width="32px",
                                                    height="32px"
                                                ),
                                                rx.text(
                                                    "0",
                                                    color="white",
                                                    font_size="0.9rem",
                                                    font_weight="medium",
                                                    min_width="40px",
                                                    text_align="center"
                                                ),
                                                rx.button(
                                                    "+",
                                                    bg="white",
                                                    color=rx.color_mode_cond(
                                                        light=Custom_theme().light_colors()["primary"],
                                                        dark=Custom_theme().dark_colors()["primary"]
                                                    ),
                                                    size="1",
                                                    variant="soft",
                                                    border_radius="8px",
                                                    min_width="32px",
                                                    height="32px"
                                                ),
                                                justify="center",
                                                spacing="2",
                                                align="center"
                                            ),
                                            
                                            # Botón agregar
                                            rx.button(
                                                "Agregar",
                                                size="3",
                                                width="100%",
                                                variant="solid",
                                                border_radius="23px",
                                                bg="white",
                                                color=rx.color_mode_cond(
                                                    light=Custom_theme().light_colors()["primary"],
                                                    dark=Custom_theme().dark_colors()["primary"]
                                                ),
                                                _hover={"opacity": 0.9}
                                            ),
                                            z_index=1,
                                            position="absolute",
                                            spacing="3",
                                            align="center",
                                            width="51%",
                                            border_radius="0 0 23px 23px",
                                            direction="column",
                                            padding="8px",
                                            bg="rgba(0,0,0,0.20)",
                                            backdrop_filter="blur(10px)",
                                        ),
                                        padding="6px",
                                        height="100%",
                                        justify="end",
                                        spacing="3",
                                        align="center",
                                        width="100%"
                                    ),
                                    height="320px",
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    border_radius="29px",
                                    #padding="6px",
                                    width="50vw",  # Ancho fijo para consistencia
                                    _hover={
                                        "transform": "translateY(-2px)",
                                        "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)"
                                    },
                                    transition="all 0.2s ease"
                                ) for i in range(1, 5)],
                                spacing="4",  # Espacio entre tarjetas
                                min_width="100%"  # Mínimo ancho de la pantalla
                            ),

                            # Configuración del scroll area
                            scrollbars="horizontal",  # Scroll horizontal
                            type="scroll",  # Aparece al hacer scroll
                            height="auto",  # Altura automática
                            width="100%",  # Ancho completo
                            padding="0 0 1em 0",  # Padding vertical
                        ),

                        # Indicadores de scroll (opcional)
                        rx.hstack(
                            rx.box(
                                width="20px",
                                height="4px",
                                bg=rx.color_mode_cond(
                                    light="rgba(0,0,0,0.2)",
                                    dark="rgba(255,255,255,0.3)"
                                ),
                                border_radius="2px",
                                opacity="0.5"
                            ),
                            rx.box(
                                width="20px",
                                height="4px",
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ),
                                border_radius="2px"
                            ),
                            rx.box(
                                width="20px",
                                height="4px",
                                bg=rx.color_mode_cond(
                                    light="rgba(0,0,0,0.2)",
                                    dark="rgba(255,255,255,0.3)"
                                ),
                                border_radius="2px",
                                opacity="0.5"
                            ),
                            spacing="1",
                            justify="center",
                            margin_top="0.5em"
                        ),
                        width="100%",
                        margin_bottom="1em"
                    ),

                    # Todos los productos - Card Slides Horizontales
                    rx.text("Todos los productos", size="5", font_weight="bold", margin_bottom="1em"),

                    # Contenedor del scroll horizontal para todos los productos
                    rx.box(
                        rx.scroll_area(
                            # Contenedor horizontal de las tarjetas
                            rx.hstack(
                                *[rx.box(
                                    rx.vstack(
                                        # Imagen del producto
                                        rx.box(
                                            rx.image(
                                                src=f"/product_{i}.png",
                                                height="120px",
                                                width="100%",
                                                object_fit="contain",
                                                border_radius="12px"
                                            ),
                                            width="100%",
                                            height="120px",
                                            bg="rgba(0,0,0,0.05)",
                                            border_radius="12px",
                                            margin_bottom="0.5em"
                                        ),

                                        # Información del producto
                                        rx.vstack(
                                            rx.text(
                                                f"Producto {i}",
                                                font_weight="bold",
                                                font_size="0.9rem",
                                                text_align="center",
                                                no_of_lines=2
                                            ),
                                            rx.text(
                                                f"${(i * 150) + 499}.00",
                                                font_weight="600",
                                                font_size="0.9rem",
                                                color=rx.color_mode_cond(
                                                    light=Custom_theme().light_colors()["primary"],
                                                    dark=Custom_theme().dark_colors()["primary"]
                                                ),
                                                text_align="center"
                                            ),
                                            spacing="1",
                                            align="center",
                                            width="100%"
                                        ),

                                        # Controles de cantidad
                                        rx.hstack(
                                            rx.button(
                                                "-",
                                                size="1",
                                                variant="soft",
                                                border_radius="8px",
                                                min_width="32px",
                                                height="32px"
                                            ),
                                            rx.text(
                                                "0",
                                                font_size="0.9rem",
                                                font_weight="medium",
                                                min_width="40px",
                                                text_align="center"
                                            ),
                                            rx.button(
                                                "+",
                                                size="1",
                                                variant="soft",
                                                border_radius="8px",
                                                min_width="32px",
                                                height="32px"
                                            ),
                                            justify="center",
                                            spacing="2",
                                            align="center"
                                        ),

                                        # Botón agregar
                                        rx.button(
                                            "Agregar",
                                            size="2",
                                            width="100%",
                                            variant="solid",
                                            border_radius="8px",
                                            bg=rx.color_mode_cond(
                                                light=Custom_theme().light_colors()["primary"],
                                                dark=Custom_theme().dark_colors()["primary"]
                                            ),
                                            color="white",
                                            _hover={"opacity": 0.9}
                                        ),

                                        spacing="3",
                                        align="center",
                                        width="100%"
                                    ),
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    border_radius="16px",
                                    padding="1em",
                                    width="280px",  # Ancho fijo para consistencia
                                    min_width="280px",  # Mínimo para evitar compresión
                                    box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
                                    border=f"1px solid {rx.color_mode_cond(light='rgba(0,0,0,0.05)', dark='rgba(255,255,255,0.1)')}",
                                    _hover={
                                        "transform": "translateY(-2px)",
                                        "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)"
                                    },
                                    transition="all 0.2s ease"
                                ) for i in range(1, 9)],  # Más productos para demostrar el scroll

                                spacing="4",  # Espacio entre tarjetas
                                padding="0 1em",  # Padding interno del contenedor
                                width="max-content",  # Ancho basado en contenido
                                min_width="100%"  # Mínimo ancho de la pantalla
                            ),

                            # Configuración del scroll area
                            scrollbars="horizontal",  # Scroll horizontal
                            type="hover",  # Aparece al hacer hover
                            height="auto",  # Altura automática
                            width="100%",  # Ancho completo
                            padding="0.5em 0",  # Padding vertical
                        ),

                        # Indicadores de scroll mejorados
                        rx.hstack(
                            *[rx.box(
                                width="12px",
                                height="4px",
                                bg=rx.cond(
                                    i == 1,  # Primer indicador activo
                                    rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["primary"],
                                        dark=Custom_theme().dark_colors()["primary"]
                                    ),
                                    rx.color_mode_cond(
                                        light="rgba(0,0,0,0.2)",
                                        dark="rgba(255,255,255,0.3)"
                                    )
                                ),
                                border_radius="2px",
                                opacity=rx.cond(i == 1, "1", "0.5")
                            ) for i in range(1, 5)],
                            spacing="1",
                            justify="center",
                            margin_top="1em"
                        ),

                        width="100%",
                        margin_bottom="2em"
                    ),
                    
                    spacing="4",
                    width="100%",
                    padding="1em",
                    margin_top="80px",
                ),
            ),
            width="100%",
        ),
        
        # Propiedades del contenedor principal.
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),
        position="absolute",
        width="100%",
    )