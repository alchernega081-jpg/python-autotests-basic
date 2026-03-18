import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Настройка драйвера
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Шаг 1: Открыть страницу https://github.com/microsoft/vscode/issues
    driver.get("https://github.com/microsoft/vscode/issues")
    print("Страница открыта")

    time.sleep(2)

    # Шаг 2: Нажать на кнопку Author
    author_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//summary[contains(text(), 'Author')]"))
    )
    author_button.click()
    print("Кнопка 'Author' нажата")

    # Небольшая пауза
    time.sleep(1)

    # Шаг 3: Ввести в поиск имя bpasero
    author_search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Filter authors']"))
    )
    author_search.clear()
    author_search.send_keys("bpasero")
    print("Имя 'bpasero' введено в поиск авторов")

    # Небольшая пауза
    time.sleep(2)

    # Шаг 4: Выбрать в выпадающем списке элемент с названием "bpasero"
    author_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@class='SelectMenu-item' and contains(., 'bpasero')]"))
    )

    # Прокручиваем к элементу
    actions = ActionChains(driver)
    actions.move_to_element(author_option).perform()
    time.sleep(0.5)

    author_option.click()
    print("Элемент 'bpasero' выбран из выпадающего списка")

    # Небольшая пауза
    time.sleep(3)

    # Шаг 5: Остановить выполнение автотеста для визуальной проверки
    print("\n" + "=" * 50)
    print("ТЕСТ ОСТАНОВЛЕН ДЛЯ ВИЗУАЛЬНОЙ ПРОВЕРКИ")
    print("Проверьте, что все отображаемые задачи созданы пользователем 'bpasero'")
    print("=" * 50 + "\n")

    # Останавливаем для проверки
    input("Нажмите Enter для завершения теста...")

finally:
    # Закрываем браузер
    driver.quit()
    print("Браузер закрыт")