"""
Servicio POO para gestión automática de períodos mensuales.
Maneja creación y finalización automática de períodos.

Principios aplicados: KISS, DRY, YAGNI, POO
"""

import sqlmodel
from datetime import datetime, timezone
from typing import Optional
from calendar import monthrange

from database.periods import Periods
from ..utils.timezone_mx import get_mexico_now


class PeriodService:
    """
    Servicio POO para manejo automático de períodos.
    Principio POO: Encapsula toda la lógica de gestión de períodos.
    """

    @classmethod
    def get_current_period(cls, session) -> Optional[Periods]:
        """
        Obtiene el período actual activo.
        Principio KISS: Método simple para obtener período actual.

        Returns:
            Periods object si existe, None si no hay período actual
        """
        try:
            current_date = get_mexico_now()

            current_period = session.exec(
                sqlmodel.select(Periods)
                .where(
                    (Periods.starts_on <= current_date) &
                    (Periods.ends_on >= current_date) &
                    (Periods.closed_at.is_(None))
                )
            ).first()

            return current_period

        except Exception as e:
            print(f"❌ Error obteniendo período actual: {e}")
            return None

    @classmethod
    def create_period_for_month(cls, session, year: int, month: int) -> Optional[Periods]:
        """
        Crea un nuevo período para el mes especificado.
        Principio KISS: Creación directa sin complejidad innecesaria.

        Args:
            session: Sesión de base de datos
            year: Año del período
            month: Mes del período (1-12)

        Returns:
            Periods object creado o None si falló
        """
        try:
            # Verificar si ya existe un período para este mes
            period_name = f"{year}-{month:02d}"
            existing_period = session.exec(
                sqlmodel.select(Periods).where(Periods.name == period_name)
            ).first()

            if existing_period:
                print(f"⚠️  Ya existe período para {period_name}")
                return existing_period

            # Calcular primer y último día del mes en UTC
            first_day = datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc)
            last_day_num = monthrange(year, month)[1]
            last_day = datetime(year, month, last_day_num, 23, 59, 59, tzinfo=timezone.utc)

            # Crear nuevo período
            new_period = Periods(
                name=period_name,
                description=f"Período {month:02d}/{year}",
                starts_on=first_day,
                ends_on=last_day,
                closed_at=None
            )

            session.add(new_period)
            session.flush()

            print(f"✅ Período creado: {period_name} ({first_day.date()} - {last_day.date()})")
            return new_period

        except Exception as e:
            print(f"❌ Error creando período para {year}-{month:02d}: {e}")
            return None

    @classmethod
    def auto_create_current_month_period(cls, session) -> Optional[Periods]:
        """
        Crea automáticamente el período para el mes actual si no existe.
        Principio DRY: Método reutilizable para crear período del mes actual.

        Returns:
            Periods object del mes actual
        """
        try:
            current_date = get_mexico_now()
            year = current_date.year
            month = current_date.month

            return cls.create_period_for_month(session, year, month)

        except Exception as e:
            print(f"❌ Error creando período del mes actual: {e}")
            return None

    @classmethod
    def finalize_period(cls, session, period_id: int) -> bool:
        """
        Finaliza un período marcándolo como cerrado.
        Principio KISS: Simplemente marca closed_at.

        Args:
            session: Sesión de base de datos
            period_id: ID del período a finalizar

        Returns:
            True si se finalizó correctamente, False si falló
        """
        try:
            period = session.exec(
                sqlmodel.select(Periods).where(Periods.id == period_id)
            ).first()

            if not period:
                print(f"❌ Período {period_id} no encontrado")
                return False

            if period.closed_at:
                print(f"⚠️  Período {period.name} ya está cerrado")
                return False

            # Marcar como cerrado
            period.closed_at = datetime.now(timezone.utc)
            session.add(period)
            session.flush()

            print(f"✅ Período {period.name} finalizado el {period.closed_at}")
            return True

        except Exception as e:
            print(f"❌ Error finalizando período {period_id}: {e}")
            return False

    @classmethod
    def auto_finalize_past_periods(cls, session) -> int:
        """
        Finaliza automáticamente todos los períodos cuya fecha de fin ya pasó.
        Principio DRY: Método reutilizable para cierre automático.

        Returns:
            Número de períodos finalizados
        """
        try:
            current_date = get_mexico_now()

            # Obtener períodos que ya terminaron pero no están cerrados
            past_periods = session.exec(
                sqlmodel.select(Periods)
                .where(
                    (Periods.ends_on < current_date) &
                    (Periods.closed_at.is_(None))
                )
            ).all()

            finalized_count = 0
            for period in past_periods:
                if cls.finalize_period(session, period.id):
                    finalized_count += 1

            if finalized_count > 0:
                print(f"✅ Finalizados {finalized_count} períodos automáticamente")

            return finalized_count

        except Exception as e:
            print(f"❌ Error finalizando períodos pasados: {e}")
            return 0

    @classmethod
    def check_and_manage_periods(cls, session) -> bool:
        """
        Verifica y gestiona períodos automáticamente:
        1. Finaliza períodos pasados
        2. Crea período del mes actual si no existe

        Principio POO: Método orquestador para gestión completa.

        Returns:
            True si se ejecutó correctamente
        """
        try:
            # 1. Finalizar períodos pasados
            cls.auto_finalize_past_periods(session)

            # 2. Crear período del mes actual si no existe
            current_period = cls.get_current_period(session)
            if not current_period:
                cls.auto_create_current_month_period(session)

            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"❌ Error gestionando períodos: {e}")
            return False
