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
├── product_service/        # Gestión de productos y tienda (catálogo, carrito)
├── order_service/          # Manejo de órdenes y envíos
├── payment_service/        # Servicios de pago (Stripe, procesamiento)
├── finance_service/        # Gestión financiera y billetera virtual
├── pages/                  # Páginas de la aplicación
├── shared_ui/              # Componentes UI reutilizables
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

#### Sistema de Reportes de Red
- Visualización de usuarios registrados por día
- Conteo de registros mensuales con filtros POO
- Información de patrocinadores en tablas
- Formateo de fechas DD/MM/YYYY
- Cálculo de niveles jerárquicos en la red MLM

### 🔄 En Desarrollo

#### MLM User Manager
- Clase `MLMUserManager` para lógica de negocio MLM separada de autenticación
- Métodos para obtener descendientes de red
- Sistema de filtrado de registros por rangos de fechas
- Cálculo de niveles de usuario usando BFS desde usuario autenticado como raíz

## Features Planeados por Implementar

### 🛍️ Servicio de Productos
1. **Visualización de Tienda**
   - Catálogo de productos con imágenes y descripciones
   - Filtros y categorías de productos
   - Páginas de detalle de producto

2. **Carrito de Compras**
   - Agregar/remover productos del carrito
   - Modificar cantidades
   - Persistencia del carrito por sesión

3. **Proceso de Compra**
   - Finalización de órdenes
   - Confirmación de compras
   - Historial de transacciones

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
- **Tienda**: E-commerce de productos
- **Herramientas**: Recursos para usuarios
- **Soporte**: Centro de ayuda

## Base de Datos

### Tablas Principales
- `users`: Información básica de usuarios
- `user_profiles`: Perfiles extendidos
- `user_tree_paths`: Estructura jerárquica MLM
- `addresses`: Direcciones de usuarios
- `auth_credentials`: Credenciales de autenticación
- `roles` y `roles_users`: Sistema de permisos

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

# Ejecutar servidor de desarrollo
reflex run

# Ejecutar migraciones
alembic upgrade head
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
1. Validar sistema de cálculo de niveles MLM
2. Implementar catálogo de productos
3. Desarrollar carrito de compras
4. Integrar sistema de pagos con Stripe
5. Crear billetera virtual
6. Desarrollar panel administrativo

---
*Última actualización: Septiembre 2025*