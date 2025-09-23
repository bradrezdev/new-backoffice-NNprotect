"""Proyecto Final | Programación Avanzada | Log in Page"""

import reflex as rx
from rxconfig import config
#from ..state import Login
from ..shared_ui.theme import Custom_theme
from .auth_state import AuthState

def login() -> rx.Component:
    # Contenedor principal
    return rx.box(
        # Versión escritorio
        rx.desktop_only(
            rx.flex(
                
                # Contenedor izquierdo | Formulario
                rx.vstack(
                    
                    rx.image(src="/logotipo.png", width="200px", height="auto"),

                    # Formulario de inicio de sesión
                    rx.form(
                        
                        # Inputs del formulario
                        rx.vstack(

                            rx.heading("Bienvenido de vuelta", size="8"),

                            rx.text("Qué gusto volverte a ver. Por favor, ingresa los datos de tu cuenta:"),
                            
                            rx.spacer(),

                            rx.text("Nombre de usuario"),
                            rx.input(
                                placeholder="Escribe tu nombre de usuario",
                                type="text",
                                value=AuthState.username,
                                on_change=AuthState.set_username,
                                required=True,
                                style={"border": "1px solid black"},
                                border_color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ),
                                border_radius="8px",
                                height="40px",
                                width="25vw",
                            ),

                            rx.text("Contraseña"),
                            rx.input(
                                placeholder="Escribe tu contraseña",
                                type="password",
                                value=AuthState.password,
                                on_change=AuthState.set_password,
                                required=True,
                                style={"border": "1px solid black"},
                                border_color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ),
                                border_radius="8px",
                                height="40px",
                                width="25vw",
                            ),

                            rx.link("Olvidé mi contraseña", href="/reset-password", color=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["primary"],
                                dark=Custom_theme().dark_colors()["primary"]
                            ), size="1"),

                            rx.button(
                                rx.text("Iniciar sesión"),
                                height="47px",
                                width="25vw",
                                type="submit",
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ),
                                border_radius="8px",
                            ),
                        ),

                        # Propiedades del formulario
                        on_submit=AuthState.login_user,
                        padding="20%",
                        width="100%",
                    ),

                    # Propiedades del contenedor izquierdo
                    justify="center",
                    padding="4%",
                    width="50%",
                ),

                # Contenedor derecho | Imagen
                rx.center(
                    rx.image(src="/image_login.png", width="80%", height="auto", align="center"),
                    width="50%",
                ),

                # Propiedades contenedor principal
                height="100vh",
                max_width="1920",
                width="100%",
            )
        ),
        
        # Versión móvil
        rx.mobile_only(
            rx.center(
                rx.vstack(
                    # Logo centrado
                    rx.center(
                        rx.image(src="/logotipo.png", width="150px", height="auto"),
                        width="100%",
                        margin_bottom="2rem"
                    ),
                    
                    # Formulario móvil
                    rx.form(
                        rx.vstack(
                            rx.heading("Bienvenido de vuelta", size="6", text_align="center"),
                            
                            rx.text(
                                "Qué gusto volverte a ver. Por favor, ingresa los datos de tu cuenta:",
                                text_align="center",
                                font_size="0.9rem",
                                margin_bottom="1rem"
                            ),
                            
                            rx.text("Nombre de usuario", font_weight="bold", font_size="0.9rem"),
                            rx.input(
                                placeholder="Escribe tu nombre de usuario",
                                type="text",
                                value=AuthState.username,
                                on_change=AuthState.set_username,
                                required=True,
                                border_color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ),
                                border_radius="8px",
                                height="45px",
                                width="100%",
                                margin_bottom="1rem"
                            ),
                            
                            rx.text("Contraseña", font_weight="bold", font_size="0.9rem"),
                            rx.input(
                                placeholder="Escribe tu contraseña",
                                type="password",
                                value=AuthState.password,
                                on_change=AuthState.set_password,
                                required=True,
                                border_color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ),
                                border_radius="8px",
                                height="45px",
                                width="100%",
                                margin_bottom="0.5rem"
                            ),
                            
                            rx.link(
                                "Olvidé mi contraseña", 
                                href="/reset-password", 
                                color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ), 
                                size="1",
                                text_align="center",
                                width="100%",
                                margin_bottom="1.5rem"
                            ),
                            
                            rx.button(
                                "Iniciar sesión",
                                height="50px",
                                width="100%",
                                type="submit",
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ),
                                color="white",
                                border_radius="8px",
                                font_weight="bold",
                                margin_bottom="1rem",
                            ),
                            
                            spacing="3",
                            width="100%"
                        ),
                        on_submit=AuthState.login_user,
                        width="100%",
                        padding="1rem"
                    ),
                    
                    # Imagen decorativa pequeña para móvil
                    rx.center(
                        rx.image(src="/image_login.png", width="200px", height="auto", opacity="0.3"),
                        width="100%",
                        margin_top="2rem"
                    ),
                    
                    spacing="4",
                    width="100%",
                    max_width="400px",
                    padding="2rem"
                ),
                height="100vh",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["background"],
                    dark=Custom_theme().dark_colors()["background"]
                )
            )
        ),
        
        width="100%",
        height="100vh"
    )