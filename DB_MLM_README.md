```markdown
# Sistema de Base de Datos para MLM Uninivel - NN Protect

## 📋 Contexto del Proyecto

### Empresa y Modelo de Negocio
- **Tipo**: Marketing Multinivel con esquema Uninivel
- **Países**: México, USA, Colombia, República Dominicana
- **Productos**: Suplementos y cuidado de la piel con nanotecnología
- **Crecimiento**: De 244 socios (Oct 2024) a 5,702 socios (Sep 2025)
- **Proyección**: 50,000 usuarios en 2 años

### Esquema Uninivel - Características Clave
- **Ancho ilimitado**: Cada distribuidor puede reclutar infinitos miembros directos en nivel 1
- **Profundidad finita**: Comisiones se pagan hasta cierto nivel (varía por rango)
- **Sin spillover**: Cada distribuidor se beneficia solo de sus propios esfuerzos de reclutamiento
- **Niveles de comisión**: Típicamente 5-10 niveles según el rango alcanzado

---

## 🎯 Conceptos Fundamentales Identificados

### Sistema de Doble Puntuación

#### 1. PV (Puntos de Volumen)
- **Propósito**: Solo para alcanzar rangos
- **Característica**: Valor uniforme global (ej: Cúrcuma = 293 PV en todos los países)
- **No se usan para**: Cálculo de comisiones

#### 2. VN (Valor Negocio)
- **Propósito**: Solo para pagar comisiones
- **Característica**: Valor localizado por país (ej: Cúrcuma = 293 VN en MX, 21 VN en USA, 67,400 VN en COP)
- **Razón**: Permite ajustar comisiones a la economía local de cada país

### Conversión de Monedas
**Decisión tomada**: Tasa de cambio FIJA establecida por la compañía
- **Razón**: Evitar volatilidad y problemas contables
- **Implementación**: Tabla de tasas configurables manualmente

**Flujo de conversión**:
1. Distribuidor mexicano refiere a colombiano
2. Colombiano compra producto (genera VN en COP)
3. Sistema calcula comisión para mexicano en COP
4. Sistema convierte a MXN usando tasa fija de la empresa
5. Mexicano recibe comisión en MXN

---

## ⏱️ Modelo Temporal de Comisiones

### Dos Sistemas de Cálculo Diferentes

#### Bono Rápido (Instantáneo)
- **Cuándo**: Inmediatamente al confirmar pago del kit de inicio
- **Frecuencia**: Por transacción
- **Implementación**: Cálculo en tiempo real
- **Se paga**: Instantáneamente

#### Bonos Mensuales (Batch Processing)
Incluye: Uninivel, Matching, Liderazgo, etc.
- **Cuándo**: Último día del mes a las 23:59:59
- **Frecuencia**: Una vez al mes
- **Implementación**: Job programado con snapshots
- **Se paga**: Primeros días del mes siguiente

### Timestamp Crítico
**Decisión tomada**: `payment_confirmed_at` es la fecha que determina el período

**Ejemplo**:
```
Orden creada: 31 Dic 23:59:59
Pago confirmado: 1 Ene 00:01:00
→ Comisiones calculadas para período de Enero
```

**Razón**: Solo transacciones exitosas generan comisiones, evita problemas con pagos rechazados.

---

## 🏗️ Arquitectura de Solución: Enfoque Híbrido

### Decisión Final
**Híbrido**: Tiempo real + Snapshots mensuales

#### Para Bono Rápido
- Cálculo en tiempo real al confirmar pago
- Inserción directa en tabla `commissions`
- Velocidad esperada: <100ms por transacción
- Usuarios ven comisión inmediatamente

#### Para Bonos Mensuales
- Job programado (cron) ejecuta el día 31 a las 23:59:59
- Genera snapshots en tabla `monthly_commission_snapshots`
- Tiempo de procesamiento estimado: 2-5 minutos para 50k usuarios
- Permite recálculo si hay correcciones

### Ventajas del Enfoque Híbrido
1. Mejor UX para distribuidores (ven Bono Rápido inmediato)
2. Eficiencia en cálculos complejos (uninivel calculado una vez al mes)
3. Auditorías simples (comparar datos raw vs snapshots)
4. Escalable hasta 50k usuarios sin problemas de performance

---

## ❌ Problemas Críticos Identificados en Código Existente

### 1. `UserTreePath` Implementada Incorrectamente

**Problema actual**:
```python
class UserTreePath(rx.Model, table=True):
    sponsor_id: int = Field(primary_key=True)
    user_id: int = Field(primary_key=True)
```

**Por qué falla**:
- Solo almacena relaciones directas (padre → hijo inmediato)
- Para saber ancestros distantes requiere queries recursivos
- Con 50k usuarios, esto colapsa en performance

**Ejemplo del fallo**:
```
A refiere a B
B refiere a C
C refiere a D

Tabla actual: (A,B), (B,C), (C,D)
Para saber que A es ancestro de D: necesitas JOIN recursivo
```

**Solución correcta (Path Enumeration)**:
```python
class UserTreePath(rx.Model, table=True):
    ancestor_id: int = Field(primary_key=True, foreign_key="users.member_id")
    descendant_id: int = Field(primary_key=True, foreign_key="users.member_id")
    depth: int = Field(primary_key=True)
```

**Por qué funciona**:
Almacena TODAS las relaciones ancestro-descendiente pre-calculadas:
```
(A, A, 0)  # Self-reference
(B, B, 0)
(C, C, 0)
(D, D, 0)
(A, B, 1)  # A es padre directo de B
(B, C, 1)
(C, D, 1)
(A, C, 2)  # A es abuelo de C
(B, D, 2)
(A, D, 3)  # A es bisabuelo de D
```

**Query para Bono Uninivel ahora es simple**:
```sql
SELECT * FROM user_tree_path 
WHERE ancestor_id = 123 
  AND depth <= 10
  AND depth > 0;
```

### 2. Falta Tabla `Transactions` (CRÍTICA)

Sin esta tabla, **no puedes calcular comisiones**.

**Necesaria para**:
- Registrar cada compra de producto/kit
- Almacenar PV y VN congelados al momento de compra
- Vincular transacciones a períodos
- Base para cálculo de todos los bonos

### 3. Timestamps con Offset Hardcodeado

**Problema**:
```python
sa_column_kwargs={"server_default": func.now() - func.interval('6 hours')}
```

**Por qué es peligroso**:
- Rompe cuando México cambia horario de verano
- Inconsistencias en datos históricos

**Solución correcta**:
- Almacenar TODO en UTC en la base de datos
- Convertir a timezone local SOLO en la UI
- Usar librerías como `pytz` o `zoneinfo` para conversiones

### 4. `products.purchase_count` Causará Desincronización

**Problema**:
Campo redundante que se desincronizará con datos reales.

**Solución**:
Calcular en tiempo real desde `transactions`:
```python
def get_purchase_count(product_id):
    return db.query(Transactions).filter(
        Transactions.product_id == product_id,
        Transactions.payment_confirmed_at.isnot(None)
    ).count()
```

### 5. `users.sponsor_id` Sin Foreign Key

**Comentario actual**: "sin FK para evitar problemas circulares"

**Corrección**: Esto es un mito. Los FKs auto-referenciales funcionan perfectamente:
```python
sponsor_id: int | None = Field(default=None, foreign_key="users.member_id")
```

---

## 📊 Estructura de Tablas Propuesta

### Tabla 1: `UserTreePath` (CORREGIDA)

```python
from sqlmodel import Field

class UserTreePath(rx.Model, table=True):
    """
    Patrón Path Enumeration para genealogía MLM.
    Almacena todas las relaciones ancestro-descendiente pre-calculadas.
    """
    # Llave primaria compuesta (los 3 campos juntos forman UNA PK)
    ancestor_id: int = Field(
        primary_key=True, 
        foreign_key="users.member_id",
        index=True
    )
    descendant_id: int = Field(
        primary_key=True, 
        foreign_key="users.member_id",
        index=True
    )
    depth: int = Field(primary_key=True)
    
    # Índices adicionales para queries comunes
    __table_args__ = (
        Index('idx_ancestor_depth', 'ancestor_id', 'depth'),
        Index('idx_descendant_depth', 'descendant_id', 'depth'),
    )
```

**Concepto de PK Compuesta**:
- NO son 3 PKs individuales
- Es UNA sola PK formada por la combinación de 3 campos
- `(ancestor_id=1, descendant_id=2, depth=1)` es único
- Permite almacenar múltiples relaciones del mismo ancestro

### Tabla 2: `Transactions` (NUEVA - CRÍTICA)

```python
from sqlmodel import Field
from datetime import datetime
from enum import Enum

class TransactionStatus(Enum):
    """Estados de una transacción"""
    PENDING = "pending"           # Orden creada, esperando pago
    CONFIRMED = "confirmed"       # Pago confirmado exitosamente
    FAILED = "failed"            # Pago rechazado
    CANCELLED = "cancelled"      # Orden cancelada

class Transactions(rx.Model, table=True):
    """
    Registro de todas las compras de productos y kits.
    Valores de PV/VN se congelan al momento de la transacción.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    # Comprador
    member_id: int = Field(foreign_key="users.member_id", index=True)
    
    # Producto comprado
    product_id: int = Field(foreign_key="products.id", index=True)
    quantity: int = Field(default=1)
    
    # País donde se realizó la compra
    country: str = Field(max_length=50, index=True)
    
    # Valores CONGELADOS al momento de la transacción
    # (No se recalculan si cambian los precios del producto)
    pv_earned: int = Field(default=0)        # Puntos de volumen ganados
    vn_earned: float = Field(default=0.0)    # Valor negocio ganado
    price_paid: float = Field(default=0.0)   # Precio pagado en moneda local
    currency: str = Field(max_length=10)     # MXN, USD, COP, etc.
    
    # Estado de la transacción
    status: str = Field(default=TransactionStatus.PENDING.value, index=True)
    
    # Timestamps críticos
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()}
    )
    payment_confirmed_at: datetime | None = Field(default=None, index=True)
    
    # Período al que pertenece (basado en payment_confirmed_at)
    period_id: int | None = Field(default=None, foreign_key="periods.id", index=True)
    
    # Metadatos adicionales
    payment_method: str | None = Field(default=None, max_length=50)
    transaction_reference: str | None = Field(default=None, unique=True)
    notes: str | None = Field(default=None, max_length=500)
```

**Campos clave explicados**:

- **`pv_earned` / `vn_earned` / `price_paid`**: Se congelan al momento de la compra
  - Razón: Si cambias precios en `products`, transacciones históricas no cambian
  - Ejemplo: Producto costaba $100, luego sube a $120, transacción antigua sigue siendo $100

- **`payment_confirmed_at`**: Determina a qué período pertenece la transacción
  - NULL = pago aún no confirmado (no genera comisiones)
  - NOT NULL = pago exitoso (genera comisiones)

- **`period_id`**: Se asigna automáticamente basándose en `payment_confirmed_at`
  - Permite queries rápidas: "todas las transacciones del período X"

### Tabla 3: `Commissions` (NUEVA - CRÍTICA)

```python
from sqlmodel import Field
from datetime import datetime
from enum import Enum

class BonusType(Enum):
    """Tipos de bonos del plan de compensación"""
    BONO_RAPIDO = "bono_rapido"           # Por inscripción (instantáneo)
    BONO_UNINIVEL = "bono_uninivel"       # Por niveles (mensual)
    BONO_MATCHING = "bono_matching"       # Matching bonus (mensual)
    BONO_ALCANCE = "bono_alcance"         # Por alcanzar rango (única vez)
    BONO_AUTOMOVIL = "bono_automovil"     # Embajador Transformador+
    BONO_TRAVELS = "bono_travels"         # NN Travels
    BONO_CASHBACK = "bono_cashback"       # Descuento en compra
    BONO_LEALTAD = "bono_lealtad"         # Compras 1-7 del mes

class CommissionStatus(Enum):
    """Estados de una comisión"""
    PENDING = "pending"       # Calculada pero no pagada
    PAID = "paid"            # Ya pagada al distribuidor
    CANCELLED = "cancelled"  # Cancelada (ej: devolución)

class Commissions(rx.Model, table=True):
    """
    Registro de todas las comisiones generadas.
    Almacena montos en moneda origen y moneda destino con tasa de conversión.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    # Receptor de la comisión
    member_id: int = Field(foreign_key="users.member_id", index=True)
    
    # Tipo de bono
    bonus_type: str = Field(max_length=50, index=True)
    
    # Origen de la comisión (opcional, según tipo de bono)
    source_member_id: int | None = Field(
        default=None, 
        foreign_key="users.member_id", 
        index=True
    )
    source_transaction_id: int | None = Field(
        default=None, 
        foreign_key="transactions.id", 
        index=True
    )
    
    # Período y profundidad (para bonos uninivel)
    period_id: int = Field(foreign_key="periods.id", index=True)
    level_depth: int | None = Field(default=None)  # 1, 2, 3... (uninivel)
    
    # Montos y conversión de moneda
    amount_vn: float = Field(default=0.0)           # Monto en VN del país origen
    currency_origin: str = Field(max_length=10)     # MXN, USD, COP
    
    amount_converted: float = Field(default=0.0)    # Monto convertido a moneda receptor
    currency_destination: str = Field(max_length=10) # Moneda del receptor
    exchange_rate: float = Field(default=1.0)       # Tasa usada para conversión
    
    # Estado y timestamps
    status: str = Field(
        default=CommissionStatus.PENDING.value, 
        index=True
    )
    calculated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()}
    )
    paid_at: datetime | None = Field(default=None)
    
    # Notas adicionales
    notes: str | None = Field(default=None, max_length=500)
    
    # Índices compuestos para queries comunes
    __table_args__ = (
        Index('idx_member_period', 'member_id', 'period_id'),
        Index('idx_member_status', 'member_id', 'status'),
        Index('idx_period_bonus_type', 'period_id', 'bonus_type'),
    )
```

**Sistema de doble moneda explicado**:

Ejemplo real:
```python
# Distribuidor mexicano (member_id=100)
# Colombiano (member_id=200) compra producto
# Producto en Colombia: VN = 67,400 COP
# Comisión uninivel nivel 1: 5% = 3,370 COP
# Tasa de cambio empresa: 1 COP = 0.00435 MXN
# Convertido: 3,370 * 0.00435 = 14.66 MXN

commission = {
    "member_id": 100,                    # Mexicano que recibe
    "bonus_type": "bono_uninivel",
    "source_member_id": 200,             # Colombiano que compró
    "amount_vn": 3370.0,                 # En COP
    "currency_origin": "COP",
    "amount_converted": 14.66,           # En MXN
    "currency_destination": "MXN",
    "exchange_rate": 0.00435,
    "level_depth": 1
}
```

### Tabla 4: `ExchangeRates` (NUEVA - RECOMENDADA)

```python
from sqlmodel import Field
from datetime import datetime

class ExchangeRates(rx.Model, table=True):
    """
    Tasas de cambio fijas establecidas por la compañía.
    Permite cambiar tasas en el futuro sin afectar comisiones pasadas.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    # Par de monedas
    from_currency: str = Field(max_length=10, index=True)  # COP
    to_currency: str = Field(max_length=10, index=True)    # MXN
    
    # Tasa de cambio
    rate: float = Field(default=1.0)
    
    # Vigencia
    effective_from: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    effective_until: datetime | None = Field(default=None)
    
    # Metadatos
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()}
    )
    notes: str | None = Field(default=None, max_length=255)
    
    __table_args__ = (
        Index('idx_currencies_effective', 'from_currency', 'to_currency', 'effective_from'),
    )
```

**Función helper para obtener tasa vigente**:
```python
def get_exchange_rate(from_currency: str, to_currency: str, date: datetime = None):
    """
    Obtiene la tasa de cambio vigente en una fecha específica.
    Si no se proporciona fecha, usa la fecha actual.
    """
    if from_currency == to_currency:
        return 1.0
    
    date = date or datetime.now(timezone.utc)
    
    rate = db.query(ExchangeRates).filter(
        ExchangeRates.from_currency == from_currency,
        ExchangeRates.to_currency == to_currency,
        ExchangeRates.effective_from <= date,
        or_(
            ExchangeRates.effective_until.is_(None),
            ExchangeRates.effective_until >= date
        )
    ).order_by(ExchangeRates.effective_from.desc()).first()
    
    return rate.rate if rate else None
```

### Tabla 5: `MonthlyCommissionSnapshots` (NUEVA - PARA AUDITORÍA)

```python
from sqlmodel import Field
from datetime import datetime

class MonthlyCommissionSnapshots(rx.Model, table=True):
    """
    Snapshots mensuales de comisiones calculadas.
    Permite auditoría y comparación con datos raw.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    member_id: int = Field(foreign_key="users.member_id", index=True)
    period_id: int = Field(foreign_key="periods.id", index=True)
    
    # Resumen por tipo de bono
    bono_uninivel_total: float = Field(default=0.0)
    bono_matching_total: float = Field(default=0.0)
    bono_liderazgo_total: float = Field(default=0.0)
    
    # Total general
    total_earned: float = Field(default=0.0)
    currency: str = Field(max_length=10)
    
    # Metadatos del cálculo
    calculated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()}
    )
    calculation_version: str = Field(default="1.0")  # Para versionado de lógica
    
    __table_args__ = (
        UniqueConstraint('member_id', 'period_id'),
    )
```

---

## 🔧 Correcciones a Tablas Existentes

### `Users` (Correcciones)

```python
class Users(rx.Model, table=True):
    # ... campos existentes ...
    
    # ✅ CORREGIR: Agregar FK
    sponsor_id: int | None = Field(
        default=None, 
        foreign_key="users.member_id",  # ← Agregar esto
        index=True
    )
    
    # ✅ CORREGIR: Timestamps en UTC puro
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),  # UTC puro
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),  # UTC puro
        sa_column_kwargs={"server_default": func.now()}
    )
```

### `Products` (Correcciones)

```python
class Products(rx.Model, table=True):
    # ... campos existentes ...
    
    # ❌ ELIMINAR este campo (calcular dinámicamente)
    # purchase_count: int = Field(default=0)
    
    # ✅ Agregar método para calcular
    def get_purchase_count(self, db_session):
        """Calcula purchase count desde transactions"""
        return db_session.query(Transactions).filter(
            Transactions.product_id == self.id,
            Transactions.payment_confirmed_at.isnot(None)
        ).count()
```

### `Periods` (Sugerencia de mejora)

```python
class Periods(rx.Model, table=True):
    # ... campos existentes ...
    
    # ✅ AGREGAR: Estado del período
    status: str = Field(default="active", index=True)
    # Valores: "active", "closed", "processing"
    
    # ✅ AGREGAR: Tipo de período
    period_type: str = Field(default="monthly", index=True)
    # Valores: "monthly", "weekly", "quarterly"
```

---

## 🚀 Plan de Implementación

### Fase 1: Correcciones Críticas (Semana 1)
1. ✅ Corregir `UserTreePath` con Path Enumeration
2. ✅ Agregar FK a `users.sponsor_id`
3. ✅ Corregir timestamps a UTC puro
4. ✅ Eliminar `products.purchase_count`
5. ✅ Migración de datos existentes

### Fase 2: Tablas Nuevas Core (Semana 2)
1. ✅ Crear tabla `Transactions`
2. ✅ Crear tabla `ExchangeRates`
3. ✅ Crear tabla `Commissions`
4. ✅ Crear tabla `MonthlyCommissionSnapshots`

### Fase 3: Lógica de Negocio (Semana 3-4)
1. ✅ Implementar cálculo de Bono Rápido (tiempo real)
2. ✅ Implementar cálculo de Bono Uninivel (mensual)
3. ✅ Implementar cálculo de Bono Matching (mensual)
4. ✅ Implementar conversión de monedas

### Fase 4: Jobs y Automatización (Semana 5)
1. ✅ Job para cierre mensual (día 31, 23:59:59)
2. ✅ Job para generación de snapshots
3. ✅ Sistema de notificaciones de comisiones

### Fase 5: Testing y Auditoría (Semana 6)
1. ✅ Tests unitarios para cálculos
2. ✅ Tests de integración
3. ✅ Validación de datos históricos
4. ✅ Dashboard de auditoría

---

## 📝 Queries Comunes Optimizadas

### Query 1: Obtener toda la red de un distribuidor hasta nivel N

```sql
-- Con UserTreePath corregido
SELECT 
    u.member_id,
    u.first_name,
    u.last_name,
    utp.depth
FROM user_tree_path utp
JOIN users u ON u.member_id = utp.descendant_id
WHERE utp.ancestor_id = :member_id
  AND utp.depth > 0        -- Excluir self-reference
  AND utp.depth <= :max_level
ORDER BY utp.depth, u.member_id;
```

### Query 2: Calcular VN total de un nivel específico en un período

```sql
-- Para Bono Uninivel
SELECT 
    SUM(t.vn_earned) as total_vn
FROM transactions t
JOIN user_tree_path utp ON utp.descendant_id = t.member_id
WHERE utp.ancestor_id = :member_id
  AND utp.depth = :level_depth
  AND t.period_id = :period_id
  AND t.payment_confirmed_at IS NOT NULL;
```

### Query 3: Obtener comisiones pendientes de pago de un miembro

```sql
SELECT 
    c.id,
    c.bonus_type,
    c.amount_converted,
    c.currency_destination,
    p.name as period_name,
    c.calculated_at
FROM commissions c
JOIN periods p ON p.id = c.period_id
WHERE c.member_id = :member_id
  AND c.status = 'pending'
ORDER BY c.calculated_at DESC;
```

### Query 4: Reporte mensual de comisiones por tipo

```sql
SELECT 
    c.bonus_type,
    COUNT(*) as commission_count,
    SUM(c.amount_converted) as total_amount,
    c.currency_destination
FROM commissions c
WHERE c.member_id = :member_id
  AND c.period_id = :period_id
GROUP BY c.bonus_type, c.currency_destination;
```

---

## ⚠️ Consideraciones de Escalabilidad

### Para 50k usuarios:

#### Tabla `UserTreePath`
- **Registros estimados**: 50k * 10 niveles promedio = 500k registros
- **Almacenamiento**: ~15 MB
- **Performance**: Queries en <50ms con índices correctos

#### Tabla `Transactions`
- **Registros/mes**: 50k usuarios * 30% activos * 1 compra = 15k transacciones/mes
- **Registros/año**: ~180k transacciones
- **Almacenamiento/año**: ~50 MB
- **Performance**: INSERT <10ms, SELECT <50ms

#### Tabla `Commissions`
- **Registros/mes**: 15k transacciones * 5 niveles promedio = 75k comisiones/mes
- **Registros/año**: ~900k comisiones
- **Almacenamiento/año**: ~100 MB
- **Performance**: Batch INSERT job ~2-5 minutos

### Índices Críticos para Performance

```sql
-- UserTreePath
CREATE INDEX idx_ancestor_depth ON user_tree_path(ancestor_id, depth);
CREATE INDEX idx_descendant_depth ON user_tree_path(descendant_id, depth);

-- Transactions
CREATE INDEX idx_member_period ON transactions(member_id, period_id);
CREATE INDEX idx_payment_confirmed ON transactions(payment_confirmed_at);
CREATE INDEX idx_period_status ON transactions(period_id, status);

-- Commissions
CREATE INDEX idx_member_period ON commissions(member_id, period_id);
CREATE INDEX idx_member_status ON commissions(member_id, status);
CREATE INDEX idx_source_transaction ON commissions(source_transaction_id);
```

---

## 🎓 Conceptos Técnicos Explicados

### Llave Primaria Compuesta

**Pregunta**: ¿Por qué 3 campos son PK en UserTreePath?

**Respuesta**: No son 3 PKs separadas, es UNA PK formada por 3 campos.

```python
# Esto significa:
PK = (ancestor_id, descendant_id, depth)

# Cada combinación única es válida:
(1, 2, 1) ✅ Válido
(1, 2, 2) ✅ Válido (mismo ancestor/descendant, diferente depth)
(1, 2, 1) ❌ Duplicado (violación de PK)
```

**Alternativa con PK simple**:
```python
class UserTreePath(rx.Model, table=True):
    id: int = Field(primary_key=True)
    ancestor_id: int = Field(foreign_key="users.member_id", index=True)
    descendant_id: int = Field(foreign_key="users.member_id", index=True)
    depth: int = Field(index=True)
    
    __table_args__ = (
        UniqueConstraint('ancestor_id', 'descendant_id', 'depth'),
    )
```

### Path Enumeration vs Closure Table

**Path Enumeration** (lo que usamos):
- Ventaja: Queries muy rápidas
- Desventaja: Inserts/updates más complejos
- Ideal para: Estructuras que cambian poco (MLM)

**Closure Table** (alternativa):
- Ventaja: Más flexible para cambios
- Desventaja: Queries más lentas
- Ideal para: Estructuras que cambian mucho

### Timestamps UTC vs Local

**❌ Mal enfoque** (offset hardcodeado):
```python
sa_column_kwargs={"server_default": func.now() - func.interval('6 hours')}
```

**✅ Buen enfoque**:
```python
# Base de datos: siempre UTC
created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc)
)

# Frontend/UI: convertir a timezone local
def display_datetime(dt_utc, user_timezone='America/Mexico_City'):
    return dt_utc.astimezone(pytz.timezone(user_timezone))
```

---

## 🔐 Consideraciones de Seguridad

### Validaciones Críticas

1. **Transacciones**:
   - ✅ Validar que `member_id` existe y está activo
   - ✅ Validar que `product_id` existe y está disponible
   - ✅ Validar que `quantity` > 0
   - ✅ Validar que `price_paid` coincide con precio del producto

2. **Comisiones**:
   - ✅ Validar que `source_transaction_id` tiene payment_confirmed_at
   - ✅ Validar que receptor de comisión está en la red del origen
   - ✅ Validar que `level_depth` no excede máximo por rango

3. **UserTreePath**:
   - ✅ Prevenir ciclos (A → B → A)
   - ✅ Validar que depth es consistente
   - ✅ Mantener integridad referencial

### Auditoría y Trazabilidad

```python
# Todas las tablas críticas deben tener:
created_at: datetime    # Cuándo se creó
updated_at: datetime    # Última modificación
created_by: int         # Quién lo creó (user_id)
notes: str              # Notas adicionales
```

---

## 📊 Métricas y Monitoring

### KPIs del Sistema

1. **Performance**:
   - Tiempo de cálculo Bono Rápido: target <100ms
   - Tiempo de job mensual: target <5 minutos
   - Tiempo de query genealogía: target <50ms

2. **Integridad de Datos**:
   - Comisiones calculadas vs comisiones pagadas
   - Total VN en transacciones vs total VN en comisiones
   - Usuarios activos vs usuarios con transacciones

3. **Negocio**:
   - Tasa de conversión (inscritos → compradores)
   - Valor promedio de transacción por país
   - Distribución de comisiones por tipo de bono

---

## 🚨 Red Flags y Alertas Automáticas

### Implementar alertas para:

1. **Comisión anormalmente alta**:
   - Si comisión > 10x promedio del miembro
   - Revisar transacción origen

2. **Período sin cierre**:
   - Si pasa día 2 del mes y período anterior aún "active"
   - Job de cierre falló

3. **Desbalance VN**:
   - Si `SUM(transactions.vn_earned)` ≠ `SUM(commissions.amount_vn)`
   - Hay comisiones no calculadas o sobre-calculadas

4. **Usuario sin sponsor**:
   - Si `sponsor_id IS NULL` y `member_id != 1` (fundador)
   - Datos de registro incompletos

---

## 📚 Recursos y Referencias

### Documentación de Patterns

- **Closure Table Pattern**: https://www.slideshare.net/billkarwin/models-for-hierarchical-data
- **Path Enumeration**: Joe Celko's "Trees and Hierarchies in SQL"
- **MLM Database Design**: Various whitepapers on network marketing systems

### Stack Tecnológico

- **Backend**: Python + SQLModel + Reflex
- **Database**: PostgreSQL (recomendado) o Supabase
- **ORM**: SQLModel
- **Timezone**: pytz o zoneinfo
- **Jobs**: APScheduler o Celery

---

## ✅ Checklist de Implementación

### Base de Datos
- [ ] Corregir `UserTreePath` con Path Enumeration
- [ ] Crear tabla `Transactions`
- [ ] Crear tabla `Commissions`
- [ ] Crear tabla `ExchangeRates`
- [ ] Crear tabla `MonthlyCommissionSnapshots`
- [ ] Agregar FK a `users.sponsor_id`
- [ ] Corregir timestamps a UTC
- [ ] Eliminar `products.purchase_count`
- [ ] Crear todos los índices recomendados
- [ ] Migrar datos existentes

### Lógica de Negocio
- [ ] Implementar cálculo Bono Rápido
- [ ] Implementar cálculo Bono Uninivel
- [ ] Implementar cálculo Bono Matching
- [ ] Implementar cálculo Bono Alcance
- [ ] Implementar conversión de monedas
- [ ] Implementar asignación de períodos

### Jobs y Automatización
- [ ] Job de cierre mensual (día 31, 23:59:59)
- [ ] Job de generación de snapshots
- [ ] Job de notificaciones
- [ ] Job de validación de integridad

### Testing
- [ ] Tests unitarios para cada tipo de comisión
- [ ] Tests de conversión de monedas
- [ ] Tests de genealogía
- [ ] Tests de integración end-to-end
- [ ] Tests de performance con datos dummy

### Monitoring
- [ ] Dashboard de comisiones pendientes
- [ ] Dashboard de auditoría
- [ ] Alertas automáticas
- [ ] Logs detallados

---

## 🤔 Preguntas Pendientes para el Cliente

1. **Tasas de Cambio**:
   - ¿Con qué frecuencia cambiarán las tasas fijas?
   - ¿Quién tiene autorización para cambiarlas?

2. **Comisiones Negativas**:
   - ¿Qué pasa si hay devolución de producto?
   - ¿Se restan comisiones ya pagadas?

3. **Periodo de Gracia**:
   - ¿Hay período de prueba donde no se pagan comisiones?
   - ¿Cuánto tiempo después de inscripción empiezan a ganar?

4. **Límites y Caps**:
   - ¿Hay límite máximo de comisión por período?
   - ¿Hay límite máximo por tipo de bono?

5. **Reglas de Activación**:
   - ¿Cuándo un usuario cambia de NO_QUALIFIED a QUALIFIED?
   - ¿Necesita compra mínima mensual para recibir comisiones?

---

## 💡 Próximos Pasos Inmediatos

1. **Revisar y aprobar** este diseño de base de datos
2. **Crear scripts de migración** para tablas existentes
3. **Implementar tablas nuevas** en ambiente de desarrollo
4. **Crear datos de prueba** (usuarios, transacciones, comisiones)
5. **Validar cálculos** con casos de prueba del plan de compensación
6. **Documentar flujos** de cada tipo de bono
7. **Implementar lógica** de cálculo paso a paso

---

**Última actualización**: Septiembre 2025  
**Versión**: 1.0  
**Estado**: Propuesta para revisión
```