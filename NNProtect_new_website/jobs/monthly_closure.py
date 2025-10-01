"""
Job programado de cierre mensual.
Se ejecuta el último día del mes a las 23:59:59 (horario México Central).
Calcula todas las comisiones mensuales (Uninivel, Matching, etc).

Principios aplicados: KISS, DRY, YAGNI, POO
"""

import reflex as rx
import sqlmodel
from typing import List, Optional
from datetime import datetime, timezone

from database.users import Users
from database.periods import Periods
from NNProtect_new_website.mlm_service.commission_service import CommissionService
from NNProtect_new_website.utils.timezone_mx import get_mexico_now


class MonthlyClosureJob:
    """
    Job de cierre mensual para cálculo de comisiones recurrentes.
    Principio POO: Encapsula toda la lógica del cierre mensual.
    """

    @classmethod
    def execute_monthly_closure(cls) -> bool:
        """
        Ejecuta el cierre mensual completo.
        Principio KISS: Proceso lineal y claro.

        Pasos:
        1. Verificar que no se haya ejecutado ya (idempotencia)
        2. Obtener período actual
        3. Calcular comisiones Uninivel para todos los usuarios activos
        4. Calcular comisiones Matching para Embajadores
        5. Marcar período como cerrado

        Returns:
            True si el cierre fue exitoso, False si falló
        """
        try:
            print("🔄 Iniciando cierre mensual...")

            with rx.session() as session:
                # 1. Obtener período actual
                current_period = cls._get_current_period(session)

                if not current_period:
                    print("❌ No hay período activo para cerrar")
                    return False

                # 2. Verificar idempotencia (no ejecutar si ya está cerrado)
                if current_period.closed_at is not None:
                    print(f"⚠️  Período {current_period.id} ya está cerrado")
                    return True

                print(f"📅 Cerrando período: {current_period.period_name} (ID: {current_period.id})")

                # 3. Obtener todos los usuarios activos (con PV > 0 en el período)
                active_users = cls._get_active_users(session, current_period.id)

                if not active_users:
                    print("⚠️  No hay usuarios activos en este período")
                    # Marcar período como cerrado aunque no haya usuarios
                    current_period.closed_at = datetime.now(timezone.utc)
                    session.add(current_period)
                    session.commit()
                    return True

                print(f"👥 Procesando {len(active_users)} usuarios activos...")

                # 4. Calcular Bono Uninivel para cada usuario
                total_commissions = 0
                for user in active_users:
                    commission_ids = CommissionService.calculate_unilevel_bonus(
                        session, user.member_id, current_period.id
                    )
                    total_commissions += len(commission_ids)

                print(f"✅ {total_commissions} comisiones Uninivel calculadas")

                # 5. Calcular Bono Matching para Embajadores
                matching_count = 0
                ambassador_ranks = [
                    "Embajador Transformador",
                    "Embajador Inspirador",
                    "Embajador Consciente",
                    "Embajador Solidario"
                ]

                for user in active_users:
                    # Obtener rango del usuario
                    from NNProtect_new_website.mlm_service.rank_service import RankService
                    from database.ranks import Ranks

                    rank_id = RankService.get_user_current_rank(session, user.member_id)
                    if not rank_id:
                        continue

                    rank = session.exec(
                        sqlmodel.select(Ranks).where(Ranks.id == rank_id)
                    ).first()

                    if not rank or rank.name not in ambassador_ranks:
                        continue

                    # Calcular Matching Bonus
                    matching_ids = CommissionService.calculate_matching_bonus(
                        session, user.member_id, current_period.id
                    )
                    matching_count += len(matching_ids)

                print(f"✅ {matching_count} comisiones Matching calculadas")

                # 6. Marcar período como cerrado
                current_period.closed_at = datetime.now(timezone.utc)
                session.add(current_period)
                session.commit()

                print(f"✅ Cierre mensual completado exitosamente")
                print(f"📊 Total comisiones: {total_commissions}")
                return True

        except Exception as e:
            print(f"❌ Error en cierre mensual: {e}")
            return False

    @classmethod
    def _get_current_period(cls, session) -> Optional[Periods]:
        """
        Obtiene el período actual activo.
        Principio DRY: Método reutilizable.
        """
        try:
            current_date = get_mexico_now()

            current_period = session.exec(
                sqlmodel.select(Periods)
                .where(
                    (Periods.starts_on <= current_date) &
                    (Periods.ends_on >= current_date)
                )
            ).first()

            return current_period

        except Exception as e:
            print(f"❌ Error obteniendo período actual: {e}")
            return None

    @classmethod
    def _get_active_users(cls, session, period_id: int) -> List[Users]:
        """
        Obtiene usuarios activos (con PV > 0) en el período.
        Principio KISS: Query directo.

        Args:
            session: Sesión de base de datos
            period_id: ID del período

        Returns:
            Lista de usuarios activos
        """
        try:
            from database.orders import Orders, OrderStatus

            # Subquery: member_ids con órdenes confirmadas en el período
            active_member_ids_subquery = (
                sqlmodel.select(Orders.member_id)
                .where(
                    (Orders.period_id == period_id) &
                    (Orders.status == OrderStatus.PAYMENT_CONFIRMED.value) &
                    (Orders.total_pv > 0)
                )
                .distinct()
                .subquery()
            )

            # Query principal: obtener usuarios
            active_users = session.exec(
                sqlmodel.select(Users)
                .where(Users.member_id.in_(sqlmodel.select(active_member_ids_subquery)))
            ).all()

            return list(active_users)

        except Exception as e:
            print(f"❌ Error obteniendo usuarios activos: {e}")
            return []


def run_monthly_closure():
    """
    Función wrapper para ejecutar el cierre mensual.
    Puede ser llamada por scheduler o manualmente.
    """
    return MonthlyClosureJob.execute_monthly_closure()


# Para testing manual
if __name__ == "__main__":
    print("🧪 Ejecutando cierre mensual manualmente...")
    success = run_monthly_closure()
    if success:
        print("✅ Cierre mensual exitoso")
    else:
        print("❌ Cierre mensual falló")
