# Automatización de pruebas

Esta es la segunda fase del proyecto. Partí del plan de pruebas manual y automaticé los flujos que más valía la pena repetir: primero por API con Postman y luego por interfaz con Selenium y Python.

## Pruebas de API con Postman

Creé una app personalizada en la tienda para tener acceso a la Admin API y armé una colección en Postman con 7 requests y unas 17 aserciones.

| # | Request | Método | Qué revisa |
|---|---------|--------|------------|
| 1 | Get all products | GET | Que la respuesta traiga la estructura y los campos esperados |
| 2 | Get single product | GET | El detalle del producto y el formato del precio |
| 3 | Create test order | POST | Que el subtotal se calcule bien (699.95 × 2 = 1,399.90) |
| 4 | Update inventory level | POST | Que el stock se actualice |
| 5 | Create order - invalid variant | POST | Caso negativo: con un variant_id que no existe, la API responde 422 |
| 6 | Create order - out of stock | POST | Hallazgo: la API crea el pedido aunque el inventario esté en 0, incluso con `inventory_policy: "deny"` |
| 7 | Delete test order | DELETE | Borra el pedido de prueba para no dejar datos sueltos |

La colección está en [`Shopify QA Automation.postman_collection.json`](./Shopify%20QA%20Automation.postman_collection.json) por si quieres importarla.

## Pruebas de interfaz con Selenium

La tienda de desarrollo tiene contraseña, así que cada test empieza con una función que entra a la tienda antes de hacer lo demás.

- `test_search_product.py` busca "snowboard" y comprueba que aparezcan resultados (salen 13).
- `test_add_to_cart.py` agrega un producto, sube la cantidad a 2 y revisa que el subtotal sea 1,399.90.
- `test_out_of_stock.py` entra a un producto sin inventario y confirma que el botón de compra esté deshabilitado y diga "Sold out".
- `test_checkout.py` recorre el checkout: datos de contacto, dirección, método de envío y llegada a la pantalla de pago.

En [este video](https://www.loom.com/share/368cd916f4c6496ca2cf003000df0544) se ve el checkout corriendo solo, desde que se abre Chrome hasta la pantalla de pago.

## Lo que encontré

**La API y la tienda no se ponen de acuerdo con el inventario.** Desde la tienda no se puede comprar un producto agotado, porque el botón aparece deshabilitado. Pero desde la Admin API sí se puede crear un pedido con ese mismo producto (request 6 de Postman). Todo indica que la validación de stock solo se aplica en la tienda y no en la API administrativa.

**Algunos campos de pago no se dejan automatizar.** Los datos de la tarjeta van cada uno dentro de su propio iframe. El número de tarjeta se llena sin problema, pero la fecha de vencimiento y el código de seguridad fallan siempre con `element not interactable`. Probé con ActionChains, escribiendo carácter por carácter, disparando los eventos del DOM a mano y desactivando el autocompletado de Chrome, y ninguna funcionó. Lo más probable es que sea una protección intencional de Shopify sobre esos campos, así que lo dejo registrado como una limitación conocida y no como una prueba fallida.

## Herramientas

Postman con aserciones en JavaScript para la API, Python 3.14 y Selenium 4.48.0 para la interfaz, y PyCharm con un entorno virtual.
