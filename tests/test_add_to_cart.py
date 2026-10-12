from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conftest import BASE_URL

PRODUCT_URL = f"{BASE_URL}/products/the-complete-snowboard"


def solo_digitos(texto):
    return "".join(c for c in texto if c.isdigit())


def test_add_to_cart_subtotal(store, wait):
    """CA-01 y CA-02: agregar un producto, subir la cantidad a 2 y revisar el subtotal (699.95 x 2 = 1,399.90)."""
    store.get(PRODUCT_URL)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='add']"))).click()

    plus_button = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "cart-drawer-items button[aria-label*='+'], cart-drawer-items button.quantity__button:last-of-type",
    )))
    plus_button.click()

    subtotal = (By.CSS_SELECTOR, "p.totals__subtotal-value")
    # El subtotal se actualiza después del clic, así que se espera a que muestre el valor esperado
    wait.until(lambda d: "139990" in solo_digitos(d.find_element(*subtotal).text))

    texto = store.find_element(*subtotal).text
    assert "139990" in solo_digitos(texto), f"Subtotal inesperado: {texto}"
