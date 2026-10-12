import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://qa-andrea-rivera.myshopify.com"


@pytest.fixture
def driver():
    """Abre Chrome sin autocompletado (interfiere con los campos de pago) y lo cierra al terminar."""
    options = Options()
    options.add_argument("--disable-features=AutofillServerCommunication")
    options.add_experimental_option("prefs", {
        "autofill.profile_enabled": False,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 15)


@pytest.fixture
def store_password():
    """La contraseña se lee de la variable de entorno STORE_PASSWORD para no dejarla en el código."""
    password = os.getenv("STORE_PASSWORD")
    if not password:
        pytest.skip("Falta la variable de entorno STORE_PASSWORD con la contraseña de la tienda")
    return password


@pytest.fixture
def store(store_password, driver, wait):
    """Entra a la tienda pasando la pantalla de contraseña de la tienda de desarrollo."""
    driver.get(BASE_URL)
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys(store_password, Keys.RETURN)
    wait.until(lambda d: "/password" not in d.current_url)
    return driver
