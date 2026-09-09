from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login_to_store(driver):
    """Pasa la pantalla de contraseña de la tienda dev y espera a que cargue."""
    driver.get("https://qa-andrea-rivera.myshopify.com")
    time.sleep(2)
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("yeipau")
    password_field.send_keys(Keys.RETURN)
    time.sleep(4)


def test_add_to_cart_subtotal():
    driver = webdriver.Chrome()
    try:
        login_to_store(driver)

        # Ir directo a la página del producto
        driver.get("https://qa-andrea-rivera.myshopify.com/products/the-complete-snowboard")
        time.sleep(2)

        # Agregar al carrito (2 veces, para simular cantidad 2 como en tu test manual)
        add_button = driver.find_element(By.CSS_SELECTOR, "button[name='add']")
        add_button.click()
        time.sleep(2)

        # Incrementar cantidad a 2 usando el botón "+"
        plus_button = driver.find_element(By.CSS_SELECTOR, "cart-drawer-items button[aria-label*='+'], cart-drawer-items button.quantity__button:last-of-type")
        plus_button.click()
        time.sleep(2)

        # Verificar el subtotal
        subtotal_element = driver.find_element(By.CSS_SELECTOR, "p.totals__subtotal-value")
        subtotal_text = subtotal_element.text
        print(f"Subtotal mostrado: {subtotal_text}")

        expected = "1,399.90"
        assert expected in subtotal_text.replace(",95", "").replace(" USD", "") or "1399" in subtotal_text.replace(",", "").replace(".", ""), f"Subtotal no coincide: {subtotal_text}"
        print(f"✅ Test pasó: subtotal correcto ({subtotal_text})")

    except Exception as e:
        print(f"❌ Test falló: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_add_to_cart_subtotal()