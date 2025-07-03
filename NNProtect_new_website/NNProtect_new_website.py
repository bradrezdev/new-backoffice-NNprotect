"""Nueva Backoffice NN Protect | Dashboard"""

import reflex as rx
from .pages.login import login
from .pages.new_register import register
from .pages.store import store
from .theme import Custom_theme
from .state import sidebar_items
from rxconfig import config
from .layout import main_container_derecha

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        # Contenedor principal centrado
        rx.desktop_only(
            # Solo se muestra en escritorio
            rx.vstack(
                # Contenedor vertical principal
                rx.hstack(
                    # Contenedor horizontal para sidebar y contenido principal
                    sidebar_items(),
                    # Sidebar (menú lateral)
                    main_container_derecha(
                        # Contenedor principal de la derecha
                        rx.vstack(
                            # Contenedor vertical para el contenido del dashboard
                            # Sección de anuncios/noticias
                            rx.box(
                                rx.image(
                                    src="/banner_dashboard.png",
                                    height="100%",  # Imagen ocupa todo el alto del box
                                    width="100%",   # Imagen ocupa todo el ancho del box
                                    object_fit="cover",  # Ajuste de imagen
                                    border_radius="64px" # Bordes redondeados
                                ),
                                height="260px",         # Alto del banner
                                width="100%",           # Ancho completo
                                margin_bottom="0.5em",  # Espacio inferior
                            ),
                            # Fila: Volumen Personal, Puntos NN Travel, Rango mayor, Rango actual
                            rx.hstack(
                                rx.box(
                                    rx.text("Volumen Personal", font_size="0.875rem", color="black"),
                                    rx.text("2,930", font_size="1.5rem", font_weight="bold", color="black"),
                                    bg="#32D74B",             # Fondo verde
                                    padding="1em",            # Espaciado interno
                                    border_radius="32px",     # Bordes redondeados
                                    width="25%",              # Ancho relativo
                                ),
                                rx.box(
                                    rx.text("Puntos NN Travel", font_size="0.875rem"),
                                    rx.text("500", font_size="1.5rem", font_weight="bold"),
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),                        # Fondo según modo
                                    padding="1em",
                                    border_radius="32px",
                                    width="25%",
                                ),
                                rx.box(
                                    rx.text("Rango más alto alcanzado", font_size="0.875rem"),
                                    rx.text("E. Consciente", font_size="1.5rem", font_weight="bold"),
                                    bg="#0039F2",             # Fondo azul
                                    color="white",            # Texto blanco
                                    padding="1em",
                                    border_radius="32px",
                                    width="25%",
                                ),
                                rx.box(
                                    rx.text("Rango Actual", font_size="0.875rem"),
                                    rx.text("E. Transformador", font_size="1.5rem", font_weight="bold"),
                                    bg="#5E79FF",             # Fondo azul claro
                                    color="white",
                                    padding="1em",
                                    border_radius="32px",
                                    width="25%",
                                ),
                                spacing="2",                 # Espacio entre cajas
                                width="100%",                # Ancho completo
                            ),
                            rx.hstack(
                                # Fila vertical: puntos de lealtad y cashback
                                rx.vstack(
                                    rx.box(
                                        rx.text("Puntos de lealtad", font_size="0.875rem"),
                                        rx.text("100", font_size="1.5rem", font_weight="bold"),
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        padding="1em",
                                        border_radius="32px",
                                        width="100%",
                                    ),
                                    rx.box(
                                        rx.text("Puntos de CASHBACK", font_size="0.875rem"),
                                        rx.text("2,930", font_size="1.5rem", font_weight="bold"),
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        padding="1em",
                                        border_radius="32px",
                                        width="100%",
                                    ),
                                    spacing="2",              # Espacio entre cajas
                                    width="25%",              # Ancho relativo
                                ),
                                # Barra de progresión
                                rx.box(
                                    rx.text("Progresión para el siguiente rango", font_size="0.875rem", color="#FFFFFF"),
                                    rx.center(
                                        rx.text("754,654 VG – 1,300,000 VG", font_size="2rem", font_weight="bold"),
                                        height="6em",          # Altura del centro
                                    ),
                                    rx.progress(
                                        bg="#D0D7FF",          # Fondo de la barra
                                        fill_color="#0039F2",  # Color de progreso
                                        height="8px",          # Altura de la barra
                                        width="100%",          # Ancho completo
                                        value=754654,          # Valor actual
                                        max=1300000,           # Valor máximo
                                    ),
                                    spacing="1",              # Espacio entre elementos
                                    bg="#5E79FF",             # Fondo del box
                                    color="white",            # Texto blanco
                                    padding="1.5em",          # Espaciado interno
                                    justify="center",         # Centrado
                                    border_radius="48px",     # Bordes redondeados
                                    height="100%",            # Alto completo
                                    width="75%",              # Ancho relativo
                                ),
                                height="11em",               # Altura de la fila
                                width="100%",                # Ancho completo
                            ),
                            # Enlace de referido
                            rx.box(
                                rx.text("Enlace de referido", font_size="0.875rem", margin_bottom="0.5em"),
                                rx.input(
                                    value="https://www.nnprotect.com.mx/mioficina/aut/register?ref=244",
                                    read_only=True,           # Solo lectura
                                    border_radius="18px"      # Bordes redondeados
                                ),
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                                padding="1em",
                                border_radius="32px",
                                width="100%",
                                margin_top="1em",            # Espacio superior
                            ),
                            # Reporte de usuarios
                            rx.box(
                                rx.text("Reporte de usuarios", font_size="0.875rem"),
                                rx.hstack(
                                    rx.box(bg="#32D74B", height="8px", width="50%", border_radius="4px"),
                                    rx.box(bg="#FF3B30", height="8px", width="50%", border_radius="4px"),
                                    spacing="1",              # Espacio entre barras
                                ),
                                rx.hstack(
                                    rx.text("Activos – 501"),
                                    rx.text("Inactivos – 501", margin_left="auto")  # Alinea a la derecha
                                ),
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                                padding="1em",
                                border_radius="32px",
                                width="100%",
                                margin_top="1em",
                            ),
                            # Ganancias y acciones
                            rx.hstack(
                                rx.box(
                                    rx.text("Estimado de ganancia del mes"),
                                    rx.text("42,659,227.68", font_size="1.5rem", font_weight="bold"),
                                    bg="#0039F2",
                                    color="white",
                                    padding="1em",
                                    border_radius="32px",
                                    width="25%",
                                ),
                                rx.box(
                                    rx.text("Billetera"),
                                    rx.text("53,324,034.60", font_size="1.5rem", font_weight="bold"),
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    padding="1em",
                                    border_radius="32px",
                                    width="25%",
                                ),
                                rx.box(
                                    rx.text("Pago en espera"),
                                    rx.text("10,664,806.92", font_size="1.5rem", font_weight="bold"),
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    padding="1em",
                                    border_radius="32px",
                                    width="25%",
                                ),
                                rx.vstack(
                                    rx.button(
                                        "Solicitar comisiones",
                                        bg="#0039F2",
                                        color="white",
                                        border_radius="32px",
                                        width="100%",
                                        height="40px",
                                    ),
                                    rx.button(
                                        "Transferencia interna",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        border="1px solid #0039F2",
                                        color=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["text"],
                                            dark=Custom_theme().dark_colors()["text"]
                                        ),
                                        border_radius="32px",
                                        width="100%",
                                        height="36px"
                                    ),
                                    margin="auto",            # Centrado vertical
                                    width="25%",
                                    spacing="2",              # Espacio entre botones
                                ),
                                spacing="2",                  # Espacio entre cajas
                                width="100%",
                                margin_top="1em",
                            ),
                            # Herramientas para tu negocio (grid)
                            rx.vstack(
                                rx.text("Herramientas para tu negocio", font_size="1rem", font_weight="bold"),
                                rx.grid(
                                    *[rx.box(bg="#E5E5E5", height="80px", border_radius="12px") for _ in range(12)],
                                    template_columns="repeat(4, 1fr)",  # 4 columnas
                                    gap="1em",                          # Espacio entre cajas
                                    width="100%",
                                    margin_top="1em",
                                ),
                            ),
                        ),
                    )
                    # Propiedades de flex dentro del vstack que contiene el contenido de la página.
                ),
                # Propiedades vstack que contiene el contenido de la página.
                justify="center",           # Centrado vertical
                margin_top="120px",         # Espacio superior
                margin_bottom="2em",        # Espacio inferior
                max_width="1440px",         # Ancho máximo
            )
        ),
        # Propiedades del contenedor principal.
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),                              # Fondo según modo
        position="absolute",            # Posición absoluta
        width="100%",                  # Ancho de la ventana
    )

app = rx.App(theme=rx.theme(appearance="inherit"))
app.add_page(index, title="NN Protect | Dashboard")
app.add_page(login, title="NN Protect | Iniciar sesión", route="/login")
app.add_page(register, title="NN Protect | Nuevo registro", route="/new_register")


app.add_page(store, title="NN Protect | Tienda", route="/store")