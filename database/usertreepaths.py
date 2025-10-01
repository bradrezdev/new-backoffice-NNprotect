import reflex as rx
from sqlmodel import Field

class UserTreePath(rx.Model, table=True):
    """
    Estructura de árbol genealógico para el sistema MLM.
    Implementa el patrón "Path Enumeration" para consultas eficientes de jerarquía.

    Esta tabla almacena todas las relaciones ancestro-descendiente pre-calculadas,
    permitiendo consultas rápidas de línea ascendente y descendente sin recursión.
    """
    # Clave primaria compuesta
    ancestor_id: int = Field(primary_key=True, foreign_key="users.member_id", index=True)
    descendant_id: int = Field(primary_key=True, foreign_key="users.member_id", index=True)
    depth: int = Field(primary_key=True)  # 0=self, 1=hijo directo, 2=nieto, etc.