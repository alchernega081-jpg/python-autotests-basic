from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service


def run_script():
    # Создаем опции для Firefox
    options = FirefoxOptions()

    # Добавляем полезные опции (опционально)
    # options.add_argument("--headless")  # без GUI
    options.add_argument("--start-maximized")  # развернуть окно

    # Создаем сервис с указанием пути к geckodriver
    # Так как geckodriver в PATH, можно просто Service()
    service = Service()  # или Service(executable_path="geckodriver")

    # Создаем драйвер Firefox
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("https://skillbox.ru")
        print(f"Заголовок страницы: {driver.title}")
        print("Страница успешно загружена!")
        input("Нажмите Enter для закрытия браузера...")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()


if __name__ == '__main__':
    run_script()