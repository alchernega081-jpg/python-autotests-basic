import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import pytest


@pytest.fixture
def set_up_browser():
    """Фикстура для настройки и закрытия браузера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


class TestGitHubAdvancedSearch: #Тест-кейс: Поиск репозиториев с количеством звёзд >20000
    def test_search_repositories_with_stars(self, set_up_browser):
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)

    # Шаг 1: Открыть страницу расширенного поиска
        print("\n1. Открываем страницу расширенного поиска...")
        driver.get("https://github.com/search/advanced")
        time.sleep(3)
        print("   ✓ Страница расширенного поиска открыта")

    # Шаг 2: В поле языка выбрать Python
        print("2. Выбираем язык Python...")
        language_dropdown = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='l']"))
        )
        Select(language_dropdown).select_by_visible_text("Python")
        print("   ✓ Выбран язык: Python")
        time.sleep(1)

        # Шаг 3: В поле количества звёзд выбрать >20000
        print("3. Указываем количество звёзд >20000...")
        stars_input = wait.until(
            EC.presence_of_element_located((By.ID, "search_stars"))
        )
        stars_input.clear()
        stars_input.send_keys(">20000")

        entered_value = stars_input.get_attribute("value")
        print(f"   ✓ Указано количество звёзд: >20000 (введено: {entered_value})")
        assert "20000" in entered_value, "Значение не введено корректно"
        time.sleep(1)

        # Шаг 4: В поле с названием файла выбрать environment.yml
        print("4. Указываем имя файла environment.yml...")
        filename_input = wait.until(
            EC.presence_of_element_located((By.ID, "search_filename"))
        )
        filename_input.clear()
        filename_input.send_keys("environment.yml")

        entered_filename = filename_input.get_attribute("value")
        print(f"   ✓ Указано имя файла: environment.yml (введено: {entered_filename})")
        assert "environment.yml" in entered_filename, "Имя файла не введено корректно"
        time.sleep(1)

        # Шаг 5: Нажать на кнопку поиска
        print("5. Нажимаем кнопку поиска...")
        search_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search')]"))
        )
        search_button.click()
        print("   ✓ Кнопка поиска нажата, выполняется переход к результатам")

        # Ждем загрузку результатов
        time.sleep(5)

        # Шаг 6: Проверить звёзды >20000
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']")))
        repos = driver.find_elements(By.CSS_SELECTOR, "div[class*='Box-row']")
        assert len(repos) > 0, "Результаты поиска не найдены"

        # Проверяем первый репозиторий
        stars_text = repos[0].find_element(By.CSS_SELECTOR, "a[href$='stargazers']").text
        stars_count = int(stars_text.replace(',', ''))
        assert stars_count > 20000, f"Количество звёзд: {stars_count} (должно быть >20000)"
        print(f"✅ Первый репозиторий имеет {stars_count} звёзд >20000")
        pass
