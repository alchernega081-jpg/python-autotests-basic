from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def run_script():
    options = Options()
    options.set_capability("browserName", "chrome")

    # Можно также добавить опции для headless режима
    # options.add_argument("--headless")

    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        options=options
    )

    try:
        driver.get("https://skillbox.ru")
        #print(f"Заголовок страницы: {driver.title}")
    finally:
        driver.quit()


if __name__ == '__main__':
    run_script()