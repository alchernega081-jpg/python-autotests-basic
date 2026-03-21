from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytest


@pytest.fixture
def set_up_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


class TestGitHubCommitGraph:
    def test_commit_graph_tooltip(self, set_up_browser):
        """Тест-кейс №5: Проверка тултипа на графике коммитов"""
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)
        actions = ActionChains(driver)

        # Шаг 1: Открыть страницу
        driver.get("https://github.com/microsoft/vscode/graphs/commit-activity")
        time.sleep(5)

        # Шаг 2: Ожидаем загрузку графика и находим столбцы
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg.highcharts-root")))
        time.sleep(2)

        # Находим все столбцы графика (точки данных)
        bars = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "rect.highcharts-point, .highcharts-point, [class*='highcharts-point']")
        ))
        print(f"Найдено столбцов: {len(bars)}")

        # Шаг 3: Навести мышку на первый столбец
        actions.move_to_element(bars[0]).perform()
        time.sleep(2)

        # Проверяем, что наведение выполнено успешно (тултип появился)
        tooltip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.highcharts-tooltip")))
        assert tooltip.is_displayed(), "Тултип не появился после наведения мыши"
        print("✅ Наведение на столбец выполнено успешно")

        pass