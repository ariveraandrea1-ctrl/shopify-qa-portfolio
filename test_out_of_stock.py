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


def test_out_of_stock_button_disabled():
    driver = webdriver.Chrome()
    try:
        login_to_store(driver)

        driver.get("https://qa-andrea-rivera.myshopify.com/products/the-out-of-stock-snowboard")
        time.sleep(2)

        add_button = driver.find_element(By.CSS_SELECTOR, "button[name='add']")

        is_disabled = add_button.get_attribute("disabled") is not None
        button_text = add_button.text

        print(f"Texto del botón: '{button_text}'")
        print(f"¿Está deshabilitado?: {is_disabled}")

        assert is_disabled, "El botón debería estar deshabilitado para un producto sin stock"
        assert "Agotado" in button_text or "Sold out" in button_text, f"Texto inesperado: {button_text}"

        print("✅ Test pasó: la UI bloquea correctamente la compra de un producto sin stock")
        print("📝 HALLAZGO: contrasta con la API Admin, que sí permite crear la orden sin validar stock (ver Postman)")

    except Exception as e:
        print(f"❌ Test falló: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_out_of_stock_button_disabled()