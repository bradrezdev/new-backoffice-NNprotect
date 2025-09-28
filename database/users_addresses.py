import reflex as rx
from sqlmodel import Field, func
from datetime import datetime
from NNProtect_new_website.utils.timezone_mx import get_mexico_now

class UserAddresses(rx.Model, table=True):
    """Direcciones de usuario con timestamps México Central (UTC - 6h)."""
    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.id")
    address_id: int = Field(foreign_key="addresses.id")
    address_name: str = Field(default=None, index=True)
    is_default: bool = Field(default=False)
    
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