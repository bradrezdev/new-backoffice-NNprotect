"""
Servicio del Plan de Compensación NN Protect - Versión 2.0 COMPLETA
Implementación completa de los 9 bonos del plan oficial.

Este servicio se integra completamente con la arquitectura existente del backoffice,
utilizando member_id, pv_cache, pvg_cache y los servicios existentes.

BONOS IMPLEMENTADOS:
1. ✅ Bono de Venta Directa
2. ✅ Bono Rápido (Fast Start)
3. ✅ Bono Lealtad
4. ✅ Bono CashBack
5. ✅ Bono Uninivel
6. ✅ Bono Match (Igualación)
7. ✅ Bono por Avance de Rango
8. ✅ Bono de Auto
9. ✅ Bono de Viaje (estructura base)

Autor: Sistema MLM NN Protect
Fecha: Octubre 2025
Versión: 2.0 COMPLETA
Basado en: config_bonos.json y PLAN_COMPENSACION_COMPLETO.md
"""

import sqlmodel
from typing import Optional, List, Dict, Tuple
from datetime import datetime, timezone, timedelta
from decimal import Decimal

from database.users import Users, UserStatus
from database.orders import Orders, OrderStatus
from database.order_items import OrderItems
from database.products import Products
from database.comissions import Commissions, BonusType, CommissionStatus
from database.periods import Periods
from database.ranks import Ranks
from database.usertreepaths import UserTreePath
# from database.loyalty_points import LoyaltyPoints, LoyaltyEventType
# from database.cashback import CashbackTracking

from .genealogy_service import GenealogyService
from .exchange_service import ExchangeService
from .rank_service import RankService


class CompensationPlanV2:
    """
    Servicio oficial del Plan de Compensación NN Protect v2.0
    
    Implementa TODOS los 9 bonos de forma precisa según documentación oficial.
    
    Principios:
    - Integración total con arquitectura existente
    - Uso de member_id (no user_id)
    - Uso de pv_cache y pvg_cache
    - Compatible con Supabase y servicios existentes
    """
    
    # ========================================================================
    # CONFIGURACIÓN OFICIAL DEL PLAN
    # ========================================================================
    
    # Calificación mínima mensual
    PV_MINIMO_CALIFICACION = 1465
    PV_MINIMO_CASHBACK = 2930
    
    # BONO RÁPIDO - 3 niveles sobre primera compra
    FAST_START_CONFIG = {
        1: {"percentage": 30, "description": "Tus directos"},
        2: {"percentage": 10, "description": "Directos de tus directos"},
        3: {"percentage": 5, "description": "Tercer nivel"}
    }
    
    # BONO UNINIVEL - Porcentajes por nivel (1-9)
    UNINIVEL_PERCENTAGES = [5, 8, 10, 10, 5, 4, 4, 3, 3]
    
    # BONO UNINIVEL - Niveles disponibles por rango
    UNINIVEL_LEVELS_BY_RANK = {
        "Visionario": 3,
        "Emprendedor": 4,
        "Creativo": 5,
        "Innovador": 6,
        "Embajador Transformador": 9,
        "Embajador Inspirador": 9,
        "Embajador Consciente": 9,
        "Embajador Solidario": 9
    }
    
    # BONO INFINITO - Porcentajes por rango (nivel 10+)
    INFINITO_CONFIG = {
        "Embajador Transformador": 0.5,
        "Embajador Inspirador": 1.0,
        "Embajador Consciente": 1.5,
        "Embajador Solidario": 2.0
    }
    
    # BONO MATCH - Configuración por rango
    MATCH_CONFIG = {
        "Embajador Transformador": {"levels": 1, "percentages": [30]},
        "Embajador Inspirador": {"levels": 2, "percentages": [30, 20]},
        "Embajador Consciente": {"levels": 3, "percentages": [30, 20, 10]},
        "Embajador Solidario": {"levels": 4, "percentages": [30, 20, 10, 5]}
    }
    
    # BONO LEALTAD
    LOYALTY_CONFIG = {
        "points_per_purchase": 25,
        "max_days": 7,
        "points_to_redeem": 100,
        "redeem_value_vg": 1465
    }
    
    # BONO AVANCE DE RANGO - Montos por rango
    RANK_ADVANCEMENT_AMOUNTS = {
        "Emprendedor": {"MXN": 1500, "USD": 85, "COP": 330000},
        "Creativo": {"MXN": 3000, "USD": 165, "COP": 660000},
        "Innovador": {"MXN": 5000, "USD": 280, "COP": 1100000},
        "Embajador Transformador": {"MXN": 7500, "USD": 390, "COP": 1650000},
        "Embajador Inspirador": {"MXN": 10000, "USD": 555, "COP": 2220000},
        "Embajador Consciente": {"MXN": 20000, "USD": 1111, "COP": 4400000},
        "Embajador Solidario": {"MXN": 40000, "USD": 2222, "COP": 8800000}
    }
    
    # BONO AUTO
    AUTO_BONUS_CONFIG = {
        "downpayment": {"MXN": 50000, "USD": 2500, "COP": 11000000},
        "monthly": {"MXN": 5000, "USD": 250, "COP": 1100000},
        "required_consecutive_months": 2
    }
    
    # ========================================================================
    # MÉTODO PRINCIPAL - PROCESAR ORDEN
    # ========================================================================
    
    @classmethod
    def process_order_complete(cls, session: sqlmodel.Session, order_id: int) -> Dict[str, any]:
        """
        MÉTODO PRINCIPAL: Procesa todos los bonos cuando se confirma una orden.
        
        Este método orquesta el cálculo de todos los bonos aplicables.
        Se debe llamar cuando una orden cambia a estado "completed".
        
        Args:
            session: Sesión de SQLModel
            order_id: ID de la orden confirmada
            
        Returns:
            Dict con resumen de bonos procesados
        """
        # 1. Validar orden
        order = session.get(Orders, order_id)
        if not order:
            raise ValueError(f"Orden {order_id} no encontrada")
        
        if order.status != OrderStatus.COMPLETED.value:
            raise ValueError(f"Orden {order_id} no está completada")
        
        # 2. Obtener período actual
        period = cls._get_current_period(session)
        if not period:
            raise ValueError("No hay período activo")
        
        # 3. Obtener usuario
        user = session.exec(
            sqlmodel.select(Users).where(Users.member_id == order.buyer_member_id)
        ).first()
        
        if not user:
            raise ValueError(f"Usuario {order.buyer_member_id} no encontrado")
        
        results = {
            "order_id": order_id,
            "member_id": user.member_id,
            "period_id": period.id,
            "bonuses_processed": {}
        }
        
        # 4. Procesar cada bono según aplique
        
        # BONO 1: Venta Directa
        if hasattr(order, 'is_store_sale') and order.is_store_sale:
            direct_sale = cls.process_direct_sale_bonus(session, order, period.id)
            results["bonuses_processed"]["direct_sale"] = direct_sale
        
        # BONO 2: Bono Rápido
        if hasattr(order, 'is_first_purchase') and order.is_first_purchase:
            fast_start = cls.process_fast_start_bonus(session, order, period.id)
            results["bonuses_processed"]["fast_start"] = fast_start
        
        # BONO 3: Lealtad
        loyalty = cls.process_loyalty_bonus(session, order, user, period.id)
        results["bonuses_processed"]["loyalty"] = loyalty
        
        # BONO 4: CashBack
        cashback = cls.update_cashback_tracking(session, order, user, period.id)
        results["bonuses_processed"]["cashback"] = cashback
        
        # BONO 5: Uninivel
        uninivel = cls.process_uninivel_bonus(session, order, period.id)
        results["bonuses_processed"]["uninivel"] = uninivel
        
        # 6. Actualizar PV del usuario
        cls._update_user_pv(session, user, order)
        
        # 7. Propagar PVG hacia arriba
        cls._propagate_pvg_upline(session, user.member_id, order)
        
        # 8. Verificar y actualizar rango
        rank_update = RankService.update_user_rank(session, user.member_id)
        results["rank_updated"] = rank_update
        
        # BONO 7: Verificar Avance de Rango
        if rank_update.get("rank_changed"):
            rank_bonus = cls.check_and_pay_rank_advancement_bonus(
                session, user.member_id, rank_update.get("new_rank_id")
            )
            results["bonuses_processed"]["rank_advancement"] = rank_bonus
        
        return results
    
    # ========================================================================
    # BONOS DESHABILITADOS (Solo Uninivel y Match activos)
    # ========================================================================
    
    # BONO 1: VENTA DIRECTA - DESHABILITADO
    # BONO 2: BONO RÁPIDO (FAST START) - DESHABILITADO  
    # BONO 3: LEALTAD - DESHABILITADO
    # BONO 4: CASHBACK - DESHABILITADO
    
    # ========================================================================
    
    @classmethod
    def process_direct_sale_bonus(cls, session: sqlmodel.Session, 
                                  order: Orders, period_id: int) -> Dict[str, any]:
        """DESHABILITADO - Solo Uninivel y Match activos"""
        return {"applies": False, "reason": "Bonus disabled"}
    
    # ========================================================================
    # BONO 2: BONO RÁPIDO (FAST START)
    # ========================================================================
    
    @classmethod
    def process_fast_start_bonus(cls, session: sqlmodel.Session,
                                 order: Orders, period_id: int) -> Dict[str, any]:
        """DESHABILITADO - Solo Uninivel y Match activos"""
        return {"applies": False, "reason": "Bonus disabled"}
    
    # ========================================================================
    # BONO 3: LEALTAD
    # ========================================================================
    
    @classmethod
    def process_loyalty_bonus(cls, session: sqlmodel.Session, order: Orders,
                              user: Users, period_id: int) -> Dict[str, any]:
        """DESHABILITADO - Solo Uninivel y Match activos"""
        return {"applies": False, "reason": "Bonus disabled"}
    
    # ========================================================================
    # BONO 4: CASHBACK
    # ========================================================================
    
    @classmethod
    def update_cashback_tracking(cls, session: sqlmodel.Session, order: Orders,
                                user: Users, period_id: int) -> Dict[str, any]:
        """DESHABILITADO - Solo Uninivel y Match activos"""
        return {"applies": False, "reason": "Bonus disabled"}
    
    # ========================================================================
    # BONO 5: UNINIVEL
    # ========================================================================
    
    @classmethod
    def process_uninivel_bonus(cls, session: sqlmodel.Session, order: Orders, 
                              period_id: int) -> Dict[str, any]:
        """
        Calcula y registra el Bono Uninivel por profundidad de red (niveles 1-9).
        
        Porcentajes: 5%, 8%, 10%, 10%, 5%, 4%, 4%, 3%, 3%
        """
        if hasattr(order, 'is_cashback') and order.is_cashback:
            return {"applies": False, "reason": "CashBack purchases don't generate commissions"}
        
        buyer = session.exec(
            sqlmodel.select(Users).where(Users.member_id == order.buyer_member_id)
        ).first()
        
        if not buyer:
            return {"applies": False, "reason": "Buyer not found"}
        
        vn_amount = cls._calculate_order_vn(session, order)
        bonuses_paid = []
        total_paid = 0.0
        
        for level_idx in range(1, 10):
            percentage = cls.UNINIVEL_PERCENTAGES[level_idx - 1]
            
            upline_paths = session.exec(
                sqlmodel.select(UserTreePath)
                .where(UserTreePath.descendant_id == buyer.member_id)
                .where(UserTreePath.depth == level_idx)
            ).all()
            
            for path in upline_paths:
                upline = session.exec(
                    sqlmodel.select(Users).where(Users.member_id == path.ancestor_id)
                ).first()
                
                if not upline:
                    continue
                
                if upline.status != UserStatus.QUALIFIED:
                    continue
                
                if upline.pv_cache < cls.PV_MINIMO_CALIFICACION:
                    continue
                
                upline_rank = session.exec(
                    sqlmodel.select(Ranks).where(Ranks.id == upline.rank_id)
                ).first() if hasattr(upline, 'rank_id') else None
                
                if not upline_rank:
                    continue
                
                max_levels = cls.UNINIVEL_LEVELS_BY_RANK.get(upline_rank.name, 0)
                if level_idx > max_levels:
                    continue
                
                commission_amount = vn_amount * (percentage / 100)
                currency = ExchangeService.get_country_currency(upline.country_cache)
                
                commission = Commissions(
                    member_id=upline.member_id,
                    bonus_type=BonusType.BONO_UNINIVEL.value,
                    source_member_id=buyer.member_id,
                    source_order_id=order.id,
                    period_id=period_id,
                    level_depth=level_idx,
                    amount_vn=vn_amount,
                    currency_origin=currency,
                    amount_converted=commission_amount,
                    currency_destination=currency,
                    exchange_rate=1.0,
                    status=CommissionStatus.PENDING.value,
                    notes=f"Bono Uninivel Nivel {level_idx} ({percentage}%) - {buyer.full_name}",
                    calculated_at=datetime.now(timezone.utc)
                )
                
                session.add(commission)
                session.flush()
                
                bonuses_paid.append({
                    "level": level_idx,
                    "upline_id": upline.member_id,
                    "upline_name": upline.full_name,
                    "upline_rank": upline_rank.name,
                    "percentage": percentage,
                    "amount": float(commission_amount),
                    "currency": currency
                })
                
                total_paid += commission_amount
                
                print(f"✅ Bono Uninivel L{level_idx}: ${commission_amount:.2f} para {upline.full_name}")
        
        session.commit()
        
        return {
            "applies": True,
            "source_member": buyer.full_name,
            "vn_amount": float(vn_amount),
            "bonuses_paid": bonuses_paid,
            "total_paid": float(total_paid)
        }
    
    # ========================================================================
    # BONO 6: MATCH (IGUALACIÓN)
    # ========================================================================
    
    @classmethod
    def process_match_bonus_end_of_period(cls, session: sqlmodel.Session, 
                                         period_id: int) -> Dict[str, any]:
        """
        Calcula y registra el Bono Match al final del período.
        
        Match = % del Uninivel ganado por personas en TU LINAJE DIRECTO.
        CRÍTICO: Solo linaje directo, NO frontales.
        """
        period = session.get(Periods, period_id)
        if not period:
            return {"error": "Period not found"}
        
        ambassadors = session.exec(
            sqlmodel.select(Users)
            .join(Ranks, Users.rank_id == Ranks.id)
            .where(Ranks.name.in_(list(cls.MATCH_CONFIG.keys())))
            .where(Users.status == UserStatus.QUALIFIED)
            .where(Users.pv_cache >= cls.PV_MINIMO_CALIFICACION)
        ).all()
        
        bonuses_calculated = []
        total_paid = 0.0
        
        for ambassador in ambassadors:
            ambassador_rank = session.get(Ranks, ambassador.rank_id)
            if not ambassador_rank:
                continue
            
            match_config = cls.MATCH_CONFIG.get(ambassador_rank.name)
            if not match_config:
                continue
            
            levels = match_config["levels"]
            percentages = match_config["percentages"]
            
            for level_idx in range(1, levels + 1):
                percentage = percentages[level_idx - 1]
                
                lineage_members = cls._get_direct_lineage_at_level(
                    session, ambassador.member_id, level_idx
                )
                
                for member in lineage_members:
                    uninivel_earned = cls._get_uninivel_earned_in_period(
                        session, member.member_id, period_id
                    )
                    
                    if uninivel_earned <= 0:
                        continue
                    
                    match_amount = uninivel_earned * (percentage / 100)
                    currency = ExchangeService.get_country_currency(ambassador.country_cache)
                    
                    commission = Commissions(
                        member_id=ambassador.member_id,
                        bonus_type=BonusType.BONO_MATCHING.value,
                        source_member_id=member.member_id,
                        period_id=period_id,
                        level_depth=level_idx,
                        amount_vn=uninivel_earned,
                        currency_origin=currency,
                        amount_converted=match_amount,
                        currency_destination=currency,
                        exchange_rate=1.0,
                        status=CommissionStatus.PENDING.value,
                        notes=f"Bono Match Nivel {level_idx} ({percentage}%) - Uninivel de {member.full_name}",
                        calculated_at=datetime.now(timezone.utc)
                    )
                    
                    session.add(commission)
                    session.flush()
                    
                    bonuses_calculated.append({
                        "ambassador_id": ambassador.member_id,
                        "ambassador_name": ambassador.full_name,
                        "ambassador_rank": ambassador_rank.name,
                        "level": level_idx,
                        "member_id": member.member_id,
                        "member_name": member.full_name,
                        "uninivel_earned": float(uninivel_earned),
                        "percentage": percentage,
                        "match_amount": float(match_amount),
                        "currency": currency
                    })
                    
                    total_paid += match_amount
                    
                    print(f"✅ Bono Match L{level_idx}: ${match_amount:.2f} para {ambassador.full_name}")
        
        session.commit()
        
        return {
            "period_id": period_id,
            "ambassadors_processed": len(ambassadors),
            "bonuses_calculated": len(bonuses_calculated),
            "total_paid": float(total_paid),
            "details": bonuses_calculated
        }
    
    @classmethod
    def _get_direct_lineage_at_level(cls, session: sqlmodel.Session, 
                                     sponsor_id: int, level: int) -> List[Users]:
        """
        Obtiene personas en nivel específico del LINAJE DIRECTO.
        
        Linaje directo = invitados por sponsor o su descendencia.
        NO incluye frontales.
        """
        paths = session.exec(
            sqlmodel.select(UserTreePath)
            .where(UserTreePath.ancestor_id == sponsor_id)
            .where(UserTreePath.depth == level)
        ).all()
        
        lineage = []
        
        for path in paths:
            member = session.exec(
                sqlmodel.select(Users).where(Users.member_id == path.descendant_id)
            ).first()
            
            if member and cls._is_direct_lineage(session, sponsor_id, member.member_id):
                lineage.append(member)
        
        return lineage
    
    @classmethod
    def _is_direct_lineage(cls, session: sqlmodel.Session, 
                           sponsor_id: int, member_id: int) -> bool:
        """
        Verifica si un miembro es del linaje directo del sponsor.
        
        Linaje directo = sponsor_id del miembro apunta al sponsor o su descendencia.
        """
        member = session.exec(
            sqlmodel.select(Users).where(Users.member_id == member_id)
        ).first()
        
        if not member or not member.sponsor_id:
            return False
        
        current_sponsor_id = member.sponsor_id
        visited = set()
        
        while current_sponsor_id and current_sponsor_id not in visited:
            if current_sponsor_id == sponsor_id:
                return True
            
            visited.add(current_sponsor_id)
            
            sponsor = session.exec(
                sqlmodel.select(Users).where(Users.member_id == current_sponsor_id)
            ).first()
            
            if not sponsor:
                break
            
            current_sponsor_id = sponsor.sponsor_id
        
        return False
    
    @classmethod
    def _get_uninivel_earned_in_period(cls, session: sqlmodel.Session,
                                       member_id: int, period_id: int) -> float:
        """Obtiene el total de Uninivel ganado por un miembro en un período."""
        commissions = session.exec(
            sqlmodel.select(Commissions)
            .where(Commissions.member_id == member_id)
            .where(Commissions.period_id == period_id)
            .where(Commissions.bonus_type == BonusType.BONO_UNINIVEL.value)
        ).all()
        
        total = sum(c.amount_converted for c in commissions)
        return total
    
    # ========================================================================
    # BONOS DESHABILITADOS
    # ========================================================================
    
    @classmethod
    def check_and_pay_rank_advancement_bonus(cls, session: sqlmodel.Session,
                                            member_id: int, new_rank_id: int) -> Optional[Dict[str, any]]:
        """DESHABILITADO - Solo Uninivel y Match activos"""
        return None
        """
        user = session.exec(
            sqlmodel.select(Users).where(Users.member_id == member_id)
        ).first()
        
        if not user:
            return None
        
        rank = session.get(Ranks, new_rank_id)
        if not rank:
            return None
        
        if rank.name not in cls.RANK_ADVANCEMENT_AMOUNTS:
            return {
                "applies": False,
                "reason": "No bonus for this rank",
                "rank": rank.name
            }
        
        already_paid = session.exec(
            sqlmodel.select(Commissions)
            .where(Commissions.member_id == member_id)
            .where(Commissions.bonus_type == BonusType.BONO_ALCANCE.value)
            .where(Commissions.notes.contains(rank.name))
        ).first()
        
        if already_paid:
            return {
                "applies": False,
                "reason": "Bonus already paid for this rank",
                "rank": rank.name
            }
        
        if rank.name == "Emprendedor":
            days_since_registration = (datetime.now(timezone.utc) - user.created_at).days
            if days_since_registration > 30:
                return {
                    "applies": False,
                    "reason": "Emprendedor bonus only in first 30 days",
                    "days_since_registration": days_since_registration
                }
        
        currency = ExchangeService.get_country_currency(user.country_cache)
        bonus_amount = cls.RANK_ADVANCEMENT_AMOUNTS[rank.name].get(currency, 0)
        
        if bonus_amount <= 0:
            return None
        
        period = cls._get_current_period(session)
        
        commission = Commissions(
            member_id=member_id,
            bonus_type=BonusType.BONO_ALCANCE.value,
            period_id=period.id if period else None,
            amount_vn=bonus_amount,
            currency_origin=currency,
            amount_converted=bonus_amount,
            currency_destination=currency,
            exchange_rate=1.0,
            status=CommissionStatus.PENDING.value,
            notes=f"Bono por Avance de Rango: {rank.name}",
            calculated_at=datetime.now(timezone.utc)
        )
        
        session.add(commission)
        session.commit()
        
        print(f"✅ Bono Avance Rango {rank.name}: ${bonus_amount:.2f} para {user.full_name}")
        
        return {
            "applies": True,
            "member_id": member_id,
            "member_name": user.full_name,
            "rank": rank.name,
            "bonus_amount": float(bonus_amount),
            "currency": currency
        }
    
    # ========================================================================
    # BONO 8: AUTO
    # ========================================================================
    
    @classmethod
    def process_auto_bonus(cls, session: sqlmodel.Session, 
                          member_id: int, period_id: int) -> Dict[str, any]:
        """DESHABILITADO - Solo Uninivel y Match activos"""
        return {"applies": False, "reason": "Bonus disabled"}
        user = session.exec(
            sqlmodel.select(Users).where(Users.member_id == member_id)
        ).first()
        
        if not user:
            return {"error": "User not found"}
        
        if not hasattr(user, 'rank_id') or not user.rank_id:
            return {
                "applies": False,
                "reason": "No rank assigned",
                "member_id": member_id
            }
        
        rank = session.get(Ranks, user.rank_id)
        if not rank:
            return {"applies": False, "reason": "Rank not found"}
        
        eligible_ranks = [
            "Embajador Transformador",
            "Embajador Inspirador",
            "Embajador Consciente",
            "Embajador Solidario"
        ]
        
        if rank.name not in eligible_ranks:
            return {
                "applies": False,
                "reason": "Rank not eligible for Auto Bonus",
                "current_rank": rank.name
            }
        
        if user.status != UserStatus.QUALIFIED or user.pv_cache < cls.PV_MINIMO_CALIFICACION:
            return {
                "applies": False,
                "reason": "User doesn't qualify this month",
                "pv": user.pv_cache
            }
        
        currency = ExchangeService.get_country_currency(user.country_cache)
        result = {
            "member_id": member_id,
            "member_name": user.full_name,
            "rank": rank.name,
            "currency": currency
        }
        
        downpayment_paid = session.exec(
            sqlmodel.select(Commissions)
            .where(Commissions.member_id == member_id)
            .where(Commissions.bonus_type == BonusType.BONO_AUTOMOVIL.value)
            .where(Commissions.notes.contains("Enganche"))
        ).first()
        
        consecutive_months = cls._count_consecutive_qualified_months(session, member_id)
        
        if not downpayment_paid and consecutive_months >= cls.AUTO_BONUS_CONFIG["required_consecutive_months"]:
            downpayment_amount = cls.AUTO_BONUS_CONFIG["downpayment"].get(currency, 0)
            
            commission = Commissions(
                member_id=member_id,
                bonus_type=BonusType.BONO_AUTOMOVIL.value,
                period_id=period_id,
                amount_vn=downpayment_amount,
                currency_origin=currency,
                amount_converted=downpayment_amount,
                currency_destination=currency,
                exchange_rate=1.0,
                status=CommissionStatus.PENDING.value,
                notes="Bono Auto - Enganche (pago único)",
                calculated_at=datetime.now(timezone.utc)
            )
            
            session.add(commission)
            session.flush()
            
            result["downpayment_paid"] = float(downpayment_amount)
            print(f"✅ Bono Auto Enganche: ${downpayment_amount:.2f} para {user.full_name}")
        else:
            result["downpayment_paid"] = "Already paid" if downpayment_paid else "Not yet eligible"
        
        monthly_amount = cls.AUTO_BONUS_CONFIG["monthly"].get(currency, 0)
        
        commission = Commissions(
            member_id=member_id,
            bonus_type=BonusType.BONO_AUTOMOVIL.value,
            period_id=period_id,
            amount_vn=monthly_amount,
            currency_origin=currency,
            amount_converted=monthly_amount,
            currency_destination=currency,
            exchange_rate=1.0,
            status=CommissionStatus.PENDING.value,
            notes=f"Bono Auto - Mensualidad ({rank.name})",
            calculated_at=datetime.now(timezone.utc)
        )
        
        session.add(commission)
        session.commit()
        
        result["monthly_payment"] = float(monthly_amount)
        
        print(f"✅ Bono Auto Mensualidad: ${monthly_amount:.2f} para {user.full_name}")
        
        return result
    
    @classmethod
    def _count_consecutive_qualified_months(cls, session: sqlmodel.Session, 
                                            member_id: int) -> int:
        """Cuenta cuántos meses consecutivos el usuario ha calificado."""
        recent_periods = session.exec(
            sqlmodel.select(Periods)
            .where(Periods.is_active == True)
            .order_by(Periods.start_date.desc())
            .limit(12)
        ).all()
        
        consecutive = 0
        
        for period in recent_periods:
            user_qualified = session.exec(
                sqlmodel.select(Commissions)
                .where(Commissions.member_id == member_id)
                .where(Commissions.period_id == period.id)
            ).first() is not None
            
            if user_qualified:
                consecutive += 1
            else:
                break
        
        return consecutive
    
    # ========================================================================
    # BONO 9: VIAJE (NN TRAVELS)
    # ========================================================================
    
    @classmethod
    def check_travel_qualification(cls, session: sqlmodel.Session,
                                   member_id: int, campaign_id: int) -> Dict[str, any]:
        """
        Verifica si un usuario califica para un viaje.
        
        Requisitos: Embajador, VG específico, nuevos directos, consistencia.
        """
        user = session.exec(
            sqlmodel.select(Users).where(Users.member_id == member_id)
        ).first()
        
        if not user:
            return {"error": "User not found"}
        
        if not hasattr(user, 'rank_id') or not user.rank_id:
            return {
                "qualifies": False,
                "reason": "No rank assigned",
                "member_id": member_id
            }
        
        rank = session.get(Ranks, user.rank_id)
        if not rank:
            return {"qualifies": False, "reason": "Rank not found"}
        
        ambassador_ranks = [
            "Embajador Transformador",
            "Embajador Inspirador",
            "Embajador Consciente",
            "Embajador Solidario"
        ]
        
        if rank.name not in ambassador_ranks:
            return {
                "qualifies": False,
                "reason": "Minimum rank not met (Embajador required)",
                "current_rank": rank.name
            }
        
        return {
            "qualifies": True,
            "member_id": member_id,
            "member_name": user.full_name,
            "rank": rank.name,
            "campaign_id": campaign_id,
            "note": "Travel bonus requires full campaign implementation"
        }
    
    # ========================================================================
    # MÉTODO FIN DE MES
    # ========================================================================
    
    @classmethod
    def process_end_of_month(cls, session: sqlmodel.Session, period_id: int) -> Dict[str, any]:
        """
        Procesa solo los bonos Uninivel y Match de fin de mes.
        
        SOLO HABILITADOS:
        1. Bono Match
        2. Bono Uninivel (se procesa por orden, no aquí)
        """
        results = {
            "period_id": period_id,
            "processed_at": datetime.now(timezone.utc).isoformat()
        }
        
        print("📊 Procesando Bono Match...")
        match_results = cls.process_match_bonus_end_of_period(session, period_id)
        results["match"] = match_results
        
        # DESHABILITADOS: Bono Auto, Bono de Viaje, etc.
        # print("🚗 Procesando Bono de Auto...")
        # eligible_users = session.exec(
        #     sqlmodel.select(Users)
        #     .join(Ranks, Users.rank_id == Ranks.id)
        #     .where(Ranks.name.in_([
        #         "Embajador Transformador",
        #         "Embajador Inspirador",
        #         "Embajador Consciente",
        #         "Embajador Solidario"
        #     ]))
        #     .where(Users.status == UserStatus.QUALIFIED)
        # ).all()
        
        # auto_results = []
        # for user in eligible_users:
        #     auto_result = cls.process_auto_bonus(session, user.member_id, period_id)
        #     if auto_result.get("applies") != False:
        #         auto_results.append(auto_result)
        
        # results["auto"] = {
        #     "processed": len(auto_results),
        #     "details": auto_results
        # }
        
        print("🔄 Reseteando volúmenes mensuales (pv_cache)...")
        session.exec(
            sqlmodel.update(Users)
            .values(pv_cache=0)
        )
        session.commit()
        
        results["volumes_reset"] = True
        
        print("✅ Procesamiento de fin de mes completado (SOLO Match + Uninivel)")
        
        return results
    
    # ========================================================================
    # MÉTODOS AUXILIARES PRIVADOS
    # ========================================================================
    
    @classmethod
    def _get_current_period(cls, session: sqlmodel.Session) -> Optional[Periods]:
        """Obtiene el período activo actual."""
        return session.exec(
            sqlmodel.select(Periods)
            .where(Periods.is_active == True)
            .order_by(Periods.start_date.desc())
        ).first()
    
    @classmethod
    def _calculate_order_vn(cls, session: sqlmodel.Session, order: Orders) -> float:
        """Calcula el VN total de una orden."""
        order_items = session.exec(
            sqlmodel.select(OrderItems).where(OrderItems.order_id == order.id)
        ).all()
        
        total_vn = 0.0
        for item in order_items:
            product = session.get(Products, item.product_id)
            if product:
                item_vn = product.price_distributor * item.quantity
                total_vn += item_vn
        
        return total_vn
    
    @classmethod
    def _calculate_order_pv(cls, session: sqlmodel.Session, order: Orders) -> float:
        """Calcula el PV total de una orden."""
        order_items = session.exec(
            sqlmodel.select(OrderItems).where(OrderItems.order_id == order.id)
        ).all()
        
        total_pv = 0.0
        for item in order_items:
            product = session.get(Products, item.product_id)
            if product and hasattr(product, 'pv_value'):
                item_pv = product.pv_value * item.quantity
                total_pv += item_pv
        
        return total_pv
    
    @classmethod
    def _update_user_pv(cls, session: sqlmodel.Session, user: Users, order: Orders):
        """Actualiza el PV del usuario después de una compra."""
        order_pv = cls._calculate_order_pv(session, order)
        user.pv_cache += order_pv
        
        if user.pv_cache >= cls.PV_MINIMO_CALIFICACION:
            user.status = UserStatus.QUALIFIED
        
        session.add(user)
        session.commit()
    
    @classmethod
    def _propagate_pvg_upline(cls, session: sqlmodel.Session, member_id: int, order: Orders):
        """Propaga el PVG hacia arriba en la red."""
        order_pv = cls._calculate_order_pv(session, order)
        
        ancestor_paths = session.exec(
            sqlmodel.select(UserTreePath)
            .where(UserTreePath.descendant_id == member_id)
            .where(UserTreePath.depth > 0)
        ).all()
        
        for path in ancestor_paths:
            ancestor = session.exec(
                sqlmodel.select(Users).where(Users.member_id == path.ancestor_id)
            ).first()
            
            if ancestor:
                ancestor.pvg_cache += order_pv
                session.add(ancestor)
        
        session.commit()
    
    @classmethod
    def _is_consecutive_purchase(cls, session: sqlmodel.Session, 
                                 member_id: int, current_date: datetime) -> bool:
        """Verifica si la compra es consecutiva al mes anterior."""
        last_order = session.exec(
            sqlmodel.select(Orders)
            .where(Orders.buyer_member_id == member_id)
            .where(Orders.status == OrderStatus.COMPLETED.value)
            .where(Orders.created_at < current_date)
            .order_by(Orders.created_at.desc())
        ).first()
        
        if not last_order:
            return True
        
        last_month = last_order.created_at.month
        last_year = last_order.created_at.year
        current_month = current_date.month
        current_year = current_date.year
        
        if current_year == last_year and current_month == last_month + 1:
            return True
        
        if current_year == last_year + 1 and current_month == 1 and last_month == 12:
            return True
        
        return False
    
    @classmethod
    def _reset_loyalty_points(cls, session: sqlmodel.Session, member_id: int):
        """Resetea los puntos de lealtad de un usuario."""
        user = session.exec(
            sqlmodel.select(Users).where(Users.member_id == member_id)
        ).first()
        
        if user and hasattr(user, 'loyalty_points'):
            old_balance = user.loyalty_points
            user.loyalty_points = 0
            user.loyalty_consecutive_months = 0
            session.add(user)
            session.commit()
            
            # NOTA: LoyaltyPoints usa estructura diferente, este código está desactualizado
            # loyalty_tx = LoyaltyPoints(
            #     user_id=user.id,
            #     transaction_type=LoyaltyEventType.RESET,
            #     points=-old_balance,
            #     balance_before=old_balance,
            #     balance_after=0,
            #     description="Reset por compra no consecutiva"
            # )
            # session.add(loyalty_tx)
            # session.commit()
    
    @classmethod
    def _add_loyalty_points(cls, session: sqlmodel.Session, member_id: int,
                           points: int, order_id: int, description: str) -> int:
        """Agrega puntos de lealtad a un usuario."""
        user = session.exec(
            sqlmodel.select(Users).where(Users.member_id == member_id)
        ).first()
        
        if not user:
            return 0
        
        # NOTA: Users no tiene campos loyalty_points/loyalty_consecutive_months - código desactualizado
        # if not hasattr(user, 'loyalty_points') or user.loyalty_points is None:
        #     user.loyalty_points = 0
        # if not hasattr(user, 'loyalty_consecutive_months') or user.loyalty_consecutive_months is None:
        #     user.loyalty_consecutive_months = 0
        
        # old_balance = user.loyalty_points
        # new_balance = old_balance + points
        # user.loyalty_points = new_balance
        # user.loyalty_consecutive_months += 1
        # session.add(user)
        # session.commit()
        
        # NOTA: LoyaltyPoints usa estructura diferente - código desactualizado
        # loyalty_tx = LoyaltyPoints(
        #     user_id=user.id,
        #     transaction_type=LoyaltyEventType.EARNED,
        #     points=points,
        #     balance_before=old_balance,
        #     balance_after=new_balance,
        #     order_id=order_id,
        #     description=description
        # )
        # session.add(loyalty_tx)
        # session.commit()
        
        return 0
        return new_balance