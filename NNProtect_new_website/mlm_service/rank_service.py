"""
Servicio POO para gestión automática de rangos de usuarios MLM.
Maneja asignación inicial y tracking de historial de rangos.

Principios aplicados: KISS, DRY, YAGNI, POO
"""

import reflex as rx
import sqlmodel
from typing import Optional
from datetime import datetime, timezone

from database.users import Users
from database.ranks import Ranks  
from database.user_rank_history import UserRankHistory
from database.periods import Periods
from ..utils.timezone_mx import get_mexico_now


class RankService:
    """
    Servicio POO para manejo automático de rangos de usuarios.
    Principio POO: Encapsula toda la lógica de gestión de rangos.
    """
    
    DEFAULT_RANK_ID = 1  # "Sin rango" - primer rango por defecto
    
    @classmethod
    def assign_initial_rank(cls, session, member_id: int) -> bool:
        """
        Asigna rango inicial "Sin rango" (id=1) a usuario recién registrado.
        Principio KISS: Método simple para asignación inicial.
        """
        try:
            # Verificar que el usuario existe
            user = session.exec(
                sqlmodel.select(Users).where(Users.member_id == member_id)
            ).first()
            
            if not user:
                print(f"❌ Usuario con member_id {member_id} no encontrado")
                return False
            
            # Verificar que no tenga ya un rango asignado
            existing_rank = session.exec(
                sqlmodel.select(UserRankHistory).where(
                    UserRankHistory.member_id == member_id
                )
            ).first()
            
            if existing_rank:
                print(f"⚠️  Usuario {member_id} ya tiene rango asignado")
                return False
            
            # Obtener período actual (si existe)
            current_period = cls._get_current_period(session)
            period_id = current_period.id if current_period else None
            
            # Crear registro de rango inicial
            rank_history = UserRankHistory(
                member_id=member_id,
                rank_id=cls.DEFAULT_RANK_ID,
                achieved_on=datetime.now(timezone.utc),
                period_id=period_id
            )
            
            session.add(rank_history)
            session.flush()
            
            print(f"✅ Rango inicial asignado a usuario {member_id}: Sin rango (id={cls.DEFAULT_RANK_ID})")
            return True
            
        except Exception as e:
            print(f"❌ Error asignando rango inicial a usuario {member_id}: {e}")
            return False
    
    @classmethod
    def get_user_current_rank(cls, session, member_id: int) -> Optional[int]:
        """
        Obtiene el rango actual de un usuario.
        Principio YAGNI: Solo obtiene lo necesario.
        """
        try:
            # Obtener el último rango asignado al usuario
            latest_rank = session.exec(
                sqlmodel.select(UserRankHistory)
                .where(UserRankHistory.member_id == member_id)
                .order_by(sqlmodel.desc(UserRankHistory.achieved_on))
            ).first()
            
            return latest_rank.rank_id if latest_rank else None
            
        except Exception as e:
            print(f"❌ Error obteniendo rango actual de usuario {member_id}: {e}")
            return None
    
    @classmethod
    def get_user_highest_rank(cls, session, member_id: int) -> Optional[int]:
        """
        Obtiene el rango más alto que ha alcanzado un usuario.
        Principio POO: Método específico para obtener máximo rango.
        """
        try:
            # Obtener el rango más alto (mayor ID = mayor nivel)
            highest_rank = session.exec(
                sqlmodel.select(UserRankHistory)
                .where(UserRankHistory.member_id == member_id)
                .order_by(sqlmodel.desc(UserRankHistory.rank_id))
            ).first()
            
            return highest_rank.rank_id if highest_rank else None
            
        except Exception as e:
            print(f"❌ Error obteniendo rango más alto de usuario {member_id}: {e}")
            return None
    
    @classmethod
    def promote_user_rank(cls, session, member_id: int, new_rank_id: int) -> bool:
        """
        Promueve usuario a un nuevo rango (si es mayor al actual).
        Principio DRY: Lógica centralizada para promociones.
        """
        try:
            # Verificar que el nuevo rango existe
            new_rank = session.exec(
                sqlmodel.select(Ranks).where(Ranks.id == new_rank_id)
            ).first()
            
            if not new_rank:
                print(f"❌ Rango con ID {new_rank_id} no existe")
                return False
            
            # Obtener rango actual
            current_rank_id = cls.get_user_current_rank(session, member_id)
            
            # Solo promover si el nuevo rango es mayor
            if current_rank_id and new_rank_id <= current_rank_id:
                print(f"⚠️  Usuario {member_id} ya tiene rango igual o mayor ({current_rank_id})")
                return False
            
            # Obtener período actual
            current_period = cls._get_current_period(session)
            period_id = current_period.id if current_period else None
            
            # Crear nuevo registro de rango
            rank_history = UserRankHistory(
                member_id=member_id,
                rank_id=new_rank_id,
                achieved_on=datetime.now(timezone.utc),
                period_id=period_id
            )
            
            session.add(rank_history)
            session.flush()
            
            print(f"✅ Usuario {member_id} promovido a rango {new_rank.name} (id={new_rank_id})")
            return True
            
        except Exception as e:
            print(f"❌ Error promoviendo usuario {member_id} a rango {new_rank_id}: {e}")
            return False
    
    @classmethod
    def get_rank_progression_history(cls, session, member_id: int) -> list:
        """
        Obtiene historial completo de progresión de rangos del usuario.
        Principio YAGNI: Solo para reportes específicos.
        """
        try:
            # Query separado para evitar problemas de JOIN en SQLModel
            rank_history = session.exec(
                sqlmodel.select(UserRankHistory)
                .where(UserRankHistory.member_id == member_id)
                .order_by(sqlmodel.desc(UserRankHistory.achieved_on))
            ).all()
            
            # Obtener nombres de rangos por separado
            result = []
            for history in rank_history:
                rank = session.exec(
                    sqlmodel.select(Ranks).where(Ranks.id == history.rank_id)
                ).first()
                
                result.append({
                    "rank_id": history.rank_id,
                    "rank_name": rank.name if rank else "Desconocido",
                    "achieved_on": history.achieved_on,
                    "period_id": history.period_id
                })
            
            return result
            
        except Exception as e:
            print(f"❌ Error obteniendo historial de rangos de usuario {member_id}: {e}")
            return []
    
    @classmethod
    def _get_current_period(cls, session) -> Optional[Periods]:
        """
        Obtiene el período actual activo.
        Principio KISS: Método helper simple.
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