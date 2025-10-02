"""
Estado y lógica de negocio para Admin App
"""

import reflex as rx
from typing import List, Dict, Any
from datetime import datetime, timezone
import sqlmodel

from database.users import Users, UserStatus
from database.userprofiles import UserProfiles, UserGender
from database.addresses import Addresses
from database.orders import Orders, OrderStatus
from database.order_items import OrderItems
from database.products import Products
from database.periods import Periods
from database.wallet import Wallets
from database.loyalty_points import LoyaltyPoints

from NNProtect_new_website.mlm_service.wallet_service import WalletService
from NNProtect_new_website.mlm_service.loyalty_service import LoyaltyService
from NNProtect_new_website.mlm_service.exchange_service import ExchangeService
from NNProtect_new_website.mlm_service.genealogy_service import GenealogyService
from NNProtect_new_website.mlm_service.rank_service import RankService


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

    # Form fields
    new_user_first_name: str = ""
    new_user_last_name: str = ""
    new_user_email: str = ""
    new_user_password: str = ""
    new_user_country: str = "Mexico"
    new_user_gender: str = "male"

    # Setters explícitos
    def set_new_user_first_name(self, value: str):
        self.new_user_first_name = value

    def set_new_user_last_name(self, value: str):
        self.new_user_last_name = value

    def set_new_user_email(self, value: str):
        self.new_user_email = value

    def set_new_user_password(self, value: str):
        self.new_user_password = value

    def set_new_user_country(self, value: str):
        self.new_user_country = value

    def set_new_user_gender(self, value: str):
        self.new_user_gender = value

    # ===================== TAB 2: CREAR USUARIOS TESTS =====================

    test_users_sponsor_id: str = "1"
    test_users_country: str = "Mexico"
    test_users_quantity: str = "10"

    def set_test_users_sponsor_id(self, value: str):
        self.test_users_sponsor_id = value

    def set_test_users_country(self, value: str):
        self.test_users_country = value

    def set_test_users_quantity(self, value: str):
        self.test_users_quantity = value

    # ===================== TAB 3: CREAR ÓRDENES =====================

    orders_member_ids: str = ""  # Comma separated
    orders_quantity: str = "1"

    def set_orders_member_ids(self, value: str):
        self.orders_member_ids = value

    def set_orders_quantity(self, value: str):
        self.orders_quantity = value

    # ===================== TAB 4: CREAR RED DESCENDENTE =====================

    network_root_member_id: str = "1"
    network_structure: str = "3x3"  # 2x2, 3x3, 4x4, 5x5
    network_depth: str = "3"

    def set_network_root_member_id(self, value: str):
        self.network_root_member_id = value

    def set_network_structure(self, value: str):
        self.network_structure = value

    def set_network_depth(self, value: str):
        self.network_depth = value

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

    def hide_alert(self):
        """Oculta la alerta"""
        self.show_alert = False
        self.alert_message = ""

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
    def create_account_without_sponsor(self):
        """Crea una cuenta de usuario sin sponsor"""
        print("\n" + "="*60)
        print("DEBUG: create_account_without_sponsor - INICIO")
        print("="*60)

        self.is_loading_create_account = True

        try:
            print(f"DEBUG: Validando campos...")
            print(f"  - Nombre: {self.new_user_first_name}")
            print(f"  - Apellido: {self.new_user_last_name}")
            print(f"  - Email: {self.new_user_email}")
            print(f"  - País: {self.new_user_country}")
            print(f"  - Género: {self.new_user_gender}")

            # Validaciones
            if not self.new_user_first_name or not self.new_user_last_name:
                print("DEBUG: ERROR - Nombre y apellido son requeridos")
                self.show_error("Nombre y apellido son requeridos")
                return

            if not self.new_user_email:
                print("DEBUG: ERROR - Email es requerido")
                self.show_error("Email es requerido")
                return

            print("DEBUG: Abriendo sesión de base de datos...")
            with rx.session() as session:
                # Verificar si email ya existe
                print(f"DEBUG: Verificando si email {self.new_user_email} ya existe...")
                existing_user = session.exec(
                    sqlmodel.select(Users).where(Users.email_cache == self.new_user_email)
                ).first()

                if existing_user:
                    print(f"DEBUG: ERROR - Email {self.new_user_email} ya registrado")
                    self.show_error(f"El email {self.new_user_email} ya está registrado")
                    return

                # Obtener siguiente member_id
                print("DEBUG: Obteniendo siguiente member_id...")
                member_id = self.get_next_member_id(session)
                print(f"DEBUG: Nuevo member_id: {member_id}")

                # Crear usuario
                print("DEBUG: Creando usuario...")
                new_user = Users(
                    member_id=member_id,
                    first_name=self.new_user_first_name,
                    last_name=self.new_user_last_name,
                    email_cache=self.new_user_email,
                    country_cache=self.new_user_country,
                    status=UserStatus.QUALIFIED,
                    sponsor_id=None,  # Sin sponsor
                    referral_link=f"https://nnprotect.com/ref/{member_id}",
                    pv_cache=0,
                    pvg_cache=0
                )

                session.add(new_user)
                session.flush()
                print(f"DEBUG: Usuario creado con ID: {new_user.id}")

                # Crear perfil
                print("DEBUG: Creando perfil de usuario...")
                profile = UserProfiles(
                    user_id=new_user.id,
                    gender=UserGender.MALE if self.new_user_gender == "male" else UserGender.FEMALE,
                    phone_number=f"+52155{member_id:07d}"  # Generar número de teléfono dummy
                )
                session.add(profile)

                # Crear dirección
                print("DEBUG: Creando dirección...")
                address = Addresses(
                    country=self.new_user_country,
                    state="N/A",
                    city="N/A",
                    street_address="N/A",
                    postal_code="00000"
                )
                session.add(address)
                session.flush()

                # Crear wallet
                print("DEBUG: Creando wallet...")
                currency = ExchangeService.get_country_currency(self.new_user_country)
                print(f"DEBUG: Moneda para {self.new_user_country}: {currency}")
                WalletService.create_wallet(session, member_id, currency)

                # Crear genealogía en UserTreePath
                print("DEBUG: Creando genealogía en UserTreePath...")
                tree_created = GenealogyService.add_member_to_tree(
                    session,
                    new_member_id=member_id,
                    sponsor_id=None  # Sin sponsor
                )
                if tree_created:
                    print(f"DEBUG: UserTreePath creado exitosamente para member_id {member_id}")
                else:
                    print(f"DEBUG: WARNING - No se pudo crear UserTreePath para member_id {member_id}")

                # Asignar rango inicial
                print("DEBUG: Asignando rango inicial...")
                rank_assigned = RankService.assign_initial_rank(session, member_id)
                if rank_assigned:
                    print(f"DEBUG: Rango inicial asignado exitosamente a member_id {member_id}")
                else:
                    print(f"DEBUG: WARNING - No se pudo asignar rango inicial a member_id {member_id}")

                session.commit()
                print("DEBUG: Transacción confirmada exitosamente")

                self.show_success(f"✓ Usuario creado exitosamente - Member ID: {member_id}")

                # Limpiar formulario
                print("DEBUG: Limpiando formulario...")
                self.new_user_first_name = ""
                self.new_user_last_name = ""
                self.new_user_email = ""
                self.new_user_password = ""

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
                    .where(Products.product_type == "supplement")
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
                        subtotal = sum(p.price_mexico for p in supplements)
                        total_pv = sum(p.pv for p in supplements)
                        total_vn = sum(p.vn_mexico for p in supplements)

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

                        # Crear order items
                        for product in supplements:
                            order_item = OrderItems(
                                order_id=order.id,
                                product_id=product.id,
                                quantity=1,
                                unit_price=product.price_mexico,
                                pv_value=product.pv,
                                vn_value=product.vn_mexico
                            )
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
        """Crea una red descendente completa desde un member_id"""
        print("\n" + "="*60)
        print("DEBUG: create_network_tree - INICIO")
        print("="*60)

        self.is_loading_network = True

        try:
            root_member_id = int(self.network_root_member_id)
            depth = int(self.network_depth)
            structure = int(self.network_structure.split("x")[0])  # Ej: "3x3" -> 3

            print(f"DEBUG: Parámetros:")
            print(f"  - Root Member ID: {root_member_id}")
            print(f"  - Profundidad: {depth}")
            print(f"  - Estructura: {structure}x{structure}")

            if depth <= 0 or depth > 5:
                print("DEBUG: ERROR - Profundidad fuera de rango")
                self.show_error("Profundidad debe estar entre 1 y 5")
                return

            if structure not in [2, 3, 4, 5]:
                print("DEBUG: ERROR - Estructura inválida")
                self.show_error("Estructura debe ser 2x2, 3x3, 4x4 o 5x5")
                return

            print("DEBUG: Abriendo sesión de base de datos...")
            with rx.session() as session:
                # Verificar que root existe
                print(f"DEBUG: Verificando usuario root {root_member_id}...")
                root = session.exec(
                    sqlmodel.select(Users).where(Users.member_id == root_member_id)
                ).first()

                if not root:
                    print(f"DEBUG: ERROR - Root {root_member_id} no existe")
                    self.show_error(f"Usuario root {root_member_id} no existe")
                    return

                print(f"DEBUG: Root encontrado: {root.first_name} {root.last_name}")
                country = root.country_cache or "Mexico"
                currency = ExchangeService.get_country_currency(country)
                print(f"DEBUG: País: {country}, Moneda: {currency}")

                # Crear red recursivamente
                print(f"DEBUG: Iniciando creación recursiva de red...")
                total_created = self._create_network_level(
                    session, root_member_id, structure, depth, 1, country, currency
                )

                # No necesitamos commit aquí porque se hacen commits incrementales en cada usuario
                print(f"DEBUG: Creación completa - {total_created} usuarios creados")

                self.show_success(f"✓ Red creada: {total_created} usuarios en {depth} niveles")
                print("DEBUG: create_network_tree - ÉXITO")

        except ValueError:
            print("DEBUG: ERROR - Valores numéricos inválidos")
            self.show_error("Valores numéricos inválidos")
        except Exception as e:
            print(f"DEBUG: ERROR CRÍTICO - {str(e)}")
            self.show_error(f"Error al crear red: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_network = False
            print("DEBUG: create_network_tree - FIN")
            print("="*60 + "\n")

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

                if period:
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
