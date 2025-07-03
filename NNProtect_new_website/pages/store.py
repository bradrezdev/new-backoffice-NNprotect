"""Nueva Backoffice NN Protect | Nuevo registro"""

import reflex as rx
from ..theme import Custom_theme
from rxconfig import config
from ..layout import main_container_derecha
from ..state import sidebar_items

def store() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    sidebar_items(),
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
                    )
                ),
                # Propiedades vstack que contiene el contenido de la página.
                justify="center",  # --- Propiedades rx.vstack ---
                margin_top="120px",
                margin_bottom="2em",
                max_width="1440px",
            )
        ),
        # Propiedades del contenedor principal.
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),
        position="absolute",
        width="100%",
    )