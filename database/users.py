import reflex as rx

# Permite encriptar la contraseña del usuario
import bcrypt

# Librerías de rx.Model para definir modelos y relaciones
from sqlmodel import Field, func
from typing import Optional
from enum import Enum

# Manejo de fechas y horas con zona horaria
from datetime import datetime, date, timezone


class UserStatus(Enum):
    """Estados posibles de un usuario en el sistema"""
    NO_QUALIFIED = "no calificado"       # Usuario no calificado
    QUALIFIED = "calificado"             # Usuario calificado
    SUSPENDED = "suspendido"             # Usuario suspendido


class UserGender(Enum):
    """Género del usuario"""
    MALE = "masculino"                  # Masculino
    FEMALE = "femenino"                  # Femenino
    OTHER = "otro"                       # Otro


class Users(rx.Model, table=True):
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
    id: int = Field(default=None, primary_key=True, index=True)

    # Identificadores únicos
    member_id: int = Field(unique=True, index=True)
    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(unique=True, index=True)

    # Estado y estructura de red
    status: UserStatus = Field(default=UserStatus.NO_QUALIFIED)
    sponsor_id: Optional[int] = Field(default=None, foreign_key="users.id")
    referral_code: str = Field(max_length=20, unique=True, default="")

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column_kwargs={"server_default": func.now()})