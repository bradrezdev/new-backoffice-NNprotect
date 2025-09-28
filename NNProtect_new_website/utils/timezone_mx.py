"""
Utilidades para manejo de timezone de México Central (GMT-6)
Solución efectiva: restar 6 horas a UTC para obtener México Central.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

def get_mexico_now() -> datetime:
    """
    Obtiene tiempo actual en México Central restando 6 horas a UTC.
    Solución KISS: UTC - 6 horas = México Central.
    """
    utc_now = datetime.utcnow()
    mexico_time = utc_now - timedelta(hours=6)
    return mexico_time

def get_mexico_date() -> datetime:
    """Alias para compatibilidad."""
    return get_mexico_now()

def get_mexico_datetime_naive() -> datetime:
    """
    Retorna datetime México Central sin tzinfo (naive).
    Para compatibilidad con código existente.
    """
    return get_mexico_now().replace(tzinfo=None)

def format_mexico_date(dt: datetime) -> str:
    """Formatea fecha en formato DD/MM/YYYY."""
    if dt:
        return dt.strftime("%d/%m/%Y")
    return ""

def format_mexico_datetime(dt: datetime) -> str:
    """Formatea datetime en formato DD/MM/YYYY HH:MM."""
    if dt:
        return dt.strftime("%d/%m/%Y %H:%M")
    return ""

def convert_to_mexico_time(dt: datetime) -> datetime:
    """Convierte cualquier datetime a México Central."""
    if dt.tzinfo is None:
        # Asumir UTC si no tiene tzinfo
        dt = dt.replace(tzinfo=timezone.utc)
    mexico_tz = timezone(timedelta(hours=-6))
    return dt.astimezone(mexico_tz)

def print_timezone_info():
    """Debug: muestra tiempo UTC vs México Central."""
    utc_time = datetime.utcnow()
    mexico_time = get_mexico_now()
    
    print(f"🌍 UTC:           {utc_time}")
    print(f"🇲🇽 México (-6h): {mexico_time}")
    print(f"✅ Diferencia:    {(utc_time - mexico_time).total_seconds() / 3600} horas")