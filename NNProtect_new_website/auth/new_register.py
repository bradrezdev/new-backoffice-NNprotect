"""Nueva Backoffice NN Protect | Nuevo registro"""

import reflex as rx
from ..shared_ui.theme import Custom_theme
from rxconfig import config
from ..shared_ui.layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, header

from .auth_state import AuthState
from database.addresses import Countries

def register() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        rx.desktop_only(
            rx.vstack(
                header(),  # Muestra el usuario logueado en la esquina superior derecha
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
                                        font_size="1.25rem",
                                        font_weight="bold",
                                        margin_bottom="0.5em"
                                    ),
                                    rx.text("Nombre(s)*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Escribe tu(s) nombre(s)...",
                                        value=AuthState.user_firstname,
                                        on_change=AuthState.set_firstname,
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Apellido(s)*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Escribe tu(s) apellido(s)...",
                                        value=AuthState.user_lastname,
                                        on_change=AuthState.set_lastname,
                                        border_radius="12px",
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
                                        value=AuthState.gender,
                                        on_change=AuthState.set_gender,
                                        border_radius="12px",
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
                                        value=AuthState.street_number,
                                        on_change=AuthState.set_street_number,
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
                                        value=AuthState.neighborhood,
                                        on_change=AuthState.set_neighborhood,
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
                                        value=AuthState.city,
                                        on_change=AuthState.set_city,
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("País*", font_weight="medium"),
                                    rx.select(
                                        AuthState.country_options,
                                        placeholder="Seleccionar país",
                                        value=AuthState.country,
                                        on_change=AuthState.set_country,
                                        border_radius="14px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        size="3",
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Estado*", font_weight="medium"),
                                    rx.select(
                                        AuthState.state_options,
                                        placeholder="Seleccionar estado",
                                        value=AuthState.state,
                                        on_change=AuthState.set_state,
                                        disabled=~(AuthState.country != ""),
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
                                        value=AuthState.zip_code,
                                        on_change=AuthState.set_zip_code,
                                        border_radius="14px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.text("Celular*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Ejemplo: 3121234567",
                                        value=AuthState.phone_number,
                                        on_change=AuthState.set_phone_number,
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    spacing="3",
                                    width="48%",
                                ),
                                # --------- Acceso al sistema (Columna Derecha) ---------
                                rx.vstack(
                                    rx.text(
                                        "Acceso al sistema",
                                        font_size="1.25rem",
                                        font_weight="bold",
                                        margin_bottom="0.5em"
                                    ),
                                    rx.text("Usuario*", font_weight="medium"),
                                    rx.input(
                                        placeholder="Usuario único",
                                        value=AuthState.username,
                                        on_change=AuthState.set_username,
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
                                        value=AuthState.email,
                                        on_change=AuthState.set_email,
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
                                        value=AuthState.password,
                                        on_change=AuthState.set_password,
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
                                        font_size="0.95rem",
                                        font_weight="bold",
                                        margin_top="0.5em"
                                    ),
                                    rx.form(
                                        rx.list_item("Debe contener mínimo 8 caracteres."),
                                        rx.list_item("Debe incluir mínimo 1 letra mayúscula."),
                                        rx.list_item("Debe incluir mínimo 1 letra minúscula."),
                                        rx.list_item("Debe incluir mínimo 1 número."),
                                        rx.list_item("Debe incluir mínimo 1 carácter/símbolo especial."),
                                        font_size="0.85rem",
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
                                        value=AuthState.confirmed_password,
                                        on_change=AuthState.set_confirmed_password,
                                        border_radius="12px",
                                        bg=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["tertiary"],
                                            dark=Custom_theme().dark_colors()["tertiary"]
                                        ),
                                        height="40px",
                                        width="100%",
                                    ),
                                    rx.hstack(
                                        rx.checkbox(
                                            checked=AuthState.terms_accepted,
                                            on_change=AuthState.set_terms_accepted,
                                        ),
                                        rx.text(
                                            "He leído los términos y condiciones.",
                                            font_size="0.97rem"
                                        ),
                                        rx.link(
                                            "Leer términos y condiciones",
                                            href="#",
                                            font_size="0.97rem",
                                            color="#0039F2",
                                            margin_left="0.2em",
                                            underline="always"
                                        ),
                                        spacing="1"
                                    ),
                                    rx.button(
                                        "Registrarse",
                                        bg="#0039F2",
                                        color="white",
                                        border_radius="12px",
                                        width="100%",
                                        height="48px",
                                        margin_top="1.5em",
                                        font_size="1.1rem",
                                        font_weight="bold",
                                        on_click=AuthState.new_register,
                                    ),
                                    width="48%",
                                    spacing="3",
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
                align="end",
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
                rx.form(
                    rx.vstack(
                        rx.text(
                            f"Referido por {AuthState.get_user_display_name}",
                            font_size="1em",
                            color=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["primary"],
                                dark=Custom_theme().dark_colors()["primary"]
                            ),
                            font_weight="bold",
                            margin_bottom="1em"
                        ),
                        
                        # Información personal
                        rx.text("Información Personal", font_weight="bold", font_size="1.1em", margin_bottom="0.5em"),
                        
                        rx.text(
                            "Nombre(s)*",
                            font_weight="medium",
                            font_size="1em",
                            ),
                        rx.input(
                            placeholder="Escribe tu(s) nombre(s)...",
                            value=AuthState.user_firstname,
                            on_change=AuthState.set_firstname,
                            required=True,
                            reset_on_submit=True,
                            border_radius="15px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="48px",
                            width="100%",
                            font_size="1em",
                        ),

                        rx.text(
                            "Apellido(s)*",
                            font_weight="medium",
                            font_size="1em",
                            ),
                        rx.input(
                            placeholder="Escribe tu(s) apellido(s)...",
                            value=AuthState.user_lastname,
                            on_change=AuthState.set_lastname,
                            required=True,
                            reset_on_submit=True,
                            border_radius="15px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="48px",
                            width="100%",
                            font_size="1em",
                        ),

                        rx.text("Sexo*", font_weight="medium", font_size="1em"),
                        rx.select(
                            ["Masculino", "Femenino"],
                            placeholder="Seleccionar una opción",
                            radius="large",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],  # Corregido
                                dark=Custom_theme().dark_colors()["tertiary"]     # Corregido
                            ),
                            width="100%",
                            size="3",
                            required=True,
                            value=AuthState.gender,
                            on_change=AuthState.set_gender,
                        ),

                        rx.text("Celular*", font_weight="medium", font_size="1em"),
                        rx.input(
                            placeholder="Ejemplo: 3121234567",
                            value=AuthState.phone_number,
                            on_change=AuthState.set_phone_number,
                            border_radius="15px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],  # Corregido
                                dark=Custom_theme().dark_colors()["tertiary"]     # Corregido
                            ),
                            height="48px",
                            width="100%",
                            font_size="1em",
                            margin_bottom="1rem"
                        ),

                        # Dirección
                        rx.text("Dirección", font_weight="bold", font_size="1.1em", margin_bottom="0.5em"),

                        rx.text("Calle y número*", font_weight="medium", font_size="1em"),
                        rx.input(
                            placeholder="Ejemplo: Av. Siempre Viva #742",
                            value=AuthState.street_number,
                            on_change=AuthState.set_street_number,
                            border_radius="15px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="48px",
                            width="100%",
                            font_size="1em",
                        ),

                        rx.text("Colonia*", font_weight="medium", font_size="1em"),
                        rx.input(
                            placeholder="Ejemplo: Centro",
                            value=AuthState.neighborhood,
                            on_change=AuthState.set_neighborhood,
                            border_radius="15px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="48px",
                            width="100%",
                            font_size="1em",
                        ),

                        rx.hstack(
                            rx.vstack(
                                rx.text("Ciudad*", font_weight="medium", font_size="1em"),
                                rx.input(
                                    placeholder="Ciudad",
                                    value=AuthState.city,
                                    on_change=AuthState.set_city,
                                    border_radius="15px",
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    height="48px",
                                    width="100%",
                                    font_size="1em",
                                ),
                                width="48%"
                            ),
                            rx.vstack(
                                rx.text("C.P.*", font_weight="medium", font_size="1em"),
                                rx.input(
                                    placeholder="28000",
                                    value=AuthState.zip_code,
                                    on_change=AuthState.set_zip_code,
                                    border_radius="15px",
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    height="48px",
                                    width="100%",
                                    font_size="1em",
                                ),
                                width="50%"
                            ),
                            justify="between",
                            width="100%",
                        ),

                        rx.text("País*", font_weight="medium", font_size="1em"),
                        rx.select(
                            AuthState.country_options,
                            placeholder="Seleccionar país",
                            value=AuthState.country,
                            on_change=AuthState.set_country,
                            radius="large",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            width="100%",
                            size="3",
                            required=True,
                        ),

                        rx.text("Estado*", font_weight="medium", font_size="1em"),
                        rx.select(
                            AuthState.state_options,
                            placeholder="Seleccionar estado",
                            value=AuthState.state,
                            on_change=AuthState.set_state,
                            disabled=~(AuthState.country != ""),
                            radius="large",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            width="100%",
                            size="3",
                            required=True,
                        ),

                        # Acceso al sistema
                        rx.text("Acceso al Sistema", font_weight="bold", font_size="1.1em", margin_bottom="0.5rem"),

                        rx.text("Usuario*", font_weight="medium", font_size="1em"),
                        rx.input(
                            placeholder="Usuario único",
                            value=AuthState.username,
                            on_change=AuthState.set_username,
                            required=True,
                            reset_on_submit=True,
                            border_radius="15px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="48px",
                            width="100%",
                            font_size="1em",
                        ),

                        rx.text("Correo electrónico*", font_weight="medium", font_size="1em"),
                        rx.input(
                            type="email",
                            placeholder="Correo electrónico",
                            value=AuthState.email,
                            on_change=AuthState.set_email,
                            required=True,
                            reset_on_submit=True,
                            border_radius="15px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="48px",
                            width="100%",
                            font_size="1em",
                        ),

                        rx.text("Contraseña*", font_weight="medium", font_size="1em"),
                        rx.input(
                            type="password",
                            placeholder="Crea una contraseña",
                            value=AuthState.password,
                            on_change=AuthState.set_password,
                            required=True,
                            reset_on_submit=True,
                            border_radius="15px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="48px",
                            width="100%",
                            font_size="1em",
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
                        rx.text("Confirmar contraseña*", font_weight="medium", font_size="1em"),
                        rx.input(
                            type="password",
                            placeholder="Confirma la contraseña",
                            value=AuthState.confirmed_password,
                            on_change=AuthState.set_confirmed_password,
                            required=True,
                            reset_on_submit=True,
                            border_radius="15px",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            height="48px",
                            width="100%",
                            font_size="1em",
                        ),
                        
                        # Términos y condiciones
                        rx.hstack(
                            rx.checkbox(
                                checked=AuthState.terms_accepted,  # Corregir prop obsoleto
                                on_change=AuthState.set_terms_accepted,
                                required=True,
                            ),
                            rx.text(
                                "He leído los ", rx.link("terminos y condiciones.", href="#"),
                                font_size="0.85em"  # --- Propiedades rx.text ---
                            ),
                            margin_bottom="1.5rem",
                            spacing="1"  # --- Propiedades rx.hstack ---
                        ),
                        
                        rx.button(
                            "Registrarse",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["primary"],
                                dark=Custom_theme().dark_colors()["primary"]
                            ),
                            color="white",
                            border_radius="24px",
                            width="100%",
                            height="64px",
                            font_size="1.1rem",
                            font_weight="bold",
                            type="submit",
                            on_click=AuthState.new_register,
                        ),
                        
                        spacing="3",
                        width="100%"
                    ),
                    width="100%",
                    padding="10px",
                    margin_top="80px",
                    margin_bottom="15px"
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
        #on_mount=AuthState.load_user_from_token,
    )