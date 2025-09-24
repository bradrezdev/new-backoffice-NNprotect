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
    
    # --- Campos de Login ---
    username: str = ""
    email: str = ""
    password: str = ""
    
    # --- Campos de Registro (prefijo new_) ---
    new_username: str = ""
    new_email: str = ""
    new_password: str = ""
    new_confirmed_password: str = ""
    new_user_firstname: str = ""
    new_user_lastname: str = ""
    new_phone_number: str = ""
    new_gender: str = ""
    new_terms_accepted: bool = False
    
    # Campos de dirección para registro
    new_street_number: str = ""
    new_neighborhood: str = ""
    new_city: str = ""
    new_zip_code: str = ""
    new_country: str = ""
    new_state: str = ""

    # --- Campos de Sesión (fusionados desde la clase Login) ---
    auth_token: str = rx.Cookie(name="auth_token", secure=True, same_site="Lax")
    logged_user_data: dict = {}
    is_logged_in: bool = False
    profile_data: dict = {}
    
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
        if not self.new_country:
            return []
        
        try:
            # Encontrar la clave del país a partir del valor amigable
            country_key = None
            for key, value in self.COUNTRY_MAP.items():
                if value == self.new_country:
                    country_key = key
                    break
            
            if country_key:
                selected_country = Countries[country_key]
                states = selected_country.states()
                return states if states is not None else []
            return []
        except:
            return []
        
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

    # --- Setters para campos de registro (prefijo new_) ---
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
        self.new_state = ""  # Resetear estado cuando cambie país

    @rx.event
    def set_new_state(self, new_state: str):
        self.new_state = new_state

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

                if new_user and new_user.id:
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
                    if self.new_street_number and self.new_city and self.new_country:
                        print("DEBUG: Creando dirección del usuario...")
                        self._create_user_address(session, new_user.id)
                        print("DEBUG: Dirección procesada")
                    else:
                        print("DEBUG: Saltando creación de dirección - datos incompletos")
                else:
                    self.error_message = "No se pudo crear el usuario."
                    self.is_loading = False
                    return

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
        return rx.redirect("/dashboard", replace=True)

    # --- Métodos auxiliares para mantener el código organizado ---

    def _validate_registration_data(self) -> bool:
        """Valida que todos los datos requeridos estén presentes."""

        # ✅ NUEVA VALIDACIÓN DE COMPLEJIDAD DE CONTRASEÑA
        if not self._validate_password_complexity():
            return False

        if self.new_password != self.new_confirmed_password:
            self.error_message = "Las contraseñas no coinciden."
            return False
        
        required_fields = [self.new_username, self.new_email, self.new_password, 
                          self.new_user_firstname, self.new_user_lastname, self.new_terms_accepted]
        if not all(required_fields):
            self.error_message = "Faltan campos obligatorios."
            return False
        
        # Validar campos de dirección si se proporcionaron
        if self.new_street_number or self.new_city or self.new_country:
            address_fields = [self.new_street_number, self.new_city, self.new_country]
            if not all(address_fields):
                self.error_message = "Si proporciona dirección, complete todos los campos obligatorios."
                return False
        
        return True

    def _validate_password_complexity(self) -> bool:
        """Valida que la contraseña cumpla con los requisitos de complejidad."""
        import re
        
        password = self.new_password
        
        # Verificar longitud mínima
        if len(password) < 8:
            self.error_message = "La contraseña debe tener al menos 8 caracteres."
            return False
        
        # Verificar que tenga al menos una letra mayúscula
        if not re.search(r'[A-Z]', password):
            self.error_message = "La contraseña debe contener al menos una letra mayúscula."
            return False
        
        # Verificar que tenga al menos una letra minúscula
        if not re.search(r'[a-z]', password):
            self.error_message = "La contraseña debe contener al menos una letra minúscula."
            return False
        
        # Verificar que tenga al menos un número
        if not re.search(r'\d', password):
            self.error_message = "La contraseña debe contener al menos un número."
            return False
        
        # Verificar que tenga al menos un símbolo especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\];\'\\`~]', password):
            self.error_message = "La contraseña debe contener al menos un símbolo especial (!@#$%^&*...)."
            return False
        
        return True

    def _user_already_exists(self, session) -> bool:
        """Verifica si el usuario ya existe."""
        return session.exec(
            sqlmodel.select(Users).where(
                (Users.username == self.new_username) | (Users.email == self.new_email)
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
            username=self.new_username,
            email=self.new_email,
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
        if self.new_gender == "Masculino":  # Valor exacto del select
            gender_enum = UserGender.MALE
        elif self.new_gender == "Femenino":  # Valor exacto del select
            gender_enum = UserGender.FEMALE
        else:
            # Valor por defecto para casos no contemplados (vacío, "Seleccionar...", etc.)
            gender_enum = UserGender.MALE
            print(f"DEBUG: Género no reconocido '{self.new_gender}', usando MALE por defecto")
            
        new_profile = UserProfiles(
            user_id=user_id,
            first_name=self.new_user_firstname,
            last_name=self.new_user_lastname,
            gender=gender_enum,
            phone_number=self.new_phone_number
        )
        session.add(new_profile)
        print(f"DEBUG: Perfil creado con género: {gender_enum} (valor original: '{self.new_gender}')")

    def _create_auth_credentials(self, session, user_id: int):
        """Crea las credenciales de autenticación con contraseña hasheada."""
        hashed_password = bcrypt.hashpw(self.new_password.encode('utf-8'), bcrypt.gensalt())
        
        new_credentials = AuthCredentials(
            user_id=user_id,
            password_hash=hashed_password.decode('utf-8'),
            terms_accepted=self.new_terms_accepted
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
        if not (self.new_street_number and self.new_city and self.new_country):
            print("DEBUG: No se proporcionaron datos de dirección, saltando creación")
            return
        
        try:
            # Encontrar la clave del país a partir del valor amigable
            country_key = None
            for key, value in self.COUNTRY_MAP.items():
                if value == self.new_country:
                    country_key = key
                    break
            
            if not country_key:
                raise ValueError(f"País '{self.new_country}' no es válido")
            
            country_enum = Countries[country_key]
            
            # Crear registro de dirección
            new_address = Addresses(
                street=self.new_street_number,
                neighborhood=self.new_neighborhood or "",
                city=self.new_city,
                state=self.new_state or "",
                country=country_enum,
                zip_code=self.new_zip_code or ""
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
        self.new_username = ""
        self.new_email = ""
        self.new_password = ""
        self.new_confirmed_password = ""
        self.new_user_firstname = ""
        self.new_user_lastname = ""
        self.new_gender = ""
        self.new_phone_number = ""
        self.new_terms_accepted = False
        # Limpiar campos de dirección
        self.new_street_number = ""
        self.new_neighborhood = ""
        self.new_city = ""
        self.new_zip_code = ""
        self.new_country = ""
        self.new_state = ""

    # --- Métodos de Sesión (fusionados desde la clase Login) ---

    def _get_jwt_secret(self) -> str:
        """Obtiene la clave JWT con detección robusta de entorno."""
        # Detectar si estamos en producción
        is_production = (
            os.environ.get("REFLEX_ENV") == "prod" or 
            not os.path.exists(".env") or
            "reflex.dev" in os.environ.get("HOSTNAME", "")
        )
        
        if is_production:
            # En producción, usar clave hardcodeada
            jwt_secret = "cd3de0d6ca1fe14e1d1893137218613d76d63f88902412c204882deec8681d7b"
            print("DEBUG: Usando JWT secret de PRODUCCIÓN (hardcodeado)")
            return jwt_secret
        else:
            # En desarrollo, usar .env
            load_dotenv()
            jwt_secret = os.environ.get("JWT_SECRET_KEY")
            if not jwt_secret:
                print("DEBUG: JWT_SECRET_KEY no encontrada en .env, usando fallback")
                jwt_secret = "cd3de0d6ca1fe14e1d1893137218613d76d63f88902412c204882deec8681d7b"
            else:
                print("DEBUG: Usando JWT secret desde .env (desarrollo)")
            return jwt_secret

    def _create_jwt_token(self, user: Users) -> str:
        """Crea un JWT token para el usuario autenticado."""
        try:
            jwt_secret_key = self._get_jwt_secret()  # ✅ Ahora el método existe
            print(f"DEBUG: JWT Secret configurado correctamente")
            
            # Validar y convertir campos del usuario
            print(f"DEBUG: Datos del usuario para token - ID: {user.id} (tipo: {type(user.id)})")
            print(f"DEBUG: Username: {user.username} (tipo: {type(user.username)})")
            
            # Asegurar que todos los valores sean del tipo correcto
            user_id = int(user.id) if user.id is not None else 0
            username = str(user.username) if user.username is not None else "unknown"
            
            print(f"DEBUG: Valores convertidos - ID: {user_id}, Username: '{username}'")
            
            # Crear payload con tipos seguros
            login_token = {
                "id": user_id,
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),  # ✅ ÚNICO CAMBIO: quitar int() y .timestamp()
            }
            
            print(f"DEBUG: Payload del token: {login_token}")
            
            # Generar el token
            token = jwt.encode(login_token, jwt_secret_key, algorithm="HS256")
            
            # Manejar diferentes versiones de PyJWT
            if isinstance(token, bytes):
                token_str = token.decode('utf-8')
            else:
                token_str = str(token)
                
            print(f"DEBUG: Token generado exitosamente (longitud: {len(token_str)})")
            return token_str
            
        except Exception as e:
            print(f"DEBUG: Error detallado creando JWT token:")
            print(f"DEBUG: - Tipo de error: {type(e).__name__}")
            print(f"DEBUG: - Mensaje: {str(e)}")
            print(f"DEBUG: - user.id: {user.id} (tipo: {type(user.id)})")
            print(f"DEBUG: - user.username: {user.username} (tipo: {type(user.username)})")
            
            import traceback
            print(f"DEBUG: - Traceback: {traceback.format_exc()}")
            raise Exception(f"Error generando token JWT: {str(e)}")

    def _decode_jwt_token(self, token: str) -> dict:
        """Decodifica el JWT token para obtener los datos del usuario."""
        print(f"DEBUG _decode_jwt_token: Llamado con token longitud: {len(token) if token else 0}")
        
        if not token or "." not in token:
            print("DEBUG _decode_jwt_token: Token vacío o inválido")
            return {}
            
        try:
            jwt_secret_key = self._get_jwt_secret()
            decoded = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
            print(f"DEBUG _decode_jwt_token: Token decodificado exitosamente")
            return decoded
            
        except jwt.ExpiredSignatureError:
            print("DEBUG _decode_jwt_token: Token expirado - MANTENIENDO ESTADO")
            self.auth_token = ""  # Solo limpiar token
            # ✅ NO limpiar is_logged_in ni profile_data
            return {}
        except Exception as e:
            print(f"DEBUG _decode_jwt_token: Error: {e}")
            return {}

    @rx.event
    def login_user(self):
        """Iniciar sesión del usuario y establecer el token de autenticación."""
        self.is_loading = True
        self.error_message = ""
        
        print("DEBUG: Iniciando login_user...")
        print(f"DEBUG: Username: '{self.username}' (tipo: {type(self.username)})")
        print(f"DEBUG: Password length: {len(self.password) if self.password else 'None'}")
        
        # Validar que tenemos datos básicos
        if not self.username or not self.password:
            print("DEBUG: Username o password vacíos")
            self.error_message = "Por favor completa todos los campos."
            self.is_loading = False
            return
        
        # Convertir username a string explícitamente
        username_str = str(self.username).strip()
        password_str = str(self.password)
        
        try:
            print("DEBUG: Intentando abrir sesión de BD...")
            with rx.session() as session:
                print("DEBUG: Sesión de BD abierta exitosamente")
                
                print(f"DEBUG: Buscando usuario con username: '{username_str}'")
                user = session.exec(
                    sqlmodel.select(Users).where(Users.username == username_str)
                ).first()
                
                if not user:
                    print("DEBUG: Usuario no encontrado en la base de datos")
                    self.error_message = "Usuario no encontrado."
                    self.is_loading = False
                    return
                    
                print(f"DEBUG: Usuario encontrado - ID: {user.id}, Username: {user.username}")
                
                # Verificar que el usuario tenga los campos necesarios
                if not hasattr(user, 'id') or user.id is None:
                    print("DEBUG: Usuario sin ID válido")
                    self.error_message = "Error en datos del usuario."
                    self.is_loading = False
                    return
                
                print("DEBUG: Buscando credenciales del usuario...")
                credentials = session.exec(
                    sqlmodel.select(AuthCredentials).where(AuthCredentials.user_id == user.id)
                ).first()
                
                if not credentials:
                    print("DEBUG: No se encontraron credenciales para el usuario")
                    self.error_message = "Error de autenticación."
                    self.is_loading = False
                    return
                
                # Verificar que las credenciales tengan hash válido
                if not credentials.password_hash or not isinstance(credentials.password_hash, str):
                    print(f"DEBUG: Hash de contraseña inválido - tipo: {type(credentials.password_hash)}, valor: {credentials.password_hash}")
                    self.error_message = "Error en credenciales."
                    self.is_loading = False
                    return
                    
                print("DEBUG: Verificando contraseña...")
                try:
                    # Asegurar que ambos valores sean strings
                    password_bytes = password_str.encode('utf-8')
                    hash_bytes = credentials.password_hash.encode('utf-8')
                    
                    password_match = bcrypt.checkpw(password_bytes, hash_bytes)
                    print(f"DEBUG: Resultado verificación contraseña: {password_match}")
                    
                except Exception as bcrypt_error:
                    print(f"DEBUG: Error en bcrypt.checkpw: {str(bcrypt_error)}")
                    print(f"DEBUG: Tipo password_hash: {type(credentials.password_hash)}")
                    print(f"DEBUG: Contenido password_hash: {repr(credentials.password_hash)}")
                    self.error_message = "Error al verificar contraseña."
                    self.is_loading = False
                    return
                
                if not password_match:
                    print("DEBUG: Contraseña incorrecta")
                    self.error_message = "Contraseña incorrecta."
                    self.is_loading = False
                    return
                
                print("DEBUG: Contraseña correcta, generando token...")
                
                # Generar token con validaciones
                try:
                    token = self._create_jwt_token(user)
                    if not token or not isinstance(token, str):
                        print(f"DEBUG: Token generado inválido - tipo: {type(token)}, valor: {token}")
                        raise Exception("Token inválido generado")
                        
                except Exception as token_error:
                    print(f"DEBUG: Error generando token: {str(token_error)}")
                    self.error_message = "Error generando sesión."
                    self.is_loading = False
                    return
                
                # Establecer datos de sesión con validaciones
                try:
                    self.auth_token = token
                    self.is_logged_in = True
                    
                    # Construir datos del usuario con validaciones
                    user_data = {
                        "id": int(user.id) if user.id is not None else 0,
                        "username": str(user.username) if user.username is not None else "",
                        "email": str(user.email) if user.email is not None else "",
                        "member_id": int(user.member_id) if user.member_id is not None else 0,
                    }
                    
                    # Manejar status que puede ser enum o string
                    if hasattr(user, 'status') and user.status is not None:
                        if hasattr(user.status, 'value'):
                            user_data["status"] = str(user.status.value)
                        else:
                            user_data["status"] = str(user.status)
                    else:
                        user_data["status"] = "UNKNOWN"
                    
                    self.logged_user_data = user_data
                    print(f"DEBUG: Datos de usuario establecidos: {user_data}")
                    
                except Exception as data_error:
                    print(f"DEBUG: Error estableciendo datos de usuario: {str(data_error)}")
                    self.error_message = "Error configurando sesión."
                    self.is_loading = False
                    return
        
        except Exception as e:
            print(f"DEBUG: Error completo durante el login: {str(e)}")
            print(f"DEBUG: Tipo de error: {type(e).__name__}")
            import traceback
            print(f"DEBUG: Traceback completo: {traceback.format_exc()}")
            self.error_message = f"Error de conexión: {str(e)}"
            self.is_loading = False
            return

        print(f"DEBUG: Login exitoso para usuario {username_str}")
        self.is_loading = False
        self.clear_login_form()
        return rx.redirect("/dashboard", replace=True)

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
            return username  # Fallback final
        
    @rx.event
    def clear_login_form(self):
        """Limpia los campos del formulario de login."""
        self.username = ""
        self.email = ""
        self.password = ""
        self.error_message = ""
        self.is_loading = False

    @rx.event
    def load_user_from_token(self):
        """Carga los datos completos del usuario desde el token almacenado en cookies."""
        payload = self._decode_jwt_token(self.auth_token)
        if not payload:
            #self.is_logged_in = False
            #self.logged_user_data = {}
            #self.profile_data = {}
            return
        
        user_id = payload.get("id")
        with rx.session() as session:
            # Obtener datos del usuario
            user = session.exec(
                sqlmodel.select(Users).where(Users.id == user_id)
            ).first()
            
            if not user:
                self.is_logged_in = False
                self.logged_user_data = {}
                self.profile_data = {}
                return
            
            # Obtener datos del perfil
            user_profile = session.exec(
                sqlmodel.select(UserProfiles).where(UserProfiles.user_id == user_id)
            ).first()
            
            # Construir profile_name usando la función helper
            profile_name = self._build_profile_name(
                user_profile.first_name if user_profile else "",
                user_profile.last_name if user_profile else "",
                user.username
            )
            
            print(f"DEBUG: Profile name construido: '{profile_name}'")
            print(f"DEBUG: - De '{user_profile.first_name if user_profile else 'N/A'}' y '{user_profile.last_name if user_profile else 'N/A'}'")
            
            # Establecer datos básicos de sesión
            self.is_logged_in = True
            self.logged_user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "member_id": user.member_id,
                "status": user.status.value if hasattr(user.status, 'value') else str(user.status)
            }
            
            # Establecer datos extendidos del perfil
            self.profile_data = {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "member_id": user.member_id,
                "firstname": user_profile.first_name if user_profile else "",
                "lastname": user_profile.last_name if user_profile else "",
                "phone": user_profile.phone_number if user_profile else "",
                "gender": user_profile.gender.value if user_profile and hasattr(user_profile.gender, 'value') else "",
                "created_at": user.created_at.strftime("%d/%m/%Y") if user.created_at else "",
                "profile_name": profile_name  # ✅ Cambio: ahora se llama profile_name y solo primeras palabras
            }

        print(f"DEBUG: Datos completos del usuario cargados: {self.profile_data}")

    @rx.var
    def get_user_display_name(self) -> str:
        """Retorna el nombre a mostrar del usuario."""
        # ✅ AGREGAR DEBUG para ver qué está pasando
        print(f"DEBUG get_user_display_name: profile_data = {self.profile_data}")
        print(f"DEBUG get_user_display_name: is_logged_in = {self.is_logged_in}")
        
        if not self.profile_data or not isinstance(self.profile_data, dict):
            print("DEBUG get_user_display_name: Retornando 'Usuario' - no hay profile_data")
            return "Usuario"
        
        profile_name = self.profile_data.get("profile_name", "")
        if profile_name:
            print(f"DEBUG get_user_display_name: Retornando profile_name: {profile_name}")
            return profile_name
        
        username = self.profile_data.get("username", "")
        if username:
            print(f"DEBUG get_user_display_name: Retornando username: {username}")
            return username
            
        print("DEBUG get_user_display_name: Retornando 'Usuario' - sin datos válidos")
        return "Usuario"

    @rx.event
    def user_profile_data(self):
        """Devuelve los datos del perfil del usuario."""
        return self.user_profile_data

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
        return rx.redirect("/", replace=True)