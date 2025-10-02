# 🧪 Plan de Testing E2E - Flujo de Compra

**Autor:** Giovann (QA & Financial Testing)  
**Fecha:** 2025-10-02  
**Objetivo:** Validar el flujo completo de compra desde móvil después de arreglos  
**Ambiente:** Localhost (desarrollo)

---

## 📱 Pre-requisitos de Testing

### Ambiente de Testing:
- ✅ Servidor Reflex corriendo en `localhost:3000`
- ✅ Base de datos Supabase (desarrollo) conectada
- ✅ Usuario de prueba con credenciales válidas
- ✅ Navegador móvil o DevTools en modo responsive

### Datos de Prueba Sugeridos:
- **Usuario:** `member_id=1` (usuario de prueba)
- **Productos:** Cualquier producto de la tienda (usar IDs: 1, 4, etc.)
- **Cantidades:** Probar con 1, 2, 5, 10 unidades

---

## 🎯 Casos de Prueba E2E

### TEST 1: Login y Acceso a Tienda ✅

**Objetivo:** Validar que el usuario puede iniciar sesión y acceder a la tienda

**Pasos:**
1. Abrir `localhost:3000` en navegador móvil o DevTools responsive
2. Hacer clic en "Iniciar Sesión" o navegar a `/login`
3. Ingresar credenciales de usuario de prueba
4. Verificar redirección exitosa al dashboard o tienda
5. Navegar a la sección "Tienda" o `/store`

**Resultado Esperado:**
- ✅ Usuario logueado exitosamente
- ✅ Página de tienda carga sin errores
- ✅ Productos visibles con imágenes, nombres, precios

**Criterios de Aceptación:**
- No hay errores en consola del navegador
- Productos se muestran correctamente formateados
- Precios corresponden al país del usuario (MXN por defecto)

---

### TEST 2: Incrementar Cantidad con Botón "+" ✅

**Objetivo:** Validar que el botón "+" incrementa el contador correctamente

**Pasos:**
1. Localizar cualquier tarjeta de producto en la tienda
2. Observar el contador inicial (debe ser 0)
3. Hacer clic en el botón "+" (color primario, redondeado)
4. Verificar que el contador incrementa a 1
5. Hacer clic nuevamente en "+"
6. Verificar que el contador incrementa a 2
7. Repetir hasta llegar a 5

**Resultado Esperado:**
- ✅ Contador incrementa con cada clic en "+"
- ✅ Número se actualiza visualmente en tiempo real
- ✅ No hay errores en consola

**Criterios de Aceptación:**
- Contador muestra el número correcto
- Animación/transición es fluida
- No hay delay excesivo (< 200ms)

---

### TEST 3: Decrementar Cantidad con Botón "-" ✅

**Objetivo:** Validar que el botón "-" decrementa el contador correctamente

**Pasos:**
1. Usando el mismo producto del TEST 2 (contador en 5)
2. Hacer clic en el botón "-" (color secundario, redondeado)
3. Verificar que el contador decrementa a 4
4. Continuar haciendo clic en "-" hasta llegar a 0
5. Intentar hacer clic en "-" cuando el contador está en 0

**Resultado Esperado:**
- ✅ Contador decrementa con cada clic en "-"
- ✅ Contador NO va por debajo de 0
- ✅ Botón "-" no genera errores cuando contador está en 0

**Criterios de Aceptación:**
- Contador nunca muestra números negativos
- Decrementar desde 0 no causa errores

---

### TEST 4: Agregar Producto al Carrito ✅

**Objetivo:** Validar que el botón "Agregar" añade productos al carrito sin errores

**Pasos:**
1. Incrementar contador de un producto a 3 usando botón "+"
2. Hacer clic en botón "Agregar" (color primario, texto blanco)
3. Observar consola del navegador para verificar sin errores
4. Verificar que el ícono del carrito en el header muestra badge con número
5. Verificar que el contador del producto se resetea a 0

**Resultado Esperado:**
- ✅ No aparece el error `AttributeError: 'CountProducts' object has no attribute 'user_id'`
- ✅ Badge del carrito muestra "3" (cantidad agregada)
- ✅ Contador del producto vuelve a 0
- ✅ No hay excepciones en Reflex Backend

**Criterios de Aceptación:**
- Sin errores de AttributeError
- Badge del carrito actualizado correctamente
- Producto se resetea después de agregar

---

### TEST 5: Agregar Múltiples Productos ✅

**Objetivo:** Validar que se pueden agregar diferentes productos al carrito

**Pasos:**
1. Agregar 2 unidades del Producto A
2. Verificar badge del carrito muestra "2"
3. Agregar 3 unidades del Producto B
4. Verificar badge del carrito muestra "5" (2+3)
5. Agregar 1 unidad del Producto C
6. Verificar badge del carrito muestra "6" (2+3+1)

**Resultado Esperado:**
- ✅ Badge del carrito suma correctamente todas las cantidades
- ✅ Cada producto se agrega independientemente
- ✅ No hay límite hasta 20 productos

**Criterios de Aceptación:**
- Total de productos en carrito = suma de todas las cantidades
- No hay interferencia entre productos diferentes

---

### TEST 6: Visualizar Carrito con Productos ✅

**Objetivo:** Validar que la página del carrito muestra los productos agregados

**Pasos:**
1. Con productos en el carrito (del TEST 5)
2. Hacer clic en el ícono del carrito en el header
3. Verificar redirección a página `/shopping_cart` o similar
4. Verificar que cada producto agregado se muestra en una tarjeta
5. Verificar que muestra: imagen, nombre, precio, cantidad, subtotal
6. Verificar subtotal del carrito (suma de subtotales de productos)
7. Verificar "Costo de Envío: $0.00" (recolección gratis)
8. Verificar "Total Final" = Subtotal + 0.00

**Resultado Esperado:**
- ✅ Todos los productos agregados se muestran
- ✅ Precios correctos según país (MXN)
- ✅ Subtotales calculados correctamente (precio × cantidad)
- ✅ Costo de envío = $0.00
- ✅ Total final correcto

**Criterios de Aceptación:**
- Producto A: 2 unidades × precio = subtotal correcto
- Producto B: 3 unidades × precio = subtotal correcto
- Producto C: 1 unidad × precio = subtotal correcto
- Subtotal del carrito = suma de subtotales
- Envío = $0.00 (NO $99.00)
- Total = Subtotal + 0.00

---

### TEST 7: Incrementar/Decrementar Desde el Carrito ✅

**Objetivo:** Validar botones + y - dentro de la página del carrito

**Pasos:**
1. En la página del carrito (`/shopping_cart`)
2. Localizar botones + y - en cada producto
3. Hacer clic en "+" del Producto A
4. Verificar que cantidad incrementa de 2 a 3
5. Verificar que subtotal se actualiza automáticamente
6. Verificar que total final se actualiza
7. Hacer clic en "-" del Producto A
8. Verificar que cantidad decrementa de 3 a 2
9. Verificar actualizaciones de subtotal y total

**Resultado Esperado:**
- ✅ Cantidad se actualiza en tiempo real
- ✅ Subtotal del producto se recalcula automáticamente
- ✅ Total del carrito se recalcula automáticamente
- ✅ Sin recargar la página

**Criterios de Aceptación:**
- Todos los cálculos son correctos
- No hay delay visible (< 300ms)
- No se requiere refrescar la página

---

### TEST 8: Eliminar Producto del Carrito ✅

**Objetivo:** Validar que se puede eliminar un producto completamente

**Pasos:**
1. En la página del carrito
2. Localizar botón "Eliminar" o ícono de basura en Producto C
3. Hacer clic en eliminar
4. Verificar que Producto C desaparece de la lista
5. Verificar que total del carrito se actualiza (resta subtotal de C)
6. Verificar que badge del carrito decrementa en 1

**Resultado Esperado:**
- ✅ Producto eliminado de la vista
- ✅ Totales actualizados correctamente
- ✅ Badge del carrito actualizado

**Criterios de Aceptación:**
- Producto removido completamente
- Sin errores al eliminar
- Otros productos no afectados

---

### TEST 9: Navegar a Método de Envío ✅

**Objetivo:** Validar que el flujo continúa hacia selección de envío

**Pasos:**
1. En la página del carrito
2. Hacer clic en botón "Continuar" o "Siguiente paso"
3. Verificar redirección a `/shipment_method`
4. Verificar que se muestran opciones de envío

**Resultado Esperado:**
- ✅ Redirección exitosa
- ✅ Página carga sin errores
- ✅ Opciones de envío visibles

---

### TEST 10: Validar Solo Recolección Disponible ✅

**Objetivo:** Verificar que solo la opción de recolección está habilitada

**Pasos:**
1. En la página `/shipment_method`
2. Verificar que "Envío a Domicilio" aparece DESHABILITADO
   - Debe tener apariencia "gris" o "disabled"
   - Debe mostrar texto "Temporalmente no disponible"
3. Verificar que "Recoger en CEDIS" aparece HABILITADO
   - Debe tener borde de color primario
   - Debe mostrar badge "DISPONIBLE"
   - Debe mostrar "GRATIS"
4. Verificar que NO se muestra sección de "Domicilios guardados"
5. Verificar que SÍ se muestra sección de "CEDIS disponibles"

**Resultado Esperado:**
- ✅ Envío a domicilio visualmente deshabilitado
- ✅ Solo recolección seleccionable
- ✅ Lista de CEDIS visible
- ✅ Costo = GRATIS

**Criterios de Aceptación:**
- No se puede seleccionar envío a domicilio
- Recolección es la única opción funcional
- UX clara sobre opciones disponibles

---

### TEST 11: Seleccionar CEDIS de Recolección ✅

**Objetivo:** Validar selección de centro de distribución

**Pasos:**
1. En la página de método de envío
2. Revisar lista de CEDIS disponibles
3. Hacer clic en un CEDIS (ej: "CEDIS Centro")
4. Verificar que se marca como seleccionado visualmente
5. Verificar que muestra dirección, horario, teléfono
6. Intentar seleccionar otro CEDIS
7. Verificar que solo uno puede estar seleccionado a la vez

**Resultado Esperado:**
- ✅ CEDIS se marca como seleccionado
- ✅ Información del CEDIS visible
- ✅ Solo un CEDIS seleccionado a la vez

**Criterios de Aceptación:**
- Radio button o indicador visual claro
- Información completa del CEDIS mostrada

---

### TEST 12: Continuar a Método de Pago ✅

**Objetivo:** Validar navegación hacia checkout final

**Pasos:**
1. Con un CEDIS seleccionado
2. Hacer clic en botón "Continuar" o "Siguiente"
3. Verificar redirección a `/payment` o página de pago
4. Verificar que carrito persiste (productos siguen ahí)
5. Verificar que muestra resumen de compra

**Resultado Esperado:**
- ✅ Redirección exitosa
- ✅ Página de pago carga correctamente
- ✅ Datos del carrito persistidos

---

### TEST 13: Verificar Resumen de Compra ✅

**Objetivo:** Validar que el resumen final es correcto

**Pasos:**
1. En la página de pago (`/payment`)
2. Verificar sección de resumen del carrito
3. Validar que muestra:
   - Lista de productos con cantidades
   - Subtotal de productos
   - Método de envío: "Recolección" o "CEDIS"
   - Costo de envío: $0.00
   - Puntos de volumen (PV) totales
   - Total final
4. Verificar que los cálculos coinciden con el carrito

**Resultado Esperado:**
- ✅ Todos los productos listados
- ✅ Subtotal correcto
- ✅ Envío = $0.00
- ✅ Total correcto
- ✅ PV totales correctos

**Criterios de Aceptación:**
- Cálculos matemáticamente precisos
- Información completa y clara

---

### TEST 14: Seleccionar Método de Pago ✅

**Objetivo:** Validar opciones de pago disponibles

**Pasos:**
1. En la página de pago
2. Verificar opciones de pago disponibles:
   - Saldo en billetera
   - Tarjeta de crédito/débito (Stripe)
3. Verificar que muestra saldo actual en billetera
4. Seleccionar "Saldo en billetera"
5. Verificar que se marca como seleccionado

**Resultado Esperado:**
- ✅ Opciones de pago claras
- ✅ Saldo en billetera visible
- ✅ Selección funcional

---

### TEST 15: Confirmar Compra (Sin Procesar Pago Real) ⚠️

**Objetivo:** Validar hasta antes de procesar pago real

**Pasos:**
1. Con método de pago seleccionado
2. Revisar botón "Confirmar Compra" o "Pagar Ahora"
3. Verificar que botón está habilitado
4. Verificar que muestra total a pagar
5. **NO hacer clic** (evitar procesar orden real en desarrollo)

**Resultado Esperado:**
- ✅ Botón de confirmación visible y habilitado
- ✅ Total mostrado correctamente
- ✅ Sin errores hasta este punto

**Criterios de Aceptación:**
- Todo el flujo hasta confirmación funciona sin errores
- UX clara y sin confusiones

---

## 📊 Matriz de Testing

| Test | Descripción | Status | Errores Encontrados | Notas |
|------|-------------|--------|---------------------|-------|
| TEST 1 | Login y Acceso a Tienda | ⏳ | - | - |
| TEST 2 | Botón "+" Incrementa | ⏳ | - | - |
| TEST 3 | Botón "-" Decrementa | ⏳ | - | - |
| TEST 4 | Agregar al Carrito | ⏳ | - | Crítico |
| TEST 5 | Múltiples Productos | ⏳ | - | - |
| TEST 6 | Visualizar Carrito | ⏳ | - | Validar cálculos |
| TEST 7 | +/- en Carrito | ⏳ | - | - |
| TEST 8 | Eliminar Producto | ⏳ | - | - |
| TEST 9 | Navegar a Envío | ⏳ | - | - |
| TEST 10 | Solo Recolección | ⏳ | - | Crítico |
| TEST 11 | Seleccionar CEDIS | ⏳ | - | - |
| TEST 12 | Continuar a Pago | ⏳ | - | - |
| TEST 13 | Resumen de Compra | ⏳ | - | Validar cálculos |
| TEST 14 | Método de Pago | ⏳ | - | - |
| TEST 15 | Confirmar (sin pagar) | ⏳ | - | No ejecutar pago |

**Leyenda:**
- ⏳ Pendiente
- ✅ Pasado
- ❌ Fallido
- ⚠️ Con observaciones

---

## 🐛 Checklist de Errores Conocidos

### Antes de los Arreglos:
- [x] ❌ `AttributeError: 'CountProducts' object has no attribute 'user_id'`
- [x] ❌ Botón "+" no incrementaba contador
- [x] ❌ Botón "Agregar" generaba exception
- [x] ❌ Costo de envío mostraba $99.00 en lugar de $0.00

### Después de los Arreglos:
- [ ] ✅ Sin AttributeError al agregar productos
- [ ] ✅ Botón "+" funciona correctamente
- [ ] ✅ Botón "-" funciona correctamente
- [ ] ✅ Botón "Agregar" funciona sin errores
- [ ] ✅ Costo de envío siempre $0.00
- [ ] ✅ Solo recolección disponible

---

## 🚀 Instrucciones de Ejecución

### 1. Iniciar Servidor:
```bash
cd /Users/bradrez/Documents/NNProtect_new_website
source nnprotect_backoffice/bin/activate
reflex run
```

### 2. Abrir Navegador:
- Desktop: Abrir Chrome DevTools → Toggle device toolbar (Cmd+Shift+M)
- Configurar viewport: iPhone 12 Pro (390 x 844)
- Mobile: Acceder desde dispositivo móvil a IP del Mac

### 3. Ejecutar Tests:
- Seguir cada test en orden
- Marcar status en la matriz
- Documentar errores encontrados con screenshots
- Validar en consola del navegador (no errores JavaScript)

### 4. Reportar Resultados:
- Completar matriz de testing
- Adjuntar screenshots de cada paso
- Documentar cualquier desviación del comportamiento esperado

---

## 📝 Notas Adicionales

### Casos Edge:
- **Límite de 20 productos:** Intentar agregar más de 20 productos totales
- **Producto sin stock:** (si aplica) Validar manejo de productos agotados
- **Usuario sin wallet:** Validar que checkout maneja ausencia de saldo

### Performance:
- **Tiempo de carga de tienda:** < 2 segundos
- **Respuesta de botones +/-:** < 200ms
- **Actualización de carrito:** < 300ms

### Accesibilidad:
- Todos los botones deben tener texto descriptivo
- Imágenes deben tener alt text
- Navegación por teclado debe funcionar

---

**Testing Owner:** Giovann (QA)  
**Fecha de Creación:** 2025-10-02  
**Última Actualización:** 2025-10-02  
**Status:** 📋 PLAN COMPLETO - LISTO PARA EJECUCIÓN
