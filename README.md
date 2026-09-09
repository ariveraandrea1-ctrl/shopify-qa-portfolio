# Shopify QA Portfolio

Proyecto de portafolio de QA construido sobre una tienda de desarrollo gratuita de Shopify (`qa-andrea-rivera.myshopify.com`), cubriendo pruebas manuales y automatizadas sobre los módulos de catálogo, carrito de compras y checkout.

## Fase 1: Pruebas manuales

Se diseñó y ejecutó un plan de pruebas de 18 casos across 3 módulos (catálogo, carrito, checkout), con resultado de 18/18 casos exitosos y 3 hallazgos documentados (1 bug funcional, 2 observaciones de UX).

- 📄 [Plan de Pruebas](./Plan_de_Pruebas_Shopify_Andrea_Rivera.docx)
- 📄 [Reporte de Resultados](./Reporte_Resultados_Pruebas_Shopify_Andrea_Rivera.docx)

## Fase 2: Automatización de pruebas

Se automatizaron los flujos principales usando **Postman** (API) y **Selenium + Python** (UI), incluyendo casos positivos, negativos, y 2 hallazgos técnicos documentados (inconsistencia API vs. UI en manejo de inventario, y limitaciones de automatización en campos de pago con iframes).

- 📄 [Documentación completa de automatización](./AUTOMATION.md)
- 📦 [Colección de Postman](<./Shopify QA Automation.postman_collection.json>)
- 🐍 Scripts de Selenium: [`test_search_product.py`](./test_search_product.py) · [`test_add_to_cart.py`](./test_add_to_cart.py) · [`test_out_of_stock.py`](./test_out_of_stock.py) · [`test_checkout.py`](./test_checkout.py)
- 🎥 [Video demostrativo del checkout automatizado](https://www.loom.com/share/368cd916f4c6496ca2cf003000df0544)

## Stack utilizado

- **Pruebas manuales**: diseño de casos de prueba, ejecución, reporte de bugs
- **Automatización de API**: Postman, JavaScript (pm.test assertions)
- **Automatización de UI**: Python 3.14, Selenium 4.48.0
- **Entorno**: PyCharm, venv

## Autora

Andrea Rivera Amador — QA Engineer Jr.
[LinkedIn](https://linkedin.com/in/andrea-rivera-qa) · [GitHub](https://github.com/ariveraandrea1-ctrl)
