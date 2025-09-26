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
    NO_QUALIFIED = "NO_QUALIFIED"       # Usuario no calificado
    QUALIFIED = "QUALIFIED"             # Usuario calificado
    SUSPENDED = "SUSPENDED"             # Usuario suspendido

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
    id: int | None = Field(default=None, primary_key=True, index=True)

    # Vinculo con Supabase Auth - UUID del usuario en auth.users
    supabase_user_id: str | None = Field(default=None, index=True, unique=True)

    # Identificadores únicos
    member_id: int = Field(unique=True, index=True)

    # Nombres de la persona
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    
    # Cache de email para consultas rápidas (email real está en Supabase auth.users)
    email_cache: str | None = Field(default=None, index=True)

    # Estado y estructura de red
    status: UserStatus = Field(default=UserStatus.NO_QUALIFIED)
    sponsor_id: int | None = Field(default=None)  # Temporal - sin FK para evitar problemas circulares
    referral_link: str | None = Field(default=None, unique=True, index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column_kwargs={"server_default": func.now()})
    
    @property
    def full_name(self) -> str:
        """Nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip()