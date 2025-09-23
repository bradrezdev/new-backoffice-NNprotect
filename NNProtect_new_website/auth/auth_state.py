import reflex as rx
import bcrypt
import jwt
import datetime
import sqlmodel
import os
from dotenv import load_dotenv
from database.users import Users, UserStatus
from database.auth_credentials import AuthCredentials
from database.roles import Roles
from database.userprofiles import UserProfiles, UserGender
from database.social_accounts import SocialAccounts, SocialNetwork
from database.roles_users import RolesUsers
from database.addresses import Countries, Addresses
from database.users_addresses import UserAddresses

class AuthState(rx.State):
    """State para manejar la autenticación del usuario, registro y sesión."""
    is_loading: bool = False
    error_message: str = ""
    
    # --- Campos de Registro ---
    username: str = ""
    email: str = ""
    password: str = ""
    confirmed_password: str = ""
    user_firstname: str = ""
    user_lastname: str = ""
    phone_number: str = ""
    gender: str = ""
    terms_accepted: bool = False
    
    # Nuevos campos de dirección
    street_number: str = ""
    neighborhood: str = ""
    city: str = ""
    zip_code: str = ""
    country: str = ""
    state: str = ""

    # --- Campos de Sesión (fusionados desde la clase Login) ---
    auth_token: str = rx.Cookie(name="auth_token", secure=False, same_site="Lax")
    logged_user_data: dict = {}
    is_logged_in: bool = False
    
    # Setters para campos de dirección
    def set_street_number(self, value: str):
        self.street_number = value
    
    def set_neighborhood(self, value: str):
        self.neighborhood = value
    
    def set_city(self, value: str):
        self.city = value
    
    def set_zip_code(self, value: str):
        self.zip_code = value
    
    def set_country(self, value: str):
        self.country = value
        self.state = ""  # Resetear estado cuando cambie país
    
    def set_state(self, value: str):
        self.state = value
    
    COUNTRY_MAP = {
        "USA": "United States",
        "COLOMBIA": "Colombia",
        "MEXICO": "Mexico",
        "PUERTO_RICO": "Puerto Rico",
    }
    
    # Computed var para obtener lista de países amigables
    @rx.var
    def country_options(self) -> list[str]:
        """Lista de países disponibles para el usuario."""
        return list(self.COUNTRY_MAP.values())
    
    # Computed var para obtener estados del país seleccionado
    @rx.var
    def state_options(self) -> list[str]:
        """Lista de estados basada en el país seleccionado."""
        if not self.country:
            return []
        
        try:
            # Encontrar la clave del país a partir del valor amigable
            country_key = None
            for key, value in self.COUNTRY_MAP.items():
                if value == self.country:
                    country_key = key
                    break
            
            if country_key:
                selected_country = Countries[country_key]
                states = selected_country.states()
                return states if states is not None else []
            return []
        except:
            return []

    profile_data: dict = {}
    social_accounts: list = []

    # Setters y getters
    @rx.event
    def set_firstname(self, firstname: str):
        self.user_firstname = firstname

    @rx.event
    def set_lastname(self, lastname: str):
        self.user_lastname = lastname

    @rx.event
    def set_gender(self, gender: str):
        self.gender = gender

    @rx.event
    def set_phone_number(self, phone_number: str):
        self.phone_number = phone_number

    @rx.event
    def set_username(self, username: str):
        self.username = username

    @rx.event
    def set_email(self, email: str):
        self.email = email

    @rx.event
    def set_password(self, password: str):
        self.password = password

    @rx.event
    def set_confirmed_password(self, confirmed_password: str):
        self.confirmed_password = confirmed_password

    @rx.event
    def set_terms_accepted(self, terms_accepted: bool):
        self.terms_accepted = terms_accepted

    @rx.event
    def new_register(self):
        """Registrar un nuevo usuario con todos sus datos relacionados."""
        print("DEBUG: Iniciando proceso de registro...")
        self.is_loading = True
        self.error_message = ""

        # --- 1. Validaciones Previas ---
        if not self._validate_registration_data():
            print("DEBUG: Validación fallida")
            self.is_loading = False
            return

        print("DEBUG: Validación exitosa, procediendo con el registro...")
        try:
            with rx.session() as session:
                print("DEBUG: Sesión de base de datos abierta")
                # --- 2. Verificar duplicados ---
                if self._user_already_exists(session):
                    print("DEBUG: Usuario ya existe")
                    self.error_message = "El usuario ya existe."
                    self.is_loading = False
                    return

                # --- 3. Obtener el siguiente member_id ---
                new_member_id = self._get_next_member_id(session)
                print(f"DEBUG: Nuevo member_id obtenido: {new_member_id}")

                # --- 4. Crear TODOS los registros en orden de dependencia ---
                
                # 4a. Crear el usuario base (primero, porque otros dependen de él)
                print("DEBUG: Creando registro de usuario base...")
                new_user = self._create_user_record(session, new_member_id)
                print(f"DEBUG: Usuario creado con ID: {new_user.id}")
                
                # 4b. Crear las credenciales de autenticación
                print("DEBUG: Creando credenciales de autenticación...")
                self._create_auth_credentials(session, new_user.id)
                print("DEBUG: Credenciales creadas")
                
                # 4c. Asignar el rol por defecto
                print("DEBUG: Asignando rol por defecto...")
                self._assign_default_role(session, new_user.id)
                print("DEBUG: Rol asignado")
                
                # 4d. Crear el perfil del usuario
                print("DEBUG: Creando perfil de usuario...")
                self._create_user_profile(session, new_user.id)
                print("DEBUG: Perfil creado")
                
                # 4e. Crear registro de cuentas sociales (vacío por defecto)
                print("DEBUG: Creando registro de cuentas sociales...")
                self._create_social_accounts(session, new_user.id)
                print("DEBUG: Cuentas sociales creadas")

                # 4f. Crear dirección del usuario (si se proporcionaron datos)
                if self.street_number and self.city and self.country:
                    print("DEBUG: Creando dirección del usuario...")
                    self._create_user_address(session, new_user.id)
                    print("DEBUG: Dirección procesada")
                else:
                    print("DEBUG: Saltando creación de dirección - datos incompletos")

                # --- 5. Confirmar todos los cambios ---
                session.commit()
                print("DEBUG: Todos los cambios confirmados en la base de datos")

        except Exception as e:
            # Si algo falla, todo se revierte automáticamente
            print(f"DEBUG: Error durante el registro: {str(e)}")
            self.error_message = f"Error al registrar usuario: {str(e)}"
            self.is_loading = False
            return

        # --- 6. Éxito: limpiar estado y redirigir ---
        print("DEBUG: Registro exitoso, limpiando formulario y redirigiendo...")
        self._clear_registration_form()
        self.is_loading = False
        return rx.redirect("/", replace=True)

    # --- Métodos auxiliares para mantener el código organizado ---

    def _validate_registration_data(self) -> bool:
        """Valida que todos los datos requeridos estén presentes."""
        if self.password != self.confirmed_password:
            self.error_message = "Las contraseñas no coinciden."
            return False
        
        required_fields = [self.username, self.email, self.password, 
                          self.user_firstname, self.user_lastname, self.terms_accepted]
        if not all(required_fields):
            self.error_message = "Faltan campos obligatorios."
            return False
        
        # Validar campos de dirección si se proporcionaron
        if self.street_number or self.city or self.country:
            address_fields = [self.street_number, self.city, self.country]
            if not all(address_fields):
                self.error_message = "Si proporciona dirección, complete todos los campos obligatorios."
                return False
        
        return True

    def _user_already_exists(self, session) -> bool:
        """Verifica si el usuario ya existe."""
        return session.exec(
            sqlmodel.select(Users).where(
                (Users.username == self.username) | (Users.email == self.email)
            )
        ).first() is not None

    def _get_next_member_id(self, session) -> int:
        """Obtiene el siguiente member_id disponible."""
        last_user = session.exec(
            sqlmodel.select(Users).order_by(sqlmodel.desc(Users.member_id))
        ).first()
        return last_user.member_id + 1 if last_user else 1

    def _create_user_record(self, session, member_id: int) -> Users:
        """Crea el registro base del usuario."""
        new_user = Users(
            member_id=member_id,
            username=self.username,
            email=self.email,
            status=UserStatus.NO_QUALIFIED,  # Usar el enum correcto
            referral_code=f"{member_id:05d}",
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        session.add(new_user)  # Usar la sesión recibida
        session.commit()  # Commit intermedio para obtener el ID
        session.refresh(new_user)  # Obtener el ID autogenerado
        return new_user

    def _create_user_profile(self, session, user_id: int):
        """Crea el perfil detallado del usuario."""
        # Convertir gender string a enum con valores exactos del select
        if self.gender == "Masculino":  # Valor exacto del select
            gender_enum = UserGender.MALE
        elif self.gender == "Femenino":  # Valor exacto del select
            gender_enum = UserGender.FEMALE
        else:
            # Valor por defecto para casos no contemplados (vacío, "Seleccionar...", etc.)
            gender_enum = UserGender.MALE
            print(f"DEBUG: Género no reconocido '{self.gender}', usando MALE por defecto")
            
        new_profile = UserProfiles(
            user_id=user_id,
            first_name=self.user_firstname,
            last_name=self.user_lastname,
            gender=gender_enum,
            phone_number=self.phone_number
        )
        session.add(new_profile)
        print(f"DEBUG: Perfil creado con género: {gender_enum} (valor original: '{self.gender}')")

    def _create_auth_credentials(self, session, user_id: int):
        """Crea las credenciales de autenticación con contraseña hasheada."""
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        
        new_credentials = AuthCredentials(
            user_id=user_id,
            password_hash=hashed_password.decode('utf-8'),
            terms_accepted=self.terms_accepted
        )
        session.add(new_credentials)

    def _create_social_accounts(self, session, user_id: int):
        """Crea un registro de cuentas sociales con valores por defecto."""
        social_accounts = SocialAccounts(
            user_id=user_id,
            provider="none",
            url=""  # URL vacía por defecto
        )
        session.add(social_accounts)
        print("DEBUG: Cuentas sociales creadas.")

    def _assign_default_role(self, session, user_id: int):
        """Asigna el rol por defecto al usuario."""
        # Asumiendo que tienes un rol "USER" por defecto
        default_role = session.exec(
            sqlmodel.select(Roles).where(Roles.role_name == "USER")
        ).first()
        
        if default_role:
            user_role = RolesUsers(
                user_id=user_id,
                role_id=default_role.role_id
            )
            session.add(user_role)
            print(f"DEBUG: Rol {user_role.role_id} agregado al usuario {user_role.user_id}")
        else:
            raise Exception("Rol por defecto 'USER' no encontrado en la base de datos.")

    def _create_user_address(self, session, user_id: int):
        """Crea la dirección del usuario si se proporcionaron datos."""
        if not (self.street_number and self.city and self.country):
            print("DEBUG: No se proporcionaron datos de dirección, saltando creación")
            return
        
        try:
            # Encontrar la clave del país a partir del valor amigable
            country_key = None
            for key, value in self.COUNTRY_MAP.items():
                if value == self.country:
                    country_key = key
                    break
            
            if not country_key:
                raise ValueError(f"País '{self.country}' no es válido")
            
            country_enum = Countries[country_key]
            
            # Crear registro de dirección
            new_address = Addresses(
                street=self.street_number,
                number="",
                neighborhood=self.neighborhood or "",
                city=self.city,
                state=self.state or "",
                country=country_enum,
                zip_code=self.zip_code or ""
            )
            session.add(new_address)
            session.flush()  # Flush para verificar errores antes del commit final
            
            # Crear relación usuario-dirección
            user_address = UserAddresses(
                user_id=user_id,
                address_id=new_address.id,
                address_name="Principal",
                is_default=True,
                created_at=datetime.datetime.utcnow().isoformat(),
                updated_at=datetime.datetime.utcnow().isoformat()
            )
            session.add(user_address)
            
            print(f"DEBUG: Dirección creada exitosamente para usuario {user_id}")
            
        except Exception as e:
            print(f"DEBUG: Error al crear dirección: {str(e)}")
            session.rollback()
            print("DEBUG: Rollback realizado, continuando registro sin dirección")


    def _clear_registration_form(self):
        """Limpia el formulario después del registro exitoso."""
        self.username = ""
        self.email = ""
        self.password = ""
        self.confirmed_password = ""
        self.user_firstname = ""
        self.user_lastname = ""
        self.gender = ""
        self.phone_number = ""
        self.terms_accepted = False
        # Limpiar campos de dirección
        self.street_number = ""
        self.neighborhood = ""
        self.city = ""
        self.zip_code = ""
        self.country = ""
        self.state = ""

    # --- Métodos de Sesión (fusionados desde la clase Login) ---

    def _create_jwt_token(self, user: Users) -> str:
        """Crea un JWT token para el usuario autenticado."""
        load_dotenv()  # Cargar variables de entorno desde .env
        jwt_secret_key = os.environ.get("JWT_SECRET_KEY")

        login_token = {
            "id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # Token válido por 60 minutos
        }
        token = jwt.encode(login_token, jwt_secret_key, algorithm="HS256")
        return token.decode('utf-8') if isinstance(token, bytes) else token
        
    def _decode_jwt_token(self, token: str) -> dict:
        """Decodifica el JWT token para obtener los datos del usuario."""
        load_dotenv()  # Cargar variables de entorno desde .env
        jwt_secret_key = os.environ.get("JWT_SECRET_KEY")
        if not token:
            return {}
        try:
            decoded = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
            return decoded
        except jwt.ExpiredSignatureError:
            self.is_logged_in = False
            self.logged_user_data = {}
            self.auth_token = ""
            print("DEBUG: Token expirado")
            return {}
        except jwt.InvalidTokenError:
            self.is_logged_in = False
            self.logged_user_data = {}
            self.auth_token = ""
            print("DEBUG: Token inválido")
            return {}
        
    @rx.event
    def login_user(self):
        """Iniciar sesión del usuario y establecer el token de autenticación."""
        self.is_loading = True
        self.error_message = ""
        
        try:
            with rx.session() as session:
                user = session.exec(
                    sqlmodel.select(Users).where(Users.email == self.email)
                ).first()
                
                if not user:
                    print("DEBUG: Usuario no encontrado")
                    self.error_message = "Usuario no encontrado."
                    self.is_loading = False
                    return
                
                credentials = session.exec(
                    sqlmodel.select(AuthCredentials).where(AuthCredentials.user_id == user.id)
                ).first()
                
                if not credentials or not bcrypt.checkpw(self.password.encode('utf-8'), credentials.password_hash.encode('utf-8')):
                    print("DEBUG: Contraseña incorrecta")
                    self.error_message = "Usuario o contraseña incorrectos."
                    self.is_loading = False
                    return
                
                # Generar y almacenar el token JWT
                token = self._create_jwt_token(user)
                self.auth_token = token
                self.is_logged_in = True
                self.logged_user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "member_id": user.member_id,
                    "status": user.status.value
                }
        
        except Exception as e:
            print(f"DEBUG: Error inesperado durante el login: {str(e)}")
            self.error_message = "Ocurrió un error inesperado. Inténtalo de nuevo."
            self.is_loading = False
            return

        print(f"DEBUG: Usuario {self.username} ha iniciado sesión exitosamente")
        self.is_loading = False
        return rx.redirect("/dashboard", replace=True)

    @rx.event
    def load_user_from_token(self):
        """Carga los datos del usuario desde el token almacenado en cookies."""
        payload = self._decode_jwt_token(self.auth_token)
        if not payload:
            self.is_logged_in = False
            self.logged_user_data = {}
            return
        
        user_id = payload.get("id")
        with rx.session() as session:
            user = session.exec(
                sqlmodel.select(Users).where(Users.id == user_id)
            ).first()
            if user:
                self.is_logged_in = True
                self.logged_user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "member_id": user.member_id,
                    "status": user.status.value
                }
            else:
                self.is_logged_in = False
                self.logged_user_data = {}

        print(f"DEBUG: Datos del usuario cargados desde token: {self.logged_user_data}")

    @rx.event
    def check_login(self):
        """Verifica si el usuario está logueado basado en el token."""
        if self.auth_token:
            self.load_user_from_token()
        else:
            self.is_logged_in = False
            self.logged_user_data = {}
        print(f"DEBUG: Estado de login verificado: {self.is_logged_in}")

    @rx.event
    def logout_user(self):
        """Cierra la sesión del usuario y limpia el estado."""
        self.auth_token = ""
        self.is_logged_in = False
        self.logged_user_data = {}
        print("DEBUG: Usuario ha cerrado sesión")
        return rx.redirect("/login", replace=True)