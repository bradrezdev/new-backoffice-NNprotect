import reflex as rx

from sqlmodel import Field, SQLModel

@rx.ModelRegistry.register
class RolesUsers(SQLModel, table=True):
    """
    Tabla intermedia para la relación muchos a muchos entre usuarios y roles.
    Permite asignar múltiples roles a un usuario y viceversa.
    """
    # Clave primaria compuesta
    user_id: int = Field(primary_key=True, foreign_key="users.id", index=True)
    role_id: int = Field(foreign_key="roles.role_id", index=True)