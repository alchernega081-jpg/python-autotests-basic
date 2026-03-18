import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# Настройка драйвера
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Шаг 1: Открыть страницу расширенного поиска
    driver.get("https://github.com/search/advanced")
    print("Страница расширенного поиска открыта")
    time.sleep(2)

    # Шаг 2: В поле языка выбрать Python
    language_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='l']"))
    )
    Select(language_dropdown).select_by_visible_text("Python")
    print("Выбран язык: Python")

    # Шаг 3: В поле количества звёзд выбрать >20000
    stars_input = driver.find_element(By.CSS_SELECTOR, "input[name='stars']")
    stars_input.clear()
    stars_input.send_keys(">20000")
    print("Указано количество звёзд: >20000")

    # Шаг 4: В поле с названием файла выбрать environment.yml
    filename_input = driver.find_element(By.CSS_SELECTOR, "input[name='filename']")
    filename_input.clear()
    filename_input.send_keys("environment.yml")
    print("Указано имя файла: environment.yml")

    # Шаг 5: Нажать на кнопку поиска
    search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    #search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
    search_button.click()
    print("Кнопка поиска нажата, выполняется переход к результатам")

    # Ждем загрузку
    time.sleep(5)

    # Шаг 6: Остановить выполнение для визуальной проверки
    print("\n" + "=" * 60)
    print("ТЕСТ ОСТАНОВЛЕН ДЛЯ ВИЗУАЛЬНОЙ ПРОВЕРКИ")
    print("Проверьте, что результаты поиска соответствуют критериям:")
    print("- Язык: Python")
    print("- Звёзд: >20000")
    print("- Файл: environment.yml")
    print("=" * 60 + "\n")

    input("Нажмите Enter для завершения теста и закрытия браузера...")

finally:
    driver.quit()
    print("Браузер закрыт")