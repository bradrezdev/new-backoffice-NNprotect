"""Nueva Backoffice NN Protect | Método de pago"""

import reflex as rx
from typing import Optional
from datetime import datetime, timezone
from ..shared_ui.theme import Custom_theme
from rxconfig import config
from ..shared_ui.layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, header

from ..product_service.store_products_state import CountProducts  # Importar estado del carrito
from ..auth_service.auth_state import AuthState  # Importar estado de autenticación

# Importaciones para creación de órdenes y pago
from database.orders import Orders, OrderStatus
from database.order_items import OrderItems
from ..payment_service.payment_service import PaymentService


class PaymentState(rx.State):
    """
    Estado para la gestión del proceso de pago.
    Maneja la selección de método de pago y la confirmación de compra.
    """
    
    # Método de pago seleccionado (wallet, stripe, oxxo)
    payment_method: str = "wallet"
    
    # Estado de procesamiento
    is_processing: bool = False
    
    # CEDIS seleccionado (si aplica)
    selected_cedis_id: Optional[int] = None
    
    # Resultado del proceso de pago
    order_result: Optional[dict] = None
    
    # Mensajes de error
    error_message: str = ""
    success_message: str = ""

    @rx.event
    def select_payment_method(self, method: str):
        """Actualiza el método de pago seleccionado."""
        self.payment_method = method
        self.error_message = ""

    @rx.event
    async def confirm_payment(self):
        """
        Confirma el pago y crea la orden con sus items.
        Flujo:
        1. Validar que hay productos en el carrito
        2. Obtener datos del usuario autenticado
        3. Crear orden con status PENDING_PAYMENT
        4. Crear order_items para cada producto del carrito
        5. Llamar al PaymentService para procesar el pago
        6. Manejar resultado (success/error)
        """
        self.is_processing = True
        self.error_message = ""
        self.success_message = ""
        
        try:
            # Obtener estado del carrito
            cart_state = await self.get_state(CountProducts)
            
            # Validar que hay productos en el carrito
            if not cart_state.cart_items or cart_state.cart_total == 0:
                self.error_message = "El carrito está vacío. Agrega productos antes de confirmar el pago."
                self.is_processing = False
                return
            
            # Obtener datos del usuario
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_logged_in or not auth_state.profile_data:
                self.error_message = "Debes iniciar sesión para realizar una compra."
                self.is_processing = False
                return
            
            # Obtener member_id del usuario
            member_id = auth_state.profile_data.get("member_id")
            country = auth_state.profile_data.get("country", "MX")
            
            if not member_id:
                self.error_message = "No se pudo obtener la información del usuario."
                self.is_processing = False
                return
            
            # Obtener moneda según país
            currency_map = {
                "MX": "MXN",
                "US": "USD",
                "CO": "COP"
            }
            currency = currency_map.get(country, "MXN")
            
            # Calcular totales del carrito
            subtotal = cart_state.cart_subtotal
            shipping_cost = cart_state.cart_shipping_cost
            total_pv = cart_state.cart_volume_points
            total = subtotal + shipping_cost
            
            # Crear orden en la base de datos
            with rx.session() as session:
                # Crear orden con status PENDING_PAYMENT
                new_order = Orders(
                    member_id=member_id,
                    country=country,
                    currency=currency,
                    subtotal=subtotal,
                    shipping_cost=shipping_cost,
                    tax=0.0,
                    discount=0.0,
                    total=total,
                    total_pv=total_pv,
                    total_vn=total,  # VN = total en moneda local
                    status=OrderStatus.PENDING_PAYMENT.value,
                    payment_method=self.payment_method,
                    submitted_at=datetime.now(timezone.utc)
                )
                
                session.add(new_order)
                session.commit()  # Commit para obtener el order_id
                session.refresh(new_order)
                
                # Verificar que se obtuvo el order_id
                if new_order.id is None:
                    self.error_message = "Error al crear la orden en la base de datos."
                    self.is_processing = False
                    return
                
                order_id = new_order.id
                
                # Crear order_items para cada producto del carrito
                cart_items_detailed = cart_state.cart_items_detailed
                
                for cart_item in cart_items_detailed:
                    order_item = OrderItems(
                        order_id=order_id,
                        product_id=cart_item["id"],
                        quantity=cart_item["quantity"],
                        unit_price=cart_item["price"],
                        unit_pv=cart_item["volume_points"],
                        unit_vn=cart_item["price"]  # VN = precio unitario
                    )
                    
                    # Calcular totales de la línea
                    order_item.calculate_totals()
                    
                    session.add(order_item)
                
                session.commit()
                
                # Procesar pago según método seleccionado
                if self.payment_method == "wallet":
                    # Llamar al PaymentService para procesar el pago con wallet
                    payment_result = PaymentService.process_wallet_payment(
                        session=session,
                        order_id=order_id,
                        member_id=member_id
                    )
                    
                    # Manejar resultado
                    if payment_result["success"]:
                        self.success_message = payment_result["message"]
                        self.order_result = payment_result
                        
                        # Limpiar carrito
                        cart_state.clear_cart()
                        
                        # Redirigir a página de confirmación
                        self.is_processing = False
                        return rx.redirect("/order_confirmation")
                    else:
                        self.error_message = payment_result["message"]
                        
                        # Si el pago falló, actualizar el estado de la orden a CANCELLED
                        new_order.status = OrderStatus.CANCELLED.value
                        session.commit()
                        
                else:
                    # Otros métodos de pago (stripe, oxxo) - próximamente
                    self.error_message = f"El método de pago '{self.payment_method}' aún no está disponible."
                    
                    # Cancelar orden
                    new_order.status = OrderStatus.CANCELLED.value
                    session.commit()
        
        except Exception as e:
            self.error_message = f"Error al procesar el pago: {str(e)}"
            print(f"ERROR en confirm_payment: {e}")
        
        finally:
            self.is_processing = False


def payment() -> rx.Component:
    # 📦 EJEMPLO DE REUTILIZACIÓN DE DATOS DEL CARRITO
    # Usando CountProducts podemos acceder a toda la información
    # del carrito desde cualquier página de forma dinámica

    return rx.center(
        # Versión desktop - dejada en blanco según requerimiento
        rx.desktop_only(),

        # Versión móvil - implementación completa
        rx.mobile_only(
            rx.vstack(
                # Header móvil
                mobile_header(),

                # Contenido principal móvil
                rx.vstack(
                    # Título principal
                    rx.text(
                        "Método de pago",
                        size="8",
                        font_weight="bold",
                        text_align="center",
                    ),

                    rx.text(
                        "Selecciona cómo quieres pagar tu pedido",
                        size="2",
                        color="gray",
                        margin_bottom="2em",
                        text_align="center"
                    ),

                    # Opciones de pago disponibles
                    rx.vstack(
                        # Opción 1: Saldo en billetera
                        rx.box(
                            rx.hstack(
                                # Icono de billetera
                                rx.box(
                                    rx.icon("wallet", size=24, color="#059669"),
                                    width="48px",
                                    height="48px",
                                    bg="rgba(5, 150, 105, 0.1)",
                                    border_radius="12px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    margin_right="1em"
                                ),

                                # Información de la billetera
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Saldo en billetera", font_weight="semibold", size="3"),
                                        rx.cond(
                                            PaymentState.payment_method == "wallet",
                                            rx.badge("Seleccionado", color_scheme="green", size="1"),
                                            rx.fragment(),
                                        ),
                                        align="center",
                                        width="100%"
                                    ),

                                    rx.vstack(
                                        rx.text(
                                            f"Saldo actual: ${AuthState.profile_data.get('wallet_balance', 0)} MXN",
                                            size="3",
                                            font_weight="medium",
                                            color="#059669"
                                        ),
                                        rx.text(
                                            "Pago instantáneo",
                                            size="1",
                                            color="gray"
                                        ),
                                        align="start",
                                        spacing="1"
                                    ),

                                    align="start",
                                    spacing="1",
                                    flex="1"
                                ),

                                align="start",
                                width="100%",
                                spacing="0"
                            ),

                            # Radio button indicator
                            rx.box(
                                rx.cond(
                                    PaymentState.payment_method == "wallet",
                                    # Seleccionado
                                    rx.box(
                                        width="12px",
                                        height="12px",
                                        border_radius="15px",
                                        bg="#059669",
                                    ),
                                    # No seleccionado
                                    rx.box(
                                        width="12px",
                                        height="12px",
                                        border_radius="15px",
                                        border="2px solid #d1d5db",
                                        bg="transparent",
                                    ),
                                ),
                            ),

                            # Estilos de la tarjeta
                            border=rx.cond(
                                PaymentState.payment_method == "wallet",
                                "2px solid #059669",
                                "2px solid transparent"
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="29px",
                            padding="1em",
                            #border="2px solid transparent",
                            _hover={"border": "2px solid #059669"},
                            transition="all 0.2s ease",
                            margin_bottom="16px",
                            width="100%",
                            cursor="pointer"
                        ),

                        # Opción 2: Tarjeta de Débito/Crédito
                        rx.box(
                            rx.hstack(
                                # Icono de tarjeta
                                rx.box(
                                    rx.icon("credit-card", size=24, color=Custom_theme().light_colors()["primary"]),
                                    width="48px",
                                    height="48px",
                                    bg=rx.color_mode_cond(
                                        light="rgba(0, 57, 242, 0.1)",
                                        dark="rgba(0, 57, 242, 0.2)"
                                    ),
                                    border_radius="12px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    margin_right="1em"
                                ),

                                # Información de tarjeta
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Tarjeta de Débito/Crédito", font_weight="semibold", size="3"),
                                        align="center",
                                        width="100%"
                                    ),

                                    rx.vstack(
                                        rx.text(
                                            "Visa, Mastercard, American Express",
                                            size="1",
                                            color="gray"
                                        ),
                                        align="start",
                                        spacing="1"
                                    ),

                                    align="start",
                                    spacing="1",
                                    flex="1"
                                ),

                                # Botón de selección (deshabilitado por ahora)
                                rx.box(
                                    rx.box(
                                        width="20px",
                                        height="20px",
                                        border_radius="50%",
                                        border="2px solid #d1d5db",
                                        bg="transparent",
                                        opacity="0.5",
                                        transition="all 0.2s ease"
                                    ),
                                    width="32px",
                                    height="32px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center"
                                ),

                                align="start",
                                width="100%",
                                spacing="0"
                            ),

                            # Estilos de la tarjeta
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="29px",
                            padding="1em",
                            border="2px solid transparent",
                            _hover={"border": "2px solid #d1d5db"},
                            transition="all 0.2s ease",
                            margin_bottom="16px",
                            width="100%",
                            cursor="not-allowed",
                            opacity="0.7"
                        ),

                        # Opción 3: Pago en OXXO
                        rx.box(
                            rx.hstack(
                                # Icono de OXXO
                                rx.box(
                                    rx.box(
                                        rx.text("OXXO", font_size="0.7rem", font_weight="bold", color="#d32f2f"),
                                        width="100%",
                                        height="100%",
                                        display="flex",
                                        align_items="center",
                                        justify_content="center"
                                    ),
                                    width="48px",
                                    height="48px",
                                    bg="rgba(211, 47, 47, 0.1)",
                                    border_radius="12px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    margin_right="1em"
                                ),

                                # Información de OXXO
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Pago en OXXO", font_weight="semibold", size="3"),
                                        align="center",
                                        width="100%"
                                    ),

                                    rx.vstack(
                                        rx.text(
                                            "Paga en cualquier tienda OXXO",
                                            size="1",
                                            color="gray"
                                        ),
                                        align="start",
                                        spacing="1"
                                    ),

                                    align="start",
                                    spacing="1",
                                    flex="1"
                                ),

                                align="start",
                                width="100%",
                                spacing="0"
                            ),

                            # Estilos de la tarjeta
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="29px",
                            padding="1em",
                            border="2px solid transparent",
                            _hover={"border": "2px solid #d32f2f"},
                            transition="all 0.2s ease",
                            margin_bottom="16px",
                            width="100%",
                            cursor="pointer"
                        ),

                        spacing="0",
                        width="100%",
                        margin_bottom="2em"
                    ),

                    # Métodos de pago alternativos
                    rx.vstack(
                        rx.text(
                            "Otros métodos",
                            size="4",
                            font_weight="semibold",
                            margin_bottom="1em",
                            text_align="center"
                        ),

                        # Pago en efectivo
                        rx.box(
                            rx.hstack(
                                rx.box(
                                    rx.icon("dollar-sign", size=24, color="#059669"),
                                    width="48px",
                                    height="48px",
                                    bg="rgba(5, 150, 105, 0.1)",
                                    border_radius="12px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    margin_right="1em"
                                ),

                                rx.vstack(
                                    rx.text("Pago en efectivo", font_weight="semibold", font_size="1rem"),
                                    rx.text(
                                        "Paga al recibir tu pedido",
                                        font_size="0.85rem",
                                        color="gray"
                                    ),
                                    align="start",
                                    spacing="1",
                                    flex="1"
                                ),

                                rx.box(
                                    rx.box(
                                        width="20px",
                                        height="20px",
                                        border_radius="50%",
                                        border="2px solid #059669",
                                        bg="transparent",
                                        _hover={"bg": "#059669"},
                                        transition="all 0.2s ease"
                                    ),
                                    width="32px",
                                    height="32px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center"
                                ),

                                align="start",
                                width="100%",
                                spacing="0"
                            ),

                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="16px",
                            padding="1em",
                            border="2px solid transparent",
                            _hover={"border": "2px solid #059669"},
                            transition="all 0.2s ease",
                            margin_bottom="12px",
                            width="100%",
                            cursor="pointer"
                        ),
                        spacing="0",
                        width="100%",
                        margin_bottom="2em"
                    ),

                    # Espacio para el box flotante
                    rx.box(height="200px"),

                    # Propiedades del vstack principal móvil
                    margin="80px 0 20px 0",
                    width="100%",
                    padding="0 1em",
                ),

                # Box flotante con resumen de pago - copiado de shopping_cart.py
                rx.box(
                    rx.vstack(
                        # Línea divisoria superior
                        rx.box(
                            width="60px",
                            height="4px",
                            bg="rgba(0,0,0,0.2)",
                            border_radius="2px",
                            margin="0 auto 1em auto"
                        ),

                        # Resumen del pedido
                        rx.vstack(
                            # Productos
                            rx.hstack(
                                rx.text(f"Productos ({CountProducts.cart_total})", font_size="0.9rem", color="gray"),
                                rx.spacer(),
                                rx.text(f"${CountProducts.cart_subtotal:.2f}", font_size="0.9rem", font_weight="medium"),
                                width="100%",
                                align="center"
                            ),

                            # Puntos de volumen
                            rx.hstack(
                                rx.text("Puntos de volumen", font_size="0.9rem", color="gray"),
                                rx.spacer(),
                                rx.text(f"{CountProducts.cart_volume_points} pts", font_size="0.9rem", font_weight="medium", color="#f59e0b"),
                                width="100%",
                                align="center"
                            ),

                            # Costo de envío
                            rx.hstack(
                                rx.text("Costo de envío", font_size="0.9rem", color="gray"),
                                rx.spacer(),
                                rx.cond(
                                    CountProducts.cart_shipping_cost == 0,
                                    rx.text("GRATIS", font_size="0.9rem", font_weight="medium", color="#059669"),
                                    rx.text(f"${CountProducts.cart_shipping_cost:.2f}", font_size="0.9rem", font_weight="medium")
                                ),
                                width="100%",
                                align="center"
                            ),

                            # Línea divisoria
                            rx.box(
                                height="1px",
                                bg="rgba(0,0,0,0.1)",
                                width="100%",
                                margin="0.5em 0"
                            ),

                            # Total
                            rx.hstack(
                                rx.text("Total", font_size="1rem", font_weight="bold"),
                                rx.spacer(),
                                rx.text(f"${CountProducts.cart_final_total:.2f}", font_size="1rem", font_weight="bold", color=Custom_theme().light_colors()["primary"]),
                                width="100%",
                                align="center"
                            ),

                            spacing="1",
                            width="100%"
                        ),

                        # Botones de acción
                        rx.vstack(
                            rx.button(
                                rx.cond(
                                    PaymentState.is_processing,
                                    rx.hstack(
                                        rx.spinner(size="3", color="white"),
                                        rx.text("Procesando…", color="white"),
                                        align="center",
                                        justify="center",
                                        spacing="2"
                                    ),
                                    "Confirmar pago"
                                ),
                                on_click=PaymentState.confirm_payment,
                                is_disabled=PaymentState.is_processing,
                                cursor=rx.cond(PaymentState.is_processing, "not-allowed", "pointer"),
                                opacity=rx.cond(PaymentState.is_processing, "0.7", "1"),
                                align="center",
                                bg=Custom_theme().light_colors()["primary"],
                                color="white",
                                size="4",
                                border_radius="15px",
                                padding="16px",
                                width="100%",
                                _hover={"opacity": 0.9, "transform": "translateY(-1px)"},
                                transition="all 0.2s ease",
                            ),
                            spacing="2",
                            width="100%",
                            margin_top="1em"
                        ),
                        spacing="0",
                        width="100%"
                    ),

                    # Estilos del box flotante
                    bg=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["tertiary"],
                        dark=Custom_theme().dark_colors()["tertiary"]
                    ),
                    border_radius="29px 29px 0 0",
                    padding="20px",
                    box_shadow="0 -4px 12px rgba(0, 0, 0, 0.1)",
                    border_top="1px solid rgba(0,0,0,0.05)",
                    position="fixed",
                    bottom="0",
                    left="0",
                    right="0",
                    z_index="100",
                    width="100%",
                    max_width="100vw"
                ),
                width="100%",
            ),
            width="100%",
        ),

        # Propiedades del contenedor principal
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),
        position="absolute",
        width="100%",
    )