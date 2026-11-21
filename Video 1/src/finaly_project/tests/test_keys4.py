import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Настройка драйвера
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Шаг 1: Открыть страницу каталога с профессиями
    driver.get("https://skillbox.ru/code/?type=profession")
    print("Шаг 1: Страница с профессиями открыта")
    time.sleep(3)

    # Шаг 2: Переход на вкладку "Профессия"
    print("Шаг 2: Фильтр по типу 'Профессия' активен (по URL)")

    # Шаг 3: Добавляем длительность 6-12 месяцев
    duration_url = "https://skillbox.ru/code/?type=profession&duration_min=6&duration_max=12"
    driver.get(duration_url)
    print("Шаг 3: Добавлен фильтр длительности (6-12 месяцев)")
    time.sleep(3)

    # Шаг 4: Открываем фильтр по тематике и выбираем "Python"
    print("Шаг 4: Начинаем выбор тематики 'Python'...")

    # 4.1: Находим и кликаем по кнопке "Тематика", чтобы открыть выпадающий список
    theme_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ui-round-select button.ui-round-select__field"))
    )
    # Прокручиваем к кнопке, открываем список
    actions = ActionChains(driver)
    actions.move_to_element(theme_button).perform()
    time.sleep(1)
    theme_button.click()
    print("  - Выпадающий список 'Тематика' открыт")
    time.sleep(1)  # Ждем анимацию открытия

    # 4.2: Ждем появления поля поиска внутри попапа и вводим "Python"
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.ui-round-select-popup__header input[placeholder='Поиск']"))
    )
    search_input.clear()
    search_input.send_keys("Python")
    print("  - В поле поиска введено 'Python'")
    time.sleep(1)

    # 4.3: Выбираем элемент "Python" из отфильтрованного списка
    python_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'ui-round-select__item') and text()='Python']"))
    )
    actions.move_to_element(python_option).perform()
    time.sleep(0.5)
    python_option.click()
    print("  - Выбрана тематика 'Python'")

    # 4.4: Нажимаем кнопку "Применить"
    apply_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ui-round-select-popup__footer button.ui-button"))
    )
    apply_button.click()
    print("  - Нажата кнопка 'Применить'")
    time.sleep(3)  # Ждем обновления результатов

    # Шаг 5: Остановка для визуальной проверки
    print("\n" + "=" * 70)
    print("ТЕСТ ОСТАНОВЛЕН ДЛЯ ВИЗУАЛЬНОЙ ПРОВЕРКИ")
    print("Проверьте, что на странице:")
    print("1. ✅ Отображаются только программы типа «Профессия».")
    print("2. ✅ Длительность программ — от 6 до 12 месяцев.")
    print("3. ✅ Тематика программ соответствует выбранной ('Python').")
    print("\nТекущий URL с фильтрами: " + driver.current_url)
    print("=" * 70 + "\n")

    input("Нажмите Enter для завершения теста и закрытия браузера...")

finally:
    driver.quit()
    print("Браузер закрыт")