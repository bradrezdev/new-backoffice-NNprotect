import reflex as rx

config = rx.Config(
    app_name="NNProtect_new_website",
    plugins=[rx.plugins.TailwindV3Plugin(), rx.plugins.SitemapPlugin()],
    db_url="postgresql://postgres.wxjknxpyqgxxjtrkuyev:nn_backoffice!@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
)