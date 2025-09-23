import reflex as rx
import os
from dotenv import load_dotenv

# Detectar si estamos en producción
IS_PRODUCTION = (
    os.environ.get("REFLEX_ENV") == "prod" or 
    not os.path.exists(".env") or
    "reflex.dev" in os.environ.get("HOSTNAME", "")
)

if IS_PRODUCTION:
    print("DEBUG: Entorno PRODUCCIÓN detectado")
    # Configuración hardcodeada para producción
    DATABASE_URL = "postgresql://postgres.wxjknxpyqgxxjtrkuyev:nn_backoffice!@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
    JWT_SECRET_KEY = "cd3de0d6ca1fe14e1d1893137218613d76d63f88902412c204882deec8681d7b"
else:
    print("DEBUG: Entorno DESARROLLO detectado")
    # Cargar desde .env en desarrollo
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

print(f"DEBUG: DATABASE_URL configurado: {'✅ Sí' if DATABASE_URL else '❌ No'}")
print(f"DEBUG: JWT_SECRET_KEY configurado: {'✅ Sí' if JWT_SECRET_KEY else '❌ No'}")

config = rx.Config(
    app_name="NNProtect_new_website",
    plugins=[rx.plugins.TailwindV3Plugin(), rx.plugins.SitemapPlugin()],
    db_url=DATABASE_URL
)