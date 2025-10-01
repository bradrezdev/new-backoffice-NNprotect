"""
Módulo centralizado para detección de entorno.
Principio DRY: un solo lugar para toda la lógica de detección de producción/desarrollo.
"""
import os
from typing import Tuple


class Environment:
    """
    Clase singleton para detección y configuración de entorno.
    Principio KISS: lógica simple y centralizada.
    """

    # Valores hardcodeados para producción
    PROD_DATABASE_URL = "postgresql://postgres.wxjknxpyqgxxjtrkuyev:nn_backoffice!@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
    PROD_JWT_SECRET_KEY = "cd3de0d6ca1fe14e1d1893137218613d76d63f88902412c204882deec8681d7b"
    PROD_BASE_URL = "https://codebradrez.tech/register"
    DEV_BASE_URL = "http://localhost:3000/register"

    @staticmethod
    def is_production() -> bool:
        """
        Detecta si estamos en entorno de producción.

        Returns:
            bool: True si es producción, False si es desarrollo
        """
        return (
            os.environ.get("REFLEX_ENV") == "prod" or
            not os.path.exists(".env") or
            "reflex.dev" in os.environ.get("HOSTNAME", "")
        )

    @staticmethod
    def get_database_url() -> str:
        """
        Obtiene la URL de la base de datos según el entorno.

        Returns:
            str: URL de la base de datos
        """
        if Environment.is_production():
            return Environment.PROD_DATABASE_URL
        else:
            from dotenv import load_dotenv
            load_dotenv()
            return os.getenv("DATABASE_URL", Environment.PROD_DATABASE_URL)

    @staticmethod
    def get_jwt_secret() -> str:
        """
        Obtiene la clave secreta JWT según el entorno.

        Returns:
            str: Clave secreta JWT
        """
        if Environment.is_production():
            return Environment.PROD_JWT_SECRET_KEY
        else:
            from dotenv import load_dotenv
            load_dotenv()
            jwt_secret = os.environ.get("JWT_SECRET_KEY")
            if not jwt_secret:
                return Environment.PROD_JWT_SECRET_KEY
            return jwt_secret

    @staticmethod
    def get_base_url() -> str:
        """
        Obtiene la URL base de la aplicación según el entorno.

        Returns:
            str: URL base de la aplicación
        """
        if Environment.is_production():
            return Environment.PROD_BASE_URL
        else:
            return Environment.DEV_BASE_URL

    @staticmethod
    def get_config() -> Tuple[str, str, str]:
        """
        Obtiene configuración completa del entorno.

        Returns:
            Tuple[str, str, str]: (database_url, jwt_secret, base_url)
        """
        return (
            Environment.get_database_url(),
            Environment.get_jwt_secret(),
            Environment.get_base_url()
        )