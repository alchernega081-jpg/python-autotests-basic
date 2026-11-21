import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pytest


@pytest.fixture
def set_up_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


class TestSkillboxFilters:
    def test_filter_courses_by_profession_duration_theme(self, set_up_browser): #Тест-кейс №4: Проверка фильтрации курсов
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)
        actions = ActionChains(driver)
        driver.get("https://skillbox.ru/code/")
        time.sleep(3)

        # Шаг 2: Выбрать вкладку "Профессия"
        print("\n2. Выбираем вкладку 'Профессия'...")
        profession_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH,
            "//button[contains(@class, 'programs-filter-desktop__tab')]//span[contains(@class, 'ui-tab__text') and contains(text(), 'Профессия')]"))
        )
        profession_tab.click()
        print("   ✓ Вкладка 'Профессия' выбрана")
        time.sleep(2)

        # Шаг 3: Выбрать длительность от 6 до 12 месяцев
        print("\n3. Выбираем длительность от 6 до 12 месяцев...")

        # Находим и открываем выпадающий список "Длительность" по кнопке с текстом
        duration_button = wait.until(
            EC.element_to_be_clickable((By.XPATH,
            "//button[contains(@class, 'ui-round-select__field')]//span[contains(text(), 'Длительность')]/ancestor::button"))
        )
        actions.move_to_element(duration_button).perform()
        time.sleep(0.5)
        duration_button.click()
        print("   ✓ Выпадающий список 'Длительность' открыт")
        time.sleep(1)

        # Выбираем диапазон "От 6 до 12 мес."
        duration_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'ui-round-select__item') and contains(text(), 'От 6 до 12 мес.')]"))
        )
        actions.move_to_element(duration_option).perform()
        time.sleep(0.5)
        duration_option.click()
        print("   ✓ Выбран диапазон 'От 6 до 12 мес.'")


        # Шаг 4: Выбрать тематику "Python"
        print("\n4. Выбираем тематику 'Python'...")

        # Находим и открываем выпадающий список "Тематика" (по классу и тексту)
        theme_button = wait.until(
            EC.element_to_be_clickable((By.XPATH,
            "//button[contains(@class, 'ui-round-select__field')]//span[contains(text(), 'Тематика')]/ancestor::button"))
        )
        actions.move_to_element(theme_button).perform()
        time.sleep(1)
        theme_button.click()
        print("   ✓ Выпадающий список 'Тематика' открыт")
        time.sleep(1)

        # Находим поле поиска и вводим "Python"
        search_input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.ui-round-select-popup__header input[placeholder='Поиск']"))
        )
        search_input.clear()
        search_input.send_keys("Python")
        print("   ✓ В поле поиска введено 'Python'")
        time.sleep(2)

        # Находим элемент "Python" в списке и кликаем по нему (чекбокс)
        python_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'ui-round-select__item') and text()='Python']"))
        )
        actions.move_to_element(python_option).perform()
        time.sleep(0.5)
        python_option.click()
        print("   ✓ Выбран чекбокс 'Python'")

        # Нажимаем кнопку "Применить"
        apply_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ui-round-select-popup__footer button.ui-button"))
        )
        apply_button.click()
        print("   ✓ Нажата кнопка 'Применить'")
        time.sleep(3)

        print("   ✓ Фильтр тематики применен")

        # Шаг 5: Получить все курсы на странице
        print("\n5. Получаем список курсов после фильтрации...")

        # Ждем загрузки карточек курсов
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='card'], div[class*='Card']"))
        )
        time.sleep(2)

        # Находим все карточки курсов
        courses = driver.find_elements(By.CSS_SELECTOR, "div[class*='card']")
        if not courses:
            courses = driver.find_elements(By.CSS_SELECTOR, "a[class*='course']")

        print(f"   ✓ Найдено курсов: {len(courses)}")
        assert len(courses) > 0, "Не найдено ни одного курса после фильтрации"

        # Шаг 6: Проверить, что курсы соответствуют выбранным фильтрам
        print("\n6. Проверяем соответствие курсов выбранным фильтрам...")
        print("   " + "=" * 65)

        invalid_courses = []

        for i, course in enumerate(courses[:10], 1):
            print(f"\n   Курс {i}:")

            # Получаем название курса
            try:
                title_element = course.find_element(By.CSS_SELECTOR, "h3, [class*='title']")
                title = title_element.text.strip()
                print(f"      📚 Название: {title[:60]}")
            except NoSuchElementException:
                title = "Не найден"
                print(f"      📚 Название: {title}")

        pass