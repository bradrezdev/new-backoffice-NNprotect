"""
State para gestión de órdenes del usuario.
Implementa filtrado, búsqueda, ordenamiento y paginación de órdenes.
"""

import reflex as rx
from typing import List, Dict, Optional, Any
from sqlmodel import select, and_, or_, desc, asc, func
from datetime import datetime, timezone
from decimal import Decimal

# Database models
from database.orders import Orders, OrderStatus
from database.order_items import OrderItems
from database.products import Products
from database.users import Users
from database.addresses import Addresses
from database.users_addresses import UserAddresses

# Timezone utilities
from ..utils.timezone_mx import format_mexico_date, convert_to_mexico_time


class OrderState(rx.State):
    """State para gestión de órdenes del usuario"""

    # ============================================================================
    # VARIABLES DE ESTADO
    # ============================================================================

    # Datos de órdenes
    all_orders: List[Dict[str, Any]] = []

    # Filtros y búsqueda
    search_query: str = ""
    status_filter: str = "Todas"
    sort_by: str = "Más reciente"

    # Paginación
    current_page: int = 1
    items_per_page: int = 10

    # Estado de carga
    is_loading: bool = False
    error_message: str = ""

    # ============================================================================
    # COMPUTED VARS - FILTRADO Y ORDENAMIENTO
    # ============================================================================

    @rx.var
    def filtered_orders(self) -> List[Dict[str, Any]]:
        """
        Retorna órdenes filtradas, buscadas, ordenadas y paginadas.
        Este es el array principal que consume el UI.
        """
        if not self.all_orders:
            return []

        orders = self.all_orders.copy()

        # 1. Filtrar por búsqueda (buscar en order_number)
        if self.search_query.strip():
            query_lower = self.search_query.lower().strip()
            orders = [
                order for order in orders
                if query_lower in str(order.get('order_number', '')).lower()
            ]

        # 2. Filtrar por estado
        if self.status_filter != "Todas":
            orders = [
                order for order in orders
                if order.get('status', '').lower() == self.status_filter.lower()
            ]

        # 3. Ordenar
        if self.sort_by == "Más reciente":
            # Ordenar por fecha descendente (más reciente primero)
            orders.sort(
                key=lambda x: self._parse_date_for_sorting(x.get('purchase_date', '')),
                reverse=True
            )
        elif self.sort_by == "Más antiguo":
            # Ordenar por fecha ascendente
            orders.sort(
                key=lambda x: self._parse_date_for_sorting(x.get('purchase_date', '')),
                reverse=False
            )
        elif self.sort_by == "Mayor monto":
            # Ordenar por total descendente
            orders.sort(
                key=lambda x: self._parse_amount_for_sorting(x.get('total', '$0')),
                reverse=True
            )
        elif self.sort_by == "Menor monto":
            # Ordenar por total ascendente
            orders.sort(
                key=lambda x: self._parse_amount_for_sorting(x.get('total', '$0')),
                reverse=False
            )

        # 4. Paginación (retornar solo los items de la página actual)
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page

        return orders[start_idx:end_idx]

    @rx.var
    def total_orders(self) -> int:
        """Total de órdenes después de aplicar filtros (antes de paginar)"""
        if not self.all_orders:
            return 0

        orders = self.all_orders.copy()

        # Aplicar búsqueda
        if self.search_query.strip():
            query_lower = self.search_query.lower().strip()
            orders = [
                order for order in orders
                if query_lower in str(order.get('order_number', '')).lower()
            ]

        # Aplicar filtro de estado
        if self.status_filter != "Todas":
            orders = [
                order for order in orders
                if order.get('status', '').lower() == self.status_filter.lower()
            ]

        return len(orders)

    @rx.var
    def total_pages(self) -> int:
        """Total de páginas basado en el total filtrado"""
        if self.total_orders == 0:
            return 1
        return (self.total_orders + self.items_per_page - 1) // self.items_per_page

    @rx.var
    def current_page_start(self) -> int:
        """Índice inicial de la página actual (1-indexed para mostrar)"""
        if self.total_orders == 0:
            return 0
        return (self.current_page - 1) * self.items_per_page + 1

    @rx.var
    def current_page_end(self) -> int:
        """Índice final de la página actual"""
        if self.total_orders == 0:
            return 0
        end = self.current_page * self.items_per_page
        return min(end, self.total_orders)

    @rx.var
    def is_first_page(self) -> bool:
        """Indica si estamos en la primera página"""
        return self.current_page <= 1

    @rx.var
    def is_last_page(self) -> bool:
        """Indica si estamos en la última página"""
        return self.current_page >= self.total_pages

    @rx.var
    def has_orders(self) -> bool:
        """Indica si el usuario tiene órdenes"""
        return len(self.all_orders) > 0

    # ============================================================================
    # MÉTODOS HELPER PRIVADOS
    # ============================================================================

    def _parse_date_for_sorting(self, date_str: str) -> datetime:
        """
        Convierte fecha en formato DD/MM/YYYY a datetime para ordenamiento.
        Retorna fecha mínima si hay error.
        """
        try:
            if not date_str:
                return datetime.min
            # Formato esperado: "10/09/2025" (DD/MM/YYYY)
            return datetime.strptime(date_str, "%d/%m/%Y")
        except Exception:
            return datetime.min

    def _parse_amount_for_sorting(self, amount_str: str) -> float:
        """
        Convierte monto en formato "$1,746.50" a float para ordenamiento.
        Retorna 0.0 si hay error.
        """
        try:
            if not amount_str:
                return 0.0
            # Remover símbolo de moneda y comas
            clean_amount = amount_str.replace('$', '').replace(',', '').strip()
            return float(clean_amount)
        except Exception:
            return 0.0

    def _format_currency(self, amount: float, currency: str = "MXN") -> str:
        """
        Formatea un monto como moneda con símbolo.
        Ej: 1746.50 -> "$1,746.50"
        """
        try:
            # Símbolos de moneda
            symbols = {
                "MXN": "$",
                "USD": "$",
                "COP": "$"
            }
            symbol = symbols.get(currency, "$")

            # Formatear con comas y 2 decimales
            formatted = f"{amount:,.2f}"
            return f"{symbol}{formatted}"
        except Exception:
            return "$0.00"

    def _map_order_status_to_display(self, db_status: str) -> str:
        """
        Mapea el estado de la base de datos al texto para mostrar en UI.

        DB Status -> UI Display
        - draft -> Pendiente
        - pending_payment -> Pendiente
        - payment_confirmed -> En proceso
        - processing -> En proceso
        - shipped -> Enviado
        - delivered -> Entregado
        - cancelled -> Cancelado
        - refunded -> Cancelado
        """
        status_map = {
            OrderStatus.DRAFT.value: "Pendiente",
            OrderStatus.PENDING_PAYMENT.value: "Pendiente",
            OrderStatus.PAYMENT_CONFIRMED.value: "En proceso",
            OrderStatus.PROCESSING.value: "En proceso",
            OrderStatus.SHIPPED.value: "Enviado",
            OrderStatus.DELIVERED.value: "Entregado",
            OrderStatus.CANCELLED.value: "Cancelado",
            OrderStatus.REFUNDED.value: "Cancelado"
        }
        return status_map.get(db_status, "Pendiente")

    def _map_status_to_shipping_status(self, db_status: str) -> str:
        """
        Mapea el estado de la orden al estado de envío para mobile.
        """
        shipping_map = {
            OrderStatus.DRAFT.value: "Pendiente",
            OrderStatus.PENDING_PAYMENT.value: "Pendiente",
            OrderStatus.PAYMENT_CONFIRMED.value: "Procesando",
            OrderStatus.PROCESSING.value: "Preparando",
            OrderStatus.SHIPPED.value: "En camino",
            OrderStatus.DELIVERED.value: "Entregado",
            OrderStatus.CANCELLED.value: "Cancelado",
            OrderStatus.REFUNDED.value: "Cancelado"
        }
        return shipping_map.get(db_status, "Pendiente")

    def _map_status_to_payment_status(self, db_status: str) -> str:
        """
        Mapea el estado de la orden al estado de pago para mobile.
        """
        if db_status in [OrderStatus.DRAFT.value, OrderStatus.PENDING_PAYMENT.value]:
            return "Pendiente"
        elif db_status == OrderStatus.REFUNDED.value:
            return "Reembolsado"
        else:
            return "Pagado"

    async def _get_user_member_id(self) -> Optional[int]:
        """
        Obtiene el member_id del usuario logueado desde AuthState.
        Retorna None si no está logueado.
        """
        try:
            # Importar AuthState dinámicamente para evitar circular imports
            from ..auth_service.auth_state import AuthState

            # Obtener la instancia del AuthState (parent state) - AWAIT para async
            auth_state = await self.get_state(AuthState)

            if not auth_state.is_logged_in:
                print("⚠️ Usuario no está logueado")
                return None

            # Obtener member_id desde logged_user_data
            member_id = auth_state.logged_user_data.get("member_id")

            if not member_id:
                print("⚠️ No se encontró member_id en logged_user_data")
                return None

            print(f"✅ Usuario logueado con member_id: {member_id}")
            return int(member_id)

        except Exception as e:
            print(f"❌ Error obteniendo member_id del usuario: {e}")
            import traceback
            traceback.print_exc()
            return None

    # ============================================================================
    # EVENT HANDLERS - CARGA DE DATOS
    # ============================================================================

    async def load_orders(self):
        """
        Carga todas las órdenes del usuario desde la base de datos.
        Ejecuta query con JOINs para obtener todos los datos necesarios.
        """
        try:
            self.is_loading = True
            self.error_message = ""

            # 1. Obtener member_id del usuario logueado (AWAIT porque es async)
            member_id = await self._get_user_member_id()

            if not member_id:
                self.error_message = "Usuario no autenticado"
                self.is_loading = False
                return

            print(f"🔍 Cargando órdenes para member_id: {member_id}")

            # 2. Query a la base de datos
            with rx.session() as session:
                # Query principal: obtener órdenes del usuario
                # Solo órdenes que NO están en estado DRAFT (carritos)
                orders_query = select(Orders).where(
                    and_(
                        Orders.member_id == member_id,
                        Orders.status != OrderStatus.DRAFT.value
                    )
                ).order_by(desc(Orders.payment_confirmed_at))

                db_orders = session.exec(orders_query).all()

                if not db_orders:
                    print(f"ℹ️ No se encontraron órdenes para member_id: {member_id}")
                    self.all_orders = []
                    self.is_loading = False
                    return

                print(f"✅ Se encontraron {len(db_orders)} órdenes")

                # 3. Formatear cada orden
                formatted_orders = []

                for order in db_orders:
                    try:
                        formatted_order = self._format_order_for_ui(order, session)
                        if formatted_order:
                            formatted_orders.append(formatted_order)
                    except Exception as e:
                        print(f"⚠️ Error formateando orden {order.id}: {e}")
                        import traceback
                        traceback.print_exc()
                        continue

                # 4. Actualizar estado
                self.all_orders = formatted_orders
                print(f"✅ {len(formatted_orders)} órdenes formateadas correctamente")

        except Exception as e:
            print(f"❌ Error cargando órdenes: {e}")
            import traceback
            traceback.print_exc()
            self.error_message = f"Error cargando órdenes: {str(e)}"

        finally:
            self.is_loading = False

    def _format_order_for_ui(self, order: Orders, session) -> Optional[Dict]:
        """
        Formatea una orden de la base de datos al formato requerido por el UI.

        Args:
            order: Instancia de Orders de la BD
            session: Sesión de base de datos activa

        Returns:
            Diccionario con todos los campos requeridos por el UI
        """
        try:
            # 1. Obtener dirección de envío
            shipping_address_str = "Sin dirección"
            shipping_alias = "Sin alias"

            if order.shipping_address_id:
                address = session.exec(
                    select(Addresses).where(Addresses.id == order.shipping_address_id)
                ).first()

                if address:
                    # Formato: "Calle, Ciudad, Estado"
                    shipping_address_str = f"{address.street}, {address.city}, {address.state}"

                    # Obtener alias de la dirección
                    user_address = session.exec(
                        select(UserAddresses).where(UserAddresses.address_id == address.id)
                    ).first()

                    if user_address and user_address.address_name:
                        shipping_alias = user_address.address_name

            # 2. Formatear fecha de compra
            purchase_date_str = "Sin fecha"
            if order.payment_confirmed_at:
                # Convertir de UTC a México Central
                mexico_dt = convert_to_mexico_time(order.payment_confirmed_at)
                purchase_date_str = format_mexico_date(mexico_dt)

            # 3. Formatear método de pago
            payment_method = order.payment_method or "No especificado"

            # 4. Formatear total
            total_str = self._format_currency(order.total, order.currency)

            # 5. Mapear estado de la orden
            status = self._map_order_status_to_display(order.status)
            shipping_status = self._map_status_to_shipping_status(order.status)
            payment_status = self._map_status_to_payment_status(order.status)

            # 6. Obtener productos de la orden
            products = self._get_order_products(order.id, session)

            # Formatear productos como string para mobile
            products_summary = ", ".join([
                f"{p['name']} (x{p['quantity']})" for p in products
            ]) if products else "Sin productos"

            # 7. Construir diccionario completo
            formatted_order = {
                # Campos para desktop y mobile
                'order_id': str(order.id),  # UUID como string
                'order_number': str(order.id),  # Mostrar el ID como número de orden
                'shipping_address': shipping_address_str,
                'purchase_date': purchase_date_str,
                'payment_method': payment_method,
                'total': total_str,
                'status': status,

                # Campos adicionales para mobile
                'shipping_status': shipping_status,
                'payment_status': payment_status,
                'shipping_alias': shipping_alias,
                'products': products,  # Lista para posible uso futuro
                'products_summary': products_summary  # String formateado para mobile
            }

            return formatted_order

        except Exception as e:
            print(f"❌ Error formateando orden {order.id}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _get_order_products(self, order_id: int, session):
        """
        Obtiene la lista de productos de una orden.

        Args:
            order_id: ID de la orden
            session: Sesión de base de datos activa

        Returns:
            Lista de diccionarios con 'name' y 'quantity'
        """
        try:
            # Query para obtener items de la orden con JOIN a productos
            items_query = select(OrderItems, Products).where(
                OrderItems.order_id == order_id
            ).join(
                Products, OrderItems.product_id == Products.id
            )

            items_with_products = session.exec(items_query).all()

            products = []
            for item, product in items_with_products:
                products.append({
                    'name': product.product_name,
                    'quantity': item.quantity
                })

            return products

        except Exception as e:
            print(f"⚠️ Error obteniendo productos de orden {order_id}: {e}")
            import traceback
            traceback.print_exc()
            return []

    # ============================================================================
    # EVENT HANDLERS - FILTROS Y BÚSQUEDA
    # ============================================================================

    def set_search_query(self, query: str):
        """
        Actualiza el query de búsqueda.
        Resetea a la primera página.
        """
        self.search_query = query
        self.current_page = 1

    def set_status_filter(self, status: str):
        """
        Actualiza el filtro de estado.
        Resetea a la primera página.
        """
        self.status_filter = status
        self.current_page = 1

    def set_sort_by(self, sort: str):
        """
        Actualiza el criterio de ordenamiento.
        No resetea página (mantiene posición).
        """
        self.sort_by = sort

    # ============================================================================
    # EVENT HANDLERS - PAGINACIÓN
    # ============================================================================

    def next_page(self):
        """Avanza a la siguiente página si no estamos en la última"""
        if not self.is_last_page:
            self.current_page += 1

    def prev_page(self):
        """Retrocede a la página anterior si no estamos en la primera"""
        if not self.is_first_page:
            self.current_page -= 1

    def go_to_page(self, page: int):
        """
        Navega a una página específica.

        Args:
            page: Número de página (1-indexed)
        """
        if 1 <= page <= self.total_pages:
            self.current_page = page

    # ============================================================================
    # EVENT HANDLERS - ACCIONES
    # ============================================================================

    def download_pdf(self, order_id: str):
        """
        Genera y descarga el PDF de una orden.
        TODO: Implementar cuando esté disponible el servicio de PDF
        """
        print(f"📄 TODO: Generar PDF para orden {order_id}")
        # Placeholder para funcionalidad futura
        pass
