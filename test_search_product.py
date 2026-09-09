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


def test_search_snowboard():
    driver = webdriver.Chrome()
    try:
        login_to_store(driver)

        search_icon = driver.find_element(By.CSS_SELECTOR, "summary.header__icon--search")
        search_icon.click()
        time.sleep(1)

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("snowboard")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        results = driver.find_elements(By.CSS_SELECTOR, "li.grid__item")
        assert len(results) > 0, "No se encontraron resultados de búsqueda"
        print(f"✅ Test pasó: se encontraron {len(results)} resultados para 'snowboard'")

    except Exception as e:
        print(f"❌ Test falló: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_search_snowboard()