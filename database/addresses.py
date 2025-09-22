import reflex as rx

from sqlmodel import Field, ForeignKey
from enum import Enum

class Countries(Enum):
    USA = "USA"
    COLOMBIA = "COLOMBIA"
    MEXICO = "MEXICO"
    PUERTO_RICO = "PUERTO_RICO"

    def states(self):
        if self == Countries.USA:
            return ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
                    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
                    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
                    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
                    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
                    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
                    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
        elif self == Countries.COLOMBIA:
            return ["Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", "Boyacá", "Caldas", "Caquetá",
                    "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía",
                    "Guaviare","Huila","La Guajira","Magdalena","Meta","Nariño","Norte de Santander","Putumayo",
                    "Quindío","Risaralda","San Andrés y Providencia","Santander","Sucre","Tolima","Valle del Cauca",
                    "Vaupés","Vichada"]
        elif self == Countries.MEXICO:
            return ["Aguascalientes","Baja California","Baja California Sur","Campeche","Chiapas","Chihuahua",
                    "Ciudad de México","Coahuila","Colima","Durango","Guanajuato","Guerrero","Hidalgo","Jalisco",
                    "México","Michoacán","Morelos","Nayarit","Nuevo León","Oaxaca","Puebla","Querétaro",
                    "Quintana Roo","San Luis Potosí","Sinaloa","Sonora","Tabasco","Tamaulipas",
                    "Tlaxcala","Veracruz","Yucatán","Zacatecas"]
        elif self == Countries.PUERTO_RICO:
            return ["Adjuntas","Aguada","Aguadilla","Aguasbuena","Aibonito","Anasco","Arecibo","Arroyo",
                    "Barceloneta","Barranquitas","Bayamón","Cabo Rojo","Caguas","Camuy","Canóvanas","Carolina",
                    "Cataño","Cayey","Ceiba","Ciales","Cidra","Coamo","Comerío","Corozal","Culebra","Dorado",
                    "Fajardo","Florida","Guánica","Guayama","Guayanilla","Guaynabo","Gurabo","Hatillo","Hormigueros",
                    "Humacao","Isabela","Jayuya","Juana Díaz","Juncos","Lajas","Lares","Las Marías","Las Piedras","Loíza",
                    "Luquillo","Manatí","Maricao","Maunabo","Mayagüez","Moca","Morovis","Naguabo","Naranjito","Orocovis",
                    "Patillas","Peñuelas","Ponce","Quebradillas","Rincón","Río Grande","Sabana Grande","Salinas","San Germán","San Juan",
                    "San Lorenzo","San Sebastián","Santa Isabel","Toa Alta","Toa Baja","Trujillo Alto","Utuado","Vega Alta","Vega Baja","Vieques",
                    "Villalba","Yabucoa","Yauco"]

class Addresses(rx.Model, table=True):
    """
    Tabla de direcciones.
    Contiene información de direcciones asociadas a usuarios.
    """
    id: int = Field(primary_key=True, index=True)

    # Información de dirección
    street: str = Field(index=True)
    neighborhood: str = Field(index=True)
    city: str = Field(index=True)
    state: str = Field(index=True)
    country: Countries = Field(index=True)
    zip_code: str = Field(index=True)