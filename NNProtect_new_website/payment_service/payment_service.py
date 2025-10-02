"""
Servicio POO para procesamiento de pagos.
Orquesta el flujo completo: pago -> confirmación -> actualización PV -> comisiones.

Principios aplicados: KISS, DRY, YAGNI, POO
"""

import sqlmodel
from typing import Optional
from datetime import datetime, timezone

from database.orders import Orders, OrderStatus
from database.wallet import Wallets
from ..mlm_service.wallet_service import WalletService
from ..mlm_service.pv_update_service import PVUpdateService
from ..mlm_service.commission_service import CommissionService
from ..mlm_service.period_service import PeriodService


class PaymentService:
    """
    Servicio POO para procesamiento de pagos.
    Principio POO: Encapsula toda la lógica de pagos y confirmación.
    """

    @classmethod
    def process_wallet_payment(
        cls,
        session,
        order_id: int,
        member_id: int
    ) -> dict:
        """
        Procesa pago de orden con wallet virtual.

        Flujo completo:
        1. Validar orden y estado
        2. Validar balance de wallet
        3. Debitar monto de wallet
        4. Confirmar pago de orden (cambiar estado + timestamp)
        5. Actualizar PV del comprador y ancestros
        6. Disparar cálculo de comisiones

        Principio: Atomicidad - todo o nada.

        Args:
            session: Sesión de base de datos
            order_id: ID de la orden a pagar
            member_id: ID del usuario que paga

        Returns:
            Dict con:
            - success: bool
            - message: str
            - order_id: int (si exitoso)
        """
        try:
            # 1. Validar orden con ROW-LEVEL LOCK (evita double-payment)
            order = session.exec(
                sqlmodel.select(Orders)
                .where(Orders.id == order_id)
                .with_for_update()  # 🔒 Bloqueo pesimista
            ).first()

            if not order:
                return {
                    "success": False,
                    "message": f"Orden {order_id} no encontrada"
                }

            if order.member_id != member_id:
                return {
                    "success": False,
                    "message": "Orden no pertenece al usuario"
                }

            if order.status != OrderStatus.PENDING_PAYMENT.value:
                return {
                    "success": False,
                    "message": f"Orden no está en estado PENDING_PAYMENT (estado actual: {order.status})"
                }

            # Verificar idempotencia: orden ya procesada
            if order.payment_reference:
                print(f"⚠️  Orden {order_id} ya fue procesada (payment_reference: {order.payment_reference})")
                return {
                    "success": False,
                    "message": "Esta orden ya fue procesada anteriormente"
                }

            # Generar payment_reference único para idempotencia
            import uuid
            order.payment_reference = f"wallet_{uuid.uuid4().hex[:16]}"
            session.add(order)
            session.flush()

            # 2. Validar balance de wallet con ROW-LEVEL LOCK (evita race condition)
            wallet = session.exec(
                sqlmodel.select(Wallets)
                .where(Wallets.member_id == member_id)
                .with_for_update()  # 🔒 Bloqueo pesimista
            ).first()

            if not wallet:
                return {
                    "success": False,
                    "message": "No existe wallet para este usuario"
                }

            # Usar order.total (NO order.total_amount)
            if not wallet.has_sufficient_balance(order.total):
                return {
                    "success": False,
                    "message": f"Balance insuficiente: tiene {wallet.balance} {order.currency}, necesita {order.total} {order.currency}"
                }

            print(f"💳 Procesando pago con wallet para orden {order_id}...")

            # 3. Debitar monto de wallet (crea transacción automáticamente)
            payment_success = WalletService.pay_order_with_wallet(
                session=session,
                member_id=member_id,
                order_id=order_id,
                amount=order.total,
                currency=order.currency
            )

            if not payment_success:
                session.rollback()
                return {
                    "success": False,
                    "message": "Error al debitar wallet"
                }

            # 4. Confirmar pago de orden
            cls._confirm_order_payment(session, order)

            # 5. Actualizar PV del comprador y ancestros (CRÍTICO)
            pv_updated = PVUpdateService.process_order_pv_update(session, order_id)

            if not pv_updated:
                session.rollback()  # ⚠️ Revertir TODO (pago, confirmación, wallet)
                print(f"❌ Error crítico actualizando PV para orden {order_id}")
                return {
                    "success": False,
                    "message": "Error procesando puntos. Pago no completado. Intente nuevamente."
                }

            # 6. Disparar cálculo de comisiones
            try:
                cls._trigger_commissions(session, order)
            except Exception as e:
                session.rollback()  # ⚠️ Revertir TODO si falla comisiones
                print(f"❌ Error disparando comisiones: {e}")
                import traceback
                traceback.print_exc()
                return {
                    "success": False,
                    "message": "Error procesando comisiones. Pago no completado."
                }

            # Commit final
            session.commit()

            print(f"✅ Pago procesado exitosamente para orden {order_id}")

            return {
                "success": True,
                "message": "Pago procesado exitosamente",
                "order_id": order_id
            }

        except Exception as e:
            session.rollback()
            print(f"❌ Error procesando pago con wallet para orden {order_id}: {e}")
            import traceback
            traceback.print_exc()

            return {
                "success": False,
                "message": f"Error interno: {str(e)}"
            }

    @classmethod
    def _confirm_order_payment(cls, session, order: Orders) -> None:
        """
        Confirma el pago de una orden.
        Cambia estado a PAYMENT_CONFIRMED y establece timestamp.

        Args:
            session: Sesión de base de datos
            order: Orden a confirmar
        """
        try:
            # Obtener período actual
            current_period = PeriodService.get_current_period(session)

            if not current_period:
                print(f"⚠️  No hay período actual, order.period_id será NULL")

            # Actualizar orden
            order.status = OrderStatus.PAYMENT_CONFIRMED.value
            order.payment_confirmed_at = datetime.now(timezone.utc)
            order.period_id = current_period.id if current_period else None
            order.payment_method = "wallet"

            session.add(order)
            session.flush()

            print(f"✅ Pago confirmado para orden {order.id} en período {order.period_id}")

        except Exception as e:
            print(f"❌ Error confirmando pago de orden {order.id}: {e}")
            raise

    @classmethod
    def _trigger_commissions(cls, session, order: Orders) -> None:
        """
        Dispara cálculo de comisiones para una orden confirmada.

        Comisiones disparadas:
        - Bono Directo (25% VN) - si total_vn > 0
        - Bono Rápido (30%/10%/5%) - solo si orden contiene kits

        Nota: Bono Uninivel se procesa mensualmente al cierre de período.

        Args:
            session: Sesión de base de datos
            order: Orden confirmada
        """
        try:
            print(f"💰 Disparando comisiones para orden {order.id}...")

            # 1. Bono Directo (25% del VN total)
            # Aplica tanto para kits como productos regulares
            if order.total_vn > 0:
                direct_commission = CommissionService.process_direct_bonus(
                    session=session,
                    buyer_id=order.member_id,
                    order_id=order.id,
                    vn_amount=order.total_vn
                )

                if direct_commission:
                    print(f"✅ Bono Directo generado para orden {order.id}")

            # 2. Bono Rápido (solo si la orden contiene kits)
            # Los kits pagan bono rápido instantáneo a 3 niveles
            commission_ids = CommissionService.process_fast_start_bonus(
                session=session,
                order_id=order.id
            )

            if commission_ids:
                print(f"✅ Bono Rápido generado para {len(commission_ids)} patrocinadores")

            # 3. Bono Uninivel - NO se procesa aquí
            # Se procesará mensualmente al cierre del período (día 31)
            # Aplica para TODOS los productos (kits y regulares)

            print(f"✅ Comisiones instantáneas disparadas para orden {order.id}")

        except Exception as e:
            print(f"❌ Error disparando comisiones para orden {order.id}: {e}")
            # No lanzar excepción, comisiones se pueden recalcular
            import traceback
            traceback.print_exc()

    @classmethod
    def validate_wallet_payment_available(
        cls,
        session,
        member_id: int,
        amount: float
    ) -> dict:
        """
        Valida si el usuario puede pagar con wallet.

        Args:
            session: Sesión de base de datos
            member_id: ID del usuario
            amount: Monto a validar

        Returns:
            Dict con:
            - available: bool
            - message: str
            - balance: float (si wallet existe)
            - currency: str (si wallet existe)
        """
        try:
            wallet = session.exec(
                sqlmodel.select(Wallets).where(Wallets.member_id == member_id)
            ).first()

            if not wallet:
                return {
                    "available": False,
                    "message": "No tienes una wallet creada",
                    "balance": 0.0
                }

            has_balance = wallet.has_sufficient_balance(amount)

            return {
                "available": has_balance,
                "message": "Balance suficiente" if has_balance else f"Balance insuficiente (tienes {wallet.balance} {wallet.currency})",
                "balance": wallet.balance,
                "currency": wallet.currency
            }

        except Exception as e:
            print(f"❌ Error validando wallet para usuario {member_id}: {e}")
            return {
                "available": False,
                "message": "Error al validar wallet",
                "balance": 0.0
            }
