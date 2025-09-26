"""
Utilidades para manejo de timezone de México Central (GMT-6)
Proporciona funciones consistentes para obtener tiempo actual en horario de México.
"""
import datetime
import pytz
from typing import Optional

# Timezone de México Central
MEXICO_TIMEZONE = pytz.timezone('America/Mexico_City')

def get_mexico_now() -> datetime.datetime:
    """
    Obtiene la fecha y hora actual en horario de México Central.
    
    Returns:
        datetime.datetime: Fecha y hora actual en timezone de México
    """
    utc_now = datetime.datetime.now(pytz.UTC)
    mexico_now = utc_now.astimezone(MEXICO_TIMEZONE)
    return mexico_now

def get_mexico_date() -> datetime.date:
    """
    Obtiene la fecha actual en horario de México Central.
    
    Returns:
        datetime.date: Fecha actual en timezone de México
    """
    return get_mexico_now().date()

def get_mexico_datetime_naive() -> datetime.datetime:
    """
    Obtiene datetime naive (sin timezone) en horario de México Central.
    Útil para compatibilidad con sistemas que no manejan timezone.
    
    Returns:
        datetime.datetime: Datetime naive en horario de México
    """
    return get_mexico_now().replace(tzinfo=None)

def convert_to_mexico_time(dt: datetime.datetime) -> datetime.datetime:
    """
    Convierte cualquier datetime a horario de México Central.
    
    Args:
        dt: Datetime a convertir (puede tener timezone o ser naive)
        
    Returns:
        datetime.datetime: Datetime convertido a horario de México
    """
    if dt.tzinfo is None:
        # Si es naive, asumimos UTC
        dt = pytz.UTC.localize(dt)
    
    return dt.astimezone(MEXICO_TIMEZONE)

def format_mexico_datetime(dt: Optional[datetime.datetime] = None, format_str: str = "%d/%m/%Y %H:%M") -> str:
    """
    Formatea datetime en horario de México con formato personalizado.
    
    Args:
        dt: Datetime a formatear (si es None, usa tiempo actual)
        format_str: Formato de salida
        
    Returns:
        str: Fecha formateada en horario de México
    """
    if dt is None:
        dt = get_mexico_now()
    elif dt.tzinfo is None:
        dt = pytz.UTC.localize(dt).astimezone(MEXICO_TIMEZONE)
    else:
        dt = dt.astimezone(MEXICO_TIMEZONE)
    
    return dt.strftime(format_str)

def format_mexico_date(dt: Optional[datetime.datetime] = None) -> str:
    """
    Formatea fecha en formato DD/MM/YYYY en horario de México.
    
    Args:
        dt: Datetime a formatear (si es None, usa tiempo actual)
        
    Returns:
        str: Fecha formateada como DD/MM/YYYY
    """
    return format_mexico_datetime(dt, "%d/%m/%Y")

def format_mexico_datetime_iso(dt: Optional[datetime.datetime] = None) -> str:
    """
    Formatea datetime en formato ISO en horario de México.
    
    Args:
        dt: Datetime a formatear (si es None, usa tiempo actual)
        
    Returns:
        str: Datetime en formato ISO
    """
    if dt is None:
        dt = get_mexico_now()
    elif dt.tzinfo is None:
        dt = pytz.UTC.localize(dt).astimezone(MEXICO_TIMEZONE)
    else:
        dt = dt.astimezone(MEXICO_TIMEZONE)
    
    return dt.isoformat()

# Debug function
def print_timezone_info():
    """Imprime información de debugging sobre el timezone actual."""
    now_utc = datetime.datetime.now(pytz.UTC)
    now_mexico = get_mexico_now()
    
    print(f"🌍 UTC: {now_utc}")
    print(f"🇲🇽 México Central: {now_mexico}")
    print(f"📅 Fecha México: {get_mexico_date()}")
    print(f"⏰ Formato estándar: {format_mexico_datetime()}")