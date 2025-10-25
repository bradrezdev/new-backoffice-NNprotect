"""
Estado y lógica de negocio para Admin App
"""

import reflex as rx
from typing import List, Dict, Any
from datetime import datetime, timezone
import sqlmodel
import random
import asyncio

from database.users import Users, UserStatus
from database.userprofiles import UserProfiles, UserGender
from database.addresses import Addresses
from database.orders import Orders, OrderStatus
from database.order_items import OrderItems
from database.products import Products
from database.periods import Periods
from database.wallet import Wallets, WalletStatus
from database.loyalty_points import LoyaltyPoints
from database.ranks import Ranks
from database.usertreepaths import UserTreePath
from database.users_addresses import UserAddresses
from database.user_rank_history import UserRankHistory

from NNProtect_new_website.mlm_service.wallet_service import WalletService
from NNProtect_new_website.mlm_service.loyalty_service import LoyaltyService
from NNProtect_new_website.mlm_service.exchange_service import ExchangeService
from NNProtect_new_website.mlm_service.genealogy_service import GenealogyService
from NNProtect_new_website.mlm_service.rank_service import RankService


class OrganizationMember(rx.Base):
    """Miembro de la organización"""
    nombre: str
    member_id: int
    pais: str
    pv: int
    pvg: int
    nivel: int
    ciudad: str


class UserAddress(rx.Base):
    """Dirección de usuario"""
    street: str
    city: str
    state: str
    zip_code: str
    country: str


class AdminState(rx.State):
    """Estado principal de Admin App"""

    # ===================== VARIABLES DE ESTADO =====================

    # Mensajes y alertas
    alert_message: str = ""
    alert_variant: str = "info"
    show_alert: bool = False

    # Loading states individuales
    is_loading_create_account: bool = False
    is_loading_test_users: bool = False
    is_loading_orders: bool = False
    is_loading_network: bool = False
    is_loading_wallet: bool = False
    is_loading_loyalty: bool = False

    # ===================== TAB 1: CREAR CUENTA SIN SPONSOR =====================

    # Form fields - Información personal
    new_user_first_name: str = ""
    new_user_last_name: str = ""
    new_user_gender: str = "Masculino"
    new_user_phone: str = ""
    
    # Form fields - Dirección
    new_user_street: str = ""
    new_user_neighborhood: str = ""
    new_user_city: str = ""
    new_user_state: str = ""
    new_user_country: str = "Mexico"
    new_user_zip_code: str = ""
    
    # Form fields - Acceso al sistema
    new_user_username: str = ""
    new_user_email: str = ""
    new_user_password: str = ""
    new_user_password_confirm: str = ""

    # Setters explícitos - Información personal
    def set_new_user_first_name(self, value: str):
        self.new_user_first_name = value

    def set_new_user_last_name(self, value: str):
        self.new_user_last_name = value
    
    def set_new_user_gender(self, value: str):
        self.new_user_gender = value
    
    def set_new_user_phone(self, value: str):
        self.new_user_phone = value
    
    # Setters - Dirección
    def set_new_user_street(self, value: str):
        self.new_user_street = value
    
    def set_new_user_neighborhood(self, value: str):
        self.new_user_neighborhood = value
    
    def set_new_user_city(self, value: str):
        self.new_user_city = value
    
    def set_new_user_state(self, value: str):
        self.new_user_state = value

    def set_new_user_country(self, value: str):
        self.new_user_country = value
    
    def set_new_user_zip_code(self, value: str):
        self.new_user_zip_code = value
    
    # Setters - Acceso al sistema
    def set_new_user_username(self, value: str):
        self.new_user_username = value

    def set_new_user_email(self, value: str):
        self.new_user_email = value

    def set_new_user_password(self, value: str):
        self.new_user_password = value
    
    def set_new_user_password_confirm(self, value: str):
        self.new_user_password_confirm = value

    # ===================== TAB 2: BUSCAR USUARIO =====================
    
    search_user_query: str = ""
    search_user_organization: list[OrganizationMember] = []
    is_loading_search: bool = False
    is_updating_user: bool = False
    has_result: bool = False
    
    # Campos del usuario (todos los solicitados)
    result_user_id: int = 0
    result_member_id: str = ""
    result_first_name: str = ""
    result_last_name: str = ""
    result_email: str = ""
    result_gender: str = ""
    result_phone: str = ""
    result_date_of_birth: str = ""
    result_status: str = ""
    result_sponsor_id: str = ""
    result_ancestor_id: str = ""
    result_referral_link: str = ""
    result_country: str = ""
    result_pv: str = ""
    result_pvg: str = ""
    result_current_rank: str = ""
    result_highest_rank: str = ""
    result_wallet_balance: str = ""
    result_addresses: list[UserAddress] = []  # Lista de direcciones
    result_fecha_registro: str = ""
    
    # Setters para campos EDITABLES según especificación
    def set_search_user_query(self, value: str):
        self.search_user_query = value
    
    def set_result_first_name(self, value: str):
        self.result_first_name = value
    
    def set_result_last_name(self, value: str):
        self.result_last_name = value
    
    def set_result_sponsor_id(self, value: str):
        self.result_sponsor_id = value
    
    def set_result_ancestor_id(self, value: str):
        self.result_ancestor_id = value
    
    def set_result_country(self, value: str):
        self.result_country = value
    
    def set_result_phone(self, value: str):
        self.result_phone = value
    
    def set_result_date_of_birth(self, value: str):
        self.result_date_of_birth = value
    
    def set_result_wallet_balance(self, value: str):
        self.result_wallet_balance = value
    
    @rx.event
    def search_user(self):
        """Busca un usuario por member_id o email y obtiene TODA su información"""
        self.is_loading_search = True
        self.has_result = False
        self.search_user_organization = []
        
        try:
            query = self.search_user_query.strip()
            if not query:
                self.show_error("Ingresa un Member ID o Email para buscar")
                return
            
            with rx.session() as session:
                # Buscar por member_id o email
                user = None
                if query.isdigit():
                    # Buscar por member_id
                    user = session.exec(
                        sqlmodel.select(Users).where(Users.member_id == int(query))
                    ).first()
                else:
                    # Buscar por email
                    user = session.exec(
                        sqlmodel.select(Users).where(Users.email_cache == query)
                    ).first()
                
                if not user:
                    self.show_error(f"Usuario no encontrado")
                    return
                
                # Obtener UserProfile
                profile = session.exec(
                    sqlmodel.select(UserProfiles).where(UserProfiles.user_id == user.id)
                ).first()
                
                # Obtener TODAS las direcciones del usuario
                user_addresses_relations = session.exec(
                    sqlmodel.select(UserAddresses).where(UserAddresses.user_id == user.id)
                ).all()
                
                addresses_list = []
                primary_address = None
                for ua in user_addresses_relations:
                    addr = session.exec(
                        sqlmodel.select(Addresses).where(Addresses.id == ua.address_id)
                    ).first()
                    if addr:
                        addresses_list.append(UserAddress(
                            street=addr.street,
                            city=addr.city,
                            state=addr.state,
                            zip_code=addr.zip_code,
                            country=addr.country
                        ))
                        if not primary_address:
                            primary_address = addr
                
                # Obtener Wallet
                wallet = session.exec(
                    sqlmodel.select(Wallets).where(Wallets.member_id == user.member_id)
                ).first()
                
                # Calcular PV y PVG del usuario
                orders = session.exec(
                    sqlmodel.select(Orders)
                    .where(Orders.member_id == user.member_id)
                    .where(Orders.status == "PAYMENT_CONFIRMED")
                ).all()
                
                pv_total = sum(order.total_pv or 0 for order in orders)
                
                # Calcular PVG (suma de PV de toda su organización)
                pvg_total = pv_total  # Iniciar con su propio PV
                organization = session.exec(
                    sqlmodel.select(Users).where(Users.sponsor_id == user.member_id)
                ).all()
                
                for member in organization:
                    member_orders = session.exec(
                        sqlmodel.select(Orders)
                        .where(Orders.member_id == member.member_id)
                        .where(Orders.status == "PAYMENT_CONFIRMED")
                    ).all()
                    pvg_total += sum(order.total_pv or 0 for order in member_orders)
                
                # Obtener ancestor_id del UserTreePath
                tree_path = session.exec(
                    sqlmodel.select(UserTreePath)
                    .where(UserTreePath.descendant_id == user.member_id)
                    .where(UserTreePath.depth == 1)
                ).first()
                
                # Asignar TODOS los campos solicitados
                self.result_user_id = user.id if user.id else 0
                self.result_member_id = str(user.member_id)
                self.result_first_name = user.first_name
                self.result_last_name = user.last_name
                self.result_email = user.email_cache or "N/A"
                self.result_gender = profile.gender.value if profile and profile.gender else "N/A"
                self.result_phone = profile.phone_number if profile else "N/A"
                self.result_date_of_birth = profile.date_of_birth.strftime("%Y-%m-%d") if profile and profile.date_of_birth else "N/A"
                self.result_status = user.status.value if hasattr(user.status, 'value') else str(user.status)
                self.result_sponsor_id = str(user.sponsor_id) if user.sponsor_id else "N/A"
                self.result_ancestor_id = str(tree_path.ancestor_id) if tree_path else "N/A"
                self.result_referral_link = user.referral_link or "N/A"
                self.result_country = primary_address.country if primary_address else user.country_cache or "N/A"
                self.result_pv = f"{pv_total:.2f}"
                self.result_pvg = f"{pvg_total:.2f}"
                self.result_current_rank = user.status.value if hasattr(user.status, 'value') else "N/A"
                self.result_highest_rank = user.status.value if hasattr(user.status, 'value') else "N/A"  # TODO: implementar highest_rank
                self.result_wallet_balance = f"{wallet.balance:.2f}" if wallet else "0.00"
                self.result_addresses = addresses_list
                self.result_fecha_registro = user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else "N/A"
                
                self.has_result = True
                
                # Construir organización para la tabla
                org_list = []
                for member in organization:
                    member_address = session.exec(
                        sqlmodel.select(UserAddresses).where(UserAddresses.user_id == member.id)
                    ).first()
                    
                    addr = None
                    if member_address:
                        addr = session.exec(
                            sqlmodel.select(Addresses).where(Addresses.id == member_address.address_id)
                        ).first()
                    
                    member_orders = session.exec(
                        sqlmodel.select(Orders)
                        .where(Orders.member_id == member.member_id)
                        .where(Orders.status == "PAYMENT_CONFIRMED")
                    ).all()
                    
                    member_pv = sum(order.total_pv or 0 for order in member_orders)
                    
                    org_list.append(OrganizationMember(
                        nombre=f"{member.first_name} {member.last_name}",
                        member_id=member.member_id,
                        pais=addr.country if addr else "N/A",
                        pv=int(member_pv),
                        pvg=int(member_pv),
                        nivel=1,
                        ciudad=addr.city if addr else "N/A"
                    ))
                
                self.search_user_organization = org_list
                self.show_success(f"Usuario encontrado: {user.first_name} {user.last_name}")
                
        except ValueError:
            self.show_error("El Member ID debe ser un número válido")
        except Exception as e:
            self.show_error(f"Error al buscar usuario: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_search = False
    
    @rx.event
    def update_user(self):
        """Actualiza SOLO los 8 campos editables del usuario"""
        self.is_updating_user = True
        
        try:
            if self.result_user_id == 0:
                self.show_error("No hay usuario seleccionado para actualizar")
                return
            
            with rx.session() as session:
                # Obtener el usuario
                user = session.exec(
                    sqlmodel.select(Users).where(Users.id == self.result_user_id)
                ).first()
                
                if not user:
                    self.show_error("Usuario no encontrado en la base de datos")
                    return
                
                # 1. Actualizar first_name y last_name en Users
                user.first_name = self.result_first_name.strip()
                user.last_name = self.result_last_name.strip()
                
                # 2. Actualizar sponsor_id en Users
                if self.result_sponsor_id != "N/A" and self.result_sponsor_id.strip():
                    try:
                        user.sponsor_id = int(self.result_sponsor_id)
                    except ValueError:
                        self.show_error("Sponsor ID debe ser un número válido")
                        return
                
                # 3. Actualizar country_cache en Users
                if self.result_country != "N/A" and self.result_country.strip():
                    user.country_cache = self.result_country.strip()
                
                # 4. Actualizar phone_number en UserProfiles
                profile = session.exec(
                    sqlmodel.select(UserProfiles).where(UserProfiles.user_id == user.id)
                ).first()
                
                if profile:
                    if self.result_phone != "N/A" and self.result_phone.strip():
                        profile.phone_number = self.result_phone.strip()
                    
                    # 5. Actualizar date_of_birth en UserProfiles
                    if self.result_date_of_birth != "N/A" and self.result_date_of_birth.strip():
                        try:
                            from datetime import datetime
                            profile.date_of_birth = datetime.strptime(self.result_date_of_birth, "%Y-%m-%d").date()
                        except ValueError:
                            self.show_error("Fecha de nacimiento inválida (usar formato YYYY-MM-DD)")
                            return
                    
                    session.add(profile)
                
                # 6. Actualizar wallet_balance en Wallets
                if self.result_wallet_balance != "N/A" and self.result_wallet_balance.strip():
                    try:
                        new_balance = float(self.result_wallet_balance)
                        wallet = session.exec(
                            sqlmodel.select(Wallets).where(Wallets.member_id == user.member_id)
                        ).first()
                        
                        if wallet:
                            wallet.balance = new_balance
                            session.add(wallet)
                        else:
                            self.show_error("Wallet no encontrada para este usuario")
                            return
                    except ValueError:
                        self.show_error("Balance debe ser un número válido")
                        return
                
                # 7. Actualizar ancestor_id en UserTreePath (COMPLEJO - requiere validación)
                # TODO: Implementar actualización de ancestor_id si es necesario
                # Esto puede requerir reconstruir el árbol genealógico
                
                session.add(user)
                session.commit()
                session.refresh(user)
                
                self.show_success(f"Usuario {user.member_id} actualizado correctamente")
                
                # Recargar datos actualizados
                self.search_user()
                
        except Exception as e:
            self.show_error(f"Error al actualizar usuario: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_updating_user = False

    # ===================== TAB 3: CREAR ÓRDENES =====================

    orders_member_ids: str = ""  # Comma separated
    orders_quantity: str = "1"

    def set_orders_member_ids(self, value: str):
        self.orders_member_ids = value

    def set_orders_quantity(self, value: str):
        self.orders_quantity = value

    # ===================== TAB 4: CREAR RED DESCENDENTE =====================

    network_root_member_id: str = "1"
    network_structure: str = "2x2"  # 2x2, 3x3, 4x4, 5x5
    network_depth: str = "3"
    network_country: str = "Al azar"  # México, USA, Colombia, República Dominicana, Al azar
    network_create_orders: bool = True  # Crear órdenes con 5 productos
    
    # Contadores y progress
    network_estimated_users: int = 0  # Usuarios que se crearán
    network_pv_per_order: int = 0  # PV por orden (5 productos)
    network_total_pvg: int = 0  # PVG total para el usuario raíz
    network_progress: int = 0  # Progreso 0-100
    network_current_user: int = 0  # Usuario actual procesando

    def set_network_root_member_id(self, value: str):
        self.network_root_member_id = value
        self._calculate_network_estimates()

    def set_network_structure(self, value: str):
        self.network_structure = value
        self._calculate_network_estimates()

    def set_network_depth(self, value: str):
        self.network_depth = value
        self._calculate_network_estimates()
    
    def set_network_country(self, value: str):
        self.network_country = value
        self._calculate_pv_estimates()
    
    @rx.event
    def set_network_create_orders(self, value: bool):
        self.network_create_orders = value
        self._calculate_pv_estimates()

    # ===================== TAB 5: AGREGAR DINERO A BILLETERA =====================

    wallet_member_ids: str = ""  # Comma separated
    wallet_amount: str = ""
    wallet_currency: str = "MXN"

    def set_wallet_member_ids(self, value: str):
        self.wallet_member_ids = value

    def set_wallet_amount(self, value: str):
        self.wallet_amount = value

    def set_wallet_currency(self, value: str):
        self.wallet_currency = value

    # ===================== TAB 6: AGREGAR PUNTOS DE LEALTAD =====================

    loyalty_member_id: str = ""
    loyalty_points: str = ""

    def set_loyalty_member_id(self, value: str):
        self.loyalty_member_id = value

    def set_loyalty_points(self, value: str):
        self.loyalty_points = value

    # ===================== MÉTODOS DE INICIALIZACIÓN =====================
    
    def on_load(self):
        """Método llamado al cargar el estado (inicializa cálculos)"""
        self._calculate_network_estimates()

    # ===================== MÉTODOS AUXILIARES =====================

    def show_success(self, message: str):
        """Muestra mensaje de éxito"""
        self.alert_message = message
        self.alert_variant = "success"
        self.show_alert = True

    def show_error(self, message: str):
        """Muestra mensaje de error"""
        self.alert_message = message
        self.alert_variant = "error"
        self.show_alert = True

    def show_info(self, message: str):
        """Muestra mensaje informativo"""
        self.alert_message = message
        self.alert_variant = "info"
        self.show_alert = True

    @rx.event
    def hide_alert(self):
        """Oculta la alerta"""
        self.show_alert = False
        self.alert_message = ""

    def _calculate_network_estimates(self):
        """Calcula estimados de usuarios a crear en la red"""
        try:
            depth = int(self.network_depth)
            structure_str = self.network_structure  # "2x2", "3x3", etc.
            structure = int(structure_str[0])  # Extrae el primer número
            
            # Calcular total de usuarios: sum(structure^level for level in 1..depth)
            total_users = sum(structure ** level for level in range(1, depth + 1))
            
            self.network_estimated_users = total_users
            self._calculate_pv_estimates()
            
        except (ValueError, IndexError):
            self.network_estimated_users = 0
            self.network_pv_per_order = 0
            self.network_total_pvg = 0
    
    def _calculate_pv_estimates(self):
        """Calcula estimados de PV por orden y PVG total"""
        try:
            if not self.network_create_orders:
                self.network_pv_per_order = 0
                self.network_total_pvg = 0
                return
            
            # PV de los 5 productos según país
            country = self.network_country
            
            # Productos: Cúrcuma, Dreaming Deep, Chia, Citrus, Jengibre
            # PV por país (basado en la estructura de Products)
            pv_map = {
                "México": [30, 40, 25, 25, 30],  # Total: 150 PV
                "USA": [30, 40, 25, 25, 30],     # Total: 150 PV
                "Colombia": [30, 40, 25, 25, 30], # Total: 150 PV
                "República Dominicana": [30, 40, 25, 25, 30], # Total: 150 PV
            }
            
            if country == "Al azar":
                # Promedio de todos los países
                pv_per_order = 150  # Todos tienen el mismo PV
            else:
                pv_per_order = sum(pv_map.get(country, [30, 40, 25, 25, 30]))
            
            self.network_pv_per_order = pv_per_order
            
            # PVG total = PV por orden × número de usuarios
            self.network_total_pvg = pv_per_order * self.network_estimated_users
            
        except Exception:
            self.network_pv_per_order = 0
            self.network_total_pvg = 0

    def get_next_member_id(self, session) -> int:
        """Obtiene el siguiente member_id disponible"""
        try:
            max_member = session.exec(
                sqlmodel.select(sqlmodel.func.max(Users.member_id))
            ).first()
            return (max_member or 0) + 1
        except Exception:
            return 1

    # ===================== TAB 1: CREAR CUENTA SIN SPONSOR =====================

    @rx.event
    async def create_account_without_sponsor(self):
        """
        Crea una cuenta Master sin sponsor siguiendo el mismo patrón que AuthState.
        ✅ Incluye registro en Supabase Auth y auth_credentials.
        """
        print("\n" + "="*60)
        print("DEBUG: create_account_without_sponsor - INICIO")
        print("="*60)

        self.is_loading_create_account = True
        yield

        try:
            print(f"DEBUG: Validando campos obligatorios...")
            
            # Validaciones básicas
            if not self.new_user_first_name or not self.new_user_last_name:
                print("DEBUG: ERROR - Nombre y apellido requeridos")
                self.show_error("Nombre y apellido son requeridos")
                return

            if not self.new_user_email:
                print("DEBUG: ERROR - Email requerido")
                self.show_error("Email es requerido")
                return
            
            if not self.new_user_username:
                print("DEBUG: ERROR - Usuario requerido")
                self.show_error("Usuario es requerido")
                return
            
            if not self.new_user_password or not self.new_user_password_confirm:
                print("DEBUG: ERROR - Contraseña requerida")
                self.show_error("Contraseña y confirmación son requeridas")
                return
            
            if self.new_user_password != self.new_user_password_confirm:
                print("DEBUG: ERROR - Contraseñas no coinciden")
                self.show_error("Las contraseñas no coinciden")
                return
            
            # Validar campos de dirección
            if not self.new_user_street or not self.new_user_city or not self.new_user_state or not self.new_user_zip_code:
                print("DEBUG: ERROR - Dirección incompleta")
                self.show_error("Todos los campos de dirección son requeridos")
                return

            await asyncio.sleep(0.1)

            # ✅ PASO 1: REGISTRAR EN SUPABASE AUTH (NUEVO - IGUAL QUE auth_state.py)
            display_name = f"{self.new_user_first_name} {self.new_user_last_name}".strip()
            
            print(f"DEBUG: Registrando en Supabase Auth...")
            from ..auth_service.auth_state import SupabaseAuthManager
            
            success, message, supabase_user_id = await SupabaseAuthManager.sign_up_user(
                self.new_user_email, 
                self.new_user_password, 
                display_name,
                self.new_user_first_name, 
                self.new_user_last_name
            )
            
            if not success or not supabase_user_id:
                error_msg = message or "Error al obtener ID de usuario de Supabase"
                print(f"DEBUG: ERROR - {error_msg}")
                self.show_error(error_msg)
                return
            
            print(f"✅ Usuario registrado en Supabase: {supabase_user_id}")

            # ✅ PASO 2: CREAR DATOS MLM (USANDO MLMUserManager COMO auth_state.py)
            print("DEBUG: Creando usuario MLM...")
            from ..mlm_service.mlm_user_manager import MLMUserManager
            
            with rx.session() as session:
                # Usar el mismo método que auth_state.py
                new_user = MLMUserManager.create_mlm_user(
                    session, 
                    supabase_user_id, 
                    self.new_user_first_name,
                    self.new_user_last_name, 
                    self.new_user_email, 
                    None  # sponsor_id = None para cuenta master
                )
                
                # Crear registros relacionados (IGUAL QUE auth_state.py)
                if new_user.id:
                    print(f"DEBUG: Creando registros relacionados para user_id {new_user.id}...")
                    
                    # UserProfile
                    MLMUserManager.create_user_profile(
                        session, new_user.id, self.new_user_phone, self.new_user_gender
                    )
                    
                    # SocialAccounts
                    MLMUserManager.create_social_accounts(session, new_user.id)
                    
                    # Role
                    MLMUserManager.assign_default_role(session, new_user.id)
                    
                    # ✅ AUTH_CREDENTIALS (ESTO FALTABA EN LA VERSION ANTERIOR)
                    MLMUserManager.create_legacy_auth_credentials(session, new_user.id)
                    print(f"✅ auth_credentials creado para user_id {new_user.id}")
                    
                    # Dirección
                    if self.new_user_street and self.new_user_city and self.new_user_country:
                        MLMUserManager.create_user_address(
                            session, new_user.id, self.new_user_street,
                            self.new_user_neighborhood, self.new_user_city, self.new_user_state,
                            self.new_user_country, self.new_user_zip_code
                        )
                        print(f"✅ Dirección creada")
                    
                    # Wallet
                    from ..mlm_service.wallet_service import WalletService
                    from ..mlm_service.exchange_service import ExchangeService
                    currency = ExchangeService.get_country_currency(self.new_user_country)
                    WalletService.create_wallet(session, new_user.member_id, currency)
                    print(f"✅ Wallet creado con moneda {currency}")
                    
                    # Rango inicial
                    from ..mlm_service.rank_service import RankService
                    rank_assigned = RankService.assign_initial_rank(session, new_user.member_id)
                    if rank_assigned:
                        print(f"✅ Rango inicial asignado")
                    
                session.commit()
                print(f"✅ Usuario MLM creado SIN SPONSOR - Member ID: {new_user.member_id}")

                self.show_success(f"✓ Cuenta Master creada - Member ID: {new_user.member_id}")

                # Limpiar formulario
                print("DEBUG: Limpiando formulario...")
                self.new_user_first_name = ""
                self.new_user_last_name = ""
                self.new_user_gender = "Masculino"
                self.new_user_phone = ""
                self.new_user_street = ""
                self.new_user_neighborhood = ""
                self.new_user_city = ""
                self.new_user_state = ""
                self.new_user_country = "Mexico"
                self.new_user_zip_code = ""
                self.new_user_username = ""
                self.new_user_email = ""
                self.new_user_password = ""
                self.new_user_password_confirm = ""

                print("DEBUG: create_account_without_sponsor - ÉXITO")

        except Exception as e:
            print(f"DEBUG: ERROR CRÍTICO - {str(e)}")
            self.show_error(f"Error al crear usuario: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_create_account = False
            print("DEBUG: create_account_without_sponsor - FIN")
            print("="*60 + "\n")

    # ===================== TAB 2: CREAR USUARIOS TESTS =====================

    @rx.event
    def create_test_users(self):
        """Crea múltiples usuarios de prueba"""
        print("\n" + "="*60)
        print("DEBUG: create_test_users - INICIO")
        print("="*60)

        self.is_loading_test_users = True

        try:
            sponsor_id = int(self.test_users_sponsor_id)
            quantity = int(self.test_users_quantity)

            print(f"DEBUG: Parámetros:")
            print(f"  - Sponsor ID: {sponsor_id}")
            print(f"  - Cantidad: {quantity}")
            print(f"  - País: {self.test_users_country}")

            if quantity <= 0 or quantity > 100:
                print("DEBUG: ERROR - Cantidad fuera de rango")
                self.show_error("Cantidad debe estar entre 1 y 100")
                return

            print("DEBUG: Abriendo sesión de base de datos...")
            with rx.session() as session:
                # Verificar que sponsor existe
                print(f"DEBUG: Verificando sponsor {sponsor_id}...")
                sponsor = session.exec(
                    sqlmodel.select(Users).where(Users.member_id == sponsor_id)
                ).first()

                if not sponsor:
                    print(f"DEBUG: ERROR - Sponsor {sponsor_id} no existe")
                    self.show_error(f"Sponsor con member_id {sponsor_id} no existe")
                    return

                print(f"DEBUG: Sponsor encontrado: {sponsor.first_name} {sponsor.last_name}")

                created_count = 0
                currency = ExchangeService.get_country_currency(self.test_users_country)
                print(f"DEBUG: Moneda para {self.test_users_country}: {currency}")

                print(f"DEBUG: Creando {quantity} usuarios...")
                for i in range(quantity):
                    member_id = self.get_next_member_id(session)
                    print(f"DEBUG: Creando usuario {i+1}/{quantity} - Member ID: {member_id}")

                    user = Users(
                        member_id=member_id,
                        first_name=f"Test{member_id}",
                        last_name=f"User{member_id}",
                        email_cache=f"test{member_id}@nnprotect.com",
                        country_cache=self.test_users_country,
                        status=UserStatus.QUALIFIED,
                        sponsor_id=sponsor_id,
                        referral_link=f"https://nnprotect.com/ref/{member_id}",
                        pv_cache=0,
                        pvg_cache=0
                    )

                    session.add(user)
                    session.flush()

                    if user.id is None:
                        raise ValueError(f"User ID cannot be None after flush for member {member_id}")

                    # Crear perfil
                    profile = UserProfiles(
                        user_id=user.id,
                        gender=UserGender.MALE,
                        phone_number=f"+52155{member_id:07d}"  # Generar número de teléfono dummy
                    )
                    session.add(profile)

                    # Crear wallet
                    WalletService.create_wallet(session, member_id, currency)

                    # Crear genealogía en UserTreePath
                    tree_created = GenealogyService.add_member_to_tree(
                        session,
                        new_member_id=member_id,
                        sponsor_id=sponsor.member_id
                    )
                    if not tree_created:
                        print(f"DEBUG: WARNING - No se pudo crear UserTreePath para member_id {member_id}")

                    # Asignar rango inicial
                    rank_assigned = RankService.assign_initial_rank(session, member_id)
                    if not rank_assigned:
                        print(f"DEBUG: WARNING - No se pudo asignar rango inicial a member_id {member_id}")

                    created_count += 1

                session.commit()
                print(f"DEBUG: Transacción confirmada - {created_count} usuarios creados")

                self.show_success(f"✓ {created_count} usuarios de prueba creados con sponsor {sponsor_id}")
                print("DEBUG: create_test_users - ÉXITO")

        except ValueError:
            print("DEBUG: ERROR - Valores numéricos inválidos")
            self.show_error("Valores numéricos inválidos")
        except Exception as e:
            print(f"DEBUG: ERROR CRÍTICO - {str(e)}")
            self.show_error(f"Error al crear usuarios: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_test_users = False
            print("DEBUG: create_test_users - FIN")
            print("="*60 + "\n")

    # ===================== TAB 3: CREAR ÓRDENES =====================

    @rx.event
    def create_orders(self):
        """Crea órdenes con 5 productos de suplementos"""
        print("\n" + "="*60)
        print("DEBUG: create_orders - INICIO")
        print("="*60)

        self.is_loading_orders = True

        try:
            # Parsear member_ids (separados por coma)
            member_ids_str = self.orders_member_ids.strip()
            if not member_ids_str:
                self.show_error("Ingrese al menos un member_id")
                return

            member_ids = [int(mid.strip()) for mid in member_ids_str.split(",")]
            orders_per_user = int(self.orders_quantity)

            print(f"DEBUG: Member IDs: {member_ids}")
            print(f"DEBUG: Órdenes por usuario: {orders_per_user}")

            if orders_per_user <= 0 or orders_per_user > 10:
                self.show_error("Cantidad de órdenes debe estar entre 1 y 10")
                return

            with rx.session() as session:
                # Obtener período actual
                period = session.exec(
                    sqlmodel.select(Periods).order_by(sqlmodel.desc(Periods.id))
                ).first()

                if not period:
                    self.show_error("No existe período activo")
                    return

                # Obtener 5 productos de suplementos
                supplements = session.exec(
                    sqlmodel.select(Products)
                    .where(Products.type == "suplemento")
                    .limit(5)
                ).all()

                if len(supplements) < 5:
                    self.show_error("No hay suficientes suplementos en la BD (se necesitan 5)")
                    return

                total_orders = 0

                for member_id in member_ids:
                    # Verificar que usuario existe
                    user = session.exec(
                        sqlmodel.select(Users).where(Users.member_id == member_id)
                    ).first()

                    if not user:
                        print(f"⚠️  Usuario {member_id} no existe, saltando...")
                        continue

                    # Crear órdenes para este usuario
                    for _ in range(orders_per_user):
                        # Calcular totales
                        subtotal = sum(p.price_mx for p in supplements)
                        total_pv = sum(p.pv_mx for p in supplements)
                        total_vn = sum(p.vn_mx for p in supplements)

                        # Crear orden
                        order = Orders(
                            member_id=member_id,
                            country=user.country_cache or "Mexico",
                            currency="MXN",
                            subtotal=subtotal,
                            shipping_cost=0.0,
                            tax=0.0,
                            discount=0.0,
                            total=subtotal,
                            total_pv=total_pv,
                            total_vn=total_vn,
                            status=OrderStatus.PAYMENT_CONFIRMED.value,
                            period_id=period.id,
                            payment_method="admin_test",
                            payment_confirmed_at=datetime.now(timezone.utc)
                        )

                        session.add(order)
                        session.flush()

                        if order.id is None:
                            raise ValueError(f"Order ID cannot be None after flush for member {member_id}")

                        # Crear order items
                        for product in supplements:
                            if product.id is None:
                                raise ValueError(f"Product ID cannot be None")
                                
                            order_item = OrderItems(
                                order_id=order.id,
                                product_id=product.id,
                                quantity=1,
                                unit_price=product.price_mx,
                                unit_pv=product.pv_mx,
                                unit_vn=product.vn_mx
                            )
                            order_item.calculate_totals()
                            session.add(order_item)

                        total_orders += 1

                session.commit()
                print(f"DEBUG: Transacción confirmada - {total_orders} órdenes creadas")

                self.show_success(f"✓ {total_orders} órdenes creadas exitosamente")
                print("DEBUG: create_orders - ÉXITO")

        except ValueError:
            print("DEBUG: ERROR - Formato inválido de member_ids")
            self.show_error("Formato de member_ids inválido (usar: 1, 2, 3)")
        except Exception as e:
            print(f"DEBUG: ERROR CRÍTICO - {str(e)}")
            self.show_error(f"Error al crear órdenes: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_orders = False
            print("DEBUG: create_orders - FIN")
            print("="*60 + "\n")

    # ===================== TAB 4: CREAR RED DESCENDENTE =====================

    @rx.event
    def create_network_tree(self):
        """Crea una red MLM completa usando algoritmo BFS (Breadth-First Search)"""
        print("\n" + "="*80)
        print("DEBUG: create_network_tree - INICIO")
        print("="*80)

        self.is_loading_network = True

        try:
            # Validar parámetros
            root_member_id = int(self.network_root_member_id)
            depth = int(self.network_depth)
            structure = int(self.network_structure.split("x")[0])  # "2x2" -> 2
            
            print(f"DEBUG: Configuración:")
            print(f"  - Sponsor raíz: member_id={root_member_id}")
            print(f"  - Estructura: {structure}x{structure}")
            print(f"  - Profundidad: {depth} niveles")
            print(f"  - País: {self.network_country}")
            print(f"  - Crear órdenes: {self.network_create_orders}")

            # Validaciones
            if depth <= 0 or depth > 20:
                self.show_error("Profundidad debe estar entre 1 y 20")
                return

            if structure not in [2, 3, 4, 5]:
                self.show_error("Estructura debe ser 2x2, 3x3, 4x4 o 5x5")
                return

            # Calcular usuarios a crear
            total_users = sum(structure ** level for level in range(1, depth + 1))
            
            if total_users > 10000:
                self.show_error(f"Esta configuración crearía {total_users} usuarios. Máximo: 10,000")
                return
            
            print(f"DEBUG: Se crearán aproximadamente {total_users} usuarios")

            with rx.session() as session:
                # Verificar sponsor raíz
                root_user = session.exec(
                    sqlmodel.select(Users).where(Users.member_id == root_member_id)
                ).first()

                if not root_user:
                    self.show_error(f"Usuario root {root_member_id} no existe")
                    return

                print(f"DEBUG: Sponsor raíz encontrado: {root_user.first_name} {root_user.last_name}")

                # Obtener productos si se van a crear órdenes
                products_map = {}
                current_period = None
                
                if self.network_create_orders:
                    print("DEBUG: Cargando productos para órdenes...")
                    required_products = ["Cúrcuma", "Dreaming Deep", "Chia", "Citrus", "Jengibre"]
                    
                    for product_name in required_products:
                        product = session.exec(
                            sqlmodel.select(Products).where(Products.product_name == product_name)
                        ).first()
                        if product:
                            products_map[product_name] = product
                        else:
                            print(f"WARNING: Producto {product_name} no encontrado")
                    
                    # Obtener período actual
                    from NNProtect_new_website.mlm_service.period_service import PeriodService
                    current_period = PeriodService.get_current_period(session)
                    if not current_period:
                        print("WARNING: No hay período actual, creando...")
                        current_period = PeriodService.auto_create_current_month_period(session)
                        session.commit()

                # Obtener próximo member_id
                from sqlmodel import func as sql_func
                max_member_id = session.exec(sqlmodel.select(sql_func.max(Users.member_id))).one()
                next_member_id = (max_member_id or 0) + 1
                print(f"DEBUG: Próximo member_id: {next_member_id}")

                # Obtener rango default
                default_rank = session.exec(
                    sqlmodel.select(Ranks).where(Ranks.name == "Sin rango")
                ).first()
                
                if not default_rank:
                    self.show_error("Rango 'Sin rango' no encontrado en BD")
                    return

                # Crear red usando BFS
                print(f"\nDEBUG: Iniciando creación BFS...")
                created_count = 0
                queue = [(root_member_id, 1)]  # (sponsor_id, nivel)
                
                # Inicializar progreso
                self.network_progress = 0
                self.network_current_user = 0

                while queue and created_count < total_users:
                    sponsor_id, current_level = queue.pop(0)
                    
                    if current_level > depth:
                        continue
                    
                    # Crear N hijos para este sponsor
                    for _ in range(structure):
                        if created_count >= total_users:
                            break
                        
                        new_member_id = next_member_id + created_count
                        
                        # Crear usuario completo
                        new_user = self._create_mlm_user(
                            session=session,
                            member_id=new_member_id,
                            sponsor_id=sponsor_id,
                            level=current_level,
                            country_config=self.network_country,
                            default_rank=default_rank,
                            products_map=products_map if self.network_create_orders else None,
                            current_period=current_period
                        )
                        
                        created_count += 1
                        queue.append((new_member_id, current_level + 1))
                        
                        # Actualizar progreso
                        self.network_current_user = created_count
                        self.network_progress = int((created_count / total_users) * 100)
                        
                        # Commit cada 50 usuarios
                        if created_count % 50 == 0:
                            session.commit()
                            print(f"  [{created_count}/{total_users}] usuarios creados... ({self.network_progress}%)")

                # Commit final
                session.commit()
                
                # Progreso completo
                self.network_progress = 100
                self.network_current_user = created_count
                
                print(f"\n✅ Red completada: {created_count} usuarios creados")
                
                self.show_success(f"✓ Red creada: {created_count} usuarios en {depth} niveles (estructura {structure}x{structure})")

        except ValueError as e:
            print(f"DEBUG: ERROR - Valor inválido: {e}")
            self.show_error(f"Valores inválidos: {str(e)}")
        except Exception as e:
            print(f"DEBUG: ERROR CRÍTICO - {str(e)}")
            self.show_error(f"Error al crear red: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_network = False
            print("DEBUG: create_network_tree - FIN")
            print("="*80 + "\n")
    
    def _create_mlm_user(
        self,
        session,
        member_id: int,
        sponsor_id: int,
        level: int,
        country_config: str,
        default_rank,
        products_map: dict | None = None,
        current_period = None
    ) -> Users:
        """Crea un usuario MLM completo con todos sus datos"""
        from datetime import date
        
        # Determinar país
        if country_config == "Al azar":
            country = random.choice(["México", "USA", "Colombia", "República Dominicana"])
        else:
            country = country_config
        
        # 1. USERS
        first_name = f"Test{member_id}"
        last_name = f"User{level}"
        email = f"test{member_id}@nnprotect.local"
        
        user = Users(
            member_id=member_id,
            sponsor_id=sponsor_id,
            first_name=first_name,
            last_name=last_name,
            email_cache=email,
            country_cache=country,
            status=UserStatus.NO_QUALIFIED,
            pv_cache=0,
            pvg_cache=0,
            created_at=datetime.now(timezone.utc)
        )
        session.add(user)
        session.flush()
        
        # 2. USERPROFILES
        if user.id is None:
            raise ValueError("User ID cannot be None after flush")
            
        profile = UserProfiles(
            user_id=user.id,
            gender=random.choice([UserGender.MALE, UserGender.FEMALE]),
            phone_number=f"+52{random.randint(1000000000, 9999999999)}",
            date_of_birth=date(1990, 1, 1),
            bio=""
        )
        session.add(profile)
        
        # 3. ADDRESSES + USERS_ADDRESSES
        address = Addresses(
            country=country,
            state=f"Estado{level}",
            city=f"Ciudad{member_id}",
            zip_code=f"{random.randint(10000, 99999)}",
            street=f"Calle {random.randint(1, 1000)}",
            neighborhood=f"Colonia{member_id}"
        )
        session.add(address)
        session.flush()
        
        if address.id is None:
            raise ValueError("Address ID cannot be None after flush")
        
        user_address = UserAddresses(
            user_id=user.id,
            address_id=address.id,
            address_name="Casa",
            is_default=True
        )
        session.add(user_address)
        
        # 4. USERTREEPATHS - Copiar árbol del sponsor
        self_path = UserTreePath(
            sponsor_id=sponsor_id,
            ancestor_id=member_id,
            descendant_id=member_id,
            depth=0
        )
        session.add(self_path)
        
        sponsor_ancestors = session.exec(
            sqlmodel.select(UserTreePath).where(UserTreePath.descendant_id == sponsor_id)
        ).all()
        
        for ancestor_path in sponsor_ancestors:
            new_path = UserTreePath(
                sponsor_id=sponsor_id,
                ancestor_id=ancestor_path.ancestor_id,
                descendant_id=member_id,
                depth=ancestor_path.depth + 1
            )
            session.add(new_path)
        
        # 5. WALLETS
        currency = self._get_currency(country)
        wallet = Wallets(
            member_id=member_id,
            balance=0.0,
            currency=currency,
            status=WalletStatus.ACTIVE.value,
            created_at=datetime.now(timezone.utc)
        )
        session.add(wallet)
        
        # 6. USER_RANK_HISTORY
        rank_history = UserRankHistory(
            member_id=member_id,
            rank_id=default_rank.id,
            achieved_on=datetime.now(timezone.utc),
            period_id=current_period.id if current_period else None
        )
        session.add(rank_history)
        
        # 7. ORDERS (si está habilitado)
        if products_map and current_period:
            self._create_mlm_order(session, user, country, products_map, current_period)
        
        return user
    
    def _create_mlm_order(self, session, user: Users, country: str, products_map: dict, current_period):
        """Crea orden con 5 productos"""
        currency = self._get_currency(country)
        
        order = Orders(
            member_id=user.member_id,
            country=country,
            currency=currency,
            subtotal=0.0,
            shipping_cost=100.0,
            tax=0.0,
            discount=0.0,
            total=0.0,
            total_pv=0,
            total_vn=0.0,
            status=OrderStatus.PAYMENT_CONFIRMED.value,
            created_at=datetime.now(timezone.utc),
            payment_confirmed_at=datetime.now(timezone.utc),
            period_id=current_period.id,
            payment_method="wallet"
        )
        session.add(order)
        session.flush()
        
        if order.id is None:
            raise ValueError("Order ID cannot be None after flush")
        
        # Agregar productos
        subtotal = 0.0
        total_pv = 0
        total_vn = 0.0
        
        for product_name, product in products_map.items():
            unit_price = self._get_price(product, country)
            unit_pv = self._get_pv(product, country)
            unit_vn = self._get_vn(product, country)
            
            if product.id is None:
                raise ValueError(f"Product {product_name} ID cannot be None")
            
            order_item = OrderItems(
                order_id=order.id,
                product_id=product.id,
                quantity=1,
                unit_price=unit_price,
                unit_pv=unit_pv,
                unit_vn=unit_vn,
                line_total=unit_price,
                line_pv=unit_pv,
                line_vn=unit_vn
            )
            session.add(order_item)
            
            subtotal += unit_price
            total_pv += unit_pv
            total_vn += unit_vn
        
        order.subtotal = subtotal
        order.total = subtotal + order.shipping_cost
        order.total_pv = total_pv
        order.total_vn = total_vn
    
    def _get_currency(self, country: str) -> str:
        """Retorna moneda según país"""
        mapping = {
            "México": "MXN",
            "USA": "USD",
            "Colombia": "COP",
            "República Dominicana": "DOP"
        }
        return mapping.get(country, "MXN")
    
    def _get_price(self, product: Products, country: str) -> float:
        """Obtiene precio según país"""
        if country == "México":
            return product.price_mx or 0.0
        elif country == "USA":
            return product.price_usa or 0.0
        elif country == "Colombia":
            return product.price_colombia or 0.0
        return product.price_mx or 0.0
    
    def _get_pv(self, product: Products, country: str) -> int:
        """Obtiene PV según país"""
        if country == "México":
            return product.pv_mx or 0
        elif country == "USA":
            return product.pv_usa or 0
        elif country == "Colombia":
            return product.pv_colombia or 0
        return product.pv_mx or 0
    
    def _get_vn(self, product: Products, country: str) -> float:
        """Obtiene VN según país"""
        if country == "México":
            return product.vn_mx or 0.0
        elif country == "USA":
            return product.vn_usa or 0.0
        elif country == "Colombia":
            return product.vn_colombia or 0.0
        return product.vn_mx or 0.0

    def _create_network_level(
        self, session, sponsor_member_id: int, width: int, max_depth: int,
        current_depth: int, country: str, currency: str
    ) -> int:
        """Crea un nivel de la red recursivamente"""
        if current_depth > max_depth:
            return 0

        total_created = 0

        # Obtener el sponsor User para obtener su Users.id
        sponsor_user = session.exec(
            sqlmodel.select(Users).where(Users.member_id == sponsor_member_id)
        ).first()

        if not sponsor_user:
            print(f"DEBUG: ERROR - Sponsor con member_id {sponsor_member_id} no existe")
            return 0

        for i in range(width):
            member_id = self.get_next_member_id(session)
            print(f"DEBUG: Nivel {current_depth}, Usuario {i+1}/{width} - Member ID: {member_id}, Sponsor Member ID: {sponsor_member_id}, Sponsor Users.id: {sponsor_user.id}")

            user = Users(
                member_id=member_id,
                first_name=f"Net{member_id}",
                last_name=f"L{current_depth}",
                email_cache=f"net{member_id}@nnprotect.com",
                country_cache=country,
                status=UserStatus.QUALIFIED,
                sponsor_id=sponsor_user.id,  # Usar Users.id del sponsor
                referral_link=f"https://nnprotect.com/ref/{member_id}",
                pv_cache=0,
                pvg_cache=0
            )

            session.add(user)
            session.flush()
            print(f"DEBUG: Usuario creado - Users.id: {user.id}, Member ID: {member_id}")

            if user.id is None:
                raise ValueError(f"User ID cannot be None after flush for member {member_id}")

            # Crear perfil
            profile = UserProfiles(
                user_id=user.id,
                gender=UserGender.MALE,
                phone_number=f"+52155{member_id:07d}"  # Generar número de teléfono dummy
            )
            session.add(profile)
            session.flush()

            # Crear wallet
            WalletService.create_wallet(session, member_id, currency)

            # Crear genealogía en UserTreePath
            tree_created = GenealogyService.add_member_to_tree(
                session,
                new_member_id=member_id,
                sponsor_id=sponsor_member_id  # Usar member_id del sponsor
            )
            if not tree_created:
                print(f"DEBUG: WARNING - No se pudo crear UserTreePath para member_id {member_id}")

            # Asignar rango inicial
            rank_assigned = RankService.assign_initial_rank(session, member_id)
            if not rank_assigned:
                print(f"DEBUG: WARNING - No se pudo asignar rango inicial a member_id {member_id}")

            # Commit incremental para que foreign keys puedan verificarse en recursión
            session.commit()
            print(f"DEBUG: Commit realizado para member_id {member_id}")

            total_created += 1

            # Recursión: crear descendientes (pasar member_id del nuevo usuario)
            if current_depth < max_depth:
                print(f"DEBUG: Iniciando recursión para descendientes de member_id {member_id}")
                total_created += self._create_network_level(
                    session, member_id, width, max_depth, current_depth + 1, country, currency
                )

        return total_created

    # ===================== TAB 5: AGREGAR DINERO A BILLETERA =====================

    @rx.event
    def add_money_to_wallet(self):
        """Agrega dinero a la billetera de usuarios"""
        print("\n" + "="*60)
        print("DEBUG: add_money_to_wallet - INICIO")
        print("="*60)

        self.is_loading_wallet = True

        try:
            # Parsear member_ids
            member_ids_str = self.wallet_member_ids.strip()
            if not member_ids_str:
                print("DEBUG: ERROR - No se ingresaron member_ids")
                self.show_error("Ingrese al menos un member_id")
                return

            member_ids = [int(mid.strip()) for mid in member_ids_str.split(",")]
            amount = float(self.wallet_amount)

            print(f"DEBUG: Parámetros:")
            print(f"  - Member IDs: {member_ids}")
            print(f"  - Monto: {amount} {self.wallet_currency}")

            if amount <= 0:
                print("DEBUG: ERROR - Monto inválido")
                self.show_error("El monto debe ser mayor a 0")
                return

            with rx.session() as session:
                success_count = 0

                for member_id in member_ids:
                    # Verificar usuario
                    user = session.exec(
                        sqlmodel.select(Users).where(Users.member_id == member_id)
                    ).first()

                    if not user:
                        print(f"⚠️  Usuario {member_id} no existe, saltando...")
                        continue

                    # Obtener o crear wallet
                    wallet = session.exec(
                        sqlmodel.select(Wallets).where(Wallets.member_id == member_id)
                    ).first()

                    if not wallet:
                        currency = ExchangeService.get_country_currency(user.country_cache or "Mexico")
                        WalletService.create_wallet(session, member_id, currency)
                        wallet = session.exec(
                            sqlmodel.select(Wallets).where(Wallets.member_id == member_id)
                        ).first()
                    
                    if not wallet:
                        self.show_error(f"No se pudo crear/obtener wallet para member_id {member_id}")
                        continue

                    # Convertir monto si la moneda es diferente
                    target_currency = wallet.currency
                    converted_amount = amount

                    if self.wallet_currency != target_currency:
                        converted_amount = ExchangeService.convert_amount(
                            session, amount, self.wallet_currency, target_currency
                        )

                    # Crear transacción de ajuste
                    import uuid
                    from database.wallet import WalletTransactions, WalletTransactionType, WalletTransactionStatus

                    balance_before = wallet.balance
                    balance_after = balance_before + converted_amount

                    transaction = WalletTransactions(
                        transaction_uuid=str(uuid.uuid4()),
                        member_id=member_id,
                        transaction_type=WalletTransactionType.ADJUSTMENT_CREDIT.value,
                        status=WalletTransactionStatus.COMPLETED.value,
                        amount=converted_amount,
                        balance_before=balance_before,
                        balance_after=balance_after,
                        currency=target_currency,
                        description=f"Ajuste administrativo - Admin App",
                        completed_at=datetime.now(timezone.utc)
                    )

                    session.add(transaction)

                    # Actualizar balance
                    wallet.balance = balance_after
                    wallet.updated_at = datetime.now(timezone.utc)

                    success_count += 1

                session.commit()
                print(f"DEBUG: Transacción confirmada - Dinero agregado a {success_count} billeteras")

                self.show_success(f"✓ Dinero agregado a {success_count} billeteras")
                print("DEBUG: add_money_to_wallet - ÉXITO")

        except ValueError:
            print("DEBUG: ERROR - Valores numéricos inválidos")
            self.show_error("Valores numéricos inválidos")
        except Exception as e:
            print(f"DEBUG: ERROR CRÍTICO - {str(e)}")
            self.show_error(f"Error al agregar dinero: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_wallet = False
            print("DEBUG: add_money_to_wallet - FIN")
            print("="*60 + "\n")

    # ===================== TAB 6: AGREGAR PUNTOS DE LEALTAD =====================

    @rx.event
    def add_loyalty_points(self):
        """Agrega puntos de lealtad a un usuario"""
        print("\n" + "="*60)
        print("DEBUG: add_loyalty_points - INICIO")
        print("="*60)

        self.is_loading_loyalty = True

        try:
            member_id = int(self.loyalty_member_id)
            points = int(self.loyalty_points)

            print(f"DEBUG: Parámetros:")
            print(f"  - Member ID: {member_id}")
            print(f"  - Puntos: {points}")

            if points <= 0 or points > 100:
                print("DEBUG: ERROR - Puntos fuera de rango")
                self.show_error("Puntos deben estar entre 1 y 100")
                return

            print("DEBUG: Abriendo sesión de base de datos...")
            with rx.session() as session:
                # Verificar usuario
                print(f"DEBUG: Verificando usuario {member_id}...")
                user = session.exec(
                    sqlmodel.select(Users).where(Users.member_id == member_id)
                ).first()

                if not user:
                    print(f"DEBUG: ERROR - Usuario {member_id} no existe")
                    self.show_error(f"Usuario {member_id} no existe")
                    return

                print(f"DEBUG: Usuario encontrado: {user.first_name} {user.last_name}")

                # Obtener o crear registro de lealtad
                print("DEBUG: Obteniendo/creando registro de lealtad...")
                loyalty = LoyaltyService.get_or_create_loyalty_record(session, member_id)

                if not loyalty:
                    print("DEBUG: ERROR - No se pudo obtener registro de lealtad")
                    self.show_error("Error al obtener registro de lealtad")
                    return

                # Añadir puntos
                points_before = loyalty.current_points
                loyalty.current_points = min(100, points_before + points)  # Max 100
                loyalty.consecutive_months = loyalty.current_points // 25  # Calcular meses
                loyalty.updated_at = datetime.now(timezone.utc)

                print(f"DEBUG: Puntos antes: {points_before}, después: {loyalty.current_points}")

                # Crear historial
                from database.loyalty_points import LoyaltyPointsHistory, LoyaltyEventType

                print("DEBUG: Creando registro de historial...")
                period = session.exec(
                    sqlmodel.select(Periods).order_by(sqlmodel.desc(Periods.id))
                ).first()

                if period and period.id is not None:
                    history = LoyaltyPointsHistory(
                        member_id=member_id,
                        period_id=period.id,
                        event_type=LoyaltyEventType.EARNED.value,
                        points_before=points_before,
                        points_after=loyalty.current_points,
                        points_change=points,
                        description="Ajuste administrativo - Admin App"
                    )
                    session.add(history)

                session.commit()
                print("DEBUG: Transacción confirmada")

                self.show_success(f"✓ {points} puntos agregados a usuario {member_id} (Total: {loyalty.current_points})")
                print("DEBUG: add_loyalty_points - ÉXITO")

        except ValueError:
            print("DEBUG: ERROR - Valores numéricos inválidos")
            self.show_error("Valores numéricos inválidos")
        except Exception as e:
            print(f"DEBUG: ERROR CRÍTICO - {str(e)}")
            self.show_error(f"Error al agregar puntos: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_loyalty = False
            print("DEBUG: add_loyalty_points - FIN")
            print("="*60 + "\n")
