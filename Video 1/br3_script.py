from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions


def run_script():
    # Создаем опции для Chrome
    options = ChromeOptions()
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "latest")

    driver = Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        options=options  # Используем параметр options вместо desired_capabilities
    )

    driver.get("https://skillbox.ru")
    print("Страница загружена успешно!")
    driver.quit()


if __name__ == '__main__':
    run_script()
