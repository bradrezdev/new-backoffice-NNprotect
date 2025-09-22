import reflex as rx
import bcrypt
import jwt
import datetime
import sqlmodel
from database.users import Users, UserStatus, UserGender
from database.auth_credentials import AuthCredentials
from database.roles import Roles
from database.userprofiles import UserProfiles
from database.social_accounts import SocialAccounts
from database.roles_users import RolesUsers

class AuthState(rx.State):
    """State para manejar la autenticación del usuario."""
    is_loading: bool = False
    error_message: str = ""
    
    """State para manejar la autenticación del usuario."""
    
    # Datos del perfil
    user_id: int = 0
    user_fullname: str = ""
    gender: str = ""
    phone_number: str = ""

    # Datos de autenticación
    username: str = ""
    email: str = ""
    password: str = ""
    confirmed_password: str = ""
    terms_accepted: bool = False

    # Sesión
    auth_token: str = rx.Cookie(name="auth_token", secure=False, same_site="Lax")
    logged_user_data: dict = {}
    is_logged_in: bool = False

    profile_data: dict = {}
    social_accounts: list = []

    # Setters y getters
    @rx.event
    def set_fullname(self, fullname: str):
        self.user_fullname = fullname

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
        if self.password != self.confirmed_password:
            self.error_message = "Las contraseñas no coinciden."
            return False
        
        required_fields = [self.username, self.email, self.password, 
                          self.user_fullname, self.terms_accepted]
        if not all(required_fields):
            self.error_message = "Faltan campos obligatorios."
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
            status="NO_QUALIFIED",
            referral_code=f"{member_id:05d}",
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        with rx.session() as session:
            session.add(new_user)
            session.commit()  # Commit intermedio para obtener el ID
            session.refresh(new_user)  # Obtener el ID autogenerado
        return new_user

    def _create_auth_credentials(self, session, user_id: int):
        """Crea las credenciales de autenticación con contraseña hasheada."""
        # Hashear la contraseña (usando bcrypt como en el ejemplo anterior)
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        
        new_credentials = AuthCredentials(
            user_id=user_id,
            password_hash=hashed_password.decode('utf-8')
        )
        with rx.session() as session:
            session.add(new_credentials)

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
            with rx.session() as session:
                session.add(user_role)
                print(f"DEBUG: Rol {user_role.role_id} agregado al usuario {user_role.user_id}")
        else:
            raise Exception("Rol por defecto 'user' no encontrado en la base de datos.")

    def _create_user_profile(self, session, user_id: int):
        """Crea el perfil detallado del usuario."""
        # Convertir gender string a enum
        if self.gender.lower() == "masculino":
            gender_enum = UserGender.MALE
        elif self.gender.lower() == "femenino":
            gender_enum = UserGender.FEMALE
        else:
            gender_enum = UserGender.OTHER
            
        new_profile = UserProfiles(
            user_id=user_id,
            fullname=self.user_fullname,
            gender=gender_enum,
            phone_number=self.phone_number
        )
        with rx.session() as session:
            session.add(new_profile)

    def _create_social_accounts(self, session, user_id: int):
        """Crea un registro vacío de cuentas sociales."""
        # Por defecto, sin cuentas sociales conectadas
        social_accounts = SocialAccounts(
            user_id=user_id,
            # Los campos específicos (facebook_id, google_id, etc.) quedan None
        )
        with rx.session() as session:
            session.add(social_accounts)
            session.commit()

    def _clear_registration_form(self):
        """Limpia el formulario después del registro exitoso."""
        self.username = ""
        self.email = ""
        self.password = ""
        self.confirmed_password = ""
        self.user_fullname = ""
        self.gender = ""
        self.phone_number = ""
        self.terms_accepted = False