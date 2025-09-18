"""Nueva Backoffice NN Protect | Nuevo registro"""

import reflex as rx
from ..shared_ui.theme import Custom_theme
from rxconfig import config
from ..shared_ui.layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, logged_in_user

"""
# Función para crear tarjetas de productos
def popular_product_card(product_id: int, price: float, is_popular: bool = False):
    #Crea una tarjeta de producto con diseño consistente
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

            # Imagen del producto
            rx.box(
                rx.image(
                    src=f"/product_{product_id}.png",
                    height="120px",
                    width="100%",
                    object_fit="contain",
                    border_radius="12px",
                    loading="lazy"  # Lazy loading para mejor performance
                ),
                width="100%",
                height="120px",
                bg="rgba(0,0,0,0.05)",
                border_radius="12px",
                margin_bottom="0.5em",
                position="relative"
            ),

            # Información del producto
            rx.vstack(
                rx.text(
                    f"Producto {product_id}",
                    font_weight="bold",
                    font_size="0.9rem",
                    text_align="center",
                    no_of_lines=2
                ),
                rx.text(
                    f"${price:.2f}",
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

            # Controles de cantidad mejorados
            rx.hstack(
                rx.button(
                    rx.icon("minus", size=14),
                    size="1",
                    variant="soft",
                    border_radius="8px",
                    min_width="32px",
                    height="32px",
                    _hover={"bg": "rgba(239, 68, 68, 0.1)"}
                ),
                rx.box(
                    rx.text(
                        "0",
                        font_size="0.9rem",
                        font_weight="medium",
                        text_align="center"
                    ),
                    min_width="40px",
                    height="32px",
                    border_radius="8px",
                    bg=rx.color_mode_cond(
                        light="rgba(0,0,0,0.05)",
                        dark="rgba(255,255,255,0.1)"
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center"
                ),
                rx.button(
                    rx.icon("plus", size=14),
                    size="1",
                    variant="soft",
                    border_radius="8px",
                    min_width="32px",
                    height="32px",
                    _hover={"bg": "rgba(34, 197, 94, 0.1)"}
                ),
                justify="center",
                spacing="2",
                align="center"
            ),

            # Botón agregar con icono
            rx.button(
                rx.hstack(
                    rx.icon("shopping-cart", size=14),
                    rx.text("Agregar"),
                    spacing="2",
                    align="center"
                ),
                size="2",
                width="100%",
                variant="solid",
                border_radius="8px",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"]
                ),
                color="white",
                _hover={"opacity": 0.9, "transform": "scale(1.02)"},
                transition="all 0.2s ease"
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
        width="120px",  # Ancho fijo para consistencia
        min_width="280px",  # Mínimo para evitar compresión
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
        border=f"1px solid {rx.color_mode_cond(light='rgba(0,0,0,0.05)', dark='rgba(255,255,255,0.1)')}",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)"
        },
        transition="all 0.2s ease",
        position="relative"
    )
"""
    

def store() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        rx.desktop_only(
            rx.vstack(
                logged_in_user(), # Muestra el usuario logueado en la esquina superior derecha
                rx.hstack(
                    desktop_sidebar(),
                    # Container de la derecha. Contiene el formulario de registro.
                    main_container_derecha(
                        # ---------- HERO BANNER SLIDER ----------
                        rx.box(
                            # Imagen de fondo (fondo absoluto)
                            rx.image(
                                src="/hero_dreamingdeep.jpg",
                                height="100%",
                                width="100%",
                                object_fit="cover",
                                border_radius="64px",
                                position="absolute",
                                z_index=0,
                                top=0,
                                left=0,
                            ),
                            # Texto encima de la imagen
                            rx.box(
                                rx.vstack(
                                    rx.text("Adiós noches largas", size="7", font_weight="regular", color="#1C1C1E", margin_bottom="-12px"),
                                    rx.text("Dreaming Deep", size="9", font_weight="bold", color="#D8B4FE"),
                                    rx.text("Melatonina, L-theanina y GABA.", size="4", color="#1C1C1E", margin_bottom="8px"),
                                    rx.button("Descubrir", bg="#FFFFFF", color="black", border_radius="24px", padding_x="24px"),
                                ),
                                padding="16px 32px 16px 32px",
                                position="absolute",
                                z_index=1,
                                margin="16px 0 16px 32px",
                            ),
                            position="relative",
                            height="260px",
                            width="100%",
                            border_radius="64px",
                            overflow="hidden",
                            margin_bottom="32px",
                        ),

                        # ---------- POPULARES DEL MES ----------
                        rx.text("Populares del mes", font_size="1.7rem", font_weight="bold", margin_bottom="0.7em"),
                        rx.grid(
                            # Tarjeta de producto
                            rx.hstack(
                                *[rx.vstack(
                                    rx.image(src="/product_{}.png".format(i), height="90px", object_fit="contain"),
                                    rx.text("Nombre del producto", font_weight="bold", font_size="1rem"),
                                    rx.text("$999.00 MXN", font_weight="medium", font_size="1rem"),
                                    rx.hstack(
                                        rx.button("-", width="28px", height="28px", border_radius="50%", bg="#f0f0f0"),
                                        rx.text("0", font_size="1rem", margin_x="1em"),
                                        rx.button("+", width="28px", height="28px", border_radius="50%", bg="#f0f0f0"),
                                        margin_top="8px",
                                    ),
                                    rx.button("Agregar al carrito", bg="#0039F2", color="white", border_radius="14px", margin_top="8px"),
                                    spacing="1",
                                    align="center"
                                ) for i in range(1,5)], # Lista de productos populares.
                                justify="between",
                                ),
                                width="100%",
                                padding="64px",
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                        border_radius="64px",
                        #box_shadow="0px 4px 18px #00000016",
                        min_width="240px",
                        margin_bottom="32px",
                    ),

                        # ---------- PRODUCTOS ----------
                        rx.text("Productos", font_size="1.7rem", font_weight="bold", margin_bottom="0.7em"),
                        rx.grid(
                            # Tarjeta de producto
                            *[rx.hstack(
                                *[rx.vstack(
                                    rx.image(src="/product_{}.png".format(i), height="90px", object_fit="contain"),
                                    rx.text("Nombre del producto", font_weight="bold", font_size="1rem"),
                                    rx.text("$999.00 MXN", font_weight="medium", font_size="1rem"),
                                    rx.hstack(
                                        rx.button("-", width="28px", height="28px", border_radius="50%", bg="#f0f0f0"),
                                        rx.text("0", font_size="1rem", margin_x="1em"),
                                        rx.button("+", width="28px", height="28px", border_radius="50%", bg="#f0f0f0"),
                                        margin="8px 0 8px 0",
                                    ),
                                    rx.button("Agregar al carrito", bg="#0039F2", color="white", border_radius="14px", margin_top="0.6em"),
                                    margin="32px",
                                    spacing="1",
                                    align="center"
                                ) for i in range(1,5)], # Lista de productos populares.
                                justify="between",
                                ) for i in range(1,4)],  # Tres filas de productos.
                                width="100%",
                                padding="32px",
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                                border_radius="64px",
                                #box_shadow="0px 4px 18px #00000016",
                                min_width="240px",
                                min_height="275px",
                        ),
                    ),
                    width="100%",
                ),
                # Propiedades vstack que contiene el contenido de la página.
                align="end",  # --- Propiedades rx.vstack ---
                margin_top="8em",
                margin_bottom="2em",
                width="100%",
                max_width="1920px",
            )
        ),
        
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
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("shopping-cart", size=20),
                                    rx.text("(6)", font_size="0.9rem"),
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
                            href="/shopping_cart",
                        ),
                        align="center",
                        justify="between",
                        width="100%",
                        #margin_bottom="0.5em",
                        padding="0 1em"
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
                                light="white" if i == 0 else Custom_theme().light_colors()["secondary"],
                                dark="white"
                            ),
                            variant="soft" if i == 0 else "outline",
                            size="2",
                            border_radius="15px",
                        ) for i, categoria in enumerate(["Todo", "Suplementos", "Belleza"])],
                        spacing="2",
                        width="100%",
                        margin_bottom="1.5em",
                        padding="0 1em"
                    ),

                    # Últimas novedades móvil
                    rx.text("Últimas novedades", size="5", font_weight="bold", padding_x="1em"),
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
                                            border_radius="19px",
                                            bg="rgba(0,0,0,0.05)",
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
                                                "$999.00",
                                                font_weight="600",
                                                font_size="0.9rem",
                                                color=rx.color_mode_cond(
                                                    light=Custom_theme().light_colors()["primary"],
                                                    dark=Custom_theme().dark_colors()["primary"]
                                                ),
                                                text_align="center"
                                            ),
                                            z_index=1,
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
                                            align="center",
                                            margin_bottom="0.5em"
                                        ),

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
                                    border_radius="29px",
                                    padding="10px",
                                    width="50vw",  # Ancho fijo para consistencia
                                    #_hover={
                                    #    "transform": "translateY(-2px)",
                                    #    "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)"
                                    #},
                                    #transition="all 0.2s ease"
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
                        padding="0 0 0 1em",
                        width="100%",
                        margin_bottom="1em"
                    ),

                    # Productos tendencia móvil
                    rx.text("Productos tendencia", size="5", font_weight="bold", padding_x="1em"),
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
                                            border_radius="19px",
                                            bg="rgba(0,0,0,0.05)",
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
                                                "$999.00",
                                                font_weight="600",
                                                font_size="0.9rem",
                                                color=rx.color_mode_cond(
                                                    light=Custom_theme().light_colors()["primary"],
                                                    dark=Custom_theme().dark_colors()["primary"]
                                                ),
                                                text_align="center"
                                            ),
                                            z_index=1,
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
                                            align="center",
                                            margin_bottom="0.5em"
                                        ),

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
                                    border_radius="29px",
                                    padding="10px",
                                    width="50vw",  # Ancho fijo para consistencia
                                    #_hover={
                                    #    "transform": "translateY(-2px)",
                                    #    "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)"
                                    #},
                                    #transition="all 0.2s ease"
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
                        padding="0 0 0 1em",
                        width="100%",
                        margin_bottom="1em"
                    ),

                    # Grid de productos móvil
                    rx.text("Todos los productos", size="5", font_weight="bold", padding_x="1em"),
                    rx.grid(
                        *[rx.box(
                            rx.vstack(
                                rx.image(src=f"/product_{i}.png", height="100px", width="100%", object_fit="contain"),
                                rx.text(f"Producto {i}", font_weight="bold", font_size="0.9rem", text_align="center"),
                                rx.text("$999.00", font_weight="600", font_size="0.9rem", color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                )),
                                rx.hstack(
                                    rx.button("-", size="1", variant="soft"),
                                    rx.text("0", font_size="0.9rem"),
                                    rx.button("+", size="1", variant="soft"),
                                    justify="center",
                                    spacing="2"
                                ),
                                rx.button("Agregar", size="2", width="100%", variant="solid"),
                                spacing="2",
                                align="center",
                                width="100%"
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="12px",
                            padding="1rem",
                            width="100%"
                        ) for i in range(1, 7)],
                        columns="2",
                        spacing="3",
                        width="100%",
                        padding_x="1em"
                    ),
                    spacing="4",
                    width="100%",
                    margin="80px 0 20px 0",
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