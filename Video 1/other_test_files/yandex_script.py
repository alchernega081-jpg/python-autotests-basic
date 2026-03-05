from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
from selenium import webdriver

options = webdriver.ChromeOptions()

binary_yandex_driver_file = 'yandexdriver.exe'  # path to YandexDriver
yandex_browser_package_name = 'com.yandex.browser'  # Release version of Yandex.Browser

options.add_experimental_option('androidPackage', yandex_browser_package_name)
driver = webdriver.Chrome(binary_yandex_driver_file, options=options)
driver.get('https://yandex.ru')
driver.quit()


def run_script():
    options = Options()

    # Путь к исполняемому файлу Яндекс Браузера
    # Обычные пути установки:
    # Windows: C:\\Users\\ИМЯ_ПОЛЬЗОВАТЕЛЯ\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\browser.exe
    # Или: C:\\Program Files (x86)\\Yandex\\YandexBrowser\\Application\\browser.exe
    yandex_path = os.path.expandvars("/Users/aleksandrcernega/Downloads/Yandex.dmg")

    # Альтернативный путь, если браузер установлен в Program Files
    #if not os.path.exists(yandex_path):
        #yandex_path = r"C:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe"

    options.binary_location = yandex_path

    # Путь к YandexDriver (нужно скачать отдельно)
    print ("Скачать можно здесь: https://github.com/yandex/YandexDriver")
    yandex_driver_path = "/Users/aleksandrcernega/Downloads/Yandex.dmg"  # Укажите свой путь

    #service = Service(yandex_driver_path)

    # Альтернативный вариант: если YandexDriver добавлен в PATH
     #service = Service("yandexdriver.exe")

    #driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://skillbox.ru")
        print(f"Заголовок страницы: {driver.title}")
        print(f"Используемый браузер: Яндекс Браузер")
        input("Нажмите Enter для закрытия браузера...")
    finally:
        driver.quit()


if __name__ == '__main__':
    run_script()