"""
Página principal de Admin App con UI minimalista - Diseño mobile mejorado
"""

import reflex as rx
from .admin_state import AdminState
from .components import admin_input, admin_select, admin_button, admin_alert
from .theme import COLORS


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


def section_title(title: str, subtitle: str = "") -> rx.Component:
    """Título de sección consistente"""
    return rx.vstack(
        rx.text(
            title,
            font_weight="700",
            font_size="1.25rem",
            color=COLORS["gray_900"],
        ),
        rx.cond(
            subtitle != "",
            rx.text(
                subtitle,
                font_size="0.9375rem",
                color=COLORS["gray_600"],
            )
        ),
        spacing="1",
        align_items="start",
        width="100%",
        margin_bottom="2rem"
    )


# ===================== TAB 1: CREAR CUENTA =====================

def tab_create_account() -> rx.Component:
    """Tab para crear cuenta sin sponsor"""
    return rx.vstack(
        section_title(
            "Crear Cuenta sin Sponsor",
            "Registra un nuevo usuario sin necesidad de sponsor"
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
            disabled=AdminState.is_loading_create_account,
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
        section_title(
            "Crear Usuarios de Prueba",
            "Genera múltiples usuarios de prueba con un sponsor específico"
        ),

        admin_input(
            "Member ID del Sponsor*",
            placeholder="1",
            value=AdminState.test_users_sponsor_id,
            on_change=AdminState.set_test_users_sponsor_id,
            input_type="number"
        ),
        admin_select(
            "País de Registro*",
            ["Mexico", "USA", "Colombia", "Republica Dominicana"],
            value=AdminState.test_users_country,
            on_change=AdminState.set_test_users_country
        ),
        admin_input(
            "Cantidad de Usuarios* (máx. 100)",
            placeholder="10",
            value=AdminState.test_users_quantity,
            on_change=AdminState.set_test_users_quantity,
            input_type="number"
        ),

        rx.box(height="1rem"),

        admin_button(
            "Crear Usuarios de Prueba",
            on_click=AdminState.create_test_users,
            disabled=AdminState.is_loading_test_users,
            width="100%"
        ),

        spacing="4",
        width="100%",
        max_width="600px",
    )


# ===================== TAB 3: CREAR ÓRDENES =====================

def tab_create_orders() -> rx.Component:
    """Tab para crear órdenes"""
    return rx.vstack(
        section_title(
            "Crear Órdenes",
            "Genera órdenes con 5 productos de suplementos predefinidos"
        ),

        admin_input(
            "Member IDs* (separados por coma)",
            placeholder="1, 2, 3, 4",
            value=AdminState.orders_member_ids,
            on_change=AdminState.set_orders_member_ids
        ),
        admin_input(
            "Cantidad de Órdenes* por Usuario (máx. 10)",
            placeholder="1",
            value=AdminState.orders_quantity,
            on_change=AdminState.set_orders_quantity,
            input_type="number"
        ),

        rx.box(
            rx.text(
                "ℹ️ Cada orden incluirá 5 productos de suplementos",
                font_size="0.875rem",
                color=COLORS["gray_700"]
            ),
            background=COLORS["info_light"],
            padding="0.875rem 1rem",
            border_radius="12px",
            margin_y="1rem",
            border=f"1px solid {COLORS['info']}40"
        ),

        admin_button(
            "Crear Órdenes",
            on_click=AdminState.create_orders,
            disabled=AdminState.is_loading_orders,
            width="100%"
        ),

        spacing="4",
        width="100%",
        max_width="600px",
    )


# ===================== TAB 4: RED DESCENDENTE =====================

def tab_network_tree() -> rx.Component:
    """Tab para crear red descendente"""
    return rx.vstack(
        section_title(
            "Crear Red Descendente",
            "Genera una estructura completa de red binaria o ternaria"
        ),

        admin_input(
            "Member ID Raíz*",
            placeholder="1",
            value=AdminState.network_root_member_id,
            on_change=AdminState.set_network_root_member_id,
            input_type="number"
        ),
        admin_select(
            "Estructura de Red*",
            ["2x2", "3x3", "4x4", "5x5"],
            value=AdminState.network_structure,
            on_change=AdminState.set_network_structure
        ),
        admin_input(
            "Profundidad* (máx. 5 niveles)",
            placeholder="3",
            value=AdminState.network_depth,
            on_change=AdminState.set_network_depth,
            input_type="number"
        ),

        rx.box(
            rx.text(
                "⚠️ Esta operación puede tomar varios segundos según la profundidad",
                font_size="0.875rem",
                color=COLORS["gray_700"]
            ),
            background=COLORS["warning_light"],
            padding="0.875rem 1rem",
            border_radius="12px",
            margin_y="1rem",
            border=f"1px solid {COLORS['warning']}40"
        ),

        admin_button(
            "Crear Red",
            on_click=AdminState.create_network_tree,
            disabled=AdminState.is_loading_network,
            width="100%"
        ),

        spacing="4",
        width="100%",
        max_width="600px",
    )


# ===================== TAB 5: WALLET =====================

def tab_wallet() -> rx.Component:
    """Tab para agregar dinero a wallet"""
    return rx.vstack(
        section_title(
            "Agregar Dinero a Billetera",
            "Añade fondos a las billeteras de uno o varios usuarios"
        ),

        admin_input(
            "Member IDs* (separados por coma)",
            placeholder="1, 2, 3, 4",
            value=AdminState.wallet_member_ids,
            on_change=AdminState.set_wallet_member_ids
        ),
        admin_input(
            "Cantidad*",
            placeholder="1000.00",
            value=AdminState.wallet_amount,
            on_change=AdminState.set_wallet_amount,
            input_type="number"
        ),
        admin_select(
            "Moneda*",
            ["MXN", "USD", "COP", "DOP"],
            value=AdminState.wallet_currency,
            on_change=AdminState.set_wallet_currency
        ),

        rx.box(
            rx.text(
                "ℹ️ El sistema convertirá automáticamente según el país del usuario",
                font_size="0.875rem",
                color=COLORS["gray_700"]
            ),
            background=COLORS["info_light"],
            padding="0.875rem 1rem",
            border_radius="12px",
            margin_y="1rem",
            border=f"1px solid {COLORS['info']}40"
        ),

        admin_button(
            "Agregar Fondos",
            on_click=AdminState.add_money_to_wallet,
            disabled=AdminState.is_loading_wallet,
            width="100%"
        ),

        spacing="4",
        width="100%",
        max_width="600px",
    )


# ===================== TAB 6: LEALTAD =====================

def tab_loyalty() -> rx.Component:
    """Tab para agregar puntos de lealtad"""
    return rx.vstack(
        section_title(
            "Agregar Puntos de Lealtad",
            "Añade puntos al programa de lealtad de un usuario"
        ),

        admin_input(
            "Member ID*",
            placeholder="1",
            value=AdminState.loyalty_member_id,
            on_change=AdminState.set_loyalty_member_id,
            input_type="number"
        ),
        admin_input(
            "Cantidad de Puntos* (máx. 100)",
            placeholder="25",
            value=AdminState.loyalty_points,
            on_change=AdminState.set_loyalty_points,
            input_type="number"
        ),

        rx.box(
            rx.text(
                "ℹ️ El máximo de puntos de lealtad es 100",
                font_size="0.875rem",
                color=COLORS["gray_700"]
            ),
            background=COLORS["info_light"],
            padding="0.875rem 1rem",
            border_radius="12px",
            margin_y="1rem",
            border=f"1px solid {COLORS['info']}40"
        ),

        admin_button(
            "Agregar Puntos",
            on_click=AdminState.add_loyalty_points,
            disabled=AdminState.is_loading_loyalty,
            width="100%"
        ),

        spacing="4",
        width="100%",
        max_width="600px",
    )


# ===================== PÁGINA PRINCIPAL =====================

def admin_page() -> rx.Component:
    """Página principal de Admin App - Diseño mobile optimizado"""
    return rx.box(
        admin_header(),

        rx.box(
            rx.container(
                admin_alert_banner(),

                # Tabs simplificadas
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("👤 Cuenta", value="create_account"),
                        rx.tabs.trigger("👥 Tests", value="test_users"),
                        rx.tabs.trigger("📦 Órdenes", value="create_orders"),
                        rx.tabs.trigger("🌳 Red", value="network_tree"),
                        rx.tabs.trigger("💰 Wallet", value="wallet"),
                        rx.tabs.trigger("🎁 Lealtad", value="loyalty"),
                        color_scheme="purple",
                    ),

                    rx.tabs.content(tab_create_account(), value="create_account"),
                    rx.tabs.content(tab_test_users(), value="test_users"),
                    rx.tabs.content(tab_create_orders(), value="create_orders"),
                    rx.tabs.content(tab_network_tree(), value="network_tree"),
                    rx.tabs.content(tab_wallet(), value="wallet"),
                    rx.tabs.content(tab_loyalty(), value="loyalty"),

                    default_value="create_account",
                    variant="line",
                    width="100%",
                ),

                max_width="1200px",
                padding_y="2rem",
                padding_x="1.5rem",
            ),

            background=COLORS["bg_main"],
            min_height="calc(100vh - 80px)"
        ),

        width="100%",
        min_height="100vh"
    )
