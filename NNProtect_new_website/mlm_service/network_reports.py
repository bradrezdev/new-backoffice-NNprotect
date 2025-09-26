"""Nueva Backoffice NN Protect | Reportes de Red"""

import reflex as rx
from ..shared_ui.theme import Custom_theme
from rxconfig import config
from ..shared_ui.layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, logged_in_user
from ..auth_service.auth_state import AuthState
from .mlm_user_manager import MLMUserManager
from typing import List, Dict, Any

def format_date(date_obj) -> str:
    """Convierte objeto datetime a formato YYYY/MM/DD"""
    try:
        # Debug: ver qué tipo de objeto llega
        print(f"🔍 DEBUG fecha recibida: '{date_obj}' (tipo: {type(date_obj)})")
        
        if not date_obj:
            return "N/A"
        
        # Manejar diferentes tipos de entrada
        from datetime import datetime
        
        # Caso 1: Ya es un objeto datetime
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%Y/%m/%d")
        
        # Caso 2: Es un string (fallback para otros casos)
        if isinstance(date_obj, str):
            if "T" in date_obj or "-" in date_obj:
                try:
                    parsed_date = datetime.fromisoformat(str(date_obj).replace("Z", ""))
                    return parsed_date.strftime("%Y/%m/%d")
                except:
                    pass
            
            if "/" in date_obj:
                parts = date_obj.split("/")
                if len(parts) == 3:
                    day, month, year = parts
                    return f"{year}/{month.zfill(2)}/{day.zfill(2)}"
        
        # Fallback: convertir a string y devolver
        return str(date_obj)
        
    except Exception as e:
        print(f"❌ Error parseando fecha '{date_obj}': {e}")
        return "N/A"

class NetworkReportsState(rx.State):
	"""State para manejar datos de reportes de red."""
	todays_registrations: List[Dict[str, Any]] = []
	monthly_registrations: List[Dict[str, Any]] = []
	is_loading: bool = False

	@rx.var
	def today_registrations_count(self) -> str:
		"""Cuenta de inscripciones del día."""
		return str(len(self.todays_registrations))

	@rx.var
	def monthly_registrations_count(self) -> str:
		"""Cuenta de inscripciones del mes."""
		return str(len(self.monthly_registrations))
	
	@rx.event
	async def load_todays_registrations(self):
		"""Carga las inscripciones del día de la red del usuario autenticado."""
		self.is_loading = True
		yield
		
		try:
			# Obtener el member_id del usuario autenticado
			auth_state = await self.get_state(AuthState)
			
			# ✅ VALIDACIÓN SIMPLIFICADA - Solo lo necesario
			member_id = auth_state.profile_data.get("member_id") if auth_state.profile_data else None
			if not member_id:
				print("❌ Usuario no autenticado o member_id no encontrado")
				self.todays_registrations = []
				return
				
			print(f"🔄 Cargando inscripciones del día para member_id: {member_id}")
			
			# Obtener inscripciones del día de la red
			registrations = MLMUserManager.get_todays_registrations(member_id)
			self.todays_registrations = registrations
			
			print(f"✅ Cargadas {len(registrations)} inscripciones del día")
			
		except Exception as e:
			print(f"❌ Error cargando inscripciones: {e}")
			self.todays_registrations = []
		finally:
			self.is_loading = False

	@rx.event
	async def load_monthly_registrations(self):
		"""Carga las inscripciones del mes de la red del usuario autenticado."""
		self.is_loading = True
		yield
		
		try:
			# Obtener el member_id del usuario autenticado
			auth_state = await self.get_state(AuthState)
			
			# ✅ VALIDACIÓN SIMPLIFICADA - Solo lo necesario
			member_id = auth_state.profile_data.get("member_id") if auth_state.profile_data else None
			if not member_id:
				print("❌ Usuario no autenticado o member_id no encontrado")
				self.monthly_registrations = []
				return
				
			print(f"🔄 Cargando inscripciones del mes para member_id: {member_id}")
			
			# Obtener inscripciones del mes de la red
			registrations = MLMUserManager.get_monthly_registrations(member_id)
			self.monthly_registrations = registrations
			
			print(f"✅ Cargadas {len(registrations)} inscripciones del mes")
			
		except Exception as e:
			print(f"❌ Error cargando inscripciones del mes: {e}")
			self.monthly_registrations = []
		finally:
			self.is_loading = False

	@rx.event
	async def load_all_registrations(self):
		"""Carga tanto las inscripciones del día como del mes."""
		self.is_loading = True
		yield
		
		try:
			# Obtener el member_id del usuario autenticado
			auth_state = await self.get_state(AuthState)
			
			# ✅ VALIDACIÓN SIMPLIFICADA - Solo lo necesario
			member_id = auth_state.profile_data.get("member_id") if auth_state.profile_data else None
			if not member_id:
				print("❌ Usuario no autenticado o member_id no encontrado")
				self.todays_registrations = []
				self.monthly_registrations = []
				return
				
			print(f"🔄 Cargando inscripciones para member_id: {member_id}")
			
			# Cargar ambos tipos de inscripciones
			daily_registrations = MLMUserManager.get_todays_registrations(member_id)
			monthly_registrations = MLMUserManager.get_monthly_registrations(member_id)
			
			self.todays_registrations = daily_registrations
			self.monthly_registrations = monthly_registrations
			
			print(f"✅ Cargadas {len(daily_registrations)} inscripciones del día")
			print(f"✅ Cargadas {len(monthly_registrations)} inscripciones del mes")
			
		except Exception as e:
			print(f"❌ Error cargando inscripciones: {e}")
			self.todays_registrations = []
			self.monthly_registrations = []
		finally:
			self.is_loading = False


def network_reports() -> rx.Component:
	"""Página de reportes de red"""
	return rx.center(
		# Contenedor principal centrado
		rx.desktop_only(
			# Solo se muestra en escritorio
			rx.vstack(
				logged_in_user(), # Muestra el usuario logueado en la esquina superior derecha
				# Contenedor vertical principal
				rx.hstack(
					# Contenedor horizontal para sidebar y contenido principal
					desktop_sidebar(),
					# Sidebar (menú lateral)
					main_container_derecha(
						# Contenedor principal de la derecha
						rx.vstack(
							# Contenedor vertical para el contenido de reportes
							# Encabezado de la página
							rx.text(
								"Reportes de Red",
								font_size="2rem",
								font_weight="bold",
								margin_bottom="0.1em"
							),
							
							# Secciones de detalles del usuario y patrocinador
							rx.hstack(
								# Sección de detalles del usuario
								rx.box(
									rx.vstack(
										rx.text(
											"Detalles personales",
											color="#FFFFFF",
											font_size="1.5rem",
											font_weight="bold",
											margin_bottom="1rem"
										),
										rx.hstack(
											# Primera columna - Etiquetas
											rx.vstack(
												rx.text("ID:", font_weight="bold", color="#FFFFFF"),
												rx.text("Nombre:", font_weight="bold", color="#FFFFFF"),
												rx.text("Rango actual:", font_weight="bold", color="#FFFFFF"),
												rx.text("Fecha de registro:", font_weight="bold", color="#FFFFFF"),
												align="start",
												spacing="3",
												width="50%"
											),
											# Segunda columna - Valores
											rx.vstack(
												rx.text(AuthState.profile_data.get("member_id"), color="#FFFFFF"),
												rx.text(AuthState.profile_data.get("full_name"), color="#FFFFFF"),
												rx.text(AuthState.profile_data.get("phone"), color="#FFFFFF"),
												rx.text(AuthState.profile_data.get("created_at"), color="#FFFFFF"),
												align="end",
												spacing="3",
												width="70%"
											),
											width="100%",
											align="stretch",
										),
										spacing="3",
										width="100%"
									),
									bg=rx.color_mode_cond(
										light=Custom_theme().light_colors()["secondary"],
										dark=Custom_theme().dark_colors()["secondary"]
									),
									border_radius="24px",
									padding="24px",
									width="45%",
									margin_right="1rem"
								),
								
								# Sección de detalles del patrocinador
								rx.box(
									rx.vstack(
										rx.text(
											"Detalles del Patrocinador",
											font_size="1.5rem",
											font_weight="bold",
											margin_bottom="1rem"
										),
										rx.hstack(
											# Primera columna - Etiquetas
											rx.vstack(
												rx.text("ID:", font_weight="bold"),
												rx.text("Patrocinador:", font_weight="bold"),
												rx.text("Rango:", font_weight="bold"),
												rx.text("Contacto:", font_weight="bold"),
												align="start",
												spacing="3",
												width="50%"
											),
											# Segunda columna - Valores
											rx.vstack(
												rx.text(AuthState.profile_data.get("sponsor_id", "N/A"), color=rx.color("gray", 11)),
												rx.text(AuthState.sponsor_data.get("full_name", "N/A"), color=rx.color("gray", 11)),
												rx.text("Por agregar", color=rx.color("blue", 11)),
												rx.text(AuthState.sponsor_data.get("phone", "N/A"), color=rx.color("gray", 11)),
												align="end",
												spacing="3",
												width="50%"
											),
											width="100%",
											align="stretch",
										),
										spacing="3",
										width="100%"
									),
									bg=rx.color_mode_cond(
										light=Custom_theme().light_colors()["tertiary"],
										dark=Custom_theme().dark_colors()["tertiary"]
									),
									border_radius="24px",
									padding="24px",
									width="55%"
								),
								width="100%",
								align="stretch",
								margin_bottom="1.5rem"
							),
							
							# Sección de reporte de volumen
							rx.box(
								rx.vstack(
									rx.text(
										"Reporte de Volumen",
										font_size="1.5rem",
										font_weight="bold",
										margin_bottom="1rem"
									),
									# Métricas principales
									rx.hstack(
										rx.vstack(
											rx.text("Volumen personal:", font_weight="bold"),
											rx.text("2,930", color="#32D74B", font_size="2rem"),
											align="center",
											spacing="1"
										),
										rx.vstack(
											rx.text("Volumen grupal:", font_weight="bold"),
											rx.text("754,654", color="#0039F2", font_size="2rem"),
											align="center",
											spacing="1"
										),
										rx.vstack(
											rx.text("Siguiente rango:", font_weight="bold"),
											rx.text("1,300,000", color="#5E79FF", font_size="2rem"),
											align="center",
											spacing="1"
										),
										justify="between",
										width="100%"
									),
									rx.divider(),
									# Tabla de volúmenes
									rx.text("Detalle por niveles:", font_weight="bold", margin_bottom="0.5rem"),
									rx.table.root(
										rx.table.header(
											rx.table.row(
												rx.table.column_header_cell("Nivel"),
												rx.table.column_header_cell("Mes actual"),
												rx.table.column_header_cell("Mes 1"),
												rx.table.column_header_cell("Mes 2"),
												rx.table.column_header_cell("Mes 3"),
												rx.table.column_header_cell("Mes 4"),
											),
											text_align="center"
										),
										rx.table.body(
											rx.table.row(
												rx.table.row_header_cell("PV", font_weight="bold"),
												rx.table.cell("$2,450", color=rx.color("green", 11)),
												rx.table.cell("$2,200", color=rx.color("gray", 11)),
												rx.table.cell("$1,950", color=rx.color("gray", 11)),
												rx.table.cell("$2,100", color=rx.color("gray", 11)),
												rx.table.cell("$2,300", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Primer nivel", font_weight="bold"),
												rx.table.cell("$3,200", color=rx.color("blue", 11)),
												rx.table.cell("$2,800", color=rx.color("gray", 11)),
												rx.table.cell("$2,500", color=rx.color("gray", 11)),
												rx.table.cell("$2,700", color=rx.color("gray", 11)),
												rx.table.cell("$3,000", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Segundo nivel", font_weight="bold"),
												rx.table.cell("$1,850", color=rx.color("orange", 11)),
												rx.table.cell("$1,600", color=rx.color("gray", 11)),
												rx.table.cell("$1,400", color=rx.color("gray", 11)),
													rx.table.cell("$1,500", color=rx.color("gray", 11)),
												rx.table.cell("$1,700", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Tercer nivel", font_weight="bold"),
												rx.table.cell("$980", color=rx.color("purple", 11)),
												rx.table.cell("$850", color=rx.color("gray", 11)),
												rx.table.cell("$750", color=rx.color("gray", 11)),
													rx.table.cell("$800", color=rx.color("gray", 11)),
												rx.table.cell("$900", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Cuarto nivel", font_weight="bold"),
												rx.table.cell("$720", color=rx.color("cyan", 11)),
												rx.table.cell("$650", color=rx.color("gray", 11)),
												rx.table.cell("$580", color=rx.color("gray", 11)),
												rx.table.cell("$600", color=rx.color("gray", 11)),
												rx.table.cell("$680", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Quinto nivel", font_weight="bold"),
												rx.table.cell("$520", color=rx.color("pink", 11)),
												rx.table.cell("$450", color=rx.color("gray", 11)),
												rx.table.cell("$400", color=rx.color("gray", 11)),
												rx.table.cell("$420", color=rx.color("gray", 11)),
												rx.table.cell("$480", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Sexto nivel", font_weight="bold"),
												rx.table.cell("$380", color=rx.color("indigo", 11)),
												rx.table.cell("$320", color=rx.color("gray", 11)),
												rx.table.cell("$280", color=rx.color("gray", 11)),
												rx.table.cell("$300", color=rx.color("gray", 11)),
												rx.table.cell("$340", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Séptimo nivel", font_weight="bold"),
												rx.table.cell("$240", color=rx.color("teal", 11)),
												rx.table.cell("$200", color=rx.color("gray", 11)),
												rx.table.cell("$180", color=rx.color("gray", 11)),
												rx.table.cell("$190", color=rx.color("gray", 11)),
												rx.table.cell("$210", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Octavo nivel", font_weight="bold"),
												rx.table.cell("$150", color=rx.color("amber", 11)),
												rx.table.cell("$120", color=rx.color("gray", 11)),
												rx.table.cell("$100", color=rx.color("gray", 11)),
												rx.table.cell("$110", color=rx.color("gray", 11)),
												rx.table.cell("$130", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Noveno nivel", font_weight="bold"),
												rx.table.cell("$95", color=rx.color("red", 11)),
												rx.table.cell("$85", color=rx.color("gray", 11)),
												rx.table.cell("$75", color=rx.color("gray", 11)),
												rx.table.cell("$80", color=rx.color("gray", 11)),
												rx.table.cell("$80", color=rx.color("gray", 11))
											),
											rx.table.row(
												rx.table.row_header_cell("Décimo nivel", font_weight="bold"),
												rx.table.cell("$70", color=rx.color("lime", 11)),
												rx.table.cell("$65", color=rx.color("gray", 11)),
												rx.table.cell("$60", color=rx.color("gray", 11)),
												rx.table.cell("$55", color=rx.color("gray", 11)),
												rx.table.cell("$50", color=rx.color("gray", 11))
											)
										),
										width="100%",
										#variant="surface"
									),
									align="start",
									spacing="3",
									width="100%"
								),
								bg=rx.color_mode_cond(
									light=Custom_theme().light_colors()["tertiary"],
									dark=Custom_theme().dark_colors()["tertiary"]
								),
								border_radius="24px",
								padding="24px",
								width="100%",
								margin_top="1.5rem"
							),
							
							# Sección de inscripciones del equipo
							rx.box(
								rx.vstack(
									rx.text(
										"Equipo de negocio",
										font_size="1.5rem",
										font_weight="bold",
										margin_bottom="1rem"
									),
									rx.hstack(
										rx.vstack(
											rx.text("Total de miembros:", font_weight="bold"),
											rx.text("47", color=rx.color("blue", 11), font_size="2rem"),
											align="center",
											spacing="1"
										),
										rx.vstack(
											rx.text("Nuevos este mes:", font_weight="bold"),
											rx.text(NetworkReportsState.monthly_registrations_count, color=rx.color("green", 11), font_size="2rem"),
											align="center",
											spacing="1"
										),
										rx.vstack(
											rx.text("Activos:", font_weight="bold"),
											rx.text("42", color=rx.color("orange", 11), font_size="2rem"),
											align="center",
											spacing="1"
										),
										justify="between",
										width="100%"
									),
									rx.divider(),
									# Tabla de inscripciones del mes
									rx.text("Inscripciones del mes:", font_weight="bold", margin_bottom="0.5rem"),
									rx.cond(
										NetworkReportsState.is_loading,
										rx.spinner(loading=True, size="2"),
										rx.cond(
											NetworkReportsState.monthly_registrations,
											rx.table.root(
												rx.table.header(
													rx.table.row(
														rx.table.column_header_cell("Nombre", align="left"),
														rx.table.column_header_cell("ID socio"),
														rx.table.column_header_cell("Contacto"),
														rx.table.column_header_cell("Volumen personal"),
														rx.table.column_header_cell("Nivel"),
														rx.table.column_header_cell("Fecha de inscripción"),
														rx.table.column_header_cell("Patrocinador"),
														rx.table.column_header_cell("ID patrocinador"),
														rx.table.column_header_cell("Estado"),
														align="center",
													),
													text_align="center"
												),
												rx.table.body(
													rx.foreach(
														NetworkReportsState.monthly_registrations,
														lambda user: rx.table.row(
															rx.table.row_header_cell(user["full_name"], align="left"),
															rx.table.cell(user["member_id"]),
															rx.table.cell(user["phone"]),
															rx.table.cell("2000"),  # Volumen personal (placeholder)
															rx.table.cell(user["level"]),  # ✅ Nivel real del usuario
															rx.table.cell(user["created_at"]),
															rx.table.cell(user["sponsor_full_name"]),
															rx.table.cell(user["sponsor_member_id"]),
															rx.table.cell(rx.cond(user["status"] == "active", rx.badge("Activo", color_scheme="green"), rx.badge("Inactivo", color_scheme="red"))),
															align="center"
														),
													),
													text_align="center",
												),
												width="100%"
											),
											rx.text(
												"No hay inscripciones del día en tu red",
												font_style="italic",
												color="gray",
												text_align="center",
												padding="2rem"
											)
										)
									),
									align="start",
									spacing="3",
									width="100%"
								),
								bg=rx.color_mode_cond(
									light=Custom_theme().light_colors()["tertiary"],
									dark=Custom_theme().dark_colors()["tertiary"]
								),
								border_radius="24px",
								padding="24px",
								width="100%",
								margin_top="1.5rem"
							),
							
							# Propiedades del vstack principal
							width="100%",
						),
					),
					width="100%",
				),
				# Propiedades vstack que contiene el contenido de la página
				align="end",
				margin_top="8em",
				margin_bottom="2em",
				max_width="1920px",
				width="100%",
				on_mount=NetworkReportsState.load_all_registrations,
			),
			#width="100%",
		),
		
		# Versión móvil
		rx.mobile_only(
			# Encabezado de la página móvil
			mobile_header(),
			rx.vstack(				
				# Sección de detalles del usuario (móvil)
				rx.box(
					rx.vstack(
						rx.text(
							"Detalles personales",
							color="#FFFFFF",
							font_size="1.2rem",
							font_weight="bold",
							margin_bottom="0.8rem",
							text_align="center"
						),
						rx.vstack(
							rx.hstack(
								rx.text("ID de Usuario:", font_weight="bold", color="#FFFFFF", font_size="0.9rem"),
								rx.text(AuthState.profile_data.get("member_id"), color="#FFFFFF", font_size="0.9rem"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Nombre:", font_weight="bold", color="#FFFFFF", font_size="0.9rem"),
								rx.text(AuthState.profile_data.get("full_name"), color="#FFFFFF", font_size="0.9rem"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Rango actual:", font_weight="bold", color="#FFFFFF", font_size="0.9rem"),
								rx.text("Distribuidor", color="#FFFFFF", font_size="0.9rem"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Fecha de registro:", font_weight="bold", color="#FFFFFF", font_size="0.9rem"),
								rx.text(AuthState.profile_data.get("created_at"), color="#FFFFFF", font_size="0.9rem"),
								justify="between",
								width="100%"
							),
							spacing="2",
							width="100%"
						),
						spacing="2",
						width="100%"
					),
					bg=rx.color_mode_cond(
						light=Custom_theme().light_colors()["secondary"],
						dark=Custom_theme().dark_colors()["secondary"]
					),
					border_radius="16px",
					padding="16px",
					width="100%",
					margin_bottom="1rem"
				),
				
				# Sección de detalles del patrocinador (móvil)
				rx.box(
					rx.vstack(
						rx.text(
							"Detalles del Patrocinador",
							font_size="1.2rem",
							font_weight="bold",
							margin_bottom="0.8rem",
							text_align="center"
						),
						rx.vstack(
							rx.hstack(
								rx.text("ID:", font_weight="bold", font_size="0.9rem"),
								rx.text(AuthState.profile_data.get("sponsor_id", "N/A"), color=rx.color("gray", 11), font_size="0.9rem"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Nombre:", font_weight="bold", font_size="0.9rem"),
								rx.text(AuthState.sponsor_data.get("full_name", "N/A"), color=rx.color("gray", 11), font_size="0.9rem"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Rango:", font_weight="bold", font_size="0.9rem"),
								rx.text("Por agregar", color=rx.color("blue", 11), font_size="0.9rem"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Contacto:", font_weight="bold", font_size="0.9rem"),
								rx.text(AuthState.sponsor_data.get("phone", "N/A"), color=rx.color("gray", 11), font_size="0.9rem"),
								justify="between",
								width="100%"
							),
							spacing="2",
							width="100%"
						),
						spacing="2",
						width="100%"
					),
					bg=rx.color_mode_cond(
						light=Custom_theme().light_colors()["tertiary"],
						dark=Custom_theme().dark_colors()["tertiary"]
					),
					border_radius="16px",
					padding="16px",
					width="100%",
					margin_bottom="1rem"
				),
				
				# Sección de equipo de negocio (móvil) - ACTUALIZADA
				rx.box(
					rx.vstack(
						rx.text(
							"Equipo de negocio",
							font_size="1.2rem",
							font_weight="bold",
							margin_bottom="0.8rem",
							text_align="center"
						),
						# Métricas del equipo en móvil
						rx.vstack(
							rx.hstack(
								rx.text("Total de miembros:", font_weight="bold", font_size="0.9rem"),
								rx.text("47", color=rx.color("blue", 11), font_size="1.5rem", font_weight="bold"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Nuevos este mes:", font_weight="bold", font_size="0.9rem"),
								rx.text(NetworkReportsState.monthly_registrations_count, color=rx.color("green", 11), font_size="1.5rem", font_weight="bold"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Activos:", font_weight="bold", font_size="0.9rem"),
								rx.text("42", color=rx.color("orange", 11), font_size="1.5rem", font_weight="bold"),
								justify="between",
								width="100%"
							),
							spacing="2",
							width="100%"
						),
						rx.divider(),
						# Inscripciones recientes con información completa para móvil
						rx.text("Inscripciones del mes:", font_weight="bold", font_size="0.9rem", margin_bottom="0.5rem"),
						rx.vstack(
							# Primera inscripción - Juan Pérez
							rx.box(
								rx.vstack(
									# Encabezado con nombre y estado
									rx.hstack(
										rx.text("Juan Pérez", font_weight="bold", font_size="1rem"),
										rx.badge("Activo", color_scheme="green", size="1"),
										justify="between",
										width="100%"
									),
									# Información principal
									rx.vstack(
										rx.hstack(
											rx.text("ID Socio:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("12345", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Contacto:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("+521234567890", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Volumen Personal:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("1465", font_size="0.8rem", font_weight="600", color=rx.color("green", 11)),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Nivel:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("2", font_size="0.8rem", font_weight="600", color=rx.color("blue", 11)),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Fecha Inscripción:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("18/07/2025", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.divider(size="1", margin_y="0.3rem"),
										rx.hstack(
											rx.text("Patrocinador:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("Bryan Núñez", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("ID Patrocinador:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("224", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										spacing="1",
										width="100%"
									),
									spacing="2",
									width="100%"
								),
								bg=rx.color_mode_cond(
									light=rx.color("gray", 2),
									dark=rx.color("gray", 12)
								),
								padding="12px",
								border_radius="8px",
								width="100%"
							),
							# Segunda inscripción - Ana Martínez
							rx.box(
								rx.vstack(
									# Encabezado con nombre y estado
									rx.hstack(
										rx.text("Ana Martínez", font_weight="bold", font_size="1rem"),
										rx.badge("Activo", color_scheme="green", size="1"),
										justify="between",
										width="100%"
									),
									# Información principal
									rx.vstack(
										rx.hstack(
											rx.text("ID Socio:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("54321", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Contacto:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("+521098765432", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Volumen Personal:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("2930", font_size="0.8rem", font_weight="600", color=rx.color("green", 11)),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Nivel:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("11", font_size="0.8rem", font_weight="600", color=rx.color("blue", 11)),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Fecha Inscripción:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("15/07/2025", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.divider(size="1", margin_y="0.3rem"),
										rx.hstack(
											rx.text("Patrocinador:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("Juan Pérez", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("ID Patrocinador:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("12345", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										spacing="1",
										width="100%"
									),
									spacing="2",
									width="100%"
								),
								bg=rx.color_mode_cond(
									light=rx.color("gray", 2),
									dark=rx.color("gray", 12)
								),
								padding="12px",
								border_radius="8px",
								width="100%"
							),
							# Tercera inscripción - Carlos López
							rx.box(
								rx.vstack(
									# Encabezado con nombre y estado
									rx.hstack(
										rx.text("Carlos López", font_weight="bold", font_size="1rem"),
										rx.badge("Inactivo", color_scheme="tomato", size="1"),
										justify="between",
										width="100%"
									),
									# Información principal
									rx.vstack(
										rx.hstack(
											rx.text("ID Socio:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("67890", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Contacto:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("+521987654321", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Volumen Personal:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("0", font_size="0.8rem", font_weight="600", color=rx.color("red", 11)),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Nivel:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("5", font_size="0.8rem", font_weight="600", color=rx.color("blue", 11)),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("Fecha Inscripción:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("12/07/2025", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.divider(size="1", margin_y="0.3rem"),
										rx.hstack(
											rx.text("Patrocinador:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("Enrique Torres", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										rx.hstack(
											rx.text("ID Patrocinador:", font_size="0.75rem", color=rx.color("gray", 9)),
											rx.text("42356", font_size="0.8rem", font_weight="600"),
											justify="between",
											width="100%"
										),
										spacing="1",
										width="100%"
									),
									spacing="2",
									width="100%"
								),
								bg=rx.color_mode_cond(
									light=rx.color("gray", 2),
									dark=rx.color("gray", 12)
								),
								padding="12px",
								border_radius="8px",
								width="100%"
							),
							spacing="2",
							width="100%"
						),
						spacing="3",
						width="100%"
					),
					bg=rx.color_mode_cond(
						light=Custom_theme().light_colors()["tertiary"],
						dark=Custom_theme().dark_colors()["tertiary"]
					),
					border_radius="16px",
					padding="16px",
					width="100%",
					margin_bottom="1rem"
				),
				
				# Sección de reporte de volumen (móvil)
				rx.box(
					rx.vstack(
						rx.text(
							"Reporte de Volumen",
							font_size="1.2rem",
							font_weight="bold",
							margin_bottom="0.8rem",
							text_align="center"
						),
						# Métricas principales en móvil
						rx.vstack(
							rx.hstack(
								rx.text("Volumen personal:", font_weight="bold", font_size="0.9rem"),
								rx.text("2,930", color="#32D74B", font_size="1.2rem", font_weight="bold"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Volumen grupal:", font_weight="bold", font_size="0.9rem"),
								rx.text("754,654", color="#0039F2", font_size="1.2rem", font_weight="bold"),
								justify="between",
								width="100%"
							),
							rx.hstack(
								rx.text("Siguiente rango:", font_weight="bold", font_size="0.9rem"),
								rx.text("1,300,000", color="#5E79FF", font_size="1.2rem", font_weight="bold"),
								justify="between",
								width="100%"
							),
							spacing="2",
							width="100%"
						),
						rx.divider(),
						# Tabla simplificada para móvil (solo mes actual)
						rx.text("Detalle por niveles (Mes actual):", font_weight="bold", font_size="0.9rem", margin_bottom="0.5rem"),
						rx.vstack(
							rx.hstack(rx.text("PV:", font_weight="bold", font_size="0.8rem"), rx.text("$2,450", color=rx.color("green", 11), font_size="0.8rem"), justify="between", width="100%"),
							rx.hstack(rx.text("Primer nivel:", font_weight="bold", font_size="0.8rem"), rx.text("$3,200", color=rx.color("blue", 11), font_size="0.8rem"), justify="between", width="100%"),
							rx.hstack(rx.text("Segundo nivel:", font_weight="bold", font_size="0.8rem"), rx.text("$1,850", color=rx.color("orange", 11), font_size="0.8rem"), justify="between", width="100%"),
							rx.hstack(rx.text("Tercer nivel:", font_weight="bold", font_size="0.8rem"), rx.text("$980", color=rx.color("purple", 11), font_size="0.8rem"), justify="between", width="100%"),
							rx.hstack(rx.text("Cuarto nivel:", font_weight="bold", font_size="0.8rem"), rx.text("$720", color=rx.color("cyan", 11), font_size="0.8rem"), justify="between", width="100%"),
							spacing="1",
							width="100%"
						),
						spacing="2",
						width="100%"
					),
					bg=rx.color_mode_cond(
						light=Custom_theme().light_colors()["tertiary"],
						dark=Custom_theme().dark_colors()["tertiary"]
					),
					border_radius="16px",
					padding="16px",
					width="100%",
					margin_bottom="0.4em",
				),
				# Propiedades del vstack móvil
				margin_top="80px",
				padding="1em",
			),
			width="100%",
		),
		
		bg=rx.color_mode_cond(
			light=Custom_theme().light_colors()["background"],
			dark=Custom_theme().dark_colors()["background"]
		),
		position="absolute",
		width="100%",
	)