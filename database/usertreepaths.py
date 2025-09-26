import reflex as rx
from sqlmodel import Field

class UserTreePath(rx.Model, table=True):
    """
    #Estructura de árbol genealógico para el sistema MLM.
    #Implementa el patrón "Path Enumeration" para consultas eficientes de jerarquía.

    #Esta tabla almacena todas las relaciones padre-hijo en la estructura de red,
    #permitiendo consultas rápidas de línea ascendente y descendente.
    """
    # Clave primaria compuesta
    sponsor_id: int = Field(primary_key=True, foreign_key="users.member_id")
    user_id: int = Field(primary_key=True, foreign_key="users.member_id")