import reflex as rx
from NNProtect_new_website.utils.environment import Environment
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Obtener configuración según el entorno (Principio DRY)
DATABASE_URL = Environment.get_database_url()
JWT_SECRET_KEY = Environment.get_jwt_secret()

config = rx.Config(
    app_name="NNProtect_new_website",
    plugins=[rx.plugins.TailwindV3Plugin(), rx.plugins.SitemapPlugin()],
    db_url=DATABASE_URL
)

# 🔧 FIX: Monkey-patch del método get_db_engine para usar pool optimizado
_original_get_db_engine = rx.Model.get_db_engine


def _get_db_engine_with_pool():
    """
    Sobrescribe get_db_engine para retornar un engine con pool optimizado.
    
    Esto previene errores de "SSL connection has been closed unexpectedly"
    """
    # Verificar si ya existe un engine configurado
    if hasattr(rx.Model, '_engine') and rx.Model._engine is not None:
        return rx.Model._engine
    
    # Crear engine con pool optimizado
    engine = create_engine(
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
    
    # Guardar el engine en rx.Model
    rx.Model._engine = engine
    
    print("✅ Database engine configurado con pool optimizado")
    
    return engine


# Aplicar monkey-patch
rx.Model.get_db_engine = staticmethod(_get_db_engine_with_pool)