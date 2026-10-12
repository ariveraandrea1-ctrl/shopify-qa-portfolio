from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conftest import BASE_URL

PRODUCT_URL = f"{BASE_URL}/products/the-out-of-stock-snowboard"


def test_out_of_stock_button_disabled(store, wait):
    """La tienda no deja comprar un producto sin inventario.

    Contrasta con la Admin API, que sí permite crear el pedido (ver la colección de Postman).
    """
    store.get(PRODUCT_URL)
    add_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name='add']")))

    assert add_button.get_attribute("disabled") is not None, "El botón debería estar deshabilitado"
    assert "Agotado" in add_button.text or "Sold out" in add_button.text, f"Texto inesperado: {add_button.text}"
