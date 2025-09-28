import reflex as rx
from sqlmodel import Field, ForeignKey
from enum import Enum


# ✅ Mantener Countries SOLO para product_service (fuera del scope del registro)
class Countries(Enum):
    USA = "USA"
    COLOMBIA = "COLOMBIA"
    MEXICO = "MEXICO"
    PUERTO_RICO = "PUERTO_RICO"


class Addresses(rx.Model, table=True):
    """
    Tabla de direcciones.
    Contiene información de direcciones asociadas a usuarios.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)

    # Información de dirección
    street: str = Field(index=True)
    neighborhood: str = Field(index=True)
    city: str = Field(index=True)
    state: str = Field(index=True)
    country: str = Field(max_length=50, index=True)  # ✅ Texto plano en lugar de ENUM
    zip_code: str = Field(index=True)