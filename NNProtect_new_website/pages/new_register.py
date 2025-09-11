"""Nueva Backoffice NN Protect | Nuevo registro"""

import reflex as rx
from ..theme import Custom_theme
from rxconfig import config
from ..layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar

def register() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    desktop_sidebar(),
                    # Container de la derecha. Contiene el formulario de registro.
                    main_container_derecha(
                        rx.vstack(
                            rx.text(
                                "Nuevo registro referido por Bryan Núñez",
                                font_size="2rem",  # --- Propiedades rx.text ---
                                font_weight="bold",
                                margin_bottom="0.5em"
                            ),
                            rx.hstack(
                                # --------- Información de contacto (Columna Izquierda) ---------
                                rx.vstack(
                                    rx.text(
                                        "Información de contacto",
                                        font_size="1.25rem",  # --- Propiedades rx.text ---
                                        font_weight="bold",
                                        margin_bottom="0.5em"
                                    ),
                                    rx.text("Nombre completo*", font_weight="medium"),  # --- Propiedades rx.text ---
                                    rx.input(
                                        placeholder="Escribe el nombre completo...",
                                        border_radius="12px",  # --- Propiedades rx.input ---
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Sexo*", font_weight="medium"),
                                    rx.select(
                                        ["Masculino", "Femenino"],
                                        placeholder="Seleccionar una opción",
                                        border_radius="12px",  # --- Propiedades rx.select ---
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        radius="large",
                                        size="3",
                                        width="100%",
                                    ),
                                    rx.text("Calle y número*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Ejemplo: Av. Siempre Viva #742",
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Colonia*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Ejemplo: Centro",
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Ciudad*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Ejemplo: Colima",
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Estado*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Ejemplo: Colima",
                                        border_radius="14px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Código postal*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Ejemplo: 28000",
                                        border_radius="14px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("País*", font_weight="medium"),
                                    rx.select(
                                        ["México", "USA", "Otro"],
                                        placeholder="Seleccionar una opción",
                                        border_radius="14px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        size="3",
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Celular*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Ejemplo: 3121234567",
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("CURP*", font_weight="medium"),
                                    rx.input(
                                        placeholder="CURP del usuario",
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    spacing="3",  # --- Propiedades rx.vstack ---
                                    width="48%",
                                    #min_width="370px",
                                ),
                                # --------- Acceso al sistema (Columna Derecha) ---------
                                rx.vstack(
                                    rx.text(
                                        "Acceso al sistema",
                                        font_size="1.25rem",  # --- Propiedades rx.text ---
                                        font_weight="bold",
                                        margin_bottom="0.5em"
                                    ),
                                    rx.text("Usuario*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Usuario único",
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Correo electrónico*", font_weight="medium"),
                                    rx.input(
                                        type="email",
                                        placeholder="Correo electrónico",
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Contraseña*", font_weight="medium"),
                                    rx.input(
                                        type="password",
                                        placeholder="Crea una contraseña",
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text(
                                        "Requisitos de la contraseña:",
                                        font_size="0.95rem",  # --- Propiedades rx.text ---
                                        font_weight="bold",
                                        margin_top="0.5em"
                                    ),
                                    rx.form(
                                        rx.list_item("Debe contener mínimo 8 caracteres."),
                                        rx.list_item("Debe incluir mínimo 1 letra mayúscula."),
                                        rx.list_item("Debe incluir mínimo 1 letra minúscula."),
                                        rx.list_item("Debe incluir mínimo 1 número."),
                                        rx.list_item("Debe incluir mínimo 1 carácter/símbolo especial."),
                                        font_size="0.85rem",  # --- Propiedades rx.form ---
                                        style={"margin-left": "1em", "color": "#333"},
                                    ),
                                    rx.text(
                                        "Confirmar contraseña*",
                                        font_weight="medium",
                                        margin_top="0.7em"
                                    ),
                                    rx.input(
                                        type="password",
                                        placeholder="Confirma la contraseña",
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.hstack(
                                        rx.checkbox(),
                                        rx.text(
                                            "He leído los términos y condiciones.",
                                            font_size="0.97rem"  # --- Propiedades rx.text ---
                                        ),
                                        rx.link(
                                            "Leer términos y condiciones",
                                            href="#",
                                            font_size="0.97rem",  # --- Propiedades rx.link ---
                                            color="#0039F2",
                                            margin_left="0.2em",
                                            underline="always"
                                        ),
                                        spacing="1"  # --- Propiedades rx.hstack ---
                                    ),
                                    rx.button(
                                        "Registrarse",
                                        bg="#0039F2",  # --- Propiedades rx.button ---
                                        color="white",
                                        border_radius="12px",
                                        width="100%",
                                        height="48px",
                                        margin_top="1.5em",
                                        font_size="1.1rem",
                                        font_weight="bold"
                                    ),
                                    width="48%",
                                    spacing="3",  # --- Propiedades rx.vstack ---

                                ),
                                spacing="9",  # --- Propiedades rx.hstack ---
                                width="100%",
                            ),
                            # Propiedades @Main container de la derecha
                            width="100%", # Ancho total del contenido de la página
                        ),
                    ),
                    width="100%", # Propiedad necesaria para que el contenedor quede centrado no importa si la ventana es muy grande.
                ),
                # Propiedades vstack que contiene el contenido de la página.
                justify="center",  # --- Propiedades rx.vstack ---
                margin_top="120px",
                margin_bottom="2em",
                max_width="1920px",
            )
        ),
        
        # Versión móvil
        rx.mobile_only(
            rx.vstack(
                # Header móvil
                mobile_header(),
                
                # Contenido principal móvil
                rx.form(
                    rx.vstack(
                        rx.text(
                            "Referido por Bryan Núñez",
                            font_size="0.9rem",
                            color=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["primary"],
                                dark=Custom_theme().dark_colors()["primary"]
                            ),
                            font_weight="bold",
                            margin_bottom="1rem"
                        ),
                        
                        # Información personal
                        rx.text("Información Personal", font_weight="bold", font_size="1.1rem", margin_bottom="0.5rem"),
                        
                        rx.text("Nombre completo*", font_weight="medium", font_size="0.9rem"),
                        rx.input(
                            placeholder="Escribe el nombre completo...",
                            border_radius="8px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="45px",
                            width="100%",
                            margin_bottom="0.5rem"
                        ),
                        
                        rx.text("Sexo*", font_weight="medium", font_size="0.9rem"),
                        rx.select(
                            ["Masculino", "Femenino"],
                            placeholder="Seleccionar una opción",
                            border_radius="8px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            width="100%",
                            margin_bottom="0.5rem"
                        ),
                        
                        rx.text("Celular*", font_weight="medium", font_size="0.9rem"),
                        rx.input(
                            placeholder="Ejemplo: 3121234567",
                            border_radius="8px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="45px",
                            width="100%",
                            margin_bottom="1rem"
                        ),
                        
                        # Dirección
                        rx.text("Dirección", font_weight="bold", font_size="1.1rem", margin_bottom="0.5rem"),
                        
                        rx.text("Calle y número*", font_weight="medium", font_size="0.9rem"),
                        rx.input(
                            placeholder="Ejemplo: Av. Siempre Viva #742",
                            border_radius="8px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="45px",
                            width="100%",
                            margin_bottom="0.5rem"
                        ),
                        
                        rx.hstack(
                            rx.vstack(
                                rx.text("Ciudad*", font_weight="medium", font_size="0.9rem"),
                                rx.input(
                                    placeholder="Ciudad",
                                    border_radius="8px",
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    height="45px",
                                    width="100%",
                                ),
                                width="48%"
                            ),
                            rx.vstack(
                                rx.text("C.P.*", font_weight="medium", font_size="0.9rem"),
                                rx.input(
                                    placeholder="28000",
                                    border_radius="8px",
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    height="45px",
                                    width="100%",
                                ),
                                width="48%"
                            ),
                            justify="between",
                            width="100%",
                            margin_bottom="1rem"
                        ),
                        
                        # Acceso al sistema
                        rx.text("Acceso al Sistema", font_weight="bold", font_size="1.1rem", margin_bottom="0.5rem"),
                        
                        rx.text("Usuario*", font_weight="medium", font_size="0.9rem"),
                        rx.input(
                            placeholder="Usuario único",
                            border_radius="8px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="45px",
                            width="100%",
                            margin_bottom="0.5rem"
                        ),
                        
                        rx.text("Correo electrónico*", font_weight="medium", font_size="0.9rem"),
                        rx.input(
                            type="email",
                            placeholder="Correo electrónico",
                            border_radius="8px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="45px",
                            width="100%",
                            margin_bottom="0.5rem"
                        ),
                        
                        rx.text("Contraseña*", font_weight="medium", font_size="0.9rem"),
                        rx.input(
                            type="password",
                            placeholder="Crea una contraseña",
                            border_radius="8px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="45px",
                            width="100%",
                            margin_bottom="0.5rem"
                        ),
                        
                        rx.text("Confirmar contraseña*", font_weight="medium", font_size="0.9rem"),
                        rx.input(
                            type="password",
                            placeholder="Confirma la contraseña",
                            border_radius="8px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="45px",
                            width="100%",
                            margin_bottom="1rem"
                        ),
                        
                        # Términos y condiciones
                        rx.hstack(
                            rx.checkbox(),
                            rx.text(
                                "Acepto términos y condiciones",
                                font_size="0.8rem"
                            ),
                            spacing="2",
                            margin_bottom="1.5rem"
                        ),
                        
                        rx.button(
                            "Registrarse",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["primary"],
                                dark=Custom_theme().dark_colors()["primary"]
                            ),
                            color="white",
                            border_radius="12px",
                            width="100%",
                            height="50px",
                            font_size="1.1rem",
                            font_weight="bold",
                            type="submit"
                        ),
                        
                        spacing="3",
                        width="100%"
                    ),
                    width="100%",
                    padding="1rem",
                    margin_top="80px",
                    margin_bottom="2rem"
                ),
                
                width="100%",
                min_height="100vh",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["background"],
                    dark=Custom_theme().dark_colors()["background"]
                )
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