import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Настройка драйвера
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Шаг 1: Открыть страницу с графиком коммитов
    driver.get("https://github.com/microsoft/vscode/graphs/commit-activity")
    print("Страница с графиком открыта")

    # Ждем загрузки графика.
    graph_background = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "rect.highcharts-background"))
    )
    print("График загружен (найден элемент rect.highcharts-background)")

    time.sleep(2)

    # Шаг 2: Навести мышку на график
    actions = ActionChains(driver)
    actions.move_to_element(graph_background).perform()
    print("Курсор мыши наведен на график (область rect.highcharts-background)")

    time.sleep(2)

    # Шаг 3: Проверка, что мышка навелась
    print("\n" + "="*60)
    print("ТЕСТ ОСТАНОВЛЕН ДЛЯ ВИЗУАЛЬНОЙ ПРОВЕРКИ")
    print("Проверьте, что курсор мыши наведен на график.")
    print("Признаки корректного наведения:")
    print("1. Появилась всплывающая подсказка (tooltip) с данными о коммитах")
    print("2. Возможно, подсветился конкретный столбец или точка на графике")
    print("3. Форма курсора могла измениться")
    print("\nТекущий URL: " + driver.current_url)
    print("="*60 + "\n")

    # Останавка выполнения
    input("Нажмите Enter для завершения теста и закрытия браузера...")

finally:
    driver.quit()
    print("Браузер закрыт")