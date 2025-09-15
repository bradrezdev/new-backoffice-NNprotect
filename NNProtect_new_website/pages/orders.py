"""Nueva Backoffice NN Protect | Órdenes"""

import reflex as rx
from ..theme import Custom_theme
from rxconfig import config
from ..layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar, header

def orders() -> rx.Component:
	"""Página que muestra todas las órdenes del usuario"""
	return rx.center(
		# Versión de escritorio
		rx.desktop_only(
			rx.vstack(
				header(),  # Muestra el usuario logueado en la esquina superior derecha
				rx.hstack(
					desktop_sidebar(),
					main_container_derecha(
						rx.vstack(
							# Encabezado de la página
							rx.text(
								"Órdenes",
								font_size="2em",
								font_weight="bold",
								margin_bottom="0.5em"
							),
							
							# Barra de búsqueda y filtros
							rx.hstack(
								# Campo de búsqueda
								rx.box(
									rx.hstack(
										rx.icon("search", size=20, color=rx.color("gray", 11)),
										rx.input(
											placeholder="Buscar por número de orden...",
											border="none",
											bg="transparent",
											width="100%",
											_focus={"outline": "none"}
										),
										width="100%",
										align="center",
										spacing="2"
									),
									bg=rx.color_mode_cond(
										light=Custom_theme().light_colors()["tertiary"],
										dark=Custom_theme().dark_colors()["tertiary"]
									),
									border_radius="32px",
									padding="12px 24px",
									width="40%",
									border=f"1px solid {rx.color('gray', 6)}"
								),
								
								# Filtros adicionales
								rx.select(
									["Todas", "Pendiente", "En proceso", "Enviado", "Entregado", "Cancelado"],
									placeholder="Estado",
									default_value="Todas",
									radius="large",
									width="200px"
								),
								
								rx.select(
									["Más reciente", "Más antiguo", "Mayor monto", "Menor monto"],
									placeholder="Ordenar por",
									default_value="Más reciente",
									radius="large",
									width="200px"
								),
								
								width="100%",
								justify="between",
								margin_bottom="2em"
							),
							
							# Tabla de órdenes
							rx.box(
								rx.table.root(
									rx.table.header(
										rx.table.row(
											rx.table.column_header_cell("# Orden"),
											rx.table.column_header_cell("Dirección de envío"),
											rx.table.column_header_cell("Fecha de compra"),
											rx.table.column_header_cell("Método de pago"),
											rx.table.column_header_cell("Total pagado"),
											rx.table.column_header_cell("Estado"),
											rx.table.column_header_cell("Acciones", text_align="center"),
										)
									),
									rx.table.body(
										# Orden 1
										rx.table.row(
											rx.table.row_header_cell("#12345", font_weight="bold"),
											rx.table.cell("Av. Siempre Viva 742, Col. Centro, Colima"),
											rx.table.cell("10/09/2025"),
											rx.table.cell(
												rx.hstack(
													rx.icon("credit-card", size=16),
													rx.text("Tarjeta crédito"),
													spacing="1"
												)
											),
											rx.table.cell("$1,746.50", font_weight="bold", color=rx.color_mode_cond(
												light=Custom_theme().light_colors()["primary"],
												dark=Custom_theme().dark_colors()["primary"]
											)),
											rx.table.cell(
												rx.badge("Pendiente", color_scheme="orange")
											),
											rx.table.cell(
												rx.hstack(
													rx.button(
														rx.icon("eye", size=16),
														"Ver detalles",
														size="2",
														variant="soft",
														color_scheme="blue",
														on_click=lambda: rx.redirect("/order_details")
													),
													rx.button(
														rx.icon("download", size=16),
														"PDF",
														size="2",
														variant="outline",
														color_scheme="gray"
													),
													spacing="2",
													justify="center"
												)
											),
										),
										
										# Orden 2
										rx.table.row(
											rx.table.row_header_cell("#67890", font_weight="bold"),
											rx.table.cell("Calle Principal 123, Santo Domingo, RD"),
											rx.table.cell("01/08/2025"),
											rx.table.cell(
												rx.hstack(
													rx.icon("wallet", size=16),
													rx.text("Billetera digital"),
													spacing="1"
												)
											),
											rx.table.cell("$1,926.50", font_weight="bold", color=rx.color_mode_cond(
												light=Custom_theme().light_colors()["primary"],
												dark=Custom_theme().dark_colors()["primary"]
											)),
											rx.table.cell(
												rx.badge("Entregado", color_scheme="green")
											),
											rx.table.cell(
												rx.hstack(
													rx.button(
														rx.icon("eye", size=16),
														"Ver detalles",
														size="2",
														variant="soft",
														color_scheme="blue",
														on_click=lambda: rx.redirect("/order_details")
													),
													rx.button(
														rx.icon("download", size=16),
														"PDF",
														size="2",
														variant="outline",
														color_scheme="gray"
													),
													spacing="2",
													justify="center"
												)
											),
										),
										
										# Orden 3
										rx.table.row(
											rx.table.row_header_cell("#11121", font_weight="bold"),
											rx.table.cell("Blvd. Camino Real 456, Guadalajara, JAL"),
											rx.table.cell("07/06/2025"),
											rx.table.cell(
												rx.hstack(
													rx.icon("credit-card", size=16),
													rx.text("Tarjeta débito"),
													spacing="1"
												)
											),
											rx.table.cell("$349.30", font_weight="bold", color=rx.color_mode_cond(
												light=Custom_theme().light_colors()["primary"],
												dark=Custom_theme().dark_colors()["primary"]
											)),
											rx.table.cell(
												rx.badge("Cancelado", color_scheme="red")
											),
											rx.table.cell(
												rx.hstack(
													rx.button(
														rx.icon("eye", size=16),
														"Ver detalles",
														size="2",
														variant="soft",
														color_scheme="blue",
														on_click=lambda: rx.redirect("/order_details")
													),
													rx.button(
														rx.icon("download", size=16),
														"PDF",
														size="2",
														variant="outline",
														color_scheme="gray"
													),
													spacing="2",
													justify="center"
												)
											),
										),
										
										# Orden 4
										rx.table.row(
											rx.table.row_header_cell("#22334", font_weight="bold"),
											rx.table.cell("Av. Revolución 789, CDMX"),
											rx.table.cell("15/05/2025"),
											rx.table.cell(
												rx.hstack(
													rx.icon("banknote", size=16),
													rx.text("Transferencia"),
													spacing="1"
												)
											),
											rx.table.cell("$2,580.00", font_weight="bold", color=rx.color_mode_cond(
												light=Custom_theme().light_colors()["primary"],
												dark=Custom_theme().dark_colors()["primary"]
											)),
											rx.table.cell(
												rx.badge("En proceso", color_scheme="blue")
											),
											rx.table.cell(
												rx.hstack(
													rx.button(
														rx.icon("eye", size=16),
														"Ver detalles",
														size="2",
														variant="soft",
														color_scheme="blue",
														on_click=lambda: rx.redirect("/order_details")
													),
													rx.button(
														rx.icon("download", size=16),
														"PDF",
														size="2",
														variant="outline",
														color_scheme="gray"
													),
													spacing="2",
													justify="center"
												)
											),
										),
										
										# Orden 5
										rx.table.row(
											rx.table.row_header_cell("#33445", font_weight="bold"),
											rx.table.cell("Calle Morelos 321, Monterrey, NL"),
											rx.table.cell("28/04/2025"),
											rx.table.cell(
												rx.hstack(
													rx.icon("credit-card", size=16),
													rx.text("Tarjeta crédito"),
													spacing="1"
												)
											),
											rx.table.cell("$4,125.80", font_weight="bold", color=rx.color_mode_cond(
												light=Custom_theme().light_colors()["primary"],
												dark=Custom_theme().dark_colors()["primary"]
											)),
											rx.table.cell(
												rx.badge("Enviado", color_scheme="cyan")
											),
											rx.table.cell(
												rx.hstack(
													rx.button(
														rx.icon("eye", size=16),
														"Ver detalles",
														size="2",
														variant="soft",
														color_scheme="blue",
														on_click=lambda: rx.redirect("/order_details")
													),
													rx.button(
														rx.icon("download", size=16),
														"PDF",
														size="2",
														variant="outline",
														color_scheme="gray"
													),
													spacing="2",
													justify="center"
												)
											),
										),
										
										# Orden 6
										rx.table.row(
											rx.table.row_header_cell("#44556", font_weight="bold"),
											rx.table.cell("Av. Universidad 852, Querétaro, QRO"),
											rx.table.cell("10/04/2025"),
											rx.table.cell(
												rx.hstack(
													rx.icon("wallet", size=16),
													rx.text("PayPal"),
													spacing="1"
												)
											),
											rx.table.cell("$892.40", font_weight="bold", color=rx.color_mode_cond(
												light=Custom_theme().light_colors()["primary"],
												dark=Custom_theme().dark_colors()["primary"]
											)),
											rx.table.cell(
												rx.badge("Entregado", color_scheme="green")
											),
											rx.table.cell(
												rx.hstack(
													rx.button(
														rx.icon("eye", size=16),
														"Ver detalles",
														size="2",
														variant="soft",
														color_scheme="blue",
														on_click=lambda: rx.redirect("/order_details")
													),
													rx.button(
														rx.icon("download", size=16),
														"PDF",
														size="2",
														variant="outline",
														color_scheme="gray"
													),
													spacing="2",
													justify="center"
												)
											),
										),
									),
									width="100%",
									variant="surface"
								),
								bg=rx.color_mode_cond(
									light=Custom_theme().light_colors()["tertiary"],
									dark=Custom_theme().dark_colors()["tertiary"]
								),
								border_radius="24px",
								padding="24px",
								width="100%"
							),
							
							# Paginación
							rx.hstack(
								rx.text("Mostrando 6 de 24 órdenes", color=rx.color("gray", 11)),
								rx.spacer(),
								rx.hstack(
									rx.button(
										rx.icon("chevron-left", size=16),
										"Anterior",
										variant="soft",
										disabled=True
									),
									rx.button("1", variant="solid", color_scheme="blue"),
									rx.button("2", variant="soft"),
									rx.button("3", variant="soft"),
									rx.button("4", variant="soft"),
									rx.button(
										"Siguiente",
										rx.icon("chevron-right", size=16),
										variant="soft"
									),
									spacing="2"
								),
								width="100%",
								margin_top="2em"
							),
							
							spacing="4",
							width="100%"
						)
					),
					width="100%"
				),
				align="end",
				margin_top="8em",
				margin_bottom="2em",
				max_width="1920px",
				width="100%"
			)
		),
		
		# Versión móvil
		rx.mobile_only(
			rx.vstack(
				# Header móvil
				mobile_header(),
				
				# Contenido principal móvil
				rx.vstack(
					# Barra de búsqueda móvil
					rx.box(
						rx.hstack(
							rx.icon("search", size=18, color=rx.color("gray", 11)),
							rx.input(
								placeholder="Buscar orden...",
								border="none",
								bg="transparent",
								width="100%",
								_focus={"outline": "none"},
								font_size="0.9em"
							),
							width="100%",
							align="center",
							spacing="2"
						),
						bg=rx.color_mode_cond(
							light=Custom_theme().light_colors()["tertiary"],
							dark=Custom_theme().dark_colors()["tertiary"]
						),
						border_radius="12px",
						padding="10px 16px",
						width="100%",
						border=f"1px solid {rx.color('gray', 6)}",
						margin_bottom="1em"
					),
					
					# Filtros móvil
					rx.hstack(
						rx.select(
							["Todas", "Pendiente", "En proceso", "Enviado", "Entregado", "Cancelado"],
							placeholder="Estado",
							default_value="Todas",
							size="2",
							width="48%"
						),
						rx.select(
							["Más reciente", "Más antiguo"],
							placeholder="Ordenar",
							default_value="Más reciente",
							size="2",
							width="48%"
						),
						justify="between",
						width="100%",
						margin_bottom="1.5em"
					),
					
					# Lista de órdenes móvil (cards en lugar de tabla)
					rx.vstack(
						# Orden 1 móvil
						rx.box(
							rx.vstack(
								rx.hstack(
									rx.text("#12345", font_weight="bold", font_size="1.1em"),
									rx.spacer(),
									rx.badge("Pendiente", color_scheme="orange", size="1")
								),
								
								rx.vstack(
									rx.hstack(
										rx.icon("map-pin", size=14, color=rx.color("gray", 11)),
										rx.text("Av. Siempre Viva 742, Colima", font_size="0.85em", color=rx.color("gray", 11)),
										spacing="1"
									),
									rx.hstack(
										rx.icon("calendar", size=14, color=rx.color("gray", 11)),
										rx.text("10/09/2025", font_size="0.85em", color=rx.color("gray", 11)),
										spacing="1"
									),
									rx.hstack(
										rx.icon("credit-card", size=14, color=rx.color("gray", 11)),
										rx.text("Tarjeta crédito", font_size="0.85em", color=rx.color("gray", 11)),
										spacing="1"
									),
									spacing="1",
									align="start",
									width="100%"
								),
								
								rx.hstack(
									rx.text("Total:", font_size="0.9em"),
									rx.text("$1,746.50", font_weight="bold", font_size="1.1em", color=rx.color_mode_cond(
										light=Custom_theme().light_colors()["primary"],
										dark=Custom_theme().dark_colors()["primary"]
									)),
									align="center"
								),
								
								rx.hstack(
									rx.button(
										"Ver detalles",
										bg=rx.color_mode_cond(
											light=Custom_theme().light_colors()["primary"],
											dark=Custom_theme().dark_colors()["primary"]
										),
										color="white",
										width="48%",
										height="36px",
										font_size="0.85em",
										on_click=lambda: rx.redirect("/order_details")
									),
									rx.button(
										rx.icon("download", size=14),
										"PDF",
										variant="outline",
										width="48%",
										height="36px",
										font_size="0.85em"
									),
									width="100%",
									justify="between"
								),
								
								spacing="3",
								width="100%"
							),
							bg=rx.color_mode_cond(
								light=Custom_theme().light_colors()["tertiary"],
								dark=Custom_theme().dark_colors()["tertiary"]
							),
							border_radius="12px",
							padding="1em",
							width="100%",
							margin_bottom="0.8em"
						),
						
						# Orden 2 móvil
						rx.box(
							rx.vstack(
								rx.hstack(
									rx.text("#67890", font_weight="bold", font_size="1.1em"),
									rx.spacer(),
									rx.badge("Entregado", color_scheme="green", size="1")
								),
								
								rx.vstack(
									rx.hstack(
										rx.icon("map-pin", size=14, color=rx.color("gray", 11)),
										rx.text("Santo Domingo, RD", font_size="0.85em", color=rx.color("gray", 11)),
										spacing="1"
									),
									rx.hstack(
										rx.icon("calendar", size=14, color=rx.color("gray", 11)),
										rx.text("01/08/2025", font_size="0.85em", color=rx.color("gray", 11)),
										spacing="1"
									),
									rx.hstack(
										rx.icon("wallet", size=14, color=rx.color("gray", 11)),
										rx.text("Billetera digital", font_size="0.85em", color=rx.color("gray", 11)),
										spacing="1"
									),
									spacing="1",
									align="start",
									width="100%"
								),
								
								rx.hstack(
									rx.text("Total:", font_size="0.9em"),
									rx.text("$1,926.50", font_weight="bold", font_size="1.1em", color=rx.color_mode_cond(
										light=Custom_theme().light_colors()["primary"],
										dark=Custom_theme().dark_colors()["primary"]
									)),
									align="center"
								),
								
								rx.hstack(
									rx.button(
										"Ver detalles",
										bg=rx.color_mode_cond(
											light=Custom_theme().light_colors()["primary"],
											dark=Custom_theme().dark_colors()["primary"]
										),
										color="white",
										width="48%",
										height="36px",
										font_size="0.85em",
										on_click=lambda: rx.redirect("/order_details")
									),
									rx.button(
										rx.icon("download", size=14),
										"PDF",
										variant="outline",
										width="48%",
										height="36px",
										font_size="0.85em"
									),
									width="100%",
									justify="between"
								),
								
								spacing="3",
								width="100%"
							),
							bg=rx.color_mode_cond(
								light=Custom_theme().light_colors()["tertiary"],
								dark=Custom_theme().dark_colors()["tertiary"]
							),
							border_radius="12px",
							padding="1em",
							width="100%",
							margin_bottom="0.8em"
						),
						
						# Orden 3 móvil
						rx.box(
							rx.vstack(
								rx.hstack(
									rx.text("#11121", font_weight="bold", font_size="1.1em"),
									rx.spacer(),
									rx.badge("Cancelado", color_scheme="red", size="1")
								),
								
								rx.vstack(
									rx.hstack(
										rx.icon("map-pin", size=14, color=rx.color("gray", 11)),
										rx.text("Guadalajara, JAL", font_size="0.85em", color=rx.color("gray", 11)),
										spacing="1"
									),
									rx.hstack(
										rx.icon("calendar", size=14, color=rx.color("gray", 11)),
										rx.text("07/06/2025", font_size="0.85em", color=rx.color("gray", 11)),
										spacing="1"
									),
									rx.hstack(
										rx.icon("credit-card", size=14, color=rx.color("gray", 11)),
										rx.text("Tarjeta débito", font_size="0.85em", color=rx.color("gray", 11)),
										spacing="1"
									),
									spacing="1",
									align="start",
									width="100%"
								),
								
								rx.hstack(
									rx.text("Total:", font_size="0.9em"),
									rx.text("$349.30", font_weight="bold", font_size="1.1em", color=rx.color_mode_cond(
										light=Custom_theme().light_colors()["primary"],
										dark=Custom_theme().dark_colors()["primary"]
									)),
									align="center"
								),
								
								rx.hstack(
									rx.button(
										"Ver detalles",
										bg=rx.color_mode_cond(
											light=Custom_theme().light_colors()["primary"],
											dark=Custom_theme().dark_colors()["primary"]
										),
										color="white",
										width="48%",
										height="36px",
										font_size="0.85em",
										on_click=lambda: rx.redirect("/order_details")
									),
									rx.button(
										rx.icon("download", size=14),
										"PDF",
										variant="outline",
										width="48%",
										height="36px",
										font_size="0.85em"
									),
									width="100%",
									justify="between"
								),
								
								spacing="3",
								width="100%"
							),
							bg=rx.color_mode_cond(
								light=Custom_theme().light_colors()["tertiary"],
								dark=Custom_theme().dark_colors()["tertiary"]
							),
							border_radius="12px",
							padding="1em",
							width="100%",
							margin_bottom="0.8em"
						),
						
						width="100%"
					),
					
					# Paginación móvil
					rx.hstack(
						rx.button(
							rx.icon("chevron-left", size=14),
							variant="soft",
							disabled=True,
							size="2"
						),
						rx.text("1 de 4", font_size="0.9em"),
						rx.button(
							rx.icon("chevron-right", size=14),
							variant="soft",
							size="2"
						),
						justify="center",
						width="100%",
						margin_top="1.5em"
					),
					spacing="4",
					width="100%",
					padding="1em",
					margin_top="80px",
					margin_bottom="0.2em"
				),
				bg=rx.color_mode_cond(
					light=Custom_theme().light_colors()["background"],
					dark=Custom_theme().dark_colors()["background"]
				),
			),
			width="100%"
		),
		# Propiedades del contenedor principal.
		bg=rx.color_mode_cond(
			light=Custom_theme().light_colors()["background"],
			dark=Custom_theme().dark_colors()["background"]
		),
		position="absolute",
		width="100%"
	)