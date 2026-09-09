from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_driver():
    options = Options()
    options.add_argument("--disable-features=AutofillServerCommunication")
    prefs = {
        "autofill.profile_enabled": False,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=options)


def login_to_store(driver):
    driver.get("https://qa-andrea-rivera.myshopify.com")
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys("yeipau", Keys.RETURN)
    time.sleep(4)


def fill_iframe_field(driver, iframe_title, value, wait):
    """Entra a un iframe por su title, llena un campo de pago, y regresa al contenido principal."""
    iframe = driver.find_element(By.CSS_SELECTOR, f"iframe[title='{iframe_title}']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", iframe)
    time.sleep(1)
    driver.switch_to.frame(iframe)
    time.sleep(1)

    field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
    actions = ActionChains(driver)
    actions.move_to_element(field).click().perform()
    time.sleep(0.3)

    for char in value:
        field.send_keys(char)
        time.sleep(0.15)

    time.sleep(0.3)
    driver.execute_script("""
        var el = arguments[0];
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.dispatchEvent(new Event('blur', { bubbles: true }));
    """, field)
    time.sleep(0.5)

    driver.switch_to.default_content()
    print(f"  ✓ Campo '{iframe_title}' llenado")


def test_checkout_flow():
    """
    Automatiza el flujo completo de checkout: contacto, dirección de envío,
    método de envío, y datos de pago (número, fecha, código de seguridad).
    """
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    try:
        login_to_store(driver)

        driver.get("https://qa-andrea-rivera.myshopify.com/products/the-complete-snowboard")
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "button[name='add']").click()
        time.sleep(2)

        driver.get("https://qa-andrea-rivera.myshopify.com/checkout")
        time.sleep(4)

        driver.find_element(By.ID, "email").send_keys("qa.test@example.com")
        driver.find_element(By.NAME, "firstName").send_keys("Andrea")
        driver.find_element(By.NAME, "lastName").send_keys("Rivera")
        driver.find_element(By.NAME, "address1").send_keys("123 Main St")
        driver.find_element(By.NAME, "city").send_keys("Miami")

        state_select = Select(driver.find_element(By.NAME, "zone"))
        state_select.select_by_visible_text("Florida")
        time.sleep(1)

        driver.find_element(By.NAME, "postalCode").send_keys("33101")
        time.sleep(3)

        print("✅ Formulario de envío completo, esperando cálculo de métodos de envío...")

        shipping_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Estándar') or contains(text(), 'Standard')]"))
        )
        shipping_option.click()
        time.sleep(4)

        print("✅ Método de envío seleccionado. Llenando datos de tarjeta...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='Card number']")))
        time.sleep(1)

        fill_iframe_field(driver, "Card number", "1", wait)
        fill_iframe_field(driver, "Expiration date (MM / YY)", "1230", wait)
        fill_iframe_field(driver, "Security code", "123", wait)
        time.sleep(2)

        print("✅ Datos de tarjeta ingresados correctamente. Checkout automatizado hasta el paso de pago completo.")

    except Exception as e:
        print(f"❌ Test falló: {e}")
        print("URL en el momento del error:", driver.current_url)

    finally:
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    test_checkout_flow()