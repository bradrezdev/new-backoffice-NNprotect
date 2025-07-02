"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from .pages.login import login
from .theme import Custom_theme
from .state import sidebar_item
from .state import sidebar_items
from rxconfig import config



def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        
        rx.desktop_only(
            rx.vstack(

                rx.hstack(
                    
                    rx.center(
                        
                        rx.vstack(
                            rx.image(src="/nnprotect_logo.png", height="5vh", position="top", margin_bottom="4em"),

                            rx.vstack(
                                
                                # Combinación de icono y enlace para Dashboard.
                                rx.link(
                                    rx.hstack(
                                        rx.icon("layout-dashboard", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        rx.text("Dashboard", size="3", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        margin_left="0.5em",
                                    ),
                                    # Propiedades @Combinación de icono y enlace para Dashboard.
                                    #bg="lightgrey",
                                    border_radius="12px",
                                    height="40px",
                                    href="/",
                                    is_external=False,
                                    margin_bottom="1em",
                                    padding="0.5em",
                                    width="10vw",
                                ),

                                # Combinación de icono y enlace para Dashboard.
                                rx.link(
                                    rx.hstack(
                                        rx.icon("circle-plus", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        rx.text("Nuevo registro", size="3", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        margin_left="0.5em",
                                    ),
                                    # Propiedades @Combinación de icono y enlace para Dashboard.
                                    #bg="lightgrey",
                                    border_radius="12px",
                                    height="40px",
                                    href="/",
                                    is_external=False,
                                    margin_bottom="1em",
                                    padding="0.5em",
                                    width="10vw",
                                ),

                                # Combinación de icono y enlace para Dashboard.
                                rx.link(
                                    rx.hstack(
                                        rx.icon("network", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        rx.text("Red de usuarios", size="3", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        margin_left="0.5em",
                                    ),
                                    # Propiedades @Combinación de icono y enlace para Dashboard.
                                    #bg="lightgrey",
                                    border_radius="12px",
                                    height="40px",
                                    href="/",
                                    is_external=False,
                                    margin_bottom="1em",
                                    padding="0.5em",
                                    width="10vw",
                                ),

                                # Combinación de icono y enlace para Dashboard.
                                rx.link(
                                    rx.hstack(
                                        rx.icon("scroll-text", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        rx.text("Compras", size="3", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        margin_left="0.5em",
                                    ),
                                    # Propiedades @Combinación de icono y enlace para Dashboard.
                                    #bg="lightgrey",
                                    border_radius="12px",
                                    height="40px",
                                    href="/",
                                    is_external=False,
                                    margin_bottom="1em",
                                    padding="0.5em",
                                    width="10vw",
                                ),

                                # Combinación de icono y enlace para Dashboard.
                                rx.link(
                                    rx.hstack(
                                        rx.icon("plane", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        rx.text("NN Travels", size="3", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        margin_left="0.5em",
                                    ),
                                    # Propiedades @Combinación de icono y enlace para Dashboard.
                                    #bg="lightgrey",
                                    border_radius="12px",
                                    height="40px",
                                    href="/",
                                    is_external=False,
                                    margin_bottom="1em",
                                    padding="0.5em",
                                    width="10vw",
                                ),

                                # Combinación de icono y enlace para Dashboard.
                                rx.link(
                                    rx.hstack(
                                        rx.icon("wallet", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        rx.text("Billetera", size="3", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        margin_left="0.5em",
                                    ),
                                    # Propiedades @Combinación de icono y enlace para Dashboard.
                                    #bg="lightgrey",
                                    border_radius="12px",
                                    height="40px",
                                    href="/",
                                    is_external=False,
                                    margin_bottom="1em",
                                    padding="0.5em",
                                    width="10vw",
                                ),

                                # Combinación de icono y enlace para Dashboard.
                                rx.link(
                                    rx.hstack(
                                        rx.icon("messages-square", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        rx.text("Tickets/Soporte", size="3", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        margin_left="0.5em",
                                    ),
                                    # Propiedades @Combinación de icono y enlace para Dashboard.
                                    #bg="lightgrey",
                                    border_radius="12px",
                                    height="40px",
                                    href="/",
                                    is_external=False,
                                    margin_bottom="1em",
                                    padding="0.5em",
                                    width="10vw",
                                ),

                                # Combinación de icono y enlace para Dashboard.
                                rx.link(
                                    rx.hstack(
                                        rx.icon("store", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        rx.text("Tienda", size="3", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        margin_left="0.5em",
                                    ),
                                    # Propiedades @Combinación de icono y enlace para Dashboard.
                                    #bg="lightgrey",
                                    border_radius="12px",
                                    height="40px",
                                    href="/",
                                    is_external=False,
                                    margin_bottom="1em",
                                    padding="0.5em",
                                    width="10vw",
                                ),

                                # Combinación de icono y enlace para Dashboard.
                                rx.link(
                                    rx.hstack(
                                        rx.icon("folder-cog", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        rx.text("Herramientas", size="3", color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])),
                                        margin_left="0.5em",
                                    ),
                                    # Propiedades @Combinación de icono y enlace para Dashboard.
                                    #bg="lightgrey",
                                    border_radius="12px",
                                    height="40px",
                                    href="/",
                                    is_external=False,
                                    margin_bottom="1em",
                                    padding="0.5em",
                                    width="10vw",
                                ),

                                # Propiedades del vstack que contiene los enlaces de navegación.
                                height="65vh",
                            ),

                            rx.center(
                                "Cerrar sesión",
                                # Propiedades de box dentro del vstack que contiene el logo + enlaces de navegación + "Cerrar sesión"
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["secondary"],
                                    dark=Custom_theme().light_colors()["secondary"],
                                ),
                                height="5vh",
                                margin_bottom="1em",
                                width="100%",
                            ),

                            # Propiedades del vstack que contiene el logo + enlaces de navegación + "Cerrar sesión"
                            height="80vh",
                        ),
                        
                        # Propiedades del container izquierdo.
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["tertiary"],
                            dark=Custom_theme().dark_colors()["tertiary"]
                        ),
                        border_radius="36px",
                        justify="start",
                        padding="2em",
                        margin_right="8px",
                        min_height="900px",
                        width="14vw",
                    ),

                    # Container de la derecha. Contiene el panel de control del usuario.
                    rx.center(
                        rx.box(
                            rx.vstack(
                                # Sección de anuncios/noticias
                                rx.box(
                                    rx.image(src="/banner_dashboard.png", height="100%", width="100%", object_fit="cover", border_radius="64px"),
                                    border_radius="64px",
                                    height="260px",
                                    width="100%",
                                    margin_bottom="0.5em",
                                ),
                                # Fila: Volumen Personal, Puntos NN Travel, Rango mayor, Rango actual
                                rx.hstack(
                                    rx.box(rx.text("Volumen Personal", font_size="0.875rem", color="black"), rx.text("2,930", font_size="1.5rem", font_weight="bold", color="black"), bg="#32D74B", padding="1em", border_radius="32px", width="25%"),
                                    rx.box(rx.text("Puntos NN Travel", font_size="0.875rem"), rx.text("500", font_size="1.5rem", font_weight="bold"), bg=rx.color_mode_cond(light=Custom_theme().light_colors()["tertiary"], dark=Custom_theme().dark_colors()["tertiary"]), padding="1em", border_radius="32px", width="25%"),
                                    rx.box(rx.text("Rango más alto alcanzado", font_size="0.875rem"), rx.text("E. Consciente", font_size="1.5rem", font_weight="bold"), bg="#0039F2", color="white", padding="1em", border_radius="32px", width="25%"),
                                    rx.box(rx.text("Rango Actual", font_size="0.875rem"), rx.text("E. Transformador", font_size="1.5rem", font_weight="bold"), bg="#5E79FF", color="white", padding="1em", border_radius="32px", width="25%"),
                                    spacing="2",
                                    width="100%",
                                ),
                                rx.hstack(
                                # Fila vertical: puntos de lealtad y cashback
                                    rx.vstack(
                                        rx.box(rx.text("Puntos de lealtad", font_size="0.875rem"), rx.text("100", font_size="1.5rem", font_weight="bold"), bg="white", padding="1em", border_radius="32px", width="100%"),
                                        rx.box(rx.text("Puntos de CASHBACK", font_size="0.875rem"), rx.text("2,930", font_size="1.5rem", font_weight="bold"), bg="white", padding="1em", border_radius="32px", width="100%"),
                                        spacing="2",
                                        width="25%",
                                    ),
                                    # Barra de progresión
                                    rx.box(
                                        rx.text("Progresión para el siguiente rango", font_size="0.875rem", color="#FFFFFF"),
                                        rx.center(rx.text("754,654 VG – 1,300,000 VG", font_size="2rem", font_weight="bold"), height="6em"),
                                        rx.progress(
                                            bg="#D0D7FF",
                                            fill_color="#0039F2",
                                            height="8px",
                                            width="100%",
                                            value=754654,
                                            max=1300000,
                                        ),
                                        spacing="1",
                                        bg="#5E79FF",
                                        color="white",
                                        padding="1.5em",
                                        justify="center",
                                        border_radius="48px",
                                        height="100%",
                                        width="75%",
                                    ),
                                    height="11em",
                                    width="100%",
                                ),
                                # Enlace de referido
                                rx.box(
                                    rx.text("Enlace de referido", font_size="0.875rem", margin_bottom="0.5em",),
                                    rx.input(value="https://www.nnprotect.com.mx/mioficina/aut/register?ref=244", read_only=True, border_radius="18px"),
                                    bg="white",
                                    padding="1em",
                                    border_radius="32px",
                                    width="100%",
                                    margin_top="1em",
                                ),
                                # Reporte de usuarios
                                rx.box(
                                    rx.text("Reporte de usuarios", font_size="0.875rem"),
                                    rx.hstack(
                                        rx.box(bg="#32D74B", height="8px", width="50%", border_radius="4px"),
                                        rx.box(bg="#FF3B30", height="8px", width="50%", border_radius="4px"),
                                        spacing="1",
                                    ),
                                    rx.hstack(rx.text("Activos – 501"), rx.text("Inactivos – 501", margin_left="auto")),
                                    bg="white",
                                    padding="1em",
                                    border_radius="32px",
                                    width="100%",
                                    margin_top="1em",
                                ),
                                # Ganancias y acciones
                                rx.hstack(
                                    rx.box(rx.text("Estimado de ganancia del mes"), rx.text("42,659,227.68", font_size="1.5rem", font_weight="bold"), bg="#0039F2", color="white", padding="1em", border_radius="32px", width="25%"),
                                    rx.box(rx.text("Billetera"), rx.text("53,324,034.60", font_size="1.5rem", font_weight="bold"), bg="white", padding="1em", border_radius="32px", width="25%"),
                                    rx.box(rx.text("Pago en espera"), rx.text("10,664,806.92", font_size="1.5rem", font_weight="bold"), bg="white", padding="1em", border_radius="32px", width="25%"),
                                    rx.vstack(
                                        rx.button("Solicitar comisiones", bg="#0039F2", color="white", border_radius="32px", width="100%", height="40px",),
                                        rx.button("Transferencia interna", bg="white", border="1px solid #0039F2", color="#0039F2", border_radius="32px", width="100%", height="36px"),
                                        margin="auto",
                                        width="25%",
                                        spacing="2",
                                    ),
                                    spacing="2",
                                    width="100%",
                                    margin_top="1em",
                                ),
                                # Herramientas para tu negocio (grid)
                                rx.vstack(
                                    rx.text("Herramientas para tu negocio", font_size="1rem", font_weight="bold"),
                                    rx.grid(
                                        *[rx.box(bg="#E5E5E5", height="80px", border_radius="12px") for _ in range(12)],
                                        template_columns="repeat(4, 1fr)",
                                        gap="1em",
                                        width="100%",
                                        margin_top="1em",
                                    ),
                                ),
                                #spacing="2",
                                #padding="2em",
                                #bg="#F2F3F8",
                                #border_radius="24px",
                                #width="100%",
                            ),
                            #bg="white",
                            #border_radius="36px",
                            #justify="start",
                            #padding="2em",
                            margin_right="20px",
                            #min_height="900px",
                            #width="60vw",
                        ),
                        justify="center",
                    )

                    # Propiedades de flex dentro del vstack que contiene el contenido de la página.
                ),

                # Propiedades vstack que contiene el contenido de la página.
                #bg="#002AFF",
                justify="center",
                #height="92%",
                margin_top="6em",
                margin_bottom="2em",
                max_width="1440px",
                width="100%",
            )
        ),

        # Propiedades del contenedor principal.
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),
        #height="100vh",
        position="absolute",
        width="100vw",
    )


app = rx.App(theme=rx.theme(appearance="dark"))
app.add_page(index, title="NN Protect | Dashboard")
app.add_page(login, title="NN Protect | Iniciar sesión", route="/login")