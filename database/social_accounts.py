import reflex as rx
from sqlmodel import Field
from enum import Enum

class SocialNetwork(Enum):
    """Redes sociales soportadas para autenticación"""
    FACEBOOK = "facebook"                 # Facebook
    INSTAGRAM = "instagram"               # Instagram
    X = "x"                               # Twitter (X)

class SocialAccounts(rx.Model, table=True):
    """
    Cuentas sociales vinculadas a usuarios.
    Permite integración con redes sociales y otros proveedores de identidad.
    """
    # Clave primaria
    socialaccount_id: int = Field(primary_key=True, index=True)

    # Vinculación con usuario
    user_id: int = Field(foreign_key="users.id")

    # Información de la cuenta social
    provider: SocialNetwork = Field(default=None, index=True)
    url: str = Field(default=None)