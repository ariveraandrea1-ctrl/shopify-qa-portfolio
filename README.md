# Shopify QA Portfolio

Este es un proyecto personal de QA que armé sobre una tienda de desarrollo gratuita de Shopify (`qa-andrea-rivera.myshopify.com`). La idea fue recorrer un ciclo de pruebas completo sobre una tienda real: primero diseñar y ejecutar las pruebas a mano, y después automatizar los flujos más importantes por API y por interfaz.

Me enfoqué en tres partes de la tienda: el catálogo y la búsqueda de productos, el carrito de compras y el checkout.

## Pruebas manuales

Escribí un plan de pruebas con 18 casos repartidos entre los tres módulos y los ejecuté sobre la tienda. Los 18 pasaron. En el camino encontré un bug funcional (Colombia no aparece como país de envío en la configuración de Markets) y dos detalles de experiencia de usuario: la búsqueda vacía no da ningún mensaje, y desde el checkout no hay un enlace para volver al carrito.

- [Plan de pruebas (PDF)](./Plan_de_Pruebas_Shopify_Andrea_Rivera.pdf)
- [Casos de prueba (Excel)](./Casos_de_Prueba_Shopify_Andrea_Rivera.xlsx)
- [Reporte de resultados (PDF)](./Reporte_Resultados_Pruebas_Shopify_Andrea_Rivera.pdf)

## Automatización

Con las pruebas manuales listas, pasé a automatizar. Por el lado de la API usé Postman contra la Admin API de Shopify, y por el lado de la interfaz usé Selenium con Python.

Lo más interesante que salió de esta fase fue una inconsistencia en el manejo de inventario: la tienda bloquea la compra de un producto agotado, pero la API sí deja crear el pedido. También me topé con que algunos campos de pago del checkout no se dejan automatizar con Selenium; lo explico en el documento de automatización.

- [Detalle de la automatización](./AUTOMATION.md)
- [Colección de Postman](<./Shopify QA Automation.postman_collection.json>)
- Scripts de Selenium: [`test_search_product.py`](./test_search_product.py), [`test_add_to_cart.py`](./test_add_to_cart.py), [`test_out_of_stock.py`](./test_out_of_stock.py), [`test_checkout.py`](./test_checkout.py)
- [Video del checkout automatizado](https://www.loom.com/share/368cd916f4c6496ca2cf003000df0544)

## Herramientas

Postman para las pruebas de API (con las aserciones escritas en JavaScript), Python 3.14 con Selenium 4.48.0 para la interfaz, y PyCharm con un entorno virtual para trabajar los scripts.

## Sobre mí

Soy Andrea Rivera Amador, QA Engineer Jr. en Medellín. Si quieres hablar del proyecto, me encuentras en [LinkedIn](https://linkedin.com/in/andrea-rivera-qa).
