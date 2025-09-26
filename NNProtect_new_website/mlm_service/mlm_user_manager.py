"""
Manager para datos MLM de usuarios - SEPARADO de autenticación Supabase.
Se enfoca únicamente en la lógica de negocio multinivel.
"""
import reflex as rx
import sqlmodel
from typing import Optional, Dict, Any
from database.users import Users, UserStatus

# Timezone utilities
from ..utils.timezone_mx import get_mexico_datetime_naive, format_mexico_date, format_mexico_datetime, get_mexico_date, convert_to_mexico_time
from datetime import timedelta
from database.userprofiles import UserProfiles, UserGender
from database.social_accounts import SocialAccounts, SocialNetwork
from database.roles import Roles
from database.roles_users import RolesUsers
from database.auth_credentials import AuthCredentials
from database.usertreepaths import UserTreePath
import os

class MLMUserManager:
    """Maneja datos MLM separados de la autenticación Supabase."""
    
    @staticmethod
    def get_next_member_id(session) -> int:
        """Obtiene el siguiente member_id disponible."""
        last_user = session.exec(
            sqlmodel.select(Users).order_by(sqlmodel.desc(Users.member_id))
        ).first()
        return last_user.member_id + 1 if last_user else 1

    @staticmethod
    def create_mlm_user(session, supabase_user_id: str, first_name: str, 
                       last_name: str, email: str, sponsor_member_id: Optional[int] = None) -> Users:
        """
        Crea registro MLM para usuario autenticado en Supabase.
        NO maneja autenticación - solo datos de negocio.
        """
        try:
            member_id = MLMUserManager.get_next_member_id(session)
            
            # Convertir sponsor_member_id a sponsor_id (users.id)
            sponsor_id = None
            if sponsor_member_id and sponsor_member_id > 0:
                sponsor = session.exec(
                    sqlmodel.select(Users).where(Users.member_id == sponsor_member_id)
                ).first()
                if sponsor:
                    sponsor_id = sponsor.id
            
            # Crear registro MLM
            new_user = Users(
                supabase_user_id=supabase_user_id,
                member_id=member_id,
                first_name=first_name,
                last_name=last_name,
                email_cache=email,
                sponsor_id=sponsor_id,
                status=UserStatus.NO_QUALIFIED
            )
            session.add(new_user)
            session.flush()
            
            # Crear entrada en UserTreePath si hay sponsor
            if sponsor_member_id and sponsor_member_id > 0:
                user_tree_path = UserTreePath(
                    sponsor_id=sponsor_member_id,  # member_id del sponsor
                    user_id=member_id              # member_id del nuevo usuario
                )
                session.add(user_tree_path)
                print(f"✅ UserTreePath creado - Sponsor ID: {sponsor_member_id}, User ID: {member_id}")
            
            # Generar referral link
            base_url = MLMUserManager.get_base_url()
            new_user.referral_link = f"{base_url}?ref={member_id}"
            
            print(f"✅ Usuario MLM creado - Member ID: {member_id}, Sponsor ID: {sponsor_id}")
            return new_user
            
        except Exception as e:
            print(f"❌ Error creando usuario MLM: {e}")
            raise

    @staticmethod
    def get_user_by_supabase_id(supabase_user_id: str) -> Optional[Users]:
        """Obtiene usuario MLM por su ID de Supabase."""
        try:
            with rx.session() as session:
                return session.exec(
                    sqlmodel.select(Users).where(Users.supabase_user_id == supabase_user_id)
                ).first()
        except Exception as e:
            print(f"❌ Error obteniendo usuario MLM: {e}")
            return None

    @staticmethod
    def get_user_by_member_id(member_id: int) -> Optional[Users]:
        """Obtiene usuario MLM por member_id."""
        try:
            with rx.session() as session:
                return session.exec(
                    sqlmodel.select(Users).where(Users.member_id == member_id)
                ).first()
        except Exception as e:
            print(f"❌ Error obteniendo usuario por member_id: {e}")
            return None

    @staticmethod
    def validate_sponsor_by_member_id(member_id: int) -> bool:
        """Verifica si existe un sponsor válido."""
        return MLMUserManager.get_user_by_member_id(member_id) is not None

    @staticmethod
    def create_user_profile(session, user_id: int, phone: str, gender: str):
        """Crea perfil extendido del usuario."""
        gender_enum = UserGender.MALE if gender == "Masculino" else UserGender.FEMALE
        
        profile = UserProfiles(
            user_id=user_id,
            gender=gender_enum,
            phone_number=phone
        )
        session.add(profile)
        print(f"✅ Perfil MLM creado para usuario {user_id}")

    @staticmethod
    def create_social_accounts(session, user_id: int):
        """Crea registro de redes sociales."""
        # Temporal: No crear registro social por defecto para evitar enum error
        pass

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
            print(f"✅ Rol asignado al usuario MLM {user_id}")
        else:
            print("⚠️ Rol 'USER' no encontrado, continuando sin rol")

    @staticmethod
    def create_legacy_auth_credentials(session, user_id: int):
        """Crea credenciales legacy para compatibilidad (sin contraseña real)."""
        try:
            credentials = AuthCredentials(
                user_id=user_id,
                password_hash="supabase_managed",  # Marcador para indicar que Supabase maneja auth
                terms_accepted=True
            )
            session.add(credentials)
            print(f"✅ Credenciales legacy creadas para usuario {user_id}")
        except Exception as e:
            print(f"⚠️ No se pudieron crear credenciales legacy: {e}")

    @staticmethod
    def get_base_url() -> str:
        """URL base para referral links."""
        is_production = (
            os.environ.get("REFLEX_ENV") == "prod" or 
            not os.path.exists(".env")
        )
        return "https://codebradrez.tech/register" if is_production else "http://localhost:3000/register"

    @staticmethod
    def load_complete_user_data(supabase_user_id: str) -> dict:
        """Carga datos completos del usuario MLM usando supabase_user_id."""
        try:
            print(f"🔄 Buscando datos MLM para Supabase ID: {supabase_user_id}")
            
            with rx.session() as session:
                user = session.exec(
                    sqlmodel.select(Users).where(Users.supabase_user_id == supabase_user_id)
                ).first()
                
                if not user:
                    print(f"❌ Usuario MLM no encontrado con supabase_user_id: {supabase_user_id}")
                    return {}
                
                print(f"✅ Usuario MLM encontrado: ID={user.id}, Member ID={user.member_id}")
                
                # Cargar perfil con manejo seguro
                user_profile = session.exec(
                    sqlmodel.select(UserProfiles).where(UserProfiles.user_id == user.id)
                ).first()
                
                # ✅ CORRECCIÓN: Los nombres están en Users, no en UserProfiles
                first_name = user.first_name if user.first_name else ''
                last_name = user.last_name if user.last_name else ''
                phone_number = user_profile.phone_number if user_profile else ''
                gender_value = ''
                
                if user_profile and user_profile.gender:
                    gender_value = user_profile.gender.value if hasattr(user_profile.gender, 'value') else str(user_profile.gender)
                
                # Construir nombres optimizados
                full_name = f"{first_name} {last_name}".strip() if first_name or last_name else f"Usuario {user.member_id}"
                
                # Profile name con primeras palabras solamente
                first_word = first_name.split()[0] if first_name and first_name.split() else ""
                last_word = last_name.split()[0] if last_name and last_name.split() else ""
                
                if first_word and last_word:
                    profile_name = f"{first_word} {last_word}"
                elif first_word:
                    profile_name = first_word
                elif last_word:
                    profile_name = last_word
                else:
                    profile_name = f"Usuario {user.member_id}"
                
                # Datos de retorno completos
                mlm_data = {
                    "id": user.id,
                    "username": f"user{user.member_id}",  # Username generado basado en member_id
                    "member_id": user.member_id,
                    "status": user.status.value if hasattr(user.status, 'value') else str(user.status),
                    "firstname": first_name,
                    "lastname": last_name,
                    "full_name": full_name,  # ✅ NUEVO: Nombre completo
                    "profile_name": profile_name,  # ✅ MEJORADO: Solo primeras palabras
                    "email": user.email_cache or '',  # ✅ NUEVO: Email del usuario
                    "phone": phone_number,
                    "gender": gender_value,
                    "referral_link": user.referral_link,
                    "sponsor_id": user.sponsor_id,
                    "created_at": format_mexico_date(user.created_at) if user.created_at else '',  # ✅ MÉXICO TIMEZONE
                    "created_at_iso": user.created_at.isoformat() if user.created_at else '',  # ✅ NUEVO: Formato ISO  
                    "last_login": format_mexico_datetime(user.updated_at) if user.updated_at else '',  # ✅ MÉXICO TIMEZONE
                }
                
                # ✅ NUEVO: Cargar datos del sponsor
                sponsor_data = MLMUserManager.load_sponsor_data(session, user)
                mlm_data["sponsor_data"] = sponsor_data
                
                print(f"✅ Datos MLM cargados exitosamente para {profile_name}")
                if sponsor_data:
                    print(f"✅ Datos de sponsor cargados: {sponsor_data.get('profile_name', 'N/A')}")
                
                return mlm_data
                
        except Exception as e:
            print(f"❌ Error detallado en load_complete_user_data: {str(e)}")
            import traceback
            traceback.print_exc()
            return {}

    @staticmethod
    def load_sponsor_data(session, user: Users) -> dict:
        """Carga datos completos del sponsor de un usuario."""
        try:
            if not user.sponsor_id:
                return {}
            
            # JOIN para obtener datos del sponsor
            sponsor = session.exec(
                sqlmodel.select(Users).where(Users.id == user.sponsor_id)
            ).first()
            
            if not sponsor:
                return {}
            
            # Cargar perfil del sponsor
            sponsor_profile = session.exec(
                sqlmodel.select(UserProfiles).where(UserProfiles.user_id == sponsor.id)
            ).first()
            
            # Construir datos del sponsor
            first_name = sponsor.first_name if sponsor.first_name else ''
            last_name = sponsor.last_name if sponsor.last_name else ''
            phone_number = sponsor_profile.phone_number if sponsor_profile else ''
            gender_value = ''
            
            if sponsor_profile and sponsor_profile.gender:
                gender_value = sponsor_profile.gender.value if hasattr(sponsor_profile.gender, 'value') else str(sponsor_profile.gender)
            
            # Construir nombres del sponsor
            full_name = f"{first_name} {last_name}".strip() if first_name or last_name else f"Usuario {sponsor.member_id}"
            
            first_word = first_name.split()[0] if first_name and first_name.split() else ""
            last_word = last_name.split()[0] if last_name and last_name.split() else ""
            
            if first_word and last_word:
                profile_name = f"{first_word} {last_word}"
            elif first_word:
                profile_name = first_word
            elif last_word:
                profile_name = last_word
            else:
                profile_name = f"Usuario {sponsor.member_id}"
            
            sponsor_data = {
                "id": sponsor.id,
                "member_id": sponsor.member_id,
                "username": f"user{sponsor.member_id}",
                "firstname": first_name,
                "lastname": last_name,
                "full_name": full_name,
                "profile_name": profile_name,
                "email": sponsor.email_cache or '',
                "phone": phone_number,
                "gender": gender_value,
                "referral_link": sponsor.referral_link or '',
                "created_at": format_mexico_date(sponsor.created_at) if sponsor.created_at else '',
                "status": sponsor.status.value if hasattr(sponsor.status, 'value') else str(sponsor.status),
            }
            
            return sponsor_data
            
        except Exception as e:
            print(f"❌ Error cargando datos del sponsor: {str(e)}")
            return {}

    @staticmethod
    def create_user_address(session, user_id: int, street: str, neighborhood: str, 
                           city: str, state: str, country: str, zip_code: str):
        """Crea dirección del usuario."""
        from database.addresses import Addresses, Countries
        from database.users_addresses import UserAddresses
        import datetime
        
        try:
            # Mapeo de países
            COUNTRY_MAP = {
                "United States": "USA",
                "Colombia": "COLOMBIA", 
                "Mexico": "MEXICO",
                "Puerto Rico": "PUERTO_RICO",
            }
            
            # Obtener enum del país
            country_key = COUNTRY_MAP.get(country)
            if not country_key:
                print(f"⚠️ País '{country}' no encontrado en mapeo")
                return
            
            country_enum = Countries[country_key]
            
            # Crear dirección
            new_address = Addresses(
                street=street,
                neighborhood=neighborhood or "",
                city=city,
                state=state or "",
                country=country_enum,
                zip_code=zip_code or ""
            )
            session.add(new_address)
            session.flush()
            
            # Crear vinculación usuario-dirección
            user_address = UserAddresses(
                user_id=user_id,
                address_id=new_address.id,
                address_name="Principal",
                is_default=True,
                created_at=get_mexico_datetime_naive().isoformat(),  # ✅ MÉXICO TIMEZONE
                updated_at=get_mexico_datetime_naive().isoformat()  # ✅ MÉXICO TIMEZONE
            )
            session.add(user_address)
            print(f"✅ Dirección creada para usuario {user_id}")
            
        except Exception as e:
            print(f"❌ Error creando dirección: {e}")
            # No fallar el registro completo por error de dirección
    
    @staticmethod
    def get_user_level(user_member_id: int, root_sponsor_id: int) -> int:
        """
        Calcula el nivel de un usuario respecto a un sponsor raíz usando BFS.
        
        Args:
            user_member_id: member_id del usuario a evaluar
            root_sponsor_id: member_id del sponsor raíz (usuario autenticado)
            
        Returns:
            int: Nivel del usuario (1, 2, 3, etc.) o 0 si no está en la red
        """
        try:
            if user_member_id == root_sponsor_id:
                return 0  # El sponsor raíz es nivel 0
            
            with rx.session() as session:
                # BFS desde el sponsor raíz hacia abajo
                from collections import deque
                
                # Cola: (member_id, nivel)
                queue = deque([(root_sponsor_id, 0)])
                visited = set([root_sponsor_id])
                
                while queue:
                    current_id, current_level = queue.popleft()
                    
                    # Buscar todos los usuarios directos de current_id
                    direct_users = session.exec(
                        sqlmodel.select(UserTreePath)
                        .where(UserTreePath.sponsor_id == current_id)
                    ).all()
                    
                    for tree_path in direct_users:
                        child_id = tree_path.user_id
                        child_level = current_level + 1
                        
                        # Si encontramos al usuario buscado
                        if child_id == user_member_id:
                            print(f"✅ Usuario {user_member_id} encontrado en nivel {child_level} de {root_sponsor_id}")
                            return child_level
                        
                        # Si no lo hemos visitado, agregarlo a la cola
                        if child_id not in visited:
                            visited.add(child_id)
                            queue.append((child_id, child_level))
                
                # Usuario no encontrado en la red
                print(f"⚠️ Usuario {user_member_id} no encontrado en la red de {root_sponsor_id}")
                return 0
                
        except Exception as e:
            print(f"❌ Error calculando nivel de usuario {user_member_id}: {e}")
            import traceback
            traceback.print_exc()
            return 0

    @staticmethod
    def get_network_descendants(sponsor_member_id: int, root_user_id: Optional[int] = None) -> list:
        """
        Obtiene toda la red descendente de un sponsor usando UserTreePath.
        
        Args:
            sponsor_member_id: member_id del sponsor principal
            root_user_id: member_id del usuario autenticado (para calcular niveles)
            
        Returns:
            Lista de diccionarios con datos de usuarios descendentes
        """
        try:
            with rx.session() as session:
                descendants = []
                
                # Buscar todos los paths que tienen como sponsor_id el member_id dado
                tree_paths = session.exec(
                    sqlmodel.select(UserTreePath)
                    .where(UserTreePath.sponsor_id == sponsor_member_id)
                ).all()
                
                for tree_path in tree_paths:
                    # Buscar el usuario correspondiente por member_id
                    user = session.exec(
                        sqlmodel.select(Users).where(Users.member_id == tree_path.user_id)
                    ).first()
                    
                    if not user:
                        continue
                    # Cargar perfil del usuario
                    user_profile = session.exec(
                        sqlmodel.select(UserProfiles).where(UserProfiles.user_id == user.id)
                    ).first()
                    
                    # Cargar información del patrocinador
                    sponsor_data = {}
                    if sponsor_member_id:
                        sponsor = session.exec(
                            sqlmodel.select(Users).where(Users.member_id == sponsor_member_id)
                        ).first()
                        if sponsor:
                            sponsor_profile = session.exec(
                                sqlmodel.select(UserProfiles).where(UserProfiles.user_id == sponsor.id)
                            ).first()
                            sponsor_data = {
                                "id": sponsor.id,
                                "member_id": sponsor.member_id,
                                "first_name": sponsor.first_name or "",
                                "last_name": sponsor.last_name or "",
                                "full_name": f"{sponsor.first_name or ''} {sponsor.last_name or ''}".strip(),
                                "phone": sponsor_profile.phone_number if sponsor_profile else "",
                                "email": sponsor.email_cache or ""
                            }
                    
                    # Formatear fecha a DD/MM/YYYY
                    formatted_date = user.created_at.strftime("%d/%m/%Y") if user.created_at else "N/A"
                    
                    # Calcular nivel del usuario respecto al usuario raíz autenticado
                    actual_root_id = root_user_id if root_user_id is not None else sponsor_member_id
                    user_level = MLMUserManager.get_user_level(user.member_id, actual_root_id)
                    
                    user_data = {
                        "id": user.id,
                        "member_id": user.member_id,
                        "first_name": user.first_name or "",
                        "last_name": user.last_name or "",
                        "full_name": f"{user.first_name or ''} {user.last_name or ''}".strip() if (user.first_name or user.last_name) else "N/A",
                        "email": user.email_cache or "",
                        "status": user.status.value if hasattr(user.status, 'value') else str(user.status),
                        "created_at": formatted_date,
                        "phone": user_profile.phone_number if user_profile else "",
                        "sponsor_member_id": sponsor_member_id,
                        "level": user_level,  # ✅ NUEVO: Nivel del usuario
                        # Agregar campos directos para patrocinador
                        "sponsor_full_name": sponsor_data.get("full_name", "N/A") if sponsor_data else "N/A",
                        "sponsor_phone": sponsor_data.get("phone", "N/A") if sponsor_data else "N/A"
                    }
                    descendants.append(user_data)
                    
                    # Buscar recursivamente los descendientes de este usuario
                    sub_descendants = MLMUserManager.get_network_descendants(user.member_id, actual_root_id)
                    descendants.extend(sub_descendants)
                
                return descendants
                
        except Exception as e:
            print(f"❌ Error obteniendo red descendente: {e}")
            return []
    
    @staticmethod
    def _filter_registrations_by_date_range(sponsor_member_id: int, start_date, end_date) -> list:
        """
        Método privado que filtra registraciones por rango de fechas.
        Aplica POO para reutilizar lógica común.
        
        Args:
            sponsor_member_id: member_id del sponsor principal
            start_date: fecha de inicio (inclusive)
            end_date: fecha de fin (inclusive)
            
        Returns:
            Lista de usuarios registrados en el rango de fechas
        """
        try:
            # Obtener toda la red descendente pasando el sponsor como root para niveles
            all_descendants = MLMUserManager.get_network_descendants(sponsor_member_id, sponsor_member_id)
            
            # Filtrar por rango de fechas
            filtered_registrations = []
            from datetime import datetime
            
            for user in all_descendants:
                if user.get("created_at") and user["created_at"] != "N/A":
                    try:
                        # Parsear string formato DD/MM/YYYY a date object
                        created_at_str = user["created_at"]  # "26/09/2025"
                        created_at_date = datetime.strptime(created_at_str, "%d/%m/%Y").date()
                        
                        # Comparar fechas
                        if start_date <= created_at_date <= end_date:
                            filtered_registrations.append(user)
                            
                    except ValueError as ve:
                        print(f"⚠️ Error parseando fecha '{user['created_at']}': {ve}")
                        continue
            
            print(f"✅ Filtradas {len(filtered_registrations)} registraciones entre {start_date} y {end_date}")
            return filtered_registrations
            
        except Exception as e:
            print(f"❌ Error filtrando registraciones por fecha: {e}")
            return []

    @staticmethod
    def get_todays_registrations(sponsor_member_id: int) -> list:
        """
        Obtiene las inscripciones del día de la red de un sponsor.
        
        Args:
            sponsor_member_id: member_id del sponsor principal
            
        Returns:
            Lista de usuarios registrados hoy en la red
        """
        try:
            # ✅ USAR FECHA DE MÉXICO
            today = get_mexico_date()
            
            # Reutilizar lógica común usando POO
            return MLMUserManager._filter_registrations_by_date_range(sponsor_member_id, today, today)
            
        except Exception as e:
            print(f"❌ Error obteniendo inscripciones del día: {e}")
            return []

    @staticmethod
    def get_monthly_registrations(sponsor_member_id: int) -> list:
        """
        Obtiene las inscripciones del mes actual de la red de un sponsor.
        
        Args:
            sponsor_member_id: member_id del sponsor principal
            
        Returns:
            Lista de usuarios registrados en el mes actual
        """
        try:
            # ✅ USAR FECHA DE MÉXICO
            today = get_mexico_date()
            
            # Calcular primer y último día del mes actual
            first_day_of_month = today.replace(day=1)  # Primer día del mes
            
            # Último día del mes (usar el día antes del primer día del siguiente mes)
            if today.month == 12:
                last_day_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                last_day_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            
            # Reutilizar lógica común usando POO
            return MLMUserManager._filter_registrations_by_date_range(sponsor_member_id, first_day_of_month, last_day_of_month)
            
        except Exception as e:
            print(f"❌ Error obteniendo inscripciones del mes: {e}")
            return []