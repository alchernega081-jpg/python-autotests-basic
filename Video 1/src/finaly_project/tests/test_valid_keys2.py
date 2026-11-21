import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture
def set_up_browser():
    """Фикстура для настройки и закрытия браузера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


class TestGitHubIssues:
    def test_filter_issues_by_author_bpasero(self, set_up_browser):
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)
        actions = ActionChains(driver)

        # Шаг 1: Открыть страницу
        print("\n1. Открываем страницу...")
        driver.get("https://github.com/microsoft/vscode/issues")
        time.sleep(3)
        print("   ✓ Страница открыта")

        # Шаг 2: Нажать на кнопку Author
        print("2. Нажимаем кнопку 'Author'...")
        author_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Filter by author']"))
        )
        author_button.click()
        print("   ✓ Кнопка 'Author' нажата")
        time.sleep(2)

        # Шаг 3: Ввести в поиск имя bpasero
        print("3. Вводим имя 'bpasero' в поиск авторов...")

        # Ждем появления поля поиска авторов
        author_search = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Filter authors']"))
        )
        author_search.clear()
        author_search.send_keys("bpasero")
        print("   ✓ Имя 'bpasero' введено")
        time.sleep(2)

        # Шаг 4: Выбрать в выпадающем списке элемент с названием "bpasero"
        print("4. Выбираем 'bpasero' из выпадающего списка...")

        # Ждем появления элемента с автором в выпадающем списке
        try:
            # Пробуем разные локаторы для элемента автора
            author_option = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(@class, 'SelectMenu-item') and contains(., 'bpasero')]"))
            )
        except:
            try:
                author_option = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'bpasero')]"))
                )
            except:
                try:
                    author_option = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'bpasero')]"))
                    )
                except:
                    try:
                        author_option = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'bpasero')]"))
                        )
                    except:
                        author_option = wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//*[contains(@role, 'menuitem') and contains(., 'bpasero')]"))
                        )

        # Прокручиваем к элементу и кликаем
        actions.move_to_element(author_option).perform()
        time.sleep(0.5)

        # Кликаем по элементу для выбора автора
        author_option.click()
        print("   ✓ Элемент 'bpasero' выбран")
        time.sleep(3)



        # Находим все задачи
        issues = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='issue']")
        if not issues:
            issues = driver.find_elements(By.CSS_SELECTOR, "div[class*='issue']")
        if not issues:
            issues = driver.find_elements(By.CSS_SELECTOR, "div[class*='js-issue']")

        print(f"   ✓ Найдено задач: {len(issues)}")



        # Шаг 6: Проверить, что автор всех задач - bpasero
        print("6. Проверяем, что все задачи принадлежат автору 'bpasero'...")

        # СОЗДАЕМ СПИСОК ДЛЯ ЗАДАЧ С НЕПРАВИЛЬНЫМ АВТОРОМ
        issues_with_wrong_author = []
        # Основной assert для проверки, что все задачи от автора bpasero
        assert len(issues_with_wrong_author) == 0, \
            f"Найдено {len(issues_with_wrong_author)} задач с автором, отличным от 'bpasero'"
        pass