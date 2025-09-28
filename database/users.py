import reflex as rx
import bcrypt
from sqlmodel import Field, func
from typing import Optional
from enum import Enum
from datetime import datetime, date, timezone

# ✅ Usar timezone utility con resta de 6 horas
from NNProtect_new_website.utils.timezone_mx import get_mexico_now


class UserStatus(Enum):
    """Estados posibles de un usuario en el sistema"""
    NO_QUALIFIED = "NO_QUALIFIED"
    QUALIFIED = "QUALIFIED" 
    SUSPENDED = "SUSPENDED"

class Users(rx.Model, table=True):
    """
    Modelo principal de usuarios con timestamps México Central (UTC - 6h).
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
    
    # Cache del país de registro desde addresses
    country_cache: str | None = Field(default=None, max_length=50, index=True)  # ✅ Texto plano

    # Estado y estructura de red
    status: UserStatus = Field(default=UserStatus.NO_QUALIFIED)
    sponsor_id: int | None = Field(default=None)  # Temporal - sin FK para evitar problemas circulares
    referral_link: str | None = Field(default=None, unique=True, index=True)

    # ✅ Timestamps México Central (UTC - 6 horas)
    created_at: datetime = Field(
        default_factory=get_mexico_now,
        sa_column_kwargs={
            "server_default": func.now() - func.interval('6 hours')
        }
    )
    updated_at: datetime = Field(
        default_factory=get_mexico_now,
        sa_column_kwargs={
            "server_default": func.now() - func.interval('6 hours')
        }
    )
    
    @property
    def full_name(self) -> str:
        """Nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip()