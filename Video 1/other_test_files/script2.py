from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
import chromedriver_binary


def run_script():
   options = ChromeOptions()
   options.add_argument("--headless")  # Правильный способ включить headless режим
   # Для новых версий Chrome также может потребоваться:
   # options.add_argument("--headless=new")
   driver = Chrome(options=options)
   driver.get("https://skillbox.ru")
   print(driver.title)  # Добавьте для проверки, что скрипт работает
   driver.quit()

if __name__ == '__main__':
    run_script()