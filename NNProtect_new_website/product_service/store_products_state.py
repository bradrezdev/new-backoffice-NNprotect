"""
Estado para la tienda de productos NN Protect.
Maneja la carga y visualización de productos con precios por país.
"""
import reflex as rx
from typing import List, Dict, Optional
from database.addresses import Countries
from .product_data.product_data_service import ProductDataService
from ..auth_service.auth_state import UserDataManager
from .product_manager import ProductManager

class CountProducts(rx.State):
    """
    Contador individual por producto y sistema de carrito.
    Principio KISS: variables estáticas que Reflex puede rastrear.
    """
    
    # ✅ SOLUCIÓN: Definir atributos directamente como variables de clase
    count_1: int = 0
    count_2: int = 0
    count_3: int = 0
    count_4: int = 0
    count_5: int = 0
    count_6: int = 0
    count_7: int = 0
    count_8: int = 0
    count_9: int = 0
    count_10: int = 0
    count_11: int = 0
    count_12: int = 0
    count_13: int = 0
    count_14: int = 0
    count_15: int = 0
    count_16: int = 0
    count_17: int = 0
    count_18: int = 0
    count_19: int = 0
    count_20: int = 0
    count_21: int = 0
    count_22: int = 0
    count_23: int = 0
    count_24: int = 0
    
    # Sistema de carrito - Principio KISS: variables simples y claras
    cart_total: int = 0
    cart_items: Dict[str, int] = {}

    @rx.event
    def increment(self, product_id: int):
        """Incrementa contador específico usando setattr"""
        current = getattr(self, f"count_{product_id}", 0)
        setattr(self, f"count_{product_id}", current + 1)
        print(f"DEBUG: Producto {product_id} incrementado a {getattr(self, f'count_{product_id}')}")
    
    @rx.event  
    def decrement(self, product_id: int):
        """Decrementa contador específico usando setattr"""
        current = getattr(self, f"count_{product_id}", 0)
        if current > 0:
            setattr(self, f"count_{product_id}", current - 1)
            print(f"DEBUG: Producto {product_id} decrementado a {getattr(self, f'count_{product_id}')}")
        else:
            print(f"DEBUG: Producto {product_id} ya está en 0")

    @rx.var
    def get_count_reactive(self) -> Dict[str, int]:
        """
        Método reactivo que devuelve un diccionario con todos los contadores.
        Principio DRY: un solo método para acceder a todos los contadores de forma reactiva.
        """
        return {
            "1": self.count_1, "2": self.count_2, "3": self.count_3, "4": self.count_4,
            "5": self.count_5, "6": self.count_6, "7": self.count_7, "8": self.count_8,
            "9": self.count_9, "10": self.count_10, "11": self.count_11, "12": self.count_12,
            "13": self.count_13, "14": self.count_14, "15": self.count_15, "16": self.count_16,
            "17": self.count_17, "18": self.count_18, "19": self.count_19, "20": self.count_20,
            "21": self.count_21, "22": self.count_22, "23": self.count_23, "24": self.count_24
        }

    @rx.event
    def add_to_cart(self, product_id: int):
        """
        Añade la cantidad actual del contador del producto al carrito.
        Principio KISS: operación simple y directa.
        """
        current_count = getattr(self, f"count_{product_id}", 0)
        
        if current_count == 0:
            print(f"DEBUG: No hay cantidad seleccionada para producto {product_id}")
            return
            
        # Verificar límite máximo de 20 productos en total
        if self.cart_total + current_count > 20:
            remaining_space = 20 - self.cart_total
            if remaining_space > 0:
                # Añadir solo lo que cabe
                self.cart_items[str(product_id)] = self.cart_items.get(str(product_id), 0) + remaining_space
                self.cart_total += remaining_space
                print(f"DEBUG: Solo se pudieron añadir {remaining_space} del producto {product_id}. Carrito lleno (20/20)")
            else:
                print(f"DEBUG: Carrito lleno. No se puede añadir producto {product_id}")
            return
        
        # Añadir productos al carrito
        self.cart_items[str(product_id)] = self.cart_items.get(str(product_id), 0) + current_count
        self.cart_total += current_count
        
        # Resetear contador del producto después de añadir
        setattr(self, f"count_{product_id}", 0)
        
        print(f"DEBUG: Añadidos {current_count} del producto {product_id} al carrito. Total: {self.cart_total}")

    @rx.event 
    def clear_cart(self):
        """
        Vacía completamente el carrito.
        Principio YAGNI: implementación simple para funcionalidad básica.
        """
        self.cart_total = 0
        self.cart_items = {}
        print("DEBUG: Carrito vaciado completamente")

    @rx.var
    def cart_items_detailed(self) -> List[Dict]:
        """
        Propiedad computada que devuelve los productos del carrito con información completa.
        Principio DRY: un solo lugar para obtener datos completos del carrito.
        """
        if not self.cart_items:
            return []
            
        from .product_manager import ProductManager
        from database.addresses import Countries
        
        cart_items = []
        user_country = Countries.MEXICO  # Por defecto México
        
        for product_id_str, quantity in self.cart_items.items():
            product_id = int(product_id_str)
            
            # Obtener información del producto
            product = ProductManager.get_product_by_id(product_id)
            if not product:
                continue
                
            # Obtener precio y puntos según país del usuario
            price = ProductManager.get_product_price_by_country(product, user_country)
            volume_points = ProductManager.get_product_pv_by_country(product, user_country)
            
            if price is None:
                continue
                
            # Calcular subtotales
            subtotal = price * quantity
            volume_subtotal = volume_points * quantity
            
            # Construir objeto de producto para el carrito
            cart_item = {
                "id": product_id,
                "name": product.product_name,
                "price": price,
                "quantity": quantity,
                "volume_points": volume_points,
                "image": f"/product_{product_id}.jpg",
                "subtotal": subtotal,
                "volume_subtotal": volume_subtotal
            }
            cart_items.append(cart_item)
            
        return cart_items

    @rx.var
    def cart_subtotal(self) -> float:
        """Subtotal de productos en el carrito"""
        return sum(item["subtotal"] for item in self.cart_items_detailed)

    @rx.var
    def cart_volume_points(self) -> int:
        """Total de puntos de volumen en el carrito"""
        return sum(item["volume_subtotal"] for item in self.cart_items_detailed)

    @rx.var
    def cart_shipping_cost(self) -> float:
        """Costo de envío basado en el subtotal"""
        return 99.00 if self.cart_subtotal < 1000 else 0.00

    @rx.var
    def cart_final_total(self) -> float:
        """Total final del carrito incluyendo envío"""
        return self.cart_subtotal + self.cart_shipping_cost

    @rx.event
    def increment_cart_item(self, product_id: int):
        """Incrementa cantidad de un producto específico en el carrito"""
        key = str(product_id)
        print(f"DEBUG CART: Intentando incrementar producto {product_id}")
        
        if key in self.cart_items and self.cart_total < 20:
            self.cart_items[key] += 1
            self.cart_total += 1
            print(f"DEBUG CART: ✅ Producto {product_id} incrementado a {self.cart_items[key]} unidades. Total carrito: {self.cart_total}")
        elif key not in self.cart_items:
            print(f"DEBUG CART: ❌ Producto {product_id} no está en el carrito")
        elif self.cart_total >= 20:
            print(f"DEBUG CART: ❌ Carrito lleno (límite 20 productos)")
    
    @rx.event
    def decrement_cart_item(self, product_id: int):
        """Decrementa cantidad de un producto específico en el carrito"""
        key = str(product_id)
        print(f"DEBUG CART: Intentando decrementar producto {product_id}")
        
        if key in self.cart_items and self.cart_items[key] > 1:
            self.cart_items[key] -= 1
            self.cart_total -= 1
            print(f"DEBUG CART: ✅ Producto {product_id} decrementado a {self.cart_items[key]} unidades. Total carrito: {self.cart_total}")
        elif key in self.cart_items and self.cart_items[key] == 1:
            # Si llega a 1, decrementar elimina el producto
            del self.cart_items[key]
            self.cart_total -= 1
            print(f"DEBUG CART: ✅ Producto {product_id} eliminado del carrito (llegó a 0). Total carrito: {self.cart_total}")
        elif key not in self.cart_items:
            print(f"DEBUG CART: ❌ Producto {product_id} no está en el carrito")
    
    @rx.event
    def remove_from_cart(self, product_id: int):
        """Elimina completamente un producto del carrito"""
        key = str(product_id)
        print(f"DEBUG CART: Intentando eliminar producto {product_id}")
        
        if key in self.cart_items:
            removed_quantity = self.cart_items[key]
            del self.cart_items[key]
            self.cart_total -= removed_quantity
            print(f"DEBUG CART: ✅ Producto {product_id} eliminado completamente ({removed_quantity} unidades). Total carrito: {self.cart_total}")
        else:
            print(f"DEBUG CART: ❌ Producto {product_id} no está en el carrito")

class StoreState(rx.State):
    """
    Estado de la tienda que maneja productos y país del usuario.
    Sigue principios POO para encapsular la lógica de estado.
    """
    
    # Lista de productos suplementos
    _products: List[Dict] = []
    _products_loaded: bool = False

    # Lista de productos de cuidado de la piel
    _skincare_products: List[Dict] = []
    _skincare_products_loaded: bool = False

    # Productos más nuevos
    _latest_products: List[Dict] = []
    _latest_products_loaded: bool = False

    # Productos más populares
    _popular_products: List[Dict] = []
    _popular_products_loaded: bool = False

    # Productos por tipo
    _kit_inicio_products: List[Dict] = []
    _kit_inicio_products_loaded: bool = False
    
    _supplement_products: List[Dict] = []
    _supplement_products_loaded: bool = False
    
    _skincare_products_new: List[Dict] = []
    _skincare_products_new_loaded: bool = False
    
    _sanitize_products: List[Dict] = []
    _sanitize_products_loaded: bool = False

    # País del usuario para mostrar precios correctos
    user_country: Countries = Countries.MEXICO
    
    # Estados de carga
    is_loading: bool = False
    error_message: str = ""

    @rx.var
    def products(self) -> List[Dict]:
        """
        Propiedad computada que carga productos automáticamente.
        Se ejecuta la primera vez que se accede a los productos.
        """
        if not self._products_loaded:
            try:
                self._products = ProductDataService.get_products_for_store(self.user_country)
                self._products_loaded = True
            except Exception as e:
                print(f"❌ Error cargando productos: {e}")
                self._products = []
        return self._products



    def on_load(self):
        """
        Evento que se ejecuta al cargar la página.
        Carga los productos automáticamente.
        """
        self.load_products()

    def load_products(self):
        """
        Carga productos desde la base de datos.
        Principio KISS: carga simple sin filtros complejos.
        """
        self.is_loading = True
        self.error_message = ""
        
        try:
            # Por ahora usar México como país por defecto
            # TODO: Integrar con autenticación para obtener país del usuario
            self.user_country = Countries.MEXICO
            
            # Cargar productos con precios según país
            self._products = ProductDataService.get_products_for_store(self.user_country)
            self._products_loaded = True
            
        except Exception as e:
            self.error_message = f"Error cargando productos: {str(e)}"
            print(f"❌ {self.error_message}")
            
        finally:
            self.is_loading = False

    def get_supplements(self) -> List[Dict]:
        """
        Obtiene solo productos de tipo suplemento.
        Principio DRY: reutiliza productos cargados.
        """
        return [p for p in self._products if p["type"] == "suplemento"]
    
    def get_skincare_products(self) -> List[Dict]:
        """
        Obtiene solo productos de cuidado de la piel.
        """
        return [p for p in self._products if p["type"] == "skincare"]
    
    def get_latest_products(self, limit: int = 6) -> List[Dict]:
        """
        Obtiene los últimos productos (primeros N productos).
        Principio YAGNI: implementación simple sin fecha de creación.
        """
        return self._products[:limit]
    
    @rx.var
    def latest_products(self) -> List[Dict]:
        """Productos más nuevos (is_new = True)"""
        if not self._latest_products_loaded:
            try:
                self._latest_products = ProductManager.get_latest_products_formatted(self.user_country)
                self._latest_products_loaded = True
            except Exception as e:
                print(f"❌ Error cargando productos nuevos: {e}")
                self._latest_products = []
        return self._latest_products

    @rx.var  
    def popular_products(self) -> List[Dict]:
        """Top 5 productos más vendidos"""
        if not self._popular_products_loaded:
            try:
                self._popular_products = ProductManager.get_popular_products_formatted(self.user_country, limit=5)
                self._popular_products_loaded = True
            except Exception as e:
                print(f"❌ Error cargando productos populares: {e}")
                self._popular_products = []
        return self._popular_products

    @rx.var
    def kit_inicio_products(self) -> List[Dict]:
        """Productos del tipo 'kit de inicio'"""
        if not self._kit_inicio_products_loaded:
            try:
                self._kit_inicio_products = ProductManager.get_kit_inicio_products_formatted(self.user_country)
                self._kit_inicio_products_loaded = True
            except Exception as e:
                print(f"❌ Error cargando kits de inicio: {e}")
                self._kit_inicio_products = []
        return self._kit_inicio_products

    @rx.var
    def supplement_products(self) -> List[Dict]:
        """Productos del tipo 'suplemento'"""
        if not self._supplement_products_loaded:
            try:
                self._supplement_products = ProductManager.get_supplement_products_formatted(self.user_country)
                self._supplement_products_loaded = True
            except Exception as e:
                print(f"❌ Error cargando suplementos: {e}")
                self._supplement_products = []
        return self._supplement_products

    @rx.var
    def skincare_products(self) -> List[Dict]:
        """Productos del tipo 'skincare'"""
        if not self._skincare_products_loaded:
            try:
                self._skincare_products = ProductManager.get_skincare_products_formatted(self.user_country)
                self._skincare_products_loaded = True
            except Exception as e:
                print(f"❌ Error cargando productos skincare: {e}")
                self._skincare_products = []
        return self._skincare_products

    @rx.var
    def sanitize_products(self) -> List[Dict]:
        """Productos del tipo 'desinfectante'"""
        if not self._sanitize_products_loaded:
            try:
                self._sanitize_products = ProductManager.get_sanitize_products_formatted(self.user_country)
                self._sanitize_products_loaded = True
            except Exception as e:
                print(f"❌ Error cargando productos desinfectantes: {e}")
                self._sanitize_products = []
        return self._sanitize_products