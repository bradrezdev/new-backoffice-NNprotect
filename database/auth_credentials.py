import reflex as rx
from sqlmodel import Field, func
from datetime import datetime, timezone
from NNProtect_new_website.utils.timezone_mx import get_mexico_now

class AuthCredentials(rx.Model, table=True):
    """
    Credenciales con timestamps México Central (UTC - 6h).
    """
    user_id: int = Field(primary_key=True, foreign_key="users.id")
    password_hash: str = Field(default="supabase_managed")
    terms_accepted: bool = Field(default=False)
    email_verified: bool = Field(default=False)
    
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