import reflex as rx
from sqlmodel import Field

class UserAddresses(rx.Model, table=True):
    """Modelo de direcciones de usuario"""
    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.id")
    address_id: int = Field(foreign_key="addresses.id")
    address_name: str = Field(default=None, index=True)
    is_default: bool = Field(default=False)
    created_at: str = Field(index=True)
    updated_at: str = Field(index=True)