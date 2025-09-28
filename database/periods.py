import reflex as rx
from sqlmodel import Field, func
from datetime import datetime, timezone

class Periods(rx.Model, table=True):
    """
    Modelo para periodos de comisiones y actividades.
    Define los periodos en los que se calculan las comisiones y otras actividades.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    # Nombre del periodo (único)
    name: str = Field(unique=True, index=True)
    
    # Descripción del periodo
    description: str | None = Field(default=None, max_length=255)

    # Fechas de inicio y fin del periodo
    starts_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column_kwargs={"server_default": func.now()})
    ends_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column_kwargs={"server_default": func.now()})