from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import chromedriver_binary


def run_script():
    options = ChromeOptions()
    options.add_argument("--headless")  # Правильный способ включения headless режима
    # или для новых версий:
    # options.headless = True  # тоже работает в некоторых версиях

    driver = webdriver.Chrome(options=options)  # Используем webdriver.Chrome
    driver.get("https://skillbox.ru")
    print(driver.title)  # Добавим вывод заголовка для проверки
    driver.quit()


if __name__ == '__main__':
    run_script()