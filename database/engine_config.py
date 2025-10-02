"""
🔧 Configuración del Engine de SQLAlchemy con Pool Optimizado

Este módulo configura el engine de base de datos con parámetros de pool
optimizados para prevenir errores de "SSL connection has been closed unexpectedly".

El problema: Sin configuración de pool, las conexiones a Supabase se cierran
inesperadamente causando reintentos y delays de 50-60 segundos.

La solución: Pool de conexiones con pre-ping para detectar conexiones muertas
antes de usarlas.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool, Pool
from NNProtect_new_website.utils.environment import Environment


# Variable global para almacenar el engine configurado
_configured_engine = None


def get_configured_engine():
    """
    Retorna un engine de SQLAlchemy con pool optimizado.
    
    Configuración:
    - pool_size=10: Mantener 10 conexiones persistentes
    - max_overflow=20: Permitir hasta 30 conexiones totales
    - pool_pre_ping=True: 🔥 CRÍTICO - Testear conexión antes de usar
    - pool_recycle=3600: Reciclar conexiones cada hora
    """
    global _configured_engine
    
    if _configured_engine is None:
        DATABASE_URL = Environment.get_database_url()
        
        _configured_engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=10,              # Mantener 10 conexiones persistentes
            max_overflow=20,           # Permitir hasta 30 conexiones en picos
            pool_pre_ping=True,        # 🔥 CRÍTICO: Testear antes de usar
            pool_recycle=3600,         # Reciclar cada hora
            echo=False,                # No mostrar queries SQL
            connect_args={
                "connect_timeout": 10  # Timeout de 10s para conexión inicial
            }
        )
        
        # Event listener para logging de pool
        @event.listens_for(_configured_engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            print("🔌 Nueva conexión a BD establecida")
        
        @event.listens_for(_configured_engine, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            # Se ejecuta cuando se obtiene una conexión del pool
            pass
        
        print("✅ Database engine configurado con pool optimizado")
        print(f"   • Pool size: 10 conexiones")
        print(f"   • Max overflow: 20 conexiones")
        print(f"   • Pre-ping: Habilitado ✅")
        print(f"   • Pool recycle: 3600s (1 hora)")
    
    return _configured_engine
