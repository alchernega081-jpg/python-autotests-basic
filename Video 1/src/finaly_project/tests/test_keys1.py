import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Шаг 1: Открыть страницу https://github.com/microsoft/vscode/issues
    driver.get("https://github.com/microsoft/vscode/issues")
    print("Страница открыта")

    time.sleep(2)

    # Шаг 2: Ввести в поиск фильтр "in:title"
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Filter']"))
    )
    search_input.clear()
    search_input.send_keys("in:title")
    print("Фильтр 'in:title' введен")

    # Шаг 3: Ввести ключевое слово "bug"
    search_input.send_keys(" bug")  # добавляем пробел
    print("Ключевое слово 'bug' введено")

    # Шаг 4: Нажать Enter
    search_input.send_keys(Keys.RETURN)
    print("Нажат Enter, поиск выполняется")

    # Небольшая пауза для загрузки результатов
    time.sleep(3)

    # Шаг 5: Остановить выполнение автотеста для визуальной проверки
    print("\n" + "="*50)
    print("ТЕСТ ОСТАНОВЛЕН ДЛЯ ВИЗУАЛЬНОЙ ПРОВЕРКИ")
    print("Проверьте, что отображаются только задачи, содержащие слово 'bug' в заголовке")
    print("="*50 + "\n")

    input("Нажмите Enter для завершения теста...")

finally:
    driver.quit()
    print("Браузер закрыт")