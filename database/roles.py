import reflex as rx

from sqlmodel import Field
from enum import Enum

class Roles(rx.Model, table=True):
    """
    Roles asignados a usuarios.
    Permite un sistema de permisos flexible basado en roles.
    """
    # Clave primaria
    role_id: int = Field(primary_key=True, index=True)

    # Información del rol
    role_name: str = Field(default="user")