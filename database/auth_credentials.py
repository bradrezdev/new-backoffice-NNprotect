import reflex as rx

from sqlmodel import Field
from typing import Optional
from datetime import datetime
from database.users import Users

# Permite encriptar la contraseña del usuario
import bcrypt


class AuthCredentials(rx.Model, table=True):
    """
    Credenciales de autenticación de usuarios.
    Almacena información sensible de autenticación de forma segura.
    """
    # Clave primaria compuesta con user_id
    user_id: int = Field(primary_key=True, foreign_key="users.id")

    # Datos de autenticación
    password_hash: str = Field(max_length=255)
    terms_accepted: bool = Field(default=False)
    last_login_at: Optional[datetime] = Field(default=None)

    @classmethod
    def create_credentials(cls, user_id: int, password: str):
        # Hashear la contraseña
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return cls(
            user_id=user_id,
            password_hash=password_hash.decode('utf-8'),
        )
