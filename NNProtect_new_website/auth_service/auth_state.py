"""
Módulo de estado de autenticación refactorizado.
Implementa autenticación con JWT y sistema de sponsors con arquitectura limpia.
Compatible con migración futura a Supabase Auth.
"""

import reflex as rx
import bcrypt
import jwt
import datetime
import sqlmodel
import os
import random
import asyncio
import re
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from dotenv import load_dotenv

# Timezone utilities
from ..utils.timezone_mx import get_mexico_now

# Database imports
from database.users import Users, UserStatus
from database.auth_credentials import AuthCredentials
from database.roles import Roles
from database.userprofiles import UserProfiles, UserGender
from database.social_accounts import SocialAccounts, SocialNetwork
from database.roles_users import RolesUsers
from database.addresses import Addresses
from database.users_addresses import UserAddresses
from database.usertreepaths import UserTreePath

# Importar nuevos managers para Supabase
from .supabase_auth_manager import SupabaseAuthManager
from ..mlm_service.mlm_user_manager import MLMUserManager


@dataclass
class UserData:
    """Estructura de datos del usuario."""
    id: int
    username: str
    email: str
    member_id: int
    status: str
    first_name: str = ""
    last_name: str = ""
    referral_link: str = ""
    profile_name: str = ""


class AuthenticationManager:
    """Maneja operaciones de autenticación y JWT."""
    
    @staticmethod
    def get_jwt_secret() -> str:
        """Obtiene la clave JWT con detección robusta de entorno."""
        is_production = (
            os.environ.get("REFLEX_ENV") == "prod" or 
            not os.path.exists(".env") or
            "reflex.dev" in os.environ.get("HOSTNAME", "")
        )
        
        if is_production:
            # En producción, usar clave hardcodeada
            print("DEBUG: Usando JWT secret de PRODUCCIÓN")
            return "cd3de0d6ca1fe14e1d1893137218613d76d63f88902412c204882deec8681d7b"
        else:
            # En desarrollo, usar .env
            load_dotenv()
            jwt_secret = os.environ.get("JWT_SECRET_KEY")
            if not jwt_secret:
                print("DEBUG: JWT_SECRET_KEY no encontrada en .env, usando fallback")
                return "cd3de0d6ca1fe14e1d1893137218613d76d63f88902412c204882deec8681d7b"
            print("DEBUG: Usando JWT secret desde .env")
            return jwt_secret

    @classmethod
    def create_jwt_token(cls, user: Users) -> str:
        """Crea un JWT token para el usuario autenticado."""
        try:
            jwt_secret_key = cls.get_jwt_secret()
            
            user_id = int(user.id) if user.id is not None else 0
            username = f"{user.first_name} {user.last_name}".strip() if user.first_name else "unknown"
            
            login_token = {
                "id": user_id,
                "username": username,
                "exp": get_mexico_now() + datetime.timedelta(minutes=60),  # ✅ MÉXICO TIMEZONE
            }
            
            token = jwt.encode(login_token, jwt_secret_key, algorithm="HS256")
            
            if isinstance(token, bytes):
                token_str = token.decode('utf-8')
            else:
                token_str = str(token)
                
            print(f"DEBUG: Token generado exitosamente (longitud: {len(token_str)})")
            return token_str
            
        except Exception as e:
            print(f"DEBUG: Error creando JWT token: {str(e)}")
            raise Exception(f"Error generando token JWT: {str(e)}")

    @classmethod
    def decode_jwt_token(cls, token: str) -> Dict[str, Any]:
        """Decodifica el JWT token para obtener los datos del usuario."""
        if not token or "." not in token:
            return {}
            
        try:
            jwt_secret_key = cls.get_jwt_secret()
            decoded = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
            print("DEBUG: Token decodificado exitosamente")
            return decoded
            
        except jwt.ExpiredSignatureError:
            print("DEBUG: Token expirado")
            return {}
        except Exception as e:
            print(f"DEBUG: Error decodificando token: {e}")
            return {}

    @staticmethod
    def hash_password(password: str) -> str:
        """Genera hash de contraseña usando bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verifica contraseña contra su hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


class SponsorManager:
    """Maneja operaciones relacionadas con sponsors."""
    
    @staticmethod
    def validate_sponsor_by_member_id(member_id: int) -> bool:
        """Verifica si existe un usuario con el member_id dado."""
        if member_id <= 0:
            return False
        
        try:
            with rx.session() as session:
                sponsor = session.exec(
                    sqlmodel.select(Users).where(Users.member_id == member_id)
                ).first()
                return sponsor is not None
        except Exception as e:
            print(f"DEBUG: Error validando sponsor: {e}")
            return False

    @staticmethod
    def get_user_id_by_member_id(member_id: int) -> Optional[int]:
        """Convierte member_id a user.id para operaciones de BD."""
        try:
            with rx.session() as session:
                user = session.exec(
                    sqlmodel.select(Users).where(Users.member_id == member_id)
                ).first()
                return user.id if user else None
        except Exception as e:
            print(f"DEBUG: Error obteniendo user_id: {e}")
            return None

    @staticmethod
    def get_sponsor_display_name(member_id: int) -> str:
        """Obtiene el nombre para mostrar del sponsor."""
        if member_id <= 0:
            return "⚠️ Sin sponsor válido"
        
        try:
            with rx.session() as session:
                sponsor = session.exec(
                    sqlmodel.select(Users).where(Users.member_id == member_id)
                ).first()
                if sponsor:
                    return f"{sponsor.first_name or ''} {sponsor.last_name or ''}".strip() or f"Member-{sponsor.member_id}"
        except Exception as e:
            print(f"DEBUG: Error obteniendo nombre sponsor: {e}")
        
        return "Sponsor desconocido"


class UserDataManager:
    """Maneja operaciones de datos de usuario."""
    
    @staticmethod
    def extract_first_word(text: str) -> str:
        """Extrae la primera palabra de un texto."""
        if not text:
            return ""
        
        clean_text = str(text).strip()
        words = clean_text.split()
        return words[0] if words else ""

    @classmethod
    def build_profile_name(cls, first_name: str, last_name: str, username: str) -> str:
        """Construye el nombre de perfil usando solo las primeras palabras."""
        first_word = cls.extract_first_word(first_name)
        last_word = cls.extract_first_word(last_name)
        
        if first_word and last_word:
            return f"{first_word} {last_word}"
        elif first_word:
            return first_word
        elif last_word:
            return last_word
        else:
            return username

    @staticmethod
    def load_user_profile_data(user_id: int) -> Dict[str, Any]:
        """Carga datos completos del perfil de usuario."""
        try:
            with rx.session() as session:
                # Implementación simplificada por ahora
                return {"user_id": user_id, "loaded": True}
                
        except Exception as e:
            print(f"DEBUG: Error cargando perfil: {e}")
            return {}
    
    @staticmethod
    def get_user_country_by_id(user_id: int) -> Optional[str]:
        """
        Obtiene el país de registro del usuario mediante JOIN con addresses.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Countries: País del usuario o None si no se encuentra
        """
        try:
            with rx.session() as session:
                # Obtener las direcciones del usuario
                from sqlmodel import select
                from database.users_addresses import UserAddresses
                from database.addresses import Addresses
                
                # Primero obtener la dirección default del usuario
                user_address_stmt = select(UserAddresses).where(
                    UserAddresses.user_id == user_id,
                    UserAddresses.is_default == True
                )
                user_address = session.exec(user_address_stmt).first()
                
                if user_address:
                    # Obtener la dirección completa
                    address_stmt = select(Addresses).where(
                        Addresses.id == user_address.address_id
                    )
                    address = session.exec(address_stmt).first()
                    
                    if address:
                        return address.country
                        
                return None
                
        except Exception as e:
            print(f"DEBUG: Error obteniendo país del usuario {user_id}: {e}")
            return None
    
    @staticmethod
    def update_user_country_cache(user_id: int) -> bool:
        """
        Actualiza el country_cache del usuario con su país de registro.
        
        Args:
            user_id: ID del usuario a actualizar
            
        Returns:
            bool: True si se actualizó correctamente, False en caso de error
        """
        try:
            country = UserDataManager.get_user_country_by_id(user_id)
            if country:
                with rx.session() as session:
                    # Buscar el usuario actual y actualizar su country_cache
                    user = session.get(Users, user_id)
                    if user:
                        user.country_cache = country
                        session.add(user)
                        session.commit()
                        session.refresh(user)
                        return True
            return False
            
        except Exception as e:
            print(f"DEBUG: Error actualizando country_cache para usuario {user_id}: {e}")
            return False


class PasswordValidator:
    """Valida y verifica requisitos de contraseña."""
    
    @staticmethod
    def has_length(password: str, min_length: int = 8) -> bool:
        """Verifica longitud mínima."""
        return len(password) >= min_length

    @staticmethod
    def has_uppercase(password: str) -> bool:
        """Verifica letra mayúscula."""
        return bool(re.search(r'[A-Z]', password))

    @staticmethod
    def has_lowercase(password: str) -> bool:
        """Verifica letra minúscula."""
        return bool(re.search(r'[a-z]', password))

    @staticmethod
    def has_number(password: str) -> bool:
        """Verifica número."""
        return bool(re.search(r'[0-9]', password))

    @staticmethod
    def has_special(password: str) -> bool:
        """Verifica carácter especial."""
        return bool(re.search(r'[^a-zA-Z0-9]', password))

    @classmethod
    def validate_complexity(cls, password: str) -> tuple[bool, str]:
        """Valida complejidad completa de contraseña."""
        if not all([
            cls.has_length(password),
            cls.has_uppercase(password),
            cls.has_lowercase(password),
            cls.has_number(password),
            cls.has_special(password)
        ]):
            return False, (
                "La contraseña debe tener al menos 8 caracteres, "
                "una letra mayúscula, una letra minúscula, un número y un carácter especial."
            )
        return True, ""


class RegistrationManager:
    """Maneja operaciones de registro de usuarios."""
    
    # ✅ Mapeo de países display → valor interno
    COUNTRY_MAP = {
        "United States": "USA",
        "Colombia": "COLOMBIA", 
        "Mexico": "MEXICO",
        "Puerto Rico": "PUERTO_RICO",
    }
    
    # ✅ Estados por país (movido desde ENUM)
    COUNTRY_STATES = {
        "USA": ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
                "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
                "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
                "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
                "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
                "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
                "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"],
        "COLOMBIA": ["Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", "Boyacá", "Caldas", "Caquetá",
                     "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía",
                     "Guaviare","Huila","La Guajira","Magdalena","Meta","Nariño","Norte de Santander","Putumayo",
                     "Quindío","Risaralda","San Andrés y Providencia","Santander","Sucre","Tolima","Valle del Cauca",
                     "Vaupés","Vichada"],
        "MEXICO": ["Aguascalientes","Baja California","Baja California Sur","Campeche","Chiapas","Chihuahua",
                   "Ciudad de México","Coahuila","Colima","Durango","Guanajuato","Guerrero","Hidalgo","Jalisco",
                   "México","Michoacán","Morelos","Nayarit","Nuevo León","Oaxaca","Puebla","Querétaro",
                   "Quintana Roo","San Luis Potosí","Sinaloa","Sonora","Tabasco","Tamaulipas",
                   "Tlaxcala","Veracruz","Yucatán","Zacatecas"],
        "PUERTO_RICO": ["Adjuntas","Aguada","Aguadilla","Aguasbuena","Aibonito","Anasco","Arecibo","Arroyo",
                        "Barceloneta","Barranquitas","Bayamón","Cabo Rojo","Caguas","Camuy","Canóvanas","Carolina",
                        "Cataño","Cayey","Ceiba","Ciales","Cidra","Coamo","Comerío","Corozal","Culebra","Dorado",
                        "Fajardo","Florida","Guánica","Guayama","Guayanilla","Guaynabo","Gurabo","Hatillo","Hormigueros",
                        "Humacao","Isabela","Jayuya","Juana Díaz","Juncos","Lajas","Lares","Las Marías","Las Piedras","Loíza",
                        "Luquillo","Manatí","Maricao","Maunabo","Mayagüez","Moca","Morovis","Naguabo","Naranjito","Orocovis",
                        "Patillas","Peñuelas","Ponce","Quebradillas","Rincón","Río Grande","Sabana Grande","Salinas","San Germán","San Juan",
                        "San Lorenzo","San Sebastián","Santa Isabel","Toa Alta","Toa Baja","Trujillo Alto","Utuado","Vega Alta","Vega Baja","Vieques",
                        "Villalba","Yabucoa","Yauco"]
    }
    
    @classmethod
    def get_country_options(cls) -> List[str]:
        """Obtiene lista de países disponibles."""
        return list(cls.COUNTRY_MAP.keys())
    
    @classmethod
    def get_states_for_country(cls, country_display: str) -> List[str]:
        """Obtiene estados para un país dado (por nombre display)."""
        country_key = cls.COUNTRY_MAP.get(country_display)
        if not country_key:
            return []
        return cls.COUNTRY_STATES.get(country_key, [])
    
    @classmethod
    def get_country_value(cls, country_display: str) -> str:
        """Convierte nombre display a valor interno."""
        return cls.COUNTRY_MAP.get(country_display, country_display)

    @staticmethod
    def get_next_member_id(session) -> int:
        """Obtiene el siguiente member_id disponible."""
        last_user = session.exec(
            sqlmodel.select(Users).order_by(sqlmodel.desc(Users.member_id))
        ).first()
        return last_user.member_id + 1 if last_user else 1

    @staticmethod
    def user_exists(session, username: str, email: str) -> bool:
        """Verifica si usuario ya existe por email_cache."""
        return session.exec(
            sqlmodel.select(Users).where(Users.email_cache == email)
        ).first() is not None

    @staticmethod
    def get_base_url() -> str:
        """Obtiene la URL base de la aplicación."""
        is_production = (
            os.environ.get("REFLEX_ENV") == "prod" or 
            not os.path.exists(".env") or
            "reflex.dev" in os.environ.get("HOSTNAME", "")
        )

        if is_production:
            return "https://codebradrez.tech/register"
        else:
            return "http://localhost:3000/register"

    @staticmethod
    def create_user_record(session, member_id: int, username: str, email: str,
                          first_name: str, last_name: str, sponsor_id: Optional[int] = None) -> Users:
        """Crea el registro base del usuario."""
        base_url = RegistrationManager.get_base_url()
        
        new_user = Users(
            member_id=member_id,
            first_name=first_name,
            last_name=last_name,
            email_cache=email,
            status=UserStatus.NO_QUALIFIED,
            referral_link=f"{base_url}?ref={member_id}",
            sponsor_id=sponsor_id
        )
        session.add(new_user)
        session.flush()
        return new_user

    @staticmethod
    def create_auth_credentials(session, user_id: int, password: str, terms_accepted: bool):
        """Crea credenciales de autenticación."""
        hashed_password = AuthenticationManager.hash_password(password)
        
        new_credentials = AuthCredentials(
            user_id=user_id,
            password_hash=hashed_password,
            terms_accepted=terms_accepted
        )
        session.add(new_credentials)

    @staticmethod
    def assign_default_role(session, user_id: int):
        """Asigna rol por defecto al usuario."""
        default_role = session.exec(
            sqlmodel.select(Roles).where(Roles.role_name == "USER")
        ).first()
        
        if default_role:
            user_role = RolesUsers(
                user_id=user_id,
                role_id=default_role.role_id
            )
            session.add(user_role)
        else:
            raise Exception("Rol por defecto 'USER' no encontrado.")

    @classmethod
    def create_user_profile(cls, session, user_id: int, phone: str, gender: str):
        """Crea perfil detallado del usuario."""
        gender_enum = UserGender.MALE  # Por defecto
        if gender == "Femenino":
            gender_enum = UserGender.FEMALE
        elif gender == "Masculino":
            gender_enum = UserGender.MALE
            
        new_profile = UserProfiles(
            user_id=user_id,
            gender=gender_enum,
            phone_number=phone
        )
        session.add(new_profile)

    @staticmethod
    def create_social_accounts(session, user_id: int):
        """Crea registro de redes sociales por defecto."""
        social_accounts = SocialAccounts(
            user_id=user_id,
            provider=SocialNetwork.NONE,
            url=""
        )
        session.add(social_accounts)

    @classmethod
    def create_user_address(cls, session, user_id: int, street: str, neighborhood: str,
                          city: str, state: str, country: str, zip_code: str):
        """Crea dirección del usuario."""
        try:
            # ✅ Convertir nombre display a valor interno
            country_value = cls.get_country_value(country)
            
            new_address = Addresses(
                street=street,
                neighborhood=neighborhood or "",
                city=city,
                state=state or "",
                country=country_value,  # ✅ Texto plano
                zip_code=zip_code or ""
            )
            session.add(new_address)
            session.flush()
            
            # ✅ Verificar que address_id no sea None
            if new_address.id is None:
                raise ValueError("Error: No se pudo crear la dirección")
            
            user_address = UserAddresses(
                user_id=user_id,
                address_id=new_address.id,
                address_name="Principal",
                is_default=True,
                created_at=get_mexico_now().isoformat(),  # ✅ MÉXICO TIMEZONE
                updated_at=get_mexico_now().isoformat()  # ✅ MÉXICO TIMEZONE
            )
            session.add(user_address)
            
        except Exception as e:
            print(f"DEBUG: Error creando dirección: {e}")
            raise


class AuthState(rx.State):
    """Estado de autenticación principal con arquitectura limpia."""
    
    # Estados básicos
    is_loading: bool = False
    error_message: str = ""
    is_logged_in: bool = False
    
    # Token de autenticación
    auth_token: str = rx.Cookie(name="auth_token", secure=True, same_site="Lax")
    
    # Datos de usuario
    logged_user_data: dict = {}
    profile_data: dict = {}
    
    # Campos de login
    username: str = ""
    email: str = ""
    password: str = ""
    
    # Campos de registro (prefijo new_)
    new_username: str = ""
    new_email: str = ""
    new_password: str = ""
    new_confirmed_password: str = ""
    new_user_firstname: str = ""
    new_user_lastname: str = ""
    new_phone_number: str = ""
    new_gender: str = ""
    new_terms_accepted: bool = False
    
    # Campos de dirección
    new_street_number: str = ""
    new_neighborhood: str = ""
    new_city: str = ""
    new_zip_code: str = ""
    new_country: str = ""
    new_state: str = ""
    
    # Sistema de sponsors
    potential_sponsor_id: int = 0

    # Computed vars para validación de contraseña
    @rx.var
    def password_has_length(self) -> bool:
        return PasswordValidator.has_length(self.new_password)

    @rx.var
    def password_has_uppercase(self) -> bool:
        return PasswordValidator.has_uppercase(self.new_password)

    @rx.var
    def password_has_lowercase(self) -> bool:
        return PasswordValidator.has_lowercase(self.new_password)

    @rx.var
    def password_has_number(self) -> bool:
        return PasswordValidator.has_number(self.new_password)

    @rx.var
    def password_has_special(self) -> bool:
        return PasswordValidator.has_special(self.new_password)

    @rx.var
    def country_options(self) -> List[str]:
        """Lista de países disponibles."""
        return RegistrationManager.get_country_options()

    @rx.var
    def state_options(self) -> List[str]:
        """Estados del país seleccionado."""
        if not self.new_country:
            return []
        return RegistrationManager.get_states_for_country(self.new_country)

    @rx.var
    def sponsor_display_name(self) -> str:
        """Nombre del sponsor para mostrar."""
        if self.potential_sponsor_id == 0:
            return "⚠️ Sin sponsor válido"
        
        if self.profile_data.get("member_id") == self.potential_sponsor_id:
            return self.profile_data.get("profile_name", "Usuario con datos")
        
        return SponsorManager.get_sponsor_display_name(self.potential_sponsor_id)

    @rx.var
    def can_register(self) -> bool:
        """Indica si se puede proceder con el registro."""
        return (self.potential_sponsor_id > 0 and 
                SponsorManager.validate_sponsor_by_member_id(self.potential_sponsor_id))

    @rx.var
    def get_user_display_name(self) -> str:
        """Nombre para mostrar del usuario logueado usando primer nombre y apellido."""
        if not isinstance(self.profile_data, dict):
            return "Usuario"
        
        # Obtener datos del perfil
        first_name = self.profile_data.get("firstname", "")
        last_name = self.profile_data.get("lastname", "")
        username = self.profile_data.get("username", "")
        
        # Usar método auxiliar para construir nombre corto
        return self._build_profile_name(first_name, last_name, username)

    @rx.var
    def sponsor_data(self) -> dict:
        """Datos del sponsor del usuario autenticado."""
        if not isinstance(self.profile_data, dict):
            return {}
        return self.profile_data.get("sponsor_data", {})

    def _extract_first_word(self, text: str) -> str:
        """Extrae la primera palabra de un texto, manejando casos edge."""
        if not text:
            return ""
        
        # Limpiar espacios extra y convertir a string
        clean_text = str(text).strip()
        if not clean_text:
            return ""
        
        # Dividir por espacios y tomar la primera palabra
        words = clean_text.split()
        return words[0] if words else ""

    def _build_profile_name(self, first_name: str, last_name: str, username: str) -> str:
        """Construye el nombre de perfil usando solo las primeras palabras."""
        first_word = self._extract_first_word(first_name)
        last_word = self._extract_first_word(last_name)
        
        # Construir nombre según disponibilidad
        if first_word and last_word:
            return f"{first_word} {last_word}"
        elif first_word:
            return first_word
        elif last_word:
            return last_word
        else:
            return username if username else "Usuario"  # Fallback final

    # Setters para campos de login  
    @rx.event
    def set_username(self, username: str):
        self.username = username

    @rx.event
    def set_email(self, email: str):
        self.email = email

    @rx.event
    def set_password(self, password: str):
        self.password = password

    # Setters para campos de registro
    @rx.event
    def set_new_username(self, new_username: str):
        self.new_username = new_username

    @rx.event
    def set_new_email(self, new_email: str):
        self.new_email = new_email

    @rx.event
    def set_new_password(self, new_password: str):
        self.new_password = new_password

    @rx.event
    def set_new_confirmed_password(self, new_confirmed_password: str):
        self.new_confirmed_password = new_confirmed_password

    @rx.event
    def set_new_firstname(self, new_user_firstname: str):
        self.new_user_firstname = new_user_firstname

    @rx.event
    def set_new_lastname(self, new_user_lastname: str):
        self.new_user_lastname = new_user_lastname

    @rx.event
    def set_new_phone_number(self, new_phone_number: str):
        self.new_phone_number = new_phone_number

    @rx.event
    def set_new_gender(self, new_gender: str):
        self.new_gender = new_gender

    @rx.event
    def set_new_terms_accepted(self, new_terms_accepted: bool):
        self.new_terms_accepted = new_terms_accepted

    @rx.event
    def set_new_street_number(self, new_street_number: str):
        self.new_street_number = new_street_number

    @rx.event
    def set_new_neighborhood(self, new_neighborhood: str):
        self.new_neighborhood = new_neighborhood

    @rx.event
    def set_new_city(self, new_city: str):
        self.new_city = new_city

    @rx.event
    def set_new_zip_code(self, new_zip_code: str):
        self.new_zip_code = new_zip_code

    @rx.event
    def set_new_country(self, new_country: str):
        self.new_country = new_country
        self.new_state = ""

    @rx.event
    def set_new_state(self, new_state: str):
        self.new_state = new_state

    # Métodos principales de autenticación
    @rx.event
    async def login_user(self):
        """
        NUEVO: Login híbrido Supabase Auth + datos MLM.
        Ahora usa email como identificador principal.
        """
        print("🔐 Iniciando login híbrido Supabase + MLM...")
        self.is_loading = True
        self.error_message = ""
        yield
        
        try:
            await asyncio.sleep(0.1)
            
            # ✅ VALIDACIÓN BÁSICA - ahora usa email en lugar de username
            login_identifier = self.email or self.username  # Backward compatibility
            if not login_identifier or not self.password:
                self.error_message = "El email y la contraseña no pueden estar vacíos."
                self.is_loading = False
                return

            # ✅ PASO 1: AUTENTICAR CON SUPABASE
            success, message, supabase_user_data = await SupabaseAuthManager.sign_in_user(
                login_identifier, self.password
            )
            
            if not success or not supabase_user_data:
                self.error_message = message or "Credenciales incorrectas"
                self.is_loading = False
                return
            
            supabase_user_id = supabase_user_data.get('id')
            if not supabase_user_id:
                self.error_message = "Error al obtener ID de usuario de Supabase"
                self.is_loading = False
                return
                
            print(f"✅ Autenticado en Supabase: {supabase_user_id}")

            # ✅ PASO 2: CARGAR DATOS MLM
            try:
                complete_user_data = MLMUserManager.load_complete_user_data(supabase_user_id)
                
                if not complete_user_data:
                    self.error_message = "Usuario no encontrado en el sistema MLM"
                    self.is_loading = False
                    return
                
                # ✅ PASO 3: ESTABLECER SESIÓN
                self.is_logged_in = True
                self.logged_user_data = {
                    "id": complete_user_data["id"],
                    "username": f"{complete_user_data['firstname']} {complete_user_data['lastname']}".strip(),
                    "email": supabase_user_data.get('email', ''),
                    "member_id": complete_user_data["member_id"],
                    "status": complete_user_data["status"],
                    "supabase_user_id": supabase_user_data.get('id'),
                }
                
                # Cargar datos extendidos del perfil
                self.profile_data = complete_user_data
                
                print(f"🎉 Login híbrido exitoso - Member ID: {complete_user_data['member_id']}")
                yield rx.redirect("/dashboard")
                return
                
            except Exception as mlm_error:
                print(f"❌ Error cargando datos MLM: {mlm_error}")
                self.error_message = "Error cargando datos del usuario"
                self.is_loading = False
                return
        
        except Exception as e:
            print(f"❌ ERROR login híbrido: {e}")
            import traceback
            traceback.print_exc()
            self.error_message = f"Error de login: {str(e)}"
        
        finally:
            self.is_loading = False

    @rx.event
    async def new_register_sponsor(self):
        """
        NUEVO: Registra usuario con Supabase Auth + datos MLM.
        Mantiene funcionalidad de sponsor obligatorio.
        """
        print("🚀 Iniciando registro híbrido Supabase + MLM...")
        self.is_loading = True
        self.error_message = ""
        yield

        try:
            await asyncio.sleep(0.1)
            
            # ✅ VALIDACIÓN CRÍTICA: SPONSOR OBLIGATORIO
            if (self.potential_sponsor_id <= 0 or 
                not MLMUserManager.validate_sponsor_by_member_id(self.potential_sponsor_id)):
                self.error_message = "No se puede realizar el registro sin un sponsor válido."
                self.is_loading = False
                return

            # ✅ VALIDACIÓN DE DATOS
            if not self._validate_registration_data():
                self.is_loading = False
                return

            # ✅ PASO 1: REGISTRAR EN SUPABASE AUTH
            display_name = f"{self.new_user_firstname} {self.new_user_lastname}".strip()
            
            success, message, supabase_user_id = await SupabaseAuthManager.sign_up_user(
                self.new_email, self.new_password, display_name,
                self.new_user_firstname, self.new_user_lastname
            )
            
            if not success or not supabase_user_id:
                self.error_message = message or "Error al obtener ID de usuario de Supabase"
                self.is_loading = False
                return
            
            print(f"✅ Usuario registrado en Supabase: {supabase_user_id}")

            # ✅ PASO 2: CREAR DATOS MLM
            with rx.session() as session:
                new_user = MLMUserManager.create_mlm_user(
                    session, supabase_user_id, self.new_user_firstname,
                    self.new_user_lastname, self.new_email, self.potential_sponsor_id
                )
                
                # Crear registros relacionados
                if new_user.id:
                    MLMUserManager.create_user_profile(
                        session, new_user.id, self.new_phone_number, self.new_gender
                    )
                    MLMUserManager.create_social_accounts(session, new_user.id)
                    MLMUserManager.assign_default_role(session, new_user.id)
                    MLMUserManager.create_legacy_auth_credentials(session, new_user.id)
                    
                    # Crear dirección si se proporcionó datos
                    if self.new_street_number and self.new_city and self.new_country:
                        MLMUserManager.create_user_address(
                            session, new_user.id, self.new_street_number,
                            self.new_neighborhood, self.new_city, self.new_state,
                            self.new_country, self.new_zip_code
                        )
                    
                session.commit()
                print(f"✅ Usuario MLM creado - Member ID: {new_user.member_id}")

            # ✅ LIMPIAR FORMULARIO Y MOSTRAR ÉXITO
            self._clear_registration_form()
            self.error_message = "¡Registro exitoso! Por favor verifica tu email antes de iniciar sesión."
            
            print("🎉 Registro híbrido completado exitosamente")

        except Exception as e:
            print(f"❌ ERROR registro híbrido: {e}")
            import traceback
            traceback.print_exc()
            self.error_message = f"Error de registro: {str(e)}"
            
        finally:
            self.is_loading = False

    @rx.event
    async def new_register_noSponsor(self):
        """
        NUEVO: Registra usuario SIN sponsor obligatorio.
        Para primeros usuarios o administradores.
        """
        print("🆕 Iniciando registro sin sponsor...")
        self.is_loading = True
        self.error_message = ""
        yield

        try:
            await asyncio.sleep(0.1)
            
            # ✅ VALIDACIÓN DE DATOS (sin sponsor)
            if not self._validate_registration_data():
                self.is_loading = False
                return

            # ✅ PASO 1: REGISTRAR EN SUPABASE AUTH
            display_name = f"{self.new_user_firstname} {self.new_user_lastname}".strip()
            
            success, message, supabase_user_id = await SupabaseAuthManager.sign_up_user(
                self.new_email, self.new_password, display_name,
                self.new_user_firstname, self.new_user_lastname
            )
            
            if not success or not supabase_user_id:
                self.error_message = message or "Error al obtener ID de usuario de Supabase"
                self.is_loading = False
                return
            
            print(f"✅ Usuario registrado en Supabase: {supabase_user_id}")

            # ✅ PASO 2: CREAR DATOS MLM (SIN SPONSOR)
            with rx.session() as session:
                new_user = MLMUserManager.create_mlm_user(
                    session, supabase_user_id, self.new_user_firstname,
                    self.new_user_lastname, self.new_email, None  # sponsor_id = None
                )
                
                # Crear registros relacionados
                if new_user.id:
                    MLMUserManager.create_user_profile(
                        session, new_user.id, self.new_phone_number, self.new_gender
                    )
                    MLMUserManager.create_social_accounts(session, new_user.id)
                    MLMUserManager.assign_default_role(session, new_user.id)
                    MLMUserManager.create_legacy_auth_credentials(session, new_user.id)
                    
                    # Crear dirección si se proporcionó datos
                    if self.new_street_number and self.new_city and self.new_country:
                        MLMUserManager.create_user_address(
                            session, new_user.id, self.new_street_number,
                            self.new_neighborhood, self.new_city, self.new_state,
                            self.new_country, self.new_zip_code
                        )
                    
                session.commit()
                print(f"✅ Usuario MLM creado SIN SPONSOR - Member ID: {new_user.member_id}")

            # ✅ LIMPIAR FORMULARIO Y MOSTRAR ÉXITO
            self._clear_registration_form()
            self.error_message = "¡Registro exitoso! Por favor verifica tu email antes de iniciar sesión."
            
            print("🎉 Registro sin sponsor completado exitosamente")

        except Exception as e:
            print(f"❌ ERROR registro sin sponsor: {e}")
            import traceback
            traceback.print_exc()
            self.error_message = f"Error de registro: {str(e)}"
            
        finally:
            self.is_loading = False

    @rx.event
    def on_load_register_page(self):
        """Captura sponsor desde URL o usuario logueado."""
        print("DEBUG: Iniciando captura de sponsor...")
        
        # Prioridad: parámetro ref en URL
        try:
            current_url = str(self.router.url)
            if "?ref=" in current_url:
                ref_param = current_url.split("?ref=")[1].split("&")[0]
                try:
                    potential_member_id = int(ref_param)
                    if SponsorManager.validate_sponsor_by_member_id(potential_member_id):
                        self.potential_sponsor_id = potential_member_id
                        print(f"DEBUG: Sponsor capturado desde URL - Member ID: {potential_member_id}")
                        return
                except (ValueError, TypeError):
                    print("DEBUG: Parámetro ref inválido en URL")
        except Exception as e:
            print(f"DEBUG: Error procesando URL: {e}")
        
        # Fallback: usuario con datos disponibles
        if self.profile_data.get("member_id"):
            sponsor_member_id = self.profile_data["member_id"]
            if SponsorManager.validate_sponsor_by_member_id(sponsor_member_id):
                self.potential_sponsor_id = sponsor_member_id
                print(f"DEBUG: Sponsor desde profile_data - Member ID: {self.potential_sponsor_id}")
                return
        
        # Sin sponsor válido
        self.potential_sponsor_id = 0
        self.error_message = "No se puede realizar el registro sin un sponsor válido."
        print("DEBUG: ERROR - No hay sponsor válido")

    @rx.event
    def load_user_from_token(self):
        """Carga datos del usuario desde token."""
        payload = AuthenticationManager.decode_jwt_token(self.auth_token)
        if not payload:
            self.is_logged_in = False
            self.logged_user_data = {}
            return
        
        user_id = payload.get("id")
        if not user_id:
            return
            
        try:
            with rx.session() as session:
                user = session.exec(
                    sqlmodel.select(Users).where(Users.id == user_id)
                ).first()
                
                if not user:
                    self.is_logged_in = False
                    self.logged_user_data = {}
                    self.profile_data = {}
                    return
                
                self.is_logged_in = True
                self.logged_user_data = {
                    "id": user.id,
                    "username": f"{user.first_name} {user.last_name}".strip(),  # Concatenar nombres
                    "email": user.email_cache,  # Usar email_cache
                    "member_id": user.member_id,
                    "status": user.status.value if hasattr(user.status, 'value') else str(user.status),
                }
                
                # Cargar datos extendidos del perfil
                self.profile_data = UserDataManager.load_user_profile_data(user_id)
                
        except Exception as e:
            print(f"DEBUG: Error cargando usuario desde token: {e}")

    @rx.event
    def check_login(self):
        """Verifica estado de login basado en token."""
        if self.auth_token:
            self.load_user_from_token()
        else:
            self.is_logged_in = False
            self.logged_user_data = {}

    @rx.event
    async def logout_user(self):
        """
        NUEVO: Logout híbrido Supabase + MLM.
        Cierra sesión tanto en Supabase como localmente.
        """
        print("🔓 Iniciando logout híbrido...")
        
        try:
            # ✅ LOGOUT DE SUPABASE
            success = SupabaseAuthManager.sign_out_user()
            if success:
                print("✅ Logout de Supabase completado")
            else:
                print("⚠️ No se pudo hacer logout de Supabase")
        except Exception as e:
            print(f"⚠️ Error en logout de Supabase: {e}")
            # Continuar con logout local aunque falle Supabase
        
        # ✅ LIMPIAR ESTADO LOCAL
        self.auth_token = ""
        self.is_logged_in = False
        self.logged_user_data = {}
        self.profile_data = {}
        
        print("🎉 Logout híbrido completado")
        return rx.redirect("/", replace=True)

    @rx.event
    def clear_login_form(self):
        """Limpia formulario de login."""
        self.username = ""
        self.email = ""
        self.password = ""
        self.error_message = ""
        self.is_loading = False

    @rx.event
    def random_username(self):
        """Genera nombre de usuario aleatorio."""
        first_part = UserDataManager.extract_first_word(self.new_user_firstname)
        last_part = UserDataManager.extract_first_word(self.new_user_lastname)
        random_number = random.randint(100, 999)
        self.new_username = f"{first_part.lower()}{last_part.lower()}{random_number}"

    def _validate_registration_data(self) -> bool:
        """Valida datos de registro."""
        # Validar complejidad de contraseña
        is_valid, error_msg = PasswordValidator.validate_complexity(self.new_password)
        if not is_valid:
            self.error_message = error_msg
            return False

        if self.new_password != self.new_confirmed_password:
            self.error_message = "Las contraseñas no coinciden."
            return False
        
        required_fields = [
            self.new_username, self.new_email, self.new_password, 
            self.new_user_firstname, self.new_user_lastname, self.new_terms_accepted
        ]
        if not all(required_fields):
            self.error_message = "Faltan campos obligatorios."
            return False
        
        # Validar dirección si se proporcionó
        if self.new_street_number or self.new_city or self.new_country:
            address_fields = [self.new_street_number, self.new_city, self.new_country]
            if not all(address_fields):
                self.error_message = "Si proporciona dirección, complete todos los campos obligatorios."
                return False
        
        return True

    def _clear_registration_form(self):
        """Limpia formulario de registro."""
        self.new_username = ""
        self.new_email = ""
        self.new_password = ""
        self.new_confirmed_password = ""
        self.new_user_firstname = ""
        self.new_user_lastname = ""
        self.new_gender = ""
        self.new_phone_number = ""
        self.new_terms_accepted = False
        self.new_street_number = ""
        self.new_neighborhood = ""
        self.new_city = ""
        self.new_zip_code = ""
        self.new_country = ""
        self.new_state = ""


# Clase para compatibilidad futura con Supabase Auth
class AuthStateSupabase(rx.State):
    """Estado preparado para migración a Supabase Auth."""
    
    # Estados básicos
    is_loading: bool = False
    error_message: str = ""
    is_logged_in: bool = False
    user_data: dict = {}
    
    # Campos de login
    email: str = ""
    password: str = ""
    
    # Campos de registro
    new_email: str = ""
    new_password: str = ""
    new_firstname: str = ""
    new_lastname: str = ""

    @rx.event
    async def login_with_supabase(self):
        """Login usando Supabase Auth (preparado para implementación futura)."""
        self.is_loading = True
        self.error_message = ""
        yield
        
        try:
            # TODO: Implementar integración con Supabase Auth
            # response = supabase.auth.sign_in_with_password({
            #     "email": self.email,
            #     "password": self.password
            # })
            
            self.error_message = "Integración con Supabase Auth pendiente de implementación."
            
        except Exception as e:
            self.error_message = f"Error de login: {str(e)}"
            
        finally:
            self.is_loading = False

    @rx.event 
    async def register_with_supabase(self):
        """Registro usando Supabase Auth (preparado para implementación futura)."""
        self.is_loading = True
        self.error_message = ""
        yield
        
        try:
            # TODO: Implementar integración con Supabase Auth
            # response = supabase.auth.sign_up({
            #     "email": self.new_email,
            #     "password": self.new_password,
            #     "options": {
            #         "data": {
            #             "first_name": self.new_firstname,
            #             "last_name": self.new_lastname,
            #         }
            #     }
            # })
            
            self.error_message = "Integración con Supabase Auth pendiente de implementación."
                
        except Exception as e:
            self.error_message = f"Error de registro: {str(e)}"
            
        finally:
            self.is_loading = False

    @rx.event
    def logout_supabase(self):
        """Logout usando Supabase."""
        try:
            # TODO: Implementar logout con Supabase
            # supabase.auth.sign_out()
            self.is_logged_in = False
            self.user_data = {}
            
        except Exception as e:
            print(f"DEBUG: Error en logout: {e}")
            
        return rx.redirect("/", replace=True)

    @rx.event
    def check_supabase_session(self):
        """Verifica sesión de Supabase."""
        try:
            # TODO: Implementar verificación de sesión con Supabase
            # session = supabase.auth.get_session()
            self.is_logged_in = False
            self.user_data = {}
                
        except Exception as e:
            print(f"DEBUG: Error verificando sesión: {e}")
            self.is_logged_in = False