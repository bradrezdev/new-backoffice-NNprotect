"""
Modelos de base de datos para rangos de usuarios.
"""

import reflex as rx
from sqlmodel import Field

class Ranks(rx.Model, table=True):
    """
    Modelo de rangos de usuarios en el sistema.
    Define los diferentes rangos que un usuario puede alcanzar basado en puntos y otros criterios.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    # Nombre del rango (único)
    name: str = Field(unique=True, index=True)
    
    # Puntos necesarios para alcanzar este rango
    pv_required: int = Field(default=0)

    # Puntos necesarios para alcanzar este rango
    pvg_required: int = Field(default=0)