```markdown
# Plan de Compensación NN Protect - Documentación Completa

## 📋 Índice
1. [Visión General](#visión-general)
2. [Sistema de Rangos](#sistema-de-rangos)
3. [Tipos de Bonos](#tipos-de-bonos)
4. [Reglas Críticas del Negocio](#reglas-críticas-del-negocio)
5. [Fórmulas de Cálculo](#fórmulas-de-cálculo)
6. [Casos Especiales](#casos-especiales)
7. [Ejemplos de Implementación](#ejemplos-de-implementación)

---

## 🎯 Visión General

### Modelo de Negocio
- **Tipo**: Marketing Multinivel (MLM) con esquema Uninivel
- **Países operativos**: México, USA, Colombia, República Dominicana
- **Total de bonos**: 9 tipos diferentes
- **Frecuencia de pago**: Variable (instantánea, semanal, mensual, única vez)

### Conceptos Fundamentales

#### Niveles de Red (Profundidad)
```
TÚ (Nivel 0)
├── Nivel 1: Personas que TÚ refieres directamente (tus directos)
│   └── Nivel 2: Personas que tu Nivel 1 refirió directamente (sus directos)
│       └── Nivel 3: Personas que tu Nivel 2 refirió directamente (sus directos)
│           └── ... hasta el infinito
```

**Importante**: Los niveles se cuentan desde la perspectiva de cada distribuidor. Lo que para ti es "Nivel 2", para tu directo de Nivel 1 es su "Nivel 1".

#### Sistema de Puntos

##### PV (Personal Volume / Volumen Personal)
- **Definición**: Puntos que adquieres cuando TÚ compras productos en tu propia cuenta
- **Uso**: SOLO para alcanzar rangos
- **Característica**: Mismo valor global (ej: producto X = 293 PV en todos los países)
- **NO se usa para**: Calcular comisiones monetarias

##### VG (Volume Group / Volumen Grupal)
- **Definición**: Suma de TODOS los PV de todas las personas en tu organización (toda tu red)
- **Cálculo**: `VG = tu_PV + PV_nivel1 + PV_nivel2 + PV_nivel3 + ... + PV_nivel_infinito`
- **Uso**: Requerido para alcanzar rangos superiores

##### VN (Valor Negocio)
- **Definición**: Valor monetario localizado por país usado para calcular comisiones
- **Uso**: SOLO para pagar comisiones en dinero
- **Característica**: Valor diferente por país (ej: producto X = 293 VN en MX, 21 VN en USA, 67,400 VN en COP)

#### Paquetes de Inscripción - REGLA ESPECIAL

**⚠️ CRÍTICO**: Los paquetes de inscripción (kits de inicio) tienen reglas diferentes:

```python
# Kits de inicio
kit_inicio = {
    "genera_VN": False,  # ❌ NO generan Valor Negocio
    "genera_PV": True,   # ✅ SÍ generan Puntos de Volumen
    "paga_bono_rapido": True,  # ✅ SÍ pagan Bono Rápido
    "paga_bono_uninivel": False,  # ❌ NO pagan Bono Uninivel
    "cuenta_para_rangos": True,  # ✅ SÍ cuentan para alcanzar rangos
    "frecuencia_compra": "una_sola_vez"  # Se compra UNA SOLA VEZ
}
```

**Razón**: Los kits solo sirven para inscribirse y pagar bonos de reclutamiento. Las comisiones recurrentes vienen de las compras de productos.

---

## 🏆 Sistema de Rangos

### Requisitos por Rango

| Rango | PV Requerido | VG Requerido | Nivel Uninivel |
|-------|--------------|--------------|----------------|
| **Visionario** | 1,465 | 1,465 | Hasta nivel 3 |
| **Emprendedor** | 1,465 | 21,000 | Hasta nivel 4 |
| **Creativo** | 1,465 | 58,000 | Hasta nivel 5 |
| **Innovador** | 1,465 | 120,000 | Hasta nivel 6 |
| **Embajador Transformador** | 1,465 | 300,000 | Hasta nivel 9 + infinito (0.5%) |
| **Embajador Inspirador** | 1,465 | 650,000 | Hasta nivel 9 + infinito (1%) |
| **Embajador Consciente** | 1,465 | 1,300,000 | Hasta nivel 9 + infinito (1.5%) |
| **Embajador Solidario** | 1,465 | 2,900,000 | Hasta nivel 9 + infinito (2%) |

### Reglas de Rango

#### Regla 1: Permanencia de Rango
```python
# Una vez alcanzado un rango, lo mantienes hasta alcanzar el siguiente
if user.VG >= 58000 and user.VG < 120000:
    user.rank = "Creativo"  # Se mantiene hasta llegar a 120,000 VG

# Ejemplo:
# VG = 44,000 → Rango Emprendedor (21,000 ≤ VG < 58,000)
# VG = 58,000 → Rango Creativo (58,000 ≤ VG < 120,000)
# VG = 119,999 → Rango Creativo (aún no llega a 120,000)
# VG = 120,000 → Rango Innovador
```

#### Regla 2: PV Mínimo Constante
```python
# TODOS los rangos requieren el mismo PV personal
MINIMUM_PV = 1465

# Esto significa que DEBES mantener compras personales activas
# No puedes subir de rango solo con el volumen de tu red
```

#### Regla 3: No Hay Regresión de Rango
Los rangos NO bajan si tu VG disminuye (a menos que política de la empresa indique lo contrario).

---

## 💰 Tipos de Bonos

### 1. Bono Venta Directa

**Tipo**: Margen de reventa  
**Frecuencia**: Por venta  
**Cálculo**: Diferencia entre precio distribuidor y precio público

```python
def calcular_bono_venta_directa(producto):
    precio_distribuidor = producto.price_distributor
    precio_publico = producto.price_public
    margen = precio_publico - precio_distribuidor
    porcentaje = (margen / precio_publico) * 100
    
    return margen  # Típicamente 40-43%

# Ejemplo:
# Precio distribuidor: $349 MXN
# Precio público: $499 MXN
# Margen: $150 MXN (43%)
```

**Implementación técnica**:
- NO se registra en tabla `commissions` (es margen comercial directo)
- Se refleja en el precio de venta final
- No depende de la estructura de red

---

### 2. Bono Cashback

**Tipo**: Descuento en compra siguiente  
**Frecuencia**: Mensual (mismo mes)  
**Requisito**: Comprar 2,930 PV en un mes

```python
def calcular_bono_cashback(user, month):
    pv_comprado = sum_pv_in_month(user.id, month)
    
    if pv_comprado >= 2930:
        # 79% de descuento en siguiente compra del mismo mes
        # Base de cálculo: $3,490 MXN
        descuento = 3490 * 0.79  # = $2,757.10 MXN
        pagas_solo = 3490 - descuento  # = $732.90 MXN (~$1,050 con envío)
        
        return {
            "elegible": True,
            "descuento_mxn": 2757.10,
            "valido_hasta": end_of_month(month)
        }
    
    return {"elegible": False}
```

**Reglas especiales**:
- Solo aplica si compras DENTRO del mismo mes
- Se aplica en la SIGUIENTE compra (no en la misma que calificó)
- Requiere volumen personal específico (2,930 PV)
- El descuento es sobre un monto fijo ($3,490 MXN)

**Implementación técnica**:
- Registrar en tabla `cashback_credits`
- Validar que no haya expirado (fin del mes)
- Marcar como usado al aplicar

---

### 3. Bono de Lealtad

**Tipo**: Regalo físico  
**Frecuencia**: Cada 4 meses consecutivos  
**Requisito**: Comprar entre día 1 y 7 de cada mes

```python
def calcular_bono_lealtad(user):
    # Sistema de puntos de lealtad (diferente a PV/VN)
    PUNTOS_POR_MES = 25
    PUNTOS_REQUERIDOS = 100  # 4 meses
    
    # Verificar compra en ventana válida (1-7 del mes)
    def compro_en_ventana(user_id, year, month):
        compras = get_purchases(user_id, year, month)
        for compra in compras:
            if 1 <= compra.day <= 7:
                return True
        return False
    
    # Acumular puntos
    for mes in ultimos_meses():
        if compro_en_ventana(user.id, mes.year, mes.month):
            user.loyalty_points += 25
        else:
            # ⚠️ CRÍTICO: Si un mes falla, SE REINICIAN los puntos
            user.loyalty_points = 0
            break
    
    # Verificar si completó 100 puntos (4 meses)
    if user.loyalty_points >= 100:
        return {
            "elegible": True,
            "opciones": [
                "paquete_5_suplementos",
                "paquete_3_serums_2_cremas"
            ],
            "se_entrega_en": "envio_del_cuarto_mes"
        }
```

**⚠️ Regla crítica de reinicio**:
```python
# Si el usuario NO compra en la ventana 1-7, sus puntos se REINICIAN a 0
# Ejemplo:
# Mes 1 (Jan 3): Compra → 25 puntos
# Mes 2 (Feb 5): Compra → 50 puntos
# Mes 3 (Mar 15): NO compra entre 1-7 → REINICIO a 0 puntos ❌
# Mes 4 (Apr 4): Compra → 25 puntos (comenzando de nuevo)
```

**Implementación técnica**:
- Tabla `loyalty_points_history` con timestamp de cada compra
- Job diario que valida compras del 1-7
- Job mensual día 8 que reinicia puntos si no hubo compra válida
- Registrar entrega de regalo en tabla `loyalty_rewards_delivered`

---

### 4. Bono Rápido (Bono Semanal)

**Tipo**: Comisión por inscripción  
**Frecuencia**: Instantánea (al confirmar pago del kit)  
**Base de cálculo**: VP (Volumen Personal) del paquete de inscripción

#### Tabla de Comisiones

| Nivel de Profundidad | Porcentaje | Cálculo Base |
|----------------------|------------|--------------|
| Nivel 1 (Directos) | 30% | 30% del VP del kit |
| Nivel 2 (Indirectos) | 10% | 10% del VP del kit |
| Nivel 3 (Indirectos) | 5% | 5% del VP del kit |

#### Paquetes de Inscripción

| Kit | Precio MXN | Precio USD | Precio COP | VP Generado |
|-----|------------|------------|------------|-------------|
| **Full Supplement** | $1,996 | $120 | $479,000 | 1,670 |
| **Full Skin** | $2,596 | $160 | $622,800 | 2,180 |
| **Full Protect** | $5,790 | $353 | $1,389,000 | 4,860 |

#### Fórmula de Cálculo

```python
def calcular_bono_rapido(nuevo_miembro, kit_comprado):
    """
    Calcula el Bono Rápido para los 3 primeros niveles ascendentes.
    Se paga INSTANTÁNEAMENTE al confirmar el pago del kit.
    """
    
    # VP del kit comprado
    vp_kit = {
        "full_supplement": 1670,
        "full_skin": 2180,
        "full_protect": 4860
    }[kit_comprado]
    
    # Obtener los 3 niveles ascendentes
    genealogia = get_upline(nuevo_miembro.id, depth=3)
    
    comisiones = []
    
    for nivel, patrocinador in enumerate(genealogia, start=1):
        if nivel == 1:
            porcentaje = 0.30
        elif nivel == 2:
            porcentaje = 0.10
        elif nivel == 3:
            porcentaje = 0.05
        else:
            break  # Solo 3 niveles
        
        # Calcular comisión en VP
        comision_vp = vp_kit * porcentaje
        
        # ⚠️ IMPORTANTE: Los kits NO generan VN
        # La comisión se paga como un monto fijo en la moneda del patrocinador
        # basándose en el precio del kit en su país
        
        precio_kit_pais_patrocinador = get_kit_price(
            kit_comprado, 
            patrocinador.country
        )
        
        comision_monetaria = precio_kit_pais_patrocinador * porcentaje
        
        comisiones.append({
            "member_id": patrocinador.id,
            "bonus_type": "bono_rapido",
            "level_depth": nivel,
            "source_member_id": nuevo_miembro.id,
            "amount": comision_monetaria,
            "currency": patrocinador.country_currency,
            "calculated_at": now(),
            "status": "pending"
        })
    
    return comisiones
```

#### Ejemplo Práctico

```python
# Escenario:
# A (México) → B (USA) → C (Colombia) → D compra kit Full Protect

# D compra Full Protect
kit = "full_protect"
precios_kit = {
    "MXN": 5790,
    "USD": 353,
    "COP": 1389000
}

# Comisiones generadas:

# C recibe (Nivel 1 de D, país Colombia):
comision_C = precios_kit["COP"] * 0.30
# = 1,389,000 * 0.30 = 416,700 COP

# B recibe (Nivel 2 de D, país USA):
comision_B = precios_kit["USD"] * 0.10
# = 353 * 0.10 = 35.30 USD

# A recibe (Nivel 3 de D, país México):
comision_A = precios_kit["MXN"] * 0.05
# = 5,790 * 0.05 = 289.50 MXN
```

**Implementación técnica**:
- Trigger al confirmar `transactions.payment_confirmed_at`
- Cálculo sincrónico (bloquea hasta completar)
- Inserción inmediata en tabla `commissions`
- Estado inicial: `pending`, cambia a `paid` al procesar pago

---

### 5. Bono Unilevel Infinito

**Tipo**: Comisión mensual recurrente  
**Frecuencia**: Mensual (día 31 a las 23:59:59)  
**Base de cálculo**: VN (Valor Negocio) de productos comprados por la red

#### Tabla de Porcentajes por Rango

| Rango | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 | N9 | N10+ |
|-------|----|----|----|----|----|----|----|----|----|----|
| **Visionario** | 5% | 8% | 10% | - | - | - | - | - | - | - |
| **Emprendedor** | 5% | 8% | 10% | 10% | - | - | - | - | - | - |
| **Creativo** | 5% | 8% | 10% | 10% | 5% | - | - | - | - | - |
| **Innovador** | 5% | 8% | 10% | 10% | 5% | 4% | - | - | - | - |
| **E. Transformador** | 5% | 8% | 10% | 10% | 5% | 4% | 4% | 3% | 3% | 0.5% |
| **E. Inspirador** | 5% | 8% | 10% | 10% | 5% | 4% | 4% | 3% | 3% | 1% |
| **E. Consciente** | 5% | 8% | 10% | 10% | 5% | 4% | 4% | 3% | 3% | 1.5% |
| **E. Solidario** | 5% | 8% | 10% | 10% | 5% | 4% | 4% | 3% | 3% | 2% |

#### Fórmula de Cálculo

```python
def calcular_bono_uninivel(member_id, period_id):
    """
    Calcula el Bono Uninivel mensual.
    Se ejecuta el último día del mes a las 23:59:59.
    """
    
    # Obtener rango actual del miembro
    member = get_member(member_id)
    rank = member.current_rank
    
    # Tabla de porcentajes por rango
    percentages = {
        "visionario": [5, 8, 10],
        "emprendedor": [5, 8, 10, 10],
        "creativo": [5, 8, 10, 10, 5],
        "innovador": [5, 8, 10, 10, 5, 4],
        "embajador_transformador": [5, 8, 10, 10, 5, 4, 4, 3, 3, 0.5],
        "embajador_inspirador": [5, 8, 10, 10, 5, 4, 4, 3, 3, 1],
        "embajador_consciente": [5, 8, 10, 10, 5, 4, 4, 3, 3, 1.5],
        "embajador_solidario": [5, 8, 10, 10, 5, 4, 4, 3, 3, 2]
    }
    
    rank_percentages = percentages[rank.lower()]
    max_depth = len(rank_percentages)
    infinity_percentage = rank_percentages[-1] if max_depth >= 10 else None
    
    total_comision = 0
    comisiones_detalle = []
    
    # Iterar por cada nivel hasta la profundidad del rango
    for depth in range(1, max_depth + 1):
        # Para rangos Embajador, nivel 10+ usa porcentaje infinito
        if depth >= 10 and infinity_percentage:
            percentage = infinity_percentage
            # Calcular VN desde nivel 10 hasta el infinito
            vn_level = sum_vn_from_depth_to_infinity(
                member_id, 
                period_id, 
                start_depth=10
            )
        else:
            percentage = rank_percentages[depth - 1]
            # Calcular VN solo de este nivel específico
            vn_level = sum_vn_by_depth(member_id, period_id, depth)
        
        if vn_level > 0:
            comision_level = vn_level * (percentage / 100)
            total_comision += comision_level
            
            comisiones_detalle.append({
                "member_id": member_id,
                "bonus_type": "bono_uninivel",
                "period_id": period_id,
                "level_depth": depth if depth < 10 else "10+",
                "amount_vn": vn_level,
                "percentage": percentage,
                "amount_converted": comision_level,
                "currency_destination": member.country_currency
            })
    
    return comisiones_detalle

def sum_vn_by_depth(member_id, period_id, depth):
    """
    Suma el VN de todas las transacciones de un nivel específico.
    
    ⚠️ SOLO cuenta transacciones de PRODUCTOS, NO de kits de inicio.
    """
    query = """
        SELECT SUM(t.vn_earned) as total_vn
        FROM transactions t
        JOIN user_tree_path utp ON utp.descendant_id = t.member_id
        JOIN products p ON p.id = t.product_id
        WHERE utp.ancestor_id = :member_id
          AND utp.depth = :depth
          AND t.period_id = :period_id
          AND t.payment_confirmed_at IS NOT NULL
          AND p.presentation != 'kit'  -- ❌ Excluir kits de inicio
    """
    
    result = db.execute(query, {
        "member_id": member_id,
        "depth": depth,
        "period_id": period_id
    })
    
    return result.total_vn or 0

def sum_vn_from_depth_to_infinity(member_id, period_id, start_depth):
    """
    Suma el VN desde un nivel hasta el infinito (para rangos Embajador).
    """
    query = """
        SELECT SUM(t.vn_earned) as total_vn
        FROM transactions t
        JOIN user_tree_path utp ON utp.descendant_id = t.member_id
        JOIN products p ON p.id = t.product_id
        WHERE utp.ancestor_id = :member_id
          AND utp.depth >= :start_depth
          AND t.period_id = :period_id
          AND t.payment_confirmed_at IS NOT NULL
          AND p.presentation != 'kit'  -- ❌ Excluir kits de inicio
    """
    
    result = db.execute(query, {
        "member_id": member_id,
        "start_depth": start_depth,
        "period_id": period_id
    })
    
    return result.total_vn or 0
```

#### Ejemplo Práctico

```python
# Escenario: Usuario es Rango Creativo
# Tiene red de 5 niveles con compras en el mes

niveles_vn = {
    1: 10000,  # VN nivel 1
    2: 8000,   # VN nivel 2
    3: 6000,   # VN nivel 3
    4: 4000,   # VN nivel 4
    5: 2000    # VN nivel 5
}

# Rango Creativo: [5%, 8%, 10%, 10%, 5%]

comisiones = {
    "nivel_1": 10000 * 0.05 = 500,
    "nivel_2": 8000 * 0.08 = 640,
    "nivel_3": 6000 * 0.10 = 600,
    "nivel_4": 4000 * 0.10 = 400,
    "nivel_5": 2000 * 0.05 = 100
}

total_uninivel = 500 + 640 + 600 + 400 + 100 = 2,240 VN
```

**Implementación técnica**:
- Job programado: día 31 de cada mes a las 23:59:59
- Procesamiento batch de todos los miembros
- Almacenar en `commissions` con `status='pending'`
- Crear snapshot en `monthly_commission_snapshots`
- Tiempo estimado: 2-5 minutos para 50k usuarios

---

### 6. Bono por Alcance

**Tipo**: Bono único por rango alcanzado  
**Frecuencia**: Una única vez por rango (por primera vez)  
**Requisito especial**: Rango Emprendedor debe lograrse en 30 días desde inscripción

#### Tabla de Bonos

| Rango | Monto MXN | Monto USD | Monto COP | Plazo Especial |
|-------|-----------|-----------|-----------|----------------|
| **Emprendedor** | $1,500 | $85 | $330,000 | ⚠️ 30 días desde inscripción |
| **Creativo** | $3,000 | $165 | $666,000 | - |
| **Innovador** | $5,000 | $280 | $1,100,000 | - |
| **E. Transformador** | $7,500 | $390 | $1,650,000 | - |
| **E. Inspirador** | $10,000 | $555 | $2,220,000 | - |
| **E. Consciente** | $20,000 | $1,111 | $4,400,000 | - |
| **E. Solidario** | $40,000 | $2,222 | $8,800,000 | - |

#### Fórmula de Cálculo

```python
def calcular_bono_alcance(member_id, new_rank):
    """
    Calcula el Bono por Alcance cuando un miembro sube de rango.
    Se paga UNA SOLA VEZ por cada rango alcanzado.
    """
    
    member = get_member(member_id)
    
    # Verificar si ya cobró este rango antes
    historico = db.query(Commissions).filter(
        Commissions.member_id == member_id,
        Commissions.bonus_type == "bono_alcance",
        Commissions.notes.contains(new_rank)
    ).first()
    
    if historico:
        return {"elegible": False, "razon": "Ya cobró este rango antes"}
    
    # ⚠️ REGLA ESPECIAL: Rango Emprendedor tiene plazo de 30 días
    if new_rank == "emprendedor":
        dias_desde_inscripcion = (now() - member.created_at).days
        if dias_desde_inscripcion > 30:
            return {
                "elegible": False, 
                "razon": "Excedió 30 días desde inscripción"
            }
    
    # Tabla de montos por país
    bonos = {
        "emprendedor": {"MXN": 1500, "USD": 85, "COP": 330000},
        "creativo": {"MXN": 3000, "USD": 165, "COP": 666000},
        "innovador": {"MXN": 5000, "USD": 280, "COP": 1100000},
        "embajador_transformador": {"MXN": 7500, "USD": 390, "COP": 1650000},
        "embajador_inspirador": {"MXN": 10000, "USD": 555, "COP": 2220000},
        "embajador_consciente": {"MXN": 20000, "USD": 1111, "COP": 4400000},
        "embajador_solidario": {"MXN": 40000, "USD": 2222, "COP": 8800000}
    }
    
    currency = member.country_currency
    monto = bonos[new_rank.lower()][currency]
    
    return {
        "elegible": True,
        "member_id": member_id,
        "bonus_type": "bono_alcance",
        "amount": monto,
        "currency": currency,
        "notes": f"Bono por alcanzar rango {new_rank} por primera vez"
    }
```

**Implementación técnica**:
- Trigger cuando `user_rank_history` registra nuevo rango
- Validar que sea la primera vez que alcanza ese rango
- Para Emprendedor: validar timestamp de inscripción
- Insertar en `commissions` inmediatamente
- Marcar en histórico para evitar duplicados

---

### 7. Bono de Igualación (Matching Bonus)

**Tipo**: Comisión sobre comisiones uninivel de tu equipo  
**Frecuencia**: Mensual (junto con uninivel)  
**Requisito**: Rango Embajador Transformador o superior  
**Base de cálculo**: Bono Uninivel ganado por miembros de tu equipo

#### Tabla de Porcentajes

| Rango | Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 |
|-------|---------|---------|---------|---------|
| **E. Transformador** | 30% | - | - | - |
| **E. Inspirador** | 30% | 20% | - | - |
| **E. Consciente** | 30% | 20% | 10% | - |
| **E. Solidario** | 30% | 20% | 10% | 5% |

**Nota**: Los "niveles" aquí son diferentes. Se refiere a niveles de profundidad en tu equipo que también son Embajadores.

#### Fórmula de Cálculo

```python
def calcular_bono_matching(member_id, period_id):
    """
    Calcula el Matching Bonus basándose en las comisiones uninivel
    de los miembros en tu equipo que sean Embajadores.
    
    ⚠️ IMPORTANTE: Solo elegible para rangos Embajador Transformador+
    """
    
    member = get_member(member_id)
    rank = member.current_rank
    
    # Solo rangos Embajador son elegibles
    embajador_ranks = [
        "embajador_transformador",
        "embajador_inspirador",
        "embajador_consciente",
        "embajador_solidario"
    ]
    
    if rank.lower() not in embajador_ranks:
        return []
    
    # Tabla de porcentajes
    matching_percentages = {
        "embajador_transformador": [30],
        "embajador_inspirador": [30, 20],
        "embajador_consciente": [30, 20, 10],
        "embajador_solidario": [30, 20, 10, 5]
    }
    
    percentages = matching_percentages[rank.lower()]
    max_depth = len(percentages)
    
    comisiones = []
    
    # Obtener miembros de tu equipo que son Embajadores
    for depth in range(1, max_depth + 1):
        # Buscar miembros en este nivel de profundidad
        team_members = get_downline_by_depth(member_id, depth)
        
        for team_member in team_members:
            # Solo si es Embajador
            if team_member.rank.lower() not in embajador_ranks:
                continue
            
            # Obtener su comisión uninivel del período
            uninivel_ganado = db.query(Commissions).filter(
                Commissions.member_id == team_member.id,
                Commissions.bonus_type == "bono_uninivel",
                Commissions.period_id == period_id
            ).sum(Commissions.amount_converted)
            
            if uninivel_ganado > 0:
                percentage = percentages[depth - 1]
                matching_bonus = uninivel_ganado * (percentage / 100)
                
                comisiones.append({
                    "member_id": member_id,
                    "bonus_type": "bono_matching",
                    "source_member_id": team_member.id,
                    "period_id": period_id,
                    "level_depth": depth,
                    "amount_vn": uninivel_ganado,
                    "percentage": percentage,
                    "amount_converted": matching_bonus,
                    "currency_destination": member.country_currency,
                    "notes": f"Matching {percentage}% sobre uninivel de {team_member.full_name}"
                })
    
    return comisiones
```

#### Ejemplo Práctico

```python
# Escenario:
# Tú: Embajador Solidario
# Nivel 1: Juan (Embajador Transformador) ganó 10,000 MXN en uninivel
# Nivel 2: María (Embajador Inspirador) ganó 8,000 MXN en uninivel
# Nivel 3: Pedro (Embajador Consciente) ganó 6,000 MXN en uninivel

# Como Embajador Solidario tienes: [30%, 20%, 10%, 5%]

matching = {
    "nivel_1_juan": 10000 * 0.30 = 3000 MXN,
    "nivel_2_maria": 8000 * 0.20 = 1600 MXN,
    "nivel_3_pedro": 6000 * 0.10 = 600 MXN
}

total_matching = 3000 + 1600 + 600 = 5,200 MXN
```

**Implementación técnica**:
- Se calcula DESPUÉS del Bono Uninivel
- Requiere que las comisiones uninivel ya estén calculadas
- Job programado junto con cierre mensual
- Validar rango del receptor (debe ser Embajador)

---

### 8. Bono de Automóvil

**Tipo**: Bono fijo mensual + enganche inicial  
**Frecuencia**: Una vez (enganche) + mensual (manteniendo rango)  
**Requisito**: Embajador Transformador por 2 meses consecutivos

```python
def calcular_bono_automovil(member_id):
    """
    Calcula el Bono de Automóvil para Embajadores Transformadores.
    
    Dos componentes:
    1. Enganche (una vez): $50,000 MXN / $2,500 USD / $11,000,000 COP
    2. Mensualidad (recurrente): $5,000 MXN / $250 USD / $1,100,000 COP
    """
    
    member = get_member(member_id)
    
    # Verificar rango actual
    if member.current_rank.lower() not in [
        "embajador_transformador",
        "embajador_inspirador",
        "embajador_consciente",
        "embajador_solidario"
    ]:
        return {"elegible": False, "razon": "No es Embajador Transformador+"}
    
    # Verificar historial de rangos (2 meses consecutivos)
    historial = get_rank_history(member_id, last_n_months=2)
    
    meses_consecutivos = 0
    for record in historial:
        if record.rank.lower().startswith("embajador"):
            meses_consecutivos += 1
        else:
            meses_consecutivos = 0
    
    bonos = []
    
    # Enganche (primera vez que cumple 2 meses consecutivos)
    if meses_consecutivos == 2:
        # Verificar que no lo haya cobrado antes
        enganche_previo = db.query(Commissions).filter(
            Commissions.member_id == member_id,
            Commissions.bonus_type == "bono_automovil",
            Commissions.notes.contains("enganche")
        ).first()
        
        if not enganche_previo:
            enganche = {
                "MXN": 50000,
                "USD": 2500,
                "COP": 11000000
            }
            
            bonos.append({
                "member_id": member_id,
                "bonus_type": "bono_automovil",
                "amount": enganche[member.country_currency],
                "currency": member.country_currency,
                "notes": "Enganche de automóvil (pago único)"
            })
    
    # Mensualidad (cada mes que mantiene el rango)
    if meses_consecutivos >= 2:
        mensualidad = {
            "MXN": 5000,
            "USD": 250,
            "COP": 1100000
        }
        
        bonos.append({
            "member_id": member_id,
            "bonus_type": "bono_automovil",
            "amount": mensualidad[member.country_currency],
            "currency": member.country_currency,
            "notes": "Mensualidad de automóvil"
        })
    
    return bonos
```

**Implementación técnica**:
- Validar historial de rangos mensual
- Marcar enganche como "pagado una vez"
- Mensualidad se calcula junto con bonos mensuales
- Si pierde el rango, se detiene la mensualidad

---

### 9. Bono NN Travels

**Tipo**: Puntos acumulables para viaje  
**Frecuencia**: Campaña semestral (cambia cada 6 meses)  
**Meta actual**: 200 puntos NN TRAVELS

#### Formas de Ganar Puntos

##### 1. Por Kits de Inicio Comprados

| Kit | Puntos Base | Bonificación Oct 2024 |
|-----|-------------|----------------------|
| **Full Supplement** | 1 punto | - |
| **Full Skin** | 2 puntos | - |
| **Full Protect** | 4 puntos | +1 punto si inscribes 5 personas |

```python
# Bonificación especial Octubre
if mes == "octubre" and full_protect_inscritos >= 5:
    puntos = (4 * 5) + 5  # 20 base + 5 bonificación = 25 puntos
```

##### 2. Por Alcanzar Rangos

**Importante**: Puntos diferentes si TÚ alcanzas el rango vs si tu DIRECTO lo alcanza.

| Rango | Tú Alcanzas | Tu Directo Alcanza | Promo Octubre (Tú) | Promo Octubre (Directo) |
|-------|-------------|--------------------|--------------------|-------------------------|
| **Visionario** | 1 | 1 | 2 | 2 |
| **Emprendedor** | 5 | 5 | 10 | 10 |
| **Creativo** | 15 | 10 | 30 | 30 |
| **Innovador** | 25 | 20 | 50 | 50 |
| **E. Transformador** | 50 | 30 | 100 | 100 |
| **E. Inspirador** | 100 | 50 | 200 | 200 |
| **E. Consciente** | 200 | 100 | 200 | 200 |
| **E. Solidario** | 200 | 100 | 200 | 200 |

#### Fórmula de Cálculo

```python
def calcular_puntos_travels(member_id, campaign_period):
    """
    Calcula puntos NN TRAVELS para una campaña semestral.
    Los puntos son acumulables durante todo el período.
    """
    
    puntos_total = 0
    
    # 1. Puntos por kits comprados en su red
    kits_comprados = db.query(Transactions).filter(
        Transactions.member_id.in_(
            get_all_downline(member_id)
        ),
        Transactions.product_id.in_(
            get_starter_kits()
        ),
        Transactions.created_at.between(
            campaign_period.start,
            campaign_period.end
        )
    ).all()
    
    for kit in kits_comprados:
        if kit.product_name == "full_supplement":
            puntos_total += 1
        elif kit.product_name == "full_skin":
            puntos_total += 2
        elif kit.product_name == "full_protect":
            puntos_total += 4
    
    # Bonificación especial: 5 Full Protect en Octubre
    if campaign_period.includes_month("octubre"):
        full_protect_oct = count_full_protect_inscriptions(
            member_id, 
            year=2024, 
            month=10
        )
        if full_protect_oct >= 5:
            puntos_total += 5
    
    # 2. Puntos por rangos alcanzados
    rank_achievements = db.query(UserRankHistory).filter(
        UserRankHistory.member_id == member_id,
        UserRankHistory.achieved_on.between(
            campaign_period.start,
            campaign_period.end
        )
    ).all()
    
    for achievement in rank_achievements:
        puntos = get_travel_points_for_rank(
            achievement.rank,
            is_self=True,
            is_october_promo=campaign_period.includes_month("octubre")
        )
        puntos_total += puntos
    
    # 3. Puntos por rangos de directos (solo nivel 1)
    directos = get_level_1_downline(member_id)
    for directo in directos:
        direct_achievements = db.query(UserRankHistory).filter(
            UserRankHistory.member_id == directo.id,
            UserRankHistory.achieved_on.between(
                campaign_period.start,
                campaign_period.end
            )
        ).all()
        
        for achievement in direct_achievements:
            puntos = get_travel_points_for_rank(
                achievement.rank,
                is_self=False,
                is_october_promo=campaign_period.includes_month("octubre")
            )
            puntos_total += puntos
    
    # Verificar si califica para el viaje
    califica = puntos_total >= 200
    
    return {
        "member_id": member_id,
        "campaign_period": campaign_period.name,
        "total_points": puntos_total,
        "target_points": 200,
        "qualifies": califica,
        "details": {
            "kit_points": kit_points,
            "self_rank_points": self_rank_points,
            "direct_rank_points": direct_rank_points
        }
    }
```

**Implementación técnica**:
- Tabla separada: `travel_campaign_points`
- Actualización en tiempo real cuando ocurre evento
- Job mensual para consolidar puntos
- Dashboard para ver progreso hacia meta

---

## 🔴 Reglas Críticas del Negocio

### Regla 1: Kits de Inicio vs Productos Regulares

```python
# ⚠️ DIFERENCIA CRÍTICA

# Kits de Inicio:
kit = {
    "genera_PV": True,      # Para rangos
    "genera_VN": False,     # ❌ NO paga uninivel
    "paga_bono_rapido": True,  # ✅ Sí paga
    "frecuencia": "una_vez"
}

# Productos Regulares:
producto = {
    "genera_PV": True,      # Para rangos
    "genera_VN": True,      # ✅ Sí paga uninivel
    "paga_bono_rapido": False,  # ❌ No aplica
    "frecuencia": "ilimitada"
}
```

### Regla 2: Conversión de Monedas

```python
# Ejemplo: Mexicano refiere Colombiano

# Colombiano compra producto: VN = 67,400 COP
# Mexicano gana comisión uninivel 5% = 3,370 COP

# Sistema convierte a MXN:
tasa_fija_empresa = 0.00435  # 1 COP = 0.00435 MXN
comision_mxn = 3370 * 0.00435 = 14.66 MXN

# ⚠️ IMPORTANTE: Se usa tasa fija de la empresa, NO tasa de bancos
```

### Regla 3: Timestamp Determinante

```python
# Para determinar a qué período pertenece una transacción:

if transaction.payment_confirmed_at.month == 12:
    period = "diciembre"
elif transaction.payment_confirmed_at.month == 1:
    period = "enero"

# NO importa cuándo se creó la orden (created_at)
# SOLO importa cuándo se confirmó el pago (payment_confirmed_at)
```

### Regla 4: Rangos No Regresan

```python
# Una vez alcanzado un rango, se mantiene
# (a menos que política futura indique lo contrario)

if user.max_rank_achieved == "creativo":
    user.current_rank = "creativo"
    # Incluso si su VG baja temporalmente
```

### Regla 5: Bono Rápido Solo 3 Niveles

```python
# SOLO los primeros 3 niveles ascendentes reciben Bono Rápido
# No importa el rango del patrocinador

upline = get_upline(nuevo_miembro, depth=3)
# upline[0] = Nivel 1 (30%)
# upline[1] = Nivel 2 (10%)
# upline[2] = Nivel 3 (5%)
# upline[3+] = ❌ No reciben nada
```

---

## 📐 Fórmulas de Cálculo Consolidadas

### Fórmula General de Comisiones

```python
def calcular_comision_uninivel(vn_base, porcentaje_nivel, tasa_cambio=1.0):
    """
    Fórmula general para calcular comisiones uninivel.
    
    Args:
        vn_base: Valor Negocio en moneda origen
        porcentaje_nivel: Porcentaje según nivel y rango (ej: 5, 8, 10)
        tasa_cambio: Tasa de conversión a moneda destino
    
    Returns:
        Comisión en moneda destino
    """
    comision_origen = vn_base * (porcentaje_nivel / 100)
    comision_destino = comision_origen * tasa_cambio
    return comision_destino

# Ejemplo:
# VN Colombia = 67,400 COP
# Nivel 1 = 5%
# Tasa COP a MXN = 0.00435

comision = calcular_comision_uninivel(67400, 5, 0.00435)
# = 67,400 * 0.05 * 0.00435
# = 3,370 * 0.00435
# = 14.66 MXN
```

### Fórmula de VG (Volumen Grupal)

```python
def calcular_vg(member_id, period_id=None):
    """
    Calcula el Volumen Grupal de un miembro.
    VG = PV propio + PV de toda la red descendente
    """
    
    # PV propio del período
    pv_propio = db.query(func.sum(Transactions.pv_earned)).filter(
        Transactions.member_id == member_id,
        Transactions.period_id == period_id if period_id else True,
        Transactions.payment_confirmed_at.isnot(None)
    ).scalar() or 0
    
    # PV de toda la red descendente
    pv_red = db.query(func.sum(Transactions.pv_earned)).filter(
        Transactions.member_id.in_(
            select(UserTreePath.descendant_id).where(
                UserTreePath.ancestor_id == member_id,
                UserTreePath.depth > 0  # Excluir self-reference
            )
        ),
        Transactions.period_id == period_id if period_id else True,
        Transactions.payment_confirmed_at.isnot(None)
    ).scalar() or 0
    
    return pv_propio + pv_red
```

---

## ⚠️ Casos Especiales y Edge Cases

### Caso 1: Usuario Pierde Rango (Temporalmente)

```python
# Política: Los rangos NO bajan
# Pero las comisiones sí se calculan basándose en rango actual

if user.current_vg < required_vg_for_rank(user.current_rank):
    # El usuario mantiene su rango visualmente
    # Pero sus comisiones siguen usando su rango actual
    # (esto puede cambiar según política de negocio)
    pass
```

### Caso 2: Compra Internacional con Conversión

```python
# Escenario complejo:
# A (México) → B (USA) → C (Colombia)
# C compra producto en Colombia: VN = 67,400 COP

# B gana uninivel nivel 1 (5%):
comision_b_cop = 67400 * 0.05 = 3,370 COP
comision_b_usd = 3370 * tasa_cop_to_usd = X USD

# A gana uninivel nivel 2 (8%):
comision_a_cop = 67400 * 0.08 = 5,392 COP
comision_a_mxn = 5392 * tasa_cop_to_mxn = Y MXN
```

### Caso 3: Cambio de Rango a Mitad de Mes

```python
# Si usuario sube de rango el día 15:
# - Bono Rápido: Se paga con porcentajes del rango ACTUAL al momento
# - Bono Uninivel: Se calcula con rango VIGENTE al final del mes (día 31)

# Recomendación: Usar rango al momento del cierre mensual
rank_at_closure = get_rank_at_date(member_id, end_of_month())
```

### Caso 4: Devolución de Producto

```python
# Si hay devolución:
# 1. Restar PV del VG del usuario
# 2. Restar VN que generó
# 3. ¿Restar comisiones ya pagadas? (definir política)

def procesar_devolucion(transaction_id):
    transaction = get_transaction(transaction_id)
    
    # Marcar transacción como devuelta
    transaction.status = "refunded"
    
    # Restar PV/VN
    # (El VG se recalcula automáticamente)
    
    # Opcional: Generar comisiones negativas
    comisiones_originales = get_commissions_from_transaction(transaction_id)
    for comision in comisiones_originales:
        crear_comision_negativa(comision)
```

### Caso 5: Bono Rápido Sin 3 Niveles Completos

```python
# Si nuevo miembro solo tiene 2 niveles ascendentes:

nuevo = Usuario(id=100)
upline = get_upline(nuevo.id, depth=3)

# upline = [Usuario(50), Usuario(10)]  # Solo 2 niveles

# Resultado:
# Usuario 50: 30% (nivel 1)
# Usuario 10: 10% (nivel 2)
# Nivel 3: No existe, no se paga a nadie
```

---

## 💻 Ejemplos de Implementación

### Ejemplo 1: Calcular Todas las Comisiones de un Período

```python
def calcular_comisiones_periodo(period_id):
    """
    Job principal que se ejecuta el día 31 a las 23:59:59.
    Calcula TODAS las comisiones mensuales.
    """
    
    # 1. Obtener todos los miembros activos
    miembros = db.query(Users).filter(
        Users.status == UserStatus.QUALIFIED
    ).all()
    
    total_comisiones = []
    
    for miembro in miembros:
        # 2. Calcular Bono Uninivel
        comisiones_uninivel = calcular_bono_uninivel(
            miembro.member_id, 
            period_id
        )
        total_comisiones.extend(comisiones_uninivel)
        
        # 3. Calcular Bono Matching (solo Embajadores)
        if miembro.current_rank.lower().startswith("embajador"):
            comisiones_matching = calcular_bono_matching(
                miembro.member_id,
                period_id
            )
            total_comisiones.extend(comisiones_matching)
        
        # 4. Calcular Bono de Automóvil (si aplica)
        if miembro.current_rank.lower() in [
            "embajador_transformador",
            "embajador_inspirador",
            "embajador_consciente",
            "embajador_solidario"
        ]:
            bonos_auto = calcular_bono_automovil(miembro.member_id)
            total_comisiones.extend(bonos_auto)
    
    # 5. Insertar todas las comisiones
    db.bulk_insert(Commissions, total_comisiones)
    
    # 6. Generar snapshots
    generar_snapshots_mensuales(period_id)
    
    # 7. Cerrar período
    period = get_period(period_id)
    period.status = "closed"
    db.commit()
    
    return {
        "period_id": period_id,
        "total_commissions": len(total_comisiones),
        "total_amount": sum(c["amount_converted"] for c in total_comisiones)
    }
```

### Ejemplo 2: Validar Elegibilidad para Bono

```python
def validar_elegibilidad_bono(member_id, bonus_type):
    """
    Valida si un miembro es elegible para un tipo de bono.
    """
    
    member = get_member(member_id)
    
    validaciones = {
        "bono_uninivel": lambda m: m.status == UserStatus.QUALIFIED,
        
        "bono_matching": lambda m: m.current_rank.lower().startswith("embajador"),
        
        "bono_alcance": lambda m: not ha_cobrado_rango_antes(m.id, m.current_rank),
        
        "bono_automovil": lambda m: (
            m.current_rank.lower().startswith("embajador") and
            meses_consecutivos_embajador(m.id) >= 2
        ),
        
        "bono_cashback": lambda m: (
            calcular_pv_mes_actual(m.id) >= 2930
        ),
        
        "bono_lealtad": lambda m: (
            compro_entre_1_y_7_ultimos_4_meses(m.id)
        )
    }
    
    if bonus_type not in validaciones:
        return False
    
    return validaciones[bonus_type](member)
```

### Ejemplo 3: Dashboard de Comisiones

```python
def get_commission_dashboard(member_id, period_id):
    """
    Genera dashboard de comisiones para mostrar al usuario.
    """
    
    # Obtener todas las comisiones del período
    comisiones = db.query(Commissions).filter(
        Commissions.member_id == member_id,
        Commissions.period_id == period_id
    ).all()
    
    # Agrupar por tipo
    por_tipo = {}
    for comision in comisiones:
        tipo = comision.bonus_type
        if tipo not in por_tipo:
            por_tipo[tipo] = {
                "count": 0,
                "total": 0,
                "details": []
            }
        
        por_tipo[tipo]["count"] += 1
        por_tipo[tipo]["total"] += comision.amount_converted
        por_tipo[tipo]["details"].append({
            "level": comision.level_depth,
            "amount": comision.amount_converted,
            "source": comision.source_member_id
        })
    
    # Calcular total
    total_period = sum(c.amount_converted for c in comisiones)
    
    return {
        "member_id": member_id,
        "period": get_period(period_id).name,
        "total_earned": total_period,
        "currency": get_member(member_id).country_currency,
        "by_bonus_type": por_tipo,
        "status": "pending" if any(c.status == "pending" for c in comisiones) else "paid"
    }
```

---

## 🎓 Glosario de Términos

- **PV (Personal Volume)**: Puntos de volumen personal, solo para rangos
- **VG (Volume Group)**: Volumen grupal, suma de PV de toda la red
- **VN (Valor Negocio)**: Valor monetario localizado, solo para comisiones
- **Nivel**: Profundidad en la red (Nivel 1 = directos, Nivel 2 = indirectos, etc.)
- **Upline**: Personas arriba de ti en la red (tus patrocinadores)
- **Downline**: Personas abajo de ti en la red (a quienes referiste directa o indirectamente)
- **Directos**: Personas que tú referiste directamente (tu Nivel 1)
- **Sponsor**: Persona que te refirió directamente
- **Kit de Inicio**: Paquete de inscripción (se compra una sola vez)
- **Rango**: Nivel de liderazgo basado en PV y VG
- **Período**: Mes calendario para cálculo de comisiones

---

## 📚 Referencias y Recursos

### Documentos Base
- Plan de Compensación NN Protect (PDF original)
- Rangos NN Protect (PDF original)
- Catálogo de Productos por País

### Políticas Pendientes de Definir
1. ¿Las comisiones se restan en caso de devolución?
2. ¿Hay período de gracia para nuevos distribuidores?
3. ¿Los rangos bajan si el VG disminuye?
4. ¿Hay límite máximo de comisión por período?
5. ¿Cuál es la política de cambio de tasas de cambio?

---

**Última actualización**: Septiembre 2025  
**Versión**: 1.0  
**Mantenido por**: Equipo de Desarrollo NN Protect
```