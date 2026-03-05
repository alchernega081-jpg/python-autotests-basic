from selenium.webdriver import Remote
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def run_script():
    # Создаем опции для Firefox
    options = FirefoxOptions()
    options.set_capability("browserName", "firefox")
    options.set_capability("platformName", "ANY")

    # Подключаемся к Selenium Server
    driver = Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        options=options
    )

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