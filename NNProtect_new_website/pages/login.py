"""Proyecto Final | Programación Avanzada | Log in Page"""

import reflex as rx
from rxconfig import config
#from ..state import Login
from ..theme import Custom_theme

def login() -> rx.Component:
    # Contenedor principal
    return rx.flex(
        
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

                    rx.text("Correo electrónico"),
                    rx.input(
                        placeholder="Escribe tu correo electrónico",
                        type="email",
                        #value=Login.email,
                        #on_change=Login.setEmail,
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
                        #value=Login.password,
                        #on_change=Login.setPassword,
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

                    rx.hstack(
                        rx.spacer(),
                        rx.text("¿No tienes una cuenta?", size="1"),
                        rx.link("Crear una cuenta", href="/sign_up", color=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["primary"],
                        dark=Custom_theme().dark_colors()["primary"]
                    ), size="1"),
                        rx.spacer(),
                        spacing="1",
                        width="100%",
                    ),
                ),

                # Propiedades del formulario
                #on_submit=Login.login_user,
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