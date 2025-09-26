import reflex as rx
from sqlmodel import Field
from datetime import datetime, timezone
from sqlmodel import func

class AuthCredentials(rx.Model, table=True):
    """
    Credenciales de autenticación de usuarios.
    Nota: Con Supabase Auth, este modelo es principalmente para compatibilidad.
    La autenticación real la maneja Supabase.
    """
    # Clave primaria compuesta con user_id
    user_id: int = Field(primary_key=True, foreign_key="users.id")
    
    # Hash de contraseña (para compatibilidad - Supabase maneja la real)
    password_hash: str = Field(default="supabase_managed")
    
    # Configuraciones de autenticación  
    terms_accepted: bool = Field(default=False)
    email_verified: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column_kwargs={"server_default": func.now()})