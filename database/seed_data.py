"""
Script de inicialización de datos maestros (seed data).
Puebla las tablas críticas que deben existir antes del primer registro.

Principios aplicados: KISS, DRY
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import reflex as rx
from sqlmodel import Session, select
from datetime import datetime, timezone

from database.ranks import Ranks
from database.roles import Roles


def seed_ranks(session: Session) -> bool:
    """
    Inicializa los rangos del sistema MLM según MLM_SCHEME_README.md

    Args:
        session: Sesión de base de datos

    Returns:
        True si se inicializaron correctamente
    """
    try:
        # Verificar si ya existen rangos
        existing_ranks = session.exec(select(Ranks)).first()
        if existing_ranks:
            print("⚠️  Los rangos ya están inicializados")
            return True

        # Definición de rangos según MLM_SCHEME_README.md líneas 74-87
        ranks_data = [
            {
                "id": 1,
                "name": "Sin rango",
                "pv_required": 0,
                "pvg_required": 0,
                "min_pvg": None
            },
            {
                "id": 2,
                "name": "Visionario",
                "pv_required": 1465,
                "pvg_required": 1465,
                "min_pvg": 1465
            },
            {
                "id": 3,
                "name": "Emprendedor",
                "pv_required": 1465,
                "pvg_required": 21000,
                "min_pvg": 21000
            },
            {
                "id": 4,
                "name": "Creativo",
                "pv_required": 1465,
                "pvg_required": 58000,
                "min_pvg": 58000
            },
            {
                "id": 5,
                "name": "Innovador",
                "pv_required": 1465,
                "pvg_required": 120000,
                "min_pvg": 120000
            },
            {
                "id": 6,
                "name": "Embajador Transformador",
                "pv_required": 1465,
                "pvg_required": 300000,
                "min_pvg": 300000
            },
            {
                "id": 7,
                "name": "Embajador Inspirador",
                "pv_required": 1465,
                "pvg_required": 650000,
                "min_pvg": 650000
            },
            {
                "id": 8,
                "name": "Embajador Consciente",
                "pv_required": 1465,
                "pvg_required": 1300000,
                "min_pvg": 1300000
            },
            {
                "id": 9,
                "name": "Embajador Solidario",
                "pv_required": 1465,
                "pvg_required": 2900000,
                "min_pvg": 2900000
            }
        ]

        # Insertar rangos
        for rank_data in ranks_data:
            rank = Ranks(**rank_data)
            session.add(rank)

        session.commit()
        print(f"✅ {len(ranks_data)} rangos inicializados correctamente")
        return True

    except Exception as e:
        session.rollback()
        print(f"❌ Error inicializando rangos: {e}")
        return False


def seed_roles(session: Session) -> bool:
    """
    Inicializa los roles del sistema.

    Args:
        session: Sesión de base de datos

    Returns:
        True si se inicializaron correctamente
    """
    try:
        # Verificar si ya existen roles
        existing_roles = session.exec(select(Roles)).first()
        if existing_roles:
            print("⚠️  Los roles ya están inicializados")
            return True

        # Definición de roles del sistema
        roles_data = [
            {
                "role_id": 1,
                "role_name": "USER"
            },
            {
                "role_id": 2,
                "role_name": "ADMIN"
            },
            {
                "role_id": 3,
                "role_name": "MODERATOR"
            }
        ]

        # Insertar roles
        for role_data in roles_data:
            role = Roles(**role_data)
            session.add(role)

        session.commit()
        print(f"✅ {len(roles_data)} roles inicializados correctamente")
        return True

    except Exception as e:
        session.rollback()
        print(f"❌ Error inicializando roles: {e}")
        return False


def initialize_master_data():
    """
    Inicializa TODOS los datos maestros necesarios para el sistema.
    Debe ejecutarse después de reflex db init.
    """
    print("🔧 Inicializando datos maestros del sistema...")

    try:
        # Obtener sesión de base de datos
        with rx.session() as session:
            # Inicializar rangos
            ranks_ok = seed_ranks(session)

            # Inicializar roles
            roles_ok = seed_roles(session)

            if ranks_ok and roles_ok:
                print("✅ Datos maestros inicializados correctamente")
                return True
            else:
                print("❌ Algunos datos maestros no se pudieron inicializar")
                return False

    except Exception as e:
        print(f"❌ Error general inicializando datos maestros: {e}")
        return False


if __name__ == "__main__":
    initialize_master_data()
