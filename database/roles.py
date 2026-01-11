import reflex as rx

from sqlmodel import Field, SQLModel
from enum import Enum

@rx.ModelRegistry.register
class Roles(SQLModel, table=True):
    """
    Roles asignados a usuarios.
    Permite un sistema de permisos flexible basado en roles.
    """
    # Clave primaria
    role_id: int = Field(primary_key=True, index=True)

    # Información del rol
    role_name: str = Field(default="user")