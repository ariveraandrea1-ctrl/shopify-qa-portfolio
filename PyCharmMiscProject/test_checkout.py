from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login_to_store(driver):
    driver.get("https://qa-andrea-rivera.myshopify.com")
    time.sleep(2)
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("yeipau")
    password_field.send_keys(Keys.RETURN)
    time.sleep(4)


def test_checkout_flow_part1():
    driver = webdriver.Chrome()
    try:
        login_to_store(driver)

        # Ir al producto y agregar al carrito
        driver.get("https://qa-andrea-rivera.myshopify.com/products/the-complete-snowboard")
        time.sleep(2)
        add_button = driver.find_element(By.CSS_SELECTOR, "button[name='add']")
        add_button.click()
        time.sleep(2)

        # Ir directo al checkout
        driver.get("https://qa-andrea-rivera.myshopify.com/checkout")
        time.sleep(4)

        print("URL actual:", driver.current_url)
        print("Título actual:", driver.title)

        # Llenar email
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys("qa.test@example.com")
        time.sleep(1)

        print("✅ Email ingresado correctamente")

        # Llenar nombre y apellido
        # (vamos a inspeccionar estos también antes de continuar)

    except Exception as e:
        print(f"❌ Test falló: {e}")
        print("URL en el momento del error:", driver.current_url)

    finally:
        time.sleep(3)  # pausa para que puedas ver el resultado antes de que se cierre
        driver.quit()


if __name__ == "__main__":
    test_checkout_flow_part1()