import reflex as rx
import os

config = rx.Config(
	app_name="NNProtect_new_website",
	plugins=[rx.plugins.TailwindV4Plugin(), rx.plugins.SitemapPlugin()],
	
	# Configuración de base de datos Supabase
    db_url="postgresql://postgres.wxjknxpyqgxxjtrkuyev:nn_backoffice!@aws-1-us-east-2.pooler.supabase.com:6543/postgres",
)