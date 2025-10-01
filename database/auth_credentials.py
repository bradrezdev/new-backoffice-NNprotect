import reflex as rx
from sqlmodel import Field, func
from datetime import datetime, timezone
from NNProtect_new_website.utils.timezone_mx import get_mexico_now

class AuthCredentials(rx.Model, table=True):
    """
    Credenciales de autenticación con timestamps en UTC puro.
    """
    user_id: int = Field(primary_key=True, foreign_key="users.id")
    password_hash: str = Field(default="supabase_managed")
    terms_accepted: bool = Field(default=False)
    email_verified: bool = Field(default=False)

    # Timestamps en UTC puro (conversión a timezone local en UI)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()}
    )