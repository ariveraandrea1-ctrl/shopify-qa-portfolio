# Fase 2: Automatización de Pruebas

Este documento describe la fase de automatización del proyecto de QA en Shopify, construida sobre la base del plan de pruebas manual (ver `Plan_de_Pruebas_Shopify_Andrea_Rivera.md`).

## 1. Automatización de API con Postman

Se construyó una colección de Postman ("Shopify QA Automation") con 7 requests y ~17 assertions, cubriendo la Admin API de Shopify.

### Endpoints cubiertos

| # | Request | Método | Qué valida |
|---|---------|--------|------------|
| 1 | Get all products | GET | Estructura de datos, campos requeridos |
| 2 | Get single product | GET | Detalle de producto, formato de precio |
| 3 | Create test order | POST | Cálculo de subtotal (699.95 × 2 = 1,399.90) |
| 4 | Update inventory level | POST | Actualización de stock |
| 5 | Create order - invalid variant | POST | Caso negativo: error 422 con variant_id inexistente |
| 6 | Create order - out of stock | POST | **Hallazgo**: la API permite crear una orden aunque el inventario sea 0, incluso con `inventory_policy: "deny"` |
| 7 | Delete test order | DELETE | Limpieza de datos de prueba |

La colección exportada está disponible en [`Shopify-QA-Automation.postman_collection.json`](./Shopify-QA-Automation.postman_collection.json).

## 2. Automatización de UI con Selenium + Python

Se automatizaron los flujos principales del plan de pruebas manual usando Selenium WebDriver.

### Tests implementados

- **`test_search_product.py`** — Verifica que la búsqueda de "snowboard" devuelva resultados (13 encontrados)
- **`test_add_to_cart.py`** — Agrega un producto al carrito, incrementa la cantidad, y verifica que el subtotal calculado coincida (699.95 × 2 = 1,399.90)
- **`test_out_of_stock.py`** — Confirma que el botón "Agregar al carrito" esté deshabilitado para un producto sin stock
- **`test_checkout.py`** — Automatiza el flujo completo de checkout: datos de contacto, dirección de envío, selección de método de envío, y llegada a la pantalla de pago

### Hallazgos técnicos

**1. Inconsistencia API vs. UI en manejo de inventario**
La API Admin permite crear una orden con un producto sin stock (ver request #6 de Postman), mientras que la interfaz de usuario correctamente deshabilita el botón de compra en ese mismo escenario (ver `test_out_of_stock.py`). Esto sugiere que la validación de inventario se aplica solo a nivel de frontend/storefront, no en la API administrativa.

**2. Resistencia a la automatización en campos de pago (iframes)**
Los campos de tarjeta de crédito en el checkout (`Expiration date`, `Security code`) están anidados en iframes individuales con protecciones que impiden la interacción automatizada estándar de Selenium, incluso tras probar múltiples estrategias: `ActionChains`, escritura carácter por carácter, disparo manual de eventos DOM (`input`, `change`, `blur`), y deshabilitación del autocompletado de Chrome. El campo `Card number` sí se completa exitosamente; los otros dos fallan consistentemente con `element not interactable`.

Esto es consistente con medidas de seguridad PCI-compliance que Shopify aplica intencionalmente a estos campos sensibles, y se documenta aquí como una limitación técnica conocida — no como una prueba fallida.

## Stack utilizado

- **API testing**: Postman, JavaScript (pm.test assertions)
- **UI testing**: Python 3.14, Selenium 4.48.0
- **Entorno**: PyCharm, venv
