import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture
def set_up_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


class TestGitHubIssues:
    def test_search_issues_with_bug_in_title(self, set_up_browser):
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)
        actions = ActionChains(driver)

        # Открываем страницу
        print("\n1. Открываем страницу...")
        driver.get("https://github.com/microsoft/vscode/issues")
        time.sleep(2)

        # Находим поле поиска
        print("2. Находим поле поиска...")
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Search Issues']"))
        )
        print("   ✓ Поле поиска найдено")

        # Способ 1: Простой клик
        print("3. Кликаем по полю...")
        search_input.click()
        print("   ✓ Клик выполнен")
        time.sleep(0.5)


        # Очищаем поле
        print("4. Очищаем поле...")
        search_input.clear()
        time.sleep(0.5)


        # Вводим текст
        print("5. Вводим фильтр 'in:title bug'...")
        search_input.send_keys("in:title bug")
        time.sleep(0.5)

        # Проверяем введенный текст
        entered_text = search_input.get_attribute("value")
        print(f"   Введено: '{entered_text}'")

        # Нажимаем Enter
        print("6. Нажимаем Enter...")
        search_input.send_keys(Keys.RETURN)
        print("   ✓ Поиск выполнен")

        # Ждем результаты
        time.sleep(3)

        # Получаем заголовки задач
        print("7. Получаем список задач...")
        titles = driver.find_elements(By.CSS_SELECTOR, "a[data-hovercard-type='issue']")
        if not titles:
            titles = driver.find_elements(By.CSS_SELECTOR, ".js-issue-title")

        issue_titles = [title for title in titles if title.text and title.text.strip()]

        if issue_titles:
            print(f"   ✓ Найдено задач: {len(issue_titles)}")

            # Проверяем наличие слова bug
            issues_without_bug = []
            for title_element in issue_titles:
                if "bug" not in title_element.text.strip().lower():
                    issues_without_bug.append(title_element.text.strip())

            if len(issues_without_bug) == 0:
                print(f"\n✅ ТЕСТ ПРОЙДЕН! Все {len(issue_titles)} задач содержат слово 'bug'")
            else:
                print(f"\n❌ ТЕСТ НЕ ПРОЙДЕН! Найдено {len(issues_without_bug)} задач без слова 'bug'")

            assert len(issues_without_bug) == 0, f"Найдено задач без 'bug': {len(issues_without_bug)}"
        else:
            print("   ⚠ Задачи не найдены")
            assert False, "Задачи не найдены после поиска"
        pass