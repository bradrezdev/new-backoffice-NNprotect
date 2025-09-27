# NNProtect Backoffice - Sistema MLM

## Descripción General
NNProtect Backoffice es un panel de control de negocio multinivel desarrollado con **Reflex** (frontend) y **Supabase** (base de datos). La aplicación permite a los usuarios gestionar su negocio personal MLM, incluyendo autenticación, registro de referidos, compra de productos, manejo de comisiones y gestión de billetera virtual.

## Objetivo del Proyecto
Crear una plataforma completa donde los usuarios puedan:
- Iniciar/cerrar sesión de forma segura
- Registrar nuevos usuarios referidos 
- Comprar productos desde la tienda integrada
- Recibir comisiones por ventas directas e indirectas
- Gestionar una billetera virtual con transacciones
- Retirar comisiones a cuentas bancarias
- Visualizar reportes de negocio y estadísticas

## Stack Tecnológico
- **Frontend**: Reflex (Python-based web framework)
- **Backend**: Python
- **Base de Datos**: Supabase
- **Autenticación**: Supabase Auth
- **Pagos**: Stripe (planeado)

## Arquitectura del Proyecto

### Estructura de Carpetas
```
NNProtect_new_website/
├── auth/                    # Sistema de autenticación (login, registro)
├── auth_service/           # Servicios de autenticación con Supabase
├── mlm_service/            # Lógica de negocio MLM (red, reportes, comisiones)
├── product_service/        # ✅ Gestión de productos y tienda (COMPLETO)
│   ├── store.py           # Catálogo principal con productos reales
│   ├── shopping_cart.py   # Carrito funcional con cálculos automáticos
│   ├── store_state.py     # Estado reactivo global
│   ├── product_manager.py # Gestión de productos con precios por país
│   └── product_data/      # Servicios POO (ProductService, CartService)
├── order_service/          # Manejo de órdenes y envíos
├── payment_service/        # Servicios de pago (Stripe, procesamiento)
├── finance_service/        # Gestión financiera y billetera virtual
├── pages/                  # Páginas de la aplicación
├── shared_ui/              # Componentes UI reutilizables (header con carrito)
└── utils/                  # Utilidades y helpers
```

## Estado Actual de Desarrollo

### ✅ Funcionalidades Implementadas

#### Sistema de Autenticación
- Inicio de sesión con email y contraseña
- Integración completa con Supabase Auth
- Gestión de estados de usuario autenticado
- Validación de credenciales y manejo de errores

#### Gestión de Usuarios MLM
- Registro de nuevos usuarios referidos
- Sistema de patrocinio/sponsor tracking
- Estructura jerárquica de red MLM usando tabla `UserTreePath`
- Cálculo de niveles de red usando algoritmo BFS
- Reportes de registros diarios y mensuales
- Campo `country_cache` en usuarios para optimización de precios por país

#### Sistema de Reportes de Red
- Visualización de usuarios registrados por día
- Conteo de registros mensuales con filtros POO
- Información de patrocinadores en tablas
- Formateo de fechas DD/MM/YYYY
- Cálculo de niveles jerárquicos en la red MLM

#### 🛒 Sistema de Carrito de Compras (COMPLETADO)
- **Base de Datos**: 24 productos reales con precios específicos por país (MX, USA, COLOMBIA)
- **Catálogo de Productos**: Visualización completa con imágenes, descripciones y precios dinámicos
- **Carrito Funcional**: Sistema completo de añadir/remover productos con cantidades
- **Precios por País**: Sistema automático de precios según ubicación del usuario
- **Puntos de Volumen (PV)**: Cálculo automático de puntos por país
- **Estado Reactivo**: Manejo con `StoreState` para actualizaciones en tiempo real
- **Interfaz Responsive**: Diseño móvil-primero completamente funcional
- **Botones +/-**: Incremento/decremento de cantidades en tarjetas de productos
- **Icono de Carrito**: Header con contador de productos y badge dinámico
- **Cálculos Automáticos**: Totales de precio y puntos PV en tiempo real

#### Servicios POO Implementados
- **ProductService**: Manejo de productos con métodos `get_product_price()`, `get_product_pv()`, `get_product_vn()`
- **CartService**: Lógica del carrito de compras
- **MLMUserManager**: Separación de lógica MLM de autenticación
- **StoreState**: Estado reactivo global para productos y carrito

### 🔄 En Desarrollo

#### Sistema de Órdenes y Pagos
- Integración con servicios de pago (Stripe)
- Proceso completo de checkout
- Historial de órdenes personales y de red
- Sistema de envíos y métodos de entrega

#### Sistema Financiero Avanzado
- Billetera virtual con transacciones
- Retiros a cuentas bancarias
- Cálculo automático de comisiones MLM

## Features Planeados por Implementar

### 🛍️ Servicio de Productos - AVANZADO
1. **Funcionalidades Adicionales**
   - Filtros y categorías de productos
   - Páginas de detalle de producto individuales
   - Sistema de favoritos/lista de deseos
   - Reviews y calificaciones de productos

2. **Inventario y Stock**
   - Control de inventario en tiempo real
   - Notificaciones de productos agotados
   - Gestión de stock por CEDIS

3. **Proceso de Compra Completo**
   - Finalización de órdenes con checkout
   - Confirmación de compras
   - Integración con sistema de pagos

### 💳 Servicio de Pagos
1. **Métodos de Pago**
   - Gestión de tarjetas de crédito/débito
   - Almacenamiento seguro de métodos de pago

2. **Integración Stripe**
   - Procesamiento de pagos con tarjetas
   - Webhooks para confirmación de pagos
   - Manejo de pagos fallidos

3. **Billetera Virtual**
   - Sistema de créditos internos
   - Suma automática por ganancias/comisiones
   - Resta por compras realizadas
   - Historial de movimientos de billetera

### 📦 Servicio de Órdenes
1. **Órdenes Personales**
   - Lista de órdenes del usuario autenticado
   - Estados: pendiente, procesando, completado, cancelado
   - Detalles de cada orden con productos

2. **Órdenes de Red**
   - Visualización de órdenes de usuarios en niveles inferiores
   - Filtros por usuario, fecha, estado
   - Cálculo de volumen generado por la red

### 🌐 Servicio MLM Avanzado
1. **Visualización de Red**
   - Árbol genealógico de la organización
   - Indicadores visuales de niveles
   - Información de cada nodo (usuario)

2. **Sistema de Puntos de Volumen**
   - Asignación automática por compras
   - Acumulación de puntos personales y grupales
   - Historial de puntos por período

3. **Sistema de Rangos**
   - Cálculo automático basado en volumen personal y grupal
   - Progresión de rangos con requisitos
   - Beneficios por rango alcanzado

4. **Plan de Compensación**
   - Cálculo de comisiones por ventas directas
   - Bonos por volumen grupal
   - Bonos de igualación y liderazgo
   - Distribución automática a billetera

### 👨‍💼 Panel Administrativo
1. **Autenticación por Roles**
   - Admin: acceso completo al sistema
   - Moderator: gestión de usuarios y productos
   - Support: atención al cliente y consultas

2. **Gestión de Tienda**
   - CRUD de productos
   - Gestión de inventario
   - Configuración de precios y promociones

3. **Gestión de Usuarios**
   - Activar/bloquear usuarios
   - Editar información de perfiles
   - Manejo manual de billeteras virtuales
   - Resolución de disputas

## Páginas de la Aplicación

### Públicas
- **Login**: Autenticación de usuarios

### Privadas (Requieren Autenticación)
- **Dashboard**: Resumen ejecutivo del negocio
- **Registrar Socio**: Formulario de registro de referidos
- **Negocio**: 
  - Árbol de socios
  - Detalles de negocio
  - Detalles de comisiones
  - Historial de compras
- **NN Travels**: Sistema de puntos por logros
- **Tienda**: ✅ E-commerce funcional con 24 productos reales, carrito y precios por país
- **Herramientas**: Recursos para usuarios
- **Soporte**: Centro de ayuda

## Base de Datos

### Tablas Principales
- `users`: Información básica de usuarios + campo `country_cache` para optimización
- `user_profiles`: Perfiles extendidos
- `user_tree_paths`: Estructura jerárquica MLM
- `addresses`: Direcciones de usuarios
- `auth_credentials`: Credenciales de autenticación
- `roles` y `roles_users`: Sistema de permisos
- **`products`**: ✅ 24 productos reales con precios por país (MX/USA/COLOMBIA)
  - Campos: `name`, `description`, `image_url`, `category`
  - Precios: `price_mx`, `price_usa`, `price_colombia`
  - Puntos: `pv_mx`, `pv_usa`, `pv_colombia` 
  - VN: `vn_mx`, `vn_usa`, `vn_colombia`

## Instalación y Configuración

### Requisitos
- Python 3.11+
- Reflex framework
- Supabase account
- Variables de entorno configuradas

### Comandos Básicos
```bash
# Instalar dependencias
pip install -r requirements.txt

# Activar entorno virtual y ejecutar servidor
source nnprotect_backoffice/bin/activate && reflex run

# Ejecutar migraciones
alembic upgrade head

# Testing del sistema de carrito
python test_final_store.py
```

### Variables de Entorno Requeridas
```bash
# Supabase Configuration
DATABASE_URL=postgresql://[usuario]:[password]@[host]/[database]
JWT_SECRET_KEY=[tu_jwt_secret_key]

# Configuración detectada automáticamente
ENVIRONMENT=DESARROLLO  # ✅ Configurado
```

## Convenciones de Desarrollo

### Principios Aplicados
- **KISS**: Mantener soluciones simples y claras
- **DRY**: Evitar duplicación de código
- **YAGNI**: No implementar funcionalidades innecesarias
- **POO**: Diseño orientado a objetos para reutilización

### Estándares de Código
- Documentación en español latinoamericano
- Comentarios explicativos en clases y métodos
- Componentes reutilizables en `shared_ui/`
- Separación clara entre lógica de negocio y presentación

## Próximos Pasos de Desarrollo
1. ✅ ~~Implementar catálogo de productos~~ **COMPLETADO**
2. ✅ ~~Desarrollar carrito de compras~~ **COMPLETADO**
3. Integrar proceso completo de checkout
4. Conectar sistema de pagos con Stripe
5. Crear billetera virtual con transacciones
6. Desarrollar panel administrativo
7. Implementar sistema de órdenes completo
8. Añadir cálculo automático de comisiones MLM

## 🎯 Logros Recientes (Diciembre 2024)

### Sistema de E-commerce Funcional
- **24 productos reales** cargados en base de datos
- **Precios dinámicos** por país (México, USA, Colombia)
- **Carrito completamente funcional** con estado reactivo
- **Interfaz responsive** móvil-primero
- **Arquitectura POO limpia** con servicios separados
- **Testing automatizado** con validaciones completas

### Métricas de Implementación
- **77 archivos** compilando correctamente
- **Arquitectura modular** con separación de responsabilidades
- **Estado reactivo** para actualizaciones en tiempo real
- **Base de datos optimizada** con campos de país para performance

---
*Última actualización: Septiembre 2025*