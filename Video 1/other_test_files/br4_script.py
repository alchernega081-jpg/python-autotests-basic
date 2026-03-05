from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def run_script():
    options = Options()

    # Для Selenium 4
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444',
        options=options
    )

    try:
        driver.get("https://skillbox.ru")
        print(f"Заголовок страницы: {driver.title}")
        input("Нажмите Enter для закрытия браузера...")
    finally:
        driver.quit()


if __name__ == '__main__':
    run_script()