"""
Servicio de inicialización de base de datos.
Crea datos iniciales necesarios como el primer período.
"""

import reflex as rx
import sqlmodel
from datetime import datetime, timezone
from calendar import monthrange
from sqlalchemy.exc import OperationalError

from .periods import Periods


def initialize_database():
    """
    Inicializa la base de datos con datos necesarios.
    Crea el período actual si no existe.
    """
    try:
        with rx.session() as session:
            # Verificar si ya existe algún período
            existing_period = session.exec(
                sqlmodel.select(Periods)
            ).first()

            if existing_period:
                print(f"✅ Ya existe período en BD: {existing_period.name}")
                return

            # Crear período para el mes actual
            now = datetime.now(timezone.utc)
            year = now.year
            month = now.month

            # Calcular primer y último día del mes en UTC
            first_day = datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc)
            last_day_num = monthrange(year, month)[1]
            last_day = datetime(year, month, last_day_num, 23, 59, 59, tzinfo=timezone.utc)

            # Crear período inicial
            period_name = f"{year}-{month:02d}"
            initial_period = Periods(
                name=period_name,
                description=f"Período inicial {month:02d}/{year}",
                starts_on=first_day,
                ends_on=last_day,
                closed_at=None
            )

            session.add(initial_period)
            session.commit()
            print(f"✅ Período inicial creado: {period_name} ({first_day.date()} - {last_day.date()})")

    except OperationalError as e:
        print(f"⚠️ No se pudo inicializar la BD (posiblemente faltan migraciones): {e}")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        import traceback
        traceback.print_exc()
