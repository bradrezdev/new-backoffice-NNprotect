"""
Servicio de datos de productos para la tienda NN Protect.
Proporciona una interfaz simplificada para acceder a productos.
"""
from typing import List, Dict, Optional
from database.addresses import Countries
from ..product_manager import ProductManager


class ProductDataService:
    """
    Servicio que proporciona acceso a datos de productos.
    Sigue principio de responsabilidad única (POO).
    """
    
    @staticmethod
    def get_products_for_store(user_country: Countries) -> List[Dict]:
        """
        Obtiene productos formateados para mostrar en la tienda.
        Principio DRY: reutiliza ProductManager.
        
        Args:
            user_country: País del usuario autenticado
            
        Returns:
            List[Dict]: Productos formateados para la tienda
        """
        products = ProductManager.get_all_products()
        return ProductManager.format_product_data_for_store(products, user_country)
    
    @staticmethod
    def get_products_by_type(user_country: Countries, product_type: str) -> List[Dict]:
        """
        Obtiene productos filtrados por tipo.
        Principio YAGNI: solo filtrado básico por tipo.
        
        Args:
            user_country: País del usuario
            product_type: Tipo de producto (suplemento, skincare, etc.)
            
        Returns:
            List[Dict]: Productos filtrados y formateados
        """
        all_products = ProductDataService.get_products_for_store(user_country)
        return [p for p in all_products if p["type"] == product_type]
    
    @staticmethod
    def get_product_by_id(product_id: int, user_country: Countries) -> Optional[Dict]:
        """
        Obtiene un producto específico por ID.
        
        Args:
            product_id: ID del producto
            user_country: País del usuario
            
        Returns:
            Dict: Datos del producto formateados, None si no existe
        """
        all_products = ProductDataService.get_products_for_store(user_country)
        for product in all_products:
            if product["id"] == product_id:
                return product
        return None