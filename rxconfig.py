import reflex as rx
from NNProtect_new_website.utils.environment import Environment

# Obtener configuración según el entorno (Principio DRY)
DATABASE_URL = Environment.get_database_url()
JWT_SECRET_KEY = Environment.get_jwt_secret()

config = rx.Config(
    app_name="NNProtect_new_website",
    plugins=[rx.plugins.TailwindV3Plugin(), rx.plugins.SitemapPlugin()],
    db_url=DATABASE_URL
)