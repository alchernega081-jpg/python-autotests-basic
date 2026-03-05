from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def run_script():
    options = Options()

    # Раскомментируйте для фонового режима
    options.add_argument("headless")

    # Автоматическая установка GeckoDriver (для Firefox)
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("https://skillbox.ru")
        print(f"Заголовок страницы: {driver.title}")
        input("Нажмите Enter для закрытия браузера...")
    finally:
        driver.quit()


if __name__ == '__main__':
    run_script()