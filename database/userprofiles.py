import reflex as rx
from sqlmodel import Field
from enum import Enum

class UserGender(Enum):
    """Género del usuario"""
    MALE = "MALE"                  # Masculino
    FEMALE = "FEMALE"                  # Femenino

class UserProfiles(rx.Model, table=True):
    """
    Perfiles extendidos de usuarios.
    Contiene información personal y de contacto adicional.
    """
    # Clave primaria compuesta con user_id
    user_id: int = Field(primary_key=True, foreign_key="users.id")

    # Información personal
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    gender: UserGender = Field(index=True)
    phone_number: str = Field(index=True)
    photo_url: str = Field(default=None)