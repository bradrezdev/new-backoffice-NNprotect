"""
Servicio de Pagos - NNProtect Backoffice

Este módulo maneja toda la funcionalidad de procesamiento de pagos:
- Métodos de pago (wallet virtual, tarjetas de crédito/débito)
- Integración con Stripe
- Procesamiento de transacciones
- Webhooks de confirmación de pagos
"""

from .payment_service import PaymentService

__all__ = ["PaymentService"]