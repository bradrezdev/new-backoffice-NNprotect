"""
Gestor de productos para la tienda NN Protect.
Maneja la lógica de negocio para obtener productos con precios según país.
"""
import reflex as rx
from typing import List, Dict, Optional
from database.products import Products
from database.addresses import Countries


class ProductManager:
    """
    Clase para gestionar la lógica de productos en la tienda.
    Sigue principios POO para encapsular operaciones de productos.
    """

    @staticmethod
    def get_all_products() -> List[Products]:
        """
        Obtiene todos los productos de la base de datos.
        
        Returns:
            List[Products]: Lista de todos los productos
        """
        try:
            with rx.session() as session:
                from sqlmodel import select
                statement = select(Products)
                products = session.exec(statement).all()
                return list(products)
        except Exception as e:
            print(f"❌ Error obteniendo productos: {e}")
            return []

    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Products]:
        """
        Obtiene un producto específico por su ID.
        Principio KISS: consulta simple y directa.
        
        Args:
            product_id: ID del producto a buscar
            
        Returns:
            Products: Objeto producto o None si no existe
        """
        try:
            with rx.session() as session:
                from sqlmodel import select
                statement = select(Products).where(Products.id == product_id)
                product = session.exec(statement).first()
                return product
        except Exception as e:
            print(f"❌ Error obteniendo producto {product_id}: {e}")
            return None

    @staticmethod
    def get_product_price_by_country(product: Products, country: Countries) -> Optional[float]:
        """
        Obtiene el precio de un producto según el país.
        Aplica principio KISS: lógica simple y directa.
        
        Args:
            product: Objeto producto
            country: País del usuario (enum Countries)
            
        Returns:
            float: Precio del producto en la moneda del país, None si no existe
        """
        price_mapping = {
            Countries.MEXICO: product.price_mx,
            Countries.USA: product.price_usa,
            Countries.COLOMBIA: product.price_colombia,
            Countries.PUERTO_RICO: product.price_usa  # Puerto Rico usa precio USA
        }
        
        return price_mapping.get(country)

    @staticmethod
    def get_product_pv_by_country(product: Products, country: Countries) -> int:
        """
        Obtiene los puntos de valor (PV) de un producto según el país.
        
        Args:
            product: Objeto producto
            country: País del usuario
            
        Returns:
            int: Puntos de valor del producto
        """
        pv_mapping = {
            Countries.MEXICO: product.pv_mx,
            Countries.USA: product.pv_usa,
            Countries.COLOMBIA: product.pv_colombia,
            Countries.PUERTO_RICO: product.pv_usa  # Puerto Rico usa PV USA
        }
        
        return pv_mapping.get(country, 0)

    @staticmethod
    def get_product_vn_by_country(product: Products, country: Countries) -> Optional[float]:
        """
        Obtiene el valor neto (VN) de un producto según el país.
        
        Args:
            product: Objeto producto
            country: País del usuario
            
        Returns:
            float: Valor neto del producto, None si no existe
        """
        vn_mapping = {
            Countries.MEXICO: product.vn_mx,
            Countries.USA: product.vn_usa,
            Countries.COLOMBIA: product.vn_colombia,
            Countries.PUERTO_RICO: product.vn_usa  # Puerto Rico usa VN USA
        }
        
        return vn_mapping.get(country)

    @staticmethod
    def get_currency_symbol_by_country(country: Countries) -> str:
        """
        Obtiene el símbolo de moneda según el país.
        Principio DRY: centralizamos la lógica de monedas.
        
        Args:
            country: País del usuario
            
        Returns:
            str: Símbolo de la moneda
        """
        currency_mapping = {
            Countries.MEXICO: "$",
            Countries.USA: "$",
            Countries.COLOMBIA: "$",
            Countries.PUERTO_RICO: "$"
        }
        
        return currency_mapping.get(country, "$")

    @staticmethod
    def format_product_data_for_store(products: List[Products], user_country: Countries) -> List[Dict]:
        """
        Formatea los datos de productos para usar en la tienda.
        Aplica principio YAGNI: solo los datos necesarios para la tienda.
        
        Args:
            products: Lista de productos
            user_country: País del usuario autenticado
            
        Returns:
            List[Dict]: Lista de productos formateados para la tienda
        """
        formatted_products = []
        
        for product in products:
            price = ProductManager.get_product_price_by_country(product, user_country)
            pv = ProductManager.get_product_pv_by_country(product, user_country)
            vn = ProductManager.get_product_vn_by_country(product, user_country)
            currency = ProductManager.get_currency_symbol_by_country(user_country)
            
            # Solo incluir productos que tengan precio definido
            if price is not None:
                formatted_products.append({
                    "id": product.id,
                    "name": product.product_name,
                    "type": product.type,
                    "presentation": product.presentation,
                    "description": product.description or "",
                    "price": price,
                    "pv": pv,
                    "vn": vn,
                    "currency": currency,
                    "formatted_price": f"{currency}{price:.2f}"
                })
        
        return formatted_products

    @staticmethod
    def get_latest_products() -> List[Products]:
        """
        Obtiene productos marcados como nuevos (is_new = True).
        Principio KISS: consulta simple y directa.
        
        Returns:
            List[Products]: Lista de productos nuevos
        """
        try:
            with rx.session() as session:
                from sqlmodel import select
                statement = select(Products).where(Products.is_new == True)
                latest_products = session.exec(statement).all()
                return list(latest_products)
        except Exception as e:
            print(f"❌ Error obteniendo productos nuevos: {e}")
            return []

    @staticmethod
    def get_popular_products(limit: int = 5) -> List[Products]:
        """
        Obtiene los productos más populares basados en purchase_count.
        Principio YAGNI: solo los datos necesarios para mostrar productos populares.
        
        Args:
            limit: Número máximo de productos a retornar (default: 5)
            
        Returns:
            List[Products]: Lista de productos más comprados
        """
        try:
            with rx.session() as session:
                from sqlmodel import select, desc
                statement = select(Products).where(
                    Products.purchase_count > 0
                ).order_by(desc(Products.purchase_count)).limit(limit)
                popular_products = session.exec(statement).all()
                return list(popular_products)
        except Exception as e:
            print(f"❌ Error obteniendo productos populares: {e}")
            return []

    @staticmethod
    def increment_purchase_count(product_id: int) -> bool:
        """
        Incrementa el contador de compras de un producto en +1.
        Se debe llamar cuando se finaliza una compra (no al agregar al carrito).
        Principio POO: método específico para una operación de negocio.
        
        Args:
            product_id: ID del producto comprado
            
        Returns:
            bool: True si se actualizó correctamente, False en caso de error
        """
        try:
            with rx.session() as session:
                from sqlmodel import select
                
                # Buscar el producto
                statement = select(Products).where(Products.id == product_id)
                product = session.exec(statement).first()
                
                if product:
                    # Incrementar contador
                    product.purchase_count += 1
                    session.add(product)
                    session.commit()
                    print(f"✅ Contador de compras incrementado para producto {product_id}")
                    return True
                else:
                    print(f"❌ Producto {product_id} no encontrado")
                    return False
                    
        except Exception as e:
            print(f"❌ Error incrementando contador de compras: {e}")
            return False

    @staticmethod
    def get_latest_products_formatted(user_country: Countries) -> List[Dict]:
        """
        Obtiene productos nuevos formateados para la tienda.
        Principio DRY: reutiliza format_product_data_for_store.
        
        Args:
            user_country: País del usuario para precios correctos
            
        Returns:
            List[Dict]: Lista de productos nuevos formateados
        """
        latest_products = ProductManager.get_latest_products()
        return ProductManager.format_product_data_for_store(latest_products, user_country)

    @staticmethod
    def get_popular_products_formatted(user_country: Countries, limit: int = 5) -> List[Dict]:
        """
        Obtiene productos populares formateados para la tienda.
        Principio DRY: reutiliza format_product_data_for_store.
        
        Args:
            user_country: País del usuario para precios correctos
            limit: Número máximo de productos a retornar
            
        Returns:
            List[Dict]: Lista de productos populares formateados
        """
        popular_products = ProductManager.get_popular_products(limit)
        return ProductManager.format_product_data_for_store(popular_products, user_country)

    @staticmethod
    def get_products_by_type(product_type: str) -> List[Products]:
        """
        Obtiene productos filtrados por tipo específico.
        Principio KISS: consulta simple y directa por tipo.
        
        Args:
            product_type: Tipo de producto ("kit de inicio", "suplemento", "skincare", "desinfectante")
            
        Returns:
            List[Products]: Lista de productos del tipo especificado
        """
        try:
            with rx.session() as session:
                from sqlmodel import select
                statement = select(Products).where(Products.type == product_type)
                products = session.exec(statement).all()
                return list(products)
        except Exception as e:
            print(f"❌ Error obteniendo productos tipo '{product_type}': {e}")
            return []

    @staticmethod
    def get_kit_inicio_products() -> List[Products]:
        """
        Obtiene productos del tipo "kit de inicio".
        Método específico para kits de inicio.
        
        Returns:
            List[Products]: Lista de kits de inicio
        """
        return ProductManager.get_products_by_type("kit de inicio")

    @staticmethod
    def get_supplement_products() -> List[Products]:
        """
        Obtiene productos del tipo "suplemento".
        Método específico para suplementos nutricionales.
        
        Returns:
            List[Products]: Lista de suplementos
        """
        return ProductManager.get_products_by_type("suplemento")

    @staticmethod
    def get_skincare_products() -> List[Products]:
        """
        Obtiene productos del tipo "skincare".
        Método específico para productos de cuidado de la piel.
        
        Returns:
            List[Products]: Lista de productos skincare
        """
        return ProductManager.get_products_by_type("skincare")

    @staticmethod
    def get_sanitize_products() -> List[Products]:
        """
        Obtiene productos del tipo "desinfectante".
        Método específico para productos desinfectantes.
        
        Returns:
            List[Products]: Lista de productos desinfectantes
        """
        return ProductManager.get_products_by_type("desinfectante")

    @staticmethod
    def get_kit_inicio_products_formatted(user_country: Countries) -> List[Dict]:
        """
        Obtiene kits de inicio formateados para la tienda.
        Principio DRY: reutiliza format_product_data_for_store.
        
        Args:
            user_country: País del usuario para precios correctos
            
        Returns:
            List[Dict]: Lista de kits de inicio formateados
        """
        kit_products = ProductManager.get_kit_inicio_products()
        return ProductManager.format_product_data_for_store(kit_products, user_country)

    @staticmethod
    def get_supplement_products_formatted(user_country: Countries) -> List[Dict]:
        """
        Obtiene suplementos formateados para la tienda.
        Principio DRY: reutiliza format_product_data_for_store.
        
        Args:
            user_country: País del usuario para precios correctos
            
        Returns:
            List[Dict]: Lista de suplementos formateados
        """
        supplement_products = ProductManager.get_supplement_products()
        return ProductManager.format_product_data_for_store(supplement_products, user_country)

    @staticmethod
    def get_skincare_products_formatted(user_country: Countries) -> List[Dict]:
        """
        Obtiene productos skincare formateados para la tienda.
        Principio DRY: reutiliza format_product_data_for_store.
        
        Args:
            user_country: País del usuario para precios correctos
            
        Returns:
            List[Dict]: Lista de productos skincare formateados
        """
        skincare_products = ProductManager.get_skincare_products()
        return ProductManager.format_product_data_for_store(skincare_products, user_country)

    @staticmethod
    def get_sanitize_products_formatted(user_country: Countries) -> List[Dict]:
        """
        Obtiene productos desinfectantes formateados para la tienda.
        Principio DRY: reutiliza format_product_data_for_store.
        
        Args:
            user_country: País del usuario para precios correctos
            
        Returns:
            List[Dict]: Lista de productos desinfectantes formateados
        """
        sanitize_products = ProductManager.get_sanitize_products()
        return ProductManager.format_product_data_for_store(sanitize_products, user_country)