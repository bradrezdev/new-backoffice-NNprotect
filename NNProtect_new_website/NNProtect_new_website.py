"""Nueva Backoffice NN Protect | Dashboard"""

import reflex as rx

# --- Pages ---
from .business.network import network
from .business.network_reports import network_reports
from .auth.login import login
from .auth.new_register import register
from .shop.store import store
from .business.income_reports import income_reports
from .shop.orders import orders
from .shop.order_details import order_details
from .finance.withdrawals import withdrawals
from .finance.new_withdrawal import new_withdrawal
from .shop.shipment import shipment_method
from .shop.shopping_cart import shopping_cart
from .shop.payment import payment

# --- Components ---
from .shared_ui.layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, header
from .shared_ui.theme import Custom_theme
from .status_bar import pwa_meta_tags, wrap_page_with_statusbar  # ← NUEVO IMPORT
from rxconfig import config

from database import *

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        # Contenedor principal centrado
        rx.desktop_only(
            # Solo se muestra en escritorio
            rx.vstack(
                header(),
                # Contenedor vertical principal
                rx.hstack(
                    # Contenedor horizontal para sidebar y contenido principal
                    desktop_sidebar(),
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
                                height="380px",         # Alto del banner
                                width="100%",           # Ancho completo
                                margin_bottom="0.5em",  # Espacio inferior
                            ),
                            # Fila: Volumen Personal, Puntos NN Travel, Rango mayor, Rango actual
                            rx.hstack(
                                rx.box(
                                    rx.text("Volumen Personal", font_size="0.875rem", color="black"),
                                    rx.text("2,930", font_size="1.5rem", font_weight="bold", color="black"),
                                    bg="#32D74B",             # Fondo verde
                                    on_click=lambda: rx.redirect("/network_reports"),  # Redirige al reporte de red
                                    cursor="pointer",        # Cambia el cursor al pasar por encima
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
                                    on_click=lambda: rx.redirect("/network_reports"),  # Redirige al reporte de red
                                    cursor="pointer",        # Cambia el cursor al pasar por encima
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
                                    rx.link(
                                        rx.button(
                                            "Solicitar comisiones",
                                            bg="#0039F2",
                                            color="white",
                                            border_radius="32px",
                                            width="100%",
                                        ),
                                        width="100%",
                                        height="40px",
                                        href="/new_withdrawal",
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
                            # Propiedades del vstack que contiene el contenido de la página
                            width="100%", # Ancho total del contenido de la página
                        ),
                    ),
                    # Propiedades de flex dentro del vstack que contiene el contenido de la página.
                    width="100%",                  # Ancho completo (Propiedad necesaria para que el contenedor quede centrado no importa si la ventana es muy grande.)
                ),
                # Propiedades vstack que contiene el contenido de la página.
                align="end",        # Centrado vertical
                margin_top="8em",         # Espacio superior
                margin_bottom="2em",      # Espacio inferior
                width="100%",
                max_width="1920px",       # Ancho máximo
            )
        ),
        
        # Versión móvil
        rx.mobile_only(
            rx.vstack(
                # Header móvil
                mobile_header(),

                # Contenido principal móvil
                rx.vstack(
                    # Banner móvil
                    rx.box(
                        rx.image(
                            src="/banner_dashboard.png",
                            height="100%",
                            width="100%",
                            object_fit="cover",
                            border_radius="16px"
                        ),
                        height="200px",
                        width="100%",
                        margin_bottom="1.5rem"
                    ),
                    
                    # Estadísticas principales - Grid 2x2
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.text("Volumen Personal", font_size="0.8rem", color="black", text_align="center"),
                                rx.text("2,930", font_size="1.3rem", font_weight="bold", color="black", text_align="center"),
                                spacing="1"
                            ),
                            bg="#32D74B",
                            padding="16px",
                            border_radius="29px",
                            width="100%",
                            on_click=lambda: rx.redirect("/network_reports")
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("NN Travel", font_size="0.8rem", text_align="center"),
                                rx.text("500", font_size="1.3rem", font_weight="bold", text_align="center"),
                                spacing="1"
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            padding="16px",
                            border_radius="29px",
                            width="100%"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Máximo rango", font_size="0.8rem"),
                                rx.text("E. Consciente", font_size="0.9rem", font_weight="bold"),
                                spacing="1"
                            ),
                            bg="#0039F2",
                            color="white",
                            padding="16px",
                            border_radius="29px",
                            width="100%"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Rango Actual", font_size="0.8rem"),
                                rx.text("E. Transformador", font_size="0.9rem", font_weight="bold"),
                                spacing="1"
                            ),
                            bg="#5E79FF",
                            color="white",
                            padding="16px",
                            border_radius="29px",
                            width="100%"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Lealtad", font_size="0.8rem", text_align="center"),
                                rx.text("100", font_size="1.2rem", font_weight="bold", text_align="center"),
                                spacing="1"
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            padding="16px",
                            border_radius="29px",
                            width="100%"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Cashback", font_size="0.8rem", text_align="center"),
                                rx.text("2,930", font_size="1.2rem", font_weight="bold", text_align="center"),
                                spacing="1"
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            padding="16px",
                            border_radius="29px",
                            width="100%"
                        ),
                        columns="2",
                        spacing="3",
                        width="100%",
                    ),
                    
                    # Progresión de rango
                    rx.box(
                        rx.vstack(
                            rx.text("Progresión siguiente rango", font_size="0.9rem", color="white", text_align="center"),
                            rx.text("754,654 VG – 1,300,000 VG", font_size="1.1rem", font_weight="bold", color="white", text_align="center"),
                            rx.progress(
                                bg="#D0D7FF",
                                fill_color="#0039F2",
                                height="6px",
                                width="100%",
                                value=754654,
                                max=1300000,
                            ),
                            spacing="2"
                        ),
                        bg="#5E79FF",
                        padding="16px",
                        border_radius="29px",
                        width="100%",
                        cursor="pointer",
                        on_click=lambda: rx.redirect("/network_reports")
                    ),
                    
                    # Enlace de referido móvil
                    rx.box(
                        rx.vstack(
                            rx.text("Enlace de referido", font_size="0.9rem", font_weight="bold", margin_bottom="0.5rem"),
                            rx.input(
                                width="100%",
                                value="https://nnprotect.com.mx/ref=244",
                                read_only=True,
                                border_radius="13px",
                                font_size="0.8rem",
                            ),
                            spacing="2"
                        ),
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["tertiary"],
                            dark=Custom_theme().dark_colors()["tertiary"]
                        ),
                        padding="16px",
                        border_radius="29px",
                        width="100%",
                    ),
                    
                    # Reporte de usuarios móvil
                    rx.box(
                        rx.vstack(
                            rx.text("Reporte de usuarios", font_size="0.9rem", font_weight="bold"),
                            rx.hstack(
                                rx.box(bg="#32D74B", height="6px", width="50%", border_radius="3px"),
                                rx.box(bg="#FF3B30", height="6px", width="50%", border_radius="3px"),
                                spacing="1",
                                width="100%"
                            ),
                            rx.hstack(
                                rx.text("Activos: 501", font_size="0.8rem"),
                                rx.spacer(),
                                rx.text("Inactivos: 501", font_size="0.8rem")
                            ),
                            spacing="2"
                        ),
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["tertiary"],
                            dark=Custom_theme().dark_colors()["tertiary"]
                        ),
                        padding="16px",
                        border_radius="29px",
                        width="100%",
                    ),
                    
                    # Finanzas móvil
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.text("Estimado ganancia mes", font_size="0.8rem", text_align="center"),
                                rx.text("$42,659,227", font_size="1.1rem", font_weight="bold", text_align="center"),
                                spacing="1"
                            ),
                            bg="#0039F2",
                            color="white",
                            padding="16px",
                            border_radius="29px",
                            width="100%"
                        ),
                        rx.hstack(
                            rx.box(
                                rx.vstack(
                                    rx.text("Billetera", font_size="0.8rem", text_align="center"),
                                    rx.text("$53,324,034", font_size="1rem", font_weight="bold", text_align="center"),
                                    spacing="1"
                                ),
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                                padding="16px",
                                border_radius="29px",
                                width="49%"
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.text("En espera", font_size="0.8rem", text_align="center"),
                                    rx.text("$10,664,806", font_size="1rem", font_weight="bold", text_align="center"),
                                    spacing="1"
                                ),
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                                padding="16px",
                                border_radius="29px",
                                width="49%"
                            ),
                            justify="between",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.link(
                                rx.button(
                                    "Solicitar comisiones",
                                    bg="#0039F2",
                                    color="white",
                                    border_radius="22px",
                                    height="48px",
                                    width="100%",
                                ),
                                width="100%",
                                href="/new_withdrawal",
                            ),
                            rx.link(
                                rx.button(
                                    "Transferencia interna",
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    color=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["text"],
                                        dark=Custom_theme().dark_colors()["text"]
                                    ),
                                    border="1px solid #0039F2",
                                    border_radius="22px",
                                    height="48px",
                                    width="100%",
                                ),
                                width="100%",
                                href="/",
                            ),
                            spacing="2",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%",
                        margin_bottom="1.5rem"
                    ),
                    
                    # Herramientas móvil
                    rx.vstack(
                        rx.text("Herramientas para tu negocio", font_size="1rem", font_weight="bold"),
                        rx.grid(
                            *[rx.box(
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ), 
                                height="60px", 
                                border_radius="8px"
                            ) for _ in range(8)],
                            columns="2",
                            spacing="2",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    spacing="4",
                    width="100%",
                    padding="1rem",
                    margin_top="80px",
                    margin_bottom="0.2em",
                ),
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["background"],
                    dark=Custom_theme().dark_colors()["background"]
                ),
                width="100%",
            ),
            width="100%",
        ),
        # Propiedades del contenedor principal.
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),                              # Fondo según modo
        position="absolute",            # Posición absoluta
        width="100%",                  # Ancho de la ventana
    )

pwa_meta = rx.el.meta(
    name="apple-mobile-web-app-status-bar-style",
    content="black-translucent"
)
app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        pwa_meta
    ]
)

app.add_page(index, title="NN Protect | Dashboard", route="/dashboard")
app.add_page(login, title="NN Protect | Iniciar sesión", route="/login")
app.add_page(register, title="NN Protect | Nuevo registro", route="/new_register")
app.add_page(network, title="NN Protect | Red", route="/network")
app.add_page(network_reports, title="NN Protect | Reportes de Red", route="/network_reports")
app.add_page(income_reports, title="NN Protect | Reportes de Ingresos", route="/income_reports")
app.add_page(store, title="NN Protect | Tienda", route="/store")
app.add_page(orders, title="NN Protect | Órdenes", route="/orders")
app.add_page(order_details, title="NN Protect | Detalles de Orden", route="/order_details")
app.add_page(withdrawals, title="NN Protect | Retiros", route="/withdrawals")
app.add_page(new_withdrawal, title="NN Protect | Nuevo Retiro", route="/new_withdrawal")
app.add_page(shipment_method, title="NN Protect | Método de Envío", route="/shipment_method")
app.add_page(shopping_cart, title="NN Protect | Carrito de Compras", route="/shopping_cart")
app.add_page(payment, title="NN Protect | Método de Pago", route="/payment")