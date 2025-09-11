"""Nueva Backoffice NN Protect | Reportes de ingresos"""

import reflex as rx
from ..theme import Custom_theme
from rxconfig import config
from ..layout import main_container_derecha, mobile_header, desktop_sidebar, mobile_sidebar

def income_reports() -> rx.Component:
    return rx.center(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    desktop_sidebar(),
                    main_container_derecha(
                        rx.vstack(
                            rx.text(
                                "Reportes de ingresos",
                                font_size="2rem",
                                font_weight="bold",
                                margin_bottom="1rem"
                            ),
                            
                            # Resumen de ingresos
                            rx.hstack(
                                rx.box(
                                    rx.vstack(
                                        rx.text("Ingresos totales", font_weight="bold", font_size="1.1rem"),
                                        rx.text("$15,420.50", font_size="2rem", font_weight="bold", color=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["primary"],
                                            dark=Custom_theme().dark_colors()["primary"]
                                        )),
                                        rx.text("Este mes", font_size="0.9rem", color="gray"),
                                        spacing="2",
                                        align="center"
                                    ),
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    border_radius="16px",
                                    padding="2rem",
                                    width="30%"
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.text("Comisiones", font_weight="bold", font_size="1.1rem"),
                                        rx.text("$3,280.75", font_size="2rem", font_weight="bold", color=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["secondary"],
                                            dark=Custom_theme().dark_colors()["secondary"]
                                        )),
                                        rx.text("Este mes", font_size="0.9rem", color="gray"),
                                        spacing="2",
                                        align="center"
                                    ),
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    border_radius="16px",
                                    padding="2rem",
                                    width="30%"
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.text("Bonos", font_weight="bold", font_size="1.1rem"),
                                        rx.text("$1,890.25", font_size="2rem", font_weight="bold", color="green"),
                                        rx.text("Este mes", font_size="0.9rem", color="gray"),
                                        spacing="2",
                                        align="center"
                                    ),
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["tertiary"],
                                        dark=Custom_theme().dark_colors()["tertiary"]
                                    ),
                                    border_radius="16px",
                                    padding="2rem",
                                    width="30%"
                                ),
                                justify="between",
                                width="100%",
                                margin_bottom="2rem"
                            ),
                            
                            # Tabla de ingresos detallada
                            rx.box(
                                rx.vstack(
                                    rx.text("Detalle de ingresos por mes", font_weight="bold", font_size="1.3rem", margin_bottom="1rem"),
                                    rx.table.root(
                                        rx.table.header(
                                            rx.table.row(
                                                rx.table.column_header_cell("Mes"),
                                                rx.table.column_header_cell("Ventas personales"),
                                                rx.table.column_header_cell("Comisiones red"),
                                                rx.table.column_header_cell("Bonos"),
                                                rx.table.column_header_cell("Total"),
                                                rx.table.column_header_cell("Estado")
                                            )
                                        ),
                                        rx.table.body(
                                            *[rx.table.row(
                                                rx.table.row_header_cell(f"Enero 2024"),
                                                rx.table.cell("$4,500.00"),
                                                rx.table.cell("$1,200.50"),
                                                rx.table.cell("$800.25"),
                                                rx.table.cell("$6,500.75", font_weight="bold"),
                                                rx.table.cell(rx.badge("Pagado", color="green"))
                                            ),
                                            rx.table.row(
                                                rx.table.row_header_cell(f"Febrero 2024"),
                                                rx.table.cell("$3,800.00"),
                                                rx.table.cell("$950.75"),
                                                rx.table.cell("$650.50"),
                                                rx.table.cell("$5,401.25", font_weight="bold"),
                                                rx.table.cell(rx.badge("Pagado", color="green"))
                                            ),
                                            rx.table.row(
                                                rx.table.row_header_cell(f"Marzo 2024"),
                                                rx.table.cell("$5,200.00"),
                                                rx.table.cell("$1,580.25"),
                                                rx.table.cell("$920.75"),
                                                rx.table.cell("$7,701.00", font_weight="bold"),
                                                rx.table.cell(rx.badge("Pendiente", color="orange"))
                                            )]
                                        ),
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
                                padding="2rem",
                                width="100%"
                            ),
                            
                            spacing="4",
                            width="100%"
                        )
                    )
                ),
                justify="center",
                margin_top="120px",
                margin_bottom="2em",
                max_width="1440px",
            )
        ),
        
        # Versión móvil
        rx.mobile_only(
            rx.vstack(
                # Header móvil
                mobile_header(),
                
                # Contenido principal móvil
                rx.vstack(
                    # Resumen de ingresos móvil
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.text("Ingresos totales", font_weight="bold", font_size="1rem", text_align="center"),
                                rx.text("$15,420.50", font_size="1.8rem", font_weight="bold", color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ), text_align="center"),
                                rx.text("Este mes", font_size="0.8rem", color="gray", text_align="center"),
                                spacing="1"
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["tertiary"],
                                dark=Custom_theme().dark_colors()["tertiary"]
                            ),
                            border_radius="12px",
                            padding="1.5rem",
                            width="100%",
                            margin_bottom="1rem"
                        ),
                        
                        rx.hstack(
                            rx.box(
                                rx.vstack(
                                    rx.text("Comisiones", font_weight="bold", font_size="0.9rem", text_align="center"),
                                    rx.text("$3,280.75", font_size="1.3rem", font_weight="bold", color=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["secondary"],
                                        dark=Custom_theme().dark_colors()["secondary"]
                                    ), text_align="center"),
                                    spacing="1"
                                ),
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                                border_radius="12px",
                                padding="1rem",
                                width="48%"
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.text("Bonos", font_weight="bold", font_size="0.9rem", text_align="center"),
                                    rx.text("$1,890.25", font_size="1.3rem", font_weight="bold", color="green", text_align="center"),
                                    spacing="1"
                                ),
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                                border_radius="12px",
                                padding="1rem",
                                width="48%"
                            ),
                            justify="between",
                            width="100%"
                        ),
                        
                        width="100%",
                        margin_bottom="2rem"
                    ),
                    
                    # Tabla móvil simplificada
                    rx.box(
                        rx.vstack(
                            rx.text("Historial de ingresos", font_weight="bold", font_size="1.2rem", margin_bottom="1rem"),
                            
                            *[rx.box(
                                rx.vstack(
                                    rx.hstack(
                                        rx.text(f"Enero 2024", font_weight="bold"),
                                        rx.spacer(),
                                        rx.badge("Pagado", color="green")
                                    ),
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text("Ventas", font_size="0.8rem", color="gray"),
                                            rx.text("$4,500.00", font_weight="bold", font_size="0.9rem")
                                        ),
                                        rx.vstack(
                                            rx.text("Comisiones", font_size="0.8rem", color="gray"),
                                            rx.text("$1,200.50", font_weight="bold", font_size="0.9rem")
                                        ),
                                        rx.vstack(
                                            rx.text("Total", font_size="0.8rem", color="gray"),
                                            rx.text("$6,500.75", font_weight="bold", font_size="1rem", color=rx.color_mode_cond(
                                                light=Custom_theme().light_colors()["primary"],
                                                dark=Custom_theme().dark_colors()["primary"]
                                            ))
                                        ),
                                        justify="between",
                                        width="100%"
                                    ),
                                    spacing="2",
                                    width="100%"
                                ),
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["tertiary"],
                                    dark=Custom_theme().dark_colors()["tertiary"]
                                ),
                                border_radius="12px",
                                padding="1rem",
                                width="100%",
                                margin_bottom="0.5rem"
                            ) for i in range(3)],
                            
                            width="100%"
                        ),
                        width="100%"
                    ),
                    
                    spacing="4",
                    width="100%",
                    padding="1rem",
                    margin_top="80px"
                ),
                
                width="100%",
                min_height="100vh",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["background"],
                    dark=Custom_theme().dark_colors()["background"]
                )
            )
        ),
        
        bg=rx.color_mode_cond(
            light=Custom_theme().light_colors()["background"],
            dark=Custom_theme().dark_colors()["background"]
        ),
        position="absolute",
        width="100%",
    )