"""
NNProtect Database Models
========================

Este módulo define todos los modelos de base de datos para el sistema NNProtect.
Incluye gestión de usuarios, perfiles, autenticación, productos, órdenes, billeteras,
rangos, volúmenes y estructura de enrolamiento (árbol genealógico).

Autor: Desarrollo NN Protect
Fecha: Septiembre 2025
Versión: 1.0

Tecnologías:
- Reflex Framework (SQLModel + SQLAlchemy)
- PostgreSQL (via Supabase)
- Alembic para migraciones

Estructura de tablas implementadas según diagrama ERD:
1. Gestión de Usuarios y Perfiles
2. Sistema de Autenticación
3. Direcciones y Cuentas Sociales
4. Estructura de Enrolamiento (MLM Tree)
5. Sistema de Rangos y Volúmenes
6. Billeteras y Métodos de Pago
7. Productos y Órdenes
8. Retiros y Transferencias
"""

import reflex as rx
from datetime import datetime, date
from typing import Optional, List
from enum import Enum
"""

import reflex as rx
from datetime import datetime, date
from typing import Optional, List
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship

import reflex as rx
from datetime import datetime, date
from typing import Optional, List
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship


# ============================================================================
# ENUMS - Definición de tipos de datos categóricos
# ============================================================================

class UserStatus(Enum):
    """Estados posibles de un usuario en el sistema"""
    PENDING = "pending"      # Usuario registrado pero pendiente de activación
    ACTIVE = "active"        # Usuario activo
    SUSPENDED = "suspended"  # Usuario suspendido
    CANCELLED = "cancelled"  # Usuario cancelado


class OrderStatus(Enum):
    """Estados posibles de una orden"""
    PENDING = "pending"      # Orden creada pero pendiente de pago
    PAID = "paid"            # Orden pagada
    SHIPPED = "shipped"      # Orden enviada
    DELIVERED = "delivered"  # Orden entregada
    CANCELLED = "cancelled"  # Orden cancelada
    REFUNDED = "refunded"    # Orden con reembolso


class WithdrawalStatus(Enum):
    """Estados posibles de un retiro"""
    REQUESTED = "requested"  # Retiro solicitado
    PROCESSING = "processing"  # Retiro en proceso
    PAID = "paid"            # Retiro pagado
    FAILED = "failed"        # Retiro fallido


class AddressType(Enum):
	"""Tipos de dirección para un usuario"""
	BILLING = "billing"			# Dirección de facturación
	SHIPPING = "shipping"		# Dirección de envío
	OTHER = "other"				# Otra dirección


class WalletType(Enum):
	"""Tipos de billetera disponibles"""
	COMMISSIONS = "commissions"	# Billetera de comisiones
	BONUSES = "bonuses"			# Billetera de bonos
	REFUNDS = "refunds"			# Billetera de reembolsos


class PayoutProvider(Enum):
	"""Proveedores de métodos de pago"""
	BANK_TRANSFER = "bank_transfer"	# Transferencia bancaria
	PAYPAL = "paypal"				# PayPal
	CRYPTO = "crypto"				# Criptomonedas
	OTHER = "other"					# Otros métodos


# ============================================================================
# MODELOS DE USUARIOS Y AUTENTICACIÓN
# ============================================================================

class User(SQLModel, table=True):
	"""
	Modelo principal de usuarios del sistema.
	Contiene información básica de identificación y estado del usuario.

	Relaciones:
	- Tiene un perfil (user_profiles)
	- Tiene credenciales de autenticación (auth_credentials)
	- Puede tener múltiples roles (roles)
	- Puede tener múltiples direcciones (user_addresses)
	- Puede tener múltiples cuentas sociales (social_accounts)
	- Forma parte de estructura de enrolamiento (user_tree_paths)
	"""
	__tablename__ = "users"

	# Clave primaria
	id: Optional[int] = Field(default=None, primary_key=True, index=True)

	# Identificadores únicos
	member_id: str = Field(max_length=20, unique=True, index=True)
	username: str = Field(max_length=50, unique=True, index=True)
	email: str = Field(max_length=100, unique=True, index=True)

	# Estado y estructura de red
	status: UserStatus = Field(default=UserStatus.PENDING)
	sponsor_id: Optional[int] = Field(default=None, foreign_key="users.id")
	referral_code: str = Field(max_length=20, unique=True)

	# Timestamps
	created_at: datetime = Field(default_factory=datetime.utcnow)
	updated_at: datetime = Field(default_factory=datetime.utcnow)


class AuthCredential(SQLModel, table=True):
	"""
	Credenciales de autenticación de usuarios.
	Almacena información sensible de autenticación de forma segura.
	"""
	__tablename__ = "auth_credentials"

	# Clave primaria compuesta con user_id
	user_id: int = Field(primary_key=True, foreign_key="users.id")

	# Datos de autenticación
	password_hash: str = Field(max_length=255)
	last_login_at: Optional[datetime] = Field(default=None)


class Role(SQLModel, table=True):
	"""
	Roles asignados a usuarios.
	Permite un sistema de permisos flexible basado en roles.
	"""
	__tablename__ = "roles"

	# Clave primaria
	id: Optional[int] = Field(default=None, primary_key=True, index=True)

	# Información del rol
	role_name: str = Field(max_length=50)
	user_id: int = Field(foreign_key="users.id")


class UserProfile(SQLModel, table=True):
	"""
	Perfiles extendidos de usuarios.
	Contiene información personal y de contacto adicional.
	"""
	__tablename__ = "user_profiles"

	# Clave primaria compuesta con user_id
	user_id: int = Field(primary_key=True, foreign_key="users.id")

	# Información personal
	first_name: str = Field(max_length=100)
	last_name: str = Field(max_length=100)
	phone_number: Optional[str] = Field(default=None, max_length=20)
	photo_url: Optional[str] = Field(default=None, max_length=500)


class SocialAccount(SQLModel, table=True):
	"""
	Cuentas sociales vinculadas a usuarios.
	Permite integración con redes sociales y otros proveedores de identidad.
	"""
	__tablename__ = "social_accounts"

	# Clave primaria
	id: Optional[int] = Field(default=None, primary_key=True, index=True)

	# Vinculación con usuario
	user_id: int = Field(foreign_key="users.id")

	# Información de la cuenta social
	provider: str = Field(max_length=50)  # google, facebook, twitter, etc.
	url: str = Field(max_length=500)


# ============================================================================
# MODELO DE DIRECCIONES
# ============================================================================

class Address(SQLModel, table=True):
	"""
	Direcciones físicas reutilizables.
	Almacena direcciones que pueden ser usadas para envío o facturación.
	"""
	__tablename__ = "addresses"

	# Clave primaria
	id: Optional[int] = Field(default=None, primary_key=True, index=True)

	# Información de dirección
	street: str = Field(max_length=200)
	number: str = Field(max_length=20)
	neighbourhood: Optional[str] = Field(default=None, max_length=100)
	city: str = Field(max_length=100)
	zip_code: str = Field(max_length=20)
	country: str = Field(max_length=100)
	note: Optional[str] = Field(default=None)


class UserAddress(SQLModel, table=True):
	"""
	Relación muchos-a-muchos entre usuarios y direcciones.
	Permite que un usuario tenga múltiples direcciones con diferentes propósitos.
	"""
	__tablename__ = "user_addresses"

	# Clave primaria compuesta
	user_id: int = Field(primary_key=True, foreign_key="users.id")
	address_id: int = Field(primary_key=True, foreign_key="addresses.id")

	# Tipo de dirección
	type: AddressType = Field()
	is_default: bool = Field(default=False)


# ============================================================================
# SISTEMA DE ENROLAMIENTO (MLM TREE)
# ============================================================================

class UserTreePath(SQLModel, table=True):
	"""
	Estructura de árbol genealógico para el sistema MLM.
	Implementa el patrón "Path Enumeration" para consultas eficientes de jerarquía.

	Esta tabla almacena todas las relaciones padre-hijo en la estructura de red,
	permitiendo consultas rápidas de línea ascendente y descendente.
	"""
	__tablename__ = "user_tree_paths"

	# Clave primaria compuesta
	sponsor_id: int = Field(primary_key=True, foreign_key="users.id")
	user_id: int = Field(primary_key=True, foreign_key="users.id")
	
	# Nivel en la estructura (0 = mismo usuario, 1 = directo, 2 = segundo nivel, etc.)
	level: int = Column(Integer, nullable=False, index=True)


# ============================================================================
# SISTEMA DE RANGOS Y VOLÚMENES
# ============================================================================

class Period(SQLModel, table=True):
	"""
	Períodos de tiempo para cálculo de comisiones y rangos.
	Define ventanas temporales para evaluación de performance.
	"""
	__tablename__ = "periods"

	# Clave primaria usando código del período (ej: "2025-09", "2025-10")
	code: str = Field(max_length=10, primary_key=True)

	# Fechas del período
	starts_on: date = Field()
	ends_on: date = Field()


class UserVolume(SQLModel, table=True):
	"""
	Volúmenes de puntos por usuario y período.
	Almacena PV (Personal Volume) y GV (Group Volume) para cálculos de comisiones.
	"""
	__tablename__ = "user_volumes"

	# Clave primaria
	id: Optional[int] = Field(default=None, primary_key=True, index=True)

	# Relaciones
	user_id: int = Field(foreign_key="users.id")
	period_id: str = Field(max_length=10, foreign_key="periods.code")

	# Volúmenes
	pv: float = Field(default=0.00)  # Personal Volume
	gv: float = Field(default=0.00)  # Group Volume


class Rank(SQLModel, table=True):
	"""
	Definición de rangos disponibles en el sistema.
	Establece los requisitos mínimos de volumen para cada rango.
	"""
	__tablename__ = "ranks"

	# Clave primaria
	id: Optional[int] = Field(default=None, primary_key=True, index=True)

	# Información del rango
	name: str = Field(max_length=100, unique=True)
	min_pv: float = Field(default=0.00)  # PV mínimo requerido
	min_gv: float = Field(default=0.00)  # GV mínimo requerido


class UserRankHistory(SQLModel, table=True):
	"""
	Historial de rangos alcanzados por usuarios.
	Mantiene un registro temporal de todos los rangos obtenidos.
	"""
	__tablename__ = "user_rank_history"

	# Clave primaria
	id: Optional[int] = Field(default=None, primary_key=True, index=True)

	# Relaciones
	user_id: int = Field(foreign_key="users.id")
	rank_id: int = Field(foreign_key="ranks.id")
	period_id: str = Field(max_length=10, foreign_key="periods.code")

	# Timestamp de logro
	achieved_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# SISTEMA DE PRODUCTOS Y ÓRDENES
# ============================================================================

class Product(rx.Model, table=True):
	"""
	Catálogo de productos disponibles para venta.
	Define los productos que pueden ser ordenados en el sistema.
	"""
	__tablename__ = "products"
	
	# Clave primaria
	id: Optional[int] = Column(Integer, primary_key=True, index=True)
	
	# Información del producto
	sku: str = Column(String(50), unique=True, nullable=False, index=True)
	name: str = Column(String(200), nullable=False)
	description: Optional[str] = Column(Text, nullable=True)
	pv: Numeric = Column(Numeric(10, 2), default=0.00)  # Puntos de volumen del producto


class Order(rx.Model, table=True):
	"""
	Órdenes de compra realizadas por usuarios.
	Almacena toda la información relacionada con una transacción.
	"""
	__tablename__ = "orders"
	
	# Clave primaria
	id: Optional[int] = Column(Integer, primary_key=True, index=True)
	
	# Identificador único de orden
	order_number: str = Column(String(50), unique=True, nullable=False, index=True)
	
	# Relación con usuario
	user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
	
	# Estado de la orden
	status: OrderStatus = Column(sa.Enum(OrderStatus), default=OrderStatus.PENDING)
	
	# Montos financieros
	subtotal_amount: Numeric = Column(Numeric(10, 2), default=0.00)
	discount_amount: Numeric = Column(Numeric(10, 2), default=0.00)
	tax_amount: Numeric = Column(Numeric(10, 2), default=0.00)
	shipping_amount: Numeric = Column(Numeric(10, 2), default=0.00)
	total_amount: Numeric = Column(Numeric(10, 2), nullable=False)
	currency: str = Column(String(3), default="USD")  # ISO 4217
	
	# Direcciones y método de pago
	shipping_address_id: int = Column(Integer, ForeignKey("addresses.id"), nullable=False)
	billing_address_id: int = Column(Integer, ForeignKey("addresses.id"), nullable=False)
	payment_method_id: int = Column(Integer, ForeignKey("payout_methods.id"), nullable=False)
	
	# Timestamps
	created_at: datetime = Column(DateTime, default=datetime.utcnow)
	updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OrderItem(rx.Model, table=True):
	"""
	Items individuales dentro de una orden.
	Almacena información snapshot del producto al momento de la compra.
	"""
	__tablename__ = "order_items"
	
	# Clave primaria
	id: Optional[int] = Column(Integer, primary_key=True, index=True)
	
	# Relaciones
	order_id: int = Column(Integer, ForeignKey("orders.id"), nullable=False)
	product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
	
	# Información snapshot (inmutable al momento de compra)
	sku_snapshot: str = Column(String(50), nullable=False)
	name_snapshot: str = Column(String(200), nullable=False)
	price_snapshot: Numeric = Column(Numeric(10, 2), nullable=False)
	
	# Cantidad y moneda
	quantity: int = Column(Integer, default=1)
	currency: str = Column(String(3), default="USD")


# ============================================================================
# SISTEMA DE BILLETERAS Y PAGOS
# ============================================================================

class Wallet(rx.Model, table=True):
	"""
	Billeteras virtuales de usuarios.
	Cada usuario puede tener múltiples billeteras para diferentes propósitos.
	"""
	__tablename__ = "wallets"
	
	# Clave primaria
	id: Optional[int] = Column(Integer, primary_key=True, index=True)
	
	# Relación con usuario
	user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
	
	# Tipo y moneda de billetera
	type: WalletType = Column(sa.Enum(WalletType), nullable=False)
	currency: str = Column(String(3), default="USD")  # ISO 4217
	
	# Timestamps
	created_at: datetime = Column(DateTime, default=datetime.utcnow)
	updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WalletLedger(rx.Model, table=True):
	"""
	Libro mayor de transacciones de billeteras.
	Registra todos los movimientos financieros con trazabilidad completa.
	"""
	__tablename__ = "wallet_ledger"
	
	# Clave primaria
	id: Optional[int] = Column(Integer, primary_key=True, index=True)
	
	# Relación con billetera
	wallet_id: int = Column(Integer, ForeignKey("wallets.id"), nullable=False)
	
	# Detalles de la transacción
	event_ts: datetime = Column(DateTime, default=datetime.utcnow)
	delta: Numeric = Column(Numeric(15, 2), nullable=False)  # Cambio en saldo (+ o -)
	reason_code: str = Column(String(50), nullable=False)  # commission, bonus, refund, etc.
	ref_id: Optional[str] = Column(String(100), nullable=True)  # ID de referencia externa
	note: Optional[str] = Column(Text, nullable=True)


class PayoutMethod(rx.Model, table=True):
	"""
	Métodos de pago configurados por usuarios.
	Almacena información de cuentas bancarias, PayPal, crypto, etc.
	"""
	__tablename__ = "payout_methods"
	
	# Clave primaria
	id: Optional[int] = Column(Integer, primary_key=True, index=True)
	
	# Relación con usuario
	user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
	
	# Tipo de método de pago
	provider: PayoutProvider = Column(sa.Enum(PayoutProvider), nullable=False)
	
	# Información específica del método (JSON flexible)
	bank_transfer: Optional[str] = Column(Text, nullable=True)  # JSON con datos bancarios
	other: Optional[str] = Column(Text, nullable=True)  # JSON con otros datos
	
	# Información de display y configuración
	last_4: Optional[str] = Column(String(4), nullable=True)  # Últimos 4 dígitos para display
	currency: str = Column(String(3), default="USD")
	is_default: bool = Column(Boolean, default=False)


class Withdrawal(rx.Model, table=True):
	"""
	Solicitudes de retiro de fondos.
	Gestiona el proceso completo desde solicitud hasta pago.
	"""
	__tablename__ = "withdrawals"
	
	# Clave primaria
	id: Optional[int] = Column(Integer, primary_key=True, index=True)
	
	# Relaciones
	user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
	payout_method_id: int = Column(Integer, ForeignKey("payout_methods.id"), nullable=False)
	
	# Detalles del retiro
	amount: Numeric = Column(Numeric(10, 2), nullable=False)
	currency: str = Column(String(3), default="USD")
	status: WithdrawalStatus = Column(sa.Enum(WithdrawalStatus), default=WithdrawalStatus.REQUESTED)
	
	# Timestamps del proceso
	requested_at: datetime = Column(DateTime, default=datetime.utcnow)
	processed_at: Optional[datetime] = Column(DateTime, nullable=True)


class Transfer(rx.Model, table=True):
	"""
	Transferencias entre billeteras.
	Permite movimiento de fondos entre diferentes billeteras del sistema.
	"""
	__tablename__ = "transfers"
	
	# Clave primaria
	id: Optional[int] = Column(Integer, primary_key=True, index=True)
	
	# Billeteras origen y destino
	from_wallet_id: int = Column(Integer, ForeignKey("wallets.id"), nullable=False)
	to_wallet_id: int = Column(Integer, ForeignKey("wallets.id"), nullable=False)
	
	# Detalles de la transferencia
	amount: Numeric = Column(Numeric(10, 2), nullable=False)
	currency: str = Column(String(3), default="USD")
	note: Optional[str] = Column(Text, nullable=True)
	
	# Timestamp
	created_at: datetime = Column(DateTime, default=datetime.utcnow)


# ============================================================================
# CONFIGURACIÓN DE RELACIONES (SQLAlchemy Relationships)
# ============================================================================

# Nota: Las relaciones se pueden definir aquí si se necesita navegación de objetos
# Por ahora, usamos ForeignKey para mantener el rendimiento óptimo

# Ejemplo de cómo definir relaciones si se necesitan:
# User.profile = relationship("UserProfile", uselist=False, back_populates="user")
# UserProfile.user = relationship("User", back_populates="profile")


# ============================================================================
# FUNCIONES DE UTILIDAD PARA LA BASE DE DATOS
# ============================================================================

def get_database_url() -> str:
	"""
	Obtiene la URL de conexión a la base de datos desde la configuración.
	Prioriza variables de entorno para configuración segura en producción.
	"""
	import os
	from rxconfig import config
	
	# Priorizar variable de entorno para producción
	if os.getenv("DATABASE_URL"):
		return os.getenv("DATABASE_URL")
	
	# Usar configuración del archivo si está disponible
	if hasattr(config, 'db_url') and config.db_url:
		return config.db_url
	
	# Fallback a SQLite local para desarrollo
	return "sqlite:///./reflex.db"


def validate_referral_code(code: str) -> bool:
	"""
	Valida el formato de un código de referido.
	
	Args:
		code: Código de referido a validar
		
	Returns:
		bool: True si el código es válido
	"""
	import re
	# El código debe tener entre 6-20 caracteres alfanuméricos
	pattern = r'^[A-Za-z0-9]{6,20}$'
	return bool(re.match(pattern, code))


def generate_order_number() -> str:
	"""
	Genera un número de orden único.
	
	Returns:
		str: Número de orden único basado en timestamp y componente aleatorio
	"""
	import random
	import time
	
	timestamp = int(time.time())
	random_part = random.randint(1000, 9999)
	return f"NN{timestamp}{random_part}"