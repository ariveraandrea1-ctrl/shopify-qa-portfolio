import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from conftest import BASE_URL

PRODUCT_URL = f"{BASE_URL}/products/the-complete-snowboard"


def ir_al_pago(driver, wait):
    """Agrega un producto, llena contacto y envío, y deja el checkout en la pantalla de pago."""
    driver.get(PRODUCT_URL)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='add']"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "cart-drawer-items")))

    driver.get(f"{BASE_URL}/checkout")
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("qa.test@example.com")
    driver.find_element(By.NAME, "firstName").send_keys("Andrea")
    driver.find_element(By.NAME, "lastName").send_keys("Rivera")
    driver.find_element(By.NAME, "address1").send_keys("123 Main St")
    driver.find_element(By.NAME, "city").send_keys("Miami")
    Select(driver.find_element(By.NAME, "zone")).select_by_visible_text("Florida")
    driver.find_element(By.NAME, "postalCode").send_keys("33101")

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[contains(text(), 'Estándar') or contains(text(), 'Standard')]")
    )).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='Card number']")))


def llenar_campo_de_pago(driver, wait, iframe_title, valor):
    """Cada dato de la tarjeta vive en su propio iframe: entra, escribe y vuelve a la página."""
    iframe = driver.find_element(By.CSS_SELECTOR, f"iframe[title='{iframe_title}']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", iframe)
    driver.switch_to.frame(iframe)
    try:
        campo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input")))
        ActionChains(driver).move_to_element(campo).click().perform()
        campo.send_keys(valor)
    finally:
        driver.switch_to.default_content()


def test_checkout_hasta_el_pago(store, wait):
    """CH-01 y CH-02: el checkout acepta contacto y envío y llega a la pantalla de pago."""
    ir_al_pago(store, wait)
    llenar_campo_de_pago(store, wait, "Card number", "1")

    for titulo in ("Expiration date (MM / YY)", "Security code", "Name on card"):
        assert store.find_elements(By.CSS_SELECTOR, f"iframe[title='{titulo}']"), f"No aparece el campo {titulo}"


@pytest.mark.xfail(
    reason="Limitación conocida: fecha de vencimiento y CVV responden 'element not interactable' "
           "por la protección de Shopify sobre esos iframes (ver AUTOMATION.md)",
    strict=False,
)
def test_fecha_y_cvv_de_la_tarjeta(store, wait):
    ir_al_pago(store, wait)
    llenar_campo_de_pago(store, wait, "Expiration date (MM / YY)", "1230")
    llenar_campo_de_pago(store, wait, "Security code", "123")
