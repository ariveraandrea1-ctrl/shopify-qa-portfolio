from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


def test_search_snowboard(store, wait):
    """CP-02: la búsqueda de un producto existente devuelve resultados."""
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "summary.header__icon--search"))).click()

    search_box = wait.until(EC.visibility_of_element_located((By.NAME, "q")))
    search_box.send_keys("snowboard", Keys.RETURN)

    results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.grid__item")))
    assert len(results) > 0, "No se encontraron resultados para 'snowboard'"
