"""
Página principal de Admin App con UI minimalista
"""

import reflex as rx
from .admin_state import AdminState
from .components import (
    admin_card, admin_input, admin_select, admin_button,
    admin_alert, admin_section_header, admin_form_group,
    admin_divider, admin_stat_card
)
from .theme import COLORS, HEADING_STYLE


def admin_header() -> rx.Component:
    """Header simple y funcional"""
    return rx.box(
        rx.hstack(
            rx.heading(
                "Admin Panel",
                font_size="1.5rem",
                font_weight="700",
                color=COLORS["gray_900"],
            ),
            rx.badge(
                "NN Protect",
                background=COLORS["primary"],
                color="white",
                padding="0.5rem 1rem",
                border_radius="9999px",
                font_size="0.875rem",
                font_weight="600",
            ),
            justify="between",
            align="center",
            width="100%"
        ),
        background="white",
        padding="1.25rem 2rem",
        border_bottom=f"1px solid {COLORS['gray_200']}",
        position="sticky",
        top="0",
        z_index="100",
    )


def admin_alert_banner() -> rx.Component:
    """Banner de alertas"""
    return rx.cond(
        AdminState.show_alert,
        rx.box(
            admin_alert(AdminState.alert_message, AdminState.alert_variant),
            rx.button(
                "✕",
                on_click=AdminState.hide_alert,
                position="absolute",
                right="1rem",
                top="50%",
                transform="translateY(-50%)",
                background="transparent",
                border="none",
                cursor="pointer",
                font_size="1.25rem",
                color=COLORS["gray_500"],
                _hover={"color": COLORS["gray_700"]}
            ),
            position="relative",
            margin_bottom="1.5rem"
        )
    )


# ===================== TAB 1: CREAR CUENTA =====================

def tab_create_account() -> rx.Component:
    """Tab para crear cuenta sin sponsor - diseño mobile"""
    return rx.vstack(
        rx.text(
            "Crear Cuenta sin Sponsor",
            font_weight="700",
            font_size="1.25rem",
            color=COLORS["gray_900"],
            margin_bottom="0.5rem"
        ),
        rx.text(
            "Registra un nuevo usuario sin necesidad de sponsor",
            font_size="0.9375rem",
            color=COLORS["gray_600"],
            margin_bottom="2rem"
        ),

        admin_input(
            "Nombre*",
            placeholder="Ej: Juan",
            value=AdminState.new_user_first_name,
            on_change=AdminState.set_new_user_first_name
        ),

        admin_input(
            "Apellido*",
            placeholder="Ej: Pérez",
            value=AdminState.new_user_last_name,
            on_change=AdminState.set_new_user_last_name
        ),

        admin_input(
            "Email*",
            placeholder="usuario@ejemplo.com",
            value=AdminState.new_user_email,
            on_change=AdminState.set_new_user_email,
            input_type="email"
        ),

        admin_input(
            "Contraseña (opcional)",
            placeholder="••••••••",
            value=AdminState.new_user_password,
            on_change=AdminState.set_new_user_password,
            input_type="password"
        ),

        admin_select(
            "País*",
            ["Mexico", "USA", "Colombia", "Republica Dominicana"],
            value=AdminState.new_user_country,
            on_change=AdminState.set_new_user_country
        ),

        admin_select(
            "Género*",
            ["male", "female"],
            value=AdminState.new_user_gender,
            on_change=AdminState.set_new_user_gender
        ),

        rx.box(height="1rem"),

        admin_button(
            "Crear Usuario",
            on_click=AdminState.create_account_without_sponsor,
            disabled=AdminState.is_loading,
            width="100%"
        ),

        spacing="4",
        width="100%",
        max_width="600px",
    )


# ===================== TAB 2: USUARIOS TESTS =====================

def tab_test_users() -> rx.Component:
    """Tab para crear usuarios de prueba"""
    return rx.vstack(
        admin_section_header(
            "Crear Usuarios de Prueba",
            "Genera múltiples usuarios de prueba con un sponsor específico"
        ),

        admin_card(
            "Configuración de Usuarios",

            admin_form_group(
                admin_input(
                    "Member ID del Sponsor",
                    placeholder="1",
                    value=AdminState.test_users_sponsor_id,
                    on_change=AdminState.set_test_users_sponsor_id,
                    input_type="number"
                ),
                admin_select(
                    "País de Registro",
                    ["Mexico", "USA", "Colombia", "Republica Dominicana"],
                    value=AdminState.test_users_country,
                    on_change=AdminState.set_test_users_country
                ),
                columns=2
            ),

            admin_divider(),

            admin_input(
                "Cantidad de Usuarios (máx. 100)",
                placeholder="10",
                value=AdminState.test_users_quantity,
                on_change=AdminState.set_test_users_quantity,
                input_type="number"
            ),

            rx.box(height="1rem"),

            admin_button(
                "Crear Usuarios de Prueba",
                on_click=AdminState.create_test_users,
                disabled=AdminState.is_loading,
                width="100%"
            )
        ),

        spacing="6",
        width="100%"
    )


# ===================== TAB 3: CREAR ÓRDENES =====================

def tab_create_orders() -> rx.Component:
    """Tab para crear órdenes"""
    return rx.vstack(
        admin_section_header(
            "Crear Órdenes",
            "Genera órdenes con 5 productos de suplementos predefinidos"
        ),

        admin_card(
            "Configuración de Órdenes",

            admin_input(
                "Member IDs (separados por coma)",
                placeholder="1, 2, 3, 4",
                value=AdminState.orders_member_ids,
                on_change=AdminState.set_orders_member_ids
            ),

            admin_divider(),

            admin_input(
                "Cantidad de Órdenes por Usuario (máx. 10)",
                placeholder="1",
                value=AdminState.orders_quantity,
                on_change=AdminState.set_orders_quantity,
                input_type="number"
            ),

            rx.box(height="1rem"),

            rx.box(
                rx.text(
                    "ℹ️ Cada orden incluirá 5 productos de suplementos",
                    font_size="0.875rem",
                    color=COLORS["gray_600"]
                ),
                background=f"{COLORS['info']}10",
                padding="0.75rem",
                border_radius="0.5rem",
                margin_bottom="1rem"
            ),

            admin_button(
                "Crear Órdenes",
                on_click=AdminState.create_orders,
                disabled=AdminState.is_loading,
                width="100%"
            )
        ),

        spacing="6",
        width="100%"
    )


# ===================== TAB 4: RED DESCENDENTE =====================

def tab_network_tree() -> rx.Component:
    """Tab para crear red descendente"""
    return rx.vstack(
        admin_section_header(
            "Crear Red Descendente",
            "Genera una estructura de red completa desde un usuario raíz"
        ),

        admin_card(
            "Configuración de Red",

            admin_input(
                "Member ID Raíz",
                placeholder="1",
                value=AdminState.network_root_member_id,
                on_change=AdminState.set_network_root_member_id,
                input_type="number"
            ),

            admin_divider(),

            admin_form_group(
                admin_select(
                    "Estructura",
                    ["2x2", "3x3", "4x4", "5x5"],
                    value=AdminState.network_structure,
                    on_change=AdminState.set_network_structure
                ),
                admin_input(
                    "Profundidad (niveles, máx. 5)",
                    placeholder="3",
                    value=AdminState.network_depth,
                    on_change=AdminState.set_network_depth,
                    input_type="number"
                ),
                columns=2
            ),

            rx.box(height="1rem"),

            rx.box(
                rx.text(
                    "⚠️ Estructura 3x3 con 3 niveles = 3 + 9 + 27 = 39 usuarios",
                    font_size="0.875rem",
                    color=COLORS["gray_600"]
                ),
                background=f"{COLORS['warning']}10",
                padding="0.75rem",
                border_radius="0.5rem",
                margin_bottom="1rem"
            ),

            admin_button(
                "Crear Red Descendente",
                on_click=AdminState.create_network_tree,
                disabled=AdminState.is_loading,
                width="100%"
            )
        ),

        spacing="6",
        width="100%"
    )


# ===================== TAB 5: WALLET =====================

def tab_wallet() -> rx.Component:
    """Tab para agregar dinero a billetera"""
    return rx.vstack(
        admin_section_header(
            "Agregar Dinero a Billetera",
            "Añade saldo a la billetera virtual de uno o más usuarios"
        ),

        admin_card(
            "Configuración de Depósito",

            admin_input(
                "Member IDs (separados por coma)",
                placeholder="1, 2, 3",
                value=AdminState.wallet_member_ids,
                on_change=AdminState.set_wallet_member_ids
            ),

            admin_divider(),

            admin_form_group(
                admin_input(
                    "Monto a Agregar",
                    placeholder="1000.00",
                    value=AdminState.wallet_amount,
                    on_change=AdminState.set_wallet_amount,
                    input_type="number"
                ),
                admin_select(
                    "Moneda",
                    ["MXN", "USD", "COP"],
                    value=AdminState.wallet_currency,
                    on_change=AdminState.set_wallet_currency
                ),
                columns=2
            ),

            rx.box(height="1rem"),

            rx.box(
                rx.text(
                    "ℹ️ El sistema convertirá automáticamente a la moneda del país de cada usuario",
                    font_size="0.875rem",
                    color=COLORS["gray_600"]
                ),
                background=f"{COLORS['info']}10",
                padding="0.75rem",
                border_radius="0.5rem",
                margin_bottom="1rem"
            ),

            admin_button(
                "Agregar Dinero",
                on_click=AdminState.add_money_to_wallet,
                disabled=AdminState.is_loading,
                width="100%"
            )
        ),

        spacing="6",
        width="100%"
    )


# ===================== TAB 6: LEALTAD =====================

def tab_loyalty() -> rx.Component:
    """Tab para agregar puntos de lealtad"""
    return rx.vstack(
        admin_section_header(
            "Agregar Puntos de Lealtad",
            "Asigna puntos de lealtad a un usuario específico"
        ),

        admin_card(
            "Configuración de Puntos",

            admin_input(
                "Member ID",
                placeholder="1",
                value=AdminState.loyalty_member_id,
                on_change=AdminState.set_loyalty_member_id,
                input_type="number"
            ),

            admin_divider(),

            admin_input(
                "Puntos a Agregar (máx. 100)",
                placeholder="25",
                value=AdminState.loyalty_points,
                on_change=AdminState.set_loyalty_points,
                input_type="number"
            ),

            rx.box(height="1rem"),

            rx.box(
                rx.text(
                    "ℹ️ El máximo de puntos de lealtad es 100",
                    font_size="0.875rem",
                    color=COLORS["gray_600"]
                ),
                background=f"{COLORS['info']}10",
                padding="0.75rem",
                border_radius="0.5rem",
                margin_bottom="1rem"
            ),

            admin_button(
                "Agregar Puntos",
                on_click=AdminState.add_loyalty_points,
                disabled=AdminState.is_loading,
                width="100%"
            )
        ),

        spacing="6",
        width="100%"
    )


# ===================== PÁGINA PRINCIPAL =====================

def admin_page() -> rx.Component:
    """Página principal de Admin App - Diseño refinado"""
    return rx.box(
        admin_header(),

        rx.box(
            rx.container(
                admin_alert_banner(),

                # Tabs con diseño mejorado
                rx.tabs.root(
                    rx.box(
                        rx.tabs.list(
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.text("👤", font_size="1.25rem"),
                                    rx.text("Crear Cuenta", font_weight="600"),
                                    spacing="2",
                                    align="center",
                                ),
                                value="create_account",
                                padding="0.875rem 1.5rem",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.text("👥", font_size="1.25rem"),
                                    rx.text("Usuarios Test", font_weight="600"),
                                    spacing="2",
                                    align="center",
                                ),
                                value="test_users",
                                padding="0.875rem 1.5rem",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.text("📦", font_size="1.25rem"),
                                    rx.text("Órdenes", font_weight="600"),
                                    spacing="2",
                                    align="center",
                                ),
                                value="create_orders",
                                padding="0.875rem 1.5rem",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.text("🌳", font_size="1.25rem"),
                                    rx.text("Red", font_weight="600"),
                                    spacing="2",
                                    align="center",
                                ),
                                value="network_tree",
                                padding="0.875rem 1.5rem",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.text("💰", font_size="1.25rem"),
                                    rx.text("Wallet", font_weight="600"),
                                    spacing="2",
                                    align="center",
                                ),
                                value="wallet",
                                padding="0.875rem 1.5rem",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.text("🎁", font_size="1.25rem"),
                                    rx.text("Lealtad", font_weight="600"),
                                    spacing="2",
                                    align="center",
                                ),
                                value="loyalty",
                                padding="0.875rem 1.5rem",
                            ),
                            color_scheme="purple",
                            spacing="1",
                        ),
                        background="white",
                        border_radius="1rem",
                        padding="0.5rem",
                        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.05)",
                        margin_bottom="2rem",
                    ),

                    rx.tabs.content(
                        tab_create_account(),
                        value="create_account"
                    ),
                    rx.tabs.content(
                        tab_test_users(),
                        value="test_users"
                    ),
                    rx.tabs.content(
                        tab_create_orders(),
                        value="create_orders"
                    ),
                    rx.tabs.content(
                        tab_network_tree(),
                        value="network_tree"
                    ),
                    rx.tabs.content(
                        tab_wallet(),
                        value="wallet"
                    ),
                    rx.tabs.content(
                        tab_loyalty(),
                        value="loyalty"
                    ),

                    default_value="create_account",
                    variant="line",
                    width="100%",
                ),

                max_width="1280px",
                padding_y="3rem",
                padding_x="2rem",
            ),

            background=COLORS["bg_main"],
            min_height="calc(100vh - 100px)"
        ),

        width="100%",
        min_height="100vh"
    )
