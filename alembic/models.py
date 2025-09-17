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
"""

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
    BILLING = "billing"      # Dirección de facturación
    SHIPPING = "shipping"    # Dirección de envío
    OTHER = "other"          # Otra dirección


class WalletType(Enum):
    """Tipos de billetera disponibles"""
    COMMISSIONS = "commissions"  # Billetera de comisiones
    BONUSES = "bonuses"         # Billetera de bonos
    REFUNDS = "refunds"         # Billetera de reembolsos


class PayoutProvider(Enum):
    """Proveedores de métodos de pago"""
    BANK_TRANSFER = "bank_transfer"  # Transferencia bancaria
    PAYPAL = "paypal"                # PayPal
    CRYPTO = "crypto"                # Criptomonedas
    OTHER = "other"                  # Otros métodos


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
    # Clave primaria compuesta
    sponsor_id: int = Field(primary_key=True, foreign_key="users.id")
    user_id: int = Field(primary_key=True, foreign_key="users.id")

    # Nivel en la estructura (0 = mismo usuario, 1 = directo, 2 = segundo nivel, etc.)
    level: int = Field(index=True)


# ============================================================================
# SISTEMA DE RANGOS Y VOLÚMENES
# ============================================================================

class Period(SQLModel, table=True):
    """
    Períodos de tiempo para cálculo de comisiones y rangos.
    Define ventanas temporales para evaluación de performance.
    """
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

class Product(SQLModel, table=True):
    """
    Catálogo de productos disponibles para venta.
    Define los productos que pueden ser ordenados en el sistema.
    """
    # Clave primaria
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Información del producto
    sku: str = Field(max_length=50, unique=True, index=True)
    name: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    pv: float = Field(default=0.00)  # Puntos de volumen del producto


class Order(SQLModel, table=True):
    """
    Órdenes de compra realizadas por usuarios.
    Almacena toda la información relacionada con una transacción.
    """
    # Clave primaria
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Identificador único de orden
    order_number: str = Field(max_length=50, unique=True, index=True)

    # Relación con usuario
    user_id: int = Field(foreign_key="users.id")

    # Estado de la orden
    status: OrderStatus = Field(default=OrderStatus.PENDING)

    # Montos financieros
    subtotal_amount: float = Field(default=0.00)
    discount_amount: float = Field(default=0.00)
    tax_amount: float = Field(default=0.00)
    shipping_amount: float = Field(default=0.00)
    total_amount: float = Field()
    currency: str = Field(max_length=3, default="USD")  # ISO 4217

    # Direcciones y método de pago
    shipping_address_id: int = Field(foreign_key="addresses.id")
    billing_address_id: int = Field(foreign_key="addresses.id")
    payment_method_id: int = Field(foreign_key="payout_methods.id")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OrderItem(SQLModel, table=True):
    """
    Items individuales dentro de una orden.
    Almacena información snapshot del producto al momento de la compra.
    """
    # Clave primaria
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relaciones
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")

    # Información snapshot (inmutable al momento de compra)
    sku_snapshot: str = Field(max_length=50)
    name_snapshot: str = Field(max_length=200)
    price_snapshot: float = Field()

    # Cantidad y moneda
    quantity: int = Field(default=1)
    currency: str = Field(max_length=3, default="USD")


# ============================================================================
# SISTEMA DE BILLETERAS Y PAGOS
# ============================================================================

class Wallet(SQLModel, table=True):
    """
    Billeteras virtuales de usuarios.
    Cada usuario puede tener múltiples billeteras para diferentes propósitos.
    """
    # Clave primaria
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relación con usuario
    user_id: int = Field(foreign_key="users.id")

    # Tipo y moneda de billetera
    type: WalletType = Field()
    currency: str = Field(max_length=3, default="USD")  # ISO 4217

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class WalletLedger(SQLModel, table=True):
    """
    Libro mayor de transacciones de billeteras.
    Registra todos los movimientos financieros con trazabilidad completa.
    """
    # Clave primaria
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relación con billetera
    wallet_id: int = Field(foreign_key="wallets.id")

    # Detalles de la transacción
    event_ts: datetime = Field(default_factory=datetime.utcnow)
    delta: float = Field()  # Cambio en saldo (+ o -)
    reason_code: str = Field(max_length=50)  # commission, bonus, refund, etc.
    ref_id: Optional[str] = Field(default=None, max_length=100)  # ID de referencia externa
    note: Optional[str] = Field(default=None)


class PayoutMethod(SQLModel, table=True):
    """
    Métodos de pago configurados por usuarios.
    Almacena información de cuentas bancarias, PayPal, crypto, etc.
    """
    # Clave primaria
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relación con usuario
    user_id: int = Field(foreign_key="users.id")

    # Tipo de método de pago
    provider: PayoutProvider = Field()

    # Información específica del método (JSON flexible)
    bank_transfer: Optional[str] = Field(default=None)  # JSON con datos bancarios
    other: Optional[str] = Field(default=None)  # JSON con otros datos

    # Información de display y configuración
    last_4: Optional[str] = Field(default=None, max_length=4)  # Últimos 4 dígitos para display
    currency: str = Field(max_length=3, default="USD")
    is_default: bool = Field(default=False)


class Withdrawal(SQLModel, table=True):
    """
    Solicitudes de retiro de fondos.
    Gestiona el proceso completo desde solicitud hasta pago.
    """
    # Clave primaria
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relaciones
    user_id: int = Field(foreign_key="users.id")
    payout_method_id: int = Field(foreign_key="payout_methods.id")

    # Detalles del retiro
    amount: float = Field()
    currency: str = Field(max_length=3, default="USD")
    status: WithdrawalStatus = Field(default=WithdrawalStatus.REQUESTED)

    # Timestamps del proceso
    requested_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = Field(default=None)


class Transfer(SQLModel, table=True):
    """
    Transferencias entre billeteras.
    Permite movimiento de fondos entre diferentes billeteras del sistema.
    """
    # Clave primaria
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Billeteras origen y destino
    from_wallet_id: int = Field(foreign_key="wallets.id")
    to_wallet_id: int = Field(foreign_key="wallets.id")

    # Detalles de la transferencia
    amount: float = Field()
    currency: str = Field(max_length=3, default="USD")
    note: Optional[str] = Field(default=None)

    # Timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow)
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
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url

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